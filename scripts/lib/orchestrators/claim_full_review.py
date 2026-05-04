"""Claim full-review orchestrator — whole-ASN deep structural review.

Drives whole-ASN review through review/revise cycles until the
substrate predicate (`is_asn_converged`) holds or `max_cycles` is
exhausted, with a +1 confirmation cycle. Includes dependency-cone
auto-detection: when one claim keeps getting revised while its
dependencies are stable, dispatches to a cone-review focused loop.

Dispatches:
- claim_review agent (whole-ASN scope, no foundation_labels narrowing)
- claim_revise agent (per-finding fix)
- cone-review orchestrator (when a thrashing cone is detected)
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from lib.provenance import attributed_to
from lib.agents.claim_review import (
    cycle_verdict, extract_findings, filter_revise,
    findings_summary, run_review,
)
from lib.agents.claim_revise import revise
from lib.backend.schema import ATTRIBUTE_SUFFIXES
from lib.claim_convergence.cone.retry import _retry_unresolved_revises
from lib.claim_convergence.cone.select import detect_dependency_cone
from lib.claim_convergence.findings import emit_findings, emit_meta
from lib.protocols.febe.session import open_session
from lib.lattice.labels import build_cross_asn_label_index
from lib.orchestrators.cone_review import run_cone_review
from lib.predicates import is_asn_converged
from lib.shared.common import (
    assemble_readonly, find_asn, step_commit_asn,
)
from lib.shared.paths import (
    CLAIM_DIR, CLAIM_FINDINGS_DIR, CLAIM_REVIEWS_DIR,
    LATTICE, WORKSPACE,
    next_review_number, review_aggregate_path,
)
from lib.shared.validate_gate import run_validate_gate


@attributed_to("full-review")
def run_full_review(asn_num, max_cycles=8, dry_run=False, model="opus"):
    """Run the full review pipeline.

    Returns "converged" or "not_converged".
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    review_dir = CLAIM_REVIEWS_DIR / asn_label

    print(f"\n  [FULL-REVIEW] {asn_label}", file=sys.stderr)

    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        print(
            f"  No claim-convergence directory for {asn_label}",
            file=sys.stderr,
        )
        return "failed"

    print(
        f"  Directory: {claim_dir.relative_to(WORKSPACE)}",
        file=sys.stderr,
    )

    start_time = time.time()
    previous_findings = ""
    naturally_converged = False
    last_cycle_revise_count = -1
    final_review_path = None
    verdict = "CONVERGED"

    session = open_session(LATTICE)
    label_index = build_cross_asn_label_index(session.store)

    asn_claim_md_paths = [
        str(md_path.relative_to(LATTICE))
        for md_path in claim_dir.glob("*.md")
        if not md_path.name.startswith("_")
        and not md_path.name.endswith(ATTRIBUTE_SUFFIXES)
    ]
    asn_claim_addrs = [
        session.get_addr_for_path(p) for p in asn_claim_md_paths
    ]
    asn_claim_addrs = [a for a in asn_claim_addrs if a is not None]

    for cycle in range(1, max_cycles + 1):
        print(f"\n  [CYCLE {cycle}/{max_cycles}]", file=sys.stderr)

        if not dry_run:
            _retry_unresolved_revises(
                session, asn_num, claim_dir, asn_claim_addrs,
            )

        gate_result = run_validate_gate(asn_label, scope_labels=None)
        if gate_result != "clean":
            print(
                f"  [GATE] halted — structural violations remain "
                f"({gate_result}); aborting full-review",
                file=sys.stderr,
            )
            session.close()
            return "failed"

        asn_content = assemble_readonly(asn_label)

        verdict, findings_text, elapsed = run_review(
            asn_num, asn_content, asn_label, previous_findings,
            model=model,
        )

        if verdict == "ERROR":
            print(
                f"\n  [FULL-REVIEW] FAILED on cycle {cycle} (review error).",
                file=sys.stderr,
            )
            break

        review_num = next_review_number(
            asn_label, kind="claim", reviews_dir=review_dir,
        )
        review_stem = f"review-{review_num}"
        meta_path = review_aggregate_path(
            asn_label, review_num, kind="claim",
        )

        findings = extract_findings(findings_text)
        review_link = emit_meta(
            session, asn_label, review_num,
            title=f"Full Review — {asn_label} (cycle {cycle})",
            timestamp=time.strftime("%Y-%m-%d %H:%M"),
            scope=f"{asn_label} (full)",
            verdict="(pending)",
            findings_summary="(pending)",
            emitted_findings=[],
            elapsed_seconds=elapsed,
            reviews_dir=CLAIM_REVIEWS_DIR,
        )
        review_addr = (
            review_link.to_set[0] if review_link.to_set else None
        )
        emitted_findings = emit_findings(
            session, review_addr, findings,
            asn_label, review_stem, label_index,
            findings_dir=CLAIM_FINDINGS_DIR,
        )
        emitted_by_title = {e["title"]: e for e in emitted_findings}

        revise_count = len(filter_revise(findings))
        emit_meta(
            session, asn_label, review_num,
            title=f"Full Review — {asn_label} (cycle {cycle})",
            timestamp=time.strftime("%Y-%m-%d %H:%M"),
            scope=f"{asn_label} (full)",
            verdict=cycle_verdict(verdict, revise_count),
            findings_summary=findings_summary(findings, revise_count),
            emitted_findings=emitted_findings,
            elapsed_seconds=elapsed,
            reviews_dir=CLAIM_REVIEWS_DIR,
        )
        final_review_path = meta_path

        for title, cls, _ in findings:
            print(f"\n  ### [{cls}] {title}", file=sys.stderr)

        previous_findings = (
            previous_findings + "\n\n" + findings_text
        ).strip()

        revise_findings = filter_revise(findings)
        last_cycle_revise_count = len(revise_findings)

        if dry_run or max_cycles == 1:
            if dry_run:
                print(
                    f"\n  [DRY RUN] {len(revise_findings)} revise "
                    f"finding(s), no fixes.", file=sys.stderr,
                )
            else:
                print(
                    f"\n  Single pass — {len(revise_findings)} revise "
                    f"finding(s), no fixes.", file=sys.stderr,
                )
            break

        any_changed = False
        for title, _cls, finding_text in revise_findings:
            emitted = emitted_by_title.get(title)
            comment_id = emitted["comment_id"] if emitted else None
            claim_path = emitted["claim_path"] if emitted else None
            ok = revise(
                asn_num, title, finding_text, claim_dir=claim_dir,
                comment_id=comment_id, claim_path=claim_path,
            )
            if ok:
                any_changed = True
                if comment_id:
                    resolutions = session.find_links(
                        to_set=[comment_id], type_="resolution",
                    )
                    if not resolutions:
                        print(
                            f"  [WARN] revise succeeded but no "
                            f"resolution link emitted for finding "
                            f"'{title}' (comment {comment_id})",
                            file=sys.stderr,
                        )

        if revise_findings or any_changed:
            step_commit_asn(
                asn_num,
                f"full-review(asn): {asn_label} — cycle {cycle}",
            )

        cone = detect_dependency_cone(asn_num)
        if cone:
            apex, deps = cone
            run_cone_review(
                asn_num, apex, deps, max_cycles=3,
                dry_run=dry_run, model=model,
            )

        if (
            last_cycle_revise_count == 0
            and is_asn_converged(session, asn_label)
        ):
            print(
                f"\n  [FULL-REVIEW] Natural convergence at cycle {cycle}.",
                file=sys.stderr,
            )
            naturally_converged = True
            break

        if revise_findings and not any_changed:
            print(
                f"  [FULL-REVIEW] Revises filed but no fixes applied "
                f"this cycle. Breaking to confirmation.",
                file=sys.stderr,
            )
            break

    failed = (verdict == "ERROR")

    confirmation_revise_count = 0
    if (
        not failed and not dry_run
        and max_cycles > 1 and not naturally_converged
    ):
        print("\n  [CONFIRMATION REVIEW]", file=sys.stderr)
        _retry_unresolved_revises(
            session, asn_num, claim_dir, asn_claim_addrs,
        )

        gate_result = run_validate_gate(asn_label, scope_labels=None)
        if gate_result != "clean":
            print(
                f"  [GATE] halted on confirmation — structural "
                f"violations ({gate_result})", file=sys.stderr,
            )
            failed = True
        else:
            asn_content = assemble_readonly(asn_label)
            confirm_verdict, confirm_findings_text, confirm_elapsed = (
                run_review(
                    asn_num, asn_content, asn_label, previous_findings,
                    model=model,
                )
            )
            if confirm_verdict == "ERROR":
                failed = True
            else:
                review_num = next_review_number(
                    asn_label, kind="claim", reviews_dir=review_dir,
                )
                review_stem = f"review-{review_num}"
                confirm_meta_path = review_aggregate_path(
                    asn_label, review_num, kind="claim",
                )

                confirm_findings = extract_findings(confirm_findings_text)
                confirm_review_link = emit_meta(
                    session, asn_label, review_num,
                    title=f"Full Review (Confirmation) — {asn_label}",
                    timestamp=time.strftime("%Y-%m-%d %H:%M"),
                    scope=f"{asn_label} (full)",
                    verdict="(pending)",
                    findings_summary="(pending)",
                    emitted_findings=[],
                    elapsed_seconds=confirm_elapsed,
                    reviews_dir=CLAIM_REVIEWS_DIR,
                )
                confirm_review_addr = (
                    confirm_review_link.to_set[0]
                    if confirm_review_link.to_set else None
                )
                emitted_findings = emit_findings(
                    session, confirm_review_addr, confirm_findings,
                    asn_label, review_stem, label_index,
                    findings_dir=CLAIM_FINDINGS_DIR,
                )
                confirmation_revise_count = len(
                    filter_revise(confirm_findings)
                )
                emit_meta(
                    session, asn_label, review_num,
                    title=f"Full Review (Confirmation) — {asn_label}",
                    timestamp=time.strftime("%Y-%m-%d %H:%M"),
                    scope=f"{asn_label} (full)",
                    verdict=cycle_verdict(
                        confirm_verdict, confirmation_revise_count,
                    ),
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
    elif dry_run or max_cycles == 1:
        converged = (last_cycle_revise_count == 0)
    else:
        converged = (
            confirmation_revise_count == 0
            and is_asn_converged(session, asn_label)
        )

    if final_review_path is not None and not failed:
        with open(final_review_path, "a") as rf:
            rf.write("\n## Result\n\n")
            if converged:
                rf.write("Converged.\n")
            else:
                rf.write(f"Not converged after {cycle} cycle(s).\n")
            rf.write(f"\n*Elapsed: {elapsed:.0f}s*\n")

        print(
            f"\n  Review: {final_review_path.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )

    print(f"  Elapsed: {elapsed:.0f}s", file=sys.stderr)

    if not dry_run:
        hint = (
            f"full-review(asn): {asn_label}"
            f"{'' if converged else ' — not converged'}"
        )
        step_commit_asn(asn_num, hint)

    session.close()
    if failed:
        return "failed"
    return "converged" if converged else "not_converged"


def run_revise_from_review(asn_num, review_spec):
    """Read an existing review file and revise each finding.

    review_spec can be:
      - a number (e.g., "7" → review-7.md)
      - a filename (e.g., "review-7.md")
      - a full path
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return False

    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        print(
            f"  No claim-convergence directory for {asn_label}",
            file=sys.stderr,
        )
        return False

    review_dir = claim_dir / "reviews"
    review_path = Path(review_spec)
    if not review_path.exists():
        if review_spec.isdigit():
            review_path = review_dir / f"review-{review_spec}.md"
        elif not review_spec.endswith(".md"):
            review_path = review_dir / f"{review_spec}.md"
        else:
            review_path = review_dir / review_spec

    if not review_path.exists():
        print(f"  Review file not found: {review_path}", file=sys.stderr)
        return False

    review_text = review_path.read_text()
    findings = extract_findings(review_text)

    if not findings:
        print(f"  No findings in {review_path}", file=sys.stderr)
        return False

    print(
        f"\n  [REVISE] {asn_label} — {len(findings)} findings from "
        f"{review_path}", file=sys.stderr,
    )

    any_changed = False
    for title, finding_text in findings:
        print(f"\n  ### {title}", file=sys.stderr)
        ok = revise(asn_num, title, finding_text, claim_dir=claim_dir)
        if ok:
            any_changed = True

    if any_changed:
        step_commit_asn(asn_num, hint="full-review revise")

    return any_changed
