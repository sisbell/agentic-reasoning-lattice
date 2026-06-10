# Channel Assignment — ASN-0127 review-3

**Date:** 2026-06-10 00:07

## Issue 1: D-NONMONO's K.μ⁻ inclusion drops the Σ.L-preservation step
Reason: Fix is internal — every property needed to bridge the states (F-PRES, F-INERT, F-IMG-CONTR, F-IMONO) is already established in the note, and the review spells out the exact insertion. No design intent or implementation evidence is at stake; this is a proof-step gap.

## Issue 2: Worked illustration misattributes the existence-invariance citation
Reason: Fix is internal — a citation correction swapping the non-monotonicity result (D-NONMONO) for the invariance results already in the note (F-INERT, optionally E-INV). All referenced properties are defined within the ASN; nothing turns on design intent or the implementation.

## Issue 3: `V_atomic` is used before it is bound
Reason: Fix is internal — the atomic vocabulary is already fully enumerated in "State and notation" (with K.μ~ already identified as the K.μ⁻+K.μ⁺ composite, citing ASN-0047); binding the symbol `V_atomic` to that existing list is a pure notation/presentation change requiring neither channel.
