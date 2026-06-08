# Channel Assignment — ASN-0111 review-24

**Date:** 2026-06-08 12:16

## Issue 1: Back-reference inventory residue in "What the read reveals that the endpoints do not"
Reason: Purely editorial — deleting a redundant back-reference inventory and rhetorical lead-in to open directly on the ownership point RL4 already states. No design intent or implementation evidence is at stake; the content (ownership via the key) is already present in the ASN.

## Issue 2: RL4 is slotted as an operation postcondition but is a fact about the key
Reason: Internal reframing only — RL4's own prose already establishes that `home(a)` is derivable by T4 projection on the key independent of the read, so restating it as a remark rather than a numbered output-postcondition is derivable from the ASN's existing content (RL4, L2 of ASN-0043).
