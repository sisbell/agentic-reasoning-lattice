"""Aggregate-anchor-coverage check.

For every `claims.statements` aggregate, the substrate must carry a
`citation.depends` anchor — somewhere in the aggregate's supersession
chain — for every (claim, content_source) pair the aggregate reads.
Without coverage, sidecar advancement (description, name, ...) goes
undetected by the freshness predicate, and the on-disk aggregate
drifts from the substrate's cascade signal.

The doctor mirrors the predicate's expected set (built from
`content_sources_for_claim`) and the chain-wide cited set
(`cited_targets_in_chain`), then reports the gap. Unlike the
predicate, this check doesn't skip on the confirmation gate —
coverage is a property of the aggregate's substrate state,
independent of whether the cluster has converged yet.
"""

from __future__ import annotations

from typing import Iterable, Optional

from lib.backend.addressing import Address
from lib.predicates.cascade import (
    cited_targets_in_chain, content_sources_for_claim,
)
from lib.predicates.quiescence import derived_claims
from lib.predicates.versions import version_head
from lib.protocols.febe.protocol import Session

from . import Issue, Severity


CHECK_NAME = "aggregate-anchor-coverage"
CHECK_DESCRIPTION = (
    "Every claims.statements aggregate must carry a citation.depends "
    "anchor for every (claim, content_source) version_head it reads. "
    "Missing anchors mean sidecar advancement goes undetected and the "
    "aggregate's rendered content drifts silently."
)
_MAX_SAMPLES = 3


def _source_note(
    session: Session, aggregate: Address,
) -> Optional[Address]:
    for link in session.active_links(
        "provenance.derivation", to_set=[aggregate],
    ):
        if link.from_set:
            return link.from_set[0]
    return None


def check_aggregate_anchor_coverage(
    session: Session,
) -> Iterable[Issue]:
    """Yield one Issue per aggregate with missing anchors."""
    classified_claims = {
        link.to_set[0]
        for link in session.active_links("claim")
        if link.to_set
    }

    for link in session.active_links("claims.statements"):
        if not link.to_set:
            continue
        aggregate = link.to_set[0]
        agg_path = session.get_path_for_addr(aggregate) or "(no path)"

        note = _source_note(session, aggregate)
        if note is None:
            yield Issue(
                severity=Severity.ERROR,
                check=CHECK_NAME,
                message=(
                    f"aggregate={aggregate} ({agg_path})  "
                    f"missing provenance.derivation from any note"
                ),
            )
            continue

        claims = [
            d for d in derived_claims(session, note)
            if d in classified_claims
        ]
        if not claims:
            continue

        cited = cited_targets_in_chain(session, aggregate)
        expected_total = 0
        missing = []
        for claim in claims:
            for source in content_sources_for_claim(session, claim):
                target = version_head(session, source)
                expected_total += 1
                if target not in cited:
                    missing.append((claim, source, target))

        if not missing:
            continue

        sample = ", ".join(
            f"claim={c} source={s} head={t}"
            for c, s, t in missing[:_MAX_SAMPLES]
        )
        extra = (
            f" (+{len(missing) - _MAX_SAMPLES} more)"
            if len(missing) > _MAX_SAMPLES else ""
        )
        yield Issue(
            severity=Severity.ERROR,
            check=CHECK_NAME,
            message=(
                f"aggregate={aggregate} ({agg_path})  "
                f"missing {len(missing)}/{expected_total} anchors; "
                f"sample: {sample}{extra}"
            ),
        )
