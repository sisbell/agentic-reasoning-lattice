"""Claim structural-rule-fix agent — refiner for validator findings.

Fires per-claim. One fire = run validator on the claim's directory,
walk the apply-mode passes in sequence, fix per-rule per-file via
the `fix_structural_rule` helper, apply diffs, emit retractions for
depends-agreement RETRACT decisions, commit per-fire. Each fire
brings one claim toward structural quiescence; the runner re-fires
until every claim in scope is clean.

This is the lifted form of the previous validate-revise orchestrator.
The multi-pass loop, scratch-dir / diff / apply machinery,
__decisions.json sidecar validation, and retraction emission all
live inside this agent. Acyclic-depends propose mode was retired
during the lift.
"""

from __future__ import annotations

import difflib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import emit_retraction
from lib.lattice.labels import build_cross_asn_label_index
from lib.protocols.febe.protocol import Session
from lib.protocols.febe.session import open_session
from lib.shared.git_ops import step_commit_asn
from lib.shared.paths import CLAIM_DIR, LATTICE

from .helpers import fix_structural_rule


VALID_ACTIONS = {"ADD", "RETRACT", "SKIP"}
MAX_REVISER_ATTEMPTS = 2

REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPTS_DIR = REPO_ROOT / "scripts"


class DecisionsCorruption(Exception):
    """Raised when the reviser's __decisions.json sidecar violates the contract.

    Distinguishes protocol corruption (must be surfaced loudly) from
    legitimate decline (all-SKIP decisions).
    """


# Apply-mode passes only. acyclic-depends propose mode retired in the lift.
PASSES = [
    {"rule": "body-uniqueness",            "tools": "Read,Edit"},
    {"rule": "declaration-label-mismatch", "tools": "Read,Edit"},
    {"rule": "declared-symbols-resolve",   "tools": "Read,Bash"},
    {"rule": "depends-agreement",          "tools": "Read,Edit"},
    {"rule": "references-resolve",         "tools": "Read,Edit"},
]


# ─── Validator integration ──────────────────────────────────────────


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "claim_validate", SCRIPTS_DIR / "claim-validate.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


VALIDATOR = _load_validator()


def run_validator(asn_label: str) -> list:
    claim_dir = CLAIM_DIR / asn_label
    pairs = VALIDATOR.load_pairs(claim_dir)
    return VALIDATOR.run_all_checks(pairs, claim_dir=claim_dir)


def _actionable_findings_for_claim(findings: list, claim_label: str) -> list:
    """Findings the agent should act on for this one claim.

    Excludes acyclic-depends (retired propose mode); restricts to
    findings whose file stem matches the claim label, and cycle-style
    findings (file=None) that mention the claim in their detail.
    """
    relevant = []
    for f in findings:
        if f["rule"] == "acyclic-depends":
            continue
        filename = f.get("file")
        if filename:
            if Path(filename).stem == claim_label:
                relevant.append(f)
        else:
            if claim_label in f.get("detail", ""):
                relevant.append(f)
    return relevant


# ─── File / git helpers ─────────────────────────────────────────────


def _md_counterpart(filename: str) -> str:
    """Map a yaml filename to its md counterpart; pass md filenames through."""
    if filename.endswith(".yaml"):
        return filename[:-5] + ".md"
    return filename


def _commit_file(path: Path, message: str) -> bool:
    """Stage a single file and commit. Returns True on success."""
    try:
        subprocess.run(
            ["git", "add", "--", str(path)],
            cwd=REPO_ROOT, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=REPO_ROOT, check=True, capture_output=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"    [commit failed] {e}", file=sys.stderr)
        return False


def _git_clean_check(files: list) -> list:
    """Return list of files with uncommitted changes."""
    dirty = []
    for path in files:
        result = subprocess.run(
            ["git", "diff", "--quiet", "HEAD", "--", str(path)],
            cwd=REPO_ROOT,
        )
        if result.returncode != 0:
            dirty.append(str(path))
    return dirty


def _unified_diff(before_text: str, after_text: str, path_label: str) -> str:
    return "".join(difflib.unified_diff(
        before_text.splitlines(keepends=True),
        after_text.splitlines(keepends=True),
        fromfile=f"a/{path_label}",
        tofile=f"b/{path_label}",
    ))


# ─── Finding grouping / metadata ────────────────────────────────────


def _group_findings_by_file(findings: list, rule: str) -> dict:
    """Group findings by the file that needs editing.

    For rules whose fix target is always the md (depends-agreement,
    references-resolve), yaml-side findings are routed to the md counterpart.
    """
    md_target_rules = {"depends-agreement", "references-resolve"}
    groups: dict = {}
    for f in findings:
        if f["rule"] != rule or not f["file"]:
            continue
        target = (
            _md_counterpart(f["file"])
            if rule in md_target_rules else f["file"]
        )
        groups.setdefault(target, []).append(f)
    return groups


