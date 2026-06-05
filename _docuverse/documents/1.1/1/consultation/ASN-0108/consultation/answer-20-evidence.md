## Question 20 [evidence]

> For "ghost links" whose endset I-addresses are silently filtered during I→V conversion, are they counted as occupying a window slot before filtering, or does filtering happen before windowing so the reader sees N valid links per window?

## KB Synthesis

Windowing happens **before** I→V filtering. Ghost links occupy window slots.

The pipeline has two distinct stages:

**Stage 1 — Link discovery (spanfilade search)**
`findlinksfromtothreesp()` searches the spanfilade by I-address intersection and returns a list of **link ISAs**. The N-item truncation (`linkset->next = NULL`) operates directly on this ISA list [SS-PAGINATE-LINKS]. Because the spanfilade is write-only and retains entries permanently after DELETE [INV-SPANF-WRITE-ONLY], ghost links whose endpoint I-addresses still match the query's I-address range appear in the ISA list and consume a window slot. The window counter counts link ISAs, not resolved V-spans.

**Stage 2 — Endpoint resolution (I→V conversion)**
Only when the caller subsequently invokes FOLLOWLINK or RETRIEVEENDSETS does the I→V filtering occur. `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()` silently drops any I-address that has no current POOM mapping [INV-ITOV-FILTERING, EC-GHOST-LINK]. A ghost link's I-addresses pass through Stage 1 successfully, then produce `[]` in Stage 2.

**Consequence:** With window size N, a caller may receive N link ISAs of which some subset are ghost links. Each ghost link consumed a slot. The caller discovers this only by calling FOLLOWLINK and receiving empty endsets [EC-GHOST-LINK]. There is no way to pre-filter ghosts at the pagination layer — `findlinksfromtothreesp()` has no visibility into POOM state.

---

## Code Exploration

Now I have everything I need to trace the complete execution path. Let me write the full answer.

---

## Ghost Links and Window Slots: The Answer

**Ghost links occupy window slots before filtering.** Windowing is applied to a raw list of link ISAs with no I→V conversion. The filtering (empty vspanset) only surfaces when the client subsequently retrieves each link's endsets.

---

### The Windowing Function: `findnextnlinksfromtothreesp` (spanf1.c:117–149)

```c
bool findnextnlinksfromtothreesp(typetask *taskptr, typespecset fromvspecset, ...,
    typeisa *lastlinkisaptr, typelinkset *nextlinksetptr, INT *nptr)
{
    n = 0;
    *nextlinksetptr = NULL;
    if (!findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset,
                                threevspecset, orglrangeptr, &linkset))    // (1)
        return (FALSE);
    if (iszerotumbler(lastlinkisaptr)) {
        *nextlinksetptr = linkset;                                          // (2)
    } else {
        for (; linkset; linkset = linkset->next) {
            if (tumblereq(&linkset->address, lastlinkisaptr)) {
                *nextlinksetptr = linkset->next;
                break;
            }
        }
    }
    for (linkset = *nextlinksetptr; linkset; linkset = linkset->next) {
        if (++n >= *nptr) {                                                 // (3)
            linkset->next = NULL;
            break;
        }
    }
    *nptr = n;
    return (TRUE);
}
```

Steps:
1. Get the **full unfiltered link ISA list** from `findlinksfromtothreesp`
2. Advance past `lastlink` (cursor-based paging)
3. Truncate at `*nptr` — the window limit

**No I→V conversion happens anywhere in this function.** The `linkset` contains `typelink` structs with `.address` fields (link ISAs — tumblers), not endset content.

---

### What `findlinksfromtothreesp` Returns (spanf1.c:56–103)

The call chain is:

