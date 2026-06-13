# Review of ASN-0125

I reviewed this as a derived-composite specification: the question is whether EDITLINK's two postconditions (`R_mut`, then the weakened `R₁`/`R₂`) are correctly shown unachievable/achievable, whether the two allocations and the discipline-preservation arguments are complete, and whether the foundation/layer citations are used soundly. I checked the load-bearing proofs line by line rather than accepting the prose.

**What I verified holds:**

- **EL0** — the invariant `J ≡ a ∈ dom(L) ∧ L(a) = ℓ₀` is genuinely inductive: the framed transitions (Vocabulary fact V is complete — I confirmed each of K.α/K.δ/K.μ⁺/K.μ⁺_L/K.μ⁻/K.ρ/K.μ~ carries `L' = L`) and the single K.λ case (freshness ⟹ `ℓ_f ≠ a`) exhaust the closed vocabulary. The `wp = false` conclusion follows.
- **EL4** — the per-claim derivation `coverage(F) ∩ dom(Σ.L) = {x}` correctly leans only on PrefixSpanCoverage + R0a (antichain), so the "no whole-state hypothesis" qualifier is earned, and the accessors are total on `Ŝ^Σ` at every reachable state.
- **EL6/EL7** — the frame is genuinely total (both steps are K.λ, which frames C, M, E, R), the two-emission distinctness chains correctly, and the conditional `nullified` frame is right: the *unconditional* `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` needs only "no R-tuple added," while the *full* equality correctly invokes edit-discipline + R0a (wp Case 2's third conjunct). I confirmed EL7(iv)'s citation of EL7(vi) is not circular (EL7(vi) depends on `DC(ℓ')` and EL6(v), not on EL7(iv)).
- **EL11(a)** — the content-address exclusion (a `t ≽ old(e)` would force `E(t)₁ = s_L` against C1/L0/SC-NEQ) is correct, so `coverage(G) ∩ ran(M(d)) = {old(e)} ∩ ran(M(d))`, and the biconditional with `listed` holds.
- **EL13** — the cross-home commutation checks out: each home's emission set is untouched by the other, so `a_emit` is stable across reorder and the map-unions commute; the per-home/per-document-chain refinement (and its honest disclaimer about per-principal "latest") is exactly right.
- **EL14(c)** — the empty-`current` standoff is correct under Df-DIR's `(old, new)` ordering: claims `(y,x)` and `(x,y)` make `reach_o(y) = {y,x}` sink-free.
- **Worked example** — I traced every address (`ℓ₁ = H.0.s_L.2`, `c₁ = .3`, `ℓ₂ = P.0.s_L.1`, `r₁ = H.0.s_L.4`, `c₃ = .5`, `r₂ = .6`), every `a_emit` branch, and the position-reuse step; all consistent, and the cross-principal `Nullify(H, c₂)` is correctly admitted under P-tgt.

**Boundary/operation checks:** value-identical edit, third-party edit-by-fork, revert (claim-only, no successor allocation), first/last/sole listing positions in EL9(2) and EL10, and cycles vs. irreflexivity in Df-DISC are all handled. The layer-transfer meta-argument (ASN-0086 facts ride on "L grows only by fresh K.λ" + "dom(M) monotone") is sound, and EL6(iv) re-derives the one fact that doesn't transfer verbatim (wp Case 2's disciplined simplification) rather than borrowing ASN-0086's layer-reachability. All ASN citations are to listed foundations.

**Two compressions I checked and found non-blocking** (not REVISE items): EL9(2)'s de-listing is a sound existence construction (contract link-subspace below `a`, re-seat survivors by iterated K.μ⁺_L); and EL11(b)'s identification of `in(y)`/`out(x)` with `Observe_{K_sup}` is exact for `y ∈ dom(L)` — the operative domain — via R0a (`old(e) ≼ y ∧ both ∈ dom(L) ⟹ old(e) = y`), and the sets are computable directly from the `old`/`new` accessors regardless, so no downstream claim depends on the identification's universal reading.

## REVISE

None. The proofs are complete, the operations are fully framed, the edge cases (empty/first/last/cycle/value-identical/third-party) are covered, the derivations are explicit, and the worked example verifies the key postconditions concretely.

## OUT_OF_SCOPE

None. The ASN explicitly declines link creation, discovery, and read operations, and uses only foundation operators (`Observe_K`, the LP-projection lemmas) where a reader capability is named — it defines no machinery for the listed out-of-scope topics. The eight Open Questions are properly deferred (cross-principal retraction authority, meta-claim stratification, supersession/retraction independence under other disciplines, etc.) and are future-ASN territory, not gaps in this one.

VERDICT: CONVERGED
