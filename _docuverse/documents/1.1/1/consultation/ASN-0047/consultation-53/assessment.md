# Channel Assignment — ASN-0047 review-53

**Date:** 2026-05-16 17:26

## Issue 1: S9 listed in per-state invariants but is structurally per-transition
Reason: Pure formal typing fix — S9's quantification in ASN-0036 is over transition pairs, parallel to S0/S1 which the ASN already correctly placed in ExtendedTransitionInvariants. Internal to the ASN.

## Issue 2: K.δ case (ii) precondition does not explicitly require t to be in E
Reason: The condition is already implicit in "previously allocated" and required for the T10a GlobalUniqueness chain the ASN cites. Fix is to surface the existing implicit precondition as a formal conjunct. Internal.

## Issue 3: K.δ k=1 sub-case restriction to documents is in prose, not in the precondition
Reason: The restriction is already justified in the ASN with both Nelson (LM 4/29) and Gregory (`docreatenewversion`) citations; only the formal precondition list needs the conjunct added. Internal formalization.

## Issue 4: K.α precondition does not list `a ∉ dom(C)` as a direct conjunct
Reason: Freshness is derivable from SubAllocatorAxiom/GlobalUniqueness as the ASN already explains, and K.λ states the parallel condition directly. Symmetry/presentation fix internal to the ASN.

## Issue 5: K.μ⁻ admissibility precondition's derivation duplicates D-SEQ★ structure
Reason: Pure reorganization — either reorder the section so D-SEQ★ precedes K.μ⁻, or restate K.μ⁻'s precondition as a structural quantification deferring the proof. No external evidence required.

## Issue 6: K.μ~ link-subspace identity clause justification (Claim A / Claim B) overlaps
Reason: Presentation/compression issue. The ASN already establishes CL-UNIQ as a per-state invariant; the question is how much detail to retain for the consistency check. Internal restructuring.

## Issue 7: ExtendedTransitionInvariants conflates S0/S1 with their subsumer P0
Reason: Notational redundancy the ASN itself flags in the proof body; fix is to drop one of {S0 ∧ S1} or P0 from the conjunction. Internal.
