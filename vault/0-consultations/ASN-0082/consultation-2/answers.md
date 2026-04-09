# Revision Consultation — ASN-0082

**Review:** review-2.md
**Date:** 2026-04-09 14:48

## Summary

5 REVISE items analyzed: 4 internal, 1 consulted (0 nelson, 1 gregory)

## Consultation Results

### Issue 2: VD's informal justification overstates T10a.1

**Category:** GREGORY
**Reason:** Whether child-spawning occurs within a subspace's element field is an implementation fact about the udanax-green allocator. If child allocators are used, VD itself could be false, not just its justification.

**Gregory question:** Within a single subspace's element field, does the udanax-green allocator ever spawn child allocators (inc(·, k') for k' > 0), or is allocation always flat sibling production?

**Gregory's Answer:**

## KB Synthesis

## Allocation Within an Element Field: Always Flat Siblings

The allocator never spawns child allocators within a single element field. All actual address generation uses `tumblerincrement(lowerbound, 0, 1)` — rightshift = 0 throughout.

### The evidence

**Text content** (`findisatoinsertmolecule`): From [ST-INSERT] Finding 0031, `inserttextgr` advances with `tumblerincrement(&lsa, 0, textset->length, &lsa)` — rightshift=0, incrementing at the final digit. Finding 0033 confirms the result: sequential inserts produce a contiguous range `doc.3.1`, `doc.3.2`, …, `doc.3.N` — all flat siblings at the same depth.

**Link orgls** (`findisatoinsertmolecule` with LINKATOM hint): From [SS-ADDRESS-ALLOC] Finding 0065, link allocation calls `tumblerincrement(&lowerbound, 0, 1, isaptr)` — rightshift=0. The concrete example shows `doc.0.2.1`, `doc.0.2.2`, … — again, flat siblings.

**The one apparent exception (upper-bound computation only)**: In `findisatoinsertnonmolecule`, the search upper bound is computed as `tumblerincrement(hintisa, depth-1, 1)`, where `depth-1 = 1` for ACCOUNT→DOCUMENT creation [SS-ADDRESS-ALLOC] Finding 0021. But this rightshift=1 value is used exclusively to compute the *search boundary* passed to `findpreviousisagr` — never to produce the allocated address itself. The actual allocation in step 4 truncates the found address and increments at rightshift=0 to produce the next sibling.

**First-child bootstrap**: The only `.0.` boundary crossing occurs once per element field: when no prior element exists, the allocator constructs `parent.0.1` by appended convention, not via `tumblerincrement` with k' > 0. After that, every subsequent address is a flat sibling increment.

### Summary

| Usage | rightshift | Purpose |
|-------|-----------|---------|
| Text address generation | 0 | Flat sibling: `doc.3.N → doc.3.(N+1)` |
| Link orgl generation | 0 | Flat sibling: `doc.0.2.N → doc.0.2.(N+1)` |
| Upper-bound search | 1 | Search limit only — not the allocated address |
| First-child bootstrap | n/a | `parent.0.1` by construction, once per field |

Allocation within any element field is strictly flat sibling production: `inc(·, 0)` is the invariant. The `inc(·, k')` form for k' > 0 appears only as a bounding artifact, never as an address generator. [SS-ADDRESS-ALLOC], [ST-INSERT], [INV-MONOTONIC]

---

## Code Exploration

---

## Answer: Child Allocators Within a Subspace's Element Field

The answer is **yes, but only once per atom type per document** — to bootstrap the initial address structure. After that, all production is flat.

---

### The Mechanism: `tumblerincrement` as inc(·, k')

The formal `inc(t, k')` maps directly to:

**`backend/tumble.c:599`**
```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    // ...
    for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
    // idx = last nonzero mantissa position of aptr
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify(cptr);
}
```

- `rightshift = 0` → increments the last digit in place: **flat sibling production**, `inc(t, 0)`
- `rightshift > 0` → places a value `rightshift` positions beyond the last nonzero digit, inserting `rightshift` zero separators: **child spawning**, `inc(t, k')` for k' = rightshift

---

### The Allocator: `findisatoinsertmolecule`

