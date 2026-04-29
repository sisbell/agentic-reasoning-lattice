# Sub-Questions — I-Space and V-Space

**Inquiry:** What is the relationship between permanent content storage (I-space) and mutable document arrangement (V-space)? What invariants connect them?

1. [nelson] Once content is permanently stored, can any document operation — rearrangement, deletion from a document, or versioning — ever alter or destroy that stored content?
2. [nelson] When a document arranges content in a particular order, does the document hold its own copy of that content, or does it refer to the single permanent instance?
3. [nelson] If two documents include the same passage, must the system guarantee that both arrangements point to identical underlying content, making the shared origin visible?
4. [nelson] When a user rearranges content within a document, what must remain invariant about the content's permanent identity — its bytes, its origin, its order of arrival?
5. [nelson] Can a document's arrangement ever reference content that does not exist in permanent storage, or must every position in a document correspond to something already stored?
6. [nelson] If content is added to permanent storage but no document currently arranges it, does that content still exist and remain retrievable?
7. [nelson] When a new version of a document rearranges its content differently, must the system preserve the previous arrangement as well, or only the underlying content?
8. [nelson] Must the mapping from a document's arrangement back to the permanent content be exact — byte-for-byte correspondence — or can a document transform or excerpt content in ways that break that correspondence?
9. [nelson] If a user inserts new content into a document, must that content first be committed to permanent storage before the document can arrange it, or can the two happen simultaneously?
10. [nelson] When content is permanently stored, does it receive a fixed identity at that moment, and must every document arrangement that uses that content refer to it by that same identity forever?
11. [gregory] When a POOM entry is split by INSERT (e.g., inserting into the middle of "ABCDE"), does the split produce two new bottom crums whose I-displacements and I-widths exactly partition the original I-span with no gaps or overlaps?
12. [gregory] After DELETE removes a V-span that covers only part of a POOM bottom crum, does `slicecbcpm` preserve the exact I-displacement of the surviving portion, or does it recompute it from the V-side cut point?
13. [gregory] When `vspanset2sporglset` walks the POOM to convert a V-span to I-spans, and the V-span crosses a boundary between two POOM entries with non-contiguous I-addresses, does it always produce exactly one sporgl per contiguous I-run — never merging across I-gaps or splitting within a contiguous I-run?
14. [gregory] Is there any operation that can change which I-address a given V-position maps to WITHOUT removing and re-inserting the POOM entry — for instance, does REARRANGE modify I-displacements in-place, or does it only adjust V-displacements while leaving I-fields untouched?
15. [gregory] When `isanextensionnd` coalesces a new insertion into an existing POOM bottom crum (the ONMYRIGHTBORDER case), does it verify that the new I-address is exactly `existing_I_end + 1`, or could it coalesce I-addresses that are close but not strictly adjacent?
16. [gregory] In the POOM's 2D enfilade, the I-dimension index enables reverse lookup (given an I-address, find V-positions). When multiple V-positions map to the same I-address (self-transclusion), does `incontextlistnd` return ALL matching V-positions in a single traversal, or does it require multiple queries?
17. [gregory] After COPY creates shared I-address references between two documents, if the source document DELETEs that content, do the target document's POOM entries still resolve correctly through the granfilade — i.e., is there any reference-counting or liveness check that could invalidate the target's I→content mapping?
18. [gregory] When CREATENEWVERSION copies the text subspace POOM, does it create new bottom crums with identical I-displacement and I-width values (byte-for-byte copies), or does it go through `insertpm` which might split or coalesce entries differently?
19. [gregory] The spanfilade indexes I-spans per document via DOCISPAN entries. When a single POOM entry (one contiguous I-span) is split by INSERT into two entries, does the original DOCISPAN entry remain valid for link discovery, or must new DOCISPAN entries be created for the two halves?
20. [gregory] Is there a mechanism that detects or prevents a POOM from containing two entries whose I-address ranges overlap — for example, if COPY transcludes content that partially overlaps with content already present in the target document at different V-positions?
