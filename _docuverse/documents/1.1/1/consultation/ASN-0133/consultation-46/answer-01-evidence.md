## Question 1 [evidence]

> Does every primitive substrate step (`K.σ`, `K.α`, `K.λ_sh`) strictly grow one of `dom(Σ.M)`, `dom(Σ.C)`, `dom(Σ.L)` — i.e., is there no domain-preserving primitive step (the substrate strictly monotone/append-only) — and do content (`K.α`) deposits grow `dom(Σ.C)` alone?

## KB Synthesis

## Substrate Monotonicity Analysis

### `K.α` (content atom deposit): YES, strictly grows `dom(Σ.C)` alone

`inserttextingranf` allocates fresh I-addresses in the granfilade and writes bytes there. This is the only mechanism that extends `dom(Σ.C)`. [INV-IADDR-IMMUTABILITY] confirms once-allocated I-addresses are permanent — no operation removes them. [FC-GRANF-ON-DELETE] confirms DELETE and REARRANGE leave the granfilade entirely untouched. [SS-GRAN-MB-ONE, FC-GRANF-ON-VERSION] confirm VERSION does not call any content allocation. The step is isolated: `insertpm` (Σ.M) and `insertspanf` (Σ.L) are separate downstream primitives that don't execute inside `inserttextingranf`.

One qualification: CREATELINK's `createorglingranf` call also allocates in the granfilade [ST-INSERT, Finding 0063]. If `K.α` is defined as the granfilade-allocation primitive regardless of entity type (text atom or link orgl), it still grows `dom(Σ.C)` alone — the DOCISPAN insertion is a distinct `K.λ_sh` step.

---

### `K.λ_sh` (spanfilade insert): YES, strictly grows `dom(Σ.L)` alone

`insertspanf` / `insertendsetsinspanf` append entries to the spanfilade. [INV-SPANF-WRITE-ONLY] establishes that no delete function exists anywhere in `spanf1.c` or `spanf2.c` — the spanfilade is write-only. [FC-CONTENT-SPANF-ISOLATION] confirms this step does not touch `dom(Σ.C)` or `dom(Σ.M)`. [ST-DELETE, Finding 0057] confirms DELETE never calls any spanf removal function, so stale entries persist permanently.

---

### `K.σ` (POOM step): NO — not uniformly domain-growing; domain-preserving steps exist

The POOM is the sole mutable layer [SS-POOM-MUTABILITY], and it admits three qualitatively distinct primitive behaviors:

