## Question 16 [evidence]

> Does the new version own an independent I-address allocation range rooted at its own docISA, such that future content allocations under the version cannot collide with the source's findisatoinsertmolecule queries, or do source and version share an allocation parent?

## KB Synthesis

## Versions Own Independent, Non-Overlapping Allocation Ranges

**Short answer:** The version allocates content I-addresses under its own document ISA, structurally partitioned from the source's range. They do not share an allocation parent for content.

---

### How the allocation ranges are structured

From [SS-ADDRESS-ALLOC] Finding 0065, content I-address allocation via `findisatoinsertmolecule` is bounded to `docISA.0.[element_field].x`:

- Links at `docISA.0.2.x` (e.g., `1.1.0.1.0.1.0.2.1`, `1.1.0.1.0.1.0.2.2`, ...)
- Text at `docISA.0.3.x` (e.g., `1.1.0.1.0.1.0.3.1`, `1.1.0.1.0.1.0.3.2`, ...)

The upper bound is set as `tumblerincrement(docISA, 2, atomtype+1)`, scoping the search to that document's element subspace. The lower bound check (`lowerbound < docISA.0.element_field.2`) detects that no allocation exists yet for that document and starts fresh at `docISA.0.element_field.1`.

For a version at `1.1.0.1.0.1.1` ([SS-VERSION-ADDRESS] Finding 0068), its content lives at:

```
1.1.0.1.0.1.1.0.3.1   (first text atom in version)
1.1.0.1.0.1.1.0.2.1   (first link in version)
```

The source's content lives at:

```
1.1.0.1.0.1.0.3.1     (first text atom in source)
1.1.0.1.0.1.0.2.1     (first link in source)
```

In tumbler ordering, `1.1.0.1.0.1.0.*` < `1.1.0.1.0.1.1.*` — these are distinct branches. The source's `findpreviousisagr` searches below `1.1.0.1.0.1.0.3.x`, so it never reaches the version's range. The version's search might see source addresses, but the lower bound check rejects them as belonging to a different document and falls back to starting fresh.

---

### Formal statement from [SS-ADDRESS-SPACE] Finding 0077

> The formal model should NOT use a single `Σ.next` counter. Instead, allocation is **a family of independent functions partitioned by tumbler range**: `next_content_addr(granf, doc) = max_content(granf, doc) + 1`

Source and version have separate `max_content(granf, doc)` computations because their docISAs are different.

---

### CREATENEWVERSION does not pollute either counter

From [ST-VERSION] Finding 0077, `CREATENEWVERSION` allocates only a document address (non-molecule), **never** a content I-address. Confirmed empirically:

> INSERT "ABC" → CREATENEWVERSION → INSERT "XYZ" yields **1 shared span pair** (contiguous I-addresses), not 2.

Contrast with INSERT "ABC" → CREATELINK → INSERT "XYZ" which yields **2 shared span pairs** because CREATELINK does allocate a content entry in the source's molecule range ([INT-LINK-INSERT] Finding 0063).

---

### Summary

| Operation | Disrupts source content contiguity? |
|-----------|--------------------------------------|
| CREATENEWVERSION | No ([INV-MONOTONIC] Finding 0077) |
| CREATELINK | Yes ([INT-LINK-INSERT] Finding 0063) |
| INSERT into version | No — uses version's ISA, separate range |

The version's content allocation range `version_ISA.0.element_field.x` is a structurally independent subtree from the source's `source_ISA.0.element_field.x`. Future inserts into either document cannot collide because the upper bounds passed to `findisatoinsertmolecule` keep each search within its own document's namespace.

---

## Code Exploration

I now have the complete picture. Finding 0068 contains the critical missing piece: V is allocated as a **child** of D, not a sibling — so V = `D.1` (e.g., `1.1.0.1.0.1.1`). Let me verify the molecule subspace math against actual addresses from that finding, then write the full answer.

The actual address sequence confirmed by golden tests (Finding 0068):
- D = `1.1.0.1.0.1`
- V = `1.1.0.1.0.1.1` (child, via depth=1 DOCUMENT-DOCUMENT hint)
- D's molecule upper bound: `tumblerincrement(D, 2, TEXTATOM+1=2)` = `1.1.0.1.0.1.0.2`
- V's molecule upper bound: `tumblerincrement(V, 2, TEXTATOM+1=2)` = `1.1.0.1.0.1.1.0.2`

Key ordering: `1.1.0.1.0.1.0.2` < `1.1.0.1.0.1.1` = V < `1.1.0.1.0.1.1.0.2`

---

## Answer: V Owns an Independent I-Address Allocation Range Rooted at Its Own docISA

**The version does NOT share an allocation parent with the source in the molecule space.** Source and version have provably non-overlapping I-address subspaces, each rooted at their own docISA. Here is the complete code-traced proof.

---

### 1. How the version ISA is allocated

`fns.c:294-296` calls `docreatenewversion(taskptr, &originaldocisa, &originaldocisa, &newdocisa)`, so `isaptr = wheretoputit = D`.

`do1.c:270-271`:
```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
```

