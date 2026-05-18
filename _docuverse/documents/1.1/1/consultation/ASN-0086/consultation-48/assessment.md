# Channel Assignment — ASN-0086 review-48

**Date:** 2026-05-18 03:09

## Issue 1: R7a proof doesn't handle multi-emission composites in `↝`
Reason: The fix is internal — the ASN's own definition of `↝` admits multi-emission composites by construction (union over higher-layer operations), and the proof can be adapted by either restricting domain or generalizing to a finite sequence of class-(iii) steps using existing Frame conditions.

## Issue 2: R0 Step 4 bundles invariants with incorrect justification
Reason: The fix is internal — the correct preservation mechanism for L12/L12a/L12b/L-fin is already stated in the class-(iii) Frame's value-preservation clause and single-key extension structure, and only the ASN-0036 S-invariants follow by `(Σ.C, Σ.M)`-substitution as the review correctly diagnoses.

## Issue 3: Meta-prose accumulation around forward references
Reason: Editorial cleanup — the redundant text and forward references can be removed using the ASN's existing per-claim conditionality tags and substantive content; no external context needed.

## Issue 4: R0a Stage 1's "covered by the same argument with roles swapped"
Reason: The fix is internal — the symmetry of the cross-home derivation in `(a, a', d, d')` is structurally present in the existing proof and just needs an explicit sentence naming it (or parameterized rewriting).

## Issue 5: R0a-Cor1 induction step doesn't handle the new-document class-(i) case explicitly
Reason: The fix is internal — the class-(i) frame conditions and the contiguous-prefix invariant already establish that `J_{d_new}^{Σ'} = -1` for fresh documents; adding the case sentence is purely a proof completion.

## Issue 6: Emit_K case B seed-independence depends on discipline-conditional R0a-Cor1
Reason: The fix is internal — all three reviewer-proposed options (precondition, domain restriction, weakened claim) use the `→_D*` reachability vocabulary already defined in R0a, and the basic correctness adjustment is a presentation choice not requiring external input.

## Issue 7: SharedDepthOneAllocator lemma — naming allocators before subspace labels are pinned
Reason: The fix is internal — T10a's allocator-opening semantics (an allocator exists when its first spawn fires) is foundational in ASN-0034, and the conditional-vs-unconditional existence clarification can be derived from those rules together with the substrate's emission history.

## Issue 8: `Σ_0` in R0a's hypothesis — implicit initial-state assumption
Reason: The fix is internal — both reviewer options (making the empty-link-store assumption explicit, or restructuring the induction base) are self-contained modifications using the ASN's existing `→_D*` reachability vocabulary and the `→` definition's single-step structure.
