# Review of ASN-0099

## REVISE

### Issue 1: "disjoint I-runs" mischaracterizes the image decomposition

**ASN-0099, "The Image Set"**: "When `R` is a contiguous V-span in subspace `s_C`, ASN-0058's mapping-block decomposition gives the image as a union of disjoint I-runs, one per maximal correspondence run."

**Problem**: The maximal correspondence runs (mapping blocks) are disjoint in their **V-extents** (B2, ASN-0058), but their **I-extents need not be disjoint**. The system deliberately permits distinct V-positions within one document to reference the same I-address (S5 UnrestrictedSharing, ASN-0036; M13/M14 IndependentOccurrences, ASN-0058 — two blocks sharing an I-extent cannot merge yet coexist). So two correspondence runs in a single contiguous V-span can have overlapping or identical I-extents. Describing the image as "a union of *disjoint* I-runs" is therefore inaccurate precisely in the shared-content case that motivates this whole operation (transclusion → shared I-addresses). The image set itself is still correct (set union absorbs the overlap), but the word "disjoint" attached to I-runs is wrong/misleading.

**Required**: Drop "disjoint," or state the property that actually holds — the correspondence runs are V-disjoint (partition `R ∩ dom(M(d))`), while their I-extents may coincide under shared content. E.g. "a union of I-runs, one per maximal correspondence run, whose V-extents partition `R ∩ dom(M(d))` but whose I-extents may coincide when V-positions share content."

## OUT_OF_SCOPE

None beyond the items the ASN already defers in "What We Have Not Specified" (procedure/computation, replication/consistency, caching, access control, FOLLOWLINK inverse, combined filtered-scoped form), all appropriately classified as future territory.

VERDICT: REVISE
