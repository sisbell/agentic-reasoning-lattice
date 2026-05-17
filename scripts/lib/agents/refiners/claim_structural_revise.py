"""Claim structural-fix agent — refiner for substrate-resident violations.

Fires per-claim with unresolved `comment.violation` links. One fire =
read the open violations from substrate, walk the apply-mode passes
in rule order, fix per-rule per-file via the `fix_structural_rule`
helper, apply diffs, emit `resolution.<kind>` per closed comment,
emit retractions for depends-agreement RETRACT decisions, commit
per-fire. Each fire brings one claim toward structural quiescence;
the runner re-fires while unresolved violations remain.

The validator no longer runs inside the refiner — that's the audit
scout's job (lib/agents/scouts/claim_structural_audit/). The refiner
reads substrate findings the scout emitted (via comment.violation
links + per-finding doc bodies), groups them by rule and by file,
dispatches the existing per-rule fix helpers, and closes each
comment via resolution.

The multi-pass loop, scratch-dir / diff / apply machinery,
__decisions.json sidecar validation, and retraction emission all
live inside this agent. Acyclic-depends propose mode was retired
when the validator-driven version was lifted.
"""

from __future__ import annotations

import difflib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import ClassVar, List, NamedTuple, Optional

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import emit_resolution, emit_retraction
from lib.lattice.labels import (
    build_cross_asn_label_index,
    parse_claim_doc_path,
)
from lib.predicates import has_resolution
from lib.protocols.febe.protocol import Session
from lib.protocols.febe.session import open_session
from lib.shared.paths import LATTICE, WORKSPACE, prompt_path
from lib.shared.invoke_claude import invoke_claude_agent





# ─── LLM helper for per-rule fix ────────────────────────────────────


# Per-rule prompt templates resolve through prompt_path() so lattice
# overrides (prompts/<lattice>/agents/refiners/claim_structural_revise/)
# can shadow the shared defaults. The bare-rule subpath convention is
# `agents/refiners/claim_structural_revise/<rule>.md`.


class StructuralRuleFixResult(NamedTuple):
    """Apply-mode agent output."""
    transcript: str
    elapsed_seconds: float
    agent_failed: bool


def fix_structural_rule(
    rule: str,
    file_path: Path,
    findings: list,
    metadata_bundle: str,
    *,
    tools: str,
    model: str = "opus",
    effort: str = "max",
    max_turns: int = 20,
) -> StructuralRuleFixResult:
    """Apply mode: invoke Claude with Edit tools to fix a per-rule violation.

    Claude reads `findings` + `metadata_bundle` and edits `file_path`
    in place. The caller (orchestrator) is responsible for copying
    the real file to a scratch path before this call and diffing
    after.

    For depends-agreement specifically, Claude also writes a
    `__decisions.json` sidecar in `file_path.parent` describing
    ADD/RETRACT/SKIP decisions per label; that contract is checked
    by the orchestrator's `parse_decisions`.
    """
    prompt = _render_prompt(
        rule, file_path, findings, metadata_bundle,
    )
    response = invoke_claude_agent(
        prompt, model=model, effort=effort, tools=tools,
        max_turns=max_turns, cwd=file_path.parent,
    )
    if response.data is None:
        return StructuralRuleFixResult(
            transcript="", elapsed_seconds=response.elapsed, agent_failed=True,
        )
    return StructuralRuleFixResult(
        transcript=response.text,
        elapsed_seconds=response.elapsed,
        agent_failed=False,
    )


# ---------------------------------------------------------------------------
# Prompt rendering


def _read_template(rule: str) -> str:
    template_path = prompt_path(
        f"agents/refiners/claim_structural_revise/{rule}.md",
    )
    if not template_path.exists():
        raise FileNotFoundError(f"missing prompt template: {template_path}")
    return template_path.read_text()


def _format_findings(findings: List[dict]) -> str:
    lines = []
    for f in findings:
        loc = f" (line {f['line']})" if f["line"] else ""
        src = f" [{f['file']}]" if f.get("file") else ""
        lines.append(f"- {f['detail']}{src}{loc}")
    return "\n".join(lines)


def _render_prompt(
    rule: str, file_path: Path, findings: list, metadata_bundle: str,
) -> str:
    template = _read_template(rule)
    return (
        template
        .replace("{file_path}", str(file_path))
        .replace("{findings_list}", _format_findings(findings))
        .replace("{metadata_bundle}", metadata_bundle)
    )


VALID_ACTIONS = {"ADD", "RETRACT", "SKIP"}
MAX_REVISER_ATTEMPTS = 2


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


# ─── Substrate-driven finding reads ─────────────────────────────────


_RULE_HEADER_RE = re.compile(r"^# Structural Violation:\s*(.+)$", re.MULTILINE)
_FILE_FIELD_RE = re.compile(r"^\*\*File:\*\*\s*(.+)$", re.MULTILINE)
_LINE_FIELD_RE = re.compile(r"^\*\*Line:\*\*\s*(\d+)$", re.MULTILINE)
_DETAIL_BLOCK_RE = re.compile(r"##\s*Detail\s*\n+(.+?)(?=\n##|\Z)", re.DOTALL)


