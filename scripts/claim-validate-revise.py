"""claim-validate-revise — apply mechanical fixes driven by validator findings.

Paired with claim-validate.py: that script finds structural-invariant
violations; this one applies per-invariant fixes. Loop is validator finds →
reviser fixes → validator re-runs between passes. Six passes in order:
body-uniqueness, declaration-label-mismatch, depends-agreement,
references-resolve, acyclic-depends (propose-only).

Usage:
    python scripts/claim-validate-revise.py 34 [--dry-run|--apply]
                                                        [--rule RULE]
                                                        [--file FILE]
                                                        [--from-pass N]
                                                        [--to-pass N]
"""

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

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from shared.common import invoke_claude_agent, find_asn
from shared.paths import LATTICE
from store.populate import build_cross_asn_label_index
from store.retract import emit_retraction
from store.store import default_store


VALID_ACTIONS = {"ADD", "RETRACT", "SKIP"}
MAX_REVISER_ATTEMPTS = 2


class DecisionsCorruption(Exception):
    """Raised when the reviser's __decisions.json sidecar violates the contract.

    Distinguishes protocol corruption (must be surfaced loudly) from
    legitimate decline (all-SKIP decisions).
    """


REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPT_DIR = REPO_ROOT / "prompts" / "shared" / "claim-convergence" / "validate-revise"


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "claim_validate",
        Path(__file__).resolve().parent / "claim-validate.py",
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
        subprocess.run(["git", "add", "--", str(path)],
                       cwd=REPO_ROOT, check=True,
                       capture_output=True)
        subprocess.run(["git", "commit", "-m", message],
                       cwd=REPO_ROOT, check=True,
                       capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"    [commit failed] {e}", file=sys.stderr)
        return False


def commit_all_staged(message):
    """Stage all modifications (including already-staged renames via git mv)
    and commit. Returns True on success, False if nothing to commit."""
    # Check if there's anything to commit (staged or unstaged tracked changes).
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    if not status.stdout.strip():
        return False
    try:
        subprocess.run(["git", "add", "-u"],
                       cwd=REPO_ROOT, check=True,
                       capture_output=True)
        subprocess.run(["git", "commit", "-m", message],
                       cwd=REPO_ROOT, check=True,
                       capture_output=True)
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
        target = _md_counterpart(f["file"]) if rule in md_target_rules else f["file"]
        groups.setdefault(target, []).append(f)
    return groups


def format_findings_list(findings):
    lines = []
    for f in findings:
        loc = f" (line {f['line']})" if f["line"] else ""
        src = f" [{f['file']}]" if f.get("file") else ""
        lines.append(f"- {f['detail']}{src}{loc}")
    return "\n".join(lines)


