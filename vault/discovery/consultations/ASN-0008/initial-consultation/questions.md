# Sub-Questions — Link Discovery

**Inquiry:** What guarantees must link discovery provide? If content A links to content B, under what conditions can B discover the link? What about transcluded content?

1. [nelson] If I create a link from my document to yours, must the system guarantee that you can discover that link exists?
2. [nelson] Does the right to discover incoming links belong to the content owner, the content itself, or anyone who can read the content?
3. [nelson] If content is transcluded from document A into document B, and someone links to that content in document B, must document A also be able to discover that link?
4. [nelson] Can a link creator restrict the target from knowing the link exists, or must all links be discoverable by both endpoints?
5. [nelson] When content has been linked to, must the system preserve the ability to discover that link permanently, or can link discovery expire?
6. [nelson] If a document has a thousand incoming links, must the system guarantee it can find all of them, or only those from published documents?
7. [nelson] Does publication change what link discovery guarantees apply — can unpublished links to published content remain hidden?
8. [nelson] If I transclude your content into my document and then someone links to that passage, who has the right to discover the link — you, me, or both?
9. [nelson] Must the system guarantee that link discovery is complete — that every link to a piece of content is findable — or only that discovered links are genuine?
10. [nelson] When the same content appears in multiple documents through sharing, must a link targeting one appearance be discoverable from all appearances, or only the one explicitly targeted?
11. [gregory] When `findlinksfromtothreesp` searches the spanfilade for links overlapping a given I-address range, does it require the query I-span to overlap the link's source endset, target endset, or type endset — or does overlap with ANY of the three endsets produce a match?
12. [gregory] The "three" in `FINDNEXTNLINKSFROMTOTHREE` takes three specset arguments — does each argument constrain a specific endset (source, target, type), and can any of the three be left empty to mean "unconstrained on this endset"?
13. [gregory] When a link's source endset spans I-addresses `[.0.1.3, .0.1.7]` and only bytes `.0.1.5` through `.0.1.7` remain in any POOM after partial deletion, does `find_links` still discover the link through the surviving partial overlap, or does it require full endset coverage?
14. [gregory] When FOLLOWLINK resolves a discovered link's endsets back to V-addresses via `span2spanset`, and some endset I-addresses are unreferenced (not in any current POOM), does it return the surviving subset of V-addresses, or does it return nothing if any portion is missing?
15. [gregory] If document A creates a link with source=A's content and target=B's content, and then document C transcludes B's content via COPY, does `find_links` called on document C with C's V-span for the transcluded content discover A's link through the target endset overlap?
16. [gregory] When two documents each INSERT the string "Hello" independently (producing different I-addresses), and a link is created on one document's "Hello", is the link completely invisible from the other document — confirming that discovery is purely I-address identity, never byte-value equality?
17. [gregory] After REARRANGE fragments a contiguous endset span into two non-contiguous V-regions within the same document, does `find_links` called with a V-span covering only ONE of those two regions still discover the link, or must the query span cover both fragments?
18. [gregory] When `sporglset2linkset` uses the hardcoded `TRUE||!homeset` override to search globally, does it search ALL link orgls across ALL documents in the system, or is the search still bounded by the I-address range of the query specset?
19. [gregory] If a link is created in document A, and then A's link subspace entry is deleted via DELETEVSPAN on `0.2.x` (reverse orphaning), can document B — which transcludes A's source content — still discover the link through `find_links`, since the spanfilade entry persists?
20. [gregory] When `find_links` returns multiple links matching the same I-address range, does the implementation guarantee any ordering among the results — by link creation order, by link I-address, or by document of origin — or is the order determined solely by spanfilade tree traversal?