def _parse_violation_body(body: str) -> Optional[dict]:
    """Parse a per-violation finding doc body into a finding dict.

    Mirrors the format the audit scout emits in
    lib/agents/scouts/claim_structural_audit/agent.py:_render_violation_body.
    Returns None if the body doesn't match the expected shape.
    """
    rule_m = _RULE_HEADER_RE.search(body)
    if rule_m is None:
        return None
    rule = rule_m.group(1).strip()
    file_m = _FILE_FIELD_RE.search(body)
    file = file_m.group(1).strip() if file_m else None
    if file == "(unknown)":
        file = None
    line_m = _LINE_FIELD_RE.search(body)
    line = int(line_m.group(1)) if line_m else None
    detail_m = _DETAIL_BLOCK_RE.search(body)
    detail = detail_m.group(1).strip() if detail_m else ""
    return {"rule": rule, "file": file, "line": line, "detail": detail}


def _read_substrate_violations(
    session: Session, claim_addr: Address,
) -> List[dict]:
    """Walk active unresolved comment.violation links targeting the claim,
    parse each finding doc body, and return a list of finding dicts.

    Each dict has keys: rule, file, line, detail, comment_addr,
    finding_addr. The comment_addr is what `resolution.<kind>` will
    target on closure.
    """
    out: List[dict] = []
    for link in session.active_links(
        "comment.violation", to_set=[claim_addr],
    ):
        if not link.from_set:
            continue
        if has_resolution(session, link.addr):
            continue
        finding_addr = link.from_set[0]
        finding_rel = session.get_path_for_addr(finding_addr)
        if finding_rel is None:
            continue
        finding_full = WORKSPACE / finding_rel
        if not finding_full.exists():
            continue
        body = finding_full.read_text()
        parsed = _parse_violation_body(body)
        if parsed is None:
            continue
        parsed["comment_addr"] = link.addr
        parsed["finding_addr"] = finding_addr
        out.append(parsed)
    return out


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
            cwd=WORKSPACE, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=WORKSPACE, check=True, capture_output=True,
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
            cwd=WORKSPACE,
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
    lattice_root = Path(WORKSPACE).resolve()

    with open_session(LATTICE) as session:
        label_index = build_cross_asn_label_index(session.store)

        if rule in ("depends-agreement", "references-resolve"):
            from lib.predicates.versions import version_head
            md_rel = str(
                (claim_dir / f"{stem}.md").resolve().relative_to(lattice_root)
            )
            md_addr = session.get_addr_for_path(md_rel)
            if md_addr is not None:
                state = session.state
                # Walk from claim's head (post-edit citations are
                # there); cited targets may be version addresses, so
                # walk back to base for path lookup.
                md_head = version_head(session, md_addr)
                for link in session.active_links(
                    "citation.depends", from_set=[md_head],
                ):
                    for cited_addr in link.to_set:
                        base = cited_addr
                        while state.parent.get(base) is not None:
                            base = state.parent[base]
                        cited_path = session.get_path_for_addr(base)
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
    from lib.predicates.versions import version_head

    citing_addr = session.get_addr_for_path(claim_path)
    if citing_addr is None:
        raise DecisionsCorruption(
            f"claim {claim_path!r} not in substrate path map"
        )
    state = session.state

    def _base(addr):
        cur = addr
        while state.parent.get(cur) is not None:
            cur = state.parent[cur]
        return cur

    citing_head = version_head(session, citing_addr)
    emitted = 0
    for d in decisions:
        if d["action"] != "RETRACT":
            continue
        cited_addr = label_index.get(d["label"])
        if cited_addr is None:
            raise DecisionsCorruption(
                f"retracting {d['label']!r} failed: unknown label"
            )
        # Walk all citations from claim's head; match by cited base
        # identity (cited target may be a version address).
        candidates = []
        for link in session.active_links(
            "citation.depends", from_set=[citing_head],
        ):
            if any(_base(t) == cited_addr for t in link.to_set):
                candidates.append(link)
        if not candidates:
            raise DecisionsCorruption(
                f"retracting {d['label']!r} failed: no active "
                f"citation.depends from {claim_path}"
            )
        emit_retraction(session.store, citing_head, candidates[0].addr)
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


