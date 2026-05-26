# Review of ASN-0077

## REVISE

(no items)

The ASN survives a rigorous proof-by-proof audit:

**O0 (origin extended to dom(L)):** Three-part derivation (structural well-definedness, semantic correspondence, totality/single-valuedness) is complete. The semantic correspondence for dom(L) explicitly composes three load-bearing pieces (L1c chain-seed identity, K.λ precondition, closure of dom(L) under K.λ-only with L₀ = ∅ + induction). The closure step inspects every elementary transition's effect on L. Solid.

**O2 (Block uniformity):** Both subspace cases handled. Content blocks route through M-sub(a) → S3★ → dom(C) → M16a. Link blocks route through M-sub(a) → S3★ → dom(L) → CL-OWN. S3★-aux discharges exhaustiveness. Each step explicitly discharges the precondition of the next.

**Equivalence chain (F1) ≡ (F2) ≡ (F3):** All three directions derived. The collapse (F2) → (F3) correctly uses O2 (not just M16a, which only handles dom(C)) to cover both subspaces.

**Singleton I-span argument:** All three length cases (#b < #a, #b = #a, #b > #a) are excluded by distinct mechanisms (T1 case analysis, T3 component agreement, structural K.α-emission-length argument). The zero-count balance argument for case #b > #a correctly traces: agreement on positions 1..#a → same three zeros at same positions → no zeros in #a+1..#b → document-element separator coincides → same origin → both from A_C(d) → A_C(d) outputs all have length #d + 3 (K.α uses only inc(·, 0)). The dependency on K.α's specific emission algorithm is correctly cited.

**O11/O11' (V-span preservation under K.μ⁺/K.μ⁺_L):** Both directions (⊆) and (⊇) derived. Case (ii) (newly-added v) is excluded by either subspace mismatch (C0a) or precondition (vi) contradiction (via cross-state depth identification using S8-depth for K.μ⁺ or LinkVPositionDepthAxiom's state-independence for K.μ⁺_L). The cross-state depth identification for K.μ⁺ proceeds in three explicit steps; for K.μ⁺_L it uses the axiom's universal form directly.

**Edge cases covered:** Empty intersection (I-span: well-defined ∅ result), singleton I-span (with full uniqueness argument), cross-subspace I-span (content-only by definition), V-span over link subspace (yields {d} via CL-OWN), empty document arrangement (precondition (iii) fails), empty-restriction within non-empty document (impossible by TA-strict + precondition (vi)).

**wp computations:** Two non-trivial, both load-bearing: single-origin I-span characterization and d_q-appearance V-span characterization (the discovery probe).

**Worked example:** Σ₀ → Σ₁ → Σ₂ with d₁, d₂, d₃, d₄ exercises O5, O6, O7, O9, O10. Includes a K.μ~ alternative path (Σ₁ → Σ₁') showing why K.μ~ doesn't admit an O11-style claim — origins shift from {d₁} to {d₃} after swap, refuting both directions of inclusion.

**Foundation references:** All citations are to ASN-0034, ASN-0036, ASN-0040, ASN-0047, ASN-0053, ASN-0058 (all foundation). No non-foundation cross-references. The author correctly identifies that ASN-0047's CL-OWN implicitly uses origin on dom(L), and O0 makes this explicit "on the same footing as S7."

**Depth check:** Every claim has explicit derivation chains. The "What SHOWORIGIN does not promise" section delineates three exclusions with reasoning. The Claims table records dependencies.

## OUT_OF_SCOPE

The ASN's Open Questions section appropriately enumerates future work (cross-subspace I-spans, intermediate chain reporting, native-vs-transcluded distinction, unreachable home documents, historical containment from Σ.R, intra-document multi-position sharing). These are correctly identified as separate ASNs.

VERDICT: CONVERGED
