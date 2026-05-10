# Revision Categorization — ASN-0051 review-13

**Date:** 2026-03-23 01:04

## Issue 1: Worked example constructs an invalid state
Category: INTERNAL
Reason: The fix requires reconstructing the example using D-CTG and D-SEQ constraints already defined in the referenced ASNs. The valid composite (K.μ~ + K.μ⁻) and its consequences are fully derivable from existing definitions.

## Issue 2: Interior contraction claim conflicts with D-SEQ
Category: INTERNAL
Reason: D-SEQ's constraint that contractions remove from the maximum end is already established in ASN-0047. Correcting "a single contraction" to describe the composite (K.μ~ + K.μ⁻) requires only the definitions already present.

## Issue 3: SV13(f) embeds a conditional claim within a theorem
Category: INTERNAL
Reason: This is a structural issue about what belongs in a theorem statement versus a remark. The split between the formally proved SV6 and the unformalised byte-level closure claim is determinable entirely from the ASN's own content and its explicit acknowledgment of which premises are formalised.
