# Channel Assignment — ASN-0093 review-35

**Date:** 2026-05-31 07:15

## Issue 1: T7 cited under a reinvented name
Reason: The correct foundation name (SubspaceDisjointness, ASN-0034) is supplied by the review itself; T7 belongs to the foundation spec layer, which neither Nelson (design intent) nor Gregory (udanax-green code) governs. Pure citation rename.

## Issue 2: `b_C(d) = inc(d, 2)` silently assumes `s_C = 1`
Reason: The `s_C = 1` dependency is already pinned by SubspaceConventionAxiom within the ASN, and the parallel `b_L(d)` step already models the citation discipline to copy. Internal.

## Issue 3: Duplicated `dom(M') = dom(M)` rationale (anti-bloat)
Reason: Editorial deduplication of identical prose across two operation definitions; no design or implementation fact at stake. Internal.

## Issue 4: Downstream-consumer inventory in Cross-document disjointness lemma (anti-bloat)
Reason: Deleting a trailing use-site pointer is a self-contained editorial removal that does not alter the lemma's substance. Internal.

## Issue 5: Repeated "state-independent citations need no per-transition discharge" (anti-bloat)
Reason: Removing one of two restatements is an editorial choice fully resolvable from the ASN's own text. Internal.

## Issue 6: Forward-reference Terminology paragraph (anti-bloat)
Reason: The operative definition ("Document = element of `dom(M)`") stands on its own, and the deleted sentence concerns explicitly-deferred entity-hierarchy machinery; removal is editorial. Internal.
