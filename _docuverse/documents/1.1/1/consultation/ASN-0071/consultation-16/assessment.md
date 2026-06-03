# Channel Assignment — ASN-0071 review-16

**Date:** 2026-06-02 23:08

## Issue 1: Worked example verifies F-PART vacuously
Reason: Internal. Extending the worked scenario to a multi-address resolution (`|iaddrs| ≥ 2`) and showing a document that references only one address uses only the ASN's own definitions and the ASN-0047/0058 machinery already cited; no design intent or implementation evidence is required.

## Issue 2: Resolve-equivalence (multi-block case) never checked against a concrete state
Reason: Internal. Building a multi-block worked state and checking `iaddrs_one` against the set-flattening of `resolve` exercises C1a/B1/B3/M14 from ASN-0058, all of which are already present and cited in the ASN; the construction is derivable from the ASN's own content.

## Issue 3: `m ≥ 2` misattributed to C0
Reason: Internal. The correct attribution (`k = m` from C0; `m ≥ 2` from S8a/S8-depth or C0a) is a citation correction resolvable against the foundation claims the ASN already references; the review states the right premises and no external channel is needed.
