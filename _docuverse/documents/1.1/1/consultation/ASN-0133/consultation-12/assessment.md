# Channel Assignment — ASN-0133 review-12

**Date:** 2026-06-13 15:58

## Issue 1: The stated H-SFAIR is too weak to imply H-FAIR at the strength Q6's regime (i) needs
Reason: Internal fix. The repair is to correct the statements of two named hypotheses — H-FAIR to explicit per-occurrence discharge, H-SFAIR to the standard GF-taken (infinitely-often-enabled ⟹ infinitely-often-taken) form — and to update the implication's proof prose accordingly. This is a self-contained logical realignment using the note's own discharge machinery (real-fire / removal / in-place falsification) plus the textbook definitions of weak vs. strong fairness; the review already supplies the corrected forms and the soundness argument. Neither channel bears on it: the note explicitly classes fairness as a scheduler property it "deliberately ships no scheduler note" for and leaves at the implementation layer, so there is no Nelson design-intent question (fairness is not a Xanadu semantic constraint) and no Gregory evidence question (udanax-green implements no such rule-scheduler whose fairness form could be read off).
