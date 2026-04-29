"""
Cone-scope review operators: cone-review (one cone) and cone-sweep
(across all qualifying cones), plus cone detection and assembly helpers.

A dependency cone is a claim (the apex) that sits atop many stable
dependencies and can't converge under per-finding revision. See
docs/patterns/dependency-cone.md for the pattern.

- detect_dependency_cone: reactive, from substrate review history
- run_cone_review: focused review/revise loop on one cone
- run_cone_sweep: proactive bottom-up DAG walk, reviews all qualifying cones
"""

import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import (
    WORKSPACE, LATTICE, CLAIM_CONVERGENCE_DIR, CLAIM_DIR, CLAIM_FINDINGS_DIR,
    CLAIM_REVIEWS_DIR, next_review_number, review_aggregate_path,
)
from lib.shared.common import (
    find_asn, build_label_index,
    step_commit_asn,
)
from lib.claim_convergence.full_review.review import (
    run_review, extract_findings, filter_revise, parse_missing_references,
    cycle_verdict, findings_summary,
)


MAX_EXPANSIONS = 5
from lib.claim_convergence.full_review.revise import revise
from lib.claim_convergence.core.build_dependency_graph import generate_claim_convergence_deps
from lib.claim_convergence.core.topological_sort import topological_levels
from lib.store.store import Store, attributed_to, default_store
from lib.store.emit import emit_findings, emit_meta
from lib.store.populate import build_cross_asn_label_index
from lib.store.queries import is_claim_converged, unresolved_revise_comments, active_links


def _retry_unresolved_revises(store, asn_num, claim_dir, scope_md_paths):
    """Re-feed open revise comments to the reviser at the top of a cycle.

    For each unresolved comment.revise targeting a scope path, fetch its
    finding text from the comment's source (the finding document under
    `_docuverse/findings/...`) and call `revise()` again. The reviser closes
    via `convergence-link-resolution.py accept` (with edit) or `convergence-link-resolution.py reject` (with rationale).
    """
    for scope_path in scope_md_paths:
        if not scope_path:
            continue
        for c in unresolved_revise_comments(store, scope_path):
            if not c["from_set"]:
                continue
            finding_path = LATTICE / c["from_set"][0]
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
    """Detect a dependency cone from substrate review history.

    Looks at the last `window` review events for this ASN (review classifier
    links sorted by timestamp). Counts active comment.revise links sourced
    from those reviews' finding documents, grouped by target claim. If one
    claim has >= `threshold` revise comments while its dependencies are
    stable (each <= half the apex's count), returns (apex_label, dep_labels).
    Otherwise returns None.
    """
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        return None

    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        return None

    label_index = build_label_index(claim_dir)
    asn_labels = set(label_index.keys())

    reviews_prefix = str((CLAIM_REVIEWS_DIR / asn_label).relative_to(LATTICE))

    store = Store()
    try:
        scoped_reviews = []
        for r in store.find_links(type_set=["review"]):
            if not r["to_set"]:
                continue
            target = r["to_set"][0]
            if target.startswith(reviews_prefix):
                scoped_reviews.append(r)

        scoped_reviews.sort(key=lambda r: r["ts"], reverse=True)
        recent = scoped_reviews[:window]
        if len(recent) < threshold:
            return None

        # Collect review-N stems from the window. The review classifier link
        # targets `_docuverse/documents/review/claims/<asn>/review-N.md`; per-
        # finding docs sit under `_docuverse/documents/finding/claims/<asn>/
        # review-N/<n>.md` and pair with their aggregate by the shared stem.
        recent_stems = set()
        for r in recent:
            target_path = Path(r["to_set"][0])
            stem = target_path.stem
            if stem.startswith("review-"):
                recent_stems.add(stem)

        cross_index = build_cross_asn_label_index(store=store)
        path_to_label = {p: l for l, p in cross_index.items()}

        revise_counts = {}
        for link in active_links(store, "comment.revise"):
            if not link["from_set"] or not link["to_set"]:
                continue
            src_parent = Path(link["from_set"][0]).parent.name
            if src_parent not in recent_stems:
                continue
            claim_label = path_to_label.get(link["to_set"][0])
            if claim_label in asn_labels:
                revise_counts[claim_label] = revise_counts.get(claim_label, 0) + 1

        if not revise_counts:
            return None

        apex = max(revise_counts, key=revise_counts.get)
        apex_count = revise_counts[apex]
        if apex_count < threshold:
            return None

        apex_path = cross_index.get(apex)
        if not apex_path:
            return None
        cites = active_links(store, "citation", from_set=[apex_path])
        dep_labels = [
            path_to_label[link["to_set"][0]]
            for link in cites
            if link["to_set"]
            and path_to_label.get(link["to_set"][0]) in asn_labels
        ]

        max_dep = max((revise_counts.get(d, 0) for d in dep_labels), default=0)
        if max_dep > apex_count // 2:
            return None

        print(f"  [CONE] Detected: {apex} ({apex_count} revises, "
              f"{len(dep_labels)} stable deps)", file=sys.stderr)
        return (apex, dep_labels)
    finally:
        store.close()


