# Channel Assignment — ASN-0075 review-16

**Date:** 2026-05-25 17:36

## Issue 1: Implicit content value assumption in D-DISCR construction
Reason: Fix is internal — the construction needs one explicit sentence stating both K.α calls supply the same v_a ∈ Val. The required choice is fully determined by the proof's agreement table; no design intent or implementation evidence is needed.

## Issue 2: "Immediately following" overstates bundling requirement
Reason: Fix is internal — J0 is already characterized as a composite-boundary coupling by ValidComposite★ (ASN-0047), which the ASN cites. The wording correction follows directly from that established semantics.

## Issue 3: Bijection between equivalence classes and witness runs left implicit
Reason: Fix is internal — the bijection is determined by the existing construction (T1-minimum, cardinality, shared origin). One explicit sentence makes the implicit assignment visible to the reader.

## Issue 4: D-ORG section heading mismatch with claim table label
Reason: Withdrawn by reviewer on re-check — no fix required.
