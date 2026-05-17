# Channel Assignment — ASN-0086 review-36

**Date:** 2026-05-17 13:44

## Issue 1: R7's headline overstates a stipulation-conditional conclusion
Reason: The note already contains the R7a/R7b decomposition explicitly and acknowledges R7b is stipulated; the requested change is to make the headline and downstream citations (R6c Consequence (d), Properties table) honestly reflect the existing analysis. Purely presentational restructuring.

## Issue 2: R6 is essentially definitional, not a lemma
Reason: The note itself concedes R6 is "essentially a definitional check" in its headline narrative; the reclassification (DEF vs LEMMA) and the choice of substitute substantive content (the active/audit distinction as set-difference) are derivable from the note's own characterization. No external evidence needed.

## Issue 3: R0 Step 4's L-invariant verification is excessively granular
Reason: The FramePreservation lemma and its five specializations (a)–(e) are already defined in the note; the fix is to apply them more uniformly to the routine L-invariants and reserve explicit bullets only for the substantive new-address checks (L0, L1, L1a, L1b, L1c, L11a, L14, L14a). Purely internal refactoring.

## Issue 4: SharedDepthOneAllocator's "exactly one allocator at allocator-tree depth 1" statement conflates two depth notions
Reason: The note's own definitions of "allocator-tree depth" and "zero-count depth" — together with the proof's step (b), which already analyzes both (d, 1) and (d, 2) and identifies which produces outputs at zero-count depth 1 — make the proper restatement derivable internally. The fix is to qualify "depth 1" with "whose outputs sit at zero-count depth 1."

## Issue 5: Cumulative hypothesis stack obscures which claims hold standalone
Reason: Pure tagging/presentation convention — the note already contains all the dependency information (in the prose tags and the Hypothesis dependency view table); standardizing the three-field convention and adding a "Model Commitments" preamble is editorial reorganization with no new content required.

## Issue 6: R5's "exhaustive non-opposition check" mixes two proof strategies
Reason: The substantive content of Stage 2 is already in the note; the fix is to restructure the 22-bullet enumeration as a partition statement (pre-existing-data invariants discharged by frame, tumbler-algebra invariants discharged by L4(c)+L13, R0-Step-4-discharged invariants), which is derivable by inspecting which class each invariant falls into. Internal.

## Issue 7: Worked Sketch's length crowds out the principle
Reason: The L-invariant verification pattern is fully shown at b₁; subsequent emissions (a₂, b₂, a₃, b₃) repeat the structure mechanically with enumeration-index updates that the note's own R0a sibling-stream invariant licenses by reference. Pure compression decision, no external input required.

## Issue 8: Class-(iii) frame conditions are presented as derivable but are actually definitional
Reason: The note's "Status — model definition, not derivation" paragraph has already declared the convention (frames are definitional; L12/L12a are consistency checks on the definitional frame). The fix is to apply that convention consistently to the remaining citation sites (notably R7a's proof) — purely an editorial consistency pass against an already-stated position.
