"""formalization-validate-revise — apply mechanical fixes driven by validator findings.

Paired with formalization-validate.py: that script finds structural-invariant
violations; this one applies per-invariant fixes. Loop is validator finds →
reviser fixes → validator re-runs between passes. Six passes in order:
body-uniqueness, declaration-label-mismatch, depends-agreement,
references-resolve, filename-label-mismatch, acyclic-depends (propose-only).

Usage:
    python scripts/formalization-validate-revise.py 34 [--dry-run|--apply]
                                                        [--rule RULE]
                                                        [--file FILE]
                                                        [--from-pass N]
                                                        [--to-pass N]
"""

import argparse
import difflib
import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from shared.common import invoke_claude_agent, find_asn


REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPT_DIR = REPO_ROOT / "prompts" / "shared" / "formalization" / "validate-revise"


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "formalization_validate",
        Path(__file__).resolve().parent / "formalization-validate.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


VALIDATOR = _load_validator()


PASSES = [
    {"rule": "body-uniqueness",            "mode": "apply",   "tools": "Read,Edit"},
    {"rule": "declaration-label-mismatch", "mode": "apply",   "tools": "Read,Edit"},
    {"rule": "depends-agreement",          "mode": "apply",   "tools": "Read,Edit"},
    {"rule": "references-resolve",         "mode": "apply",   "tools": "Read,Edit"},
    {"rule": "filename-label-mismatch",    "mode": "apply",   "tools": "Read,Edit,Grep,Bash"},
    {"rule": "acyclic-depends",            "mode": "propose", "tools": "Read"},
]


def run_validator(asn_label):
    claim_dir = VALIDATOR.formalization_dir(asn_label)
    pairs = VALIDATOR.load_pairs(claim_dir)
    findings = []
    findings.extend(VALIDATOR.check_file_pair_completeness(pairs))
    findings.extend(VALIDATOR.check_yaml_well_formed(pairs))
    findings.extend(VALIDATOR.check_filename_matches_label(pairs))
    findings.extend(VALIDATOR.check_depends_agreement(pairs))
    findings.extend(VALIDATOR.check_references_resolve(pairs))
    findings.extend(VALIDATOR.check_acyclic_dependency_graph(pairs))
    findings.extend(VALIDATOR.check_declaration_and_body_uniqueness(pairs))
    return findings


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


def build_yaml_bundle(rule, filename, pairs, claim_dir):
    """Return a markdown-formatted block of relevant yaml file contents, or ''.

    The reviser needs authoritative label/name data from yaml but must never
    edit yaml. Embedding yaml content in the prompt removes the guessing
    failure mode (name-hallucination) and narrows the reviser's surface.
    """
    stem = Path(filename).stem
    companion = pairs.get(stem, {}).get("yaml")

    labels_to_include = []
    if rule in ("declaration-label-mismatch", "filename-label-mismatch"):
        labels_to_include.append(stem)
    elif rule == "depends-agreement":
        labels_to_include.append(stem)
        if isinstance(companion, dict):
            for dep in (companion.get("depends") or []):
                for other_stem, entry in pairs.items():
                    data = entry.get("yaml")
                    if isinstance(data, dict) and data.get("label") == dep:
                        labels_to_include.append(other_stem)
                        break
    elif rule == "references-resolve":
        labels_to_include.append(stem)
        if isinstance(companion, dict):
            for dep in (companion.get("depends") or []):
                for other_stem, entry in pairs.items():
                    data = entry.get("yaml")
                    if isinstance(data, dict) and data.get("label") == dep:
                        labels_to_include.append(other_stem)
                        break
    else:
        return ""

    seen = set()
    blocks = []
    for s in labels_to_include:
        if s in seen:
            continue
        seen.add(s)
        yaml_path = claim_dir / f"{s}.yaml"
        if not yaml_path.exists():
            continue
        content = yaml_path.read_text().rstrip()
        blocks.append(f"### `{s}.yaml`\n\n```yaml\n{content}\n```")

    if not blocks:
        return ""
    return "\n\n".join(blocks)