def assemble_cone(asn_label, apex_label, dep_labels):
    """Assemble just the cone claims for focused review.

    Returns concatenated text of apex + same-ASN dependency claims.
    """
    claim_dir = CLAIM_DIR / asn_label
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


def _declined_findings_for_cone(store, cone_md_paths, max_rejects=5):
    """Return text of recently-declined findings on this cone.

    A declined finding is a `comment.revise` targeting any cone claim
    that was closed by `resolution.reject` (the reviser refused to act).
    Each block contains the original finding body plus the reviser's
    rationale text. Sorted by recency, capped at `max_rejects`.

    Accepted findings (closed by `resolution.edit`) are NOT included —
    their resolution lives in the prose itself, so re-evaluating the
    current prose is the correct check on whether the issue persists.
    Open findings (no resolution yet) are NOT included either — they're
    handled by the orchestrator's retry pass at cycle entry.

    The reviewer is shown only the declined ones to discourage
    re-surfacing findings of the same shape that have already been
    deliberated and refused.
    """
    cone_paths = set(cone_md_paths)
    rejects = store.find_links(type_set=["resolution.reject"])
    rejects.sort(key=lambda r: r.get("ts", ""), reverse=True)

    blocks = []
    lattice = Path(LATTICE)
    for r in rejects:
        if len(blocks) >= max_rejects:
            break
        if not r.get("to_set") or len(r["to_set"]) < 2:
            continue
        comment_id = r["to_set"][0]
        rationale_rel = r["to_set"][1]

        comment = store.get(comment_id)
        if comment is None or not comment.get("to_set"):
            continue
        if comment["to_set"][0] not in cone_paths:
            continue
        if not comment.get("from_set"):
            continue

        finding_full = lattice / comment["from_set"][0]
        finding_body = (finding_full.read_text().strip()
                        if finding_full.exists() else "(finding body missing)")
        rationale_full = lattice / rationale_rel
        rationale_text = (rationale_full.read_text().strip()
                          if rationale_full.exists() else "(rationale missing)")

        ts = r.get("ts", "?")
        blocks.append(
            f"### Declined ({ts})\n\n"
            f"**Finding (rejected as invalid):**\n\n{finding_body}\n\n"
            f"**Reviser's rationale for declining:**\n\n{rationale_text}"
        )

    return "\n\n---\n\n".join(blocks) if blocks else ""


