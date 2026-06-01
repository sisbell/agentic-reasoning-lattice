# Channel Assignment — ASN-0086 review-133

**Date:** 2026-06-01 01:21

## Issue 1: wp Case 2 domain restriction is insufficient — the derivation silently requires the unit-depth retraction discipline, which substrate-conformance does not supply
Reason: The fix is internal — the unit-depth retraction discipline and R0a are both already defined in the ASN, and the reviewer has identified the exact correction (add the discipline as a precondition conjunct, cite both R0a and the discipline in the rationale). No design-intent or implementation evidence is needed; this is a logical-consistency repair derivable from the ASN's own definitions.

## Issue 2: the audit-vs-active mechanism is stated three times with cross-deferral (anti-bloat)
Reason: Pure editorial deduplication — state the audit-vs-active distinction once at the Definition of `nullified`, delete the forward pointer, and let R6b assert its consequence. Entirely derivable from the ASN's existing content.

## Issue 3: R7a statement carries proof-case elaboration in the statement slot
Reason: Pure editorial relocation — the length-1 and single-fresh-home cases already appear in the proof, so the fix is to move or cut the preview from the statement slot. No external input required.
