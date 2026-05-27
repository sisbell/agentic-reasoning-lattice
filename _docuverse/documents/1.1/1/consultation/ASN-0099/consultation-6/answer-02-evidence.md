## Question 2 [evidence]

> In the udanax-green implementation, do the K.μ⁺ (content extension) and K.μ⁻ (content contraction) code paths ever modify the link store L, or are their state mutations confined strictly to the per-document arrangement M(d)?

## KB Synthesis

**Short answer:** Neither K.μ⁺ nor K.μ⁻ ever modify the link store L. Their mutations are strictly confined elsewhere, with the caveat that K.μ⁺ writes to a *non-link* portion of the spanfilade.

---

## K.μ⁻ (DELETE) — cleanest case

DELETE is completely isolated from L. [ST-DELETE] (Finding 0057) establishes the frame condition explicitly:

> `delete(D, vspan) ⟹ spanf_entries_after = spanf_entries_before`

`dodeletevspan` calls only `deletevspanpm` → `deletend` (POOM surgery in granf) and `logbertmodified`. No spanf function is called anywhere in this path. [INV-SPANF-WRITE-ONLY] (Finding 0057) reinforces this at a system level: no `deletespanf` function exists anywhere in `spanf1.c` or `spanf2.c`. The link orgl in I-space is equally untouched — DELETE frees POOM bottom crums via `disown` + `subtreefree`, not granfilade entries ([ST-DELETE] Finding 0064).

DELETE mutations are confined to M(d) only.

---

## K.μ⁺ (INSERT/VCOPY) — more nuanced

K.μ⁺ does write to the spanfilade, but not to L's link-index component. [FC-CONTENT-SPANF-ISOLATION] (Finding 0036) corrects the naive isolation claim:

> The frame condition must be refined: `spanf.link_index' = spanf.link_index` (link findability unchanged), but `spanf.docispan' ≠ spanf.docispan` (document findability changes).

The call chain is `doinsert` → `inserttextingranf` → `docopy` → `insertpm` + `insertspanf(..., **DOCISPAN**)`. The `DOCISPAN` tag routes the write to the *document-to-content* sub-index (enabling `find_documents` queries), not to the link sub-index (which enables `find_links` queries). These are structurally separate sub-indexes within the spanfilade, as established by [SS-DOCISPAN] and [SS-DUAL-ENFILADE] (Finding 0012).

VCOPY follows the identical path through `docopy` ([ST-VCOPY], Findings 0002, 0046).

---

## What only CREATELINK does

The operations that actually write to L are:

1. **Link orgl in I-space** — only `createorglingranf` via `docreatelink`
2. **Link index in spanf** — only `insertendsetsinspanf` via `docreatelink`

[ST-CREATE-LINK] (Finding 0012) and [INT-LINK-INSERT] (Finding 0063) confirm that content operations and link creation draw from the same monotonic I-address allocator, but content extension (K.μ⁺) writes atoms to granf under a TEXTATOM hint and indexes them under DOCISPAN — never touching the link index entries or link orgls.

---

## Summary

| Operation | M(d) / POOM | Granf content | DOCISPAN (spanf) | Link index (spanf) | Link orgl (I-space) |
|-----------|-------------|---------------|------------------|--------------------|---------------------|
| K.μ⁺ INSERT/VCOPY | Modified | Modified | **Modified** | **Unchanged** | **Unchanged** |
| K.μ⁻ DELETE | Modified | Unchanged | **Unchanged** | **Unchanged** | **Unchanged** |
| CREATELINK (for contrast) | Modified | Modified | Modified | Modified | **Created** |

The link store L — comprising link orgls in I-space and the link-index portion of the spanfilade — is invariant under both K.μ⁺ and K.μ⁻. [FC-CONTENT-SPANF-ISOLATION] captures this as a modular reasoning property: content operations and link search operations can be verified independently.

---

## Code Exploration

I have verified the key claims against actual source. Here is the complete answer.

---

## K.μ⁺/K.μ⁻ and the Link Store: A Source-Level Answer

**The short answer is no.** K.μ⁺ and K.μ⁻ never modify the link store L. Their state mutations are confined strictly to M(d) — the per-document POOM enfilade — plus document-scoped entries in the shared spanfilade. Here is the proof.

---

### K.μ⁺ (Content Extension / `doinsert`)

Entry: `backend/do1.c:87-123`

```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
);
```

`inserttextingranf` allocates content in the granfilade and returns an I-span set — it writes to the content store, not to any link structure.

`docopy` at `do1.c:45-65`:

```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

- `insertpm` (`orglinks.c:75-134`) modifies `docorgl` — the caller's per-document POOM node — exclusively. It calls `insertnd(taskptr, (typecuc*)orgl, ...)` at `orglinks.c:130`, which edits that enfilade node in-place. No link structure is touched.
- `insertspanf` is called with the flag **`DOCISPAN`** (`xanadu.h:39`, value `4`). As confirmed in `spanf1.c:168`, DOCISPAN keys into a distinct region of the spanfilade: `tumblerincrement(&docspace.stream, 0, DOCISPAN, &docspace.stream)`. This records the document's V→I mapping, not link endpoints.

---

### K.μ⁻ (Content Contraction / `dodeletevspan`)

Entry: `backend/do1.c:158-167`

```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
);
```

`deletevspanpm` at `orglinks.c:145-152`:

```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
logbertmodified(docisaptr, user);
return (TRUE);
```

Two calls, nothing more. `deletend` removes the crum from `docorgl` (the per-document enfilade node). `logbertmodified` marks M(d) dirty in the bert table. No spanfilade write occurs at all — there is no `insertspanf` or `insertendsetsinspanf` call anywhere in this path.

---

### The Link Store (L) — How It Actually Gets Written

Link store writes happen only through `insertendsetsinspanf`, defined at `do2.c:116-120`:

```c
bool insertendsetsinspanf(...)
{
    return (
        insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
      &&insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN));
}
```

Checking all call sites for this function:

```
backend/do1.c:191  domakelink    → insertendsetsinspanf(... NULL)
backend/do1.c:219  docreatelink  → insertendsetsinspanf(... threesporglset)
```

Neither `doinsert` nor `dodeletevspan` — nor any function they transitively call — reaches `insertendsetsinspanf`. The call graph is completely disjoint.

The distinguishing constants make the partition explicit (`xanadu.h:36-39`):

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define DOCISPAN        4
```

K.μ⁺ and K.μ⁻ exclusively use `DOCISPAN`. Link-endpoint insertion exclusively uses `LINKFROMSPAN`/`LINKTOSPAN`. These key into different address regions inside the spanfilade, and the code paths that supply each constant never intersect.

---

### Summary

| Operation | Modifies granf | Modifies M(d) via `insertnd`/`deletend` | Writes spanfilade with `DOCISPAN` | Writes L via `LINKFROMSPAN`/`LINKTOSPAN` |
|-----------|---------------|----------------------------------------|-----------------------------------|------------------------------------------|
| K.μ⁺ (`doinsert`) | Yes (allocates text) | Yes (`insertpm` → `insertnd`) | Yes | **Never** |
| K.μ⁻ (`dodeletevspan`) | No | Yes (`deletend`) | No | **Never** |
| `docreatelink` / `domakelink` | Yes (allocates link atom) | Yes (places link ref in doc) | No | **Yes** |

State mutations from K.μ⁺ and K.μ⁻ are strictly confined to the content store and M(d). The link store L is invariant under both operations.
