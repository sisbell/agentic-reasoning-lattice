## Question 15 [evidence]

> If a link's source endset is anchored entirely within region `[a,b)`, after that region moves does `find_links` still resolve it through unchanged I-address overlap, and do the reported endset V-addresses reflect the new post-move positions?

## KB Synthesis

**Yes to both sub-questions.**

**find_links still resolves**

REARRANGE is a pure V-address permutation — I-addresses are completely invariant [INV-REARRANGE-IDENTITY]. The link was indexed in the spanfilade against the endset's I-addresses when it was created. Since those I-addresses do not change, the I-address intersection that drives `find_links` is unaffected [SS-FIND-LINKS, ST-FIND-LINKS]. Link discovery is "a function of content identity, not position" [INV-LINK-CONTENT-TRACKING].

**Reported endset V-addresses reflect new positions**

Endsets are **dynamic** — they are not stored as V-spans but are recomputed at query time by converting the stored I-addresses back through the document's current POOM [SS-LINK-ENDPOINT Finding 0019, SS-FOLLOWLINK]. REARRANGE updates the POOM's V-address entries in place [SS-POOM-MUTABILITY, ST-REARRANGE]. So when FOLLOWLINK or RETRIEVEENDSETS runs afterward, `linksporglset2specset` traverses the updated POOM and returns the moved V-positions.

**Caveat for pivot cuts through the endset**

If the pivot/swap cuts *inside* the endset rather than moving it as a whole, fragmentation occurs and `find_links` may return duplicate results [EC-PIVOT-LINK-FRAGMENTATION]. But for your stated case — endset entirely within [a,b), region moved atomically — no fragmentation applies and the above holds cleanly.

---

## Code Exploration

I now have everything I need. Here is the complete answer with direct code citations.

---

## How `find_links` Resolves Link Endsets After a Region Move

### Architecture: Two Separate Address Spaces

The system maintains a strict separation between **V-addresses** (virtual, position-dependent) and **I-addresses** (intrinsic, identity-permanent). Conversion between them is mediated by the **POOM** (permutation matrix enfilade, `typeorgl`). This separation is the key to understanding the entire question.

---

### Step 1 — How Link Endsets Are Stored at Creation

When a link is created, `insertendsetsinspanf` is called [do2.c:116-128]:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
    typesporglset fromsporglset, typesporglset tosporglset, typesporglset threesporglset)
{
    insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
    && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)
```

Inside `insertspanf` [spanf1.c:15-54], the endset's **I-address** (from the sporgl item's `stream`/`width`) is placed into the **SPANRANGE** dimension of the spanfilade:

```c
// spanf1.c:27-29 — extract I-address from sporglset item
movetumbler (&((typeispan *)sporglset)->stream, &lstream);
movetumbler (&((typeispan *)sporglset)->width, &lwidth);

// spanf1.c:49-51 — store in SPANRANGE (I-address dimension)
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

