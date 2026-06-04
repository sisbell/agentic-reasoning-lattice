# Channel Assignment — ASN-0087 review-37

**Date:** 2026-06-03 23:37

## Issue 1: Problem statement overstates the discoverability guarantee
Reason: Internal. The body already proves the conditional nature via M-WP and LP17; reconciling the intro to say MAKELINK establishes the LP12 *property* (yielding actual discoverability only on arrangement-reach or reflexivity, and permitting orphaned birth) is a logical edit derivable from claims already present.

## Issue 2: Reflexive authoring contradicts "cannot specify the address"
Reason: Internal. "Cannot specify" vs. "must predict" is a terminological clarification, and the soundness precondition (no intervening `A_L(d)` emission) is derivable from the deterministic emission rules already cited from ASN-0093; scoping to the protocol layer mirrors the ASN's own atomicity treatment.

## Issue 3: Reflexive case derived twice
Reason: Internal. Purely editorial deduplication — keep one derivation and have the other cite it; no design intent or implementation evidence is at stake.

## Issue 4: Essayistic rationale in structural slots
Reason: Internal. The load-bearing statements are already carried by M-NoIndexState, M-CompAtomicity, and the operation-level no-permission-check statement; reducing the Nelson-attribution prose to operational statements (or demoting to a non-normative note) is an editorial restructuring.
