# Review of ASN-0081

## REVISE

### Issue 1: OrdinalDisplacementProjection missing formal precondition and postcondition parity with peer definitions

**ASN-0081, Ordinal Extraction — OrdinalDisplacementProjection**: "For a V-depth displacement w with w₁ = 0 and #w = m, the *ordinal displacement* is: w_ord = [w₂, ..., wₘ] of depth m − 1."

**Problem**: The definition lacks a formal `*Precondition:*` block and its `*Postcondition:*` block is incomplete relative to the peer definitions in the same section. Compare:

- **ord** has `*Precondition:* #v ≥ 2` and `*Postconditions:* ord(v) ∈ T with #ord(v) = #v − 1 ≥ 1`.
- **vpos** has `*Preconditions:* #o ≥ 1, S ≥ 1` and `*Postconditions:* vpos(S, o) ∈ T with #vpos(S, o) = #o + 1`.
- **w_ord** has no `*Precondition:*` block at all, and its postcondition states only `w_ord > 0` (conditional on `w > 0 ∧ w₁ = 0`), omitting `w_ord ∈ T` and `#w_ord = #w − 1`.

The critical missing precondition is `#w ≥ 2`. When `#w = 1`, the construction produces the empty sequence, which is not in T (T0 requires length ≥ 1). The scoping axiom (`#p = 2`, `#w = #p`) prevents this within the contraction, but the definition is stated in the general Ordinal Extraction section *before* the scoping axiom is introduced — it should be self-contained.

**Required**: Add a formal precondition and expand the postcondition to match peer definitions:

- `*Preconditions:* #w ≥ 2, w₁ = 0.`
- `*Postconditions:* w_ord ∈ T, #w_ord = #w − 1 ≥ 1. When w > 0, w_ord > 0.`

## OUT_OF_SCOPE

### Topic 1: Generalization to ordinal depth > 1
**Why out of scope**: The ASN explicitly scopes to `#p = 2` (single-component ordinals) and lists the deeper case as an open question. The TA4 zero-prefix condition and TA3-strict equal-length precondition are both trivially satisfied at depth 1; the multi-component case requires separate analysis of when these hold, which is genuinely new work.

### Topic 2: Compositional properties of sequential contractions
**Why out of scope**: The ASN specifies one contraction and verifies invariant preservation, which means the post-state is a valid pre-state for a subsequent contraction. But commutativity, associativity, or optimal ordering of multiple contractions is a separate algebraic question.

VERDICT: REVISE
