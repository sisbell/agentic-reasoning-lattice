## Question 2 [evidence]

> Do udanax-green operations (e.g. INSERT/DELETE/REARRANGE) ever emit more than one link into the spanf store within a single user-level operation, or does each operation touch the link store at most once?

## KB Synthesis

## Spanf Writes Per User-Level Operation

The spanf (span enfilade) has two distinct sub-indices: **DOCISPAN** (content reverse-index) and **link endpoint entries** (LINKFROMSPAN / LINKTOSPAN / LINKTHREESPAN). The answer differs sharply by operation.

---

### Content Operations (INSERT / DELETE / REARRANGE)

**INSERT** always emits exactly **one** DOCISPAN entry per call. `doinsert` → `docopy` → `insertspanf(..., DOCISPAN)` passes a single contiguous I-span (fresh allocation is always contiguous) to `insertspanf`, which makes one `insertnd` call [SS-DOCISPAN, ST-INSERT Finding 0047]. No link endpoint entries are written. Zero link-tracking writes.

**DELETE** writes **nothing** to the spanf. `dodeletevspan` → `deletevspanpm` → `deletend` operates exclusively on the document's POOM in the granfilade. There is no call to any spanf function [ST-DELETE Finding 0057, INV-SPANF-WRITE-ONLY].

**REARRANGE** writes **nothing** to the spanf. It only modifies V-address displacements in POOM crums via `tumbleradd` [ST-REARRANGE Finding 0056, FC-CONTENT-SPANF-ISOLATION].

---

### COPY / VCOPY — Multiple DOCISPAN entries possible

COPY breaks the "at most once" pattern for content operations. `docopy` → `insertspanf` loops over the source `ispanset` and makes **one `insertnd` call per I-span** [SS-DOCISPAN Finding 0047]. If the source content is fragmented (e.g., transcluded from three different origins), a single COPY emits three DOCISPAN entries:

> "COPY of fragmented source content (e.g., 3 non-contiguous regions) creates 3 DOCISPAN entries." [ST-COPY Finding 0047]

Still no link endpoint entries.

---

### CREATELINK — Always emits multiple spanf entries

CREATELINK is the only operation that writes **link endpoint entries** to the spanf, and it always writes more than one. `docreatelink` performs three steps [ST-CREATE-LINK Finding 0012]:

1. Calls `docopy` to store the link ISA in the document's 2.x subspace → **1 DOCISPAN entry** (via the same `insertspanf(..., DOCISPAN)` path)
2. Calls `insertendsetsinspanf()` for from-endpoint → **≥1 LINKFROMSPAN entry**
3. Calls `insertendsetsinspanf()` for to-endpoint → **≥1 LINKTOSPAN entry**
4. Optionally: three-endpoint → **≥1 LINKTHREESPAN entry**

Each endpoint call iterates over its sporglset, writing one `insertnd` per I-span [INT-SPORGL-LINK-INDEX Finding 0013]. If a V-span covers content transcluded from N sources, it produces N sporgls, thus N spanf entries for that endpoint [ST-LINK-CREATE Finding 0037]. A single CREATELINK on transcluded content can therefore emit substantially more than three spanf writes.

---

### Summary

| Operation | DOCISPAN writes | Link endpoint writes |
|-----------|----------------|----------------------|
| INSERT | exactly 1 | 0 |
| DELETE | 0 | 0 |
| REARRANGE | 0 | 0 |
| COPY/VCOPY | 1 per I-span in source (≥1) | 0 |
| CREATELINK | 1 (for link ref in 2.x) | ≥2 (from + to), potentially many more |

The content operations INSERT/DELETE/REARRANGE touch the spanf **at most once** (INSERT) or **not at all** (DELETE, REARRANGE). CREATELINK is the only user-level operation that emits link endpoint entries, and it always emits multiple — minimum three total spanf writes (DOCISPAN + LINKFROMSPAN + LINKTOSPAN), more when endpoints span multiple I-address regions.

---

## Code Exploration

I now have all the information needed. Here is the full answer:

---

## Do udanax-green operations ever emit more than one entry into the spanf store per user-level operation?

