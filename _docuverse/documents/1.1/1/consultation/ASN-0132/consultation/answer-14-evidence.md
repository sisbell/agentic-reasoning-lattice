## Question 14 [evidence]

> If a link's endset I-addresses have been transcluded into N documents via COPY, does that link contribute 1 to the count or N — i.e., is the counted unit the link identity or its appearances through shared content identity?

## KB Synthesis

The counted unit is the **link identity** — the link contributes **1** to the count regardless of how many documents have transcluded its endpoint content.

## Why transclusion doesn't multiply the link count

The spanfilade contains two independent sub-indices [SS-SPANF-OPERATIONS, SS-DOCISPAN]:

1. **Link endpoint index** (types 1/2/3, LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN): I-address → link ISA. Written once, at link creation, by `insertendsetsinspanf()`.
2. **DOCISPAN** (type 4): I-address → document ISA. Written on every COPY/INSERT, by `insertspanf(..., DOCISPAN)`.

`find_links` searches sub-index #1 exclusively [INT-SPORGL-LINK-INDEX]. `COPY` writes only to sub-index #2 [FC-CONTENT-SPANF-ISOLATION, ST-COPY]. When content is transcluded into N documents via COPY, N new DOCISPAN entries are created — but the link endpoint index is not touched. The link ISA was entered into the link endpoint index once, at creation time, and remains there as a single entry regardless of subsequent transclusions.

## How the count is computed

From [SS-PAGINATE-LINKS]: `FINDNUMOFLINKSFROMTOTHREE` materializes the result list from `findlinksfromtothreesp()` then counts elements. From [SS-FIND-LINKS]: `findlinksfromtothreesp()` converts the query specset to I-addresses, searches the link endpoint index for matching entries, and returns link ISAs. Since the endpoint index holds the link's ISA exactly once, the search returns it once — the count is 1.

## The appearance of sharing is in discoverability, not identity

Transclusion makes the link *discoverable* from all N documents (via shared I-addresses), but discovery and counting work through the same single entry. This is the INT-LINK-TRANSCLUSION invariant: `vcopy(content, src, dst)` does not create new links, does not copy links, and does not add entries to the link endpoint index [INT-LINK-TRANSCLUSION, FC-LINK-PERSISTENCE]. The link object is genuinely singular.

The only known duplication edge cases are pivot-induced fragmentation [EC-PIVOT-LINK-FRAGMENTATION] and multi-span link endset duplication [EC-MULTISPAN-LINK-DUPLICATION] — both unrelated to COPY transclusion, and both involving the same link appearing twice due to enfilade internal structure, not due to transclusion multiplying the link count.

---

## Code Exploration

I have traced the full execution path. Here is my complete answer.

---

## The counted unit is link identity: the answer is **1**, not N.

This is not an assumption — it is determined by three interlocking properties of the code. I'll trace each one.

---

### 1. What `docreatelink` writes into the spanfilade

`docreatelink` [`do1.c:195–221`] is the sole place a link's endset entries are inserted into the global spanfilade:

```c
&& specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
&& specset2sporglset(taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
...
&& insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

`specset2sporglset` → `vspanset2sporglset` [`sporgl.c:35–65`] converts the endset V-specs into sporgls. Each sporgl holds: `{sporgladdress: docisa, sporglorigin: i_stream, sporglwidth: i_width}`. The I-addresses come from passing the V-spans through the document's POOM via `vspanset2ispanset` [`orglinks.c:397–402`].

`insertendsetsinspanf` → `insertspanf` [`spanf1.c:15–54`] writes one entry per sporgl into the 2D spanfilade:

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
// ...
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);  // I-addresses
movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

The spanfilade entry maps: **(I-address range)** → **(spantype + link ISA)**, where `spantype` is one of `LINKFROMSPAN=1`, `LINKTOSPAN=2`, or `LINKTHREESPAN=3` [`xanadu.h:36–38`].

This `insertspanf` call happens **once**, at link creation, and is never called again for that link.

---

### 2. What `docopy` writes — and does not write — into the spanfilade

`docopy` [`do1.c:45–65`] also calls `insertspanf`, but with a different spantype:

```c
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)
&& insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)   // spantype = 4
```

`DOCISPAN = 4` [`xanadu.h:39`]. These entries record which documents contain which I-addresses (used by `finddocscontaining`). They occupy a completely different region of the ORGLRANGE axis from the link entries (which use prefixes 1–3).

When content with I-addresses `[X, X+W)` is COPYed into N documents, `docopy` is called N times. Each call creates a new `DOCISPAN=4` entry for that document. **No new `LINKFROMSPAN`, `LINKTOSPAN`, or `LINKTHREESPAN` entries are created.** The link's original entries — written once at `docreatelink` time — are unchanged.

---

### 3. How `findlinksfromtothreesp` searches and deduplicates

`dofindnumoflinksfromtothree` [`do1.c:355–360`] calls `findnumoflinksfromtothreesp` [`spanf1.c:105–115`]:

```c
bool findnumoflinksfromtothreesp(...)
{
    typelinkset linkset;
    INT n;

    if (!findlinksfromtothreesp(taskptr, spanfptr, ..., &linkset))
        return(FALSE);
    for (n = 0; linkset; linkset = linkset->next, ++n);
    *numptr = n;
    return (TRUE);
}
```

`findlinksfromtothreesp` [`spanf1.c:56–103`] converts the query V-spec into a sporglset via `specset2sporglset` (the same V→I conversion), then calls `sporglset2linkset` → `sporglset2linksetinrange` [`sporgl.c:239–269`]:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, ...);
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
    onlinklist(taskptr, linksetptr, &linksa);
}
```

The `range` is built as `prefixtumbler(&orglrange->stream, spantype, &range.stream)` — it restricts the ORGLRANGE query to `LINKFROMSPAN`, `LINKTOSPAN`, or `LINKTHREESPAN`. The `DOCISPAN=4` entries from COPY are structurally invisible here.

Finally, `onlinklist` [`spanf2.c:26–44`] deduplicates by link ISA equality:

```c
bool onlinklist(typetask *taskptr, typelinkset *linksetptr, typeisa *linkisaptr)
{
    // ...
    for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
        if (tumblereq(&temp->address, linkisaptr))
            return(0);   // already present — skip
    }
    temp->next = linkset;
}
```

Even if the spanfilade traversal encounters the same link ISA multiple times (e.g., because the query I-range partially overlaps with separate stored sporgl entries), it is added to the linkset only once.

---

### Synthesis

The I-addresses are the stable identity of content. When content is COPYed into N documents, each copy's POOM maps new V-addresses to the **same** original I-addresses. The link's endset entries in the spanfilade were indexed by those I-addresses at creation, and they remain indexed by those I-addresses forever — there is no mechanism by which COPY retriggers `insertspanf` with `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN`.

When any of those N documents queries for links touching its copy of the content:
- The V-addresses are converted to I-addresses via that document's POOM — yielding the same original I-addresses regardless of which document is queried from.
- The spanfilade search finds the same single link ISA.
- `onlinklist` ensures it appears once in the result.
- `findnumoflinksfromtothreesp` counts list length: **1**.

**The counted unit is the link identity. A link that points at content transcluded into N documents contributes 1 to any link count query from any of those N documents, not N.**
