## Question 15 [gregory]

> If a deeply orphaned link's endpoint I-addresses are transcluded into a brand-new document years later, does `find_links` rediscover the link immediately, or does the stale DOCISPAN entry for the original (now-deleted) document interfere with the lookup?

## KB Synthesis

Yes — `find_links` rediscovers the link immediately, and stale DOCISPAN entries do not interfere. Here is the full chain of reasoning:

---

**Why the link is rediscovered**

When the link was created, `insertendsetsinspanf` permanently indexed α₁..αₙ → link_ISA in the spanfilade's **link endset sub-index** [ST-CREATE-LINK, SS-SPANF-OPERATIONS]. Because the spanfilade is write-only and append-only, these entries survive forever regardless of what happens to the documents referencing those I-addresses [INV-SPANF-WRITE-ONLY].

When D_new transcludes the content via COPY, `insertpm` gives D_new's POOM V→I mappings for α₁..αₙ [ST-VCOPY]. Now `find_links` on D_new works as follows:

1. The search specset is converted to I-addresses via D_new's POOM → yields α₁..αₙ [SS-FIND-LINKS].
2. The spanfilade link endset index is queried for those I-addresses [SS-SPANF-OPERATIONS].
3. The link endset entries α₁..αₙ → link_ISA were never removed → intersection succeeds → link returned.
4. FOLLOWLINK succeeds because D_new's POOM now provides V-position resolution for α₁..αₙ [SS-FOLLOWLINK, INV-ITOV-FILTERING].

This is exactly the mechanism documented in [INT-LINK-TRANSCLUSION]: transclusion enables link discovery by sharing I-addresses, with no special "link recovery" logic required.

---

**Why stale DOCISPAN entries don't interfere**

The spanfilade has two independent sub-indices [FC-CONTENT-SPANF-ISOLATION, SS-DOCISPAN]:

- **Link endset index** (written by `insertendsetsinspanf` at link creation): maps I-addresses → link ISAs. This is what `find_links` / `findlinksfromtothreesp` queries.
- **DOCISPAN index** (written by `insertspanf(..., DOCISPAN)` at INSERT/COPY): maps I-addresses → document ISAs. This is what `FINDDOCSCONTAINING` queries.

`find_links` never touches the DOCISPAN portion [SS-GRANF-OPERATIONS, SS-SPANF-OPERATIONS]. Stale DOCISPAN entries from the original (now-empty) document are only relevant to `FINDDOCSCONTAINING` queries, where they cause the "superset" behavior documented in [EC-STALE-SPANF-REFERENCE] — they would spuriously include the old document in those results, but that is completely orthogonal to link discovery.

---

**One relevant quirk**

From [EC-FIND-LINKS-GLOBAL] (Finding 0069), the orgl-range parameter to `find_links` is effectively disabled — searches are global in the orgl dimension. This is actually favorable here: the link endset entries exist in the global orgl space regardless of which document the link was originally created in, so the disabled filter cannot accidentally exclude the result.

---

## Code Exploration

I now have everything I need for a complete, code-grounded answer.

---

## Answer: Does `find_links` Rediscover an Orphaned Link After Retransclusion?

**Yes — `find_links` rediscovers the link immediately. The stale DOCISPAN entry for the deleted document does not interfere at all.** Here is the complete mechanistic explanation.

---

### How Links Are Indexed at Creation Time

When `docreatelink` [do1.c:195–221] is called, it fires `insertendsetsinspanf` [do2.c:116–128]:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
    typesporglset fromsporglset, typesporglset tosporglset, typesporglset threesporglset)
{
    insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
    && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)
    ...
}
```

`insertspanf` [spanf1.c:15–54] performs a 2D insert into the spanfilade. The two dimensions of each stored crum are:

- **ORGLRANGE dimension**: the link ISA, prefixed with the span-type tag (e.g. `LINKFROMSPAN` = 1).  
  `prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);` [spanf1.c:22]

- **SPANRANGE dimension**: the **raw I-address** of the endpoint content.  
  For a `SPORGLID` (content specified as a document + V-span), the I-address is in `sporglorigin`:  
  `movetumbler(&((typesporgl*)sporglset)->sporglorigin, &lstream);` [spanf1.c:31–32]  
  For an `ISPANID`, the I-address is the stream field directly. [spanf1.c:27–28]

The V→I conversion (for `VSPECID` endpoint specs) happens in `vspanset2sporglset` [sporgl.c:35–65], which calls `vspanset2ispanset` [orglinks.c:397–402] via `permute` to get the absolute I-address at creation time. **Only the I-address is stored in the spanfilade.** The source document ISA is held in `sporgladdress`, but as we will see, it is never used as a filter during lookup.

---

### How `find_links` Searches

The call chain for a `find_links` query:

```
dofindlinksfromtothree       [do1.c:348–353]
  → findlinksfromtothreesp   [spanf1.c:56–103]
    → specset2sporglset       [sporgl.c:14–33]  (convert query specs to sporgls)
    → sporglset2linkset       [sporgl.c:222–237]
      → sporglset2linksetinrange [sporgl.c:239–269]
