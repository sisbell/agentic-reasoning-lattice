"""Claim-validate-revise orchestrator — gate loop over structural-rule fixes.

Paired with the structural validator (`scripts/claim-validate.py`).
The validator finds violations of structural invariants; this
orchestrator dispatches the structural-rule-fix agent
(`lib/agents/structural_rule_fix/`) per rule, gathers metadata from
substrate, manages scratch directories, validates the agent's
__decisions.json sidecar (depends-agreement only), applies retractions,
and loops validate→revise→re-validate until clean or declined.

Two entry points:
- `run_passes(asn_label, *, scope_labels, rules, mode, ...)` — main
  orchestration entry; runs over selected passes/rules
- `main()` — CLI invoked from `scripts/claim-validate-revise.py`
"""

from __future__ import annotations

import argparse
import difflib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from lib.agents.structural_rule_fix import (
    fix_structural_rule,
    propose_structural_fix,
)
from lib.backend.emit import emit_retraction
from lib.protocols.febe.session import open_session
from lib.lattice.labels import build_cross_asn_label_index
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE


VALID_ACTIONS = {"ADD", "RETRACT", "SKIP"}
MAX_REVISER_ATTEMPTS = 2

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = REPO_ROOT / "scripts"


class DecisionsCorruption(Exception):
    """Raised when the reviser's __decisions.json sidecar violates the contract.

    Distinguishes protocol corruption (must be surfaced loudly) from
    legitimate decline (all-SKIP decisions).
    """


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "claim_validate", SCRIPTS_DIR / "claim-validate.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


VALIDATOR = _load_validator()


PASSES = [
    {"rule": "body-uniqueness",            "mode": "apply",   "tools": "Read,Edit"},
    {"rule": "declaration-label-mismatch", "mode": "apply",   "tools": "Read,Edit"},
    {"rule": "declared-symbols-resolve",   "mode": "apply",   "tools": "Read,Bash"},
    {"rule": "depends-agreement",          "mode": "apply",   "tools": "Read,Edit"},
    {"rule": "references-resolve",         "mode": "apply",   "tools": "Read,Edit"},
    {"rule": "acyclic-depends",            "mode": "propose", "tools": "Read"},
]


def run_validator(asn_label):
    claim_dir = VALIDATOR.claim_convergence_dir(asn_label)
    pairs = VALIDATOR.load_pairs(claim_dir)
    return VALIDATOR.run_all_checks(pairs, claim_dir=claim_dir)


def _md_counterpart(filename):
    """Map a yaml filename to its md counterpart; pass md filenames through."""
    if filename.endswith(".yaml"):
        return filename[:-5] + ".md"
    return filename


def filter_findings_by_scope(findings, scope_labels):
    """Restrict findings to those touching labels in scope_labels.

    A finding is in scope if:
      - its file's stem is in scope_labels, OR
      - it's a cycle finding (file=None) and a scope label appears in the detail.

    scope_labels=None passes everything through.
    """
    if scope_labels is None:
        return list(findings)
    relevant = []
    for f in findings:
        if f.get("file"):
            stem = Path(f["file"]).stem
            if stem in scope_labels:
                relevant.append(f)
        else:
            detail = f.get("detail", "")
            if any(lbl in detail for lbl in scope_labels):
                relevant.append(f)
    return relevant


def commit_file(path, message):
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


