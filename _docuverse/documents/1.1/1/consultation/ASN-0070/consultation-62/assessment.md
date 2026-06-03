# Channel Assignment — ASN-0070 review-62

**Date:** 2026-06-03 02:15

## Issue 1: Three defined behaviors are never exercised by any worked example
Reason: Internal. The Setting already admits `V_S(d) = ∅` as a structural possibility, the Vacuous-subspace convention fixes the result, and F-slot/F-multidoc are stated lemmas — constructing a content-only document and re-running `follow` at a second slot/document is fully derivable from the ASN's own definitions and the existing configuration machinery.

## Issue 2: Transitive-dependency tracing in F-det's Depends slot
Reason: Internal. This is a mechanical deletion of a parenthetical; F0 already discharges S2 in its own Well-definedness clause, so no external evidence or design intent is needed.

## Issue 3: F-slot introduces an undefined `followAll` operation
Reason: Internal. Removing the `followAll` aside and reducing it to the slot-independence point already made requires only the ASN's own F-slot postcondition.
