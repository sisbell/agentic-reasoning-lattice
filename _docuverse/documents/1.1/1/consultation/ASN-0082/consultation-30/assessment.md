# Channel Assignment — ASN-0082 review-30

**Date:** 2026-05-15 10:59

## Issue 1: Missing span width preservation lemma for contraction
Reason: The proof technique mirrors I3-S exactly (TumblerAdd/TumblerSub commutativity at depth-2 single-component ordinals), and all required foundation citations (D2, S6, T12, TA4, TumblerSub) are already present in this ASN. The choice between adding D-S or deferring is a scoping decision derivable from the ASN's stated purpose.

## Issue 2: wp analysis style inconsistency
Reason: This is a presentation-uniformity decision between two equivalent proof styles. Both forward proofs (already present in contraction lemmas) and wp derivations (illustrated in insertion lemmas) discharge the same obligations against the same cited foundation lemmas; the choice is internal.

## Issue 3: Depth = 2 restriction grounds mix levels
Reason: The fix is restructuring existing material — the three grounds are already stated in the ASN with their specific citations (LM passages, udanax-green source locations, TA4 zero-prefix mechanics). Relocating design-intent and implementation-reality material to a separate section does not require new external claims.

## Issue 4: I3-V exclusion clause readability
Reason: Purely a presentation issue — either rewrite the formal statement or add a one-line gloss. The semantic content is already fully specified by I3-V and verified by the consistency check and the worked example's I3-V trace.

## Issue 5: V_S(d) and V_1(d) used interchangeably
Reason: Notation consistency within the post-contraction section. The subspace scoping axiom fixes S = 1, and the foundation convention is already cited in the ASN. The fix is mechanical replacement of V_S(d) with V_1(d) throughout the contraction section.