```

The critical function is `sporglset2linksetinrange` [sporgl.c:239–269]:

```c
int sporglset2linksetinrange(typetask *taskptr, typecuc *spanfptr, typesporglset sporglset,
    typelinkset *linksetptr, typeispan *orglrange, INT spantype)
{
    infoptr = &linfo;
    for (; sporglset; sporglset = ...) {
        if (FALSE/*trying to kluge links followable thru versions */
            && ((typeitemheader *)sporglset)->itemid == SPORGLID) {
            infoptr = &linfo;
            movetumbler(&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
        } else
            infoptr = NULL;   // <-- ALWAYS executes
        ...
        context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                                     &range, ORGLRANGE, (typeisa*)infoptr);
        ...
    }
}
```

The guard `FALSE && ...` at [sporgl.c:251] ensures `infoptr = NULL` on **every single call** — unconditionally. The developer comment is explicit: *"trying to kluge links followable thru versions"*. This was an intentional design decision to make link discovery document-independent.

With `infoptr = NULL`, `retrieverestricted` performs a pure 2D range scan:
- **Query key (SPANRANGE)**: the I-address extracted from the query sporgl (from the new document's content, via V→I conversion).
- **Result key (ORGLRANGE)**: the link ISAs stored at that I-address.

There is **no filtering by source document** anywhere in this path.

---

### What DOCISPAN Entries Are and Why They Don't Matter

DOCISPAN entries are written by `docopy` [do1.c:62] and `docopyinternal` [do1.c:79] every time content is transcluded into a document:

```c
insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // do1.c:62
```

This inserts a crum with:
- ORGLRANGE: `DOCISPAN.documentISA`
- SPANRANGE: I-address of the transcluded content

The purpose is to answer the question: "given an I-span, which documents currently contain it?" The **only** function that reads DOCISPAN entries is `finddocscontainingsp` [spanf1.c:151–188]:

```c
tumblerincrement(&docspace.stream, 0, DOCISPAN, &docspace.stream);  // spanf1.c:168
...
context = retrieverestricted((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, ...);
```

`finddocscontainingsp` is a completely separate operation. It is **never called** from `findlinksfromtothreesp` or anywhere in the link-finding call chain. The two queries live in orthogonal tag-prefixed regions of the ORGLRANGE dimension (DOCISPAN=4 vs. LINKFROMSPAN=1/LINKTOSPAN=2/LINKTHREESPAN=3) and never overlap.

---

### The Scenario, Step by Step

1. **Original link created**: `docreatelink` stores in the spanfilade — SPANRANGE = I-address X, ORGLRANGE = `LINKFROMSPAN.linkISA`. [do1.c:219, spanf1.c:22,49–51]

2. **Original document deleted**: The DOCISPAN entry "I-address X is in document A" remains in the spanfilade. The granfilade orgl for document A may be gone or inaccessible. The LINKFROMSPAN entry for I-address X is **untouched** — there is no garbage-collection step.

3. **Content at I-address X transcluded into new document B**: `docopy` [do1.c:45–65] calls `insertspanf(..., DOCISPAN)` [do1.c:62], writing a new DOCISPAN crum: "I-address X is in document B." The old DOCISPAN entry for document A also remains, but in a different ORGLRANGE slot.

4. **Client calls `find_links` with a VSPECID spec for document B**: `specset2sporglset` [sporgl.c:14–33] calls `vspanset2sporglset` [sporgl.c:35–65], which opens document B's enfilade via `findorgl`, calls `vspanset2ispanset` [orglinks.c:397–402] to map the V-address in B → I-address X, and produces a sporgl with `sporglorigin = X`.

5. **`sporglset2linksetinrange` runs**: `infoptr = NULL` (the `FALSE&&` guard fires) [sporgl.c:254–255]. `retrieverestricted` searches SPANRANGE for I-address X, filtered to ORGLRANGE in the LINKFROMSPAN region. It finds the original link's crum. `beheadtumbler` extracts the link ISA. [sporgl.c:263–265]

6. **Link returned to client.** The stale DOCISPAN entry for document A was never consulted.

---

### Architectural Summary

The spanfilade serves as two independent indexes sharing one data structure, distinguished by the tag prefix in the ORGLRANGE dimension:

| Tag (ORGLRANGE prefix) | Written by | Read by | Meaning |
|---|---|---|---|
| LINKFROMSPAN (1) | `insertendsetsinspanf` | `sporglset2linksetinrange` | I-addr → link ISA (from-end) |
| LINKTOSPAN (2) | `insertendsetsinspanf` | `sporglset2linksetinrange` | I-addr → link ISA (to-end) |
| LINKTHREESPAN (3) | `insertendsetsinspanf` | `sporglset2linksetinrange` | I-addr → link ISA (3-end) |
| DOCISPAN (4) | `docopy` / `docopyinternal` | `finddocscontainingsp` | I-addr → containing document ISA |

These two indexes never cross. Link finding reads only tags 1–3. DOCISPAN entries (stale or fresh) are invisible to it.

The `FALSE&&` at [sporgl.c:251] is the definitive proof that link discovery is intentionally document-blind. The system designers understood that tying link discovery to document membership would break link persistence across versions and transclusions — so they hard-coded the document filter off.

**Conclusion**: The link is rediscovered immediately and completely. The stale DOCISPAN entry for the deleted document sits in a different part of the spanfilade index and is structurally unreachable from the link-finding path. Transclusion's I-address preservation is the mechanism that makes this work: since I-addresses are permanent content identifiers, the LINKFROMSPAN index entry written at link-creation time remains valid and findable as long as any document anywhere contains that content.
