"""
Regional-scale V-cycle operators: regional-review (one cone) and
regional-sweep (across all qualifying cones), plus cone detection
and assembly helpers.

A dependency cone is a claim (the apex) that sits atop many stable
dependencies and can't converge under per-finding revision. See
docs/patterns/dependency-cone.md for the pattern.

- detect_dependency_cone: reactive, from git history
- run_regional_review: focused review/revise loop on one cone
- run_regional_sweep: proactive bottom-up DAG walk, reviews all qualifying cones
"""

import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, FORMALIZATION_DIR, next_review_number
from lib.shared.common import (
    find_asn, build_label_index,
    step_commit_asn,
)
from lib.formalization.full_review.review import (
    run_review, extract_findings, filter_revise, parse_missing_references,
)


MAX_EXPANSIONS = 5
from lib.formalization.full_review.revise import revise
from lib.formalization.core.build_dependency_graph import generate_formalization_deps
from lib.formalization.core.topological_sort import topological_levels
from lib.store.store import Store
from lib.store.emit import emit_review, emit_findings
from lib.store.populate import build_cross_asn_label_index
from lib.store.queries import is_claim_converged, unresolved_revise_comments


def _retry_unresolved_revises(store, asn_num, claim_dir, scope_md_paths):
    """Re-feed open revise comments to the reviser at the top of a cycle.

    For each unresolved comment.revise targeting a scope path, fetch its
    finding text from the comment's source (the finding document under
    `_store/findings/...`) and call `revise()` again. The reviser closes
    via `decide.py accept` (with edit) or `decide.py reject` (with rationale).
    """
    for scope_path in scope_md_paths:
        if not scope_path:
            continue
        for c in unresolved_revise_comments(store, scope_path):
            if not c["from_set"]:
                continue
            finding_path = WORKSPACE / c["from_set"][0]
            if not finding_path.exists():
                continue
            finding_text = finding_path.read_text()
            findings = extract_findings(finding_text)
            if not findings:
                continue
            title = findings[0][0]
            target_path = c["to_set"][0] if c["to_set"] else None
            print(f"  [RETRY] re-feeding open comment {c['id']} ({title})",
                  file=sys.stderr)
            revise(asn_num, title, finding_text, claim_dir=claim_dir,
                   comment_id=c["id"], claim_path=target_path)


# End-of-cone compress pass — disabled 2026-04-22 pending re-evaluation
# under the Dijkstra-voice reviser. The generative reviser should not
# produce the meta-prose accumulation that compress was built to clean up.
# Flip to True to re-enable without touching anything else.
_COMPRESS_ENABLED = False


