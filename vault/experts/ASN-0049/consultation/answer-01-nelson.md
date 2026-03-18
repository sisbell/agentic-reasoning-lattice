## Question 1 [nelson]

> When the same content appears in two documents, does the system guarantee that both documents reference one stored instance rather than maintaining separate copies?

## Yes — But the Guarantee Is Structural, Not About Storage Efficiency

The system guarantees that transcluded content shares a single I-space identity. This is not an optimization; it is the architecture itself.

### The Mechanism: I-Space Is Append-Only; V-Space Is Reference

Content is created once in I-space and receives a permanent address. Documents are V-space arrangements that *reference* I-space content. When document B includes content from document A, B's V-stream maps to A's I-space bytes. No duplication occurs.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The COPY operation — the mechanism for transclusion — creates a V-space mapping to existing I-space content, not a duplicate:

> "The material determined by \<spec set\> is copied to the document \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

Nelson is explicit that this eliminates copying:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

### The Guarantee Is About Identity, Not Deduplication

The deeper point: shared I-space addresses are what make attribution, royalty tracking, and version comparison *work*. The system can answer "which documents contain this content?" (FINDDOCSCONTAINING) precisely because transcluded content shares I-addresses with the original:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

If content were duplicated, this operation would be impossible — there would be no structural link between the copy and the original.

### The Critical Distinction: Transclusion vs. Independent Creation

The guarantee applies **only to content that enters the second document through transclusion** (the COPY operation or CREATENEWVERSION). If two users independently type the same words, each gets separate I-space bytes with different permanent addresses. The system distinguishes "quoted from the original" (shared I-address) from "wrote the same words independently" (different I-addresses).

This is by design. Content identity is based on *creation*, not *value*. The I-address encodes provenance — which document created which bytes — and that relationship is what makes attribution structural rather than metadata.

### Summary

| Scenario | Shared instance? | Why |
|----------|-----------------|-----|
| Transclusion (COPY) | **Yes** — V-space maps to existing I-space | The whole point of transclusion |
| New version (CREATENEWVERSION) | **Yes** — new V-arrangement over same I-content | Versions share I-space by definition |
| Independent creation of identical text | **No** — separate I-space bytes | Identity is by creation, not value |

The guarantee is not "we won't waste storage on duplicates." It is: **transcluded content maintains a permanent, structural connection to its origin that cannot be severed.** Single-instance storage is how that connection is implemented.
