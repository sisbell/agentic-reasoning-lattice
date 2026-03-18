## Question 1 [nelson]

> If two regions of content partially overlap, must the system always be able to identify the exact sub-region they share in common?

## Yes — and this is structural, not heuristic.

The system must always identify the exact shared sub-region when two content regions overlap, because overlap is defined by **shared I-space origin**, and every byte's I-address is permanently known.

### Why it works

Every byte in the docuverse has a permanent I-space address. When content appears in multiple documents (through transclusion via COPY, or through shared version ancestry via CREATENEWVERSION), those appearances share the same I-addresses. The V→I mapping (the POOM enfilade) can resolve any byte in any document to its permanent I-address. Comparing I-address sets between two regions yields the exact overlap — down to the individual byte.

Two operations make this explicit:

**SHOWRELATIONOF2VERSIONS** directly returns the shared sub-regions:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

**FINDDOCSCONTAINING** finds partial overlap across the entire docuverse:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

Note "any portion" — the system handles partial overlap, not just complete containment.

### The deeper guarantee

Nelson frames this as essential to the entire versioning system:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

> "Moreover, highlighting the corresponding parts is a vital aspect of intercomparison." [LM 3/13]

> "The user may scroll through any two versions to see corresponding parts; and much more." [LM 2/21]

The system doesn't approximate what's shared — it knows precisely, because correspondence is a structural relation derivable from I-addresses.

### The critical caveat

Overlap is defined by **provenance**, not by **value**. Two independently typed copies of identical text have different I-addresses and are NOT considered overlapping. Only content that shares I-space origin — through transclusion or version derivation — registers as shared.

This is by design. As noted in the content provenance materials: content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address. This is how the system distinguishes "wrote the same words" from "quoted from the original."

So: if two regions share any I-space content at all, the system can always identify the exact sub-region they have in common — because that sub-region is simply the intersection of their I-address sets, and every byte's I-address is permanent and known.