**1. Addition sub-step (INSERT's new-entry path in `insertpm`)**
Creates a new bottom crum mapping a fresh V-position to the just-allocated I-address. This strictly grows `dom(Σ.M)`. [ST-INSERT, Finding 0062]

**2. Shift sub-step (INSERT's `insertcutsectionnd` path in `makegappm`)**
Adds the insertion width to the V-displacement of existing POOM entries falling within `[blade[0], blade[1])`. [SS-TWO-BLADE-KNIFE, Finding 0054] The domain `dom(Σ.M)` is unchanged — same entries, modified V-displacement values. This is a **domain-preserving primitive step**, directly contradicting the claim that no such step exists.

REARRANGE (`rearrangend`) applies pure tumbler-displacement arithmetic to existing entries without adding or removing any [ST-REARRANGE, Finding 0056]. It is likewise domain-preserving on `dom(Σ.M)`.

**3. Removal sub-step (DELETE's `deletend`)**
`disown` + `subtreefree` removes bottom crums from the POOM tree [ST-DELETE, Finding 0064]. This **shrinks** `dom(Σ.M)`. The entries are not shifted to invalid positions under cross-subspace conditions (the `strongsub` exponent guard prevents that [SS-TUMBLER, Finding 0055]); they are physically freed.

---

### Summary

| Step | `dom(Σ.C)` | `dom(Σ.M)` | `dom(Σ.L)` | Strictly grows one domain? |
|------|-----------|-----------|-----------|---------------------------|
| `K.α` (granfilade alloc) | +grows | unchanged | unchanged | **YES** |
| `K.λ_sh` (spanfilade insert) | unchanged | unchanged | +grows | **YES** |
| `K.σ` add sub-step | unchanged | +grows | unchanged | YES (this sub-step) |
| `K.σ` shift sub-step | unchanged | ≡preserved | unchanged | **NO** — domain-preserving |
| `K.σ` remove sub-step | unchanged | −shrinks | unchanged | **NO** — domain-shrinking |

The answer to the compound question: `K.α` and `K.λ_sh` are strictly monotone on exactly their respective domains. `K.σ` is **not** uniformly monotone — the shift and rearrange sub-steps are domain-preserving on `dom(Σ.M)`, and the delete sub-step shrinks it. The claim of no domain-preserving primitive step fails because `makegappm`'s shift pass and `rearrangend`'s displacement pass both leave `|dom(Σ.M)|` unchanged. `K.α` deposits do grow `dom(Σ.C)` alone. [SS-POOM-MUTABILITY, FC-GRANF-ON-DELETE, INV-SPANF-WRITE-ONLY, SS-TWO-BLADE-KNIFE, ST-DELETE]

---

## Code Exploration

I now have everything needed for a complete answer. Here it is.

---

## Answer

**In brief:** Yes on all three counts. Each of the named primitives strictly grows exactly one domain; there is no domain-preserving step among them; and `K.α` (content deposit) grows `dom(Σ.C)` alone. The substrate is strictly append-only at the granfilade level — `dom(Σ.M)`, `dom(Σ.C)`, and `dom(Σ.L)` are never shrunk by any primitive step.

---

### Domain Identification in the Code

Three disjoint domain sets map directly onto the granfilade entry type and hint:

| Formal domain | Granfilade infotype | Hint atomtype | Code label |
|---|---|---|---|
| `dom(Σ.M)` | `GRANORGL` | `DOCUMENT`, `ACCOUNT`, `NODE` | molecule ISAs |
| `dom(Σ.C)` | `GRANTEXT` | `TEXTATOM` | permascroll (I-space) |
| `dom(Σ.L)` | `GRANORGL` | `LINKATOM` | link molecule ISAs |

The constants are declared in `xanadu.h:140-145`:

```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
#define TEXTATOM  1
#define LINKATOM  2
```

The two `GRANORGL` entry types (`DOCUMENT`-family vs `LINKATOM`) are distinguished at allocation time by the `typehint.atomtype` field, which is baked in by `makehint` [do2.c:78-84] before being handed to `findisatoinsertgr` [granf2.c:130-156].

---

### `K.σ` — Molecule Creation (`docreatenewdocument`)

**Entry point:** `createnewdocument` [fns.c:276-286] → `docreatenewdocument` [do1.c:234-241]

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr) {
    makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf(taskptr, granf, &hint, isaptr));
}
```

Call chain: `createorglingranf` [granf1.c:50-54] → `createorglgr` [granf2.c:111-128]:

```c
bool createorglgr(...) {
    if (!findisatoinsertgr((typecuc*)fullcrumptr, hintptr, isaptr))
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf(POOM);
    // ...
    insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);   // ← only mutation
    return (TRUE);
}
```

**`findisatoinsertgr`** [granf2.c:130-156] branches on `hintptr->subtype`. For `DOCUMENT` (not `ATOM`), it calls `findisatoinsertnonmolecule` [granf2.c:203-242], which computes the next available ISA under the account by traversing the granfilade with `findpreviousisagr` [granf2.c:255-278] and incrementing.

**Then `insertseq` writes one new `GRANORGL` entry at the fresh ISA.**

No `insertspanf`, no `insertpm`, no `inserttextingranf` is called. The POOM and spanfilade are untouched.

**Effect: `dom(Σ.M)` += {new ISA}. `dom(Σ.C)` and `dom(Σ.L)` are unchanged. `K.σ` strictly grows `dom(Σ.M)` alone.**

---

### `K.α` — Content Deposit (`doinsert` / `inserttextgr`)

**Entry point:** `insert` [fns.c:84-98] → `doinsert` [do1.c:87-123]

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy(taskptr, docisaptr, vsaptr, ispanset));
    return(ret);
}
```

#### Sub-step 1: `inserttextingranf` → `inserttextgr` [granf2.c:83-109]

```c
bool inserttextgr(...) {
    if (!findisatoinsertgr((typecuc*)fullcrumptr, hintptr, &lsa))
        return (FALSE);
    movetumbler(&lsa, &spanorigin);
    for (; textset; textset = textset->next) {
        locinfo.infotype = GRANTEXT;                       // ← content type
        movmem(textset->string, locinfo.granstuff.textstuff.textstring, ...);
        insertseq((typecuc*)fullcrumptr, &lsa, &locinfo); // ← only mutation to granfilade
        tumblerincrement(&lsa, 0, textset->length, &lsa);
    }
    // build ispanset pointing to [spanorigin, lsa)
    return (TRUE);
}
```