@attributed_to("cone-review")
def run_cone_review(asn_num, apex_label, dep_labels, max_cycles=3,
                        dry_run=False, model="opus"):
    """Run a focused cone-scope review/revise loop on one dependency cone.

    Same structure as full-review but with narrower context:
    only the apex and its same-ASN dependencies.

    Returns "converged" or "not_converged".
    """
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        return "failed"

    claim_dir = CLAIM_DIR / asn_label
    review_dir = CLAIM_REVIEWS_DIR / asn_label

    print(f"\n  [REGIONAL-REVIEW] {apex_label} + {len(dep_labels)} deps",
          file=sys.stderr)

    store = default_store()
    label_index = build_cross_asn_label_index(store=store)

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
        for link in active_links(store, "citation", from_set=[from_path]):
            if not link["to_set"]:
                continue
            dep_label = rev_index.get(link["to_set"][0])
            if (dep_label and dep_label not in asn_labels
                    and dep_label not in cross_asn_deps):
                cross_asn_deps.append(dep_label)

    print(f"  Foundation: {len(cross_asn_deps)} cross-ASN deps", file=sys.stderr)

    # Capture baseline SHA so the end-of-cone compress pass knows which
    # files changed during this cone.
    from lib.shared.common import git_head_sha
    baseline_sha = git_head_sha()

    # Build the cone's claim-path set once. Used to scope the declined-
    # findings query that primes the reviewer's "do not re-raise" context.
    apex_md_path = label_index.get(apex_label)
    cone_paths = [apex_md_path] if apex_md_path else []
    for d in dep_labels:
        p = label_index.get(d)
        if p:
            cone_paths.append(p)

    start_time = time.time()
    verdict = "CONVERGED"
    naturally_converged = False
    last_cycle_revise_count = -1
    final_review_path = None

    for cycle in range(1, max_cycles + 1):
        print(f"\n  [CYCLE {cycle}/{max_cycles}]", file=sys.stderr)

        # Retry pass: re-feed any open revise comments from prior cycles
        # or invocations to the reviser. Reviser closes via convergence-link-resolution.py.
        if not dry_run:
            _retry_unresolved_revises(store, asn_num, claim_dir, [apex_md_path])

        # Declined-findings context: substrate-derived list of recently-
        # declined revises on the cone, with reviser rationales. Queried
        # fresh each cycle so any newly-rejected finding from this run's
        # earlier cycles is included.
        previous_findings = _declined_findings_for_cone(store, cone_paths)

        from lib.shared.validate_gate import run_validate_gate
        scope = {apex_label} | set(dep_labels)
        gate_result = run_validate_gate(asn_label, scope_labels=scope)
        if gate_result != "clean":
            print(f"  [GATE] halted — structural violations remain in cone "
                  f"({gate_result}); aborting cone-review",
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

        review_num = next_review_number(asn_label, kind="claim", reviews_dir=review_dir)
        review_stem = f"review-{review_num}"
        meta_path = review_aggregate_path(asn_label, review_num, kind="claim")

        findings = extract_findings(findings_text)
        emitted_findings = emit_findings(
            store, meta_path, findings,
            asn_label, review_stem, label_index,
            findings_dir=CLAIM_FINDINGS_DIR,
        )
        emitted_by_title = {e["title"]: e for e in emitted_findings}

        revise_count = len(filter_revise(findings))
        emit_meta(
            store, asn_label, review_num,
            title=f"Cone Review — {asn_label}/{apex_label} (cycle {cycle})",
            timestamp=time.strftime("%Y-%m-%d %H:%M"),
            scope=f"{apex_label} + {len(dep_labels)} deps (cone)",
            verdict=cycle_verdict(verdict, revise_count),
            findings_summary=findings_summary(findings, revise_count),
            emitted_findings=emitted_findings,
            elapsed_seconds=elapsed,
            reviews_dir=CLAIM_REVIEWS_DIR,
        )
        final_review_path = meta_path

        for title, cls, _ in findings:
            print(f"\n  ### [{cls}] {title}", file=sys.stderr)

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
                            f"cone-review(asn): {asn_label}/{apex_label} — cycle {cycle}")

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

        from lib.shared.validate_gate import run_validate_gate
        scope = {apex_label} | set(dep_labels)
        gate_result = run_validate_gate(asn_label, scope_labels=scope)
        if gate_result != "clean":
            print(f"  [GATE] halted on confirmation — structural violations remain "
                  f"({gate_result})", file=sys.stderr)
            failed = True
        else:
            cone_content = assemble_cone(asn_label, apex_label, dep_labels)
            confirm_verdict, confirm_findings_text, confirm_elapsed = run_review(
                asn_num, cone_content, asn_label, previous_findings,
                model=model, foundation_labels=cross_asn_deps,
            )
            if confirm_verdict == "ERROR":
                failed = True
            else:
                review_num = next_review_number(asn_label, kind="claim", reviews_dir=review_dir)
                review_stem = f"review-{review_num}"
                confirm_meta_path = review_aggregate_path(asn_label, review_num, kind="claim")

                confirm_findings = extract_findings(confirm_findings_text)
                emitted_findings = emit_findings(
                    store, confirm_meta_path, confirm_findings,
                    asn_label, review_stem, label_index,
                    findings_dir=CLAIM_FINDINGS_DIR,
                )
                confirmation_revise_count = len(filter_revise(confirm_findings))
                emit_meta(
                    store, asn_label, review_num,
                    title=f"Cone Review (Confirmation) — {asn_label}/{apex_label}",
                    timestamp=time.strftime("%Y-%m-%d %H:%M"),
                    scope=f"{apex_label} + {len(dep_labels)} deps (cone)",
                    verdict=cycle_verdict(confirm_verdict, confirmation_revise_count),
                    findings_summary=findings_summary(
                        confirm_findings, confirmation_revise_count,
                    ),
                    emitted_findings=emitted_findings,
                    elapsed_seconds=confirm_elapsed,
                    reviews_dir=CLAIM_REVIEWS_DIR,
                )
                final_review_path = confirm_meta_path

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
                rf.write(f"Cone review converged.\n")
            else:
                rf.write(f"Cone review not converged after {cycle} cycle(s).\n")
            rf.write(f"\n*Elapsed: {elapsed:.0f}s*\n")

    print(f"  [REGIONAL-REVIEW] Elapsed: {elapsed:.0f}s", file=sys.stderr)

    # End-of-cone compress pass — strip accumulated meta-commentary drift
    # introduced across the cycles. Scoped to files this cone actually
    # changed (via baseline SHA diff). No-op if nothing changed or if
    # dry-run is set.
    if _COMPRESS_ENABLED and not failed:
        from lib.claim_convergence.compress import compress_changed_files_since
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
            f"cone-review(asn): {asn_label}/{apex_label} — final",
        )

    store.close()

    if failed:
        return "failed"
    return "converged" if converged else "not_converged"


