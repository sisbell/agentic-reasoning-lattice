# Sub-Questions — RETRIEVEDOCVSPAN Operation (document V-stream extent query)

**Inquiry:** What happens when a document is asked, by its identity alone, for the origin and extent of its V-stream? What does the returned span describe, what relationship must it bear to the document's current arrangement, what does the caller learn from the answer that the document's identity alone does not already disclose, and what invariants govern the span the operation may return?

1. [theory] When a document is asked only by its identity to report where its content begins and how far it extends, what must that answer describe about the document as a whole?
2. [theory] What does the origin of a document's content stream signify, and must it remain fixed for the entire life of the document?
3. [theory] What relationship must hold between the extent the document reports and the content currently arranged within that document?
4. [theory] If a document's arrangement changes through editing, must the reported extent change with it, or is extent independent of how content is arranged?
5. [theory] What does a caller learn from the returned origin and extent that the document's identity alone does not already make known?
6. [theory] Must every document be able to answer this question about itself, or are there documents for which an origin and extent are undefined?
7. [theory] What permanence guarantee governs the reported span, given that the document's content may be shared with or referenced by other documents?
8. [theory] Must the reported extent account for all content the document has ever held, or only the content presently belonging to it?
9. [theory] What invariant ensures the reported origin and extent together describe one continuous, well-formed region rather than a fragmented or empty one?
10. [theory] If two documents share content, must each still report its own distinct origin and extent, independent of the other's answer?
11. [evidence] When RETRIEVEDOCVSPAN reports the root width of a document containing both text (1.x) and link (2.x) subspaces, does the returned span's width tumbler bridge across the inter-subspace gap, and what start position does it report?
12. [evidence] Does the span returned by RETRIEVEDOCVSPAN derive its start position from the 2D POOM root's displacement coordinate (tracked via `setwispnd`), and is that displacement guaranteed to equal the minimum V-address of any current POOM bottom crum?
13. [evidence] For an empty-after-DELETE document whose POOM tree retains intermediate nodes (levelpull disabled), does RETRIEVEDOCVSPAN return a zero-width span or does the residual tree height affect the reported root width?
14. [evidence] Is the width tumbler returned by RETRIEVEDOCVSPAN computed as root offset plus root displacement, and does it reflect logical V-extent independent of the physical tree shape per enfilade confluence?
15. [evidence] When a document has text only in subspace 1.x with no links, does RETRIEVEDOCVSPAN return exactly the contiguous text extent, and does that span's start equal the lowest text V-address rather than 1.0?
16. [evidence] After INSERT shifts text V-positions rightward, does the RETRIEVEDOCVSPAN root width grow by exactly the inserted width n, and does the reported start position remain unchanged?
17. [evidence] Does RETRIEVEDOCVSPAN require the document to be in the caller's open-document list (BERT-gated via findorgl), and does it fail silently returning nothing if the document is not open?
18. [evidence] Can RETRIEVEDOCVSPAN ever return a span whose width tumbler has a negative magnitude if a prior same-subspace DELETE produced negative V-position entries in the POOM?
19. [evidence] Does the bounding span RETRIEVEDOCVSPAN returns for a link-bearing document have a width whose exponent reflects the link subspace's exp=0 magnitude rather than the text subspace's finer-grained exp, given the V-width/I-width exponent encoding difference?
20. [evidence] Is the start position the operation returns the grasp (offset + displacement) at the POOM root, and does that grasp necessarily coincide with an actual occupied V-address, or can it point into an unoccupied gap?
