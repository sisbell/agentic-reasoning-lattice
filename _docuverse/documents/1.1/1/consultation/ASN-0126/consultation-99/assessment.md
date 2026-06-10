# Channel Assignment — ASN-0126 review-99

**Date:** 2026-06-10 09:51

## Issue 1: The born-nullified analysis stops one inference short of the consequence its own setup establishes
Reason: Internal. Every premise of the corollary is already in play in the note or its cited ASN-0086 results — sequential `a_emit` advance via `inc(ℓ_prev, 0)`, L-ContiguousPrefix transferred by B2, L12 immutability, and the `nullified`-reads-`L_R` machinery the worked illustration already traces — and the review explicitly leaves the design question (whether the substrate should prevent it) open, so no intent or implementation evidence is required.

## Issue 2: The bridge section's intro claims more than B2 proves
Reason: Internal. The correct scope is already stated in B2's own carve-outs three sentences later, and the layer-reachability counterexample (a range-G `Emit_R` projecting to a non-Nullify `L_R`-growing step) is the note's own worked-illustration Step 1; the fix is rewording the intro to match what the section already proves.

## Issue 3: The wp inheritance is misattributed to B2, and the guard rule's semantics is unstated
Reason: Internal. The correct justification chain (ProjectionBridge + effect-identity + B1) consists of pieces the section's own derivation already uses, and the wp convention to be stated is a proof-bookkeeping choice about this note's refinement, not a question about designed behavior or implementation — the gate's partiality is already a settled commitment within the note.

## Issue 4: "Precondition L3 only" contradicts the note's own P5 lift
Reason: Internal. This is a consistency fix between two passages of the same note: the P5 proof already uses the correct inventory (L3 plus `d ∈ dom(Σ.M)` plus the fresh key from `K.λ`'s contract), and the precondition set comes from ASN-0086's stated step contract, a dependency the revision reads directly — neither design intent nor code evidence bears on it.

## Issue 5: RegisteredAdmissible cites C0 for a premise C0 does not state
Reason: Internal. Both repair options the review offers — citing the registry typing in "The registry," or folding the `K_j ∈ T_admissible` typing into C0's well-formedness clause — rearrange material already present in the note; it is a pure citation-precision fix.

## Issue 6: The span-count-vs-coverage point is stated in full twice; P1's conclusion is pre-stated
Reason: Internal. This is prose deduplication and forward-reference trimming within the note itself; the review even specifies which section keeps the discussion, so no external input is needed.
