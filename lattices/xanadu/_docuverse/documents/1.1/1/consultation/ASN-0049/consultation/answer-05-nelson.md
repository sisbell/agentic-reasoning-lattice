## Question 5 [nelson]

> Must the system preserve the identity of shared content — meaning a reader can always determine that the same content appears in multiple documents?

# Yes — Preserving Shared Content Identity Is Architecturally Fundamental

This is not merely a feature of Xanadu. It is the central architectural invariant from which most other guarantees flow.

## The Structural Mechanism

Xanadu separates content storage (I-space) from content arrangement (V-space). Every byte ever created has a permanent I-space address that never changes. When content appears in multiple documents, it does so through **transclusion** — inclusion by reference to the same I-space address, not duplication.

This means shared content is not merely "the same text" — it is **the same bytes at the same address**. The system distinguishes identity from coincidence:

> "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address."
> — sporgl-provenance design intent

## The User-Facing Guarantee

Nelson states this directly:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and regular in layout. You always know where you are, and can at once ascertain the home document of any specific word or character."
> — [LM 2/40]

This is not aspirational. It is a design requirement that the architecture enforces structurally:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations."
> — [LM 4/11]

When you view a compound document containing transcluded content, the system fetches that content from its home location. The fetching mechanism itself encodes the origin. Attribution cannot be severed because **the connection is the retrieval path**.

## The Explicit Discovery Operation

Nelson provides a dedicated FEBE operation for exactly this purpose:

> **FINDDOCSCONTAINING**: "This returns a list of all documents containing any portion of the material included by \<vspec set\>."
> — [LM 4/70]

This operation answers the question: "Where else does this content appear?" It works because transclusions share I-addresses — the system can trace from any content to every document that includes it.

## Why This Matters: Three Consequences

**1. Correspondence across versions.** When two versions of a document share I-space content, the system can identify which parts correspond without explicit annotation:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same."
> — [LM 2/20]

**2. Automatic royalty attribution.** The economic model depends on knowing whose content is being delivered:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically."
> — [LM 2/45]

This "determined automatically" is possible only because the system preserves content identity through I-addresses.

**3. Non-destructive quotation.** The entire publishing model rests on content identity being preserved through transclusion:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document."
> — [LM 2/36]

## The Contrast: Live vs Dead

Nelson draws a sharp line between content within the system (identity preserved) and content extracted from it (identity lost):

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about."
> — [LM 2/48]

A copy outside the system is "frozen and dead" precisely because it severs the identity relationship. Inside the system, the identity relationship is what makes content *alive* — discoverable, attributable, compensable, and interconnected.

## Summary

The system **must** preserve the identity of shared content. This is not one guarantee among many — it is the architectural foundation. The I-space/V-space separation exists to make this possible. Transclusion depends on it. Royalties depend on it. Version comparison depends on it. Link survivability depends on it. The FINDDOCSCONTAINING operation exists to expose it. A reader can always determine that content appearing in their document originated elsewhere, trace it to its home, and discover every other document that shares it.
