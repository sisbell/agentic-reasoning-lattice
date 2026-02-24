# Sub-Questions — Links and Endsets

**Inquiry:** What must bidirectional links guarantee? What are endset semantics — how do links survive editing, deletion, and rearrangement of their target content?

1. [nelson] When a link connects two spans of content across different documents, what exactly does each endset point to — the content itself, or its position within the document?
2. [nelson] If a user inserts new content in the middle of a span that a link's endset references, does the link now include the new content, or does it continue to reference only the original content?
3. [nelson] When content that a link points to is deleted from a document, does the link break, or does it continue to exist pointing to the permanent content that was removed?
4. [nelson] Must every link be discoverable from both ends — if I can find all links pointing FROM a span, must I equally find all links pointing TO that span?
5. [nelson] Can a link's endsets be changed after the link is created, or is a link as permanent and immutable as the content it connects?
6. [nelson] If content referenced by a link is rearranged — moved from one position to another within the same document — does the link follow the content to its new location?
7. [nelson] When a new version of a document is created, do links that pointed to the original version automatically apply to the new version, or do they remain attached only to the version they were created against?
8. [nelson] What must the system guarantee about link creation — can a user create a link to any published content, or only to content they own?
9. [nelson] If one endset of a link references content that spans multiple documents through transclusion, does the link point to the original source content or to the transcluded appearance?
10. [nelson] Must the system guarantee that a user can discover ALL links whose endsets touch a given span of content, or is it acceptable for some links to be invisible to certain users?
11. [gregory] When FOLLOWLINK resolves a link's source endset to V-addresses via `span2spanset`, and only half the endset's I-address range is currently referenced by any POOM, does it return the reachable half as a partial VSpec or does it discard the entire endset?
12. [gregory] If INSERT splits a contiguous I-address range that a link's target endset references — say endset covers I:[.0.1.3,.0.1.7] and INSERT at V:1.5 pushes .0.1.5-.0.1.7 to non-contiguous V-positions — does RETRIEVEENDSETS return one VSpec or two VSpecs for that endset?
13. [gregory] When a link's source endset content exists in three documents simultaneously (original + two transclusions sharing the same I-addresses), does FOLLOWLINK return V-addresses from all three documents, or only from the document used in the find_links query?
14. [gregory] Are the three endsets (source, target, type) resolved independently during FOLLOWLINK — can the source endset resolve successfully while the target endset returns empty because its content was deleted from all POOMs?
15. [gregory] When REARRANGE fragments a link's endset across non-contiguous V-positions within the same document, does subsequent find_links using a VSpec covering only ONE of the fragments still discover the link, or must the query span overlap ALL fragments?
16. [gregory] After DELETE removes content that a link's type endset references, making the type endset unresolvable to any V-address, does the link still appear in find_links results when querying by source or target content that IS still referenced?
17. [gregory] When `insertendsetsinspanf` indexes a link's endsets in the spanfilade, does it create one spanfilade entry per endset or one entry per I-span within each endset — i.e., if the source endset contains two non-contiguous I-ranges, how many spanfilade entries result?
18. [gregory] If a document is versioned via CREATENEWVERSION and then a link is created on the original with source content shared by both documents, does find_links from the VERSION discover this after-the-fact link through the shared I-addresses?
19. [gregory] When `link2sporglset` extracts I-addresses from a link orgl's three endsets, does it preserve the endset boundary (source vs target vs type) in the sporgl structures, or are all three endsets flattened into a single sporgl set for spanfilade search?
20. [gregory] Does the system guarantee that a link created with a multi-span source endset (e.g., two disjoint VSpecs from different parts of the same document) stores those spans in endset-order in the link orgl, and does RETRIEVEENDSETS return them in that same order?
