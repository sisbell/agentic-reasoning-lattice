"""Review-coverage-completeness check.

Every review-classified doc (`review.content` or `review.structural`)
must carry at least one outgoing `review.coverage` link recording
which doc(s) it reviews. Without coverage, downstream predicates and
resolvers can't connect the review back to the claim(s) it covers —
`is_claim_confirmed` can't find the relevant review for a given
claim, claim-findings can't resolve its scope hold, and so on.

This check flags review docs that lack any outgoing `review.coverage`.
It aggregates rather than emits one Issue per missing review — a
gap this big (298/298 on the current substrate) gives too much noise
per-finding.
"""

from __future__ import annotations

from typing import Iterable

from lib.protocols.febe.protocol import Session

from . import Issue, Severity


CHECK_NAME = "review-coverage-completeness"
CHECK_DESCRIPTION = (
    "Every review-classified doc must have at least one outgoing "
    "review.coverage link recording the doc(s) it covers. Without "
    "coverage, downstream predicates can't trace a review back to "
    "the claims it applies to."
)
_SAMPLE_SIZE = 3


def check_review_coverage(session: Session) -> Iterable[Issue]:
    """Yield one aggregate Issue when any review doc lacks coverage."""
    review_addrs = set()
    for classifier in ("review.content", "review.structural"):
        for link in session.active_links(classifier):
            if link.to_set:
                review_addrs.add(link.to_set[0])

    if not review_addrs:
        return

    missing = []
    for addr in sorted(review_addrs, key=lambda a: a.digits):
        if not session.active_links("review.coverage", from_set=[addr]):
            missing.append(addr)

    if not missing:
        return

    sample = ", ".join(str(a) for a in missing[:_SAMPLE_SIZE])
    extra = (
        f" (+{len(missing) - _SAMPLE_SIZE} more)"
        if len(missing) > _SAMPLE_SIZE else ""
    )
    yield Issue(
        severity=Severity.ERROR,
        check=CHECK_NAME,
        message=(
            f"{len(missing)}/{len(review_addrs)} review docs have no "
            f"outgoing review.coverage; sample: {sample}{extra}"
        ),
    )
