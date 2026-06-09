## Question 15 [evidence]

> Does the link orgl get created in the granfilade while a V→I POOM entry for the link is placed in the home document's link subspace (`2.x`), making the link reside in both granfilade and the home document's POOM?

## KB Synthesis

Yes, exactly. Link creation writes to both structures simultaneously.

**Granfilade (I-space):** `createorglingranf()` allocates a fresh I-address for the link orgl itself — the permanent link object. This address follows the document-scoped monotonic allocation scheme (`docISA.0.2.N`). [SS-ADDRESS-SPACE / Finding 0065], [SS-GRANF-OPERATIONS]

**Home document's POOM (V-space):** The link orgl's ISA is then converted to an ispanset via `tumbler2spanset()`, and `findnextlinkvsa()` computes the next available position in the `2.x` subspace (starting at `2.1`, growing by append). `docopy()` inserts a V→I mapping into the home document's POOM at that `2.x` position, pointing to the link orgl's I-address. [SS-LINK-SUBSPACE], [ST-CREATE-LINK / Finding 0009]

**Spanfilade:** Additionally, the link's *endpoint content* I-addresses (the FROM/TO/THREE endsets) are indexed in the spanfilade via `insertendsetsinspanf()`. [SS-SPANF-OPERATIONS], [SS-THREE-LAYER-MODEL / Finding 0040]

So the three-layer picture is:
- **I-space (granfilade):** link orgl at permanent address `docISA.0.2.N`
- **POOM (home document's `2.x` subspace):** V→I entry mapping `2.N → link_orgl_ISA`
- **Spanfilade:** endpoint content I-addresses → link ISA index entries

The POOM entry in `2.x` is what makes the link visible in `retrieve_vspanset` results. It can be removed via `DELETEVSPAN(2.x)` without destroying the link orgl or spanfilade entries — producing the "reverse orphan" state. [EC-REVERSE-ORPHAN], [FC-LINK-DELETE-ISOLATION]

---

## Code Exploration

I now have a complete picture from the source. Here is my full answer.

---

## Yes — Links Reside in Both the Granfilade and the Home Document's POOM

The answer is **yes**, with precise mechanics worth spelling out.

---

### Step 1: Link Orgl Created in the Granfilade

`docreatelink` at `do1.c:195` is the entry point. The very first operation is:

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);   // do1.c:207
createorglingranf (taskptr, granf, &hint, linkisaptr)    // do1.c:209
```

`LINKATOM` is defined as `2` at `xanadu.h:146`. The hint marks this as an atomic link object belonging to the home document (`docisaptr`).

`createorglingranf` routes to `granf2.c:158` (`findisatoinsertmolecule`) for the `LINKATOM` case:

```c
} else if (hintptr->atomtype == LINKATOM) {          // granf2.c:170
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
    if (tumblercmp (&lowerbound, isaptr) == LESS)
        tumblerincrement (isaptr, 1, 1, isaptr);
    else
        tumblerincrement (&lowerbound , 0, 1, isaptr);
}
```

This derives the link's ISA from the document's ISA, appended with `.0.2…` in the granfilade address space (LINKATOM=2 at depth 2). The orgl is then inserted into the granfilade as a `GRANORGL` entry at `linkisaptr` with a freshly created `POOM` enfilade:

```c
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);   // granf2.c (createorglgr)
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
```

**The link now exists in the granfilade as its own orgl at address `linkisaptr`.**

---

### Step 2: V→I Entry Placed in the Home Document's POOM at 2.x

After creating the link orgl, `docreatelink` does:

```c
tumbler2spanset (taskptr, linkisaptr, &ispanset)          // do1.c:210
findnextlinkvsa (taskptr, docisaptr, &linkvsa)            // do1.c:211
docopy (taskptr, docisaptr, &linkvsa, ispanset)           // do1.c:212
```

`findnextlinkvsa` at `do2.c:151` establishes a minimum V-address of **2.1** for link entries:

```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);   // component[0] = 2  → 2.0
tumblerincrement (&firstlink, 1, 1, &firstlink);   // component[1] = 1  → 2.1
```

If the document's existing vspan doesn't yet reach 2.1, `linkvsa = 2.1`. Otherwise it appends after the current vspan end. Either way, `linkvsa` is in the **2.x subspace** of the document's V-space.

`docopy` at `do1.c:45` then inserts the link's I-address into the **home document's own POOM** (not the link orgl's POOM) at that V-address:

```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)    // do1.c:60
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN) // do1.c:62
```

`insertpm` at `orglinks.c:75` signature:
```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl,
              tumbler *vsaptr, typesporglset sporglset)
```

Here `orglisa = docisaptr` and `orgl = docorgl` — the home document's orgl — and `vsaptr = linkvsa` (≥ 2.1). This writes `linkvsa → ispanset` as a V→I mapping into the home document's POOM tree.

**The link's I-address now appears as a V→I entry in the home document's POOM at V-address ≥ 2.1.**

---

### Step 3: Endpoint Data Stored in the Link Orgl's Own POOM

Separately, `insertendsetsinorgl` at `do2.c:130` writes the from/to/three endpoint data into the **link orgl's own POOM** (not the home document's):

```c
insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)   // do2.c:132
insertpm(taskptr, linkisaptr, link, tovsa, tosporglset)       // do2.c:133
insertpm(taskptr, linkisaptr, link, threevsa, threesporglset) // do2.c:137
```

`setlinkvsas` at `do2.c:169` defines the V-addresses inside the link orgl:

```c
fromvsa = 1.1   // endpoint from-set at 1.1 within the link orgl's POOM
tovsa   = 2.1   // endpoint to-set at 2.1 within the link orgl's POOM
threevsa = 3.1  // optional three-set at 3.1 within the link orgl's POOM
```

These are V-addresses **within the link's own orgl**, not within the home document.

---

### Summary: Two Distinct Residences

| Location | What is stored | V-address |
|----------|---------------|-----------|
| **Granfilade** | The link orgl itself (a POOM with endpoint data at 1.1, 2.1, 3.1) | ISA `linkisaptr` (derived from `docisa.0.2…`) |
| **Home document's POOM** | V→I entry: `linkvsa → ispanset` (the link's I-address) | V-address ≥ 2.1 (the 2.x subspace) |

The home document's POOM entry is a **transclude reference**: it records *where* in I-space the link orgl lives, establishing the link's identity within the document's V-space. The link's actual data (endpoints) lives inside the link orgl in the granfilade.

---

### Note on a Stale Comment

`do1.c:408` contains the comment:

> "Spans with stream < 1.0 are in link subspace - skip them"

This comment (added in a Bug 009 fix patch) is **incorrect**. The code in `findnextlinkvsa` unambiguously places link entries at V-address ≥ 2.1. The recent commits `e416769` and `bbeb9e8` (fix: "correct link subspace from 0.x to 2.x") confirm the link subspace is at **2.x**, not 0.x. The filter function at `do1.c:386` retains everything ≥ 1.0, which means it accidentally retains links at 2.x — a latent bug from the incorrect 0.x assumption.
