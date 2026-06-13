# Channel Assignment — ASN-0108 review-43

**Date:** 2026-06-13 06:46

## Issue 1: Claim statements W5 and W9 carry their own proofs and cross-references
Reason: Pure relocation of existing material — the cancellation mechanism already lives in walk 3 and the cut-point mechanics in W9c; the fix trims the claim slots and moves nothing new, all internal to the ASN.

## Issue 2: W5's exposition cannot stand without three downstream claims
Reason: The two conditionals ("clause 1 ⟹ no re-delivery; clause 1 + termination ⟹ no skip") are already the logic the ASN establishes; restating them and reversing the W5↔W9b reference direction is a structural rephrasing derivable from the ASN's own content.

## Issue 3: Defensive aside rebutting a wrong reason
Reason: The preceding sentence (`κ_Σ(a) = κ_{Σ'}(a) = a`) already establishes state-stability by state-independence alone, so dropping or compressing the allocation-axiom aside removes redundancy without needing design intent or implementation evidence.

## Issue 4: W7 re-states M-mut's loss direction with its full citation chain
Reason: The loss mechanism and its citations already appear verbatim in the State section's M-mut; replacing the re-derivation with a cite to M-mut and keeping only W7's per-window consequence is internal deduplication.
