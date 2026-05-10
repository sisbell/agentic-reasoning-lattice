# Review of ASN-0081

## REVISE

### Issue 1: D-BJ postcondition does not formally state the bijectivity it claims

**ASN-0081, Shift Correctness (D-BJ)**: "The map σ : R → Q₃ is an order-preserving bijection."

**Problem**: The statement and registry both claim σ is a bijection, but the formal postcondition is only `σ(v₁) < σ(v₂)` — order-preservation. Injectivity is derived in a prose sentence afterward ("Order preservation implies injectivity: v₁ ≠ v₂ ⟹ σ(v₁) ≠ σ(v₂)"), and surjectivity is left implicit (by definition of Q₃). Downstream, S2-post cites "D-BJ, injectivity" to establish uniqueness of the pre-image. A formal postcondition should include every property that downstream lemmas cite.

**Required**: Expand the postconditions to:

- (a) Order-preservation: `v₁ < v₂ ⟹ σ(v₁) < σ(v₂)` (as stated)
- (b) Injectivity: `v₁ ≠ v₂ ⟹ σ(v₁) ≠ σ(v₂)` (derived from (a) by trichotomy)
- (c) Surjectivity: `Q₃ = {σ(v) : v ∈ R}` (by definition of Q₃)

### Issue 2: OrdinalExtraction and VPositionReconstruction definitions missing preconditions

**ASN-0081, Ordinal Extraction**: "For a V-position v with #v = m and subspace(v) = v₁, the ordinal is: `ord(v) = [v₂, ..., vₘ]`"

**Problem**: When #v = 1, ord(v) = [] — the empty sequence, which is not in T (T0 requires length ≥ 1). The definition needs #v ≥ 2 as an explicit precondition. Similarly, vpos(S, o) = [S, o₁, ..., oₖ] requires #o ≥ 1 to produce a result in T. The scoping axiom (#p = 2) prevents these from arising in this ASN, but the definitions are introduced as general utilities ("Per the ordinal-only formulation of TA7a") intended for reuse. A definition should be self-contained — the scoping axiom constrains the ASN's analysis, not the definition's domain.

**Required**: Add explicit preconditions:

- ord(v): Precondition `#v ≥ 2`. Postcondition `ord(v) ∈ T` with `#ord(v) = #v − 1`.
- vpos(S, o): Precondition `#o ≥ 1`, `S ≥ 1`. Postcondition `vpos(S, o) ∈ T` with `#vpos(S, o) = #o + 1`.

## OUT_OF_SCOPE

None. The depth-2 restriction is honestly scoped and the open question is well-formulated.

VERDICT: REVISE
