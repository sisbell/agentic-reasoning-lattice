# Channel Assignment — ASN-0097 review-4

**Date:** 2026-05-24 11:17

## Issue 1: Π15a's S3 invocation contradicts the worked example's d_link setup
Reason: Resolution hinges on whether S3's referential integrity was designed and implemented as global (ran(M(d)) ⊆ dom(C)) or as subspace-specific (separate constraints for text and link subspaces). Need design intent from Nelson and implementation evidence from Gregory to know which formulation the ASN should commit to.
Nelson question: Was the arrangement map M(d) designed to be subspace-stratified — with referential integrity stated per-subspace (M(d)|_text ⊆ dom(C) and M(d)|_links ⊆ dom(L)) — or was a single global constraint ran(M(d)) ⊆ dom(C) intended, in which case link subspaces are arranged differently?
Gregory question: In udanax-green, how is the link subspace of a document arranged — does the V→I map for the link subspace point into the link store's address space, and is it implemented as a separate map or as a typed range within a unified arrangement?

## Issue 2: Π15a's two-part freshness argument is conflated by "either"
Reason: The underlying facts — K.λ allocator freshness and dom(L) ∩ dom(C) = ∅ via L14/L0a — are already established in ASN-0043 (already cited). The fix is purely expository decomposition of the chain.

## Issue 3: The "I-side equivalent of reach" is used as a lemma without being labeled
Reason: Purely structural promotion of an already-proved equivalence to a labeled claim. The proof is present; only the label and table entry need to be added.

## Issue 4: Π4's proof asserts negations about transitions rather than deriving them
Reason: Π0, Π2, and L6/L7 (already cited in the original Π4 paragraph) are sufficient to derive directional permanence as a tuple-equality consequence. The fix is internal rephrasing from "no transition does X" to "Π0/Π2 forces tuple preservation; L6/L7 makes role a function of slot position."
