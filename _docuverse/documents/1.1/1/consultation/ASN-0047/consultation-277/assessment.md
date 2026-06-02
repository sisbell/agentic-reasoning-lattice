# Channel Assignment — ASN-0047 review-277

**Date:** 2026-06-01 18:51

## Issue 1: P4a discharge does not name the premise that the witness survives to the composite boundary
Reason: Internal fix — J1'★ is already defined within this ASN as a ValidComposite★ clause-(2) constraint; naming it as the premise that forbids place-then-remove composites is a cross-reference to existing content, not a design or implementation question.

## Issue 2: The operand-tracking discriminator is restated four to five times within J4
Reason: Internal fix — pure deduplication of an already-settled rule (operand-tracking source for k=0 vs k=1); collapsing five restatements into one canonical statement requires no external intent or evidence.

## Issue 3: The `max`-greatest-element well-definedness derivation is duplicated across K.α and K.λ
Reason: Internal fix — the derivation is inherited from ASN-0093 and duplicated locally; citing ASN-0093's emission cases and removing the duplicate is an editorial consolidation derivable from the ASN's own foundation references.
