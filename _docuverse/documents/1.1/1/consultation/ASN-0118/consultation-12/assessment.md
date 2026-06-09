# Channel Assignment — ASN-0118 review-12

**Date:** 2026-06-09 00:06

## Issue 1: Stated effect/frame clauses do not vacate pre-shift positions — S2 (functionality) is not established by the postconditions in the displacing case
Reason: Internal. The fix is a formal choice already modeled inside the ASN — either add a vacating/domain-closure postcondition (the ASN-0082 I3-V/D-DOM analogue the reviewer cites) or declare COPY *defined* as the exhibited K.μ⁻+K.μ⁺ composite with CP2/CP3 derived. Both routes draw only on machinery already present (ASN-0082's vacating clause, the composite decomposition); no design intent or implementation evidence is at stake.

## Issue 2: CP8 range-new characterization is internally contradictory
Reason: Internal. A pure wording/logic repair — define range-new as "placed by CP2 *and* not already in the pre-state content-subspace range" — fully determined by the ASN's own subsequent case-split and worked example.

## Issue 3: Empty-destination depth uses `m_{s_C}(d)` before it is defined
Reason: Internal. The circularity is resolved by the ASN's own cited definitions (ASN-0047 LinkSubspaceDepth, ValidFirstInsertionPosition's chosen `m ≥ 2`): state `#p = m` and note it *defines* `m_{s_C}(d)` for the post-state. No external channel needed.
