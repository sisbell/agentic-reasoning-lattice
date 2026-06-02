# Channel Assignment — ASN-0086 review-255

**Date:** 2026-06-01 23:31

## Issue 1: wp Case 2 states an incorrect rationale for restricting the domain to layer-reachable states
Reason: The binding rationale (unit-depth discipline rules out a pre-existing retraction covering the fresh address) is already stated in the Case 2 derivation, and the contrast with Case 1's `→*`-reachable domain is internal to the note. No design intent or implementation evidence required.

## Issue 2: Defensive parenthetical in the discipline commitment (forward-reference/anti-bloat)
Reason: Pure deletion of redundant defensive prose; the positive specification it duplicates is already present. Fully internal.

## Issue 3: The discipline commitment is restated nearly verbatim in the discharge paragraph (duplication)
Reason: Collapsing a verbatim restatement to a citation of an existing definition is a mechanical edit derivable from the note alone. No external channel needed.

## Issue 4: Exhaustiveness meta-narration in the discharge enumeration
Reason: Deleting a framing sentence while leaving the load-bearing enumeration intact is internal editing. No design or implementation question arises.
