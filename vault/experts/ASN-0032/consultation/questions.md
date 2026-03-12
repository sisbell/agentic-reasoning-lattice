# Sub-Questions — Link Ontology

**Inquiry:** What is a link in the Xanadu system? What are links for, what do they connect, and what must be true about them as permanent objects in the docuverse?

1. [nelson] What does a link actually connect — whole documents, specific spans of content within documents, or both?
2. [nelson] Must every link be a permanent object in the docuverse with its own stable identity, just as documents and content are permanent?
3. [nelson] Must a link remain valid and meaningful even after the content it connects has been edited, rearranged, or extended by its author?
4. [nelson] Must a link be visible and discoverable from both ends — so that an author can always see who has linked to their content?
5. [nelson] Does a link exist outside the documents it connects, as an independent object in the docuverse rather than being embedded inside one of them?
6. [nelson] Who owns a link — the person who created it, one of the connected document authors, or does ownership not apply to links?
7. [nelson] Can a link ever be destroyed or retracted, or does permanence mean that once a link exists it must exist forever?
8. [nelson] How do links relate to quotation and transclusion — is a transclusion a special kind of link, or are they fundamentally different operations?
9. [nelson] Must the system guarantee that every version of a document preserves the links that were present at each point in its history?
10. [nelson] Can anyone create a link to any content in the docuverse, or must the system enforce permissions about who may link to what?
11. [gregory] When a link's source endset contains multiple non-contiguous I-spans (e.g., from content that was rearranged after link creation), does RETRIEVEENDSETS return all spans as a single specset, and does the ordering of spans within that specset carry semantic meaning?
12. [gregory] The type endset references I-addresses at `1.0.2.x` in the global type namespace — what types were defined or envisioned, and does the type endset point to actual stored content in the granfilade (like a type name string) or to a conventionally assigned address?
13. [gregory] Was link permanence — no delete operation exists for links in any storage layer — a deliberate design requirement of the Xanadu model, or an implementation simplification that happened to align with the "nothing is ever lost" philosophy?
14. [gregory] When an orphaned link (all endpoint content deleted from every V-stream) becomes discoverable again because its endpoint I-addresses reappear via transclusion into a new document, was this "resurrection" behavior an intended design property that users/applications were expected to rely on?
15. [gregory] Can a single link endset legitimately reference content from multiple different documents (e.g., source endset contains I-spans from doc A and doc B), and if so, what is the intended semantic — does such a link assert a relationship across a composite selection?
16. [gregory] The `TRUE||!homeset` override in `sporglset2linkset` makes find_links search globally rather than scoped to a home document set — was global link discovery the original design intent, with the home-document filtering being dead code, or was scoped discovery intended but never completed?
17. [gregory] CREATENEWVERSION copies text but not links, yet links remain discoverable from the version through shared I-addresses — was this asymmetry (links follow content identity rather than document membership) a core design principle, and were there discussions about whether versions should carry their own link copies?
18. [gregory] Links are stored in the document's link subspace at `0.2.x` in the POOM — what is the significance of a link having a V-address within a specific document, given that links are discoverable globally via I-address overlap regardless of which document "owns" them?
19. [gregory] For a link whose target endset spans a region that has been partially deleted (some I-addresses still in V-streams, others orphaned), FOLLOWLINK returns only the surviving portion after I→V filtering — was partial endset resolution an acceptable design outcome, or should the system have signaled incompleteness to the caller?
20. [gregory] Internal links (source and target both reference the same document) — what concrete use cases motivated support for same-document links, and does bidirectional follow-link on an internal link have different semantics than on a cross-document link?
