## Question 7 [evidence]

> Does the udanax-green implementation of the operations corresponding to K.μ⁺ (content arrangement extension), K.μ⁻ (arrangement contraction), and K.ρ (provenance recording) leave the link store unmodified across each operation's execution?

## KB Synthesis

## Link Store Frame Conditions for K.μ⁺, K.μ⁻, and K.ρ

**Yes — all three operations leave the link store unmodified**, with one precision required about what constitutes the "link store" versus the DOCISPAN sub-index.

---

### What counts as the link store

The link store in udanax-green has two physical components:

1. **Link orgls in granf** — permanent link objects at their I-addresses
2. **Link index in spanf** — entries mapping content I-addresses → link ISAs (queried by `find_links`)

The spanfilade also contains a third, distinct component:

3. **DOCISPAN in spanf** — entries mapping content I-addresses → document ISAs (queried by `find_documents`)

DOCISPAN is provenance recording, not link storage. The distinction is critical for K.ρ.

---

### K.μ⁺ — content arrangement extension (INSERT / VCOPY)

INSERT and VCOPY leave both link orgls and the link index unmodified.

INSERT writes to:
- **granf**: fresh I-addresses allocated, document POOM updated [ST-INSERT]
- **spanf.docispan**: one DOCISPAN entry per new I-span [FC-CONTENT-SPANF-ISOLATION, ST-INSERT]

It does **not** touch `spanf.link_index` or any link orgl. The refined frame condition is explicit: `spanf.link_index' = spanf.link_index` [FC-CONTENT-SPANF-ISOLATION]. Existing links are never invalidated — `forall L :: INSERT does not modify L.from_iaddr or L.to_iaddr` [INT-LINK-INSERT]. All pre-existing V→I mappings outside the target document are unchanged [FC-INSERT-IADDR].

---

### K.μ⁻ — arrangement contraction (DELETE)

DELETE leaves the **entire spanfilade** — both link index and DOCISPAN — unmodified.

`dodeletevspan` → `deletevspanpm` → `deletend` touches only the document's POOM in granf, plus `logbertmodified`. There is no call to any spanf function [ST-DELETE, Finding 0057]. The spanfilade continues to assert that the document contains I-addresses that the POOM no longer maps — permanent stale entries. No `deletespanf` function exists anywhere in the codebase [INV-SPANF-WRITE-ONLY].

The frame condition is categorical: `delete(D, vspan) ⟹ spanf_entries_after = spanf_entries_before` [ST-DELETE]. Link objects, their endpoint specifications, and their I-stream addresses are all preserved [FC-LINK-DELETE-ISOLATION].

---

### K.ρ — provenance recording (DOCISPAN insertion)

K.ρ writes to `spanf.docispan` only — the link index portion of the spanfilade is untouched.

DOCISPAN insertion is the final step of `docopy` → `insertspanf(..., DOCISPAN)`, recording which I-address ranges are now present in a document. This writes to the document-discovery sub-index. The link discovery sub-index (entries of the form `I-address → link ISA`) is written only by `insertendsetsinspanf` during `CREATELINK` [ST-CREATE-LINK, FC-CONTENT-SPANF-ISOLATION].

The two spanfilade sub-indexes are structurally separate, addressed via different ORGLRANGE prefixes [SS-RETRIEVE-ENDSETS, Finding 0035].

---

### Summary table

| Operation | Link orgls (granf) | spanf.link_index | spanf.docispan | POOM |
|-----------|-------------------|------------------|----------------|------|
| K.μ⁺ (INSERT) | unchanged | **unchanged** | modified | modified |
| K.μ⁻ (DELETE) | unchanged | **unchanged** | unchanged | modified |
| K.ρ (DOCISPAN) | unchanged | **unchanged** | modified | unchanged |

The link store (link orgls + link index) is a frame-condition invariant across all three operations. Only `CREATELINK` — a distinct fourth operation — writes to the link index [SS-GRANF-OPERATIONS, FC-CONTENT-SPANF-ISOLATION].

---

## Code Exploration

## Answer: Link Store Invariance Across K.μ⁺, K.μ⁻, and K.ρ

