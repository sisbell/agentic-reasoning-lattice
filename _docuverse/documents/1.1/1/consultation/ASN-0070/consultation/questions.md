# Sub-Questions — FOLLOWLINK Operation

**Inquiry:** Given a link and a document, how does the system resolve the link's endsets to visible Vstream positions? What determines which content is reachable and what is the form of the result?

1. [theory] What must the system guarantee about which content a link's endsets identify when the document being viewed is a different version than the one the link was originally attached to?
2. [theory] When a link references content that has been edited, what determines whether the endset still resolves to visible content or becomes unreachable?
3. [theory] What is the design's commitment about the form of the resolved result — must it be a contiguous region of visible content, a set of disjoint regions, or something else?
4. [theory] How must the system handle an endset that refers to content which has been removed from every version of the document currently being viewed?
5. [theory] What guarantees must hold about the ordering of resolved endset positions relative to the order of content as it appears to the user?
6. [theory] When the same underlying content appears in multiple places within a single document, must a link's endset resolve to all such occurrences, or only the original?
7. [theory] What must the system promise about the stability of a link's resolution — if the same link is resolved against the same document version twice, must the result be identical?
8. [theory] How does the design distinguish between content that is genuinely part of a document and content that is merely transcluded from elsewhere, when resolving link endpoints?
9. [theory] What is the guarantee about partial resolution — if some portion of an endset is reachable in the current document but another portion is not, what must the user see?
10. [theory] Must the resolved result preserve the identity of the original content, so that the user can tell which underlying material each visible region came from?
11. [evidence] When `retrieveendsets` resolves a link's three endsets, does it materialize all three (source, target, type) in a single spanfilade traversal or perform three separate `findlinksfromtothreesp`-style searches?
12. [evidence] During I→V conversion via `span2spanset`, what is the exact filtering rule that drops "unreferenced" I-addresses (DEL5) — does it test membership in the target document's POOM only, or scan all open documents?
13. [evidence] When an endset's I-span maps to multiple V-positions in the target document (due to self-transclusion creating multiple POOM entries pointing at the same I-addresses), does `incontextlistnd` return all V-positions or only the first one encountered during 2D tree traversal?
14. [evidence] For a link whose endset references I-addresses that exist in the granfilade but appear in NO open document's POOM, does endset resolution return an empty VSpecSet, a partial result containing only the source-document positions, or raise an error?
15. [evidence] When the home document parameter to `find_links` is specified but `sporglset2linkset` overrides it via `TRUE||!homeset` [EC-FIND-LINKS-GLOBAL], does the endset resolution step also ignore the home document, or is the home document used to scope which POOM is consulted for I→V conversion?
16. [evidence] If an endset's I-span crosses a non-contiguous boundary in the target document's POOM (the linked content has been split by REARRANGE), does the resolved VSpecSet contain one VSpec per contiguous V-run, or a single VSpec covering the bounding range?
17. [evidence] Does endset resolution require the target document to be opened with BERT access, or can endsets be resolved against a closed document's persisted POOM via direct enfilade query?
18. [evidence] What is the wire format of the returned endsets — a flat list of VSpec triples, three separately tagged VSpecSets keyed by endset role (source/target/type), or sporgls preserving I-address provenance?
19. [evidence] When the type endset references a type registered at `1.0.2.x` in the global type namespace, is that I-address resolved to a V-position in the type document's POOM, or returned as a raw I-address since the type namespace has no document context?
20. [evidence] Does `retrieveendsets` apply the same V-address insertion-sort ordering used by `incontextlistnd` to the returned positions, or does it preserve the I-address order from the link's endset specset?
