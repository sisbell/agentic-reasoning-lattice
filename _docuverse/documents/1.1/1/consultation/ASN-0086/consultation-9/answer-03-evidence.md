## Question 3 [evidence]

> Does any path in udanax-green ever deposit a link at an address that is a strict prefix-extension of an existing link address, or is the `lowerbound + 1` / `docaddr + 2` pattern in `findisatoinsertmolecule` the only link-emission discipline in the substrate?

## KB Synthesis

## Answer

No path in udanax-green ever deposits a link orgl at an address that is a strict prefix-extension of an existing link address. The `lowerbound + 1` increment is the sole link-emission discipline.

**Why the mechanism can only produce siblings**

Link I-address allocation flows through `findisatoinsertmolecule`, triggered by `createorglingranf` via `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` [SS-ADDRESS-ALLOC Finding 0065]. The algorithm:

1. Sets `upperbound = tumblerincrement(docISA, 2, LINKATOM+1)` — bounding the search to element-field 2 (links), exclusive of field 3 [SS-ADDRESS-ALLOC Finding 0065, code ref `granf2.c:162`].
2. Calls `findpreviousisagr` to locate the highest existing address below that bound.
3. Calls `tumblerincrement(&lowerbound, 0, 1, isaptr)` — increments at `rightshift=0`, meaning the **last significant digit** of `lowerbound`.

Step 3 is the critical constraint. `rightshift=0` adds 1 at the current last significant digit position. For an existing link at `docISA.0.2.1` (mantissa length N), this produces `docISA.0.2.2` — a sibling at the same depth. A prefix-extension like `docISA.0.2.1.1` would require adding a digit at position N+1 (one level deeper), which would require `rightshift=-1` or a call to `findisatoinsertnonmolecule` with `depth=1`. Neither occurs here [SS-TUMBLER Finding 0031, SS-ADDRESS-ALLOC Finding 0021].

**No alternative emission paths exist**

The only code that creates link orgls is `docreatelink` → `createorglingranf` [ST-CREATE-LINK Finding 0012]. `findisatoinsertnonmolecule` (which can produce child addresses via `depth=1`) is reserved for DOCUMENT and VERSION allocation [SS-ADDRESS-ALLOC Findings 0021, 0068]. LINKATOM is explicitly handled by `findisatoinsertmolecule`, not `findisatoinsertnonmolecule` [SS-ADDRESS-SPACE Finding 0077, code ref `granf2.c:130-156` dispatch].

**Consequence for the address space**

All links under a given document form a flat sequence `docISA.0.2.1`, `docISA.0.2.2`, … with no nesting among them. The tumbler containment predicate [SS-TUMBLER-CONTAINMENT] would never classify one link address as being "under" another link address. This is consistent with the monotonicity invariant [INV-MONOTONIC Finding 0065]: link allocation within a document is strictly sequential and independent between documents.

---

## Code Exploration

I now have everything I need. Here is the complete answer.

---

## Does Any Path Deposit a Link at a Prefix-Extension of an Existing Link Address?

**No.** The `lowerbound + 1` / `docaddr + 2` pattern in `findisatoinsertmolecule` is the only link-emission discipline in the substrate, and it structurally prevents prefix-extension collisions by allocating all links for a given document as fixed-depth siblings.

---

### The Single Entry Point

Every link ISA allocation flows through one mandatory chain:

```
domakelink / docreatelink (do1.c:169–221)
  → makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)  [do1.c:180/207]
  → createorglingranf(...)                                  [do1.c:182/209]
    → createorglgr(...)                                     [granf2.c:111]
      → findisatoinsertgr(...)                              [granf2.c:117]
        → findisatoinsertmolecule(...)  [LINKATOM branch]   [granf2.c:142]
```

No other function computes a new link ISA. The remaining call sites merely consume a pre-computed `linkisaptr`:

- `findorgl` [granf1.c:17–41] — fetches an existing ORGL at a known address
- `insertspanf` [spanf1.c:15–54] — indexes `linkisaptr` into the spanfilade, no address computation
- `insertendsetsinorgl` / `insertendsetsinspanf` [do2.c:130–148, 111–128] — record endpoint data against `linkisaptr`
- `findnextlinkvsa` [do2.c:151–167] — computes the V-space slot for the link *reference* inside the containing document, not the link's own ISA
- `klugefindisatoinsertnonmolecule` [granf2.c:183–201] — dead code under `#ifdef UnDeFIned`; handles DOCUMENT type, not LINKATOM anyway

---

### Dissecting `findisatoinsertmolecule`

```c
/* granf2.c:158–181 */
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound); /* 162 */
    clear (&lowerbound, sizeof(lowerbound));                                       /* 163 */
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);     /* 164 */
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {       /* 165 */
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);             /* 166 */
        tumblerincrement (isaptr, 1, 1, isaptr);                                  /* 167 */
    } else if (hintptr->atomtype == TEXTATOM) {
            tumblerincrement (&lowerbound, 0, 1, isaptr);                         /* 169 */
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);                       /* 171 */
        if (tumblercmp (&lowerbound, isaptr) == LESS)                             /* 172 */
            tumblerincrement (isaptr, 1, 1, isaptr);                              /* 173 */
        else
            tumblerincrement (&lowerbound , 0, 1, isaptr);                        /* 175 */
    }
}
```

