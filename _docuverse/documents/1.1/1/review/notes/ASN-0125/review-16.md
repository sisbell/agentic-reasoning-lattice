# Review of ASN-0125

The technical core is sound. I traced the operation contracts (EL6, EL7), the discipline-maintenance induction (EL-DM), the wp arguments inherited from ASN-0086, and the discovery characterisations (EL11), and verified the worked example arithmetically (the H/P chain `s_L.1…6`, the standoff `current(ℓ₀) = ∅`, the post-demotion `current(ℓ₀) = {ℓ₀}`). EL0's `wp = false` is a clean closure of L12; EL1's intent-invisibility and EL2's carrier-elimination are airtight; EL10's position-reuse construction and EL13's cross-home commutation both check out. Operations are precondition-complete and the K.λ-only composites are correctly shown valid. I found no correctness gap, no missing boundary case (empty store, single link, `x = y`, retraction-valued `ℓ'`, fork, standoff are all covered), and no drift into implementation mechanics. The findings below are scoped to one under-proved existence claim and one accreted defensive aside.

## REVISE

### Issue 1: EL9(2) de-listing existence is asserted, not constructed
**ASN-0125, EL9 (ThreeAxes), axis (2)**: "K.μ⁻ de-lists (existence: contract the link subspace below a's position and re-extend the survivors in order — each re-seating satisfies K.μ⁺_L's precondition in turn, and D-SEQ★ shapes the result)"

**Problem**: This is a one-line justification standing in for a multi-step construction, and it glosses the structurally load-bearing fact. K.μ⁻'s retention set is a position-*prefix* `{[s_L, 1], …, [s_L, n'_{s_L}]}` (ASN-0047, per-subspace scope) — it can only drop a *suffix*. So de-listing a link `a` sitting at a non-last position `[s_L, j]` is not surgical: it forces dropping `a` together with every link at positions `> j`, then re-seating those survivors via successive K.μ⁺_L, which relocates each to `[s_L, j], [s_L, j+1], …` (shifted down by one). The phrase "contract the link subspace below `a`'s position" hides that the contraction necessarily takes the whole suffix, and "each re-seating satisfies K.μ⁺_L's precondition in turn" asserts the survivor re-extension without exhibiting it. The claim "listing is mutable in both directions" depends on this middle-link case (the last-link and only-link cases are the trivial ones), so the gloss is exactly where a reader stumbles. This is a "claim derived in one sentence that requires a multi-step argument."

**Required**: Show the construction for the general (middle-link) case — make explicit that K.μ⁻ drops the position-suffix from `j` onward and that the `n − j` survivors are re-seated in order by K.μ⁺_L (each satisfying `origin(ℓ) = d ∧ ℓ ∉ ran(M(d)) ∧ v_ℓ = shift(max(V_{s_L}(d)), 1)`), with the resulting position shift noted (consistent with EL10). Alternatively, scope the claim to what is being demonstrated.

### Issue 2: EL7(vi) defensive aside about a precondition-excluded self-reference
**ASN-0125, EL7 (EditContract), clause (vi)**: "so the new claim at a' conforms to Df-DISC(ii) at Σ₁ (and since a' ∉ dom(Σ.L) is fresh, neither witness is a' — the new claim references two genuinely pre-existing links, never itself)"

**Problem**: The parenthetical is appended *after* conformance is already established, and it is not consumed by the conformance argument — Df-DISC(ii) needs only `x, y ∈ dom(Σ₁.L) ∧ x ≠ y`, which the preceding clause supplies. It derives a fact ("neither witness is `a'`") about a self-reference case that `DC(ℓ')` already excludes (the witnesses are pinned at `Σ`, so `x, y ∈ dom(Σ.L)`, and `a'` is fresh against `dom(Σ.L)`). This is the reviser-drift pattern the anti-bloat mode flags — prose that imagines a case the precondition already excludes — and a precise reader following the conformance chain must register and discard it. It is a small, isolated instance, but it is the kind that compounds across cycles, so it is worth removing at source.

**Required**: Drop the parenthetical; `x, y ∈ dom(Σ.L) ⊆ dom(Σ₁.L)` with `x ≠ y` is the complete conformance witness.

## OUT_OF_SCOPE

None. EL11's discoverability machinery, EL16's reference-survival, and EL9/EL10's listing analysis are all intrinsic to specifying what editlink does to the original and the relationship — not general link discovery, and not document operations re-specified. The eight Open Questions correctly defer genuinely new territory (cross-asserter retraction authority, endset-level correspondence under reshaping, edit/listing coupling).

VERDICT: REVISE
