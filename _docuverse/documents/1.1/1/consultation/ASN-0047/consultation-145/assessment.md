# Channel Assignment — ASN-0047 review-145

**Date:** 2026-05-31 14:52

## Issue 1: K.μ~ existence condition `|dom_C(M(d))| ≥ 2` is not sufficient when content positions share an I-address
Reason: The fix is internal — S5 (UnrestrictedSharing) is already cited in the ASN, and the corrected condition ("`M(d)|_{dom_C}` takes at least two distinct values"), the net-effect reading of clause (ii), and the witness-pair selection are all derivable from definitions already present. No design intent or implementation evidence is required to sharpen a formal condition the ASN's own machinery exposes.

## Issue 2: Non-circularity / document-ordering meta-prose and verbatim repetition (anti-bloat patterns)
Reason: The fix is internal — this is purely editorial consolidation (collapsing meta-prose into premise lists, introducing a named handle, removing deferral chains) with no bearing on design intent or implementation behavior.
