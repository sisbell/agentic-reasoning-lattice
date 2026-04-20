# Sub-Questions — Transclusion (COPY)

**Inquiry:** What must content sharing through transclusion guarantee? How does transclusion differ from duplication? What properties of the original are preserved in the copy?

1. [nelson] When content from one document appears in another through transclusion, must the system guarantee that both occurrences share the same identity rather than being independent copies?
2. [nelson] If a reader encounters transcluded content in a document, must the system always be able to reveal the original document and position from which that content originated?
3. [nelson] Can an author who transcludes content from another document ever modify the transcluded portion independently, or must it remain identical to the original?
4. [nelson] When content is transcluded, do links that point to that content in its original document also apply when the same content appears in the transcluding document?
5. [nelson] Must the original author of content always be discoverable when that content appears through transclusion in someone else's document?
6. [nelson] If the system supports compensation for content use, must transclusion trigger a payment or royalty obligation to the original creator that mere duplication would not?
7. [nelson] When a new version of the original document is created, must transcluded content in other documents reflect the original version that was shared, or track the latest version?
8. [nelson] Is there a limit to how many times content can be transitively transcluded — that is, can a document transclude content that is itself a transclusion from a third document?
9. [nelson] Must the system guarantee that deleting a transclusion reference from a document leaves the original content completely unaffected in its source document?
10. [nelson] Can an author prevent their content from being transcluded by others, or does the design guarantee that all published content is available for transclusion by anyone?
11. [gregory] When COPY transfers a V-span from document A to document B, does docopy reuse the exact same I-addresses from A's POOM in B's new POOM entries, or does it allocate fresh I-addresses and duplicate the granfilade content?
12. [gregory] If document A contains "Hello" (I-addresses .0.1.1-.0.1.5) and document B transcludes that span via COPY, does find_links on document B discover links whose endsets reference I-addresses .0.1.1-.0.1.5 that were originally created against document A?
13. [gregory] After COPY creates a transclusion in document B, does INSERT into document A (shifting A's V-positions) alter any POOM entries in document B, or does B's POOM remain completely unchanged?
14. [gregory] When document B holds a transclusion of document A's content and that content is DELETEd from A's POOM, do B's POOM entries and the underlying granfilade content remain intact and retrievable?
15. [gregory] Does COPY create DOCISPAN entries in the spanfilade for the target document, making the target independently discoverable via FINDDOCSCONTAINING even if the source document is later emptied?
16. [gregory] When COPY transfers a V-span that maps to non-contiguous I-addresses (e.g., after an INSERT split the original span), does vspanset2sporglset automatically split the specset into multiple sporgls, each preserving the correct I-address mapping in the target?
17. [gregory] Does SHOWRELATIONOF2VERSIONS detect content overlap between a document and its transclusion target — that is, does compare_versions identify shared I-address spans between two documents that share content solely through COPY rather than through CREATENEWVERSION?
18. [gregory] If document B transcludes content from A, and document C then transcludes the same V-span from B, does C's POOM contain the same I-addresses as A's original content — making links created against A discoverable from C through the transitive chain?
19. [gregory] When COPY places content at a V-position in the target where adjacent POOM entries happen to have contiguous I-addresses with the copied content, does isanextensionnd merge the copy into the existing crum rather than creating a separate entry, and does this merging affect any observable query behavior?
20. [gregory] Does COPY transfer any link subspace (0.2.x) entries from the source document's POOM to the target, or does it only copy the V-spans explicitly specified in the source specset — meaning a COPY of a full document's text carries no links into the target?
