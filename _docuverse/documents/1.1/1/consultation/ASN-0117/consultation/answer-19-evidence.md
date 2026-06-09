## Question 19 [evidence]

> If DELETE removes the last content referencing a link's endset I-addresses from this document's POOM, does the link orgl persist in granfilade and spanfilade, becoming undiscoverable via `find_links` from this document but re-discoverable if the content reappears via transclusion?

## KB Synthesis

Yes, exactly — with one important nuance about the spanfilade.

**Link orgl persists in granfilade and spanfilade**

The three-layer model [SS-THREE-LAYER-MODEL] is definitive here. DELETE operates exclusively on the POOM layer via `deletend`. The link orgl at its I-address in granfilade is untouched — I-addresses are permanent [INV-LINK-PERMANENCE, INV-IADDR-IMMUTABILITY]. The spanfilade is append-only with no delete operation [INV-SPANF-WRITE-ONLY], so the DOCISPAN entries linking those I-addresses to this document also persist [INT-DELETE-SPANF-DIVERGENCE].

**Discoverability after DELETE**

`find_links` works by converting a query V-span to I-addresses via the POOM, then intersecting against the spanfilade [SS-FIND-LINKS]. Once the endpoint content is removed from the document's POOM, that V-span resolves to no matching I-addresses — the link becomes undiscoverable from *this document* via content-based search [ST-DELETE, Finding 0029]. However, `follow_link` on the link ID still works, since it reads the link orgl directly without consulting the POOM [EC-GHOST-LINK, INV-LINK-PERMANENCE].

One subtlety: the stale spanfilade entry means `find_documents` *still* reports this document as containing those I-addresses [EC-STALE-SPANF-REFERENCE]. Callers must post-filter via I→V conversion to distinguish live from stale results [INV-ITOV-FILTERING].

**Re-discoverability via transclusion**

Yes — but only via VCOPY (not INSERT). VCOPY shares the original I-addresses [ST-VCOPY], so if any document still holds those I-addresses and is VCOPYed back, the link becomes discoverable again through the shared identity [INT-LINK-TRANSCLUSION, INV-TRANSITIVE-IDENTITY]. INSERT would allocate fresh I-addresses [ST-INSERT, INV-NO-IADDR-REUSE] — the resulting text looks identical but has no identity relationship with the link's endset, so the link would not be found.

---

## Code Exploration

I now have everything needed to answer precisely. Here is the full analysis:

---

## Answer: Link Orgl Persistence After DELETE

### Short answer

**Yes on all three counts.** The link orgl survives in both granfilade and spanfilade; `find_links` loses the link because the V→I translation via POOM returns nothing for deleted content; and the link becomes rediscoverable when the same I-addresses return via transclusion, because the spanfilade index is keyed on I-addresses, not V-addresses.

---

### 1. What DELETE actually touches

`dodeletevspan` [`do1.c:158-167`] does exactly two things:

```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)   // do1.c:164
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)        // do1.c:165
);
```

`deletevspanpm` [`orglinks.c:145-152`]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);  // orglinks.c:149
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` operates on `docorgl` — the **document's POOM enfilade** — in the `V` (virtual address) dimension only. It removes V-address entries from that enfilade.

**Neither the granfilade registration of any link orgl nor the spanfilade is touched.** `dodeletevspan` has no call path that reaches `insertspanf`, no call path that reaches `createorglingranf`, and no call path that modifies anything other than the document's POOM.

---

### 2. How link creation stores endpoints — keyed by I-address

`docreatelink` [`do1.c:195-221`] does two relevant things with the endsets:

```c
&& specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)  // do1.c:214
&& specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)  // do1.c:215
...
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)  // do1.c:219
```

`specset2sporglset` [`sporgl.c:14-33`] → `vspanset2sporglset` [`sporgl.c:35-65`] walks each vspan in the endset, calls `vspanset2ispanset` → `permute` [`orglinks.c:397-416`] to translate V→I, and packs the result into a sporgl with:

```c
movetumbler (docisa, &sporglset->sporgladdress);     // sporgl.c:53
movetumbler(&ispanset->stream, &sporglset->sporglorigin);  // sporgl.c:54
movetumbler (&ispanset->width, &sporglset->sporglwidth);   // sporgl.c:55
```

`insertspanf` [`spanf1.c:15-54`] then stores each sporgl into the spanfilade with:

```c
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);  // spanf1.c:49 — I-address stream
movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);   // spanf1.c:50 — I-address width
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);  // spanf1.c:51
```

The SPANRANGE key is the **I-address** (content address), not the V-address. The ORGLRANGE key is the link ISA prefixed by the endset role (`LINKFROMSPAN` / `LINKTOSPAN` / `LINKTHREESPAN`).

---

### 3. How `find_links` queries — and why deletion breaks it

`dofindlinksfromtothree` [`do1.c:348-353`] delegates directly to `findlinksfromtothreesp` [`spanf1.c:56-103`].

That function converts the caller's query vspecset → sporglset via the same V→I chain:

```c
if (fromvspecset)
    specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);  // spanf1.c:71