def _build_metadata_bundle(rule, filename, claim_dir):
    """Return a markdown block of (label, name) pairs for the claim being
    fixed plus its dependencies (for depends-agreement / references-resolve), or ''.
    """
    stem = Path(filename).stem
    labels_to_include = [stem]
    lattice_root = Path(LATTICE).resolve()

    with open_session(LATTICE) as session:
        label_index = build_cross_asn_label_index(session.store)

        if rule in ("depends-agreement", "references-resolve"):
            md_rel = str(
                (claim_dir / f"{stem}.md").resolve().relative_to(lattice_root)
            )
            md_addr = session.get_addr_for_path(md_rel)
            if md_addr is not None:
                for link in session.active_links(
                    "citation.depends", from_set=[md_addr],
                ):
                    for cited_addr in link.to_set:
                        cited_path = session.get_path_for_addr(cited_addr)
                        if cited_path:
                            dep_stem = Path(cited_path).stem
                            if dep_stem not in labels_to_include:
                                labels_to_include.append(dep_stem)
        elif rule not in (
            "declaration-label-mismatch", "body-uniqueness",
            "declared-symbols-resolve",
        ):
            return ""

        rows = []
        seen = set()
        for label in labels_to_include:
            if label in seen:
                continue
            seen.add(label)
            md_addr = label_index.get(label)
            name = "(no substrate name link)"
            if md_addr is not None:
                name_links = session.active_links(
                    "name", from_set=[md_addr],
                )
                if name_links and name_links[0].to_set:
                    sidecar_addr = name_links[0].to_set[0]
                    sidecar_rel = session.get_path_for_addr(sidecar_addr)
                    if sidecar_rel:
                        full = lattice_root / sidecar_rel
                        if full.exists():
                            first = (
                                full.read_text().strip().split("\n", 1)[0].strip()
                            )
                            if first:
                                name = first
            rows.append(f"- `{label}` — {name}")

    if not rows:
        return ""
    return (
        "### Claim metadata (label · name from substrate)\n\n"
        + "\n".join(rows)
    )


# ─── Decisions sidecar ──────────────────────────────────────────────


_BULLET_LABEL_RE = re.compile(r"^\+\s*-\s+([A-Za-z][\w.-]*)\b")


def _added_bullet_labels(diff_text: str) -> set:
    """Extract labels from added bullets in a unified diff."""
    labels = set()
    for line in diff_text.splitlines():
        m = _BULLET_LABEL_RE.match(line)
        if m:
            labels.add(m.group(1))
    return labels


def _parse_decisions(scratch_dir, valid_labels, label_index, diff_text):
    """Read and validate `__decisions.json` from scratch_dir."""
    decisions_path = Path(scratch_dir) / "__decisions.json"
    if not decisions_path.exists():
        raise DecisionsCorruption("__decisions.json not written by reviser")
    try:
        raw = json.loads(decisions_path.read_text())
    except json.JSONDecodeError as e:
        raise DecisionsCorruption(f"__decisions.json is not valid JSON: {e}")
    if not isinstance(raw, list):
        raise DecisionsCorruption("__decisions.json must be a JSON array")

    added_labels = _added_bullet_labels(diff_text)
    valid_labels = set(valid_labels)

    decisions = []
    for i, entry in enumerate(raw):
        if not isinstance(entry, dict):
            raise DecisionsCorruption(f"decision {i} is not an object")
        label = entry.get("label")
        action = entry.get("action")
        if not isinstance(label, str):
            raise DecisionsCorruption(f"decision {i} missing string `label`")
        if not isinstance(action, str) or action not in VALID_ACTIONS:
            raise DecisionsCorruption(
                f"decision for {label!r}: action {action!r} not in "
                f"{sorted(VALID_ACTIONS)}"
            )
        if label not in valid_labels:
            raise DecisionsCorruption(
                f"decision for {label!r}: label not in findings list"
            )
        if label not in label_index:
            raise DecisionsCorruption(
                f"decision for {label!r}: label not in lattice label_index"
            )
        if action == "ADD" and label not in added_labels:
            raise DecisionsCorruption(
                f"decision for {label!r}: action=ADD but no matching bullet "
                f"in diff"
            )
        decisions.append({
            "label": label,
            "action": action,
            "rationale": entry.get("rationale", ""),
        })
    return decisions


