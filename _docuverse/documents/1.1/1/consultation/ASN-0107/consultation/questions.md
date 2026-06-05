# Sub-Questions — FINDNUMOFLINKSFROMTOTHREE Operation

**Inquiry:** What happens when the system is asked how many links match a from/to/type description? What is being counted, what does the count assert about the link store, what does the count not say that the caller might expect, and what invariants govern how the count changes as content is added or links are retracted?

1. [theory] When the system reports how many links match a from/to/type description, what is the unit being counted — distinct links, distinct endpoints, or distinct documents touched?
2. [theory] Does the count assert that exactly that many links currently exist with that description, or only that at least that many were once created?
3. [theory] What must the count guarantee about links whose endpoints reference content that has since been superseded by a newer version?
4. [theory] If two links share identical from, to, and type descriptions but were authored separately, must the count treat them as one or as two?
5. [theory] What does the count deliberately not tell the caller about the identity or permanence of the individual links it summarizes?
6. [theory] When new content is added to a document that links already point into, must the count for an unchanged description remain stable?
7. [theory] When a link is retracted, what invariant governs how much the count may decrease, and may it ever decrease by more than one per retraction?
8. [theory] Must a count taken at one moment and the same count taken later differ only by the net of links added and links retracted in between?
9. [theory] Does a description that matches zero links assert that no such link has ever existed, or only that none exists now?
10. [theory] When a link's endpoint spans a portion of a document that is partially edited, must the link still be counted under its original from/to/type description?
11. [evidence] When FINDNUMOFLINKSFROMTOTHREE counts matching links, is it counting distinct link orgls or counting spanfilade DOCISPAN entries, and can a single link with a multi-span endset be counted more than once?
12. [evidence] Is the count computed by fully materializing the matching link set into a transient list and then taking its length, or is there an incremental counter that avoids building the list?
13. [evidence] Since `sporglset2linkset` hardcodes the orgl range via the `TRUE||!homeset` override, does the count reflect a global I-address intersection rather than a count scoped to the supplied home document range?
14. [evidence] Because the spanfilade is write-only with no `deletespanf`, does the count include links whose endpoint content has been deleted from all POOMs — i.e., are ghost/orphaned links counted?
15. [evidence] Are the DEL5 unreferenced I-addresses (silently filtered during I→V conversion in retrieval) filtered before counting, or does the count include links that would resolve to empty endsets?
16. [evidence] After a DELETE removes a link endpoint's V→I mapping from a document's POOM while leaving spanfilade entries intact, does the reported count stay the same or decrease?
17. [evidence] Is the count monotonically non-decreasing across the lifetime of the store given that links are never retracted (INV-LINK-PERMANENCE) and the spanfilade only grows (FC-SPANFILADE-MONOTONIC)?
18. [evidence] When content is transcluded via COPY into a new document, does the count for a from/to/type query against that new document's V-span increase because the shared I-addresses now overlap additional spanfilade endset entries?
19. [evidence] For a zero-width or empty from/to/type specset, does the count return 0 cleanly, and does a specset whose I-spans match no spanfilade entry also return 0 without error?
