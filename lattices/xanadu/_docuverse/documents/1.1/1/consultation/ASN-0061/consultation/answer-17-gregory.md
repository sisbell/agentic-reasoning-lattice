## Question 17 [gregory]

> When DELETE removes a V-span that was previously the target of a transclusion (shared I-addresses with another document), do the now-orphaned DOCISPAN entries in the spanfilade cause `find_documents_containing` to falsely report that the deleted-from document still contains that content?

## KB Synthesis

Yes — this is a confirmed, permanent behavior. The relevant KB entries converge on a clear picture.

## What Happens

**DELETE does not touch the spanfilade.** `dodeletevspan` → `deletevspanpm` → `deletend` modifies only the document's POOM (the V-to-I mapping). There is no call to any spanf removal function — none exists [ST-DELETE, Finding 0057].

**The spanfilade is write-only.** Inspection of `spanf1.c` and `spanf2.c` reveals only insertion and query functions. No `deletespanf` exists anywhere in the codebase [INV-SPANF-WRITE-ONLY].

**Consequence:** After DELETE removes a V-span from document D, the DOCISPAN entries that were created when that content was originally placed (via INSERT or COPY) persist indefinitely in the spanfilade, asserting that D contains those I-addresses. `FINDDOCSCONTAINING` queries the spanfilade directly and returns D in its results — even though D's POOM no longer maps those I-addresses to any V-position [EC-STALE-SPANF-REFERENCE, INV-IADDRESS-PERMANENT].

This applies equally whether the content was transcluded (shared I-addresses with another document) or not — the DOCISPAN entry records `D` as a containing document regardless of where the I-addresses originated.

## The Formal Characterization

The invariant is asymmetric [INT-DELETE-SPANF-DIVERGENCE]:

```
∀ D, i: (∃ v : poom.D(v) = i) ⟹ i ∈ spanf_index(D)
```

But the converse **does not hold** after DELETE:

```
i ∈ spanf_index(D) ⇏ ∃ v : poom.D(v) = i
```

So `find_documents(i)` returns a **superset** of actual containing documents:

```
actual_docs(i) ⊆ find_documents(i)
```

## The "Correction" Mechanism

The I-to-V conversion layer [INV-ITOV-FILTERING] silently drops unreferenced I-addresses when converting results back to V-addresses — `span2spanset` returns NULL for I-addresses with no POOM mapping, which are silently excluded. But this filtering only applies when a caller subsequently tries to resolve V-positions from the result. The `find_documents_containing` result itself is unfiltered.

## One Nuance: Transclusion Context

For the specific transclusion scenario you describe: if D transcluded content from source S (sharing I-addresses), and D then deletes that content, the DOCISPAN entry for D persists. Searching those I-addresses returns both S (which still has them in its POOM) and D (stale). Finding 0018 [FC-CONTENT-SPANF-ISOLATION] confirms this: "The spanf index retains the I-address mapping even after deletion from a document's V-stream" — even for the deleted-from document itself.

There is no reference counting, no cleanup mechanism, and no tombstone. The stale entry is permanent [INV-SPANF-WRITE-ONLY].

---

## Code Exploration

This has been thoroughly documented already. Here is the complete answer:

---

## Answer

**Yes, stale DOCISPAN entries in the spanfilade cause `find_documents_containing` to falsely report deleted-from documents.** This is a confirmed architectural property, documented in Findings 0057 and 0023.

---

### The Write Path (COPY → INSERT)

`docopy` in `do1.c:45-65` writes to **two** independent structures:

```c
// do1.c:60-62
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

1. **`insertpm`** — writes the V→I mapping into the document's POOM (in `granf`)
2. **`insertspanf`** — writes a DOCISPAN record into the global `spanf`, indexing the document as containing those I-addresses

`insertspanf` in `spanf1.c:15-54` encodes the ORGLRANGE key as `prefix(docisa, DOCISPAN)` and the SPANRANGE key as the I-address. This is an independent, global index entry.

---

### The Delete Path (DELETE)

`dodeletevspan` in `do1.c:158-167`:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  return (
     findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
  /*&& TRUE*/ /* ht stuff */ );
}
```

`deletevspanpm` in `orglinks.c:145-152`:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
  if (iszerotumbler(&vspanptr->width))
    return (FALSE);
  deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
  logbertmodified(docisaptr, user);
  return (TRUE);
}
```

`deletend` operates only on `docorgl` — the document's POOM node in `granf`. The global `spanf` is never touched. **There is no call to remove the DOCISPAN entry.**

---

### No Delete Function Exists for Spanf

A search across all `backend/*.c` confirms: there is no `deletespanf`, no `removespanf`, and no call to `deletend` on `spanf` anywhere in the codebase. The spanfilade is **write-only** — `spanf1.c` and `spanf2.c` implement only insertion and querying:

- `insertspanf` — ✅ exists
- `finddocscontainingsp` — ✅ exists
- `deletespanf` — ❌ does not exist

---

### How `find_documents_containing` Queries

`finddocscontainingsp` in `spanf1.c:151-188`:

```c
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                  ispanset, SPANRANGE, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
        // ... return docid
    }
}
```

It queries `spanf` using the DOCISPAN subspace as the ORGLRANGE filter and the query I-span as the SPANRANGE restriction. It returns every document ISA found in matching spanfilade crums. Since those crums are never removed, the deleted-from document returns every time.

---

### The Asymmetry, Summarized

| Operation | Granf (POOM) | Spanf (DOCISPAN) |
|-----------|-------------|-------------------|
| **COPY** (transclusion) | `insertpm` adds V→I | `insertspanf` adds I→docISA |
| **DELETE** | `deletend` removes V→I | ❌ Nothing |

---

### Observable Behavior

After `DELETE`:

1. The POOM for the deleted-from document has no V-address mapping to the transcluded I-addresses. `retrieve_contents` returns nothing for those addresses.
2. The spanfilade still has the DOCISPAN entry: `(docISA at DOCISPAN offset) → I-addresses`.
3. `find_documents_containing` returns the deleted-from document. The result is a **false positive** — the document is reported as containing content whose V→I mapping no longer exists.
4. Filtering is only possible post-hoc by attempting V-conversion (Finding 0048): a caller who tries to resolve the returned docISA's V-addresses will get empty results.

---

### Architectural Interpretation

This is consistent across all spanfilade indexing: link deletion also leaves stale entries (Finding 0024). The spanfilade acts as a **historical journal** — it records "this document has ever contained this I-address" — not a **current index**. Whether this is intentional (permanent-record philosophy aligned with the permascroll) or a missing feature (no `deletend`-for-SPAN implementation was ever written) cannot be determined from the code alone. The code comment `/* ht stuff */` at `do1.c:166` suggests delete was also meant to have additional work that was never completed.