Because `hintptr->subtype == ATOM`, `findisatoinsertgr` [granf2.c:134-142] calls `findisatoinsertmolecule` [granf2.c:158-181]:

```c
static int findisatoinsertmolecule(...) {
    tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear(&lowerbound, sizeof(lowerbound));
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    if (hintptr->atomtype == TEXTATOM) {
        tumblerincrement(&lowerbound, 0, 1, isaptr);  // next available I-address
    }
    // ...
}
```

This allocates an ISA in the text-content subspace (`atomtype` 1) beneath the document's ISA. The result is a fresh `GRANTEXT` entry — a new position in the permascroll. This is the only place a new entry enters `dom(Σ.C)`.

**Finding 0061 confirms:** `findpreviousisagr` always queries the live granfilade tree and increments monotonically; deleted I-addresses are never reused because the granfilade has no delete operation.

#### Sub-step 2: `docopy` [do1.c:45-65]

```c
bool docopy(...) {
    return (
       specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa(vsaptr, docorgl)
    && insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)      // POOM update
    && insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)   // spanfilade update
    );
}
```

- **`insertpm`** [orglinks.c:75-134] calls `insertnd` [insertnd.c:15-111] on the document's existing POOM (orgl) to add new V→I mapping crums. This updates internal tree structure of an already-existing molecule; it creates no new molecule ISA in the granfilade.
- **`insertspanf`** [spanf1.c:15-53] calls `insertnd` on the spanfilade with `DOCISPAN = 4`, recording the document-to-content span relationship. No new GRANORGL or GRANTEXT entries are created in the granfilade.
- **`logbertmodified`** [bert.c:97-109] sets a flag in the in-memory bert table; no domain mutation.

**Effect: `dom(Σ.C)` += {new I-span for the text bytes}. `dom(Σ.M)` and `dom(Σ.L)` are unchanged. `K.α` strictly grows `dom(Σ.C)` alone.**

---

### `K.λ_sh` — Link Creation (`docreatelink`)

**Entry point:** `createlink` [fns.c:100-112] → `docreatelink` [do1.c:195-221]

```c
bool docreatelink(..., typeisa *linkisaptr) {
    makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
    return (
         createorglingranf(taskptr, granf, &hint, linkisaptr)         // (1) allocate link ISA
      && tumbler2spanset(taskptr, linkisaptr, &ispanset)              // (2) wrap as ispan
      && findnextlinkvsa(taskptr, docisaptr, &linkvsa)                // (3) find V-address
      && docopy(taskptr, docisaptr, &linkvsa, ispanset)               // (4) V→I in doc POOM
      && findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)  // (5) get link's orgl
      && specset2sporglset(...) && specset2sporglset(...) && specset2sporglset(...)
      && setlinkvsas(&fromvsa, &tovsa, &threevsa)                     // (6) set endpoint V-addrs
      && insertendsetsinorgl(taskptr, linkisaptr, link, ...)          // (7) endpoints in link POOM
      && insertendsetsinspanf(taskptr, spanf, linkisaptr, ...)        // (8) endpoints in spanf
    );
}
```

**Step (1) is the only domain mutation:**

`createorglingranf` calls `createorglgr` [granf2.c:111-128] with `LINKATOM` hint. `findisatoinsertmolecule` computes an ISA in the link subspace (atomtype 2) beneath the owning document. `insertseq` writes a `GRANORGL` entry at that ISA. This is the link's home ISA — a new element of `dom(Σ.L)`.

The link ISA address space is in a distinct tumbler subspace from text-atom addresses (atomtype 1 vs 2), as confirmed by `findisatoinsertmolecule` [granf2.c:168-175]:

```c
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement(&hintptr->hintisa, 2, 2, isaptr);   // link subspace starts at .0.0.2
    if (tumblercmp(&lowerbound, isaptr) == LESS)
        tumblerincrement(isaptr, 1, 1, isaptr);
    else
        tumblerincrement(&lowerbound, 0, 1, isaptr);
}
```

**Steps (2)–(8) are structure/index updates only:**

