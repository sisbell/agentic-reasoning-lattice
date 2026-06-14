# Review of ASN-0123

I worked the proofs of this note rather than its prose, and they hold. The SA antichain argument (three distinct zero positions forcing `zeros(d') ≥ 3`), VN-B1's case split (only frontier arrivals land in a version namespace — every K.δ instance other than the frontier `k=1`/`k=0` step is excluded structurally), the V9 severance theorem (the O5(ii) maximality now discharged structurally from the `[pfx(π), 0]` prefix carrying `zeros = 2`), V8's coverer-set equality, V13's two-sided pinning, and both worked instances (including `|R' ∖ R| = |A| = 2 < n = 3`, the shared-address gap made concrete) all check out. The boundary cases the topic demands — empty source (`n = 0`), iterated forks, cross-owner severance — are each handled explicitly. I found no correctness gap.

In anti-bloat mode the one thing I had to read around is below.

## REVISE

### Issue 1: V0 supplies a redundant second distinctness witness

**ASN-0123, V0 (FreshUniquePermanentIdentity)**: "Distinctness from *all* other allocation events … is GlobalUniqueness (ASN-0034), which rules out collisions alike from the same allocator, sibling allocators, and allocators at different hierarchy depths. … Across distinct namespaces it is corroborated unconditionally by B7 (NamespaceDisjointness) and B8's cross-namespace case."

**Problem**: The up-front citation already claims GlobalUniqueness covers *all* other allocation events, explicitly including "sibling allocators, and allocators at different hierarchy depths" — which is exactly the cross-namespace case (two documents' version streams are sibling/different-depth allocators). The closing clause then supplies B7/B8 as a second witness for that same sub-case, already discharged unconditionally one sentence earlier. This is a backup proof for an already-closed conclusion — the "corroborated unconditionally by …" is defensive justification the reader has to recognize as redundant before moving on. (This is not the declined deps-audit finding: that was about replacing foundation *redevelopment* with citations; this is the inverse — a surplus citation atop a sufficient one. The reviser's prior rationale endorsed V0's GlobalUniqueness path but did not address the B7/B8 add-on.)

**Required**: Drop the B7/B8 corroboration clause — GlobalUniqueness's stated coverage closes cross-namespace already. Alternatively, if B7/B8 is meant to be the *primary* cross-namespace witness, scope the opening GlobalUniqueness citation to the same-allocator case only (versions of one document) so the two witnesses partition the cases without overlap, rather than both claiming the cross-namespace case.

## OUT_OF_SCOPE

None. The scope boundary is respected: editing, comparison, link creation, delivery, and replication are touched only through frame conditions and open questions, and V10/V11 specify fork *guarantees* (carry-through, edit-independence) rather than the operations themselves.

VERDICT: REVISE
