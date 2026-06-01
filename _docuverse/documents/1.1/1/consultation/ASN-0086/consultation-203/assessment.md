# Channel Assignment — ASN-0086 review-203

**Date:** 2026-06-01 15:13

## Issue 1: The `↝` / conformance-taxonomy / R6d / R7a apparatus generalizes to higher-layer operations that do not exist
Reason: Whether forward-looking cross-layer guarantees belong in the substrate note turns on the design's layering intent — was the link store meant to serve as a foundation that higher layers extend, justifying conformance guarantees stated in advance? That is a design-intent question, not derivable from the ASN's own content or from the implementation.
Nelson question: Was the link store designed as a substrate meant to be extended by higher relational layers, such that invariants like retraction-stability are intended to be guaranteed against future layer operations — or is each layer expected to re-establish its own guarantees?

## Issue 2: L-ContiguousPrefix re-proves a foundation lemma for the reachable case
Reason: The fix is a cross-reference cleanup — replace the re-derivation with a citation to ASN-0093's ChainMembershipForOrigin, which the note itself concedes coincides with the reachable case. Derivable from the ASN and its cited foundation alone.

## Issue 3: "Tuple address" / `A_rel^Σ` terminology overclaims relative to the arity-3 restriction
Reason: Purely a terminological/definitional fix internal to the note — restrict `A_rel^Σ` to arity-3 addresses or rename and mark `addr`'s codomain as into-not-onto. The arity-3 restriction and the higher-arity exclusion are already stated in the ASN.
