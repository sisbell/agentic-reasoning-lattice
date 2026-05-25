# Channel Assignment — ASN-0051 review-56

**Date:** 2026-05-16 08:06

## Issue 1: Misleading foundation citation in Notation section
Reason: Pure lattice-citation fix. OrdinalShiftBase vs M-aux distinction is settled within ASN-0058's own structure; no design intent or implementation evidence is at issue.

## Issue 2: K.μ~ composite structure of Worked Example understates elementary chain
Reason: Internal consistency fix. ASN-0051 already contains SV5's composite-scope note and ASN-0047 defines K.μ~ as the K.μ⁻ + K.μ⁺ composite; the choice between annotating or cross-referencing is editorial and self-contained.

## Issue 3: Implicit V-position arithmetic in SV11 multi-block witness
Reason: Formalization gap derivable from ASN-0058's block representation and ASN-0036's V-position structure. Stating `v_k = [s_C, k]` at depth m_C = 2 closes the gap using definitions already in scope.

## Issue 4: SV6 proof's T4-validity argument for t — boundary case clarity
Reason: Proof-presentation issue. The required mathematics (element-field-zero-confinement, k > p₃ inequality, T4 inheritance) is already established in the ASN's own SV6 proof; only the case split needs to be made explicit.
