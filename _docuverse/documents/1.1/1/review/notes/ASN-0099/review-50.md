# Review of ASN-0099

## REVISE

### Issue 1: A1b's premise that K.μ⁺ and K.μ⁻ omit `L` from their published frames is false in the operative (extended-state) vocabulary

**ASN-0099, A1 / A1b / Appendix**: "Five of the eight non-allocating operations list `L' = L` in their published frames ({K.σ, K.α, K.δ, K.μ⁺_L, K.ρ}); two atomic operations (K.μ⁺, K.μ⁻) omit `L` from the published frame." A1b then derives their link-store inertness from a "closed-world reading … not formally axiomatise[d]" and the entire appendix is built to justify this.

**Problem**: This ASN operates in the extended state `Σ = (C, L, M, E, R, …)`, so the operative definitions of K.μ⁺ and K.μ⁻ are ASN-0047's **amended** versions, not the pre-link-subspace originals. Both amended frames publish `L' = L` explicitly:

- *K.μ⁺ amendment — ContentSubspaceRestriction*: "*Frame (extended state):* `C' = C; L' = L; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`."
- *K.μ⁻ (per-subspace scope) — PerSubspaceContractionScope*: "1. The link-store frame clause `L' = L` is added. … *Frame (extended state):* `C' = C; L' = L; E' = E; R' = R; …`."

So K.μ⁺ and K.μ⁻ are A1a (published-frame) operations, not A1b (closed-world) operations. The count is wrong (seven atomic ops publish `L' = L`, not five), and the closed-world reading, the convention-grounded tag on A1b, the appendix, and the dozens of "inherits A1b's commitment" annotations threaded through F9, F9~, F9-cor, F9★, F17, F18 are all built on a false premise. This is the same reclassification the project already applied to K.ρ (recent commit "reclassify K.ρ from A1b closed-world to A1a published-frame") — the pattern was simply not carried through to the amended K.μ⁺/K.μ⁻ frames.

**Required**: Move K.μ⁺ and K.μ⁻ into A1a, citing their amended extended-state frames' explicit `L' = L`. With that, A1b becomes empty among the atomic operations (only K.μ~ remains, and it is non-atomic and reached via its K.μ⁻+K.μ⁺ decomposition, both now A1a). Drop or drastically reduce the appendix and the per-claim "inherits A1b's commitment" tags, since no convention-grounded reading is needed once the published frames are read correctly. If the intent was to reason about the *unamended* operations, state explicitly why the unamended frames are operative here despite the extended state — but that would contradict ASN-0047's ValidComposite★, which lists "K.μ⁺ (amended)" and "K.μ⁻ (amended)" as the vocabulary.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