def build_prompt(rule, file_path, findings, pairs, claim_dir):
    template_path = PROMPT_DIR / f"{rule}.md"
    if not template_path.exists():
        raise FileNotFoundError(f"missing prompt template: {template_path}")
    template = template_path.read_text()
    yaml_bundle = build_yaml_bundle(rule, Path(file_path).name, pairs, claim_dir)
    return (template
            .replace("{file_path}", str(file_path))
            .replace("{findings_list}", format_findings_list(findings))
            .replace("{yaml_bundle}", yaml_bundle))


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


def process_file_scratch(rule, tools, claim_dir, filename, findings, pairs):
    """Passes 1-4: copy target file to scratch, let Claude edit scratch, diff.

    Returns (diff_text, scratch_path).
    """
    real_path = claim_dir / filename
    before = real_path.read_text()

    scratch_dir = Path(tempfile.mkdtemp(prefix=f"validate-revise-{rule}-"))
    scratch_path = scratch_dir / filename
    shutil.copy2(real_path, scratch_path)

    prompt = build_prompt(rule, scratch_path, findings, pairs, claim_dir)
    print(f"    [{rule}] invoking reviser on {filename}...", flush=True)
    data, elapsed = invoke_claude_agent(
        prompt,
        model="opus",
        effort="max",
        tools=tools,
        max_turns=20,
        cwd=scratch_dir,
    )
    if data is None:
        print(f"    [{rule}] claude invocation failed for {filename}", file=sys.stderr)
        return None, scratch_path
    print(f"    [{rule}] done in {elapsed:.0f}s", flush=True)

    after = scratch_path.read_text()
    diff = unified_diff(before, after, filename)
    return diff, scratch_path


def process_propose(rule, tools, claim_dir, findings):
    """Pass 6: Claude reads, produces a proposal document; no file edits."""
    prompt_path = PROMPT_DIR / f"{rule}.md"
    template = prompt_path.read_text()
    findings_text = format_findings_list(findings)
    prompt = (template
              .replace("{findings_list}", findings_text)
              .replace("{claim_dir}", str(claim_dir))
              .replace("{yaml_bundle}", ""))
    print(f"    [{rule}] invoking proposer...", flush=True)
    data, elapsed = invoke_claude_agent(
        prompt,
        model="opus",
        effort="max",
        tools=tools,
        max_turns=10,
        cwd=claim_dir,
    )
    if data is None:
        return None
    print(f"    [{rule}] done in {elapsed:.0f}s", flush=True)
    return data.get("result", "")


def run_pass(pass_spec, asn_label, claim_dir, findings, dry_run,
             file_filter, *, scope_labels=None, commit=False,
             require_git_clean=True):
    rule = pass_spec["rule"]
    mode = pass_spec["mode"]
    tools = pass_spec["tools"]
    pairs = VALIDATOR.load_pairs(claim_dir)
    if scope_labels is not None:
        findings = filter_findings_by_scope(findings, scope_labels)
    print(f"\n=== Pass: {rule} ({mode}) ===")

    if mode == "propose":
        rule_findings = [f for f in findings if f["rule"] == rule]
        if file_filter:
            rule_findings = [f for f in rule_findings
                             if f.get("file") == file_filter or not f.get("file")]
        if not rule_findings:
            print(f"  no findings; skipping")
            return
        output = process_propose(rule, tools, claim_dir, rule_findings)
        if output:
            print("\n--- proposal ---")
            print(output)
            print("--- end proposal ---\n")
        return

    groups = group_findings_by_file(findings, rule)
    if file_filter:
        groups = {k: v for k, v in groups.items() if k == file_filter}
    if not groups:
        print(f"  no findings for this rule; skipping")
        return

    if require_git_clean:
        target_paths = [claim_dir / fn for fn in groups]
        dirty = git_clean_check(target_paths)
        if dirty:
            print(f"  uncommitted changes in target files; aborting pass:", file=sys.stderr)
            for d in dirty:
                print(f"    {d}", file=sys.stderr)
            return

    for filename, file_findings in sorted(groups.items()):
        print(f"\n  {filename} ({len(file_findings)} finding(s))")

        if mode == "apply" and rule == "filename-label-mismatch":
            if dry_run:
                print(f"    [SKIP] filename renames not supported in dry-run "
                      f"(would need lattice-wide reference scan). Run with --apply "
                      f"to execute, or propose manually.")
                continue
            print(f"    [filename-label-mismatch] in-place rename + reference update")
            file_path = claim_dir / filename
            prompt = build_prompt(rule, file_path, file_findings, pairs, claim_dir)
            data, elapsed = invoke_claude_agent(
                prompt, model="opus", effort="max",
                tools=tools, max_turns=30, cwd=REPO_ROOT,
            )
            if data is None:
                print(f"    claude invocation failed", file=sys.stderr)
                continue
            print(f"    done in {elapsed:.0f}s")
            subprocess.run(["git", "diff", "--cached", "--stat", "HEAD"],
                           cwd=REPO_ROOT)
            if commit:
                committed = commit_all_staged(
                    f"validate-revise(asn): {rule} on {filename}"
                )
                if committed:
                    print(f"    [committed] {filename}")
                else:
                    print(f"    [no changes to commit] {filename}")
            continue

        diff, scratch_path = process_file_scratch(
            rule, tools, claim_dir, filename, file_findings, pairs
        )
        if diff is None:
            continue

        if not diff:
            print(f"    [no change]")
            shutil.rmtree(scratch_path.parent, ignore_errors=True)
            continue

        print("\n--- proposed diff ---")
        print(diff)
        print("--- end diff ---\n")

        if not dry_run:
            real_path = claim_dir / filename
            shutil.copy2(scratch_path, real_path)
            print(f"    [APPLIED] {filename}")
            if commit:
                commit_file(
                    real_path,
                    f"validate-revise(asn): {rule} on {filename}",
                )

        shutil.rmtree(scratch_path.parent, ignore_errors=True)


