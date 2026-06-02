# Review of ASN-0069

## REVISE

### Issue 1: Foundation claims cited under incorrect names

**ASN-0069, §"Sharing, Not Duplication"**: "which the foundation's J0 (AllocationRequiresPlacement) requires to be paired with placement."

**Problem**: ASN-0047 names J0 **AllocationPlacementCoupling**, not "AllocationRequiresPlacement." This is an invented name for a foundation claim. The same drift recurs systematically elsewhere:
- V9 and the composite verification cite J1★ as **ExtensionRecordsProvenanceContentSubspace** — ASN-0047's actual name is **ExtensionRecordsProvenance**.
- They cite J1'★ as **ProvenanceRequiresExtensionContentSubspace** — actual: **ProvenanceRequiresExtension**.
- V12(d) cites P4★ as **ProvenanceBoundsContentSubspace** — actual: **ProvenanceBounds**.

Standard 7 forbids inventing notation for something a foundation already defines. A reader cross-checking against ASN-0047 will not find these names.

**Required**: Cite each foundation claim by the exact name ASN-0047 assigns (AllocationPlacementCoupling, ExtensionRecordsProvenance, ProvenanceRequiresExtension, ProvenanceBounds). If a descriptive qualifier like "content-subspace" is wanted, add it as prose, not as part of the claim name.

### Issue 2: "Chain of custody is reconstructable" contradicts V9a

**ASN-0069, §"Provenance Recording"** (final paragraph): "The chain of custody — A transcluded to B, B forked to C — is not stored in R; it is reconstructable from the I-addresses themselves, because origin(a) identifies the original allocator and V2's prefix-ancestry identifies the immediate parent in the fork tree."

**Problem**: This asserts the *chain of custody* is reconstructable, but **V9a** states the opposite: "the relation does not distinguish whether d_new acquired a via fork from d_src, via transclusion from a third document also containing a, or via direct allocation," and §"Why I-Address Identity Suffices" lists "derivation lineage at the I-address level" among what identity does **not** capture. What is actually recoverable is (a) the content allocator via `origin(a)` and (b) the document fork tree via prefixes — but *not* the acquisition path (the "A transcluded to B" step). The sentence overstates recoverability and conflicts with the very property it precedes.

**Required**: Restate to match V9a — the fork-tree lineage (document prefixes) and content origin are reconstructable, but the transclusion/acquisition path by which a document obtained an I-address is not. Drop or qualify "chain of custody ... is reconstructable."

## OUT_OF_SCOPE

None. Deferred topics (concurrency, snapshot vs. living forks, transcludent sources, descendant enumeration) are correctly confined to the Open Questions section as future work, not claimed here.

VERDICT: REVISE
