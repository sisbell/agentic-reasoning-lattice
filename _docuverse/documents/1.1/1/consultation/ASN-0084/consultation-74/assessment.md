# Channel Assignment — ASN-0084 review-74

**Date:** 2026-05-30 15:35

## Issue 1: Post-state S8 maximality is deferred to the same downstream result in three separate places
Reason: Purely expository deduplication — the discharge is a one-line consequence of dom-preservation plus the invariant audit, all already present in the ASN. No design intent or implementation evidence is needed to state it once and cross-reference.

## Issue 2: The Merge operation's operational use (canonical-partition recovery) is re-announced as deferred in four locations
Reason: Removing three of four redundant deferral announcements is an editorial change internal to the ASN; the Merge definition and its S8-cons proof already stand on their own. No channel input required.

## Issue 3: Width-positivity derivation silently relies on CS3/CS4, the very clause R-CS3 proves is load-bearing
Reason: The fix is to cite CS3/CS4 explicitly where the T1 comparison reduces to ordinal comparison — and R-CS3 already in the ASN constructs the exact failure case, supplying all the reasoning. Fully derivable from the ASN's own content.
