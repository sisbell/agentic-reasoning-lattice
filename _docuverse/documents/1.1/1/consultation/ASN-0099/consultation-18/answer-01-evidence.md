## Question 1 [evidence]

> In the udanax-green implementation, do the routines corresponding to content extension, content contraction, and provenance/redirect recording ever modify the link store, or is link mutation confined entirely to the link-allocation routine?

## KB Synthesis

Based on the KB, the answer depends on which part of the link store you mean. The spanfilade has two independent sub-indices: the **link endpoint index** (I-address → link ISA) and the **DOCISPAN index** (I-address → document ISA). These behave very differently.

**Link endpoint index: confined to CREATELINK only**

CREATELINK is the sole operation that writes to the link endpoint index, via `insertendsetsinspanf()` [ST-CREATE-LINK, Finding 0012]. No other operation modifies it. The spanfilade has no deletion path for these entries at all — it is append-only [INV-SPANF-WRITE-ONLY, Finding 0057].

**Content extension (INSERT) and provenance recording (COPY/VCOPY): touch DOCISPAN, not the link index**

INSERT calls `insertspanf(..., DOCISPAN)` through the `docopy` path [ST-INSERT, Finding 0036]. VCOPY does likewise [ST-COPY, Finding 0047]. Both write to the DOCISPAN sub-index, making content discoverable via `find_documents`. However, `FC-CONTENT-SPANF-ISOLATION` (Finding 0036) explicitly refines the earlier stronger claim: content operations do not affect the *link index* portion of spanf — only the DOCISPAN portion.

**Content contraction (DELETE): does not touch the spanfilade at all**

`dodeletevspan` calls only `deletend` (operating on the POOM in granf) and `logbertmodified` — there is no call to any spanf function [ST-DELETE, Finding 0057]. This produces the well-known spanf/POOM divergence: after deletion, `find_documents` still returns the document (stale DOCISPAN entry persists), but the POOM no longer maps those I-addresses [EC-STALE-SPANF-REFERENCE].

**In short:** Link mutation in the sense of the link endpoint index is confined entirely to the link-allocation routine (CREATELINK). INSERT and COPY/VCOPY do write to the broader spanfilade structure (DOCISPAN sub-index), but DELETE does not write to the spanfilade at all, in either sub-index.

---

## Code Exploration

I have all the information needed. Here is the full answer.

---

## Link Store Mutation: Confined to Link-Allocation Only

### What constitutes the link store

The link store has two components:

1. **The spanfilade (`spanf`)**, a 2D enfilade whose `ORGLRANGE` axis is partitioned by span type (`xanadu.h:36–39`):
   ```c
   #define LINKFROMSPAN    1
   #define LINKTOSPAN      2
   #define LINKTHREESPAN   3
   #define DOCISPAN        4
   ```
   Entries 1–3 are link endpoints; entry 4 is the document content index. These are distinct namespaces within the same physical structure.

2. **Each link's own POOM (orgl)**, accessed via `findorgl`. This maps fixed V-addresses (FROM=1.1, TO=2.1, THREE=3.1) → I-spans of the endpoint content. It is populated by `insertpm` called through `insertendsetsinorgl`.

---

### Content extension: `doinsert`, `docopy`

`doinsert` [do1.c:117–122] calls `inserttextingranf` then delegates to `docopy`:

```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)  );
```

