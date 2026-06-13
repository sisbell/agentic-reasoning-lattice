# Channel Assignment — ASN-0123 review-24

**Date:** 2026-06-13 08:47

## Issue 1: V0 cites B8 same-namespace, whose preconditions the ASN itself proves do not transfer
Reason: Internal — the fix is pure citation hygiene fully specified by the review and derivable from foundations the ASN already cites. GlobalUniqueness (ASN-0034) already carries same-namespace distinctness in V0's first clause, and applies because the version sub-allocator `A_v(d)` is shown T10a-conforming (siblings by `inc(·,0)`, spawned by `inc(d,1)`, `k'=1 ∈ {1,2}`); deleting the redundant, B1/B2-dependent B8 same-namespace clause (or re-deriving it VN-B1-style) needs neither design intent nor implementation evidence. Uniqueness itself is not in dispute, only which already-present lemma discharges it.
