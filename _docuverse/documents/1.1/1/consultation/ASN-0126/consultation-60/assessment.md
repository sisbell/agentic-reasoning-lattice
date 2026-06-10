# Channel Assignment — ASN-0126 review-60

**Date:** 2026-06-09 17:39

## Issue 1: "Properties established" verbatim-restates P1–P6
Reason: Purely an organizational de-duplication fix — pick a single home for each P statement and have proof sections reference rather than re-state. This concerns document structure only, requiring no design intent or implementation evidence; the property statements themselves already exist in the ASN.

## Issue 2: forward-cite over-justifies a definitional fact in the wp derivation
Reason: The fix is to recast a forward-cited fact as definitional, and the ASN's own definition of `K.λ_sh` ("`K.λ` with three added preconditions") fully supplies the justification — adding preconditions cannot alter the C/M/L effect. Entirely internal to the note's existing definitions; no external channel needed.