`docopy` [do1.c:59–63]:
```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

`docopy` writes only `DOCISPAN` entries to `spanf` — the document content index lane. It touches the **document's own POOM** via `insertpm` [orglinks.c:99–131], and `spanf` via `insertspanf` with type `DOCISPAN = 4`. Neither `insertendsetsinorgl` nor `insertendsetsinspanf` is called. **No link endpoint entries are written.**

---

### Content contraction: `dodeletevspan`, `dorearrange`

`dodeletevspan` [do1.c:158–167] calls only `deletevspanpm`:

```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)  );
```

`deletevspanpm` [orglinks.c:145–152]:
```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
logbertmodified(docisaptr, user);
```

`deletend` operates on the document POOM only. **`spanf` is not touched at all** — not even for `DOCISPAN`. There is no delete path into `spanf` from contraction. The `DOCISPAN` entries written at insert time are not cleaned up.

`dorearrange` [do1.c:34–43] similarly calls only `rearrangepm` [orglinks.c:137–142]:
```c
rearrangend((typecuc*)docorgl, cutseqptr, V);
logbertmodified(docisaptr, user);
```

`rearrangend` rewires the document POOM in-place. **`spanf` is not touched.** No link entries written.

---

### Provenance/redirect recording: `docreatenewversion`

`docreatenewversion` [do1.c:260–298] creates a new orgl, then copies the old version's content into it via `docopyinternal`:

```c
createorglingranf(taskptr, granf, &hint, newisaptr)    // allocates new ISA in granf
→ doretrievedocvspanfoo(taskptr, isaptr, &vspan)
→ addtoopen(newisaptr, user, TRUE, WRITEBERT)
→ docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec)
→ logbertmodified(newisaptr, user)
→ doclose(taskptr, newisaptr, user)
```

`docopyinternal` [do1.c:66–82] is the internal variant of `docopy`:
```c
if (!insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)) return FALSE;
```

Same as content extension: only `DOCISPAN = 4` entries are written to `spanf`. `insertendsetsinspanf` and `insertendsetsinorgl` are never called. **No link endpoint entries are written.**

---

### Link allocation: `docreatelink`, `domakelink`

`docreatelink` [do1.c:207–220] is the only operation that invokes both link-store mutation functions:

```c
createorglingranf (taskptr, granf, &hint, linkisaptr)   // allocate link ISA in granf
&& tumbler2spanset (taskptr, linkisaptr, &ispanset)
&& findnextlinkvsa (taskptr, docisaptr, &linkvsa)
&& docopy (taskptr, docisaptr, &linkvsa, ispanset)      // registers link ISA in host doc (DOCISPAN)
&& findorgl (taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
&& specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, tospecset, &tosporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
&& setlinkvsas (&fromvsa, &tovsa, &threevsa)
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset,
                        &tovsa, tosporglset, &threevsa, threesporglset)  // ← link POOM
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset,
                         tosporglset, threesporglset)                   // ← spanf link lanes
```

`insertendsetsinorgl` [do2.c:130–148] calls `insertpm` three times against the **link's own POOM** at V-addresses set by `setlinkvsas` [do2.c:169–183]: FROM=1.1, TO=2.1, THREE=3.1.

`insertendsetsinspanf` [do2.c:116–128] calls `insertspanf` with the three link endpoint types:
```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // lane 1
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)     // lane 2
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset,LINKTHREESPAN)  // lane 3
```

`insertspanf` [spanf1.c:51] calls `insertnd` on `spanfptr`, which is the global `spanf`. These are the **only** sites in the codebase where `LINKFROMSPAN`, `LINKTOSPAN`, or `LINKTHREESPAN` entries are written into `spanf`.

Note: `docopy` is also called within `docreatelink` [do1.c:212] to register the link's ISA as content occupying a V-address in the host document. That writes a `DOCISPAN` entry — the link-as-content index, not the link endpoint record.

---

### Conclusion

**Link mutation is confined entirely to `docreatelink` and `domakelink`.** No other operation writes `LINKFROMSPAN`, `LINKTOSPAN`, or `LINKTHREESPAN` entries to `spanf`, and no other operation calls `insertendsetsinorgl` to populate a link POOM.

The three other classes of operation behave as follows with respect to `spanf`:

| Operation | `spanf` DOCISPAN | `spanf` link lanes | link POOM |
|---|---|---|---|
| `doinsert` / `docopy` (content extension) | **written** | untouched | untouched |
| `dodeletevspan` / `dorearrange` (contraction) | untouched | untouched | modified (deletend / rearrangend) |
| `docreatenewversion` (provenance) | **written** | untouched | untouched |
| `docreatelink` / `domakelink` (link allocation) | **written** | **written** | **written** |

An important structural asymmetry: content contraction (`dodeletevspan`, `dorearrange`) modifies only the document POOM and does not touch `spanf` at all — meaning the `DOCISPAN` records written at insertion time are never removed when content is deleted. This is not a defect specific to link lanes; it is a property of the entire spanfilade design.
