## Question 5 [evidence]

> Does udanax-green's link allocation primitive (e.g., `findisatoinsertmolecule`) unconditionally enforce sibling-frontier placement, or can callers/code paths produce link addresses that are strict prefix-extensions of existing link addresses?

## KB Synthesis

## Link Allocation: Sibling-Frontier vs Prefix-Extension

The allocation is **unconditionally sibling-frontier**. There is no code path that produces a prefix-extension of an existing link address. But the mechanism differs from the non-molecule case, and the two are worth distinguishing.

---

### How `findisatoinsertmolecule` enforces sibling placement for links

From [SS-ADDRESS-ALLOC / Finding 0065], MAKELINK's allocation sequence is:

1. `upperbound = tumblerincrement(docISA, 2, atomtype+1)` → bounds the search to `docISA.0.2.*` (element-field 2, link subspace)
2. `findpreviousisagr` finds the highest existing address strictly below that bound
3. If none found: allocate at `docISA.0.2.1` (first child)
4. Otherwise: `tumblerincrement(lowerbound, 0, 1, isaptr)` — increment the last significant digit

Step 4 with `rightshift=0` increments only the terminal digit. Given that all existing link addresses live at `docISA.0.2.N`, the result is always `docISA.0.2.N+1`. The concrete example confirms: first link at `1.1.0.1.0.1.0.2.1`, second at `1.1.0.1.0.1.0.2.2`.

A prefix-extension would require allocating `1.1.0.1.0.1.0.2.1.1` — a child of an existing link address. This cannot occur because:

- The range bound `[docISA.0.2, docISA.0.3)` prevents `findpreviousisagr` from returning anything deeper than `docISA.0.2.N`, so there is never a "previous maximum" at the wrong depth.
- `tumblerincrement(docISA.0.2.N, rightshift=0, amount=1)` = `docISA.0.2.N+1` — a sibling, never a child.

---

### Contrast with `findisatoinsertnonmolecule` (documents, versions)

The non-molecule allocator ([SS-ADDRESS-ALLOC / Finding 0021, 0068]) achieves sibling placement differently: it **explicitly truncates** the found address to the parent's depth before incrementing. This is an unconditional structural guard against any address that might exist at unexpected depth.

The molecule allocator has **no truncation step** — it relies purely on the range bound to ensure the found address is always at the correct depth. This is a weaker structural guarantee: if the granfilade ever contained a link address at the wrong depth (e.g., via external manipulation), `findisatoinsertmolecule` would increment from it and produce a child-of-child address rather than a sibling of the top-level links.

Under normal operation this cannot happen because:
- Allocation is the only mechanism that writes into the `docISA.0.2.*` range
- The [INV-ATOMICITY / Finding 0042] single-threaded event loop prevents concurrent allocation races
- [INV-MONOTONIC / Finding 0065] confirms per-document link monotonicity holds, independent of other documents

---

### Summary

`findisatoinsertmolecule` unconditionally enforces sibling-frontier placement for link addresses through **range-constrained search**, not truncation. The range bound `[docISA.0.2, docISA.0.3)` is the critical invariant: it ensures `findpreviousisagr` only ever returns an address at the `docISA.0.2.N` level, from which a `rightshift=0` increment always produces the next sibling. No caller code path produces prefix-extensions under the normal allocation contract.

---

## Code Exploration

I now have all the data I need. Let me write the complete answer.

---

## Does `findisatoinsertmolecule` Unconditionally Enforce Sibling-Frontier Placement?

**Short answer:** Yes — for all stored link addresses — with one important nuance: the enforcement relies on an implicit invariant rather than an explicit guard, and would silently break if that invariant were violated by external means.

---

### The Full Code Path

```
fns.c:createlink
  → do1.c:docreatelink [line 195]
      makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)  [do1.c:207]
    → granf1.c:createorglingranf
    → granf2.c:createorglgr [line 111]
    → granf2.c:findisatoinsertgr [line 130]
         hintptr->subtype == ATOM → findisatoinsertmolecule()  [line 142]
    → granf2.c:findisatoinsertmolecule [line 158]
```

`LINKATOM = 2` and `TEXTATOM = 1` are fixed constants [xanadu.h:145–146]. There is exactly one code path for link allocation; `docreatelink` always calls `createorglingranf` with an `LINKATOM` hint [do1.c:207–209]. No callers bypass this.

---

### What `findisatoinsertmolecule` Actually Does

```c
// granf2.c:158–181
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound); // line 162
    clear (&lowerbound, sizeof(lowerbound));                                       // line 163
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);      // line 164
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {        // line 165
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);              // line 166
        tumblerincrement (isaptr, 1, 1, isaptr);                                   // line 167
    } else if (hintptr->atomtype == TEXTATOM) {
            tumblerincrement (&lowerbound, 0, 1, isaptr);                          // line 169
    } else if (hintptr->atomtype == LINKATOM) {                                    // line 170
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);                        // line 171
        if (tumblercmp (&lowerbound, isaptr) == LESS)                              // line 172
            tumblerincrement (isaptr, 1, 1, isaptr);                               // line 173
        else
            tumblerincrement (&lowerbound , 0, 1, isaptr);                         // line 175
    }
}
```

**`tumblerincrement(base, rightshift, value, result)`** [tumble.c:599–623]:  
finds the last non-zero mantissa position `idx` of `base`, then sets `result.mantissa[idx + rightshift] += value`. A higher `rightshift` means deeper nesting.