**Short answer:** It depends on the operation. INSERT/COPY write to the spanf exactly once per call (though `insertspanf`'s internal loop can produce multiple crums). DELETE and REARRANGE do not touch the spanf at all. CREATELINK is the outlier — it calls `insertspanf` **three or four times** in a single operation.

---

### Tracing Each Operation

#### INSERT → `doinsert` [do1.c:87–123]

```
doinsert
  → inserttextingranf(granf, ..., &ispanset)      # writes text to granfilade only
  → docopy(docisaptr, vsaptr, ispanset)            # do1.c:119
      → insertpm(...)                              # writes to POOM (doc enfilade)
      → insertspanf(spanf, docisaptr, ispanset, DOCISPAN)  # do1.c:62 — ONE call
```

`insertspanf` is called **exactly once** from `docopy` [do1.c:62]. Its internal loop at [spanf1.c:25] calls `insertnd` once per item in `sporglset` — so if `ispanset` is multi-span, multiple crums are written in that single call. But there is only one `insertspanf` invocation.

`inserttextingranf` → `inserttextgr` [granf2.c:83] writes only to the granfilade (calls `insertseq`, not `insertnd` on spanf), so the granf path is spanf-clean.

#### COPY → `docopy` [do1.c:45–65]

Same path as INSERT's inner call. One `insertspanf` invocation [do1.c:62].

#### DELETE → `dodeletevspan` [do1.c:158–167]

```
dodeletevspan
  → findorgl(granf, ...)
  → deletevspanpm(docisaptr, docorgl, vspanptr)   # orglinks.c:145
      → deletend((typecuc*)docorgl, ...)           # operates on POOM only
      → logbertmodified(...)
```

`deletevspanpm` [orglinks.c:145–152] calls only `deletend` (on the POOM enfilade) and `logbertmodified`. **No `insertspanf` call.** DELETE never touches the spanf.

#### REARRANGE → `dorearrange` [do1.c:34–43]

```
dorearrange
  → findorgl(granf, ...)
  → rearrangepm(docisaptr, docorgl, cutseqptr)    # orglinks.c:137
      → rearrangend((typecuc*)docorgl, cutseqptr, V)
      → logbertmodified(...)
```

`rearrangepm` [orglinks.c:137–142] calls only `rearrangend` (POOM) and `logbertmodified`. **No `insertspanf` call.** REARRANGE never touches the spanf.

#### CREATELINK → `docreatelink` [do1.c:195–221]

```
docreatelink
  → createorglingranf(granf, ...)           # allocate new link orgl
  → tumbler2spanset(linkisaptr, &ispanset)
  → findnextlinkvsa(...)
  → docopy(docisaptr, &linkvsa, ispanset)   # do1.c:212
      → insertspanf(..., DOCISPAN)          # do1.c:62 — call #1
  → findorgl(granf, linkisaptr, ...)
  → specset2sporglset(fromspecset, ...)
  → specset2sporglset(tospecset, ...)
  → specset2sporglset(threespecset, ...)
  → setlinkvsas(...)
  → insertendsetsinorgl(...)               # writes to link POOM
  → insertendsetsinspanf(spanf, linkisaptr, from, to, three)  # do1.c:219
      → insertspanf(..., fromsporglset, LINKFROMSPAN)  # do2.c:119 — call #2
      → insertspanf(..., tosporglset,   LINKTOSPAN)    # do2.c:120 — call #3
      → insertspanf(..., threesporglset, LINKTHREESPAN) # do2.c:123 — call #4 (if threesporglset != NULL)
```

`insertendsetsinspanf` [do2.c:116–128]:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
    typesporglset fromsporglset, typesporglset tosporglset, typesporglset threesporglset)
{
    if (!(
        insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)   // do2.c:119
        &&insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))   // do2.c:120
        return (FALSE);
    if (threesporglset) {
        if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN)){  // do2.c:123
            return (FALSE);
        }
    }
    return(TRUE);
}
```

CREATELINK is the only user-level operation that calls `insertspanf` more than once. It calls it **3 times** (4 if a three-end specset is provided): once via `docopy` for the link's own document-space entry (DOCISPAN), then once each for LINKFROMSPAN, LINKTOSPAN, and optionally LINKTHREESPAN.

---

### Summary Table

| Operation   | `insertspanf` invocations | `insertnd` calls in spanf | Notes |
|-------------|--------------------------|---------------------------|-------|
| INSERT      | 1 (DOCISPAN)             | 1 per ispan in set        | [do1.c:62] via docopy |
| COPY        | 1 (DOCISPAN)             | 1 per ispan in set        | [do1.c:62] |
| DELETE      | 0                        | 0                         | [orglinks.c:149] POOM only |
| REARRANGE   | 0                        | 0                         | [orglinks.c:139] POOM only |
| CREATELINK  | 3–4                      | multiple                  | [do1.c:212,219] + [do2.c:119,120,123] |

---

### Key Detail: Multi-crum writes within a single `insertspanf` call

Even a single `insertspanf` call is not necessarily a single write. The loop at [spanf1.c:25–52]:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    ...
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
```

iterates over each item in `sporglset` and calls `insertnd` once per item. For a multi-span ispan set (e.g., a copy across discontiguous content), this produces multiple crum insertions per `insertspanf` call.

---

### Conclusion

- **INSERT, DELETE, REARRANGE** each touch the spanf store at most once (`insertspanf` called once for INSERT/COPY, zero times for DELETE/REARRANGE).
- **CREATELINK** is the outlier: it calls `insertspanf` three to four times per user-level operation — once for document space (DOCISPAN) and once per link endpoint type (FROM, TO, optionally THREE).
- Within any single `insertspanf` call, the number of actual `insertnd` writes to the spanf tree equals the number of items in the `sporglset` argument.
