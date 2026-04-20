## Question 12 [gregory]

> If a link L references content at I-addresses `[i, i+3)`, that content is deleted from all documents (making L orphaned), and then a COPY transcludes just `[i+1, i+2)` (a subset of the original endset) into a new document, does `find_links` on that new document rediscover L — and if so, does the returned endset show only the single transcluded byte or the full original three-byte span?

## KB Synthesis

## Answer

**Yes, `find_links` rediscovers L. The returned endset shows only the single transcluded byte, not the original three-byte span.**

---

### Part 1: Rediscovery

`find_links` operates on I-address intersection, not V-stream presence [SS-FIND-LINKS]:

> `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`

Partial overlap suffices. D_new's COPY puts `[i+1, i+2)` into its POOM. L's source endset covers `[i, i+3)`. The intersection is `{i+1}` — non-empty. L is returned.

Two invariants make this work despite the prior deletion:

1. **The spanfilade is write-only** [INV-SPANF-WRITE-ONLY]: When L was originally created, `insertendsetsinspanf` indexed `[i, i+3) → L` in the spanfilade. DELETE removes POOM entries but never touches the spanfilade [ST-DELETE, Finding 0057]. Those index entries still exist.

2. **The spanfilade is not disturbed by orphaning** [INV-LINK-PERMANENCE]: Even when all documents deleted the content, L's spanfilade entries persisted. The COPY into D_new creates a new DOCISPAN entry for D_new at `i+1` [SS-DOCISPAN], but the link index entry `i+1 → L` was already there from L's creation.

---

### Part 2: The Endset Shows Only One Byte

The endset resolution is governed by [INV-ITOV-FILTERING] and [SS-FOLLOWLINK]:

> FOLLOWLINK extracts I-addresses from the link orgl, then converts them to V-addresses using the **querying document's POOM**. If an I-address has no POOM mapping, it is silently dropped — no V-span is added to the result.

D_new's POOM maps:
- `i` → no entry (not transcluded) → **dropped**
- `i+1` → some V-position v₁ → **included**
- `i+2` → no entry (not transcluded) → **dropped**

The endset returned is the V-span `[v₁, v₁+1)` in D_new — one byte.

This matches the behavior documented in the `partial_vcopy_of_linked_span` test [SS-FOLLOW-LINK]: a link created on "hyperlink text" (14 chars) is discovered via a transcluded "link" (4 chars), but `follow_link` resolves to only the 4 chars present in the querying document, not the original 14.

The same filtering applies here, but more aggressively: only 1 of 3 original bytes is present in D_new, so only 1 appears in the endset.

---

### What Cannot Be Recovered

The original 3-byte span is unrecoverable through normal operations. `follow_link` against any document that once held the full `[i, i+3)` range returns empty `[]` — because deletion freed those POOM entries [ST-DELETE, FC-VERSION-ISOLATION]. The link orgl in I-space still stores the full original I-address range [INV-LINK-PERMANENCE], but resolution requires a live POOM mapping, and none exists for `i` or `i+2`. COPY is the only mechanism for identity-preserving restoration [ST-COPY, Finding 0064], and only `i+1` was re-introduced.

---

## Code Exploration

Now I have all the information needed. Let me trace the full execution path to answer both sub-questions.

---

## Full Answer

### Scenario Setup Recap

- Link L created with a from-endset (or to-endset) covering I-addresses `[i, i+3)` (3 bytes)
- All documents' POOMs updated by `dodeletevspan` to remove `[i, i+3)` from V-space
- New document D: COPY transcluded only `[i+1, i+2)` (1 byte) into it
- Question: Does `find_links` on D rediscover L? And what does the endset show?

---

### Part 1: Does `find_links` rediscover L?

**Yes.** Here is the trace:

#### Step A — Link creation stores the full I-span in the spanfilade

When L was created, `docreatelink` [do1.c:195–221] called `insertendsetsinspanf` [do2.c:116–128], which called `insertspanf` [spanf1.c:15–54] for each endset sporgl. That call stored a crum in the global `spanf` with:

```c
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);   // I-address: i
movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);     // width: 3
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```
[spanf1.c:49–51]

The spanfilade crum records: `SPANRANGE = [i, i+3)`, `ORGLRANGE = linkisa.LINKFROMSPAN`.

#### Step B — Deletion does NOT touch the spanfilade

`dodeletevspan` [do1.c:158–167] calls only:

```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
logbertmodified(docisaptr, user);
```
[orglinks.c:149–150]

Only the **document's POOM** is modified. The global `spanf` and L's own POOM (`insertpm` records) are never touched. L's spanfilade entry for `[i, i+3)` persists intact.

#### Step C — COPY of `[i+1, i+2)` into D

`docopy` [do1.c:45–65] calls:

```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)    // [i+1, i+2)
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)         // D's POOM: V→[i+1,i+2)
&& insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)     // spanf DOCISPAN entry
```

D's POOM now has a single crum: `I-axis = [i+1, i+2)` ↔ `V-axis = some vD`.

#### Step D — `find_links` on D

`findlinksfromtothree` [fns.c:189] → `dofindlinksfromtothree` [do1.c:348] → `findlinksfromtothreesp` [spanf1.c:56]:

```c
specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
```
[spanf1.c:71, 77]

`specset2sporglset` [sporgl.c:14] → `vspanset2sporglset` [sporgl.c:35]:

```c
vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);    // permute V→I in D's POOM
```