def detect_dependency_cone(asn_num, window=5, threshold=3):
    """Detect a dependency cone from git history.

    Scans the last `window` full-review commits for this ASN.
    If one claim has >= `threshold` touches while its YAML
    dependencies have <= 1 touch, returns (apex_label, dep_labels).
    Otherwise returns None.
    """
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        return None

    claim_dir = FORMALIZATION_DIR / asn_label
    rel_dir = claim_dir.relative_to(WORKSPACE)

    # Get last N review commits touching this ASN.
    # Match both grep prefixes (cross-review + full-review) so historical
    # commits remain findable across the prefix rename.
    # Include both path prefixes (new lattices/xanadu/formalization + legacy
    # vault/3-formalization) so pre-restructure history is findable too.
    legacy_rel_dir = Path("vault") / "3-formalization" / asn_label
    try:
        result = subprocess.run(
            ["git", "log", "-E", "--grep=cross-review|full-review",
             f"-{window}",
             "--format=%H", "--",
             str(rel_dir), str(legacy_rel_dir)],
            capture_output=True, text=True, cwd=str(WORKSPACE),
        )
    except Exception:
        return None

    commits = result.stdout.strip().split("\n")
    commits = [c for c in commits if c]

    if len(commits) < threshold:
        return None

    # Count claim file touches per commit
    touch_counts = {}  # label → count
    label_index = build_label_index(claim_dir)
    stem_to_label = {stem: lbl for lbl, stem in label_index.items()}

    for commit_hash in commits:
        try:
            result = subprocess.run(
                ["git", "diff-tree", "--no-commit-id", "--name-only", "-r",
                 commit_hash],
                capture_output=True, text=True, cwd=str(WORKSPACE),
            )
        except Exception:
            continue

        for line in result.stdout.strip().split("\n"):
            # Accept lines under either the current or the legacy formalization
            # directory so pre-restructure history is still counted.
            if not (line.startswith(str(rel_dir))
                    or line.startswith(str(legacy_rel_dir))):
                continue
            fname = Path(line).name
            # Skip reviews, structural files, non-claim files
            if "reviews/" in line or fname.startswith("_") or fname.startswith("."):
                continue
            stem = fname.replace(".md", "").replace(".yaml", "")
            label = stem_to_label.get(stem, stem)
            touch_counts[label] = touch_counts.get(label, 0) + 1

    if not touch_counts:
        return None

    # Find candidate apex: most-touched claim above threshold
    apex = max(touch_counts, key=touch_counts.get)
    if touch_counts[apex] < threshold:
        return None

    # Load apex dependencies (same-ASN only) from the substrate's citation links.
    asn_labels = set(label_index.keys())
    apex_path = str(
        (claim_dir / f"{label_index[apex]}.md").relative_to(WORKSPACE)
    )
    store = Store()
    try:
        cross_index = build_cross_asn_label_index()
        rev_index = {p: l for l, p in cross_index.items()}
        cites = store.find_links(from_set=[apex_path], type_set=["citation"])
        dep_labels = [
            rev_index[link["to_set"][0]]
            for link in cites
            if link["to_set"] and rev_index.get(link["to_set"][0]) in asn_labels
        ]
    finally:
        store.close()

    # Check if dependencies are stable relative to apex
    # Apex should have at least 2x the touches of any single dep
    apex_count = touch_counts[apex]
    max_dep_touches = max(
        (touch_counts.get(d, 0) for d in dep_labels), default=0
    )
    if max_dep_touches > apex_count // 2:
        return None  # Dependencies are also thrashing — not a cone

    print(f"  [CONE] Detected: {apex} ({touch_counts[apex]} touches, "
          f"{len(dep_labels)} stable deps)", file=sys.stderr)
    return (apex, dep_labels)


def assemble_cone(asn_label, apex_label, dep_labels):
    """Assemble just the cone claims for focused review.

    Returns concatenated text of apex + same-ASN dependency claims.
    """
    claim_dir = FORMALIZATION_DIR / asn_label
    label_index = build_label_index(claim_dir)
    parts = []

    # Include dependencies first (context), then apex
    for label in dep_labels + [apex_label]:
        stem = label_index.get(label)
        if stem is None:
            continue
        md_path = claim_dir / f"{stem}.md"
        if md_path.exists():
            parts.append(md_path.read_text().strip())

    return "\n\n---\n\n".join(parts)


def _extract_apex_history(asn_label, apex_label, max_reviews=5):
    """Extract recent review findings that mention the apex label."""
    review_dir = FORMALIZATION_DIR / asn_label / "reviews"
    if not review_dir.exists():
        return ""

    review_files = sorted(review_dir.glob("review-*.md"),
                          key=lambda f: int(re.search(r'\d+', f.stem).group()),
                          reverse=True)

    relevant = []
    for rf in review_files[:max_reviews]:
        text = rf.read_text()
        if apex_label in text:
            relevant.append(text.strip())

    if not relevant:
        return "(no recent findings)"

    return "\n\n---\n\n".join(reversed(relevant))


