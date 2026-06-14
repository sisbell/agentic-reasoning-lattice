# Review of ASN-0123

I checked the load-bearing proofs — VN-B1's contiguity induction, SA's antichain argument, V-WF's two-branch composite discharge, V8's coverer-set equality, V9's structural O5(ii)/severance, and V10's LP12 instantiation — against the foundation contracts. The logic is sound, including the cross-owner severance theorem and the worked instances (the position-4 divergence and the `|A| = 2 < n = 3` provenance count both check out). Two findings remain, one a citation-precision slip in a load-bearing precondition, one an anti-bloat repetition.

## REVISE

### Issue 1: nextd's B6-validity justification misattributes `zeros(pfx(π)) = 1` to O1a
**ASN-0123, "nextv, nextd" apparatus**: "`(pfx(π), 2)` is B6-valid — `pfx(π)` is account-tier (`zeros(pfx(π)) = 1`, O1a), T4-valid and entity-resident (PS incumbency), depth `2 ∈ {1, 2}`, `zeros(pfx(π)) + 1 = 2 ≤ 3`."

**Problem**: O1a (AccountOwnershipBoundary, ASN-0042) gives `zeros(pfx(π)) ≤ 1`, not `= 1`. The equality is genuinely needed here — for `g = 2` it is exactly VN-B1's side condition `zeros(p) + (g−1) = 2`, and it is what makes the stream members documents rather than accounts — but it comes from the account-tier hypothesis in the definition's own lead-in ("the account-document namespace of an account-tier principal `π`"), not from O1a. The distinction is not cosmetic: node-tier principals exist. PS(iii) forces `pfx(π₀) ≼ n₀ = [1]`, hence `pfx(π₀) = [1]` with `zeros = 0`, for the bootstrap principal — so O1a's `≤ 1` admits a tier for which `(pfx(π), 2)` is *not* document-producing (its members are accounts, `zeros = 1`). Attributing `= 1` to O1a inverts what O1a supplies (an upper bound), and by the note's own per-step citation standard it is a miscitation in a precondition consumed by V-WF and V9.

**Required**: Attribute `zeros(pfx(π)) = 1` to the account-tier hypothesis (equivalently the Account-entity occupancy from PS incumbency), citing O1a only for the `≤ 1` ceiling it actually provides.

### Issue 2: the node-tier-exclusion rationale is restated across five sites, with V0 carrying a worked-out excluded case
**ASN-0123, V0**: "P-tier is what confines the operation to these two branches … `nextd(E,π) = next(E,pfx(π),2)` would yield `inc(pfx(π),2)=[pfx(π),0,1]` with zeros=1, an Account rather than a Document, so a single K.δ cannot deliver `v ∈ E_doc`. Forking a foreign document from the node tier would demand minting an account *and* a document under it — more than the one identity the operation allocates — and so falls outside VERSION's domain."

**Problem**: The fact "the cross-owner branch requires an account-tier forker / P-tier excludes the node-tier non-owner" is stated in five places: the P-tier contract line and its comment, the identity-clause comment, V0, V-WF, and V9. The V-WF and V9 occurrences are load-bearing proof obligations (V-WF discharges the K.δ descent precondition `zeros(t) ≤ 1`; V9's structural O5(ii) needs `zeros(w) = 2`) and must stay. What is repeated is the *rationale* for the domain restriction, and V0 carries the fullest version — computing the excluded node-tier case mechanically. This is precisely the flagged anti-bloat pattern: a paragraph imagining a precondition-excluded case in detail, restating a restriction P-tier already fixes. V0's "exactly one identity" count is established by the two in-domain branches plus GlobalUniqueness; the excluded-case mechanics do not advance it, and a precise reader following the count proof must skip past them.

**Required**: Keep the discharges in V-WF and V9. Replace V0's mechanical computation of the node-tier case with a citation of P-tier's domain condition, and consolidate the exclusion rationale to one canonical site (P-tier's commentary, which the recent revision already touched).

## OUT_OF_SCOPE

None requiring relocation. The note confines itself to the fork and correctly defers adjacent territory — concurrent-fork serialization, location-fixed windowing, withdrawal/supersession, and version-comparison correspondence — to its Open Questions rather than smuggling claims about them into the contract. V11's windowing remark stops at "realizable as a read-time query" and defers the guarantee itself; V10's link claims are guarantees *of* the fork, not a specification of link operations.

VERDICT: REVISE
