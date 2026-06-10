# Channel Assignment — ASN-0126 review-93

**Date:** 2026-06-10 05:52

## Issue 1: "Emit_K ... carry over unchanged" contradicts the gating thesis
Reason: Purely internal consistency fix — the note already establishes that `K.λ_sh` gates `Emit_K` (*The shape-gated emit*, P3, P5) while `Observe_K` is a pure read; the correction merely splits the two claims to match the note's own thesis, with the required wording already supplied. Neither design intent nor implementation evidence is needed.
