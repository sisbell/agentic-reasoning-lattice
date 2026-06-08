# Sub-Questions — DELETE Operation

**Inquiry:** What happens when content over a span of a document is deleted? What is removed from the document's current arrangement and what survives in the permanent content store, what relationship must the remaining content bear to its prior V-positions and to other documents that may share the deleted I-addresses through transclusion, what does deleting a span (rather than a single position) reveal about the distinction between an arrangement no longer binding content and that content ceasing to exist, and what invariants must the operation preserve about content permanence, cross-document arrangement isolation, the survival of links anchored to addresses the deletion no longer arranges, and the discoverability of deleted material from other documents that still arrange it?

1. [theory] When content over a span is deleted, what is removed from the document's current arrangement and what must survive permanently in the content store?
2. [theory] What relationship must the content remaining after a deletion bear to the positions it occupied in the document before the span was removed?
3. [theory] Does deleting a span from one document guarantee that every other document sharing that same content through transclusion remains entirely unchanged?
4. [theory] What does deleting a span — rather than a single position — reveal about the distinction between an arrangement ceasing to bind content and that content ceasing to exist?
5. [theory] Must the system guarantee that deleted content remains permanently discoverable from other documents that still arrange it?
6. [theory] What must happen to a link anchored to content that a document's arrangement no longer includes after a deletion?
7. [theory] Can content that one document has deleted still be retrieved and shared as living content through any other document that continues to arrange it?
8. [theory] What invariant must the design preserve about content permanence when an editing operation removes a span from a document's current arrangement?
9. [theory] Must the boundaries of the deleted span be exactly reflected in how the remaining content is renumbered or re-positioned within the document?
10. [theory] When a span is deleted, what guarantee isolates that document's arrangement change from the arrangements of all documents that share the affected content?
11. [evidence] When DELETE targets a span, does `slicecbcpm` only fire for entries that partially overlap the cut boundaries (interior cuts where `whereoncrum == THRUME`), while entries entirely within the span are disowned and freed via `subtreefree`?
12. [evidence] For a boundary-aligned DELETE where cut points exactly match existing crum boundaries, is `slicecbcpm` skipped entirely, and does this guarantee no zero-width POOM pieces are ever produced?
13. [evidence] After DELETE removes a span, are surviving entries beyond the deleted region shifted left by the deletion width via `tumblersub`, and under what offset conditions does this produce a negative V-position tumbler?
14. [evidence] When a left-shift via `tumblersub` produces a negative V-position, does that entry sort before all positive entries in `tumblercmp`, and does the POOM continue to function for retrieval despite violating the expected bijectivity invariant?
15. [evidence] Does DELETE leave the granfilade entirely untouched, such that the I-addresses underlying the deleted span remain resolvable to their original bytes even though no POOM currently references them?
16. [evidence] After DELETE, do the corresponding DOCISPAN entries remain in the spanfilade (since no `deletespanf` exists), causing `find_documents_containing` to still return this document for the deleted I-addresses?
17. [evidence] When DELETE removes a span from document A, does a separate document B that transcludes those same I-addresses retain its own POOM entries and content completely unchanged, per the F0 cross-document frame axiom?
18. [evidence] When a DELETE in the text subspace `1.x` subtracts a text-level width (exp=-1) from a link position (exp=0), does the `strongsub` exponent guard return the link position unchanged, preserving link subspace `2.x` entries?
19. [evidence] If DELETE removes the last content referencing a link's endset I-addresses from this document's POOM, does the link orgl persist in granfilade and spanfilade, becoming undiscoverable via `find_links` from this document but re-discoverable if the content reappears via transclusion?
20. [evidence] After a DELETE that removes all of a document's content, does the enfilade retain intermediate nodes from prior growth (since `levelpull` is disabled), leaving the empty tree structurally taller than a freshly created empty tree while query results stay identical?