def _apply_retract_decisions(session, decisions, claim_path, label_index):
    """Emit a retraction for each RETRACT decision. Returns count emitted."""
    citing_addr = session.get_addr_for_path(claim_path)
    if citing_addr is None:
        raise DecisionsCorruption(
            f"claim {claim_path!r} not in substrate path map"
        )
    emitted = 0
    for d in decisions:
        if d["action"] != "RETRACT":
            continue
        cited_addr = label_index.get(d["label"])
        if cited_addr is None:
            raise DecisionsCorruption(
                f"retracting {d['label']!r} failed: unknown label"
            )
        candidates = session.active_links(
            "citation.depends",
            from_set=[citing_addr], to_set=[cited_addr],
        )
        if not candidates:
            raise DecisionsCorruption(
                f"retracting {d['label']!r} failed: no active "
                f"citation.depends from {claim_path}"
            )
        emit_retraction(session.store, citing_addr, candidates[0].addr)
        emitted += 1
        if d["rationale"]:
            print(
                f"    [retract] {d['label']}: {d['rationale']}",
                file=sys.stderr,
            )
    return emitted


def _dump_failure_transcript(asn_label, filename, attempt, transcript, reason):
    """Write a corruption transcript to a lattice-local failures dir."""
    import time as _time
    safe_ts = _time.strftime("%Y%m%dT%H%M%SZ", _time.gmtime())
    out_dir = (
        LATTICE / "_store" / "_failures" / "validate-revise" / asn_label
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{filename}.{safe_ts}.attempt{attempt}.txt"
    body = (
        f"# Validate-revise corruption: {filename} (attempt {attempt})\n"
        f"# Reason: {reason}\n"
        f"# Timestamp: {safe_ts}\n"
        f"\n"
        f"--- BEGIN AGENT TRANSCRIPT ---\n"
        f"{transcript}\n"
        f"--- END AGENT TRANSCRIPT ---\n"
    )
    out_path.write_text(body)
    return out_path


# ─── Per-file scratch flow ──────────────────────────────────────────


def _process_file_scratch(rule, tools, claim_dir, filename, findings):
    """Apply mode: copy target file to scratch, dispatch agent, diff."""
    real_path = claim_dir / filename
    before = real_path.read_text()

    scratch_dir = Path(
        tempfile.mkdtemp(prefix=f"validate-revise-{rule}-")
    )
    scratch_path = scratch_dir / filename
    shutil.copy2(real_path, scratch_path)

    metadata_bundle = _build_metadata_bundle(rule, filename, claim_dir)

    print(f"    {filename}: invoking... ", end="", flush=True)
    result = fix_structural_rule(
        rule, scratch_path, findings, metadata_bundle, tools=tools,
    )
    if result.agent_failed:
        print(" → claude invocation failed", flush=True)
        return None, scratch_path, ""
    print(f"{result.elapsed_seconds:.0f}s", end="", flush=True)

    after = scratch_path.read_text()
    diff = _unified_diff(before, after, filename)
    return diff, scratch_path, result.transcript


# ─── Per-pass loop ──────────────────────────────────────────────────


def _run_pass(pass_spec, asn_label, claim_dir, findings,
              skip_pairs):
    """Run one rule pass on the claim. Returns the set of (filename, rule)
    declines accumulated by the agent producing no change."""
    rule = pass_spec["rule"]
    tools = pass_spec["tools"]
    declined = set()

    groups = _group_findings_by_file(findings, rule)
    skipped_set = {
        fn for fn in groups if (Path(fn).stem, rule) in skip_pairs
    }
    groups = {k: v for k, v in groups.items() if k not in skipped_set}

    for fn in sorted(skipped_set):
        print(f"    {fn}: skipped (declined earlier)")

    if not groups:
        return declined

    file_word = "file" if len(groups) == 1 else "files"
    print(f"  {rule}: {len(groups)} {file_word}")

    target_paths = [claim_dir / fn for fn in groups]
    dirty = _git_clean_check(target_paths)
    if dirty:
        print(
            "  uncommitted changes in target files; aborting pass:",
            file=sys.stderr,
        )
        for d in dirty:
            print(f"    {d}", file=sys.stderr)
        return declined

    if rule == "depends-agreement":
        with open_session(LATTICE) as session:
            label_index = build_cross_asn_label_index(session.store)
    else:
        label_index = None

    for filename, file_findings in sorted(groups.items()):
        diff = None
        scratch_path = None
        decisions = None
        cli_failed = False
        corrupted = False

        valid_labels = set()
        if rule == "depends-agreement":
            for f in file_findings:
                m = re.search(r"\[(.*)\]", f["detail"])
                if m:
                    for tok in m.group(1).split(","):
                        lbl = tok.strip().strip("'\"")
                        if lbl:
                            valid_labels.add(lbl)

        for attempt in range(1, MAX_REVISER_ATTEMPTS + 1):
            diff, scratch_path, transcript = _process_file_scratch(
                rule, tools, claim_dir, filename, file_findings,
            )
            if diff is None:
                cli_failed = True
                break
            if rule != "depends-agreement":
                break
            try:
                decisions = _parse_decisions(
                    scratch_path.parent, valid_labels, label_index, diff,
                )
                break
            except DecisionsCorruption as e:
                dump = _dump_failure_transcript(
                    asn_label, filename, attempt, transcript, str(e),
                )
                if attempt < MAX_REVISER_ATTEMPTS:
                    print(
                        f"\n    [retry {attempt}/{MAX_REVISER_ATTEMPTS}] "
                        f"{e}; transcript: {dump}", file=sys.stderr,
                    )
                    shutil.rmtree(scratch_path.parent, ignore_errors=True)
                    continue
                print(
                    f" → ERROR (depends-agreement): {filename}: {e}",
                    file=sys.stderr,
                )
                print(f"   transcript: {dump}", file=sys.stderr)
                shutil.rmtree(scratch_path.parent, ignore_errors=True)
                corrupted = True
                break

        if cli_failed or corrupted:
            continue

        retract_decisions = [
            d for d in (decisions or []) if d["action"] == "RETRACT"
        ]
        all_skip = (
            decisions is not None
            and decisions
            and all(d["action"] == "SKIP" for d in decisions)
        )

        if not diff and not retract_decisions:
            if all_skip:
                rationale_summary = "; ".join(
                    f"{d['label']}: {d['rationale']}" for d in decisions
                )
                print(f" → declined (all SKIP: {rationale_summary})")
            else:
                print(" → declined (no change)")
            declined.add((Path(filename).stem, rule))
            shutil.rmtree(scratch_path.parent, ignore_errors=True)
            continue

        real_path = claim_dir / filename
        if diff:
            shutil.copy2(scratch_path, real_path)

        retracted_count = 0
        if retract_decisions:
            real_claim_path = str(
                real_path.resolve().relative_to(LATTICE.resolve())
            )
            try:
                with open_session(LATTICE) as session:
                    retracted_count = _apply_retract_decisions(
                        session, retract_decisions, real_claim_path,
                        label_index,
                    )
            except DecisionsCorruption as e:
                print(
                    f" → ERROR (depends-agreement): {filename}: {e}",
                    file=sys.stderr,
                )
                shutil.rmtree(scratch_path.parent, ignore_errors=True)
                continue

        if diff:
            committed = _commit_file(
                real_path,
                f"validate-revise(asn): {rule} on {filename}",
            )
            status = "committed" if committed else "commit failed"
        else:
            status = "applied (no md change)"
        suffix = (
            f" + {retracted_count} retracted" if retracted_count else ""
        )
        print(f" → {status}{suffix}")

        shutil.rmtree(scratch_path.parent, ignore_errors=True)

    return declined


# ─── Agent class ────────────────────────────────────────────────────


class ClaimStructuralFixAgent(Agent):
    """One claim's structural quiescence work per fire.

    Runs the validator, walks the apply-mode passes in order, dispatches
    fix_structural_rule per (rule, file), applies diffs, emits retractions
    for depends-agreement RETRACT decisions, commits per-file. Returns
    AgentResult after all passes complete. The runner re-fires until
    is_claim_structurally_clean(claim_addr) flips True.
    """

    role: ClassVar[str] = "claim-structural-fix"

    def run(self, session: Session, claim_addr: Address) -> AgentResult:
        claim_rel = session.get_path_for_addr(claim_addr)
        if claim_rel is None:
            return AgentResult(success=False, detail="no-claim-path")

        m = re.search(r"(ASN-(\d{4}))/([^/]+)\.md$", claim_rel)
        if m is None:
            return AgentResult(success=False, detail="unparseable-claim-path")
        asn_label = m.group(1)
        asn_num = int(m.group(2))
        claim_label = m.group(3)

        claim_dir = CLAIM_DIR / asn_label
        if not claim_dir.exists():
            return AgentResult(success=False, detail="no-claim-dir")

        findings = run_validator(asn_label)
        relevant = _actionable_findings_for_claim(findings, claim_label)
        if not relevant:
            return AgentResult(
                success=True, detail="already-clean",
            )

        print(
            f"\n  [STRUCTURAL-FIX] {asn_label}/{claim_label} "
            f"{len(relevant)} actionable finding(s)",
            file=sys.stderr,
        )

        declined: set = set()
        for p in PASSES:
            pass_findings = run_validator(asn_label)
            pass_relevant = _actionable_findings_for_claim(
                pass_findings, claim_label,
            )
            pass_declined = _run_pass(
                p, asn_label, claim_dir, pass_relevant, skip_pairs=declined,
            )
            if pass_declined:
                declined |= pass_declined

        # Final commit hook for any uncommitted residue (per-rule edits
        # commit individually via _commit_file; this is the agent-fire
        # boundary marker).
        step_commit_asn(
            asn_num,
            f"claim-structural-fix(asn): {asn_label}/{claim_label}",
        )

        return AgentResult(
            success=True,
            detail=f"declined={len(declined)}",
        )
