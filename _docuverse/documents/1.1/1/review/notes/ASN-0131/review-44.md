# Review of ASN-0131

I checked the definition, every introduced claim, the worked instance, both wp derivations, and the stability case analysis against the foundations. The core is sound. Below I record the load-bearing verifications and the few places I pressed hardest, none of which yielded a defect.

## REVISE

None. Details of what was checked:

**Definition and selection.** `RE(W, d, Σ) = {(i, e) : (∃ a ∈ addressable(Σ) : … ∧ Σ.L(a).eᵢ = e ∧ touch_W(e))}` is well-formed; the reformulation `RE = {(i, e) ∈ Avail(Σ) : touch_W(e)}` is valid because `touch_W(e)` depends only on `e` and so factors out of the existential. `I ⊆ dom(Σ.C)` from `subspace(v) = s_C` + S3★ (ASN-0047) is correct. RE-BND's three boundary reads (empty image, no addressable links, empty slot via `coverage(∅) = ∅`) are exact reads of the definition.

**Worked instance.** Verified `a₂ ⊕ δ(2, #a₂) = shift(a₂, 2) = a₄`, so the first span of `e₁` denotes `{t : a₂ ≤ t < a₄} ⊇ {a₂, a₃}` (exclusive at `a₄`); the `coverage(e₃) ∩ dom(Σ.C) = ∅` separator-zero argument is sound (θ's three zeros land on any extending content `c`, forcing `E(c)₁ = E(θ)₁ ≠ s_C`); the five touch tests resolve to `RE = {(1, e₁)}`, and each postcondition (RE-OVL, RE-CLIP, RE-WHOLE, RE-UNIT) is genuinely exercised.

**RE-UDIST / RE-SEL.** Image distributes over union unconditionally; `touch_{W₁∪W₂} = touch_{W₁} ∨ touch_{W₂}`; `Avail(Σ)` is region-independent — union-distributivity follows. The intersection-failure note (via M13/M14 non-injectivity) is correctly stated as `⊆` with possible strictness. `sel(W,d,Σ) = findlinks_V(W,d,Σ) ∩ addressable(Σ)` checks out against F-V/F-FIND/F-MATCH.

**RE-CWP.** Re-derived: post-image `= I_R`, `Avail` fixed by the frame, so `RE(Σ') ⊆ RE(Σ)`; equality reduces (using `image = I_R ⊎ Δ`) to `coverage(e) ∩ Δ ≠ ∅ ⟹ coverage(e) ∩ I_R ≠ ∅`; boundary `R = ∅` collapses to `RE(W,d,Σ) = ∅`. Matches the claim.

**RE-RET.** Both halves verified under the net-removal hypothesis: forward (sole bearer ⟹ drop) from R6a + emitter `b` surfacing nothing; backward (other bearer ⟹ survive) from R-Scope confining nullification to `ℓ` so any `ℓ' ≠ ℓ` stays addressable with value/image fixed. The from/to content-disjointness via the unit-depth prefix argument is sound; the type-slot `Θ` exception is correctly carried as a hypothesis (OQ6), and the forward direction is correctly flagged as resting on it.

**Points I pressed hardest, and why each holds.**

- *The insert/delete M-only lift and its depth asymmetry.* I3 (insert) is genuinely M-only — its frame (content-unchanged, cross-doc-unchanged) leaves `Σ.M(d)` as the only write, so the lift's "frames L, E, R" is justified, not asserted; insert holds at every text depth `#p ≥ 2`, delete (D-SHIFT) only at `#p = 2`. The note does not overclaim a higher-depth interior delete and correctly routes higher-depth contraction through `K.μ⁻`/RE-CWP. The depth-independence-of-reasoning vs. bounded-delete-stability split is precise.
- *The cross-model bridge to ASN-0086.* "Every ASN-0086 lemma constraining `Σ.L` alone transfers" is sound: every non-K.λ ASN-0047 transition frames `Σ.L`, so `Σ.L`-only invariants (R0a) and step-properties (R6a) hold inductively across the larger vocabulary. This also justifies the note re-establishing wp Case 2's third-conjunct discharge via the transferable R0a rather than citing ASN-0086's `layer-reachable`-scoped disciplined simplification — the simplification is not `Σ.L`-only, so the re-derivation is deliberate, not redundant.
- *RE-WHOLE provisionality propagation.* RE-DEF correctly localizes its provisional part (the returned value, not the selection or name-withholding); RE-SND/RE-CMP are sound for the adopted definition.

## OUT_OF_SCOPE

The note's seven Open Questions and its Scope section bound future territory appropriately (touching-spans extent, multiplicity, rendered V-order, intersection-distributivity, non-co-resident stores, type-slot/content match, link-subspace regions). It cites ASN-0127's image machinery and existence/discovery taxonomy rather than rebuilding them, and cites ASN-0098's projection lemmas rather than re-deriving — no scope violation. I have no additional future-territory topic to add.

META: not applicable — the note specifies an abstract operation (state read, pure-query semantics, soundness/completeness/stability guarantees) that any RETRIEVEENDSETS implementation must satisfy, so it remains squarely a specification ASN.

VERDICT: CONVERGED