Let `D = docisa` with `tumblerlength(D) = L` (mantissa non-zero through position `L−1`).

**`tumblerincrement(base, rightshift, bint)` semantics** [tumble.c:599–623]:  
Finds last non-zero mantissa position `idx` in `base`, then adds `bint` to `mantissa[idx + rightshift]`. So `rightshift = 2` appends two slots and adds `bint` at the second; `rightshift = 0` increments in place.

#### Line 162 — upper bound

```
upperbound = tumblerincrement(D, 2, atomtype+1)
           = tumblerincrement(D, 2, 3)          [LINKATOM=2, so +1=3]
           = D.0.3                              [mantissa[L+1] = 3]
```

`findpreviousisagr` [granf2.c:255–278] returns `lowerbound` = highest address in the granfilade strictly below `D.0.3`.

---

#### Branch A — empty document (lines 165–167)

If nothing has yet been allocated under `D`, `findpreviousisagr` returns `D` itself (the document ORGL node). Then:

```
tumblerlength(hintisa=D) == tumblerlength(lowerbound=D)  →  TRUE
```

- Line 166: `isaptr = tumblerincrement(D, 2, LINKATOM=2)` = `D.0.2` — `mantissa[L+1] = 2`
- Line 167: `isaptr = tumblerincrement(D.0.2, 1, 1)` = `D.0.2.1` — `mantissa[L+2] = 1`

**First link address = `D.0.2.1`, depth = `L + 3`.**

---

#### Branch B — prior content exists (lines 170–175, LINKATOM path)

Prior content is text at `D.0.1.X` or a prior link at `D.0.2.N`. In both cases `tumblerlength(lowerbound) ≠ L`, so branch A is skipped.

- Line 171: probe = `D.0.2` — `mantissa[L+1] = 2`
- Line 172: `tumblercmp(lowerbound, probe)`

**Case B1** — `lowerbound < D.0.2` (prior content is text, `D.0.1.X`):

At mantissa position `L+1`: text has value 1, probe has value 2 → `LESS`.

- Line 173: `isaptr = tumblerincrement(D.0.2, 1, 1)` = `D.0.2.1` — depth `L+3`.

**Case B2** — `lowerbound ≥ D.0.2` (prior content is a link `D.0.2.N`):

At mantissa position `L+2`: link has value `N > 0`, probe has value 0 → probe < lowerbound, condition `LESS` is false.

- Line 175: `isaptr = tumblerincrement(D.0.2.N, 0, 1)` = `D.0.2.(N+1)` — depth `L+3` (same depth as prior link).

---

### Why Prefix-Extension Is Impossible

For new link `B` to be a strict prefix-extension of existing link `A = D.0.2.N`:

- A in mantissa: `[..., 2, N, 0, 0, ...]` — last non-zero at position `L+2`
- B (prefix-extension): `[..., 2, N, 0, X, ...]` where `X > 0` — last non-zero at position `L+3`

This would require `mantissa[L+3] ≠ 0` in the result. But:

- Branch A and Case B1 both produce `D.0.2.1` = `mantissa[L+2] = 1`, leaving `mantissa[L+3] = 0`
- Case B2 produces `D.0.2.(N+1)` = `mantissa[L+2] = N+1`, leaving `mantissa[L+3] = 0`

**Every link for document `D` lands at exactly depth `L+3` — one slot deeper than the `docisa.0.2` probe point, never two.** The sequence is:

```
D.0.2.1 → D.0.2.2 → D.0.2.3 → ...
```

All siblings. The critical guard at line 172 is what prevents descent: if `lowerbound` (a prior link) is *above* the probe `D.0.2`, branch B2 fires and stays at the same depth via `lowerbound + 1` [line 175], rather than branching through line 173 which would try to extend the probe point (but the probe point `D.0.2` is already strictly LESS than any prior link, so B2's condition is reliably met after the first link exists).

#### The `findpreviousisagr` search bound is tight

`upperbound = D.0.3` [line 162]. Link addresses `D.0.2.N` are all `< D.0.3` (at position `L+1`: value 2 < 3). Text addresses `D.0.1.X` are also `< D.0.3`. So the search always returns the correct predecessor in the link subrange `[D.0.2, D.0.3)`, and the sibling-increment invariant is maintained.

---

### Summary

| Path | Code | Result | Depth |
|---|---|---|---|
| First link, empty document | granf2.c:166–167 | `D.0.2.1` | `L+3` |
| First link, document has text | granf2.c:171–173 | `D.0.2.1` | `L+3` |
| N-th link (N ≥ 2) | granf2.c:175 | `D.0.2.N+1` | `L+3` |

The `lowerbound + 1` and `docaddr + 2` (line 175 and lines 171/173, respectively) are the only allocation operations for link ISAs. All produce fixed-depth siblings. No code path ever walks deeper into an existing link's address subspace, so the strict-prefix-extension scenario cannot arise.
