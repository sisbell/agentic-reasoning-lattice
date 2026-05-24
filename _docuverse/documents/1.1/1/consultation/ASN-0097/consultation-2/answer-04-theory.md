## Question 4 [theory]

> What are the seventeen FEBE editing and document commands, and what is each command's intended state-level effect — in particular, which ones beyond INSERT, COPY/VCOPY, DELETEVSPAN, REARRANGE, APPEND, MAKELINK, CREATENEWDOCUMENT, CREATENEWVERSION can affect a document's arrangement?

# The Seventeen FEBE Commands in XU.87.1

Nelson states: "Of the 17 current commands in XU.87.1, only one command (RETRIEVEV) is concerned with delivery of the actual content fragments." [LM 4/61]

## Arrangement-Modifying Commands (8)

All 8 of these are already in your list:

1. **INSERT** [LM 4/66] — "This inserts <text set> in document <doc id> at <doc vsa>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text."
2. **DELETEVSPAN** [LM 4/66] — "This removes the given span from the given document." (Vstream removal; Istream content preserved.)
3. **COPY** [LM 4/67] — Transclusion: "The material determined by <spec set> is copied to the document determined by <doc id> at the address determined by <doc vsa>." The copy shares I-addresses with the source.
4. **REARRANGE** [LM 4/67] — "Rearrange transposes two regions of text."
5. **APPEND** [LM 4/67] — "This appends <text set> onto the end of the text space of the document <doc id>."
6. **MAKELINK** [LM 4/68] — "This creates a link in document <doc id> from <from set> to <to set> connected to <three set>."
7. **CREATENEWDOCUMENT** [LM 4/65] — "This creates an empty document. It returns the id of the new document."
8. **CREATENEWVERSION** [LM 4/66] — "This creates a new document with the contents of document <doc id>... The new document's id will indicate its ancestry."

## Read-Only Commands (9)

None affect document arrangement:

9. **RETRIEVEV** [LM 4/67] — Returns material specified by spec-set.
10. **RETRIEVEDOCVSPAN** [LM 4/68] — Returns origin and extent of document's V-stream.
11. **RETRIEVEDOCVSPANSET** [LM 4/68] — Returns counts of characters and links.
12. **RETRIEVEENDSETS** [LM 4/70] — Returns endsets of specified links.
13. **FINDLINKSFROMTOTHREE** [LM 4/69] — Returns links matching home/from/to/three constraints.
14. **FINDNUMOFLINKSFROMTOTHREE** — Counts matching links.
15. **FINDNEXTNLINKSFROMTOTHREE** [LM 4/69] — Paginated link search.
16. **FINDDOCSCONTAINING** [LM 4/70] — Returns documents containing specified material.
17. **SHOWRELATIONOF2VERSIONS** [LM 4/70] — "Returns a list of ordered pairs of the spans of the two spec-sets that correspond."

## Direct Answer

**None of the remaining 9 commands beyond your list affect a document's arrangement.** All non-arrangement-modifying commands are purely read-only — searches, retrievals, comparisons, and metadata queries. The 8 you enumerated exhaust the arrangement-affecting operations in XU.87.1.

NEED_RAW: 4/61-4/70 to verify (a) whether VCOPY is a distinct command from COPY (your phrasing "COPY/VCOPY" suggests a variant my curated sources don't document), and (b) that exactly these 17 names appear in Nelson's published command roster — my list synthesizes operations.md and febe-protocol coverage to reach 17 unique commands matching Nelson's count, but the precise published nomenclature would benefit from page-image verification.