def build_metadata_bundle(rule, filename, pairs, claim_dir):
    """Return a markdown block of (label, name) pairs for the claim being
    fixed plus its dependencies (for depends-agreement / references-resolve), or ''.

    Sources:
    - label = filename stem (the dictionary keys in pairs)
    - name = first line of the substrate `name` link's sibling doc
      (queried via active_links)

    The reviser uses this to write the correct `**<Label> (<Name>).**`
    declaration form and the `- <Label> (<Name>) — gloss` Depends entries.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
    from store.queries import active_links
    from store.populate import build_cross_asn_label_index
    from shared.paths import WORKSPACE

    stem = Path(filename).stem
    labels_to_include = [stem]

    workspace = Path(WORKSPACE).resolve()

    with default_store() as store:
        label_index = build_cross_asn_label_index(store=store)

        if rule in ("depends-agreement", "references-resolve"):
            md_rel = str(
                (claim_dir / f"{stem}.md").resolve().relative_to(workspace)
            )
            for link in active_links(store, "citation.depends", from_set=[md_rel]):
                if link["to_set"]:
                    dep_stem = Path(link["to_set"][0]).stem
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
            md_path = label_index.get(label)
            name = "(no substrate name link)"
            if md_path:
                name_links = active_links(store, "name", from_set=[md_path])
                if name_links and name_links[0]["to_set"]:
                    full = workspace / name_links[0]["to_set"][0]
                    if full.exists():
                        first = full.read_text().strip().split("\n", 1)[0].strip()
                        if first:
                            name = first
            rows.append(f"- `{label}` — {name}")

    if not rows:
        return ""
    return "### Claim metadata (label · name from substrate)\n\n" + "\n".join(rows)


def build_prompt(rule, file_path, findings, pairs, claim_dir):
    template_path = PROMPT_DIR / f"{rule}.md"
    if not template_path.exists():
        raise FileNotFoundError(f"missing prompt template: {template_path}")
    template = template_path.read_text()
    metadata_bundle = build_metadata_bundle(
        rule, Path(file_path).name, pairs, claim_dir,
    )
    return (template
            .replace("{file_path}", str(file_path))
            .replace("{findings_list}", format_findings_list(findings))
            .replace("{metadata_bundle}", metadata_bundle))


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
    """Extract labels from added bullets in a unified diff.

    Looks for lines starting with `+  - <label>` and returns the set of
    labels. Used to validate that an ADD decision has a corresponding
    edit in the diff.
    """
    labels = set()
    for line in diff_text.splitlines():
        m = _BULLET_LABEL_RE.match(line)
        if m:
            labels.add(m.group(1))
    return labels


def parse_decisions(scratch_dir, valid_labels, label_index, diff_text):
    """Read and validate `__decisions.json` from scratch_dir.

    Returns the list of validated decision dicts.
    Raises DecisionsCorruption with a specific reason on any violation.
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
                f"decision for {label!r}: action {action!r} not in {sorted(VALID_ACTIONS)}"
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
                f"decision for {label!r}: action=ADD but no matching bullet in diff"
            )
        decisions.append({
            "label": label,
            "action": action,
            "rationale": entry.get("rationale", ""),
        })
    return decisions


def apply_retract_decisions(store, decisions, claim_path, label_index):
    """Emit a retraction for each RETRACT decision. Returns count emitted.

    On the first emit_retraction failure (citation not found — substrate
    inconsistent with the validator's finding), re-raises as
    DecisionsCorruption so the caller surfaces it loudly.
    """
    emitted = 0
    for d in decisions:
        if d["action"] != "RETRACT":
            continue
        try:
            link_id, created = emit_retraction(
                store, claim_path, d["label"], label_index,
            )
        except (ValueError, KeyError) as e:
            raise DecisionsCorruption(
                f"retracting {d['label']!r} failed: {e}"
            )
        emitted += 1
        if d["rationale"]:
            print(f"    [retract] {d['label']}: {d['rationale']}", file=sys.stderr)
    return emitted


def _dump_failure_transcript(asn_label, filename, attempt, transcript, reason):
    """Write a corruption transcript to a lattice-local failures dir.

    Returns the dump path so callers can mention it in the user-visible
    error message. Path: lattices/<lattice>/_docuverse/_failures/validate-revise/
    <asn_label>/<filename>.<ts>.attempt<N>.txt (gitignored).
    """
    import time as _time
    safe_ts = _time.strftime("%Y%m%dT%H%M%SZ", _time.gmtime())
    out_dir = LATTICE / "_store" / "_failures" / "validate-revise" / asn_label
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
    """Passes 1-4: copy target file to scratch, let Claude edit scratch, diff.

    Returns (diff_text, scratch_path, transcript).
    transcript is data["result"] (agent's final text); empty string on
    CLI failure. Used for diagnostic dump on DecisionsCorruption.
    """
    real_path = claim_dir / filename
    before = real_path.read_text()

    scratch_dir = Path(tempfile.mkdtemp(prefix=f"validate-revise-{rule}-"))
    scratch_path = scratch_dir / filename
    shutil.copy2(real_path, scratch_path)

    prompt = build_prompt(rule, scratch_path, findings, pairs, claim_dir)
    print(f"    {filename}: invoking... ", end="", flush=True)
    data, elapsed = invoke_claude_agent(
        prompt,
        model="opus",
        effort="max",
        tools=tools,
        max_turns=20,
        cwd=scratch_dir,
    )
    if data is None:
        print(f" → claude invocation failed", flush=True)
        return None, scratch_path, ""
    print(f"{elapsed:.0f}s", end="", flush=True)

    after = scratch_path.read_text()
    diff = unified_diff(before, after, filename)
    transcript = data.get("result", "") or ""
    return diff, scratch_path, transcript