def run_cone_sweep(asn_num, min_deps=4, max_cycles=8, dry_run=False,
                   model="opus", all_mode=False):
    """Proactive cone-scope sweep — bottom-up DAG walk.

    For each claim with >= min_deps same-ASN dependencies,
    run a cone review. Process in topological order (foundations first)
    so each cone's dependencies are stable when it runs.

    Resumable: writes progress to
    `_workspace/cone-sweep/<asn>/progress.json` at apex transitions.
    On restart, skips apexes already completed in the same sweep
    (matched by min_deps + all_mode params). Within a sweep, also
    skips apexes whose convergence predicate already holds — unless
    `all_mode=True`, which forces re-review of every cone (useful
    for surfacing new observations on prior-clean apexes).

    Returns "converged" or "not_converged".
    """
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        print(f"  No claim-convergence directory for {asn_label}", file=sys.stderr)
        return "failed"

    deps_data = generate_claim_convergence_deps(asn_num)
    if not deps_data:
        print(f"  No dependency data for {asn_label}", file=sys.stderr)
        return "failed"

    levels = topological_levels(deps_data)
    asn_labels = set(build_label_index(claim_dir).keys())

    # Workspace progress: skip apexes already done in this in-progress sweep.
    # `--all` unconditionally clears prior progress (it's a fresh re-review of
    # every cone). Otherwise, resume by replaying the completed set.
    from lib.claim_convergence.sweep_progress import (
        read_progress, write_progress, clear_progress,
    )
    if all_mode:
        clear_progress(asn_label)
        completed = set()
    else:
        saved = read_progress(asn_label)
        completed = set(saved.get("completed", [])) if saved else set()
        if completed:
            print(f"\n  [REGIONAL-SWEEP] resuming — {len(completed)} "
                  f"apex(es) already done in this sweep", file=sys.stderr)

    print(f"\n  [REGIONAL-SWEEP] {asn_label} — {len(asn_labels)} claims, "
          f"min_deps={min_deps}{'  --all' if all_mode else ''}",
          file=sys.stderr)

    start_time = time.time()
    cones_reviewed = 0
    cones_skipped = 0
    any_not_converged = False

    store = Store()
    label_index = build_cross_asn_label_index(store=store)
    rev_index = {p: l for l, p in label_index.items()}
    try:
        for level_idx, level_labels in enumerate(levels):
            for label in level_labels:
                from_path = label_index.get(label)
                if not from_path:
                    continue
                same_deps = [
                    rev_index[link["to_set"][0]]
                    for link in active_links(
                        store, "citation", from_set=[from_path],
                    )
                    if link["to_set"]
                    and rev_index.get(link["to_set"][0]) in asn_labels
                ]
                if len(same_deps) < min_deps:
                    continue

                # Workspace gate: already done in this sweep run.
                if label in completed:
                    cones_skipped += 1
                    continue

                # Decide whether to process. Both `--all` and predicate-False
                # process; predicate-True in default mode skips the work.
                if all_mode:
                    cones_reviewed += 1
                    result = run_cone_review(
                        asn_num, label, same_deps,
                        max_cycles=max_cycles, dry_run=dry_run, model=model)
                    if result != "converged":
                        any_not_converged = True
                elif is_claim_converged(store, from_path):
                    print(f"  [REGIONAL-SWEEP] {label}: predicate True, skipping",
                          file=sys.stderr)
                    cones_skipped += 1
                else:
                    cones_reviewed += 1
                    result = run_cone_review(
                        asn_num, label, same_deps,
                        max_cycles=max_cycles, dry_run=dry_run, model=model)
                    if result != "converged":
                        any_not_converged = True

                # Uniform marking: mark completed iff the predicate now holds.
                # This makes `completed` mean exactly "predicate True at the
                # time this apex was visited" — same answer for skip and
                # process paths. Apexes that didn't converge stay re-visitable.
                if is_claim_converged(store, from_path):
                    completed.add(label)
                    write_progress(asn_label, {"completed": sorted(completed)})
    finally:
        store.close()

    elapsed = time.time() - start_time
    if cones_reviewed == 0 and cones_skipped == 0:
        print(f"\n  [REGIONAL-SWEEP] No claims with >= {min_deps} same-ASN deps.",
              file=sys.stderr)
    else:
        print(f"\n  [REGIONAL-SWEEP] {cones_reviewed} reviewed, "
              f"{cones_skipped} skipped, in {elapsed:.0f}s",
              file=sys.stderr)

    # Natural completion → clear progress (no resume needed next time).
    if not dry_run:
        clear_progress(asn_label)

    return "not_converged" if any_not_converged else "converged"