...
sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);  // spanf1.c:77
```

`specset2sporglset` → `vspanset2sporglset` [`sporgl.c:35-65`] does:

```c
if (!findorgl (taskptr, granf, docisa, &orgl, type))   // sporgl.c:44
    return (NULL);
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);  // sporgl.c:48
    for (; ispanset; ispanset = ispanset->next) { ... }
}
```

`vspanset2ispanset` [`orglinks.c:397-401`] → `permute` walks the POOM enfilade of the document orgl, finding what I-address range corresponds to the queried V-address range.

**If the content at those V-addresses has been deleted from the POOM (via `deletend` in orglinks.c:149), the permute/span2spanset traversal finds no mapping.** The POOM simply no longer has an entry covering that V-range. The sporglset comes back empty. `sporglset2linkset` queries nothing. `findlinksfromtothreesp` returns `*linksetptr = NULL` at `spanf1.c:79-82`.

The link orgl in granfilade is still there. The spanfilade entries are still there. The link is **undiscoverable from this document** because the V→I bridge through the document's POOM has been severed.

---

### 4. Re-discoverability via transclusion

When content is transcluded back, `docopy` [`do1.c:212`] (used in `doinsert`) inserts new POOM entries mapping fresh V-addresses to the same source I-addresses. The POOM enfilade gains a `V→I` mapping for those I-addresses again.

When `find_links` is then called with a vspec covering the transcluded region:

- `vspanset2sporglset` → `vspanset2ispanset` → `permute` succeeds: the POOM now resolves those V-addresses to the original I-addresses
- The sporgl contains those I-addresses as `sporglorigin`/`sporglwidth`
- `sporglset2linkset` queries the spanfilade in SPANRANGE with those I-addresses
- The **pre-existing spanfilade entries** — written at link creation time, never touched by DELETE — are found
- The link IS returned

---

### Conclusion

| Claim | Verdict | Key evidence |
|---|---|---|
| Link orgl persists in granfilade after DELETE | **Yes** | `deletevspanpm` only calls `deletend` on document POOM [`orglinks.c:149`]; granfilade is untouched |
| Spanfilade entries persist after DELETE | **Yes** | No code path in `dodeletevspan` reaches `insertspanf` or modifies spanfilade |
| Spanfilade keyed by I-address, not V-address | **Yes** | `crumorigin.dsas[SPANRANGE]` = sporgl I-address [`spanf1.c:49`] |
| find_links fails after deletion | **Yes** | V→I via `permute` returns empty for deleted V-range; sporglset empty; linkset NULL [`spanf1.c:79`] |
| Link rediscovered after transclusion of same I-addresses | **Yes** | `docopy` rebuilds V→I POOM mapping; spanfilade query succeeds on unchanged entries |

The architecture is deliberate: by indexing links on I-addresses (permanent content identity) rather than V-addresses (document-relative position), the spanfilade acts as a persistent, document-independent record of links. The POOM is the only bridge between V-space and I-space, so deleting content severs discoverability from this document — but the link itself is preserved and ready to reappear the moment any document's POOM maps to those I-addresses again, whether via transclusion of the original content or reuse of the same ISA.
