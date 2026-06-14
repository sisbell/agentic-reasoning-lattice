# Review of ASN-0123

I checked the operation contract and every introduced claim against its cited foundations, with attention to the cross-owner branch (where the real soundness work lives), the boundary cases (empty source `n=0`, first vs. later version, iterated forks), and the couplings.

The mathematics holds up. I verified each of these in full and found no gap:

- **SA** — the antichain proof's separator-zero argument is correct (`#d' ≥ #d₀+1` forces `d`'s separator into `b`'s document prefix, pushing `zeros(d') ≥ 3`).
- **VN-B1** — all four K.δ arrival cases (Node, k=2, k=1, k=0) are genuinely exhausted; the k=0 case correctly pins the operand to `c_{j−1}` and forces `j = m+1`.
- **V9 O5(ii)** — the maximality theorem (any prefix of `v` longer than `pfx(π)` must absorb the separator zero at position `#pfx(π)+1`, contradicting O1a) is airtight, and it genuinely closes the cross-transition-system gap that ASN-0042's O5 axiom could not transfer.
- **V9(a) severance** — both branches of the prefix comparison close.
- **V-WF** — both ValidComposite★ clauses discharged for both branches; `n=0` handled.
- The owned/cross-owner worked instances check arithmetically (zeros counts, divergence position 4, `a₁ ⋠ a₂`).

I have one finding, in the note's active anti-bloat register.

## REVISE

### Issue 1: V9's preamble re-establishes the cross-owner allocation setup already proved in V-WF

**ASN-0123, V-WF**: "In the cross-owner branch … the forker π allocates the identity as one document-level K.δ at the frontier of its account document sub-allocator A_doc(pfx(π)) = S(pfx(π), 2) … so zeros(v) = zeros(pfx(π)) + 1 = 2 … and every stream member is T4-valid (B6(a), ASN-0040) — whence Document(v) directly".

**ASN-0123, V9**: "π's account pfx(π) ∈ E (PS incumbency) carries the document sub-allocator A_doc(pfx(π)), which is the sibling stream S(pfx(π), 2) … π creates v there as a single document-level K.δ in its own namespace (… a first document via the k = 2 descent, a later one via a k = 0 sibling, both lying in S(pfx(π), 2)) … — Document(v) — zeros(v) = zeros(pfx(π)) + 1 = 2 (the lone separator) and T4-valid (B6(a) on the stream, ASN-0040), so v ∈ E_doc".

**Problem**: The two sections independently re-establish the same cross-owner allocation core — `pfx(π) ∈ E` (PS incumbency) carrying `A_doc(pfx(π)) = S(pfx(π), 2)`; the single document-level K.δ split into the `k=2` first-document descent and the `k=0` later sibling, both landing in `S(pfx(π), 2)`; `zeros(v) = zeros(pfx(π)) + 1 = 2`; T4-validity via B6(a), hence `Document(v)`. V-WF establishes these to discharge composite validity (the K.δ operand/freshness and the K.μ⁺ `v ∈ E_doc` precondition); V9 restates them to set up severance. A reader arriving at V9 having just read V-WF must skip past ~2–3 sentences of re-derivation before reaching V9's genuinely new content. (V0's brief "a single document K.δ in π's existing document namespace" is fine — it is a one-clause count-support mention, not a re-derivation.)

**Required**: Have V9's preamble cite V-WF for the shared allocation facts — `v` is a single document-level K.δ in `A_doc(pfx(π)) = S(pfx(π), 2)`, with `Document(v)` and `zeros(v) = 2` — and proceed directly to the content V9 uniquely needs: the SiblingStream positional form `v = [pfx(π)₁, …, pfx(π)_{#pfx(π)}, 0, k]` (one step from `v ∈ S(pfx(π), 2)`) and the O5(i)/O5(ii) theorems built on it. This removes the duplication while leaving the soundness-closing O5(ii) discharge and the severance derivation fully intact — none of the protected content is touched.

## OUT_OF_SCOPE

None. The note correctly confines itself to the fork: it scopes out document creation, comparison, content/link operations, delivery, and replication, and touches them only via frame conditions or foundation invariants. The cross-owner branch's use of `A_doc` is the foundation's document sub-allocator, not a CREATENEWDOCUMENT contract, so it does not stray into ASN-0103 territory.

VERDICT: REVISE
