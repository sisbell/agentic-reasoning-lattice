# Channel Assignment — ASN-0087 review-47

**Date:** 2026-06-04 00:44

## Issue 1: StandardAuthoring is unsatisfiable for any non-empty endset
Reason: The fix is a formal correction internal to the math — restrict the predicate to the substrate-emittable address set `F`, mirroring ASN-0098's existing `tight` definition that the review itself cites. No design intent or implementation evidence is needed; the cardinality mismatch (infinite coverage ⊆ finite store) and its repair are derivable from definitions already present in ASN-0087 and ASN-0098.

## Issue 2: Redundant lemma assembly (anti-bloat)
Reason: Pure logical simplification — LP13 subsumes L12 and coverage equality follows from value equality since `coverage` is a deterministic function of the endset. Entirely derivable from the ASN's own cited properties; no channel needed.
