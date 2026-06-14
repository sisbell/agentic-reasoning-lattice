# Channel Assignment — ASN-0134 review-38

**Date:** 2026-06-14 10:52

## Issue 1: Forward-reference inventory prose that catalogs where things are handled instead of advancing a claim
Reason: The load-bearing content (`K.σ` is scoped out of the conflict analysis; freshness and register-before-allocate are assumed preconditions from an excluded layer) is already stated in §4; the fix only deletes the inventory of where downstream consumers handle registration and collapses two duplicate OQ5 pointers. Pure structural trim, no design intent or implementation evidence required.

## Issue 2: A "synthesis" paragraph that restates per-instance conclusions already established
Reason: All three resolutions and the W1/W2 model-intrinsic/serialization-borne labels are already established where each instance and claim is analyzed; the fix removes redundant restatement and folds the labels into the §5 partition prose. Internal deduplication derivable from the ASN's existing content.

## Issue 3: Post-proof design-intent essays that self-admittedly add no derivation
Reason: The Nelson grounding is already present and quoted in the ASN; the fix relocates it to a consistent convention (one trailing sentence per claim or a motivation subsection), not re-deriving or re-validating intent — the note itself flags these essays as non-derivational. Structural reorganization, no channel needed.

## Issue 4: V2's claim statement is overloaded with worked witnesses and scope analysis that belong in prose
Reason: Both converse-failure witnesses, the writer/reader duality, and the type-scoped-vs-home-scoped analysis already exist verbatim in V2; the fix pares the claim to the implication chain and moves the worked material into §8 prose alongside the existing trace. Pure relocation derivable from the ASN.
