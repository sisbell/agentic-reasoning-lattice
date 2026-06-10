# Channel Assignment — ASN-0127 review-6

**Date:** 2026-06-10 01:02

## Issue 1: F-CIL-perlink is stated without a derivation, and is not an instance of F-CIL
Reason: The fix is internal — the required derivation is the per-link tail of F-CIL's own chain (L6 arity + per-slot endset equality, coverage determinism, then the `matches` existential and per-slot conjunct built from exactly these), all of which are already present in the ASN. No design-intent or implementation evidence is needed; the per-link premise and every inference step are stated machinery.

## Issue 2: D-NONMONO's K.μ⁺ direction is asserted in prose where the symmetric K.μ⁻ direction is proved by formula
Reason: The fix is internal — it chains F-INERT, F-IMG-MONO, and F-IMONO (all established in this note) into the inclusion the review already spells out, mirroring the existing K.μ⁻ clause. No external channel is required.
