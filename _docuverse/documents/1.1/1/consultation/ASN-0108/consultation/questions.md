# Sub-Questions — FINDNEXTNLINKSFROMTOTHREE Operation

**Inquiry:** What happens when matching links are read a window at a time? What determines the order in which they arrive, what invariants does the enumeration order satisfy across the system's evolution between calls, what determines when the reader has seen them all, and how does the reader know how far along they are?

1. [theory] When matching links are delivered to a reader in successive windows rather than all at once, what must the system guarantee about the order in which those links arrive?
2. [theory] Must the enumeration order over a set of matching links be a property the reader can rely on as total and unambiguous, so that no two links could ever occupy the same position?
3. [theory] If content, documents, or links are created or changed between one window request and the next, what must remain stable about the order of links the reader has already seen?
4. [theory] When new links come into existence partway through a windowed reading, where in the ordering must they appear relative to links the reader has already received?
5. [theory] How must the reader know that the final window has been reached and that every matching link has now been seen?
6. [theory] What must the design guarantee so that a reader paging through windows never receives the same link twice and never silently skips one?
7. [theory] By what shared, durable identity does a reader mark its place between window requests, so that resuming continues exactly where it left off?
8. [theory] How must the system let a reader know how far through the full set of matching links it has progressed at any point during windowed reading?
9. [theory] If links are removed between window requests, what must the design guarantee about the positions and completeness of the windows still owed to the reader?
10. [theory] Must the boundaries between successive windows be a private convenience for the reader, or a stable property of the system that any reader would observe identically?
11. [evidence] When FINDNEXTNLINKSFROMTOTHREE returns a window of links, what determines the order of links within that window — spanfilade I-address span ordering, link orgl I-address, or the insertion-sort by V-address in `incontextlistnd`?
12. [evidence] Does the cursor for windowed retrieval encode an absolute position into the materialized link list, or does it encode an I-address/tumbler boundary into the spanfilade search itself?
13. [evidence] Since `findlinksfromtothreesp` performs full materialization into a transient list before truncating, is the complete result list rebuilt from the spanfilade on every windowed call, or is any state retained across calls?
14. [evidence] If a new link is created (CREATELINK) between two windowed reads, does the new link appear in a later window, and does its insertion disturb the cursor position of links already enumerated?
15. [evidence] Given FC-SPANFILADE-MONOTONIC, can a link enumerated in an earlier window ever disappear from a later window — for instance if its endpoint content is deleted from all POOMs between calls?
16. [evidence] Does the windowed enumeration order remain stable across calls regardless of spanfilade tree height growth, consistent with INV-ENFILADE-CONFLUENCE, or can tree restructuring between calls permute the order?
17. [evidence] How does the reader detect exhaustion — does a final window return fewer than N links, an explicit terminal marker, or an empty window on the call after the last full one?
18. [evidence] Does the cursor returned to the reader expose absolute progress (e.g., index k of total), or only enough state to request the next window without revealing how many links remain?
19. [evidence] When the EC-FIND-LINKS-GLOBAL behavior (`TRUE||!homeset` override with hardcoded width 100) is in effect, does the ignored orgl-range parameter affect the windowed enumeration order or only the global membership of the result set?
20. [evidence] For "ghost links" whose endset I-addresses are silently filtered during I→V conversion, are they counted as occupying a window slot before filtering, or does filtering happen before windowing so the reader sees N valid links per window?
