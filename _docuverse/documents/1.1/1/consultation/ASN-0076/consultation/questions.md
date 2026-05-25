# Sub-Questions — EDITLINK Operation

**Inquiry:** Nelson (LM 4/79) lists 'editable links' as a desired feature. The current spec makes links immutable once created (L12). Editing a link should follow the same permanence pattern as editing a document — the original is never destroyed. A new link is created with modified endsets, and the relationship between old and new is recorded. The original link's guarantees are unaffected.

1. [theory] When a user "edits" a link, what must the system guarantee about the original link's continued existence and addressability?
2. [theory] What is the identity relationship between an original link and its edited successor — are they considered the same link or distinct links sharing a lineage?
3. [theory] Must every document or link that referenced the original link continue to resolve to the unchanged original after an edit occurs?
4. [theory] What must the system record about the relationship between an old link and its modified successor so users can trace the editing history?
5. [theory] If a link's endsets are modified, must the original endsets remain permanently retrievable as content in their own right?
6. [theory] Can multiple users independently "edit" the same original link, producing divergent successor links, and what must the system guarantee about each branch?
7. [theory] What permissions or ownership claims must govern who may create an edited successor to an existing link?
8. [theory] Must edited links be visible to the original link's author, or is the successor relationship purely a public record?
9. [theory] How does the design distinguish between a link that has been "edited" and a wholly new link that happens to share endpoints with an existing one?
10. [theory] What must the system guarantee about the permanence of the lineage record itself — can the connection between original and edited link ever be severed or revised?
11. [evidence] When a link is created via `docreatelink`, is there any field in the link orgl structure reserved for a "supersedes" or "previous version" pointer that could record a relationship to a prior link?
12. [evidence] Does `findnextlinkvsa` allocate link V-addresses in a way that would allow a "revised" link to be placed adjacent to its predecessor in the document's link subspace (`2.x`), or are they always strictly monotonic with no spatial relationship?
13. [evidence] Can a link's endsets be re-indexed in the spanfilade without removing the original endset entries, given that `insertspanf` is write-only and no `deletespanf` exists?
14. [evidence] If a "new version" link were created with the same three endsets as an existing link, would `findlinksfromtothreesp` return both as discoverable, or does the spanfilade have any deduplication that would suppress the duplicate?
15. [evidence] Does the link orgl structure include a type field separate from the type endset, that could distinguish an "original" link from a "revision-of" link?
16. [evidence] Could CREATENEWVERSION be invoked on a link orgl ISA (e.g., `docISA.0.2.N`) the way it is invoked on a document ISA, given that both are non-molecules allocated via `findisatoinsertnonmolecule`?
17. [evidence] When `link2sporglset` extracts I-addresses from a link, does it traverse a fixed three-endset structure, or could it handle a fourth endset slot representing a "supersedes" relationship to a prior link's ISA?
18. [evidence] If a link's POOM entry is removed via DELETEVSPAN on subspace `2.x` and a new link is then created at the same V-position, does the new link's `findnextlinkvsa` allocation account for the freed position or skip past the original's I-address?
19. [evidence] Does `retrieveendsets` accept a link ISA and return its endsets regardless of whether the link is currently mapped in any document's POOM, allowing an "old" superseded link to still be queried by ID?
20. [evidence] Is there any mechanism in the spanfilade index structure that would let `find_links` distinguish between two links with overlapping I-address endsets — e.g., a "current" and a "superseded" version — or are they returned as an undifferentiated set?