All atom (text/link) addresses within a document's element field go through `findisatoinsertmolecule` (**`backend/granf2.c:158–181`**):

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound); // search ceiling
    clear(&lowerbound, sizeof(lowerbound));
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);     // find previous

    if (tumblerlength(&hintptr->hintisa) == tumblerlength(&lowerbound)) {
        tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);  // [A] k' = 2
        tumblerincrement(isaptr, 1, 1, isaptr);                        // [B] k' = 1
    } else if (hintptr->atomtype == TEXTATOM) {
        tumblerincrement(&lowerbound, 0, 1, isaptr);                   // [C] k' = 0
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement(&hintptr->hintisa, 2, 2, isaptr);             // [D] k' = 2
        if (tumblercmp(&lowerbound, isaptr) == LESS)
            tumblerincrement(isaptr, 1, 1, isaptr);                    // [E] k' = 1
        else
            tumblerincrement(&lowerbound, 0, 1, isaptr);               // [F] k' = 0
    }
}
```

The branch taken depends on **`tumblerlength(hintisa) == tumblerlength(lowerbound)`**, where `hintisa` = the document's own address D, and `lowerbound` is the rightmost granfilade entry before the search ceiling.

---

### When Is the Condition TRUE? (Child Spawning Required)

`findpreviousisagr` returns D itself (the document's GRANORGL node) as `lowerbound` when no prior atom of this type exists under D. Since `lowerbound = D = hintisa`, their lengths are trivially equal.

**First text insertion into D** — lowerbound = D (the ORGL node at D's address):

- **[A]** `tumblerincrement(D, 2, TEXTATOM, isaptr)` → k' = 2, produces **D.0.1** (adds two zero slots and the atom-type discriminator `TEXTATOM=1`)
- **[B]** `tumblerincrement(D.0.1, 1, 1, isaptr)` → k' = 1, produces **D.0.1.1** (adds the serial counter one level deeper)

Two child spawns: total depth increase = 3 levels below D's address level.

**First link insertion, no prior text** — same structure but atomtype=2:

- **[A]** k' = 2: produces **D.0.2**
- **[B]** k' = 1: produces **D.0.2.1**

**First link insertion, text already exists** — lowerbound = D.0.1.N (a text atom, depth > L(D)):
- Length condition is FALSE; falls to LINKATOM branch
- **[D]** `tumblerincrement(D, 2, 2, isaptr)` → k' = 2, produces D.0.2 (always recomputed)
- Then: `tumblercmp(D.0.1.N, D.0.2) == LESS` (since 1 < 2 at the atom-type position) → TRUE
- **[E]** `tumblerincrement(D.0.2, 1, 1, isaptr)` → k' = 1, produces **D.0.2.1**

Again, child spawning.

---

### When Is the Condition FALSE? (Flat Sibling Production)

Once any prior atom of a given type exists under D, `lowerbound` is at depth L(D) + 3 (e.g., D.0.1.N for a text atom). Since `tumblerlength(D.0.1.N) > tumblerlength(D)`, the length-equality condition fails.

**All subsequent text insertions** — branch **[C]**:
```c
tumblerincrement(&lowerbound, 0, 1, isaptr);  // k' = 0
```
Pure sibling: D.0.1.N → D.0.1.(N+1). **`granf2.c:169`**

**All subsequent link insertions** — branch **[F]**:
```c
tumblerincrement(&lowerbound, 0, 1, isaptr);  // k' = 0
```
Pure sibling: D.0.2.M → D.0.2.(M+1). **`granf2.c:175`**

**Within a single insert call** — `inserttextgr` loop (**`granf2.c:100`**):
```c
tumblerincrement(&lsa, 0, textset->length, &lsa);  // k' = 0 always
```
Each text chunk advances the address by its character count at k' = 0.

---

### Summary

| Situation | k' | Reference |
|---|---|---|
| First atom of any type into D (lowerbound = D) | **2, then 1** | `granf2.c:166–167` |
| First link when text exists (lowerbound < D.0.2) | **2, then 1** | `granf2.c:171,173` |
| Nth text atom (N ≥ 2) | **0** | `granf2.c:169` |
| Nth link atom (N ≥ 2) | **0** | `granf2.c:175` |
| Sequential chunks within one insert call | **0** | `granf2.c:100` |

**Conclusion:** Within a single subspace's element field, the allocator **does** spawn child allocators (`inc(·, k')` for k' > 0) — but exactly once per atom type, when bootstrapping the two-level nesting that establishes the atom-type discriminator (`D.0.atomtype`) and serial-counter level (`D.0.atomtype.serial`). This requires k'=2 (jump two levels to insert the type slot) followed by k'=1 (one more level to seat the first serial number). All subsequent allocations within that atom type's subspace are flat sibling production at k'=0. Allocation is therefore not purely flat, but the child-spawning is structurally bounded: at most two child-spawns per atom type, per document, ever.