def _emit_resolutions_for_findings(
    session: Session, claim_addr: Address, findings: list, *, kind: str,
) -> int:
    """Emit `resolution.<kind>` per comment.violation in `findings`.

    `kind` is "edit" (fix applied) or "reject" (declined / not actionable).
    by_doc is the claim itself; no rationale doc is created — the closure
    fact is captured by the resolution link's tumbler addr + by_doc.
    Returns count of resolutions emitted.

    On `kind="edit"` with at least one resolution emitted, advance the
    claim's supersession chain via `register_version`. Mirrors the
    behavior of the LLM-driven refiner path (claim_revise → resolution.py
    on accept). Without this, downstream sidecar predicates
    (description_is_fresh, signature_is_fresh, references_is_fresh)
    would stay True after a structural-edit accept and the producers
    would fail to re-attest against the new prose.
    """
    n = 0
    for f in findings:
        comment_addr = f.get("comment_addr")
        if comment_addr is None:
            continue
        if has_resolution(session, comment_addr):
            continue
        emit_resolution(
            session.store, claim_addr, comment_addr, kind=kind,
        )
        n += 1
    if kind == "edit" and n > 0:
        session.register_version(claim_addr)
    return n


def _run_pass(
    session, pass_spec, asn_label, claim_dir, claim_addr, findings,
    skip_pairs,
):
    """Run one rule pass on the claim.

    `findings` is the list of finding dicts (substrate-sourced) carrying
    comment_addr per finding. After per-(file, rule) processing, emits
    `resolution.edit` per comment whose group's fix landed, or
    `resolution.reject` per comment whose group declined.

    Returns the set of (filename, rule) declines for in-fire skip
    tracking. Decline state across fires is captured by the
    resolution.reject links emitted here — the runner sees those
    comments as resolved and the predicate skips them on next fire.
    """
    rule = pass_spec["rule"]
    tools = pass_spec["tools"]
    declined = set()

    groups = _group_findings_by_file(findings, rule)
    skipped_set = {
        fn for fn in groups if (Path(fn).stem, rule) in skip_pairs
    }
    groups = {k: v for k, v in groups.items() if k not in skipped_set}

    for fn in sorted(skipped_set):
        print(f"    {fn}: skipped (declined earlier in fire)")

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
            n_rej = _emit_resolutions_for_findings(
                session, claim_addr, file_findings, kind="reject",
            )
            print(f"    resolution.reject × {n_rej}")
            shutil.rmtree(scratch_path.parent, ignore_errors=True)
            continue

        real_path = claim_dir / filename
        if diff:
            shutil.copy2(scratch_path, real_path)

        retracted_count = 0
        if retract_decisions:
            real_claim_path = str(
                real_path.resolve().relative_to(WORKSPACE.resolve())
            )
            try:
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
        n_edit = _emit_resolutions_for_findings(
            session, claim_addr, file_findings, kind="edit",
        )
        suffix_parts = [f"resolution.edit × {n_edit}"]
        if retracted_count:
            suffix_parts.append(f"{retracted_count} retracted")
        print(f" → {status} ({'; '.join(suffix_parts)})")

        shutil.rmtree(scratch_path.parent, ignore_errors=True)

    return declined


# ─── Agent class ────────────────────────────────────────────────────


class ClaimStructuralReviseAgent(Agent):
    """One claim's structural quiescence work per fire.

    Reads unresolved comment.violation findings from substrate (emitted
    by the structural-audit scout), walks the apply-mode passes in
    rule order, dispatches fix_structural_rule per (rule, file),
    applies diffs, emits resolution.<kind> per closed comment, emits
    retractions for depends-agreement RETRACT decisions, commits
    per-file. Each fire processes the substrate snapshot read at fire
    start; if rule-N fixes invalidate rule-(N+1) findings, the audit
    re-fires next runner pass and emits fresh substrate.

    No validator runs inside this agent — the structural-audit scout
    is the detector. The refiner is pure closure.
    """

    role: ClassVar[str] = "claim-structural-revise"
    node: ClassVar[str] = "1.3"

    def run(self, session: Session, claim_addr: Address) -> AgentResult:
        claim_rel = session.get_path_for_addr(claim_addr)
        if claim_rel is None:
            return AgentResult(success=False, detail="no-claim-path")

        parsed = parse_claim_doc_path(claim_rel)
        if parsed is None:
            return AgentResult(success=False, detail="unparseable-claim-path")
        asn_label, claim_label, asn_num = parsed

        claim_dir = self.claim_dir / asn_label
        if not claim_dir.exists():
            return AgentResult(success=False, detail="no-claim-dir")

        relevant = _read_substrate_violations(session, claim_addr)
        if not relevant:
            return AgentResult(
                success=True, detail="already-clean",
            )

        print(
            f"\n  [STRUCTURAL-FIX] {asn_label}/{claim_label} "
            f"{len(relevant)} unresolved violation(s)",
            file=sys.stderr,
        )

        declined: set = set()
        for p in PASSES:
            pass_relevant = [f for f in relevant if f["rule"] == p["rule"]]
            if not pass_relevant:
                continue
            pass_declined = _run_pass(
                session, p, asn_label, claim_dir, claim_addr,
                pass_relevant, skip_pairs=declined,
            )
            if pass_declined:
                declined |= pass_declined

        # Final commit hook — per-rule edits commit individually via
        # _commit_file; this is the agent-fire boundary marker. No-op
        # if every per-rule commit already landed.

        return AgentResult(
            success=True,
            detail=f"processed={len(relevant)} declined-this-fire={len(declined)}",
        )
