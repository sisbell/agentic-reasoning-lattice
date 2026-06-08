# Sub-Questions — COPY Operation

**Inquiry:** What happens when content named by a spec-set is placed at a V-position in a document — what Nelson calls transclusion? What is reused from the existing content store and what is recorded fresh in the destination, what relationship must the placed material bear to its source's identity, to the destination's prior arrangement, and to any other documents that already share those I-addresses, what does placing content from multiple non-contiguous sources together (rather than from a single contiguous source) reveal about shared identity, ownership independence, and the boundary between reuse and replication, and what invariants must the operation preserve about content immutability, the permanence of the source's identity in the destination, the survival of links anchored to the reused content, and the isolation of the source document from the act of being copied from?

1. [theory] When content is placed into a document by transclusion, what must remain identical between the placed material and its source — and what does the destination record as newly its own?
2. [theory] What relationship must transcluded content bear to the identity of its source, such that the system can always say where the content originally came from?
3. [theory] Must the act of transcluding content into a destination leave the source document completely unaware that it has been copied from?
4. [theory] When the same content appears in multiple documents through transclusion, what must the design guarantee about the shared identity those documents hold in common?
5. [theory] What must the design preserve about the immutability of content when that content is reused in a new document rather than recreated?
6. [theory] How does placing content together from several separate, non-adjacent sources — rather than one continuous stretch — reveal the difference between genuine reuse and mere replication?
7. [theory] When transcluded material is set into a destination's existing arrangement, what must the operation guarantee about the prior ordering and position of the content already there?
8. [theory] What must the system guarantee about the survival of links anchored to content that is reused through transclusion?
9. [theory] When content drawn from independently owned sources is gathered into one document, what must remain true about the ownership independence of each contributing source?
10. [theory] What makes transclusion a sharing of one identity across documents rather than the manufacture of a separate copy — what is the boundary the design must hold?
11. [evidence] When COPY places a spec-set at V-position v in the target, does it create new POOM entries pointing to the SAME I-addresses as the source, leaving the granfilade entirely unmodified?
12. [evidence] Does COPY shift existing target POOM entries at V-positions ≥ v to the right by the copied width, using the same makegappm machinery as text insertion?
13. [evidence] When a copied V-span maps to non-contiguous I-addresses in the source, does vspanset2sporglset automatically split it into multiple sporgls without front-end pre-splitting?
14. [evidence] If copied content lands contiguous with existing I-addresses already in the target POOM, does isanextensionnd merge it into one bottom crum via reach==origin rather than creating a separate entry?
15. [evidence] Does COPY create a DOCISPAN entry in the spanfilade for the target document while the source document's spanfilade entries remain untouched?
16. [evidence] Does COPY read only the source document's POOM and write exclusively to the target's fullcrumptr, leaving the source POOM and every other transcluding document's POOM unchanged?
17. [evidence] When multiple documents already share the I-addresses being copied, does the new target's COPY make those documents' links discoverable from the target via I-address overlap in find_links?
18. [evidence] For a sporgl built from multiple non-contiguous source spans, does each contiguous I-span produce its own DOCISPAN entry, making destination storage O(span count) rather than O(byte count)?
19. [evidence] In self-transclusion (source and target ranges within the same document), does the I→V mapping via incontextlistnd correctly return all V-positions bound to the shared I-address, including overlapping copy ranges?
20. [evidence] Does COPY require the target open with WRITEBERT and the source open with at least READBERT, and does the source's read-only access guarantee no mutation of its content identity during the copy?
