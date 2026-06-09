# Sub-Questions — REARRANGE Operation

**Inquiry:** What happens when two regions of a document's content are transposed by cut points? What changes about position and what is preserved about content identity, what relationship must the rearranged regions bear to their prior V-positions, to the content between them that was not part of either region, and to links anchored within or across the moved regions, what does transposing two regions together (rather than moving one and waiting to move another) reveal about ordering invariants, link survival across reorderings, and the visibility of content that is structurally unchanged but newly displaced, and what invariants must the operation preserve about content permanence, the V-extent of the document, the discoverability of moved content under its new positions, and the isolation of other documents whose arrangements share I-addresses with the rearranged content?

1. [theory] When two regions are transposed, what must be preserved about the identity of the content even though its position within the document changes?
2. [theory] What relationship must each rearranged region bear to the positions it occupied before the transposition?
3. [theory] What must the design guarantee about the content lying between the two moved regions that was itself part of neither?
4. [theory] How must a link anchored entirely within one of the moved regions behave once that region appears at its new position?
5. [theory] What must happen to a link that spans across both moved regions, or from a moved region into stationary content, after the transposition?
6. [theory] What does transposing two regions in a single operation — rather than moving one and later the other — reveal about the ordering guarantees the document must uphold?
7. [theory] What must remain true about the document's total extent of content after the rearrangement, compared with before?
8. [theory] How must moved content remain discoverable to a user who looks for it under its new position in the document?
9. [theory] What must the design guarantee about the permanence of content that is displaced but otherwise structurally unchanged?
10. [theory] When the rearranged content is shared with another document, what isolates that other document's arrangement from being altered by this transposition?
11. [evidence] In a 4-cut swap REARRANGE exchanging regions `[a,b)` and `[c,d)`, does `makeoffsetsfor3or4cuts` compute the offset for the intervening region `[b,c)` as pure tumbler arithmetic, and what net V-displacement does that middle region receive?
12. [evidence] After a pivot or swap, do the I-displacement and I-width fields of every affected POOM bottom crum remain byte-for-byte identical to their pre-REARRANGE values while only V-displacement changes?
13. [evidence] Does the total root width (V-extent) of the document's text subspace remain invariant across REARRANGE, given that `rearrangend` only redistributes offsets among existing crums rather than allocating or freeing span?
14. [evidence] When a swap moves region `[c,d)` to where `[a,b)` was, can the resulting V-positions of the two regions overlap or collide, or does `rearrangecutsectionnd`'s region classification guarantee a disjoint partition of the new V-space?
15. [evidence] If a link's source endset is anchored entirely within region `[a,b)`, after that region moves does `find_links` still resolve it through unchanged I-address overlap, and do the reported endset V-addresses reflect the new post-move positions?
16. [evidence] When a single endset spans a cut boundary so that part lies in `[a,b)` and part in the untouched middle `[b,c)`, does REARRANGE fragment that endset into multiple non-contiguous V-spans on subsequent resolution?
17. [evidence] Does `makeoffsetsfor3or4cuts` apply any guard against a computed offset pushing a `1.x` text crum's V-position across the `2.x` link subspace boundary, or is cross-subspace displacement possible as in [EC-REARRANGE-CROSS-SUBSPACE]?
18. [evidence] For content structurally unchanged but newly displaced (the middle region in a swap), does it receive a fresh POOM entry or is its existing crum's V-displacement simply adjusted by `tumbleradd`/`tumblersub`?
19. [evidence] Given [INV-ENFILADE-CONFLUENCE], does performing a single 4-cut swap produce the same final POOM logical content as two separate sequential pivots achieving the same transposition, or do the intermediate states differ in discoverable results?
20. [evidence] When the rearranged content shares I-addresses with another document via transclusion, does [FC-DOC-ISOLATION] guarantee that document's POOM V-positions are wholly unaffected, since REARRANGE operates on a single `fullcrumptr`?
