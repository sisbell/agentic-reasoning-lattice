# Channel Assignment — ASN-0097 review-5

**Date:** 2026-05-24 12:40

## Issue 1: Π15a's stratified-S3 axioms modify a foundation invariant
Reason: The fix requires both design intent on whether M(d) was meant to be subspace-stratified (Nelson) and implementation evidence on what the running system actually permits in M(d)'s range (Gregory).
Nelson question: Was the design intent for M(d) to be subspace-stratified — text-subspace V-positions arranging content addresses and link-subspace V-positions arranging link addresses — or was M(d) intended to range exclusively over content addresses?
Gregory question: Does the udanax-green implementation allow a document's arrangement to reference link addresses (e.g., for link-subspace V-positions), and if so what referential-integrity invariant does it enforce across the subspaces?

## Issue 2: Proof justification by "consultation evidence"
Reason: This is an editorial fix derivable from the ASN — remove the empirical appeals and label the underlying premises as local axioms. The substantive grounding of those premises is handled under Issues 1 and 7.

## Issue 3: Π4 invokes an undeclared external interpretation function
Reason: The fix is to name the role-by-index function and cite ASN-0043's L7 (a stated foundation in this work); this is derivable from existing ASN content without external consultation.

## Issue 4: Empty endset / empty coverage boundary unaddressed
Reason: The fix requires knowing whether the design admits empty endsets (Nelson) and whether the implementation enforces a non-emptiness precondition at link creation (Gregory).
Nelson question: Did Nelson's design intend MAKELINK to admit endsets with no spans or with all-zero-width spans (yielding cov(e) = ∅), or was an endset always required to denote at least one I-address?
Gregory question: Does udanax-green's link-creation primitive reject endsets whose span tuples are empty or whose spans all have zero width, or does it accept such endsets without precondition failure?

## Issue 5: R13 (CCR-conditional) not exemplified in the worked example
Reason: The fix constructs two sub-traces directly from CCR-restricted and CCR-open as already defined in the ASN; no external evidence is needed to exhibit the divergence.

## Issue 6: Heavy reliance on cross-ASN labels with no foundations listed in this review
Reason: The fix establishes ASN-0036/0043/0047 as declared foundations or restates load-bearing contracts inline; both options draw on already-available foundation ASN content and need no external consultation.
