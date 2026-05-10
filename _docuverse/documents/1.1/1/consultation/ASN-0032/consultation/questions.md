# Sub-Questions — Link Ontology

**Inquiry:** What is a link in the Xanadu system? What are links for, what do they connect, and what must be true about them as permanent objects in the docuverse?

**Trimmed from 20 to 10 — removed 3,4,8,9,11,14,16,17,19,20 (out of scope: discovery, operations, versioning)**

1. [nelson] What does a link actually connect — whole documents, specific spans of content within documents, or both?
2. [nelson] Must every link be a permanent object in the docuverse with its own stable identity, just as documents and content are permanent?
5. [nelson] Does a link exist outside the documents it connects, as an independent object in the docuverse rather than being embedded inside one of them?
6. [nelson] Who owns a link — the person who created it, one of the connected document authors, or does ownership not apply to links?
7. [nelson] Can a link ever be destroyed or retracted, or does permanence mean that once a link exists it must exist forever?
10. [nelson] Can anyone create a link to any content in the docuverse, or must the system enforce permissions about who may link to what?
12. [gregory] The type endset references I-addresses at `1.0.2.x` in the global type namespace — what types were defined or envisioned, and does the type endset point to actual stored content in the granfilade (like a type name string) or to a conventionally assigned address?
13. [gregory] Was link permanence — no delete operation exists for links in any storage layer — a deliberate design requirement of the Xanadu model, or an implementation simplification that happened to align with the "nothing is ever lost" philosophy?
15. [gregory] Can a single link endset legitimately reference content from multiple different documents (e.g., source endset contains I-spans from doc A and doc B), and if so, what is the intended semantic — does such a link assert a relationship across a composite selection?
18. [gregory] Links are stored in the document's link subspace at `0.2.x` in the POOM — what is the significance of a link having a V-address within a specific document, given that links are discoverable globally via I-address overlap regardless of which document "owns" them?
