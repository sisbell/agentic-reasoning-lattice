# Channel Assignment — ASN-0036 review-200

**Date:** 2026-05-30 00:42

## Issue 1: S5 claims consistency with S0–S3 but the witness discharges only S2, S3
Reason: The fix is a matter of logical bookkeeping internal to the ASN — either construct the trivial transition-system model from the state definitions already present, or rescope the headline/table claim to match what the single-state witness discharges (S2, S3). No design intent or implementation evidence bears on whether the proof's vacuity argument is sound; that is a property of the ASN's own definitions of S0/S1 as transition-level invariants.

## Issue 2: Lockstep image well-formedness on the I-side asserted, not derived, in the run definition
Reason: Establishing that `shift(a, k)` is well-defined for an element-level address with internal zeros follows directly from the OrdinalShift/TumblerAdd machinery of ASN-0034 already cited in the note (action point `#a`, last component incremented). This is a one-line derivation from definitions already in scope, requiring neither design intent nor implementation evidence.

## Issue 3: S8a introduced inside a postcondition slot despite being load-bearing
Reason: Promoting S8a from a parenthetical aside to a named definition is a purely editorial/structural fix internal to the document; the property itself is already stated, and every downstream dependency already references it. No external channel is implicated.
