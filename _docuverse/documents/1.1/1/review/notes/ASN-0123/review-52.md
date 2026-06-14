# Review of ASN-0123

I verified the soundness-critical proofs before turning to the anti-bloat pass. **V-WF** discharges both ValidComposite★ clauses correctly across the owned and (account-tier) cross-owner branches, including the n=0 boundary; **V9** O5(ii)-maximality and the severance argument are valid (I re-derived the `w = [pfx(π), 0]`, `zeros(w) = 2` step against O1a); **SA** correctly forces the `zeros(d') ≥ 3` contradiction; **VN-B1**'s case split (base-tier spawn, the other inter-tier spawn ruled out by the penultimate component, k=0 frontier-only) is exhaustive and the "prove once for both g∈{1,2} streams" framing is sound. The worked instances check out arithmetically, including `|A| = 2 < n = 3` and `a₁ ⋠ a₂`. The single finding below is prose-level — the forward-reference accretion the `review-mode.anti-bloat` classifier targets — not a correctness gap.

## REVISE

### Issue 1: Forward/backward-reference accretion around the cross-owner allocation
**ASN-0123, Identity clause comment and V0**

Three cited instances restate facts whose load-bearing form lives elsewhere, with no content usable at their site:

(a) Identity clause: *"Realization as one K.δ in each branch, single-valued, is V-WF."*
This is a pure deferral — it announces where well-formedness is proved without giving the reader anything actionable in the contract. The operation definition should carry the constraint; the realization proof is V-WF's job.

(b) Identity clause: *"The cross-owner branch presupposes an account-tier forker (zeros(pfx(π)) = 1, forced by P-tier when ω(d_src) ≠ π)."*
P-tier sits a few lines above in the *same* precondition block and already states `ω(d_src) = π ∨ zeros(pfx(π)) = 1` with its full rationale. Restating its consequence in the inline comment is redundant within the contract.

(c) V0: *"…excluding the node-tier non-owner (the exclusion's rationale recorded with P-tier above)."*
A bare back-pointer. The clause "excluding the node-tier non-owner" already states the fact; the parenthetical adds only "see P-tier."

**Problem**: The account-tier restriction and its single-K.δ realization are stated as load-bearing hypotheses in P-tier (with rationale), V-WF, V0, and V9 — which is correct, each consumes the hypothesis. The instances above are the non-load-bearing residue: a deferral, a same-block restatement, and a pointer. These are exactly the "multiple paragraphs defer to the same downstream location" / forward-reference patterns that compound across cycles.

**Required**: Drop (a) and (c) outright. For (b), either remove it (P-tier is adjacent) or, if a branch-site reminder is wanted, reduce to the bare fact without re-deriving the P-tier guard. As a lighter related instance, the equation `A_doc(pfx(π)) = S(pfx(π), 2) (ASN-0047, AllocatorHierarchy)` is re-asserted at four sites (identity-clause comment, V-WF preamble, V-WF clause 1, V9 preamble); state the identity once and let later sites refer to it rather than re-citing the equation.

## OUT_OF_SCOPE

None. The note scopes document creation, version comparison, content/link operations, delivery, and replication out cleanly, and the in-note treatment of edit-independence (V11) and link carry-through (V10) is held to fork *guarantees* rather than specifying the out-of-scope operations themselves.

VERDICT: REVISE