def commit_all_staged(message):
    """Stage all modifications and commit. Returns True on success, False if
    nothing to commit."""
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    if not status.stdout.strip():
        return False
    try:
        subprocess.run(
            ["git", "add", "-u"],
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


def group_findings_by_file(findings, rule):
    """Group findings by the file that needs editing.

    For rules whose fix target is always the md (depends-agreement,
    references-resolve), yaml-side findings are routed to the md counterpart.
    """
    md_target_rules = {"depends-agreement", "references-resolve"}
    groups = {}
    for f in findings:
        if f["rule"] != rule or not f["file"]:
            continue
        target = (
            _md_counterpart(f["file"])
            if rule in md_target_rules else f["file"]
        )
        groups.setdefault(target, []).append(f)
    return groups


def build_metadata_bundle(rule, filename, pairs, claim_dir):
    """Return a markdown block of (label, name) pairs for the claim being
    fixed plus its dependencies (for depends-agreement / references-resolve), or ''.

    Sources:
    - label = filename stem (the dictionary keys in pairs)
    - name = first line of the substrate `name` link's sibling doc

    The reviser uses this to write the correct `**<Label> (<Name>).**`
    declaration form and the `- <Label> (<Name>) — gloss` Depends entries.
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


def git_clean_check(files):
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


def unified_diff(before_text, after_text, path_label):
    return "".join(difflib.unified_diff(
        before_text.splitlines(keepends=True),
        after_text.splitlines(keepends=True),
        fromfile=f"a/{path_label}",
        tofile=f"b/{path_label}",
    ))


_BULLET_LABEL_RE = re.compile(r"^\+\s*-\s+([A-Za-z][\w.-]*)\b")


def _added_bullet_labels(diff_text):
    """Extract labels from added bullets in a unified diff."""
    labels = set()
    for line in diff_text.splitlines():
        m = _BULLET_LABEL_RE.match(line)
        if m:
            labels.add(m.group(1))
    return labels


def parse_decisions(scratch_dir, valid_labels, label_index, diff_text):
    """Read and validate `__decisions.json` from scratch_dir.

    Returns the list of validated decision dicts. Raises
    DecisionsCorruption with a specific reason on any violation.
    """
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


def apply_retract_decisions(session, decisions, claim_path, label_index):
    """Emit a retraction for each RETRACT decision. Returns count emitted.

    On any retraction failure (citation not found — substrate
    inconsistent with the validator's finding), re-raises as
    DecisionsCorruption so the caller surfaces it loudly.
    """
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


def process_file_scratch(rule, tools, claim_dir, filename, findings, pairs):
    """Apply mode: copy target file to scratch, dispatch agent, diff.

    Returns (diff_text, scratch_path, transcript). transcript is the
    agent's final text; empty string on agent failure. Used for
    diagnostic dump on DecisionsCorruption.
    """
    real_path = claim_dir / filename
    before = real_path.read_text()

    scratch_dir = Path(
        tempfile.mkdtemp(prefix=f"validate-revise-{rule}-")
    )
    scratch_path = scratch_dir / filename
    shutil.copy2(real_path, scratch_path)

    metadata_bundle = build_metadata_bundle(
        rule, filename, pairs, claim_dir,
    )

    print(f"    {filename}: invoking... ", end="", flush=True)
    result = fix_structural_rule(
        rule, scratch_path, findings, metadata_bundle, tools=tools,
    )
    if result.agent_failed:
        print(" → claude invocation failed", flush=True)
        return None, scratch_path, ""
    print(f"{result.elapsed_seconds:.0f}s", end="", flush=True)

    after = scratch_path.read_text()
    diff = unified_diff(before, after, filename)
    return diff, scratch_path, result.transcript


def process_propose(rule, tools, claim_dir, findings):
    """Propose mode: agent reads, returns proposal document; no edits."""
    print("    invoking proposer... ", end="", flush=True)
    output = propose_structural_fix(
        rule, findings, claim_dir, tools=tools,
    )
    if output is None:
        print("failed", file=sys.stderr)
        return None
    print("done", flush=True)
    return output


def run_pass(pass_spec, asn_label, claim_dir, findings, dry_run,
             file_filter, *, scope_labels=None, commit=False,
             require_git_clean=True, skip_pairs=None,
             pass_index=None, total_passes=None):
    """Run one pass. Returns a set of (filename, rule) pairs where the reviser
    produced no change — the gate uses this to avoid re-invoking on known
    declines in later iterations.
    """
    rule = pass_spec["rule"]
    mode = pass_spec["mode"]
    tools = pass_spec["tools"]
    pairs = VALIDATOR.load_pairs(claim_dir)
    skip_pairs = skip_pairs or set()
    declined = set()
    if scope_labels is not None:
        findings = filter_findings_by_scope(findings, scope_labels)

    index_prefix = (
        f"pass {pass_index}/{total_passes} "
        if pass_index is not None and total_passes is not None
        else "pass "
    )

    if mode == "propose":
        rule_findings = [f for f in findings if f["rule"] == rule]
        if file_filter:
            rule_findings = [
                f for f in rule_findings
                if f.get("file") == file_filter or not f.get("file")
            ]
        if not rule_findings:
            return declined
        print(
            f"  {index_prefix}{rule} (propose): "
            f"{len(rule_findings)} finding(s)"
        )
        output = process_propose(rule, tools, claim_dir, rule_findings)
        if output:
            print("--- proposal ---")
            print(output)
            print("--- end proposal ---")
        return declined

    groups = group_findings_by_file(findings, rule)
    if file_filter:
        groups = {k: v for k, v in groups.items() if k == file_filter}
    skipped_set = {
        fn for fn in groups if (Path(fn).stem, rule) in skip_pairs
    }
    skipped = sorted(skipped_set)
    groups = {k: v for k, v in groups.items() if k not in skipped_set}
    if not groups and not skipped:
        return declined

    file_word = "file" if len(groups) == 1 else "files"
    if groups:
        print(f"  {index_prefix}{rule}: {len(groups)} {file_word}")
    elif skipped:
        print(f"  {index_prefix}{rule}: all skipped (declined earlier)")

    for fn in skipped:
        print(f"    {fn}: skipped (declined earlier in gate)")

    if not groups:
        return declined

    if require_git_clean:
        target_paths = [claim_dir / fn for fn in groups]
        dirty = git_clean_check(target_paths)
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
            diff, scratch_path, transcript = process_file_scratch(
                rule, tools, claim_dir, filename, file_findings, pairs,
            )
            if diff is None:
                cli_failed = True
                break
            if rule != "depends-agreement":
                break
            try:
                decisions = parse_decisions(
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

        if cli_failed:
            continue
        if corrupted:
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

        if dry_run:
            if diff:
                print(" → proposed diff:")
                print(diff)
            if retract_decisions:
                labels = ", ".join(d["label"] for d in retract_decisions)
                print(f" → WOULD RETRACT: {labels}")
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
                    retracted_count = apply_retract_decisions(
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

        if commit and diff:
            committed = commit_file(
                real_path,
                f"validate-revise(asn): {rule} on {filename}",
            )
            status = "committed" if committed else "commit failed"
        elif diff:
            status = "applied (uncommitted)"
        else:
            status = "applied (no md change)"
        suffix = (
            f" + {retracted_count} retracted" if retracted_count else ""
        )
        print(f" → {status}{suffix}")

        shutil.rmtree(scratch_path.parent, ignore_errors=True)

    return declined


def run_passes(asn_label, *, scope_labels=None, rules=None, mode="apply",
               commit=False, from_pass=1, to_pass=None, file_filter=None,
               skip_pairs=None):
    """Programmatic entry: run validate-revise passes over an ASN.

    Returns (before_count, after_count, declined) — finding counts
    before/after the run, plus the accumulated (filename, rule) declines.
    Counts are scoped via scope_labels when provided.
    """
    dry_run = (mode == "dry-run")
    if to_pass is None:
        to_pass = len(PASSES)

    claim_dir = VALIDATOR.claim_convergence_dir(asn_label)
    if not claim_dir.exists():
        raise FileNotFoundError(f"No claim-convergence directory: {claim_dir}")

    rule_filter = set(rules) if rules is not None else None
    scope = set(scope_labels) if scope_labels is not None else None
    declined = set(skip_pairs) if skip_pairs else set()

    selected_passes = []
    for i, p in enumerate(PASSES, start=1):
        if i < from_pass or i > to_pass:
            continue
        if rule_filter is not None and p["rule"] not in rule_filter:
            continue
        selected_passes.append((i, p))

    if not selected_passes:
        print(
            f"[VALIDATE-REVISE] {asn_label} "
            f"({'dry-run' if dry_run else 'APPLY'}) — no passes selected"
        )
        return (0, 0, declined)

    baseline = run_validator(asn_label)
    before_count = len(filter_findings_by_scope(baseline, scope))
    print(
        f"[VALIDATE-REVISE] {asn_label} "
        f"({'dry-run' if dry_run else 'APPLY'}) — "
        f"{before_count} finding(s) in scope"
    )

    findings = baseline
    total = len(PASSES)
    for i, p in selected_passes:
        pass_declined = run_pass(
            p, asn_label, claim_dir, findings, dry_run, file_filter,
            scope_labels=scope, commit=commit,
            require_git_clean=not commit, skip_pairs=declined,
            pass_index=i, total_passes=total,
        )
        if pass_declined:
            declined |= pass_declined
        findings = run_validator(asn_label)

    after_count = len(filter_findings_by_scope(findings, scope))
    print(f"[VALIDATE-REVISE] done — {after_count} remaining")
    return (before_count, after_count, declined)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Structural reviser for claim-document-contract invariants."
        ),
    )
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--rule", help="restrict to one rule")
    parser.add_argument(
        "--file", help="restrict to one filename (e.g., T4.md)",
    )
    parser.add_argument(
        "--from-pass", type=int, default=1,
        help="start at pass N (1-indexed)",
    )
    parser.add_argument(
        "--to-pass", type=int, default=len(PASSES),
        help="stop after pass N (1-indexed, inclusive)",
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--dry-run", action="store_true", default=True,
        help="preview changes; default",
    )
    mode_group.add_argument(
        "--apply", action="store_true",
        help="apply changes to real files",
    )
    args = parser.parse_args()

    _, asn_label = find_asn(args.asn)
    if asn_label is None:
        print(f"ASN-{args.asn} not found", file=sys.stderr)
        return 2

    try:
        run_passes(
            asn_label,
            rules=[args.rule] if args.rule else None,
            mode="apply" if args.apply else "dry-run",
            commit=False,
            from_pass=args.from_pass,
            to_pass=args.to_pass,
            file_filter=args.file,
        )
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 2
    return 0
