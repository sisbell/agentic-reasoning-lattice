# Revision Categorization — ASN-0067 review-13

**Date:** 2026-03-22 22:52



## Issue 1: Elementary decomposition (Case 1) misapplies K.μ~ and violates D-CTG
Category: INTERNAL
Reason: The fix requires restructuring the elementary decomposition to use valid transition sequences from ASN-0047's own definitions. All necessary information — K.μ⁻ and K.μ⁺ preconditions, D-CTG requirements, ValidCompositeExtended — is already present in the referenced ASNs.

## Issue 2: P.7 is too weak to restrict COPY to the content subspace
Category: INTERNAL
Reason: ASN-0047 already defines SubspaceIdentifiers with s_C and s_L both satisfying ≥ 1, and the K.μ⁺ amendment already requires subspace(v) = s_C. The fix is a direct substitution using definitions already present in the foundation.

## Issue 3: Link subspace identifier stated as 0
Category: INTERNAL
Reason: ASN-0047 derives s_L ≥ 1 and ASN-0036 S8a requires v₁ ≥ 1. The parenthetical contradicts established definitions within the spec itself.

## Issue 4: C3 omits extended-state invariants
Category: INTERNAL
Reason: The extended invariants (S3★, P4★, CL-OWN, etc.) are defined in ASN-0047 and their preservation follows directly from L being in the frame and C' = C. No external evidence is needed — the derivation uses only existing ASN-0047 definitions.
