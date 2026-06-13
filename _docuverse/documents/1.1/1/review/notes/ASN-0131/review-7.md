# Review of ASN-0131

I checked the operation's definition, the touch relation, the decidability argument, the worked instance computation, the union-distributivity proof, the discovery-side selection equation, the weakest-precondition for contraction-stability, the retraction dynamics, and the full transition taxonomy. The mathematical content holds.

A few load-bearing arguments I verified in detail, since they recur:

- **The field-segment agreement argument** (`θ ≼ c ⟹ E(θ)₁ = E(c)₁` for T4-valid element-level `θ`, `c`), used for `e₃` in the worked instance and again for the retraction emitter's to-set in RE-RET, is sound: `θ`'s three zeros pin down `c`'s three zeros (since `zeros(c) = 3`), forcing `c`'s element field to start at the same position, and `z₃ < #θ` (from `θ_{#θ} ≠ 0`) guarantees the agreement covers the subspace-identifier position. The note's distinction from T7 (which gives distinctness, not non-prefix) is correct, as is its observation that the "all extensions carry the identifier" reading fails on T4-invalid extensions.

- **The worked instance** is arithmetically correct: `a₄ = shift(a₂, 2) = a₂ ⊕ δ(2, #a₂)`, so the first span of `e₁` covers `[a₂, a₄)` ⊇ `{a₂, a₃}` (exclusive at `a₄`); `a₁ ⋠ a₂` so `e₂` misses; and the `(1, e₁)` result correctly exercises RE-OVL (straddling endset surfaced), RE-CLIP (touching span returned unclipped), RE-WHOLE (the out-of-region `a₄` span retained), and RE-UNIT (`ℓ₁`, `ℓ₂` collapse to one pair).

- **RE-CWP** is genuinely the weakest precondition: `RE(Σ') ⊆ RE(Σ)` holds unconditionally under contraction (`I_R ⊆ image(Σ)` via F-IMG-CONTR), and the implication `coverage(e) ∩ Δ ≠ ∅ ⟹ coverage(e) ∩ I_R ≠ ∅` correctly captures "no pair dropped" after rewriting `coverage(e) ∩ image(Σ) ≠ ∅` against the disjoint decomposition `image(Σ) = I_R ⊎ Δ`. The `R = ∅` boundary correctly collapses to `RE(W,d,Σ) = ∅`.

- **RE-RET's deduplication subtlety** is handled correctly: the retraction step both nullifies `ℓ` (R6a, permanent) and emits `b`, but under the seating discipline `b` carries no content-touching endset, so a pair leaves iff `ℓ` was its sole addressable bearer. The note is admirably explicit that `coverage(R) ∩ dom(Σ.C) = ∅` for the *type* slot is an imposed layer convention, not a derivation — the to-set disjointness *is* derived, the type-set disjointness is disciplined.

- **The transition taxonomy is complete and correct**: all of {K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ} are classified, and the underlying observation — that only K.λ touches `Σ.L`, hence only K.λ moves `addressable`, while only content-subspace arrangement edits move the image — is sound. K.μ⁺_L correctly leaves a content-region image fixed because its added `s_L` position lies outside `W ⊆ s_C`.

- **RE-SEL** correctly identifies that RE is `findlinks_V ∩ addressable` — a genuine refinement of the bare discovery query, which does *not* exclude nullified links. The existence/discovery reconciliation (discovery on query-mode, existence-of-anchoring on deliverable) is a coherent and non-circular framing.

All references are to foundation ASNs; no notation is reinvented; the content-region image machinery and the existence/discovery taxonomy are cited (F-IMG, D-PRES/D-NONMONO/D-ZERO) rather than rebuilt. The decidability argument correctly tests each member of the finite image `I` against `coverage(e)` rather than treating `I` as an interval union. Boundary cases (empty image, no addressable links, empty endset slot, freshly registered document) are all addressed.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Whole-endset vs touching-spans surfacing (Open Question 1)
**Why out of scope**: RE-WHOLE is the adopted convention and is explicitly held provisional; the load-bearing invariant RE-CLIP is settled under either reading. Choosing between the two is a separate design commitment, correctly deferred.

### Topic 2: Multiplicity preservation across links sharing an endset value (Open Question 2)
**Why out of scope**: RE-DEF commits to collapsing identical (slot, endset) pairs, and the ASN is internally consistent under that choice. Whether multiplicity *ought* to be preserved is a reflective question about the chosen semantics, not a defect in the current definition.

### Topic 3: Rendered V-position mode (Open Question 3)
**Why out of scope**: The ASN returns content-identity endsets; rendering surfaced anchoring into the querying document's V-positions is V-order display territory (ASN-0082), correctly deferred.

### Topic 4: Intersection-distributivity (Open Question 4)
**Why out of scope**: The union half is derived (RE-UDIST); intersection genuinely fails to distribute under the non-injective arrangement (M13/M14), so it is a separate question, correctly left open with a structural reason given.

### Topic 5: Link store not co-resident with the queried document (Open Question 5)
**Why out of scope**: Completeness against a distributed/replicated link store is BEBE territory, correctly deferred.

### Topic 6: Link-subspace regions (Open Question 7)
**Why out of scope**: The precondition `W ⊆ s_C` is a stated caller obligation; relaxing it to `s_L` regions reopens the retraction-emitter analysis (the to-set would meet the image), correctly identified and deferred.

VERDICT: CONVERGED
