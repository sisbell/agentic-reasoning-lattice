# Review of ASN-0084

## REVISE

### Issue 1: Duplicate Open Question (same question, two phrasings)
**ASN-0084, Open Questions**: The fifth question — "By what operational process is the S8-unique maximal (canonical) run partition recovered from the valid but non-maximal partition B' that R-BLK produces, and under what conditions does iterated merging of V-adjacent, I-adjacent runs terminate at it?" — and the final question — "By what operational process is the S8-unique maximal (canonical) run partition recovered from the valid partition B' that R-BLK produces, and is that process confluent independently of merge order?"
**Problem**: These are the same question (recovering the maximal partition from R-BLK's non-maximal B' by merging), differing only in the trailing sub-clause (termination vs. confluence). Two paragraphs in the same document saying the same thing in different words.
**Required**: Collapse into a single open question whose trailing clause names both properties: "...and under what conditions does iterated merging terminate, and is the result confluent independent of merge order?"

### Issue 2: Document-coordination meta-prose around the post-state S8 discharge
**ASN-0084, Invariant preservation**: "This one-line consequence is the sole derivation of post-state S8 in this ASN; R-BLK and the Canonical-decomposition paragraph below invoke it rather than re-arguing it."
**Problem**: This is a use-site inventory — it does not advance the discharge, it merely catalogs which downstream paragraphs consume it. The pattern compounds: the Canonical-decomposition paragraph ("for the post-state M'(d) this is exactly the post-state S8 discharge recorded in the Invariant-preservation audit above") and the R-BLK closing ("...is the post-state S8 discharge recorded in the Invariant-preservation audit above") both defer back to the same location. Three sites coordinating around one fact is exactly the forward-reference accretion the precise reader must skip past.
**Required**: Delete the inventory sentence. Keep at most one back-pointer (the R-BLK closing is the natural site); have the Canonical-decomposition paragraph state the maximal-partition fact directly rather than re-deferring.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4
**Why out of scope**: The ASN explicitly restricts to n ∈ {3, 4} (CS1) and lists generalization as an open question. The class of permutations expressible by larger cut sequences is new territory, not a defect here.

### Topic 2: Composition of multiple rearrangements
**Why out of scope**: Whether the composite of two REARRANGE_K operations is itself a single rearrangement is a property of operation sequences, belonging to a future ASN; this note correctly defines the single-operation semantics.

### Topic 3: Cross-subspace and depth > 2 rearrangement
**Why out of scope**: The depth-2, text-subspace restriction is a deliberate scope choice (CS3, CS4, m_1 = 2). Extending to the link subspace or deeper arrangements is future work, not an error.

VERDICT: REVISE
