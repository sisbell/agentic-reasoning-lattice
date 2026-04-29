## Question 11 [gregory]

> When two documents both hold V→I mappings to the same I-address range (via transclusion), does the system record which document originally created that content, or are all V→I references to shared I-addresses indistinguishable at the storage level?

## KB Synthesis

The system records provenance at two distinct levels, but with different precision.

## At the POOM level: provenance is recorded per-crum

Each POOM bottom crum has a `homedoc` field (the `sporgladdress`) that records which document the I-addresses originated from [SS-SPORGL]. The `isanextensionnd()` function checks this field — it only coalesces adjacent content when the `homedoc` matches [ST-INSERT, Finding 0046, EC-LINK-PARTIAL-SURVIVAL]. This means two documents that both transcluded from the same source will have crums that share I-addresses but carry the same `homedoc` origin [INV-IADDR-PROVENANCE].

**Concretely:** if document B inserts "hello" natively (I-addresses α₁–α₅, homedoc=B) and document C transcludes that content (same I-addresses α₁–α₅, homedoc=B), both POOMs carry the same provenance. The `homedoc` records the *original allocator* (B), not the transcluder (C). This is a key asymmetry: INSERT allocates fresh I-addresses under the target document's address space, so the allocating document IS the homedoc; COPY shares existing I-addresses, so the homedoc is inherited from the original.

## At the granfilade level: I-addresses are fully distinguishable by address structure

I-addresses are allocated per-document within element subspace 3 (for text): `account.0.document.0.3.N` [SS-ADDRESS-SPACE, Finding 0065]. The document component is encoded directly in the I-address tumbler. So by inspection of the I-address itself, you can determine which document allocated it.

## At the spanfilade level: DOCISPAN entries record document-to-I-address associations

The DOCISPAN index maps I-address ranges to document ISAs [SS-DOCISPAN]. Every INSERT and COPY creates entries, so the index reflects *which documents hold references* — but since DELETE never removes spanfilade entries [INV-SPANF-WRITE-ONLY], this is a historical superset, not a current-state answer [EC-STALE-SPANF-REFERENCE].

## Summary

| Level | What's recorded | Distinguishable? |
|-------|----------------|-----------------|
| I-address structure | Allocating document encoded in tumbler digits | Yes — by address inspection |
| POOM crum `homedoc` | Original allocating document | Yes — per-crum field |
| Spanfilade DOCISPAN | All documents that have ever referenced the I-address | Yes, but stale after DELETE |

Two different documents' V→I references to the same shared I-address range are **distinguishable** — each POOM crum carries a `homedoc` field pointing to the original creator, and the I-address itself encodes the origin document [INV-IADDR-PROVENANCE]. What the system cannot tell you is which documents *currently* hold live references (POOM mappings) vs. which ones *ever did* (spanfilade) — that distinction requires cross-referencing both layers [INT-DELETE-SPANF-DIVERGENCE].

---

## Code Exploration

I have now read all the relevant source files directly. Here is my full answer.

---

## V→I Mapping Provenance in udanax-green

**Short answer:** The system stores V→I mappings per-document, so two documents transcluding the same I-address range produce *distinguishable* spanfilade entries — each tagged with the transcluding document's ISA. However, there is **no flag or field distinguishing "content creator" from "content transcluder"** at the spanfilade level. The original creator is recorded elsewhere (granfilade hints), not in the V→I mapping itself.

---

### The spanfilade: one global 2D index

There is a single global spanfilade (`spanf`). Every V→I mapping from every document is stored there. It is a 2D enfilade:

- **Axis 1 (`ORGLRANGE`):** document ISA, prefixed with `DOCISPAN = 4` [`xanadu.h:39`]. This identifies *which document* holds this V→I mapping.
- **Axis 2 (`SPANRANGE`):** I-address range (the invariant content address).

Every leaf node is a `type2dcbc` (2D core bottom crum) [`enf.h:108-131`]:

```c
struct struct2dcbc {
    ...
    typedsp  cdsp;
    typewid  cwid;
    type2dbottomcruminfo c2dinfo;   /* [enf.h:129] */
};
```

And `type2dbottomcruminfo` is defined in `wisp.h:106-109`:

```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

So each leaf carries exactly one extra tumbler: `homedoc`. This stores the ISA of the document that performed the `docopy()` call.

---

### How `homedoc` is populated: `insertspanf`

`insertspanf` [`spanf1.c:15-54`] is the write path for all V→I registrations. For each item in the sporglset it sets `linfo.homedoc` and calls `insertnd`:

```c
if (itemid == ISPANID) {
    movetumbler(&((typeispan*)sporglset)->stream, &lstream);
    movetumbler(&((typeispan*)sporglset)->width,  &lwidth);
    movetumbler(isaptr, &linfo.homedoc);            /* [spanf1.c:29] — transcluding doc */
} else if (itemid == SPORGLID) {
    movetumbler(&((typesporgl*)sporglset)->sporglorigin,  &lstream);
    movetumbler(&((typesporgl*)sporglset)->sporglwidth,   &lwidth);
    movetumbler(&((typesporgl*)sporglset)->sporgladdress, &linfo.homedoc); /* [spanf1.c:33] */
} else if (itemid == TEXTID) {
    ...
    movetumbler(isaptr, &linfo.homedoc);            /* [spanf1.c:42] */
}
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