`findlinksfromtothreesp` → `sporglset2linkset` → `sporglset2linksetinrange` (sporgl.c:239–269):

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                             &range, ORGLRANGE, (typeisa*)infoptr);
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
    onlinklist(taskptr, linksetptr, &linksa);              // (sporgl.c:265)
}
```

This queries the spanfilade by **SPANRANGE** (I-address range of the endsets stored at link-creation time) and extracts **ORGLRANGE** values (link ISAs). The spanfilade is never purged of dead entries — see the `find_documents` note in the client API about stale results (Finding 0057: spanfilade is write-only). A link whose I-address endset was registered at link-creation time remains findable forever, regardless of whether the V-mapping for that I-address still exists.

The result is a list of link ISAs. Ghost status is unknowable at this level.

---

### Where I→V Conversion Actually Happens

When the client calls `follow_link(linkid, end)`, the path is:

`followlink` (fns.c:114) → `dofollowlink` (do1.c:223):

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr,
                  typespecset *specsetptr, INT whichend)
{
    return (
        link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
     && linksporglset2specset(taskptr, &((typesporgl*)sporglset)->sporgladdress,
                              sporglset, specsetptr, NOBERTREQUIRED));
}
```

**Step 1 — `link2sporglset` (sporgl.c:67–95):** Reads the link's own POOM granfilade node, queries V-position `whichend` (1.x = FROM, 2.x = TO, 3.x = THREE), extracts the **stored I-address** via `retrieverestricted(..., V, ..., I, ...)`. This is reading the link's internal POOM — it always succeeds as long as the link node exists.

**Step 2 — `linksporglset2specset` (sporgl.c:97–123):** For each sporgl (I-address), calls `linksporglset2vspec` → `sporglset2vspanset`:

```c
specptr->itemid = VSPECID;
specptr->vspanset = NULL;                                    // (sporgl.c:135)
sporglset2vspanset(taskptr, homedoc, sporglsetptr,
                   &specptr->vspanset, type);                // (sporgl.c:136)
```

Inside `sporglset2vspanset` (sporgl.c:141–176):

```c
vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);
```

`ispan2vspanset` → `permute` → `span2spanset` (orglinks.c:389–454) → `retrieverestricted`. **If the I-address has no current V-mapping** (the content was deleted from V-space via `dodeletevspan`/`deletevspanpm`), `retrieverestricted` returns a NULL context list, `span2spanset` appends nothing, and `vspansetptr` is left pointing to the same unchanged slot. The `specptr->vspanset` remains NULL.

**Critically**, back in `linksporglset2specset` (sporgl.c:118–120):

```c
((typeitemheader*)specset)->next = NULL;
*specsetptr = specset;                         // ALWAYS appended
specsetptr = (typespecset*)&((typeitemheader*)specset)->next;
```

The `typevspec` node is **always** allocated and appended to the returned specset, even when `vspanset = NULL`. The ghost endset is silently included.

---

### The Same Pattern for `retrieve_endsets`

When the client calls `retrieve_endsets(specset)` (protocol command 28):

`retrieveendsets` (fns.c:350) → `doretrieveendsets` (do1.c:369) → `retrieveendsetsfromspanf` (spanf1.c:190–235) → `linksporglset2specset` — same path, same ghost behavior.

---

### Conclusion

The ordering is:

```
findnextnlinksfromtothreesp:
  1. findlinksfromtothreesp → returns ALL matching link ISAs (incl. ghosts)
  2. window applied: skip to cursor, truncate at N
  3. return N link ISAs to client

[later, per link]
  4. follow_link / retrieve_endsets → ispan2vspanset
  5. if I→V mapping gone → vspanset = NULL (ghost, silent)
```

**Window slots are counted from the raw, unfiltered ISA list.** A client that requests N links via `find_next_n_links` gets exactly N link ISAs (or fewer if the total is smaller), but some of those N may prove to be ghosts when their endsets are subsequently retrieved. There is no pre-filtering pass that removes ghosts before the window is counted.

The mechanism: `sporglset2linksetinrange` [sporgl.c:239] queries the spanfilade by I-address overlap and returns link ISAs — a purely I-space operation. `findnextnlinksfromtothreesp` [spanf1.c:117] windows that list — also a purely I-space operation. Only when the client chases a link ISA through `linksporglset2specset` [sporgl.c:97] → `ispan2vspanset` [orglinks.c:389] does the silent ghost emerge as a VSPECID node with `vspanset = NULL`.
