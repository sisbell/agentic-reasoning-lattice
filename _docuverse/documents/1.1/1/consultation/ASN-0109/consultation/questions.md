# Sub-Questions — RETRIEVEENDSETS Operation

**Inquiry:** What happens when a link's endsets are read directly by the link's address? What is returned, what does the reader learn about the relationship the link records, what does this reveal that following the link would not, and what invariants govern the endsets the read can return?

1. [theory] When a link is read by its address, what must the system return about the content endpoints the link connects?
2. [theory] What guarantee governs whether the endsets a read returns are the original endpoints recorded at the link's creation, or the endpoints as they exist in the current versions?
3. [theory] Must reading a link's endsets reveal the identity of every document participating in the relationship, even documents the reader has never seen?
4. [theory] What does the reader learn about the direction or roles of the connected endpoints — which side is the source and which is the destination of the relationship?
5. [theory] What does reading the endsets directly reveal about the relationship that traversing to one endpoint would never expose?
6. [theory] Must the endsets returned by a read identify content by stable identity, so the same link read at different times names the same content?
7. [theory] When a link connects spans of content rather than whole documents, what must the read return about the precise boundaries of each connected region?
8. [theory] What invariant ensures the endsets a read returns are consistent with what is actually stored — that the system cannot report endpoints the link does not hold?
9. [theory] Must reading a link's endsets be permitted even when the content at those endpoints has been edited, deleted, or made inaccessible to the reader?
10. [theory] What must the read reveal about the type or meaning of the relationship the link records, beyond merely naming its endpoints?
11. [evidence] When RETRIEVEENDSETS reads a link by its address, does it return all three endsets (source/from, target/to, type) as distinct I-address spans, and in what order are they delivered?
12. [evidence] Does reading endsets resolve the stored I-address spans into V-positions, or does the reader receive raw I-addresses from the link orgl before any I→V conversion occurs?
13. [evidence] During the I→V conversion of a read endset, are unreferenced I-addresses (those in no current POOM) silently filtered, and does this produce a partial or empty endset for ghost links?
14. [evidence] Does RETRIEVEENDSETS search the spanfilade to reconstruct the endsets, or does it read the endset spans directly from the link orgl stored in the granfilade?
15. [evidence] Since endsets reference content by I-address identity, does reading a link's source endset reveal the same I-spans regardless of which document or version the linked content currently appears in?
16. [evidence] When the type endset is read, does it return the I-address registered in the global type namespace (`1.0.2.x`), and is that resolved differently from the source and target content endsets?
17. [evidence] If a single logical endset was split into multiple sporgl entries at creation time (content spanning non-contiguous I-ranges), does the read return multiple spans, and does the reader see them as one endset or several?
18. [evidence] Does reading endsets require the link's home document to be open under BERT, or can endsets be read by link address without an open-document precondition?
19. [evidence] After REARRANGE fragments linked content across non-contiguous V-positions, does reading the endset report multiple V-spans where a single span existed before, while the underlying I-address spans remain unchanged?
20. [evidence] Are the I-address spans returned by a read endset guaranteed immutable for the life of the link, such that two reads of the same link's endsets at different times always return identical I-spans even after DELETE on the referenced content?
