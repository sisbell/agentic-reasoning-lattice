# Channel Assignment — ASN-0097 review-3

**Date:** 2026-05-24 10:56

## Issue 1: Π5 (ProjectionLocality) has no formal proof
Reason: The fix is a one-line derivation directly from the definition of `proj` already given in the ASN. No external evidence or design context is required.

## Issue 2: Π7 (CoverageEquivalence) has no proof
Reason: The fix is a one-line proof from the definition of `proj`, which depends on `e` only through `cov(e)`. Fully internal.

## Issue 3: Π17 (PartialReach) is notationally malformed and unproven
Reason: The fix is a notational restatement (implication form) and witness-based proof using only the ASN's own definitions of `reaches`, `proj`, and the already-proven bridge equality. Internal.

## Issue 4: Π13, Π14, Π16 proofs are sketches, not derivations
Reason: The required proofs combine the frame conditions already cited from ASN-0047 (K.α leaves M untouched; K.λ leaves M untouched) with Π5, plus — for Π16 — the bridge equality proven earlier in this ASN. All ingredients are in hand internally.

## Issue 5: Π15a relies on an uncited well-formedness axiom
Reason: The review explicitly accepts "state it as an explicit precondition this ASN assumes" as a valid fix path. This is a purely internal editorial addition; no external evidence is required to introduce a well-formedness precondition.

## Issue 6: Worked example forward-references the wp section
Reason: Pure document reordering or rephrasing within this ASN. No external consultation needed.

## Issue 7: Mode I "boundary insertion" argument elides a chain
Reason: The required chain combines S0 (already cited in the ASN) with the freshness semantics of K.α (allocating new addresses extends `dom(C)` with addresses not already in it — derivable from the ASN-0047 vocabulary already cited). Internal.