def run_regional_review(asn_num, apex_label, dep_labels, max_cycles=3,
                        dry_run=False, model="opus"):
    """Run a focused regional-scale review/revise loop on one dependency cone.

    Same structure as full-review but with narrower context:
    only the apex and its same-ASN dependencies.

    Returns "converged" or "not_converged".
    """
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        return "failed"

    claim_dir = FORMALIZATION_DIR / asn_label
    review_dir = claim_dir / "reviews"

    print(f"\n  [REGIONAL-REVIEW] {apex_label} + {len(dep_labels)} deps",
          file=sys.stderr)

    store = Store()
    label_index = build_cross_asn_label_index()

    # Collect cross-ASN deps for narrowed foundation loading.
    # Read from the substrate's citation links rather than YAML's depends.
    asn_labels = set(build_label_index(claim_dir).keys())
    all_cone_labels = [apex_label] + dep_labels
    rev_index = {p: l for l, p in label_index.items()}
    cross_asn_deps = []
    for label in all_cone_labels:
        from_path = label_index.get(label)
        if not from_path:
            continue
        for link in store.find_links(from_set=[from_path], type_set=["citation"]):
            if not link["to_set"]:
                continue
            dep_label = rev_index.get(link["to_set"][0])
            if (dep_label and dep_label not in asn_labels
                    and dep_label not in cross_asn_deps):
                cross_asn_deps.append(dep_label)

    print(f"  Foundation: {len(cross_asn_deps)} cross-ASN deps", file=sys.stderr)

    # Load review history for the apex
    history = _extract_apex_history(asn_label, apex_label)

    # Capture baseline SHA so the end-of-cone compress pass knows which
    # files changed during this cone.
    from lib.shared.common import git_head_sha
    baseline_sha = git_head_sha()

    start_time = time.time()
    previous_findings = history
    had_findings = False
    verdict = "CONVERGED"
    apex_md_path = label_index.get(apex_label)
    naturally_converged = False
    last_cycle_revise_count = -1
    final_review_path = None

    for cycle in range(1, max_cycles + 1):
        print(f"\n  [CYCLE {cycle}/{max_cycles}]", file=sys.stderr)

        # Retry pass: re-feed any open revise comments from prior cycles
        # or invocations to the reviser. Reviser closes via decide.py.
        if not dry_run:
            _retry_unresolved_revises(store, asn_num, claim_dir, [apex_md_path])

        from lib.formalization.gate import run_validate_gate
        scope = {apex_label} | set(dep_labels)
        gate_result = run_validate_gate(asn_label, scope_labels=scope)
        if gate_result != "clean":
            print(f"  [GATE] halted — structural violations remain in cone "
                  f"({gate_result}); aborting regional-review",
                  file=sys.stderr)
            store.close()
            return "failed"

        # Review with lazy cone expansion: if the reviewer flags claim
        # labels it saw referenced but not shown, expand the cone to
        # include them and re-review. Bounded by MAX_EXPANSIONS. Only the
        # final stable review is saved and acted on.
        current_deps = list(dep_labels)
        expansion_round = 0
        while True:
            cone_content = assemble_cone(asn_label, apex_label, current_deps)
            verdict, findings_text, elapsed = run_review(
                asn_num, cone_content, asn_label, previous_findings,
                model=model, foundation_labels=cross_asn_deps)

            if verdict == "ERROR":
                break

            missing = parse_missing_references(findings_text)
            real_missing = [
                m for m in missing
                if m in asn_labels
                and m not in current_deps
                and m != apex_label
            ]

            if not real_missing:
                break
            if expansion_round >= MAX_EXPANSIONS:
                print(f"  [EXPAND] max rounds ({MAX_EXPANSIONS}) reached; "
                      f"unresolved: {real_missing}", file=sys.stderr)
                break

            expansion_round += 1
            print(f"  [EXPAND] round {expansion_round}: adding "
                  f"{real_missing} to cone", file=sys.stderr)
            current_deps.extend(real_missing)

        if verdict == "ERROR":
            print(f"\n  [REGIONAL-REVIEW] FAILED on cycle {cycle} (review error). Skipping.",
                  file=sys.stderr)
            break

        # Always write review file + emit_review (records the review event
        # in the substrate even when reviewer was CONVERGED with no findings)
        had_findings = True
        review_dir.mkdir(parents=True, exist_ok=True)
        review_num = next_review_number(asn_label, reviews_dir=review_dir)
        review_path = review_dir / f"review-{review_num}.md"
        with open(review_path, "w") as rf:
            rf.write(f"# Regional Review — {asn_label}/{apex_label} (cycle {cycle})\n\n")
            rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
            rf.write(findings_text + "\n")
        final_review_path = review_path

        findings = extract_findings(findings_text)

        emit_review(store, review_path)
        emitted_findings = emit_findings(
            store, review_path, findings,
            asn_label, review_path.stem, label_index,
        )
        emitted_by_title = {e["title"]: e for e in emitted_findings}

        for title, cls, _ in findings:
            print(f"\n  ### [{cls}] {title}", file=sys.stderr)

        previous_findings = (previous_findings + "\n\n" + findings_text).strip()

        revise_findings = filter_revise(findings)
        last_cycle_revise_count = len(revise_findings)

        if dry_run:
            print(f"\n  [DRY RUN] {len(revise_findings)} revise finding(s), no fixes.",
                  file=sys.stderr)
            break

        # Revise each REVISE-class finding
        any_changed = False
        for title, _cls, finding_text in revise_findings:
            emitted = emitted_by_title.get(title)
            comment_id = emitted["comment_id"] if emitted else None
            claim_path = emitted["claim_path"] if emitted else None
            ok = revise(asn_num, title, finding_text, claim_dir=claim_dir,
                        comment_id=comment_id, claim_path=claim_path)
            if ok:
                any_changed = True
                if comment_id:
                    resolutions = store.find_links(
                        to_set=[comment_id], type_set=["resolution"],
                    )
                    if not resolutions:
                        print(
                            f"  [WARN] revise succeeded but no resolution "
                            f"link emitted for finding '{title}' "
                            f"(comment {comment_id})",
                            file=sys.stderr,
                        )

        if revise_findings or any_changed:
            step_commit_asn(asn_num,
                            f"regional-review(asn): {asn_label}/{apex_label} — cycle {cycle}")

        # Natural convergence check: this cycle's reviewer filed no revises
        # AND predicate True. The cycle's review is the natural confirmation;
        # no +1 needed.
        if last_cycle_revise_count == 0 and is_claim_converged(store, apex_md_path):
            print(f"\n  [REGIONAL-REVIEW] Natural convergence at cycle {cycle}.",
                  file=sys.stderr)
            naturally_converged = True
            break

        # No-progress short-circuit: revises filed but reviser couldn't fix any.
        # Without progress, looping won't help; break and let +1 confirmation run.
        if revise_findings and not any_changed:
            print(f"  [REGIONAL-REVIEW] Revises filed but no fixes applied this cycle. "
                  f"Breaking to confirmation.", file=sys.stderr)
            break

    failed = (verdict == "ERROR")

    # +1 confirmation cycle (only if we didn't naturally converge and aren't failed/dry-run)
    confirmation_revise_count = 0
    if not failed and not dry_run and not naturally_converged:
        print(f"\n  [CONFIRMATION REVIEW]", file=sys.stderr)
        _retry_unresolved_revises(store, asn_num, claim_dir, [apex_md_path])

        from lib.formalization.gate import run_validate_gate
        scope = {apex_label} | set(dep_labels)
        gate_result = run_validate_gate(asn_label, scope_labels=scope)
        if gate_result != "clean":
            print(f"  [GATE] halted on confirmation — structural violations remain "
                  f"({gate_result})", file=sys.stderr)
            failed = True
        else:
            cone_content = assemble_cone(asn_label, apex_label, dep_labels)
            confirm_verdict, confirm_findings_text, _ = run_review(
                asn_num, cone_content, asn_label, previous_findings,
                model=model, foundation_labels=cross_asn_deps,
            )
            if confirm_verdict == "ERROR":
                failed = True
            else:
                review_dir.mkdir(parents=True, exist_ok=True)
                review_num = next_review_number(asn_label, reviews_dir=review_dir)
                confirm_review_path = review_dir / f"review-{review_num}.md"
                with open(confirm_review_path, "w") as rf:
                    rf.write(f"# Regional Review (Confirmation) — "
                             f"{asn_label}/{apex_label}\n\n")
                    rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
                    rf.write(confirm_findings_text + "\n")
                final_review_path = confirm_review_path

                confirm_findings = extract_findings(confirm_findings_text)
                emit_review(store, confirm_review_path)
                emit_findings(
                    store, confirm_review_path, confirm_findings,
                    asn_label, confirm_review_path.stem, label_index,
                )
                confirmation_revise_count = len(filter_revise(confirm_findings))

    elapsed = time.time() - start_time
    if failed:
        converged = False
    elif naturally_converged:
        converged = True
    elif dry_run:
        # In dry_run we exit after first review; no convergence judgment.
        converged = (last_cycle_revise_count == 0)
    else:
        # +1 confirmation ran; converged iff predicate True AND confirmation quiet
        converged = (
            confirmation_revise_count == 0
            and is_claim_converged(store, apex_md_path)
        )

    if final_review_path is not None and not failed:
        with open(final_review_path, "a") as rf:
            rf.write(f"\n## Result\n\n")
            if converged:
                rf.write(f"Regional review converged.\n")
            else:
                rf.write(f"Regional review not converged after {cycle} cycle(s).\n")
            rf.write(f"\n*Elapsed: {elapsed:.0f}s*\n")

    print(f"  [REGIONAL-REVIEW] Elapsed: {elapsed:.0f}s", file=sys.stderr)

    # End-of-cone compress pass — strip accumulated meta-commentary drift
    # introduced across the cycles. Scoped to files this cone actually
    # changed (via baseline SHA diff). No-op if nothing changed or if
    # dry-run is set.
    if _COMPRESS_ENABLED and not failed:
        from lib.formalization.compress import compress_changed_files_since
        compress_changed_files_since(
            claim_dir, baseline_sha, asn_num,
            apex_label=apex_label, dry_run=dry_run,
        )

    # Commit any residue that per-cycle commits didn't catch: the Result
    # section appended to the last review file, cache updates, and
    # OBSERVE-only cycles whose review files are never reached by the
    # in-loop step_commit_asn (which only runs after a REVISE-driven
    # revise succeeds). step_commit_asn no-ops if nothing is staged.
    if not failed and not dry_run:
        step_commit_asn(
            asn_num,
            f"regional-review(asn): {asn_label}/{apex_label} — final",
        )

    store.close()

    if failed:
        return "failed"
    return "converged" if converged else "not_converged"


