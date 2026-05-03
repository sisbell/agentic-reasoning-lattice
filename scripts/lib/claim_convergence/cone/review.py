"""Cone review — the per-cone review/revise loop."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import (
    LATTICE, WORKSPACE_DIR, CLAIM_DIR,
    CLAIM_FINDINGS_DIR, CLAIM_REVIEWS_DIR,
    next_review_number, review_aggregate_path,
)
from lib.shared.common import find_asn, build_label_index, step_commit_asn
from lib.claim_convergence.full_review.review import (
    run_review, extract_findings, filter_revise,
    cycle_verdict, findings_summary,
)
from lib.claim_convergence.full_review.revise import revise
from lib.claim_convergence.finding_classifier import apply_classifier_verdict
from lib.store.store import attributed_to, default_store
from lib.store.emit import emit_findings, emit_meta
from lib.store.populate import build_cross_asn_label_index
from lib.store.queries import is_claim_converged, active_links

from .scope import assemble_cone, transitive_same_asn_deps
from .retry import _retry_unresolved_revises, _declined_findings_for_cone


# End-of-cone compress pass — disabled 2026-04-22 pending re-evaluation
# under the Dijkstra-voice reviser. The generative reviser should not
# produce the meta-prose accumulation that compress was built to clean up.
# Flip to True to re-enable without touching anything else.
_COMPRESS_ENABLED = False


@attributed_to("cone-review")
def run_cone_review(asn_num, apex_label, dep_labels, max_cycles=3,
                        dry_run=False, model="sonnet"):
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

    store = default_store()
    label_index = build_cross_asn_label_index(store=store)
    asn_labels = set(build_label_index(claim_dir).keys())
    rev_index = {p: l for l, p in label_index.items()}

    # Walk the citation.depends graph transitively from the apex to get
    # the full grounding chain for soundness review. Replaces whatever
    # `dep_labels` the caller passed (typically direct deps) — substrate
    # is now the source of truth.
    apex_md_path = label_index.get(apex_label)
    if apex_md_path:
        dep_labels = transitive_same_asn_deps(
            store, apex_md_path, asn_labels, rev_index,
        )

    print(f"\n  [REGIONAL-REVIEW] {apex_label} + {len(dep_labels)} deps",
          file=sys.stderr)

    # Collect cross-ASN deps for narrowed foundation loading.
    all_cone_labels = [apex_label] + dep_labels
    cross_asn_deps = []
    for label in all_cone_labels:
        from_path = label_index.get(label)
        if not from_path:
            continue
        for link in active_links(store, "citation.depends", from_set=[from_path]):
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

        # Review on the complete cone in one pass. Cone-assembly walks
        # the citation.depends graph transitively from the apex, so the
        # full grounding chain is in scope from round 0; lazy expansion
        # via reviewer-emitted MISSING-REFERENCES is no longer needed.
        cone_content = assemble_cone(asn_label, apex_label, dep_labels)
        verdict, findings_text, elapsed = run_review(
            asn_num, cone_content, asn_label, previous_findings,
            model=model, foundation_labels=cross_asn_deps)

        if verdict == "ERROR":
            print(f"\n  [REGIONAL-REVIEW] FAILED on cycle {cycle} (review error). Skipping.",
                  file=sys.stderr)
            break

        # Persist raw reviewer output for diagnosis. emit_findings drops
        # findings whose Foundation/ASN body fields don't yield a parseable
        # target label; without this dump the bodies are lost.
        raw_dir = WORKSPACE_DIR / "cone-sweep" / asn_label / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_path = raw_dir / f"{apex_label}-cycle{cycle}.txt"
        raw_path.write_text(findings_text)

        review_num = next_review_number(asn_label, kind="claim", reviews_dir=review_dir)
        review_stem = f"review-{review_num}"
        meta_path = review_aggregate_path(asn_label, review_num, kind="claim")

        findings = extract_findings(findings_text)
        apply_classifier_verdict(findings)
        emitted_findings = emit_findings(
            store, meta_path, findings,
            asn_label, review_stem, label_index,
            findings_dir=CLAIM_FINDINGS_DIR,
        )
        emitted_by_title = {e["title"]: e for e in emitted_findings}

        # Count only findings that actually emitted — skipped findings
        # (no parseable target) won't drive revise work, so they shouldn't
        # be counted toward the cycle's revise total.
        emitted_titles = set(emitted_by_title.keys())
        emitted_for_filter = [f for f in findings if f[0] in emitted_titles]
        revise_count = len(filter_revise(emitted_for_filter))
        emit_meta(
            store, asn_label, review_num,
            title=f"Cone Review — {asn_label}/{apex_label} (cycle {cycle})",
            timestamp=time.strftime("%Y-%m-%d %H:%M"),
            scope=f"{apex_label} + {len(dep_labels)} deps (cone)",
            verdict=cycle_verdict(verdict, revise_count),
            findings_summary=findings_summary(emitted_for_filter, revise_count),
            emitted_findings=emitted_findings,
            elapsed_seconds=elapsed,
            reviews_dir=CLAIM_REVIEWS_DIR,
        )
        final_review_path = meta_path

        for title, cls, _ in findings:
            print(f"\n  ### [{cls}] {title}", file=sys.stderr)

        revise_findings = filter_revise(emitted_for_filter)
        last_cycle_revise_count = len(revise_findings)

        if dry_run:
            print(f"\n  [DRY RUN] {len(revise_findings)} revise finding(s), no fixes.",
                  file=sys.stderr)
            break

        # Revise each REVISE-class finding. Orphans (findings whose target
        # didn't parse) are excluded above by filtering against
        # emitted_titles, so this loop only sees findings the substrate
        # actually accepted. Defensive check preserved as a loud guard
        # against future regressions.
        any_changed = False
        for title, _cls, finding_text in revise_findings:
            emitted = emitted_by_title.get(title)
            if emitted is None:
                print(
                    f"  [WARN] orphan revise skipped — finding '{title[:70]}' "
                    f"has no emitted target (target unparseable from "
                    f"Foundation/ASN). Raw reviewer output at: {raw_path}",
                    file=sys.stderr,
                )
                continue
            comment_id = emitted["comment_id"]
            claim_path = emitted["claim_path"]
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

        # Sync substrate citation links to the .md as the source of
        # truth. The agentic reviser may have edited *Depends:* /
        # *Forward References:* sections without emitting matching
        # cite/retract calls; auto-correct closes the drift before the
        # cycle commits, so substrate can't diverge from prose.
        from lib.store.sync import sync_claim_citations
        for label in [apex_label] + dep_labels:
            md_rel = label_index.get(label)
            if not md_rel:
                continue
            changes = sync_claim_citations(store, md_rel, label_index)
            if changes is None:
                continue
            for direction in ("depends", "forward"):
                for added in changes[direction]["added"]:
                    print(f"  [DRIFT-FIX] {label}: emitted citation.{direction} "
                          f"→ {added} (in *{'Depends' if direction == 'depends' else 'Forward References'}:*)",
                          file=sys.stderr)
                for retracted in changes[direction]["retracted"]:
                    print(f"  [DRIFT-FIX] {label}: retracted citation.{direction} "
                          f"→ {retracted} (no longer in *{'Depends' if direction == 'depends' else 'Forward References'}:*)",
                          file=sys.stderr)

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
                # Persist raw reviewer output for diagnosis (same as cycle path).
                confirm_raw_dir = WORKSPACE_DIR / "cone-sweep" / asn_label / "raw"
                confirm_raw_dir.mkdir(parents=True, exist_ok=True)
                confirm_raw_path = confirm_raw_dir / f"{apex_label}-confirm.txt"
                confirm_raw_path.write_text(confirm_findings_text)

                review_num = next_review_number(asn_label, kind="claim", reviews_dir=review_dir)
                review_stem = f"review-{review_num}"
                confirm_meta_path = review_aggregate_path(asn_label, review_num, kind="claim")

                confirm_findings = extract_findings(confirm_findings_text)
                apply_classifier_verdict(confirm_findings)
                emitted_findings = emit_findings(
                    store, confirm_meta_path, confirm_findings,
                    asn_label, review_stem, label_index,
                    findings_dir=CLAIM_FINDINGS_DIR,
                )
                # Count only emitted findings — orphans don't drive work.
                confirm_emitted_titles = {e["title"] for e in emitted_findings}
                confirm_emitted_for_filter = [
                    f for f in confirm_findings if f[0] in confirm_emitted_titles
                ]
                confirmation_revise_count = len(filter_revise(confirm_emitted_for_filter))
                emit_meta(
                    store, asn_label, review_num,
                    title=f"Cone Review (Confirmation) — {asn_label}/{apex_label}",
                    timestamp=time.strftime("%Y-%m-%d %H:%M"),
                    scope=f"{apex_label} + {len(dep_labels)} deps (cone)",
                    verdict=cycle_verdict(confirm_verdict, confirmation_revise_count),
                    findings_summary=findings_summary(
                        confirm_emitted_for_filter, confirmation_revise_count,
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
