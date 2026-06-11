## Question 1 [evidence]

> Does udanax-green's link allocator ever emit a link address whose element field has depth greater than 2 (anything other than incrementing the final digit of `d.0.s_L.n`), or allocate links homed under nodes outside the `n₀` lineage — or is the frontier chain `inc(·, 0)` at depth 2 the only allocation path?

## KB Synthesis

## Link Address Allocation: Single Depth-2 Increment Path

The KB is unambiguous: there is only one allocation path, and it never produces addresses deeper than the pattern `docISA.0.2.n`.

### The Allocation Mechanism

[SS-ADDRESS-ALLOC / ST-ADDRESS-ALLOC — Finding 0065] describes the complete path for MAKELINK:

1. **Upper bound**: `tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound)` — for LINKATOM (atomtype=2) this produces `docISA.0.3` (or equivalently written `docISA.2.3` in the KB notation), bounding the search to element field 2 exclusively within the home document.
2. **Find previous**: `findpreviousisagr` returns the highest existing link address below that bound and under `docISA`.
3. **First link**: if nothing found (`lowerbound < docISA.0.2`), allocate at `docISA.0.2.1`.
4. **Subsequent links**: `tumblerincrement(&lowerbound, 0, 1, isaptr)` — `rightshift=0` increments the **final digit** by 1.

The critical point is `rightshift=0`. From [SS-TUMBLER / ST-INSERT — Finding 0031], `rightshift=0` increments at the last significant digit position — no `.0.` separator (hierarchy boundary) is ever inserted. Contrast with `rightshift > 0`, which would append zero-separator digits and increase address depth.

### What This Means for the Address Structure

For home document `1.1.0.1.0.1`, the emitted link addresses are strictly:

```
1.1.0.1.0.1.0.2.1   (first link)
1.1.0.1.0.1.0.2.2   (second link)
1.1.0.1.0.1.0.2.3   ...
```

The element field is always `2` (hardcoded by the `atomtype = LINKATOM = 2` passed to `makehint` per [SS-ADDRESS-SPACE — Finding 0065]), and the element number is a flat monotonically-increasing integer at depth 1 within that field. No address of the form `docISA.0.2.x.y` (depth > 1 in element number) is ever produced.

### No Out-of-Lineage Allocation

The upper bound `docISA.0.3` and the `findpreviousisagr` containment check (which [PRE-ADDRESS-ALLOC — Finding 0021] confirms was added specifically to prevent cross-boundary leakage, fixing Bug 0013) together ensure the allocator never crosses into a different document's namespace. The search is bounded both above (`docISA.0.3`) and implicitly below (`docISA.0.2`), producing a closed interval within the home document's link subspace.

[INV-MONOTONIC — Finding 0065] confirms this per-document monotonicity: link addresses in document A grow independently of link addresses in document B, with each document's counter starting at `.0.2.1`.

### Answer

**`inc(·, 0)` at depth 2 is the only allocation path.** The allocator never emits link addresses with element number depth greater than 1, and never allocates links under any orgl outside the home document's `docISA.0.2.*` subspace. The address structure is completely flat within element field 2: `{account}.0.{docnum}.0.2.{n}` where `n` increments by 1 each time.

---

## Code Exploration

I have all the code I need. Let me now trace every line precisely.

---

## Full Answer

### The Link ISA Allocator — Complete Call Chain

**Entry:** `createlink` [fns.c:100–112]
```c
getcreatelink(taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
docreatelink(taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)
```

**Core allocation:** `docreatelink` [do1.c:195–221]
```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);   // [do1.c:207]
createorglingranf (taskptr, granf, &hint, linkisaptr)    // [do1.c:209]
```

`makehint` [do2.c:78–84] writes:
```c
hintptr->supertype = DOCUMENT  (= 3)
hintptr->subtype   = ATOM      (= 4)
hintptr->atomtype  = LINKATOM  (= 2)
hintptr->hintisa   = *docisaptr          // document address d
```

`createorglingranf` → `createorglgr` [granf2.c:111–128] → `findisatoinsertgr` [granf2.c:117].

---

### `findisatoinsertgr` [granf2.c:130–156]

```c
if (hintptr->subtype == ATOM) {          // TRUE: ATOM == 4
    if (!isaexistsgr(fullcrumptr, &hintptr->hintisa))
        return (FALSE);                  // document must exist
    findisatoinsertmolecule(fullcrumptr, hintptr, isaptr);
}
tumblerjustify(isaptr);
```

For links, `subtype == ATOM` is always true; the call unconditionally goes to `findisatoinsertmolecule`. The non-molecule path (`findisatoinsertnonmolecule`) is never reachable for links.

---

### `findisatoinsertmolecule` [granf2.c:158–181] — The Only Link ISA Path

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);   // [granf2.c:166]
        tumblerincrement (isaptr, 1, 1, isaptr);                        // [granf2.c:167]
    } else if (hintptr->atomtype == TEXTATOM) {
        tumblerincrement (&lowerbound, 0, 1, isaptr);
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);             // [granf2.c:171]
        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);                    // [granf2.c:173]
        else
            tumblerincrement (&lowerbound , 0, 1, isaptr);              // [granf2.c:175]
    }
}
```

---

### `tumblerincrement` Semantics [tumble.c:599–623]

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    if (iszerotumbler (aptr)) {
        cptr->exp = -rightshift;
        cptr->mantissa[0] = bint;
        return(0);
    }
    if (aptr != cptr) movetumbler(aptr, cptr);
    for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
    cptr->mantissa[idx + rightshift] += bint;   // [tumble.c:621]
    tumblerjustify(cptr);
}
```