def run_passes(asn_label, *, scope_labels=None, rules=None, mode="apply",
               commit=False, from_pass=1, to_pass=None, file_filter=None):
    """Programmatic entry: run validate-revise passes over an ASN.

    scope_labels: iterable of claim labels to restrict findings to; None = all.
    rules:        iterable of rule names to run; None = all passes in order.
    mode:         "apply" or "dry-run".
    commit:       if True, git-commit each applied file; skip git-clean precheck.
    from_pass:    1-indexed start pass (CLI compatibility).
    to_pass:      1-indexed end pass inclusive (CLI compatibility); None = len(PASSES).
    file_filter:  restrict to one filename (e.g., "T4.md"); None = all affected.

    Returns (before_count, after_count) — finding counts before and after the run.
    Counts are scoped via scope_labels when provided.
    """
    dry_run = (mode == "dry-run")
    if to_pass is None:
        to_pass = len(PASSES)

    claim_dir = VALIDATOR.formalization_dir(asn_label)
    if not claim_dir.exists():
        raise FileNotFoundError(f"No formalization directory: {claim_dir}")

    rule_filter = set(rules) if rules is not None else None
    scope = set(scope_labels) if scope_labels is not None else None

    selected_passes = []
    for i, p in enumerate(PASSES, start=1):
        if i < from_pass or i > to_pass:
            continue
        if rule_filter is not None and p["rule"] not in rule_filter:
            continue
        selected_passes.append((i, p))

    print(f"[VALIDATE-REVISE] {asn_label} ({'dry-run' if dry_run else 'APPLY'})")
    print(f"  claim dir: {claim_dir}")
    if scope is not None:
        print(f"  scope: {sorted(scope)}")

    if not selected_passes:
        print("  no passes selected")
        return (0, 0)

    baseline = run_validator(asn_label)
    before_count = len(filter_findings_by_scope(baseline, scope))
    print(f"\n  baseline: {before_count} finding(s) in scope")

    findings = baseline
    for i, p in selected_passes:
        print(f"\n----- Pass {i}/{len(PASSES)} -----")
        run_pass(p, asn_label, claim_dir, findings, dry_run, file_filter,
                 scope_labels=scope, commit=commit,
                 require_git_clean=not commit)
        findings = run_validator(asn_label)
        in_scope = len(filter_findings_by_scope(findings, scope))
        print(f"\n  after pass {i}: {in_scope} finding(s) remaining (in scope)")

    after_count = len(filter_findings_by_scope(findings, scope))
    print("\n[VALIDATE-REVISE] done")
    return (before_count, after_count)


def main():
    parser = argparse.ArgumentParser(
        description="Structural reviser for claim-file-contract invariants.")
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
