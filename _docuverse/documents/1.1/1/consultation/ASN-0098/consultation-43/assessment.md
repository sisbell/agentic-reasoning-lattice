# Channel Assignment — ASN-0098 review-43

**Date:** 2026-06-02 15:08

## Issue 1: "Canonical span" is defined twice, with different content, and the decidability bridge is left implicit
Reason: Internal. The required bridge lemma `dom(Σ.C) ∪ dom(Σ.L) ⊆ F` is provable from ASN-0093 lemmas (ChainMembershipForOrigin, FirstEmission/ChainDiscipline, M0) that the ASN already cites — LP12b proves the link half by exactly this chain, and the content half is symmetric. Unifying the two "canonical span" definitions is a self-contained editorial choice.

## Issue 2: Repetitive composite-level meta-prose after LP11
Reason: Internal. Pure prose reduction of a thrice-stated fact; no design intent or implementation evidence is in question.

## Issue 3: Citation-choice meta-prose in LP18
Reason: Internal. Deleting the parenthetical and citing the single lemma the step uses is a self-contained editorial fix.

## Issue 4: Defensive "what we are not doing" prose around the F definition and LP9
Reason: Internal. Removing disclaimers while retaining the stated constructions and facts-used is editorial; the underlying reasoning is unchanged and self-contained.
