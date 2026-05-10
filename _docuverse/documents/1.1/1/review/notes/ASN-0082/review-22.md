# Review of ASN-0082

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Straddling spans under insertion shift
I3-S establishes width preservation for spans entirely within the shifted region (s ≥ p). A span that straddles the insertion point — partially before p, partially at or beyond — would need to be split at p (via S4, ASN-0053) before each piece can be shifted independently. This composition of S4 with I3-S belongs in the INSERT ASN that fills the gap, not here.
**Why out of scope**: I3-S is the atomic span-shift property; composing it with split is a downstream operation-level concern.

### Topic 2: Contraction generalization beyond depth 2
The scoping axiom (#p = 2) restricts the contraction to single-component ordinals, where TA4's zero-prefix condition is vacuously satisfied. At ordinal depth ≥ 2 (V-position depth ≥ 3), D-SEQ positions have the form [S, 1, ..., 1, k], so ord(p) = [1, ..., 1, p_m] — the zero-prefix condition (A i : 1 ≤ i < k : a_i = 0) fails because the intermediate components are 1, not 0. The OrdinalAdditiveCompatibility machinery already works at all depths, so the gap is specifically in the subtraction round-trip for contraction. This is correctly identified in the open questions.
**Why out of scope**: The current depth-2 treatment is self-consistent; deeper ordinals require new algebraic results (or a restructured proof avoiding TA4), which is future work.

VERDICT: CONVERGED