def process_propose(rule, tools, claim_dir, findings):
    """Pass 6: Claude reads, produces a proposal document; no file edits."""
    prompt_path = PROMPT_DIR / f"{rule}.md"
    template = prompt_path.read_text()
    findings_text = format_findings_list(findings)
    prompt = (template
              .replace("{findings_list}", findings_text)
              .replace("{claim_dir}", str(claim_dir))
              .replace("{metadata_bundle}", ""))
    print(f"    invoking proposer... ", end="", flush=True)
    data, elapsed = invoke_claude_agent(
        prompt,
        model="opus",
        effort="max",
        tools=tools,
        max_turns=10,
        cwd=claim_dir,
    )
    if data is None:
        print(f"failed", file=sys.stderr)
        return None
    print(f"{elapsed:.0f}s", flush=True)
    return data.get("result", "")


def run_pass(pass_spec, asn_label, claim_dir, findings, dry_run,
             file_filter, *, scope_labels=None, commit=False,
             require_git_clean=True, skip_pairs=None,
             pass_index=None, total_passes=None):
    """Run one pass. Returns a set of (filename, rule) pairs where the reviser
    produced no change — the gate uses this to avoid re-invoking on known
    declines in later iterations."""
    rule = pass_spec["rule"]
    mode = pass_spec["mode"]
    tools = pass_spec["tools"]
    pairs = VALIDATOR.load_pairs(claim_dir)
    skip_pairs = skip_pairs or set()
    declined = set()
    if scope_labels is not None:
        findings = filter_findings_by_scope(findings, scope_labels)

    index_prefix = (f"pass {pass_index}/{total_passes} "
                    if pass_index is not None and total_passes is not None
                    else "pass ")

    if mode == "propose":
        rule_findings = [f for f in findings if f["rule"] == rule]
        if file_filter:
            rule_findings = [f for f in rule_findings
                             if f.get("file") == file_filter or not f.get("file")]
        if not rule_findings:
            return declined
        print(f"  {index_prefix}{rule} (propose): "
              f"{len(rule_findings)} finding(s)")
        output = process_propose(rule, tools, claim_dir, rule_findings)
        if output:
            print("--- proposal ---")
            print(output)
            print("--- end proposal ---")
        return declined

    groups = group_findings_by_file(findings, rule)
    if file_filter:
        groups = {k: v for k, v in groups.items() if k == file_filter}
    skipped_set = {fn for fn in groups if (Path(fn).stem, rule) in skip_pairs}
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
            print(f"  uncommitted changes in target files; aborting pass:", file=sys.stderr)
            for d in dirty:
                print(f"    {d}", file=sys.stderr)
            return declined

    if rule == "depends-agreement":
        with default_store() as store:
            label_index = build_cross_asn_label_index(store=store)
    else:
        label_index = None

    for filename, file_findings in sorted(groups.items()):
        # Bounded retry: corruption may be a one-off LLM lapse. Retry once;
        # persistent corruption falls through to the error path with the
        # transcript dumped for diagnosis.
        diff = None
        scratch_path = None
        decisions = None
        cli_failed = False
        corrupted = False

        valid_labels = set()
        if rule == "depends-agreement":
            # Collect labels from finding detail (only_in_store format:
            # "in store citations but not in md Depends: ['X', 'Y']").
            for f in file_findings:
                m = re.search(r"\[(.*)\]", f["detail"])
                if m:
                    for tok in m.group(1).split(","):
                        lbl = tok.strip().strip("'\"")
                        if lbl:
                            valid_labels.add(lbl)

        for attempt in range(1, MAX_REVISER_ATTEMPTS + 1):
            diff, scratch_path, transcript = process_file_scratch(
                rule, tools, claim_dir, filename, file_findings, pairs
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
                    print(f"\n    [retry {attempt}/{MAX_REVISER_ATTEMPTS}] "
                          f"{e}; transcript: {dump}", file=sys.stderr)
                    shutil.rmtree(scratch_path.parent, ignore_errors=True)
                    continue
                print(f" → ERROR (depends-agreement): {filename}: {e}",
                      file=sys.stderr)
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
                print(f" → declined (no change)")
            declined.add((Path(filename).stem, rule))
            shutil.rmtree(scratch_path.parent, ignore_errors=True)
            continue

        if dry_run:
            if diff:
                print(f" → proposed diff:")
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
            real_claim_path = str(real_path.resolve().relative_to(REPO_ROOT.resolve()))
            try:
                with default_store() as store:
                    retracted_count = apply_retract_decisions(
                        store, retract_decisions, real_claim_path, label_index,
                    )
            except DecisionsCorruption as e:
                print(f" → ERROR (depends-agreement): {filename}: {e}",
                      file=sys.stderr)
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
        suffix = f" + {retracted_count} retracted" if retracted_count else ""
        print(f" → {status}{suffix}")

        shutil.rmtree(scratch_path.parent, ignore_errors=True)

    return declined


def run_passes(asn_label, *, scope_labels=None, rules=None, mode="apply",
               commit=False, from_pass=1, to_pass=None, file_filter=None,
               skip_pairs=None):
    """Programmatic entry: run validate-revise passes over an ASN.

    scope_labels: iterable of claim labels to restrict findings to; None = all.
    rules:        iterable of rule names to run; None = all passes in order.
    mode:         "apply" or "dry-run".
    commit:       if True, git-commit each applied file; skip git-clean precheck.
    from_pass:    1-indexed start pass (CLI compatibility).
    to_pass:      1-indexed end pass inclusive (CLI compatibility); None = len(PASSES).
    file_filter:  restrict to one filename (e.g., "T4.md"); None = all affected.

    skip_pairs:   set of (filename, rule) tuples the reviser declined on in a
                  prior call; run_pass skips matching groups. Newly-declined
                  pairs discovered during this call are unioned into the
                  returned set.

    Returns (before_count, after_count, declined) — finding counts before and
    after the run, plus the accumulated (filename, rule) declines. Counts are
    scoped via scope_labels when provided.
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
        print(f"[VALIDATE-REVISE] {asn_label} "
              f"({'dry-run' if dry_run else 'APPLY'}) — no passes selected")
        return (0, 0, declined)

    baseline = run_validator(asn_label)
    before_count = len(filter_findings_by_scope(baseline, scope))
    print(f"[VALIDATE-REVISE] {asn_label} "
          f"({'dry-run' if dry_run else 'APPLY'}) — "
          f"{before_count} finding(s) in scope")

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
        description="Structural reviser for claim-document-contract invariants.")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--rule", help="restrict to one rule")
    parser.add_argument("--file", help="restrict to one filename (e.g., T4.md)")
    parser.add_argument("--from-pass", type=int, default=1,
                        help="start at pass N (1-indexed)")
    parser.add_argument("--to-pass", type=int, default=len(PASSES),
                        help="stop after pass N (1-indexed, inclusive)")
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--dry-run", action="store_true", default=True,
                            help="preview changes; default")
    mode_group.add_argument("--apply", action="store_true",
                            help="apply changes to real files")
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


if __name__ == "__main__":
    sys.exit(main())
