## Question 18 [gregory]

> For content stored via APPEND (which skips `insertspanf`), the I-address is permanent in the granfilade but has no DOCISPAN entry — can `find_links` ever discover a link whose endset references APPEND-created I-addresses, given that the spanfilade search is the only discovery path?

## KB Synthesis

Yes — **`find_links` can discover a link whose endset references APPEND-created I-addresses**. The DOCISPAN omission by APPEND is irrelevant to link discovery. Here's why.

## The Two Spanfilade Sub-Indices Are Independent

The KB makes a critical distinction [FC-CONTENT-SPANF-ISOLATION]:

> The spec must model spanf as having two independent sub-indices: `SpanEnfilade = { link_index: Map<IAddress, Set<LinkISA>>, docispan: Map<IAddress, Set<DocISA>> }`

APPEND skips `insertspanf(..., DOCISPAN)` [EC-APPEND-NO-DOCISPAN]. This makes content invisible to `find_documents`. But `find_links` searches the **link endset index**, not DOCISPAN. These are orthogonal.

## Link Creation Populates the Link Endset Index

When a link is created over content — regardless of whether that content arrived via INSERT or APPEND — `docreatelink` calls `insertendsetsinspanf()` [ST-CREATE-LINK]:

> Link creation is a compound state transition that updates both enfilades atomically: (1) create a link orgl in `granf`; (2) copy the link's ISA reference into the document's link subspace; (3) **index all link endpoints in `spanf` via `insertendsetsinspanf()`**.

The endpoint I-addresses are indexed in the link endset sub-index at link creation time. How those I-addresses were originally allocated (INSERT vs APPEND) is irrelevant — they're now in the spanfilade link index.

## The `find_links` Search Path Bypasses DOCISPAN

`find_links` converts the query V-span to I-addresses via the POOM, then searches the spanfilade **link endset** [SS-FIND-LINKS, INT-SPORGL-LINK-INDEX]:

> `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`

The V→I conversion uses the document's POOM (granfilade), not the DOCISPAN index. As long as the APPEND content has a live POOM mapping (it does — APPEND does write to `insertpm`) and the link endset was indexed at creation time, the search succeeds.

## The Gap

The only scenario where this fails is if the APPEND content's I-addresses are somehow not in the POOM of the queried document — but APPEND does update the POOM (`appendpm`). The content is addressable at its V-positions; `find_links` can convert those V-positions to I-addresses and match against the link endset.

**In summary:** APPEND's omission of DOCISPAN breaks `find_documents` for that content, but `find_links` operates entirely through the link endset sub-index. A link created over APPEND content has its endpoint I-addresses in the link endset, and searching those V-spans finds the link normally.

---

## Code Exploration

## Answer

**No. `find_links` cannot discover a link whose endset references APPEND-created I-addresses.** The spanfilade is the sole discovery path, and APPEND never registers its I-addresses there.

---

### How `find_links` searches

The FEBE `find` command dispatches to `findlinksfromtothree()` [`fns.c:189`], which calls `dofindlinksfromtothree()` [`do1.c:348`]:

```c
return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, threevspecset, orglrangeptr, linksetptr);
```

That function [`spanf1.c:56`] converts each vspec to a sporgl-set, then calls `sporglset2linkset()` for each of the three endset roles (FROM, TO, THREE).

Inside `sporglset2linksetinrange()` [`sporgl.c:245`], every candidate span is looked up by calling:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
```

The `range` is built with `prefixtumbler(&orglrange->stream, spantype, &range.stream)` where `spantype` is one of `LINKFROMSPAN=1`, `LINKTOSPAN=2`, or `LINKTHREESPAN=3` [`xanadu.h:35-38`]. The search is entirely inside `spanf` — the spanfilade. No other data structure is consulted.

---

### What DOCISPAN is and who creates it

There are four span types [`xanadu.h:35-39`]:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

`DOCISPAN` entries map I-addresses back to the document they live in. They are created by `docopy()` [`do1.c:62`]:

```c
&& insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

This is called from the normal `doinsert()` path [`do1.c:87-123`].

---

### How APPEND bypasses this

`doappend()` [`do1.c:25-32`]:

```c
bool doappend(typetask *taskptr, typeisa *docptr, typetextset textset)
{
    bool appendpm(),insertspanf(); /*zzz dies this put in granf?*/

    return (appendpm(taskptr, docptr, textset)/*&&
       appendpm includes insertspanf!   insertspanf(taskptr,spanf,docptr,textset,DOCISPAN)*/
    );
}
```

The `insertspanf(…, DOCISPAN)` call is **commented out**. The comment `/*zzz dies this put in granf?*/` signals this was a known open question when the code was written. `appendpm()` [`orglinks.c:17`] finds the end-of-document address via `findvsatoappend()`, then calls `doinsert()` — but `doinsert()` here goes through `inserttextingranf()` to allocate content in the granfilade. The DOCISPAN registration step never executes.

---

### Why this breaks link discovery

For `find_links` to return a link, the V-addresses in the query must:
1. Be converted to sporgl-set entries (I-spans in the spanfilade under LINKFROMSPAN/TO/THREE)
2. Match link endpoint entries in the spanfilade

APPEND-created content gets an I-address in the granfilade via `inserttextingranf()`, but since `insertspanf(…, DOCISPAN)` is skipped, no DOCISPAN entry maps that I-address back to any V-address. And since `docreatelink()` stores link endpoints as LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN entries in the spanfilade (via the normal `insertspanf` call), if a link *endpoint* were ever created that referenced an APPEND I-address, the lookup would proceed into the spanfilade — but the spanfilade has no record connecting that V-span to the APPEND I-address.

There is no secondary index, no fallback to the granfilade, and no content-walk in the `find_links` path. `sporglset2linksetinrange()` calls only `retrieverestricted()` on `spanf`, and `retrieverestricted()` does a pure enfilade traversal of that one structure.

---

### Conclusion

APPEND-created I-addresses are **dead ends** from the link-discovery perspective:

- They exist in the granfilade (document content), allocated by `inserttextingranf()`.
- They have no DOCISPAN entry in the spanfilade (the `insertspanf` call in `doappend()` is commented out, `do1.c:29-31`).
- If a link were created whose endset happened to reference one of these I-addresses, `find_links` would still fail to return it — because link discovery searches the spanfilade's LINK*SPAN entries, not the granfilade, and can only resolve V→I mappings that were registered via `insertspanf`.
- The spanfilade is the exclusive discovery path [`sporgl.c:259,261`], and APPEND never populates it.