**Yes — the link store remains unmodified across all three operations.** Here is the full code trace.

---

### Terminology

The "link store" in udanax-green is the **spanfilade** (`spanf`) indexed with link-type span identifiers: `LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN`. These are distinct from `DOCISPAN` (provenance). The permutation matrix (`docorgl`) is a separate structure tracking content placement.

---

### K.μ⁺ — Content Arrangement Extension (Insert)

**Entry:** `backend/fns.c:84-98` — `void insert()` → calls `doinsert()`

**Core:** `backend/do1.c:87-123` — `bool doinsert()`

```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
  && docopy (taskptr, docisaptr, vsaptr, ispanset)
```

Two writes occur:

1. **`inserttextingranf()`** (`backend/granf2.c:83-109`) — writes text bytes into the granfilade content store. This is raw character storage, not links.

2. **`docopy()`** (`backend/do1.c:45-65`) — writes to the permutation matrix (dimension `V`) via `insertpm()`, and writes provenance metadata to spanfilade via `insertspanf(..., DOCISPAN)`. See below.

Neither path reaches `insertendsetsinspanf()` or any call using `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN`.

**Link store: unmodified.**

---

### K.μ⁻ — Arrangement Contraction (Delete)

**Entry:** `backend/fns.c:333-347` — `void deletevspan()` → calls `dodeletevspan()`

**Core:** `backend/do1.c:158-167` — `bool dodeletevspan()`

```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
);
```

**`deletevspanpm()`** at `backend/orglinks.c:145-152`:

```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

`deletend()` is called on `docorgl` (the permutation matrix) with index `V` (content/V-space). This removes a content placement record — it does not touch `spanf` at all.

No call to `insertendsetsinspanf()`, no call to `insertspanf()` with any link span type.

**Link store: unmodified.**

---

### K.ρ — Provenance Recording (Copy)

**Entry:** `backend/fns.c:35-47` — `void copy()` → calls `docopy()`

**Core:** `backend/do1.c:45-65` — `bool docopy()`

```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa (vsaptr, docorgl)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
);
```

Two writes occur:

1. **`insertpm()`** (`backend/orglinks.c:75-134`) — inserts into the permutation matrix with dimension `V` (`insertnd(..., V)` at line 130). This records where in V-space the copied content lands.

2. **`insertspanf(..., DOCISPAN)`** (`backend/spanf1.c:15-54`) — writes to `spanf`, but with span type `DOCISPAN`. Inside `insertspanf()`:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
/* ... */
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

The `spantype` parameter becomes part of the ORGL-range key, meaning `DOCISPAN` entries are stored at a distinct address from link entries. This is provenance metadata (which source documents contributed content), not link topology.

**Link span types** (`LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN`) are never passed into `insertspanf()` from `docopy()`.

**Link store: unmodified.**

---

### Confirmation: What Does Modify the Link Store

The only path that writes link entries is `insertendsetsinspanf()` at `backend/do2.c:116-128`:

```c
insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
  && insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)
```

This function is called exclusively from:
- `domakelink()` — `backend/do1.c:169-193`
- `docreatelink()` — `backend/do1.c:195-221`

Neither `doinsert`, `dodeletevspan`, nor `docopy` calls `domakelink()` or `docreatelink()`, and neither calls `insertendsetsinspanf()` directly.

---

### Summary Table

| Operation | Symbol | Granfilade Content | Permutation Matrix | Spanfilade DOCISPAN | Link Store |
|-----------|--------|-------------------|-------------------|---------------------|------------|
| `doinsert` | K.μ⁺ | ✓ writes text | ✓ writes V | — | **✗ none** |
| `dodeletevspan` | K.μ⁻ | — | ✓ deletes V | — | **✗ none** |
| `docopy` | K.ρ | — | ✓ writes V | ✓ writes DOCISPAN | **✗ none** |
| `docreatelink` | createlink | — | ✓ writes link orgl | — | **✓ writes LINKFROMSPAN/LINKTOSPAN** |

The architectural invariant holds: K.μ⁺, K.μ⁻, and K.ρ operate exclusively on the content and provenance structures. Link topology is a separate concern, modified only by explicit link-creation operations.
