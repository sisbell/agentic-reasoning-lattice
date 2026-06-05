# Sub-Questions — RETRIEVEENDSETS Operation (content-region search)

**Inquiry:** What happens when the system is asked, of a given region of content, which link endsets touch it? What is returned, what relationship must the returned endsets bear to the region asked about, what does the result reveal about the links anchored to that region without naming the links themselves, and what invariants govern the endsets the operation may return?

1. [theory] When the system is asked which endsets touch a region of content, must it return the endsets themselves rather than the identities of the links that own them?
2. [theory] What relationship of overlap must hold between a returned endset and the region asked about — must they share content, or merely touch at a boundary?
3. [theory] Must an endset be returned in full even when only part of it falls within the queried region, or only the portion that intersects?
4. [theory] Does the design guarantee that every endset anchored to any part of the region appears in the result, with none omitted?
5. [theory] Must the system guarantee that no endset is returned which fails to touch the region at all?
6. [theory] What must the result reveal about how many distinct links are anchored to the region, given that links are never named in the answer?
7. [theory] If the same region is asked about twice with the content unchanged, must the system return identical endsets each time?
8. [theory] When content within the region has been edited, what must the endsets in the result reflect about where the links now reside?
9. [theory] Must endsets belonging to a single link be distinguishable in the result from endsets belonging to different links touching the same region?
10. [theory] Does the design permit a region with no links anchored to it to yield an empty result, and must that emptiness be a permanent guarantee about that region's content?
11. [evidence] When a content region is supplied as a V-span, is it first converted to an I-span via the POOM before any spanfilade search for touching endsets, and what is returned if part of the region maps to no POOM entry?
12. [evidence] What overlap relation must a returned endset's I-span bear to the queried region's I-span — full containment, partial overlap, or any non-empty intersection?
13. [evidence] When a matching endset only partially overlaps the queried region, does the operation return the endset's full I-span or only the sub-span that intersects the region?
14. [evidence] Does the region-to-endset query distinguish among the three endset roles (source, target, type), or does it return any endset of any role whose I-span touches the region?
15. [evidence] Because the spanfilade is write-only and monotonic, can the query return endsets pointing at content that has been deleted from every current POOM (stale DOCISPAN entries)?
16. [evidence] Are unreferenced I-addresses (DEL5 ghosts) within a matching endset silently filtered during the I→V conversion of the result, yielding partial or empty endset reports?
17. [evidence] Does the operation discover endsets anchored through transclusion — endsets whose I-addresses this document shares with another document — when the region is phrased in this document's V-space?
18. [evidence] Given that `find_links` ignores the orgl range parameter (`TRUE||!homeset`), does the region-to-endset query likewise search the spanfilade globally rather than scoping to the queried document?
19. [evidence] If the queried region covers multiple non-contiguous I-address ranges (from CREATELINK or insert gaps), is one spanfilade search issued per I-span and the matching endsets unioned?
20. [evidence] What invariant guarantees the returned endsets reference content by I-address identity, so the result is stable under INSERT/DELETE/REARRANGE shifts of the V-positions used to phrase the query?
