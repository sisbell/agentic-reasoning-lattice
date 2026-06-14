# Channel Assignment — ASN-0123 review-48

**Date:** 2026-06-13 21:41

## Issue 1: the cross-owner identity clause does not pin v; its determinism rests on an unproved document-namespace contiguity
Reason: Internal. The fix is a proof generalization plus a definition (or a scope declaration), all derivable from foundations the ASN already cites — VN-B1's induction over K.δ's cases carries to `S(pfx(π),2)` with the k=2 descent as the base-arrival case, and `nextd(E,π) := next(E, pfx(π), 2)` uses ASN-0040's `next`. Whether v should be pinned deterministically is already settled by the Effect clause presenting it as a function of Σ; no design intent or implementation evidence is at issue.

## Issue 2: nextv carries a forward-referenced restatement
Reason: Internal. Pure reordering (move generalized VN-B1 ahead of nextv) and deduplication (drop the informal registry-purity sentence in favor of V5(b)); no design or implementation facts are involved.
