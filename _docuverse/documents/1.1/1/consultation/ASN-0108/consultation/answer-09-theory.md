## Question 9 [theory]

> If links are removed between window requests, what must the design guarantee about the positions and completeness of the windows still owed to the reader?

## The guarantee: stable positions and clean completeness under concurrent deletion

The scenario is paginated retrieval — a reader pulls links/windows in successive batches (`FINDNEXTNLINKSFROMTOTHREE`, 4/69), and between two requests some links are deleted. Two design properties must hold so the remaining windows are delivered correctly.

### 1. Positions must be stable — deletion never renumbers survivors

Links are addressed by **permanent order of arrival**, and that address is fixed for the life of the link. Removing one link does not shift the addresses of the others.

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

From the curated `links` source:
> "Deleting link `2.5` doesn't renumber `2.6` through `2.N`."

This is what makes paginated retrieval safe. A continuation request is anchored to a specific link and returns "no more than `<nlinks>` items past that link on that list" (`FINDNEXTNLINKSFROMTOTHREE`). Because the anchor's address and every survivor's address are unchanged by the deletion, the cursor stays valid: no survivor is skipped, none is re-delivered, and the order the reader sees across batches stays consistent.

### 2. Completeness — removed links drop out cleanly without impeding the rest

The removed links simply cease to satisfy the request; their absence must not block or delay delivery of the windows still owed.

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

A deleted link enters a "not currently addressable" state, while everything else remains fully addressable:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

So the reader is still owed **every surviving window, in its original creation-order position**, with the deleted ones merely absent — not leaving gaps that misalign the remaining results, and not causing the renumbering that would otherwise drop or duplicate a survivor.

### Summary

If links are removed between window requests, the design must guarantee that (a) surviving windows keep their permanent order-of-arrival positions — deletion renumbers nothing, so a continuation cursor remains valid — and (b) the removed links fall out without impeding delivery of the rest, so the reader still receives the complete set of remaining windows, correctly ordered and aligned.

---

**Verification note:** The quotes above (4/31, 4/60, 4/9) and the no-renumbering property are verified in the curated sources. Nelson does not, in the curated material, state the *specific* case of concurrent deletion during paginated `FINDNEXTNLINKSFROMTOTHREE` retrieval — that application is my synthesis from the permanent-order-of-arrival and search-satisfaction invariants. If you want Nelson's exact treatment of the pagination operation's behavior under change, flag: NEED_RAW: 4/58-4/60, 4/69.