The **ORGLRANGE** dimension receives the link's own ISA prefixed with `LINKFROMSPAN`/`LINKTOSPAN` [spanf1.c:22]:
```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

**The spanfilade is thus a 2D structure indexed by: (I-address of endset content) × (link identity tagged by endset role).** V-addresses are never stored here.

Additionally, `insertendsetsinorgl` [do2.c:130-149] stores the endsets inside the link document's POOM via `insertpm` [orglinks.c:105, 113]:

```c
movetumbler (&lstream, &crumorigin.dsas[I]);  // I-address copied unchanged
movetumbler (vsaptr,   &crumorigin.dsas[V]);   // V-address at creation time
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```

---

### Step 2 — What a Copy/Move Does to Addresses

`docopy` [do1.c:45-64] performs three steps:

```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)   // V→I conversion
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)      // write new V→I into POOM
&& insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)   // index content in spanfilade
```

Inside `insertpm` [orglinks.c:100-131], the I-address is **copied unchanged** while only the V-address is updated to the destination:

```c
// orglinks.c:105 — I-address is invariant
movetumbler (&lstream, &crumorigin.dsas[I]);
// orglinks.c:113 — V-address is set to the new destination
movetumbler (vsaptr,   &crumorigin.dsas[V]);
```

A move (cut+paste) additionally calls `rearrangepm` or `deletevspanpm` [orglinks.c:137-152] to remove the old V→I mapping from the POOM:

```c
bool deletevspanpm(...) {
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

After the move: the I-addresses `[x,y)` that used to be reached via V-address `[a,b)` are now reached via V-address `[c,d)`. The I-addresses themselves are unchanged.

**The spanfilade's SPANRANGE entries for the link endsets are entirely unaffected, because they were keyed on I-addresses from the start.**

---

### Step 3 — How `find_links` Resolves Post-Move

The call chain is: `findlinksfromtothree` [fns.c:189] → `dofindlinksfromtothree` [do1.c:348-352] → `findlinksfromtothreesp` [spanf1.c:56-103].

When called with a post-move V-spec (e.g., `[c,d)`), `findlinksfromtothreesp` first converts to I-addresses [spanf1.c:70-71]:

```c
if (fromvspecset)
    specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
```

`specset2sporglset` → `vspanset2ispanset` [orglinks.c:397-402] → `permute` walks the POOM and resolves the current V-address `[c,d)` to the same I-address range `[x,y)` that was there before the move.

Then `sporglset2linkset` queries the spanfilade [spanf1.c:77]:

```c
sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
```

This resolves to `retrievesporglsetinrange` [spanf1.c:237-267], which queries the spanfilade with the I-address `[x,y)` in SPANRANGE:

```c
// spanf1.c:245
context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE,
    whichspace, ORGLRANGE, (typeisa*)NULL);
```

Since the link's endset was stored under the same I-address `[x,y)` at creation time, this query **still matches**. The move changed V-addresses; it left I-addresses — and the spanfilade's index — completely undisturbed.

**Answer to part 1: YES. `find_links` resolves the link through unchanged I-address overlap in the SPANRANGE dimension of the spanfilade.**

---

### Step 4 — Do Reported Endset V-Addresses Reflect Post-Move Positions?

When `dofollowlink` [do1.c:223-232] returns endsets:

```c
link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
&& linksporglset2specset (taskptr, ..., sporglset, specsetptr, NOBERTREQUIRED)
```

`link2sporglset` retrieves the link's endset I-spans from the orgl. `linksporglset2specset` then calls `ispan2vspanset` [orglinks.c:389-393]:

```c
typevspanset *ispan2vspanset(...) {
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

`permute` [orglinks.c:404-422] → `span2spanset` [orglinks.c:425-454] → `retrieverestricted` on the link's POOM with the I-span as restriction, querying the V dimension → `context2span` [context.c:176-212].

In `context2span`, the output V-address is read from the accumulated `totaloffset` of the current POOM traversal:

```c
// context.c:206-207
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

`grasp` is filled by `prologuecontextnd` [context.c:217-221] which reads `totaloffset` — the offset accumulated as the retrieval walked the tree to find the crum containing those I-addresses. This reflects the **current state of the POOM**, which after the move maps the endset's I-addresses to the new V-position `[c,d)`.

**Answer to part 2: YES. The reported endset V-addresses reflect the new post-move positions, because `ispan2vspanset` derives V-addresses by querying the live POOM, not any snapshot from link creation time.**

---

### Summary

| Stage | Mechanism | File:Line |
|-------|-----------|-----------|
| Link endset stored | I-addresses in SPANRANGE of spanfilade | spanf1.c:49-51 |
| Copy/move preserves I-addresses | `insertpm` copies `lstream` → `crumorigin.dsas[I]` | orglinks.c:105 |
| Move updates V-mapping only | `insertpm` sets new V; POOM tracks new location | orglinks.c:113, 130 |
| `find_links` queries by I-address | `specset2sporglset` → I-addr query in SPANRANGE | spanf1.c:71, 245 |
| Endset I-address unchanged → still matches | SPANRANGE hit regardless of V movement | spanf1.c:245, 250 |
| Reported V-address is post-move | `ispan2vspanset` → `permute` → live POOM query | orglinks.c:393; context.c:206 |

The system's correctness here is architectural: V-addresses are **never** the primary key for link endset storage. The POOM is the sole keeper of the V↔I mapping, and `find_links` operates entirely on the I-address layer. Moving a region rewrites the POOM's V side while leaving the I side — and thus every link indexed against it — intact. The reported V-addresses are always freshly derived from the current POOM state at query time.
