# Sub-Questions — Content Retrieval

**Inquiry:** What must RETRIEVE guarantee about returned content? How does retrieval interact with transclusion, versioning, and the two address spaces?

1. [nelson] When a user retrieves a span of a document, must the returned content be identical byte-for-byte to what was originally stored, regardless of how many documents transclude that same content?
2. [nelson] If a document includes content by transclusion from another document, must retrieval return the content as though it were native to the requesting document, or must the system reveal its origin?
3. [nelson] When retrieving from a specific version of a document, must the system guarantee that the returned content reflects exactly the state at version-creation time, even if later versions exist?
4. [nelson] Must retrieval of a document region that spans both original and transcluded material return a seamless, contiguous result, or may the system return fragments with gaps?
5. [nelson] If the same content appears at two different positions within a document through transclusion, must retrieval at each position return identical results?
6. [nelson] Does retrieval carry any obligation to report where the returned content originally came from, or is provenance information separate from the content guarantee?
7. [nelson] When content is retrieved by its permanent identity rather than by its position in a document, must the system return exactly the same bytes as retrieval by document position would?
8. [nelson] Must the system guarantee that content retrievable today remains retrievable tomorrow — does permanence of storage imply permanence of access?
9. [nelson] If a link points to a region of a document and that region contains transcluded content, must retrieval through the link return the content as the document presents it, not as the source document organizes it?
10. [nelson] When a document has multiple versions, must retrieval of shared content across those versions return identical results, confirming that versioning does not alter the underlying content?
11. [gregory] When RETRIEVEDOCVSPAN is called on a document containing both text and links, does it return a single bounding span covering both subspaces, and if so, does the returned content include raw link orgl bytes interleaved with text?
12. [gregory] Does RETRIEVEDOCVSPANSET always return exactly two VSpecs (one for text subspace 1.x, one for link subspace 0.2.x), or can it return more than two if there are gaps within a single subspace?
13. [gregory] When retrieving a V-span that crosses a POOM entry boundary (where two non-contiguous I-address ranges are mapped to adjacent V-positions), does the retrieval silently concatenate the content from both I-ranges into a single byte sequence?
14. [gregory] After COPY transcludes content from doc1 into doc2, does retrieving the same V-span from both documents return byte-identical content, and is the retrieval path identical (same granfilade leaf nodes accessed)?
15. [gregory] After CREATENEWVERSION, does retrieving the full text span from the version return byte-identical content to retrieving the same span from the original, even if the original has been subsequently edited?
16. [gregory] When a V-span request partially overlaps a POOM entry (e.g., requesting V:[1.3,1.5] when a single entry covers V:[1.1,1.7]), does the retrieval slice the I-address range correspondingly, or does it return the full entry's content?
17. [gregory] Does retrieval of link subspace content (V-addresses in 0.2.x) return the raw link orgl structure as bytes, and if so, what is the byte layout — are the three endsets stored as serialized tumbler sequences?
18. [gregory] After INSERT shifts existing content to higher V-positions, does retrieving by the OLD V-addresses return the newly inserted content, or does it return empty/error for addresses that no longer map to the original content?
19. [gregory] Does `incontextlistnd` affect retrieval ordering when a document contains self-transclusion (the same I-addresses at multiple V-positions), and if so, are results always returned in ascending V-address order regardless of POOM tree shape?
20. [gregory] When retrieving from a document where DELETE has produced negative V-position tumblers, does the retrieval function accept a negative V-address as a query parameter and return the displaced content, or are negative V-positions unreachable through the normal retrieval interface?
