## Question 14 [evidence]

> Does `find_documents_containing` use the spanfilade DOCISPAN entries as its sole source of truth, meaning two documents identified as sharing content may in fact no longer share it after DELETE operations [EC-STALE-SPANFILADE]?

## KB Synthesis

Yes, exactly correct — with one important qualification about how "stale" results are handled.

## DOCISPAN Is the Sole Source of Truth for `find_documents`

`find_documents_containing` (FINDDOCSCONTAINING) queries only the DOCISPAN sub-index in the spanfilade [SS-DOCISPAN]. DELETE operations modify only the POOM enfilade (the document's V→I mapping) and never touch the spanfilade [ST-DELETE, INV-SPANF-WRITE-ONLY]. There is no `deletespanf` function anywhere in the codebase [INV-SPANF-WRITE-ONLY].

This creates a permanent divergence [INT-DELETE-SPANF-DIVERGENCE]:

```
After DELETE(doc, vspan):
  POOM(doc):   V→I mappings removed       ← updated
  spanfilade:  DOCISPAN entries unchanged  ← stale
```

## The Result Is a Superset, Not an Exact Set

`find_documents` returns a **superset** of documents currently containing the queried I-addresses [EC-STALE-SPANF-REFERENCE]:

```
actual_docs(i) ⊆ find_documents(i)
```

The converse does NOT hold. A document returned by `find_documents` may have had that content deleted and its POOM entry removed, while its spanfilade DOCISPAN entry persists indefinitely.

This is confirmed experimentally [EC-STALE-SPANF-REFERENCE]:

```
Source doc S has content at α₁..α₅
Target doc T COPYs → DOCISPAN registers T for α₁..α₅
DELETE from T removes POOM entries
FIND_DOCUMENTS(α₁..α₅) → {S, T}  ← T is stale
I-to-V(α₁, T) → ∅               ← no V-position in T
```

## The System's Defense: Silent I→V Filtering

The I-to-V conversion path (used by FOLLOWLINK, RETRIEVEENDSETS, etc.) silently drops I-addresses that have no current POOM mapping [INV-ITOV-FILTERING]. `span2spanset` calls `retrieverestricted` on the document's POOM; if NULL is returned, the I-address is excluded from the result without error [SS-FOLLOWLINK].

So callers must post-filter `find_documents` results: attempting to resolve the stale reference via I→V conversion yields empty rather than an error — the caller learns the reference is stale only by attempting resolution.

## This Is Permanent and By Design

The monotonicity of the spanfilade [INV-SPANF-WRITE-ONLY]:

```
∀ t₁ < t₂ : spanf_entries(t₁) ⊆ spanf_entries(t₂)
```

This is not a bug — it reflects the Xanadu principle that I-addresses and their provenance associations are permanent. `find_documents` is accurately described as a historical journal of all content placements ever made, not a current-state index [INV-IADDRESS-PERMANENT].

---

## Code Exploration

Finding 0057 and 0023 already document this thoroughly. Here is the complete answer, grounded in the source code.

---

## Answer: [EC-STALE-SPANFILADE] Confirmed

**Yes.** `find_documents_containing` uses spanfilade DOCISPAN entries as its sole source of truth, and those entries are never invalidated by DELETE. Two documents identified by the query as sharing content may no longer share it after a delete.

---

### The Query Path — Spanfilade Only

`finddocscontaining` in `fns.c:20-32` dispatches to:

```
fns.c:21  → getfinddocscontaining
fns.c:28  → dofinddocscontaining  (do1.c:15)
              → specset2ispanset   (do2.c:14) — converts V-spec to I-spans
              → finddocscontainingsp (spanf1.c:151)
```

`finddocscontainingsp` at `spanf1.c:151-188` is the entire query implementation. It:

1. Constructs a search window in DOCISPAN space [spanf1.c:167-169]:
   ```c
   tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
   tumblerincrement (&docspace.width, 0, 1, &docspace.width);
   ```

2. For each I-span, calls `retrieverestricted` directly on the spanfilade (`spanf`) [spanf1.c:171]:
   ```c
   context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                  ispanset, SPANRANGE, (typeisa*)NULL);
   ```

3. Extracts document IDs from the context and returns them [spanf1.c:173-180]. **No step** cross-checks these IDs against the current granfilade state. The returned documents are exactly whatever the spanfilade says.

---

### The Write Path — DOCISPAN Written on COPY Only

DOCISPAN entries are created by `docopy` in `do1.c:45-65`:

```c
/* do1.c:60 */  && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
/* do1.c:62 */  &&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

`insertspanf` at `spanf1.c:15-54` encodes the document address at `DOCISPAN` position in the spanfilade for each I-span in the transcluded set. Both `doinsert` (`do1.c:118-122`) and `docopyinternal` (`do1.c:79`) do the same.

---

### The Delete Path — Spanfilade Never Updated

`dodeletevspan` at `do1.c:158-167`:

```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
/*&& TRUE*/ /* ht stuff */ );
```

`deletevspanpm` at `orglinks.c:145-152`:

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

`deletend` (called at `orglinks.c:149`) operates on `docorgl` — the document's POOM node in the granfilade. It removes the V→I mapping there. **There is no call to touch the spanfilade.** The DOCISPAN entry for this document and these I-addresses remains.

---

### No Spanfilade Delete Function Exists

A grep for `deletespanf`, `removespanf`, and `delete.*spanf` across the entire backend returns **no matches**. The spanfilade module (`spanf1.c`, `spanf2.c`) provides:

- `insertspanf` — adds entries [spanf1.c:15]
- `finddocscontainingsp` — queries DOCISPAN entries [spanf1.c:151]
- `findlinksfromtothreesp` — queries link entries [spanf1.c:56]
- `retrieveendsetsfromspanf` — retrieves endsets [spanf1.c:190]
- `retrievesporglsetinrange` — retrieves sporgl sets [spanf1.c:237]

**No removal function of any kind.** The spanfilade is structurally write-only.

---

### Direct Answer to [EC-STALE-SPANFILADE]

Yes, the concern is confirmed by the code. The mechanism is:

1. **Document A** transcluded content from I-addresses `x..y` → `docopy` wrote `insertspanf(..., DOCISPAN)` registering docA as containing `x..y` [do1.c:62].
2. **Document B** also transcluded from `x..y` — same write.
3. `find_documents_containing(x..y)` queries `retrieverestricted` on `spanf` at DOCISPAN [spanf1.c:168-171] and sees both docA and docB.
4. **Document A** later deleted that content — `deletevspanpm` removed the V→I mapping from docA's POOM [orglinks.c:149], but the spanfilade DOCISPAN entry for docA was **not touched**.
5. Subsequent `find_documents_containing(x..y)` still returns **[docA, docB]**, even though docA no longer contains that content.

The two documents "identified as sharing content" by the query may thus be in a state where one (or both) have had that content deleted. The query result is a **historical inclusion index** — documents that ever contained those I-addresses — not a **current containment index**.

This is documented in **Finding 0057** (code analysis) and **Finding 0023** (golden test evidence confirming the behavior at runtime).
