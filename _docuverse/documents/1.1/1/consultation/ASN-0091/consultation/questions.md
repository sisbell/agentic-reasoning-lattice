# Sub-Questions — REARRANGE Operation

**Inquiry:** What is the precise effect of reordering segments of Vstream content by cut points? What is preserved about content identity, what changes about position, and what invariants must the completed operation maintain?

1. [nelson] When segments of a document's content stream are rearranged by cut points, does every byte of content retain its original identity, or does the act of repositioning create new content?
2. [nelson] If a link addresses a span of content that is split by a cut point during rearrangement, must the link continue to address exactly the same content bytes, even though they now occupy non-contiguous positions?
3. [nelson] After rearrangement, does the document's content stream contain exactly the same set of content as before — no additions, no losses — or may rearrangement discard or duplicate material?
4. [nelson] Must the system preserve a record of the original ordering so that the prior arrangement can be recovered, or is rearrangement a one-way transformation of document structure?
5. [nelson] When a segment is moved to a new position in the content stream, do the positions of all other segments shift to accommodate it, and must the system guarantee that no two segments occupy the same position?
6. [nelson] If a document transcludes content from another document and that transcluded region is split by a cut point during rearrangement, does the transclusion relationship survive intact for each resulting piece?
7. [nelson] Does rearrangement change what content the document contains, or only the order in which that content appears — and is this distinction a fundamental design guarantee?
8. [nelson] When two previously non-adjacent segments become adjacent through rearrangement, does the system treat the boundary between them differently from content that was originally contiguous?
9. [nelson] Must a rearrangement operation be expressible purely in terms of the document's own content stream, or can it reference content positions as they exist in other documents that share the same material?
10. [nelson] After rearrangement, if a reader follows a link into the rearranged document, must they arrive at the same content they would have reached before the rearrangement, regardless of its new position within the document?
11. [gregory] In `rearrangend`, how does `rearrangecutsectionnd` classify each POOM bottom crum relative to the 3 or 4 cut points — what are the distinct region categories, and which offset is applied to entries in each region?
12. [gregory] When a cut point falls in the interior of an existing POOM bottom crum (not on a boundary), does `rearrangend` split the crum into two pieces before applying offsets, or does it treat the entire crum as belonging to one region?
13. [gregory] In `makeoffsetsfor3or4cuts`, how are the tumbler offsets for each region derived from the cut positions — is it pure arithmetic on the cut-point differences, and does the computation use `tumblersub`/`tumbleradd` or a different mechanism?
14. [gregory] Does REARRANGE create, modify, or remove any spanfilade entries, or does it exclusively mutate the document's POOM while leaving the spanfilade and granfilade completely untouched?
15. [gregory] If a 3-cut pivot is issued where cut `a` is in text subspace `1.x` and cut `c` crosses into link subspace `2.x`, does `rearrangend` proceed and relocate link POOM entries into text V-positions (or vice versa), or does some other guard prevent this?
16. [gregory] What happens in `rearrangend` when the supplied cut points are outside the document's current V-span — does the function detect this and abort, silently produce a no-op, or apply offsets to whatever entries happen to be in range?
17. [gregory] After a 3-cut pivot fragments a previously contiguous I-span across two non-adjacent V-regions, does `incontextlistnd` correctly return both V-positions when resolving that I-span back to V-space for link endset retrieval?
18. [gregory] Can `makeoffsetsfor3or4cuts` produce a negative tumbler offset that, when added to a POOM entry's V-displacement, yields a negative V-position — analogous to the `tumblersub` issue in DELETE?
19. [gregory] In a 4-cut swap where the middle region `[b,c)` contains no POOM entries (a gap), does `rearrangend` still compute and apply offsets to the empty region, or does it skip the middle and only exchange the `[a,b)` and `[c,d)` regions?
20. [gregory] After REARRANGE moves entries within the POOM's 2D enfilade, does `recombinend` fire to rebalance the tree, and if so, does the diagonal-sum reordering ever change the logical V-address ordering of the result — or is confluence guaranteed regardless of post-rearrange tree shape?
