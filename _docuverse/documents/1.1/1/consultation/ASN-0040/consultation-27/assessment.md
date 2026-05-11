# Channel Assignment — ASN-0040 review-27

**Date:** 2026-05-11 11:15

## Issue 1: Bop's FRAME is incompatible with Bridge1's whole-state equality
Reason: This is an internal logical inconsistency between two clauses in the same ASN — the FRAME clause asserts only Σ.B changes while Bridge1 demands whole-state equality with an operation that (per ASN-0034) also touches Act/nₛ. The review supplies three concrete reconciliation options (qualifying the frame, weakening Bridge1 to Σ.B-component equality, or partitioning Op), all of which are editorial choices about how to formulate the spec for internal consistency; no design intent or implementation evidence is required.
