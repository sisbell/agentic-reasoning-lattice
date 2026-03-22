## Question 19 [gregory]

> After CREATELINK completes, does `find_links` on the home document discover the newly created link through the link orgl's own I-address in the POOM, through the endset I-spans in the spanfilade, or through both paths — and which path is the actual discovery mechanism?

## KB Synthesis

`find_links` discovers the newly created link **exclusively through the spanfilade endset entries** — the POOM 2.x entry plays no role in this path.

## The Two Layers CREATELINK Writes

[ST-CREATE-LINK, SS-THREE-LAYER-MODEL] make clear that CREATELINK produces three effects:

1. **I-space (granfilade):** New link orgl at a fresh ISA (e.g., `1.1.0.1.0.1.0.2.1`)
2. **POOM (home document):** V-position 2.x → link orgl ISA (makes the link visible in the document's V-stream)
3. **Spanfilade:** Endset entries mapping the *endpoint content I-addresses* → link ISA (indexed by `insertendsetsinspanf`)

## What `find_links` Actually Searches

[SS-DUAL-ENFILADE] Finding 0012 states it directly: "Link search (`find_links`) accesses only `spanf`." [SS-SPANF-OPERATIONS] confirms the spanfilade maps I-addresses to the links referencing them, and `dofindlinksfromtothree()` delegates entirely to `findlinksfromtothreesp()`.

The search algorithm ([SS-FIND-LINKS]):
1. Convert the query specset to content I-addresses (permascroll addresses from the text subspace)
2. Search the spanfilade for those I-addresses
3. Return any link ISA whose endpoint I-addresses intersect

## Why the POOM 2.x Entry Is Irrelevant to Discovery

The POOM 2.x entry stores the link orgl's ISA — a document-structure address, not a content identity. `find_links` searches by *endpoint content I-addresses*, not by link orgl positions. The 2.x entries serve `retrieve_vspanset` (showing the link in the document's V-stream) and direct orgl access, but are invisible to the spanfilade search.

[INT-LINK-TRANSCLUSION] confirms this architectural separation: when transcluded content makes a link discoverable from a new document, it works because the transclusion shares content I-addresses that match the spanfilade entries — no POOM 2.x entries are involved or required.

## Consequence

This means `find_links` on the home document after CREATELINK succeeds only when the query specset covers content whose I-addresses match the link's endpoint I-addresses in the spanfilade. Querying the home document's *link subspace* (2.x) would not discover the link — the spanfilade is indexed by endpoint content identity, not by where the link orgl lives. [FC-CONTENT-SPANF-ISOLATION] formalizes this: the two search paths are entirely independent.

---

## Code Exploration

All citations confirmed. Here is the complete answer.

---

## How `find_links` Discovers Links After CREATELINK

The answer is **Path 2 only — the endset I-spans in the spanfilade**. The link's own POOM is written during CREATELINK but is never consulted during discovery. Here is the full trace.

---

### What CREATELINK Writes

`docreatelink` [`do1.c:195–221`] ends with two back-to-back writes:

```c
  && insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, ...)   // do1.c:218
  && insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, ...)            // do1.c:219
```

**Write 1 — POOM** (`insertendsetsinorgl`, `do2.c:130–148`):

Calls `insertpm` to store the endsets inside the link's own granfilade node. This is internal link structure — used by FOLLOWLINK to navigate *from* a known link to its endsets. It is a dead end for discovery.

**Write 2 — Spanfilade** (`insertendsetsinspanf`, `do2.c:116–128`):

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)  // do2.c:119
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)    // do2.c:120
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset,LINKTHREESPAN) // do2.c:123
```

Inside `insertspanf` [`spanf1.c:15–54`], for each endset I-span in the sporglset:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);   // spanf1.c:22
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);             // spanf1.c:49
movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);              // spanf1.c:50
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE); // spanf1.c:51
```

Each node inserted into the spanfilade encodes:
- **ORGLRANGE key**: link ISA prefixed with `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN`
- **SPANRANGE key**: the actual I-span of the endset content
- **`linfo.homedoc`**: the link ISA

The spanfilade is therefore a 2D index: given an I-span in content space (SPANRANGE), it returns the link ISAs of all links whose endsets cover that span (ORGLRANGE).

---

### What FIND Reads

The call chain for FINDLINKSFROMTOTHREE:

**`fns.c:196–201`**:
```c
getfindlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset,
                        (typeispan*)NULL/*homeset*/,    // ← homeset silently dropped
                        &linkset)
```

Note the cast to `NULL`: even though the client sends a `homeset` (orgl address restriction), `fns.c:198` discards it, making the search unconditionally global.

**`do1.c:348–353`** — delegates directly to the spanfilade:
```c
return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset,
                              threevspecset, orglrangeptr, linksetptr);
```

**`spanf1.c:56–103`** — `findlinksfromtothreesp` converts the query V-specsets to sporglsets (I-span form), then calls:
```c
sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset,
                   orglrange, LINKFROMSPAN);   // spanf1.c:77
sporglset2linkset (taskptr, (typecuc*)spanfptr, tosporglset,   &tolinkset,
                   orglrange, LINKTOSPAN);     // spanf1.c:85
```

**`sporgl.c:222–269`** — `sporglset2linkset` → `sporglset2linksetinrange`:

```c
// orglrange is NULL (from fns.c:198), so takes the else branch:
context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE,
                              (typespan*)NULL, ORGLRANGE,
                              (typeisa*)infoptr);            // sporgl.c:261
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa); // sporgl.c:264
    onlinklist (taskptr, linksetptr, &linksa);               // sporgl.c:265
}
```

`retrieverestricted` queries the spanfilade with the endset I-spans as the SPANRANGE key and returns all matching ORGLRANGE values. `beheadtumbler` strips the `LINKFROMSPAN`/`LINKTOSPAN` prefix from the ORGLRANGE value to recover the raw link ISA.

The POOM is never opened.

---

### Summary

| | During CREATELINK | During FIND |
|---|---|---|
| **POOM** (link's granfilade node) | Written by `insertendsetsinorgl` [`do1.c:218`] | Never read |
| **Spanfilade** (2D I-span index) | Written by `insertendsetsinspanf` [`do1.c:219`] → `insertspanf` [`spanf1.c:51`] | Read by `sporglset2linksetinrange` [`sporgl.c:259–265`] |

**The actual discovery mechanism is Path 2: the endset I-spans in the spanfilade.** The spanfilade acts as a pre-built reverse index from content spans to link ISAs. FIND never touches the link's own POOM; it searches the spanfilade directly, resolves matching ORGLRANGE entries back to link ISAs via `beheadtumbler`, and returns them. The POOM write at `do1.c:218` enables FOLLOWLINK (endset traversal from a *known* link) — a structurally separate operation that is not involved in discovery.