def run_regional_sweep(asn_num, min_deps=4, max_cycles=8, dry_run=False, model="opus"):
    """Proactive regional-scale sweep — bottom-up DAG walk.

    For each claim with >= min_deps same-ASN dependencies,
    run a regional review. Process in topological order (foundations first)
    so each cone's dependencies are stable when it runs.

    Returns "converged" or "not_converged".
    """
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    claim_dir = FORMALIZATION_DIR / asn_label
    if not claim_dir.exists():
        print(f"  No formalization directory for {asn_label}", file=sys.stderr)
        return "failed"

    deps_data = generate_formalization_deps(asn_num)
    if not deps_data:
        print(f"  No dependency data for {asn_label}", file=sys.stderr)
        return "failed"

    levels = topological_levels(deps_data)
    asn_labels = set(build_label_index(claim_dir).keys())

    print(f"\n  [REGIONAL-SWEEP] {asn_label} — {len(asn_labels)} claims, "
          f"min_deps={min_deps}", file=sys.stderr)

    start_time = time.time()
    cones_reviewed = 0
    any_not_converged = False

    store = Store()
    label_index = build_cross_asn_label_index()
    rev_index = {p: l for l, p in label_index.items()}
    try:
        for level_idx, level_labels in enumerate(levels):
            for label in level_labels:
                from_path = label_index.get(label)
                if not from_path:
                    continue
                same_deps = [
                    rev_index[link["to_set"][0]]
                    for link in store.find_links(
                        from_set=[from_path], type_set=["citation"],
                    )
                    if link["to_set"]
                    and rev_index.get(link["to_set"][0]) in asn_labels
                ]
                if len(same_deps) < min_deps:
                    continue

                cones_reviewed += 1
                result = run_regional_review(
                    asn_num, label, same_deps,
                    max_cycles=max_cycles, dry_run=dry_run, model=model)

                if result != "converged":
                    any_not_converged = True
    finally:
        store.close()

    elapsed = time.time() - start_time
    if cones_reviewed == 0:
        print(f"\n  [REGIONAL-SWEEP] No claims with >= {min_deps} same-ASN deps.",
              file=sys.stderr)
    else:
        print(f"\n  [REGIONAL-SWEEP] {cones_reviewed} cones reviewed in {elapsed:.0f}s",
              file=sys.stderr)

    return "not_converged" if any_not_converged else "converged"