So conceptually, for parent document address `D`:

| Call | Effect | Result |
|------|--------|--------|
| `tumblerincrement(&D, 2, 3, &upperbound)` [line 162] | D + 3 at depth+2 | `D.0.3` (search upper bound) |
| `tumblerincrement(&D, 2, 2, isaptr)` [line 171] | D + 2 at depth+2 | `D.0.2` (virtual link-namespace root) |
| `tumblerincrement(D.0.2, 1, 1, isaptr)` [line 173] | D.0.2 + 1 at depth+1 | `D.0.2.1` (first link) |
| `tumblerincrement(&lowerbound, 0, 1, isaptr)` [line 175] | lowerbound + 1 at same depth | `D.0.2.K+1` (next sibling link) |

---

### The Two Branches and Why Neither Produces a Prefix-Extension

**The same-depth branch (lines 165–167)** — triggered when `findpreviousisagr` returns the document `D` itself (i.e., no atoms exist yet):

```c
tumblerincrement(&lowerbound=D, 2, LINKATOM=2, isaptr);  // isaptr = D.0.2
tumblerincrement(isaptr, 1, 1, isaptr);                   // isaptr = D.0.2.1
```

First link = `D.0.2.1`. The intermediate `D.0.2` is never stored.

**The LINKATOM branch (lines 170–175)** — triggered on all subsequent allocations:

- Line 171 computes candidate `D.0.2` (never stored — internal only)
- Line 172: is `lowerbound < D.0.2`?

  - **Yes (line 173):** `tumblerincrement(D.0.2, 1, 1, isaptr)` = `D.0.2.1`  
    This path is taken when no existing link is ≥ `D.0.2` — meaning no links exist yet. `D.0.2.1` is their first assignment.
  
  - **No (line 175):** `tumblerincrement(&lowerbound, 0, 1, isaptr)` = `lowerbound + 1`  
    This path is taken when an existing link address `D.0.2.K` is present. Since `D.0.2.K > D.0.2` (confirmed by `abscmp` at tumble.c:92–110: same `exp`, and mantissa at the K-slot is nonzero while `D.0.2`'s is zero), this always produces `D.0.2.(K+1)` — a sibling.

**The virtual prefix `D.0.2` is never itself stored.** It appears only as an intermediate value in line 171 and is used solely for the `< / ≥` split at line 172. What gets committed to the granfilade (via `insertseq` at granf2.c:125) is always one level deeper than `D.0.2` on the first allocation, or a sibling increment of an existing link on all subsequent ones.

---

### `tumblercmp` Ordering Confirms the Guard Works

```c
// tumble.c:87–111
static INT abscmp(tumbler *aptr, tumbler *bptr)
{
    if (aptr->exp != bptr->exp) {
        return (aptr->exp < bptr->exp) ? LESS : GREATER;
    } else {
        // compare mantissa arrays MSB-first
        for (i = NPLACES; i--;) {
            cmp = *a++ - *b++;
            if (cmp < 0) return LESS;
            if (cmp > 0) return GREATER;
        }
    }
    return EQUAL;
}
```

For `D.0.2.1` vs `D.0.2`: same `exp`, same mantissa prefix through the "2" position, then `D.0.2.1` has `1` where `D.0.2` has `0` → `D.0.2.1 > D.0.2`. The `== LESS` test at line 172 is therefore **false** once any link exists, routing correctly to line 175 (sibling increment) rather than line 173 (first-child creation).

---

### One Implicit Invariant Not Explicitly Checked

The LINKATOM branch does NOT explicitly verify that `D.0.2` is unoccupied before deciding to nest under it at line 173. The code assumes by construction that `D.0.2` is always empty. This invariant holds because:

- No allocation path writes to `D.0.2` directly (the intermediate value is never passed to `insertseq`)
- Text atoms occupy `D.0.1.X` (TEXTATOM = 1, so text virtual root = `D.0.1`)
- Document addresses occupy `A.0.K` (allocated by `findisatoinsertnonmolecule` under a different hint type)
- None of these subspaces produce an address equal to `D.0.2`

If an entry at `D.0.2` existed via some external corruption or bug in a different code path, line 172's `lowerbound = D.0.2` would yield `EQUAL` (not `LESS`), routing to line 175: `tumblerincrement(D.0.2, 0, 1, ...) = D.0.3`. So even in that degenerate case the result would be `D.0.3`, not a prefix-extension of `D.0.2` — though it would then overlap with the upper-bound marker for the next atom type.

---

### Conclusion

**`findisatoinsertmolecule` does enforce sibling-frontier placement among all stored link addresses**, through a combination of:

1. A virtual namespace root `D.0.2` that is computed but never stored
2. A comparison gate (line 172) that routes to sibling-increment (line 175) whenever existing links are present
3. The `tumblercmp` ordering which correctly treats `D.0.2.K > D.0.2`

No caller path — the chain runs exclusively through `docreatelink → createorglingranf → createorglgr → findisatoinsertgr → findisatoinsertmolecule` — can produce a new link address that is a strict prefix-extension of any existing stored link address. The enforcement is implicit (it depends on `D.0.2` being permanently unoccupied) rather than explicit (there is no `isaexistsgr` guard on the virtual prefix before nesting), but the structural invariant is maintained throughout the codebase.