`idx` is the 0-based index of the **last non-zero mantissa slot**. With `rightshift = N`, the value `bint` is added at position `idx + N`, which appends N zero-separator digits then `bint`. `rightshift = 0` increments the existing last digit without extending depth.

---

### Depth Analysis — All Branches for LINKATOM

Let document `d` have `tumblerlength(d) = L` (L mantissa slots occupied, idx = L−1 for tumblerincrement).

**Setup (both branches):**
```c
tumblerincrement(&d, 2, LINKATOM+1, &upperbound)
// = d with mantissa[L−1+2] += 3  →  d.0.3   depth L+2 (value 3 at slot L+1)
findpreviousisagr(fullcrumptr, &upperbound, &lowerbound)
// → largest existing ISA strictly < d.0.3
```

**Branch A — `tumblerlength(&d) == tumblerlength(&lowerbound)` [granf2.c:165]:**

This fires when lowerbound is at exactly depth L (e.g. lowerbound is the document `d` itself, on first link allocation):
```c
tumblerincrement(&lowerbound, 2, LINKATOM, isaptr)  // d.0.2  (depth L+2)
tumblerincrement(isaptr, 1, 1, isaptr)              // d.0.2.1 (depth L+3)
```
Result: **`d.0.2.1`**, depth L+3.

**Branch B — `atomtype == LINKATOM` [granf2.c:170]:**

This fires when lowerbound is deeper than L (e.g. an existing link `d.0.2.n` at depth L+3):
```c
tumblerincrement(&d, 2, 2, isaptr)      // d.0.2   (depth L+2)

if (tumblercmp(&lowerbound, isaptr) == LESS)
    tumblerincrement(isaptr, 1, 1, isaptr);         // d.0.2.1  (depth L+3)
else
    tumblerincrement(&lowerbound, 0, 1, isaptr);    // d.0.2.(n+1)  (depth L+3)
```

- Sub-branch `LESS`: lowerbound is before `d.0.2` — first link in this subspace → `d.0.2.1`, depth L+3.
- Sub-branch `else`: lowerbound `d.0.2.n` ≥ `d.0.2` — increment its last digit → `d.0.2.(n+1)`, depth L+3.

**Both branches produce exactly depth L+3: the invariant form `d.0.2.n`.**

---

### Does the element field ever exceed depth 2?

No. In every reachable execution path of `findisatoinsertmolecule` with `atomtype == LINKATOM`:

| Scenario | Path | Result | Element suffix depth |
|---|---|---|---|
| First link ever (lowerbound = d) | Branch A | `d.0.2.1` | 2 (`.2.n`) |
| First link in subspace (lowerbound < d.0.2) | Branch B, LESS | `d.0.2.1` | 2 |
| Nth link (lowerbound = d.0.2.n) | Branch B, else | `d.0.2.(n+1)` | 2 |

There is no code that appends a fourth component beyond `.0.2.n`. `tumblerincrement` with `rightshift=0` increments the existing last digit; it cannot increase depth. `tumblerincrement` with `rightshift=1` adds exactly one separator+digit, bringing depth from L+2 to L+3 exactly once. No invocation in the LINKATOM branch uses `rightshift ≥ 2` on an address that is already at depth L+2 or deeper.

---

### Is `inc(·, 0)` at depth 2 the Only Frontier for Subsequent Links?

Yes. Once the first link `d.0.2.1` exists:

- `findpreviousisagr` returns lowerbound = `d.0.2.n` (depth L+3)
- `tumblerlength(&lowerbound) ≠ L` → Branch A is skipped
- `tumblercmp(&lowerbound, d.0.2)` is GREATER (not LESS) → `else` sub-branch fires:
  ```c
  tumblerincrement (&lowerbound, 0, 1, isaptr);   // [granf2.c:175]
  ```
  This is exactly `inc(lowerbound, 0)` — increment the final digit of `d.0.2.n`, yielding `d.0.2.(n+1)`.

The frontier chain is a simple linear increment of the terminal digit within the `.0.2` subspace. No other structure is ever emitted.

---

### Are Links Ever Homed Outside the `n₀` Lineage?

The allocator itself is lineage-agnostic. The only guard is:

```c
if (!isaexistsgr(fullcrumptr, &hintptr->hintisa))   // [granf2.c:136]
    return (FALSE);
```

This verifies that a granfilade entry for the document address exists — it does not check account ownership or `n₀` parentage. The `hintisa` is whatever `docisaptr` the caller passes in [do1.c:207]. Any document address that resolves to an existing granfilade entry could serve as the link home.

The ownership gate is enforced upstream at the bert/access-control layer (`checkforopen`/`findbert` in `bert.c`), not inside `findisatoinsertmolecule`. Within the allocator proper there is no code path that restricts link allocation to the `n₀` lineage.

---

### Summary

1. **The link ISA allocator has exactly one allocation path** for LINKATOM: `findisatoinsertmolecule` [granf2.c:158–181], reached unconditionally via `findisatoinsertgr` [granf2.c:142] whenever `subtype == ATOM`.

2. **Every emitted link address has the form `d.0.2.n`** — the element field beyond document `d` is always the two-component suffix `.2.n`. No address deeper than `d.0.2.n` (i.e., no `d.0.2.n.m` or beyond) is reachable from any branch of the function.

3. **The frontier mechanism for link N+1 is `inc(d.0.2.n, 0)` at depth 2** — `tumblerincrement(&lowerbound, 0, 1, isaptr)` [granf2.c:175]. This is the only active allocation path once any link exists in the document. The first link arrives by constructing `d.0.2` then appending `.1` via `rightshift=1`.

4. **The allocator does not restrict home nodes to the `n₀` lineage.** That constraint, if enforced, lives in the bert layer. `findisatoinsertmolecule` only checks that the target document exists in the granfilade.