`isaptr` is the **calling document's ISA** — the document doing the transcluding. When two documents A and B both `docopy()` the same I-range, `insertspanf` is called twice (once per `docopy`), and each call inserts a separate spanfilade node with its own `homedoc` value.

**The two V→I references are therefore distinguishable by `homedoc`.**

---

### `doinsert` vs `docopy`: same storage, different granfilade

`doinsert` [`do1.c:87-123`] first creates new I-space content in the granfilade, then immediately transclubes it into the originating document via `docopy`:

```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);  /* [do1.c:117] */
inserttextingranf(taskptr, granf, &hint, textset, &ispanset);
docopy(taskptr, docisaptr, vsaptr, ispanset);           /* [do1.c:119] */
```

`docopy` [`do1.c:45-65`] is the shared V→I registration path:

```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED);
findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT);
insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset);  /* [do1.c:60] */
insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN); /* [do1.c:62] */
```

The `ispanset` items passed into `insertspanf` have `ISPANID` type — bare I-spans with no embedded owner field. In that branch, `homedoc` is always set to `isaptr` (the calling document) [`spanf1.c:29`].

**Conclusion on doinsert vs docopy:** The spanfilade entry produced by the creator document (via `doinsert → docopy`) is structurally identical to the entry produced by any other document that later calls `docopy` on the same I-range. Both receive `homedoc = their own ISA`. The spanfilade cannot tell you which document was first.

The original creator *is* recorded — but in the **granfilade** via the `hint` (`TEXTATOM`, document ISA) stored in `inserttextingranf`. That is a separate lookup path from the V→I mapping.

---

### `finddocscontaining`: all transclusions are returned as equals

The FEBE command `FINDDOCSCONTAINING` [`fns.c:20-29`] calls:
```
finddocscontaining → dofinddocscontaining [do1.c:15] → finddocscontainingsp [spanf1.c:151]
```

In `finddocscontainingsp` [`spanf1.c:151-188`], the spanfilade is queried for all `ORGLRANGE` entries that overlap the requested I-span:

```c
tumblerincrement(&docspace.stream, 0, DOCISPAN, &docspace.stream);  /* [spanf1.c:168] */
tumblerincrement(&docspace.width, 0, 1, &docspace.width);
context = retrieverestricted((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    movetumbler(&c->totaloffset.dsas[ORGLRANGE], &docid);
    beheadtumbler(&docid, &document.address);       /* [spanf1.c:174] strip prefix → doc ISA */
    ...
}
```

This returns every document whose `ORGLRANGE` axis falls in the `DOCISPAN` band and whose `SPANRANGE` overlaps the query I-span. The content creator and every transcluder appear here identically. There is no "created by" bit in the result.

---

### The `homedoc` filter exists but is dead code at the call site

`crumqualifies2d` [`retrie.c:270-280`] contains a filter:

```c
if ((crumptr->height == 0) && infoptr
&& !tumblereq(&infoptr->homedoc, &(((type2dcbc*)crumptr)->c2dinfo.homedoc))) {
    return (FALSE);
}
```

This would allow retrieval restricted to a specific document's homedoc. But `findcbcinarea2d` — the only caller — unconditionally errors if `infoptr` is non-NULL:

```c
#ifndef DISTRIBUTION
if(infoptr){
    fprintf(stderr,"not NULL infoptr versions mumble specialcase 11/27/84 ...");
    gerror("findcbcinarea2d");
}
#else
    if (infoptr) gerror("!NULL");   /* [retrie.c:249-250] */
#endif
```

The comment "shouldnt happen till we try something fancier" [`retrie.c:245-246`] confirms this was planned but never activated. The filter is unreachable in any shipped build.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Are two transclusions of the same I-range distinguishable? | **Yes** — by `homedoc` in each spanfilade leaf | `wisp.h:108`, `spanf1.c:29`, `enf.h:129` |
| Does `homedoc` identify the original content creator? | **No** — it identifies the document that called `docopy()` | `spanf1.c:29,42` (always set to `isaptr` = caller) |
| Where is the original creator recorded? | In the **granfilade** via `makehint(TEXTATOM, docisaptr)` | `do1.c:117`, `inserttextingranf` |
| Does `finddocscontaining` distinguish creator from transcluder? | **No** — all are returned as equal document ISAs | `spanf1.c:168-179` |
| Is the `homedoc` retrieval filter active? | **No** — `findcbcinarea2d` crashes if `infoptr != NULL` | `retrie.c:244-251` |

**Bottom line:** The spanfilade records one node per `(document, I-range)` pair. Two documents mapping to the same I-range produce two separate, homedoc-distinguished nodes. But both nodes look identical in type — neither is marked as "original creator." Creation provenance lives in the granfilade hint, not in the V→I mapping. At the spanfilade storage level, all V→I references to a shared I-address range are structurally indistinguishable from one another.
