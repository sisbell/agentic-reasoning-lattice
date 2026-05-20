# Channel Assignment — ASN-0094 review-7

**Date:** 2026-05-19 21:57

## Issue 1: ShapeWellFormedness biconditional reading is awkward and requires disambiguation prose
Reason: Pure notational/presentation fix — replacing the biconditional with two explicit implications. The semantics are already fully specified in the ASN; no design intent or implementation evidence is required.

## Issue 2: Sh4 layer-discipline contract operates on potentially undefined inputs
Reason: Specification ordering fix between Sh-conf gates and the layer contract. The choice is internal to the framework's own design; both options the reviewer offers are derivable from the ASN's existing structure.

## Issue 3: FunctionalDependencyDiscipline preservation delegated by hand-wave
Reason: Proof completion task — either execute Cases A/B/C explicitly under the C_fd substitution or extract an invariance lemma. The proof material is already present in Sh4's argument; the fix is to make the FDD adaptation explicit.

## Issue 4: A_doc/A_rel naming inherited from ASN-0086 conflicts with prose "document" usage
Reason: Terminology clarification using ASN-0086's already-established definitions (A_doc = dom(Σ.C), distinct from dom(Σ.M)). The fix is a single clarifying sentence pointing to existing dependency content.

## Issue 5: Multi-slot Observe_K over-approximation generalized implicitly
Reason: Proof elaboration — spelling out the per-element generalization of an argument already justified for the single-slot case. AllocatedAddressAntichain and Sh-conf (d) are both already proved in the ASN.

## Issue 6: No worked example exercises `c_F = *` with non-empty F
Reason: Adding a worked example demonstrating already-specified Retraction-shape mechanics. The framework's `(*, 1, A, A_rel, ⊤)` shape is fully defined; the example just exercises existing structure.

## Issue 7: K = comment worked example does not derive emission addresses
Reason: Mechanical computation using K.λ's first/subsequent emission rule from ASN-0086, which is already cited. The Coverage walkthrough already does this derivation at the required level of detail.

## Issue 8: "(b')" reference in Sh5 status is an undefined editing artifact
Reason: Typo fix — replace `(b')` with `(b)`. No external input required.
