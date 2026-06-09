# Channel Assignment — ASN-0126 review-56

**Date:** 2026-06-09 14:46

## Issue 1: "Properties established" is a pointer index, not a contract
Reason: Pure reorganization of content already present in the ASN. The properties P1–P6 are all stated and derived within the note's own sections; picking role (a) or (b) and relocating P6's proof requires no design intent or implementation evidence — only the note's existing statements.

## Issue 2: C0 is consumed by P2 but stated later, papered over with forward-reference prose
Reason: A section-ordering fix internal to the note. The dependency is one-directional and stated outright in the ASN (C0 → P2, not the reverse); moving Registration entries/C0 ahead of Registry permanence and deleting the forward-reference prose is mechanical and derivable from the note's own dependency structure.

## Issue 3: the wp's C2 paragraph re-derives Single-source
Reason: Deduplication against content the ASN already establishes. The empty-from-Nullify contrast and the Binary-wrapper construction both live in full in Single-source; reducing C2 to the self-nullification witness and citing Single-source needs only the note's existing material.
