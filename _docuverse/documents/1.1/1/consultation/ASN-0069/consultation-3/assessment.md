# Channel Assignment — ASN-0069 review-3

**Date:** 2026-05-25 12:41

## Issue 1: V1's subsequent-fork case extends J4 without explicit acknowledgment
Reason: The fix is purely editorial — adding parallel framing language similar to V7's existing extension acknowledgment. The ASN already cites ASN-0047's Allocator hierarchy as the basis for A_v(d_src)'s subsequent emissions; no new theoretical input or implementation evidence is needed.

## Issue 2: K.δ sub-case A freshness argument cites unnamed foundation property
Reason: The fix requires citing T10a's at-most-once-per-(t, k') constraint from ASN-0034 (the foundation document already referenced throughout this ASN). This is a reference-precision fix derivable from the existing foundation citations — not a question about design intent or implementation behavior.

## Issue 3: V8b is informal but makes precise claims requiring formal grounding
Reason: The required derivation uses V5a (already established in this ASN) and the per-document frame discipline of K.μ⁻/K.μ~/K.μ⁺ from ASN-0047 (already cited). All necessary components are present; the fix is formalization of reasoning already implicit in the ASN.
