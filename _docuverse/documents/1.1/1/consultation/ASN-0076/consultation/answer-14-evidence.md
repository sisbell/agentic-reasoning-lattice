## Question 14 [evidence]

> If a "new version" link were created with the same three endsets as an existing link, would `findlinksfromtothreesp` return both as discoverable, or does the spanfilade have any deduplication that would suppress the duplicate?

## KB Synthesis

Both links would be returned. The spanfilade has no deduplication mechanism.

**Why both are discoverable:**

1. **Each link gets a distinct I-address** [SS-ADDRESS-ALLOC, ST-ADDRESS-ALLOC]: MAKELINK always allocates the next available I-address via `findisatoinsertmolecule`. Even if two links have identical FROM/TO/THREE specsets, they are allocated distinct link ISAs — e.g., `docA.2.1` and `docA.2.2`.

2. **Both link ISAs are registered in the spanfilade** [ST-CREATE-LINK, SS-SPANF-OPERATIONS]: `docreatelink` calls `insertendsetsinspanf` for each link. The spanfilade is modeled as `Map<IAddress, Set<LinkISA>>` — both link ISAs are inserted under the same endpoint I-addresses. The second insertion does not replace the first.

3. **The spanfilade is append-only** [INV-SPANF-WRITE-ONLY]: There is no deduplication or merging in `insertspanf`. Every `insertnd` call adds an entry regardless of whether equivalent entries already exist.

4. **`findlinksfromtothreesp` returns the full matching set** [SS-FIND-LINKS]: The search returns all link ISAs whose endpoint I-addresses intersect the query. The `intersectlinksets()` operation [SS-FIND-LINKS Finding 0035] intersects across FROM/TO/THREE endpoint queries to require all three match — but it does not deduplicate among links that *all* satisfy those constraints.

**Consequence:** If you create two links with identical endsets pointing to the same content, both are permanently stored and both are returned by any `find_links` query. This is consistent with [INV-LINK-PERMANENCE] — links are append-only entities with no identity-merging semantics. The KB documents no uniqueness constraint on link endpoints in preconditions [PRE-LINK-CREATE].

---

## Code Exploration

I now have all the verified source. Here is the full answer with exact citations.

---

## Answer: Both Links Would Be Returned — No Content-Level Deduplication

### Short answer

If two links are created with identical endsets but at different moments (and thus different ISA tumblers), `findlinksfromtothreesp` **returns both**. The spanfilade has no deduplication at the content level. The only deduplication that exists is identity-level: it prevents the *same link's ISA address* from appearing twice in a single traversal result, which is a different concern.

---

### Insertion: No Duplicate Guard

`docreatelink` [do1.c:195–221] allocates a fresh ISA tumbler via `createorglingranf` on every call, then stores the link's endsets into the spanfilade:

```
docreatelink [do1.c:195]
  → insertendsetsinspanf [do2.c:116]
    → insertspanf [spanf1.c:15] (called 3×: LINKFROMSPAN, LINKTOSPAN, LINKTHREESPAN)
      → insertnd [spanf1.c:51]
```

`insertspanf` [spanf1.c:51] calls `insertnd` directly with no check against existing entries:

```c
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

There is nothing in `insertspanf` or `insertendsetsinspanf` [do2.c:116–128] that inspects whether an identical span-set is already indexed. Two links with identical endsets get two independent index entries — one per `linkisaptr` address.

---

### Retrieval: Identity Deduplication Only

`findlinksfromtothreesp` [spanf1.c:56–103] takes this path:

```
findlinksfromtothreesp [spanf1.c:56]
  → specset2sporglset (for each of from/to/three) [spanf1.c:71–75]
  → sporglset2linkset [sporgl.c:222]
    → sporglset2linksetinrange [sporgl.c:239]
      → retrieverestricted (spanfilade tree traversal) [sporgl.c:259/261]
      → onlinklist [spanf2.c:26] (for each found context)
  → intersectlinksets [spanf2.c:46]
```

`sporglset2linksetinrange` extracts a link's ISA address from each traversal context, then calls `onlinklist` [sporgl.c:264–265]:

```c
beheadtumbler(&c->totaloffset.dsas[ORGLRANGE],&linksa);
onlinklist (taskptr, linksetptr, &linksa);
```

`onlinklist` [spanf2.c:26–44] deduplicates by *ISA address*:

```c
for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
    if (tumblereq (&temp->address, linkisaptr))
        return(0);   // drop only if same ISA address already on list
}
temp->next = linkset;
```

`tumblereq` compares the **link's own ISA tumbler**, not its endset content. Two distinct links produced by two separate `docreatelink` calls have different ISA addresses by construction. `onlinklist` will add both to the accumulation list and return 0 for neither.

`intersectlinksets` [spanf2.c:46–120] then takes the intersection of the from/to/three link lists. Both links appear in all three per-endset lists (since their endsets are the same address ranges), so both survive the intersection and appear in the final result.

---

### What `onlinklist` Actually Guards Against

The deduplication in `onlinklist` exists because a single link's ISA address can appear in *multiple spanning nodes* of the enfilade during tree traversal — the same link might be encountered more than once while walking the tree for a given query range. `onlinklist` collapses those redundant traversal hits back to one. It is not a semantic "have I seen this content before" check.

---

### Conclusion

The spanfilade is a **positional index by span**, not a content-addressed store. It records *where* each link's endsets fall in address space, then looks up which links touch a given range. Nothing in the insertion path (`insertspanf`) checks whether another link already covers the same spans. Nothing in the retrieval path (`onlinklist`) compares endset content between distinct links.

Two links with identical endsets are two distinct objects with distinct ISA tumblers. `findlinksfromtothreesp` would return **both** of them.
