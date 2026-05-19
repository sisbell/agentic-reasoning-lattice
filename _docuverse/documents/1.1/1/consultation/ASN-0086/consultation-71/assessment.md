# Channel Assignment — ASN-0086 review-71

**Date:** 2026-05-19 16:03

## Issue 1: Variable name collision in Worked Sketch
Reason: Pure editorial rename — pick an unused symbol for the Step 3 link address. No design or implementation question is involved.

## Issue 2: A_R^{Σ_3} computation omitted from Worked Sketch
Reason: The missing computation follows directly from the Definition of `A_K` applied at the `R` coverage class with `nullified(Σ_3)` already computed in the sketch. Fully derivable from the ASN's own content.

## Issue 3: R5-Cor's invariant enumeration omits L14a's per-call discharge mechanism
Reason: R0's proof in this same ASN already carries the L14a discharge argument explicitly (via S3 + ASN-0093 L0 + SC-NEQ). The fix is restating or inheriting that argument in R5-Cor — internal to the ASN.

## Issue 4: R7a's L1c discharge at replay step needs explicit construction
Reason: ASN-0093's SubAllocatorAxiom already axiomatizes chain existence as a structural consequence of `d ∈ dom(M)`, and the ASN cites this. The fix is one clarifying sentence that L1c's witness is structural (tumbler-only), not trajectory-dependent — derivable from existing citations.

## Issue 5: R0a-Cor2 offers two equivalent routes without selecting one
Reason: Editorial consolidation — choose one canonical route (Route A is more foundational via TA5) and demote the other to parenthetical. No external input needed.

## Issue 6: Definition of nullified — A_rel restriction scope rationale leaves edge case open
Reason: The question is whether excluding retraction-to-document/content/ghost reflects Ted Nelson's design intent for what retraction means in the link model — content immutability and document-as-arrangement vs. link-as-claim is a design-layer distinction that benefits from theory-channel grounding.
Nelson question: In Nelson's design, is retraction conceived as a withdrawal operation that applies specifically to *link claims* (excluding content and documents), or was retraction intended to operate uniformly over any addressable entity?