D's POOM maps `vD → [i+1, i+2)`, so `ispanset = [i+1, i+2)`. This becomes a sporgl with `sporglorigin=i+1, sporglwidth=1`.

`sporglset2linkset` [sporgl.c:222] → `sporglset2linksetinrange` [sporgl.c:239]:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, ...);
```

`retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` [retrie.c:229]. The restriction is SPANRANGE = `[i+1, i+2)`. The query checks whether L's spanfilade crum (`SPANRANGE = [i, i+3)`) qualifies:

```c
bool crumqualifies2d(... span1start=[i+1], span1end=[i+2] ...) {
    endcmp = whereoncrum(crumptr, ..., span1end=[i+2], SPANRANGE);   // [i,i+3) contains i+2 → THRUME
    // NOT ≤ ONMYLEFTBORDER → passes
    startcmp = whereoncrum(crumptr, ..., span1start=[i+1], SPANRANGE); // [i,i+3) contains i+1 → THRUME
    // NOT > THRUME → passes
    ...
    return TRUE;
```
[retrie.c:270–305]

`[i, i+3)` contains `[i+1, i+2)` entirely, so `crumqualifies2d` returns TRUE. The context is built from this crum. Then:

```c
beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
onlinklist(taskptr, linksetptr, &linksa);
```
[sporgl.c:264–265]

L's ISA is extracted from the ORGLRANGE and added to the result. **L is found.**

---

### Part 2: What does the endset show?

`find_links` returns only link ISAs — no endset is included in the `findlinksfromtothreesp` result. The subsequent call to retrieve L's endset goes through two distinct paths:

#### Path A — `follow_link` (via `dofollowlink`)

`dofollowlink` [do1.c:223] → `link2sporglset` [sporgl.c:67]:

```c
retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)
```

This queries L's **own POOM** (populated by `insertpm` at creation time) at V-address `whichend`. L's POOM crum has `I-axis = [i, i+3)` (the full 3 bytes stored at creation). `contextintosporgl` [sporgl.c:205] extracts:

```c
movetumbler(&context->context2dinfo.homedoc, &sporglptr->sporgladdress);  // original source doc
movetumbler(&context->totaloffset.dsas[I], &sporglptr->sporglorigin);     // i
movetumbler(&context->contextwid.dsas[I], &sporglptr->sporglwidth);       // 3
```

Then `linksporglset2specset` [sporgl.c:97]:

```c
} else {
    linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
}
```

Since `sporgladdress` (the original source doc) is non-zero, it calls `sporglset2vspanset` [sporgl.c:141] → `ispan2vspanset` [orglinks.c:389] → `permute` on the **original source document** with I-span `[i, i+3)`. That document's POOM no longer has any mapping for those bytes (deleted). `permute` → `span2spanset` → `retrieverestricted` finds no crums. **Returns empty vspanset.**

The document D (which has `[i+1, i+2)`) is never consulted here, because `homedoc` in the sporgl is the original source document set at link creation time [sporgl.c:53]:

```c
movetumbler(docisa, &sporglset->sporgladdress);   // set to original source doc
```
[sporgl.c:53]

#### Path B — `retrieve_endsets` (via `retrieveendsetsfromspanf`)

`retrieveendsetsfromspanf` [spanf1.c:190] finds L's spanfilade entry for its from-endset. `contextintosporgl` [sporgl.c:205] extracts the stored I-span: `sporglorigin=i, sporglwidth=3` — the **full 3 bytes** — with `sporgladdress = homedoc` (original source doc). `linksporglset2vspec` then calls `ispan2vspanset` on the original source document with `[i, i+3)` → **empty vspanset** (deleted).

The returned specset is a `VSPECID` node with `docisa=homedoc` and `vspanset=NULL`.

#### The clipping function `context2span` is not the issue

`context2span` [context.c:176–212] does proportional clipping when translating between I and V dimensions in `span2spanset`/`permute`. This function would correctly return just 1 byte if called on document D's POOM with restriction `[i, i+3)`. But it is only invoked during `ispan2vspanset` on `homedoc` — and `homedoc` is always the **original source document**, not D, because that is what was stored in the spanfilade at creation time.

---

### Summary

| Question | Answer | Key Code |
|---|---|---|
| Does `find_links` on D find L? | **Yes** | `crumqualifies2d` at retrie.c:270 passes because `[i, i+3) ∩ [i+1, i+2) ≠ ∅` |
| What endset does `follow_link` return? | **Empty vspanset** | `sporglset2vspanset` at sporgl.c:141 looks up `[i, i+3)` in original source doc (deleted); D is never consulted |
| What is stored in the spanfilade? | **Full 3-byte I-span `[i, i+3)`** | `insertspanf` at spanf1.c:49–51 stores the full original width; deletion never modifies `spanf` |
| Is the 1-byte transcluded copy ever reflected in the endset? | **No** | The `homedoc` pointer in the sporgl permanently locks endset resolution to the original source document |

**The returned endset is neither "1 byte" nor "3 bytes"** — it is **empty** (`vspanset = NULL`). The spanfilade stores the full original 3-byte I-span `[i, i+3)` and that is what `crumqualifies2d` matches against during `find_links`. But when any endset retrieval attempts to resolve those I-addresses back to V-space, it does so against `homedoc` (the original source document, where the content was deleted). The 1-byte copy in D updates D's own POOM and a new DOCISPAN entry in `spanf`, but it does not update L's LINKFROMSPAN/LINKTOSPAN entries or L's internal POOM. There is no mechanism by which L's stored endsets point at D.