- **`tumbler2spanset`** [do2.c:48-61]: wraps the link ISA as an ispan in task-local memory; no granfilade write.
- **`findnextlinkvsa`** [do2.c:151-167]: reads the document's current V-span reach to find the next available V-address in link space (≥ 2.1); read-only.
- **`docopy`** [do1.c:45-65]: inserts V→I mapping into the document's POOM (`insertpm`) and records the DOCISPAN relationship in the spanfilade (`insertspanf`). The ispan here is the link's ISA-as-span — no new `GRANTEXT` content is deposited.
- **`insertendsetsinorgl`** [do2.c:130-149] → three calls to `insertpm`: writes from/to/three endpoint V→I mappings into the **link's own POOM** (the orgl allocated in step 1). Modifies internal structure of the new link molecule; no additional ISAs in granfilade.
- **`insertendsetsinspanf`** [do2.c:116-128] → three calls to `insertspanf` with `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`: records endpoint spans in the spanfilade index. No GRANORGL or GRANTEXT entries created.

**Effect: `dom(Σ.L)` += {new link ISA}. `dom(Σ.M)` and `dom(Σ.C)` are unchanged. `K.λ_sh` strictly grows `dom(Σ.L)` alone.**

---

### Is the Substrate Strictly Monotone?

**Yes.** For all three primitives, the allocation mechanism is:

1. `findpreviousisagr` [granf2.c:255-278] traverses the granfilade tree to find the current maximum ISA below the upper-bound
2. Increment by 1 → new ISA
3. `insertseq` writes a new entry at that ISA

No entry is ever removed from the granfilade. There is no `deletetextgr`, no `deleteorglgr`, no mechanism to reclaim or reuse an allocated ISA. Finding 0061 confirms this empirically: interleaved INSERT-DELETE-INSERT sequences show that deleted I-addresses are never reused — the allocation pointer only moves forward.

**`dodeletevspan`** [do1.c:158-167] → `deletevspanpm` [orglinks.c:145-152] → `deletend` on the POOM: this removes V→I *mappings* from the document's orgl, but does not touch the granfilade. The granfilade entry for the deleted content remains permanently. As Finding 0064 states: "V-space is reconstructible; I-space is not."

```c
bool deletevspanpm(...) {
    if (iszerotumbler(&vspanptr->width)) return(FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V); // POOM only
    logbertmodified(docisaptr, user);
    return(TRUE);
}
```

**No call to anything in the granfilade.** `deletend` operates exclusively on the orgl tree.

**The spanfilade is also append-only** (Finding 0057, confirmed in Finding 0067): `insertspanf` is called by every mutating primitive; there is no `deletespanf`. Stale entries accumulate but do not remove domain elements — they are query-index garbage, not domain deletions.

---

### Summary Table

| Primitive | Code entry | Granfilade write | Domain grown | Other writes |
|---|---|---|---|---|
| `K.σ` | `docreatenewdocument` [do1.c:234] | `GRANORGL` (DOCUMENT) via `createorglgr` [granf2.c:111] | `dom(Σ.M)` ← +1 | none |
| `K.α` | `doinsert` [do1.c:87] | `GRANTEXT` (TEXTATOM) via `inserttextgr` [granf2.c:83] | `dom(Σ.C)` ← +|text| | POOM update (`insertpm`), spanfilade update (`insertspanf` with DOCISPAN) — derived structures only |
| `K.λ_sh` | `docreatelink` [do1.c:195] | `GRANORGL` (LINKATOM) via `createorglgr` [granf2.c:111] | `dom(Σ.L)` ← +1 | POOM updates (`insertpm` ×4), spanfilade updates (`insertspanf` ×4) — derived structures only |

**Conclusions:**

1. **Every named primitive strictly grows one domain.** No primitive step leaves all three domains unchanged; the substrate is strictly monotone/append-only with respect to `dom(Σ.M)`, `dom(Σ.C)`, `dom(Σ.L)`.

2. **`K.α` grows `dom(Σ.C)` alone.** The `docopy` call within `doinsert` updates the POOM (V→I mapping within an existing molecule) and the spanfilade (an index), but creates no new `GRANORGL` or `GRANTEXT` entries beyond those created by `inserttextgr` itself. `dom(Σ.M)` and `dom(Σ.L)` are unaffected.

3. **The three domains are independent targets.** The `TEXTATOM` / `LINKATOM` / non-ATOM branching in `findisatoinsertgr` [granf2.c:134-156] ensures that content deposits land only in the GRANTEXT subspace, link allocations land only in the GRANORGL+LINKATOM subspace, and molecule creation lands only in the GRANORGL+DOCUMENT subspace. There is no code path in any primitive step that crosses these boundaries.
