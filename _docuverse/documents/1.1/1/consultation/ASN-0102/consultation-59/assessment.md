# Channel Assignment — ASN-0102 review-59

**Date:** 2026-06-08 01:44

## Issue 1: `Contains_C ⊆ R` is used as both a non-invariant and a per-step inductive hypothesis
Reason: Internal. The fix is a proof-architecture correction — discharge P4★ at the composite-boundary level using J1★ on prior steps and the ASN-0047 coupling structure already cited, rather than via a per-elementary-step invariant that K.μ⁺ refutes. All needed machinery (P4★ semantics, K.μ⁺/K.ρ coupling, composite boundaries) is in the ASN and its stated ASN-0047 dependency; no design intent or implementation evidence is required.

## Issue 2: J1'★ Old-branch discharge inherits the unsound assumption
Reason: Internal. Same root cause as Issue 1 — the Old-branch must be re-derived either composite-wide or restricted to addresses provably in `Σ.R` at the entering state, using only the coupling/provenance definitions already present in the ASN and ASN-0047. No external design or implementation question is involved.
