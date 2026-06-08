# Review of ASN-0110

I reviewed the touching semantics, the return-shape claims (witness set, role families, arity), the proofs of the derived lemmas, the worked instance, and the V-side reduction. I checked boundary cases (empty region, empty store, empty endset, empty interior slot, deleted V-region) and the cross-ASN references (all to foundation ASNs 0034/0036/0043/0047/0086/0093/0098/0099 — permitted).

## Findings

No REVISE items. Details of what I checked:

**Touching and decidability.** RE-touch/RE-overlap correctly reduce `coverage(e) ∩ I ≠ ∅` to a finite per-span half-open membership test; the half-open boundary note (`α = s ⊕ ℓ` excluded) is right. RE-decide grounds termination on L-fin + finite endsets + finite `I` + T2, and correctly separates the finite region `I` from the generally-infinite `coverage`.

**Return shape.** RE-result's value-keyed (not coverage-keyed) deduplication is correct and the contrast with L8's coverage-keyed `same_type` is genuine. RE-arity's `N_max(Σ)` length is region-stable and the empty-store `⟨⟩` vs non-empty `⟨∅,…,∅⟩` (RE-zero) distinction is internally consistent, with the empty-store divergence from a fixed three-slot implementation correctly isolated in RE-conform as the sole conformance gap.

**Worked instance.** Verified the arithmetic: `d` and the `cₖ`/`θ` addresses are well-formed element/document tumblers; the touching table is correct (including `c₃ ∈ [c₃,c₄)` and `c₃ ∉ [c₂,c₃)` half-open boundaries); `W = {(a₁,1),(a₂,1),(a₂,2)}`; result `⟨{F₁,F₂},{F₁},∅⟩` exercises RE-full (F₁ returned whole including the non-touching `(c₄,δ)` span), RE-role (F₁ filed under both slots 1 and 2), and RE-arity (empty slot 3 reported in position).

**Derived lemmas.** RE-mono correctly uses the multi-step LP13/LP3★ rather than resting the single-step RE-immut on a multi-step hypothesis (explicitly noted). RE-wp's witness partition (old vs fresh `ℓ_new`) is sound; the disjunction is correctly derived and the "mutually exclusive" qualifier applies to witnesses, not disjuncts. RE-anon's lower bound `max_i |Eᵢ| ≤ distinct contributing links` is sound. RE-Vside's finiteness of `image(R,d,Σ) ⊆ ran(Σ.M(d))` for arbitrary `R` via S8-fin is correct, as is the deleted-region → `I = ∅` → RE-zero chain.

RE-sound/RE-complete/RE-exact are stated without internal derivation, but this matches the accepted foundation pattern (ASN-0099 F2/F3 state Completeness/Soundness as conformance lemmas the same way); they express the implementation contract against the spec-defined `Eᵢ`, not a skipped proof obligation.

The ASN defines state-reading semantics, a pure query operation, and abstract invariants (determinism, monotonicity, additivity, survivability) without drifting into implementation mechanics. Scope boundaries (counting, V-presentation, link-by-address) are correctly deferred.

VERDICT: CONVERGED
