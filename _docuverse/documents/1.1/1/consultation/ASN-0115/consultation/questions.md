# Sub-Questions — RETRIEVEV Operation (content delivery by spec-set)

**Inquiry:** What happens when the system is asked to deliver the actual content determined by a spec-set? What is returned, what relationship must the returned material bear to the spec-set asked about and to the arrangements that bind those spans to content, what does delivering the material together reveal about transclusion and subspace crossing that single-span delivery would not, and what invariants govern the material the operation may return?

1. [theory] When the system is asked to deliver the actual content named by a set of spans, what exactly must come back — the bytes of content themselves, or some description of where they live?
2. [theory] Must the delivered content correspond span-for-span to what the spec-set asked about, so that nothing extra is returned and nothing requested is silently omitted?
3. [theory] What relationship must the returned material bear to the arrangement that binds those spans to content — must delivery reflect the exact content each span currently designates, or content as it stood at some version?
4. [theory] When the requested spans draw on content that is shared by transclusion across documents, what does delivering them together reveal that delivering one span at a time would conceal?
5. [theory] If the same underlying content appears in two of the requested spans through transclusion, must the system reveal that the two deliveries are the identical content, or may it return them as if unrelated?
6. [theory] When a single request gathers spans whose content originates in different documents, what must the design guarantee about presenting that material as one coherent delivery rather than disconnected fragments?
7. [theory] Must the order in which content is delivered honor the order of the spans as asked for, and what guarantee governs the boundaries between one span's content and the next?
8. [theory] What invariant ensures the delivered content is faithful — that no character is altered, fabricated, or dropped relative to the content the spans permanently designate?
9. [theory] If part of the spec-set names content that no longer exists or was never established, what must the operation do — refuse entirely, deliver what it can, or signal the gap?
10. [theory] What must the design promise about repeatability: if the same spec-set is asked for again against unchanged arrangements, must the delivered material be identical every time?
11. [evidence] When RETRIEVECONTENTS is given a multi-span SpecSet, does it return content in spec-set order or re-sort the spans by V-address via `incontextlistnd` before delivering bytes?
12. [evidence] How does content delivery walk the POOM to resolve each VSpec to I-addresses, and does it route through `vspanset2sporglset` before the granfilade lookup?
13. [evidence] For a VSpec whose V-range maps to non-contiguous I-addresses (e.g. across a CREATELINK allocation gap), is the returned content split into multiple segments or concatenated as one contiguous byte run?
14. [evidence] Does the returned byte length always equal the sum of the SpecSet's V-widths, or can boundary slicing via `whereoncrum`/`slicecbcpm` alter the delivered extent?
15. [evidence] When a SpecSet references V-positions with no backing POOM entry (a gap or deleted range), are those positions silently filtered during I→V resolution, or does delivery fail?
16. [evidence] If two VSpecs in one SpecSet resolve to the same shared I-addresses (transclusion within a document), does RETRIEVECONTENTS return the identical bytes twice, once per V-position?
17. [evidence] Can a single RETRIEVECONTENTS SpecSet span multiple documents, and if so does it honor FC-DOC-ISOLATION by reading each target document's POOM independently?
18. [evidence] Given INV-BYTE-OPAQUE, does retrieving a VSpec whose boundaries fall mid-character return split partial UTF-8 bytes without any encoding correction?
19. [evidence] If a SpecSet crosses into the link subspace (`2.x` internally), does content delivery return link-orgl I-address bytes, or is delivery restricted to text subspace `1.x`?
20. [evidence] Does RETRIEVECONTENTS always source bytes from the granfilade by I-address (FC-GRANFILADE-PERMANENT), meaning deleted-then-orphaned I-addresses are still deliverable if a SpecSet somehow references them?