Since `isaptr == wheretoputit`, `tumbleraccounteq` is trivially true. For a user's own document, `isthisusersdocument` (`socketbe.c:197-201`) returns true. So the hint is always DOCUMENT-DOCUMENT with `hintisa = D`.

`do2.c:78-84` — `makehint` stores: `supertype = DOCUMENT(3)`, `subtype = DOCUMENT(3)`, `hintisa = D`.

In `findisatoinsertnonmolecule` (`granf2.c:209`):
```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
// DOCUMENT == DOCUMENT → depth = 1
```

With depth = 1, `granf2.c:213`:
```c
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
// depth-1 = 0: adds 1 to last non-zero digit of D
// D = 1.1.0.1.0.1 → upperbound = 1.1.0.1.0.2
```

`findpreviousisagr` finds the last item before `1.1.0.1.0.2`. For the first version of D, that is D itself. The "nothing under hint" branch at `granf2.c:237`:
```c
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
// depth = 1: adds 1 one position further right
// D = 1.1.0.1.0.1 → V = 1.1.0.1.0.1.1
```

**V is a child of D, not a sibling.** Confirmed by golden tests (Finding 0068): `1.1.0.1.0.1` → `1.1.0.1.0.1.1`.

---

### 2. Molecule allocation is rooted at the document's own ISA

When content is inserted into any document X, `do1.c:117`:
```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
```

In `findisatoinsertgr` (`granf2.c:135`):
```c
if (hintptr->subtype == ATOM) {
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
```

`findisatoinsertmolecule` (`granf2.c:158-181`) computes the search bounds using `hintisa = X`:
```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
// TEXTATOM = 1, so atomtype+1 = 2
// upperbound = X.0.2  (two positions right of X's last digit)
```

For D = `1.1.0.1.0.1`:  upperbound(D) = `1.1.0.1.0.1.0.2`  
For V = `1.1.0.1.0.1.1`: upperbound(V) = `1.1.0.1.0.1.1.0.2`

---

### 3. The non-overlap proof

**Ordering of key addresses** (by `abscmp`, `tumble.c:87-111`, which compares mantissa left-to-right):

```
1.1.0.1.0.1              = D
1.1.0.1.0.1.0.1.0.N      = D's content at D.0.1.0.N
1.1.0.1.0.1.0.2          = upperbound(D)   [compare position 6: 0 < 1 → below V]
1.1.0.1.0.1.1            = V               [position 6: 1 > 0]
1.1.0.1.0.1.1.0.1.0.N    = V's content at V.0.1.0.N
1.1.0.1.0.1.1.0.2        = upperbound(V)
```

Therefore: `D.0.content < upperbound(D) < V < V.0.content < upperbound(V)`

**Claim A: D's allocator never sees V's content.**  
D's `findpreviousisagr` searches only addresses < `upperbound(D) = 1.1.0.1.0.1.0.2`. V's content is at `V.0.1.0.N > 1.1.0.1.0.1.1 > upperbound(D)`. Out of range. ✓

**Claim B: V's allocator finds V itself as lowerbound, not D's content.**  
V's `findpreviousisagr` searches for the last address < `upperbound(V) = 1.1.0.1.0.1.1.0.2`. The granfilade contains D's content at `D.0.1.0.N` and the V document node at `V = 1.1.0.1.0.1.1`. Since `V > D.0.1.0.N` (position 6: 1 > 0), V is the largest item below `upperbound(V)`. So `lowerbound = V`.

**Claim C: V's first allocation goes to V.0.1.0.1, not into D's subspace.**  
`granf2.c:165`:
```c
if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);  // lowerbound=V, atomtype=1 → V.0.1
    tumblerincrement (isaptr, 1, 1, isaptr);                       // → V.0.1.0.1
}
```
`tumblerlength(hintisa=V) == tumblerlength(lowerbound=V)` → true → first slot is `V.0.1.0.1`. ✓

---

### 4. CREATENEWVERSION does not advance D's allocation counter

Finding 0077 (confirmed by `do1.c:277-298`): `docreatenewversion` calls `createorglingranf` (allocates V's document node) and `docopyinternal` → `insertspanf` (copies span metadata). It does **not** call `findisatoinsertgr`. No text molecule I-address is allocated by the version operation itself. D's molecule allocation pointer remains exactly where it was before versioning.

---

### 5. Formal summary

| Subspace | Owner | I-address range | Upper bound |
|---|---|---|---|
| D's molecules | Document D | `(D, D.0.2)` = `(1.1.0.1.0.1, 1.1.0.1.0.1.0.2)` | `do1.c:117` + `granf2.c:162` |
| V's ISA | Version V | `1.1.0.1.0.1.1` | `do1.c:271` + `granf2.c:237` |
| V's molecules | Document V | `(V, V.0.2)` = `(1.1.0.1.0.1.1, 1.1.0.1.0.1.1.0.2)` | `do1.c:117` + `granf2.c:162` |

Because `upperbound(D) < V < V.0.molecule`, these three ranges are **strictly disjoint**. The version's ISA itself, sitting between D's molecule range and V's molecule range, acts as the natural sentinel.

**The new version owns an independent I-address allocation range rooted at its own docISA.** Source and version do not share an allocation parent in molecule space. Their ranges are isolated by V's document ISA in the globally-ordered granfilade.
