# Channel Assignment — ASN-0133 review-23

**Date:** 2026-06-14 01:30

## Issue 1: The starvation-separation argument is re-derived in five places
Reason: Pure consolidation of an argument the ASN already states fully — the fix relocates one fact (`|W(σ)|=∞` with zero real fires) to its definitional home (H-RF) and replaces re-derivations with references. No design intent or implementation behavior is at stake; everything needed is already in the note.

## Issue 2: Q0's closing parenthetical restates the body's view partition, and Q7 re-inventories it
Reason: Editorial deduplication — the four-element view-sensitive inventory and its rebuild method are already worked through in Q0's body, so dropping the recap parenthetical and replacing Q7's re-enumeration with a back-reference is derivable from the note's own content. The view machinery is ASN-0129's, already cited, not a fresh evidence or intent question.

## Issue 3: H-SFAIR is offered as a second route, then argued to be barely one, at length and in two sections
Reason: This is a restructuring of the note's own logic — the near-coincidence of H-SFAIR-satisfiability with regime (i), and the unused H-SFAIR ⟹ H-FAIR positioning, are both argued internally. Choosing between "one route, two framings" vs. "keep but compress" turns on the note's own theorem-consumption record, not on external design or code.

## Issue 4: Multiple deferrals to one downstream section, and a premature forward-result in RG
Reason: Structural cleanup of cross-section pointers and a forward-reference — collapsing duplicate "deferred — see X" pointers and removing the RG preview of Q5a's open/closed collapse are mechanical relocations within the note. The deferred scheduler material and the Q5a result both already exist in their proper sites; no intent or evidence input required.
