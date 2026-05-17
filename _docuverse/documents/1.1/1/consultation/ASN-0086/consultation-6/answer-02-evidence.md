## Question 2 [evidence]

> In udanax-green, does emitting a link at address `a` require prior or implicit emission at all intermediate L1c-chain addresses, or can the allocator deposit directly at `a` while leaving intermediate positions vacant?

## KB Synthesis

The KB does not directly address "L1c-chain" as a named concept, but the link allocation mechanism is fully documented and answers this precisely.

## Link Address Allocation Is Sequential, Not Declarative

From [SS-ADDRESS-ALLOC] / Finding 0065, the MAKELINK allocator uses **query-and-increment within the document's link subspace**:

1. Compute `upperbound = docISA.0.2.3` (bounding to the document's link namespace)
2. Call `findpreviousisagr` to find the highest existing link address below that bound
3. If none exist: allocate at `docISA.0.2.1` (first child directly)
4. Otherwise: increment from `lowerbound` by `0.1`

The postcondition is strictly: `new_link_addr = max_existing_link_in_doc + 0.1`. The caller never specifies a target address — the allocator computes it.

## No Intermediate Positions Are Required

- The allocator only requires that the **home document orgl exists** in the granfilade [PRE-LINK-CREATE]
- No intermediate link addresses must be pre-populated; the first link deposits directly at `docISA.0.2.1`
- The granfilade is a B-tree; containment is checked by tumbler prefix matching ([SS-TUMBLER-CONTAINMENT]), not by existence of intermediate records

## The Invariant This Enforces

From [INV-MONOTONIC] / Finding 0065: link I-address allocation is strictly monotonically increasing and independent across documents. This means there is no mechanism to **skip** to an arbitrary address — but there is equally no requirement to populate any prior addresses, because the allocator always reads the current maximum and steps forward from there.

**Conclusion:** The allocator deposits directly at `max + 1` without requiring intermediate chain positions to exist first. Intermediate positions cannot be left vacant by design — they simply don't exist until a MAKELINK operation naturally reaches them.

---

## Code Exploration

I now have all the source code I need. Here is the complete answer.

---

## Does link emission at address `a` require a contiguous L1c chain?

**No. The allocator deposits directly at the next-after-highest address and makes no pass over intermediate positions. Gaps are structurally permitted and unchecked.**

---

### Call chain (fully confirmed from source)

```
fns.c:100   createlink(taskptr)
  do1.c:195   docreatelink(...)
    do1.c:207     makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)
    do1.c:209     createorglingranf(taskptr, granf, &hint, linkisaptr)
      granf1.c:50   createorglingranf → createorglgr(...)
        granf2.c:117  createorglgr → findisatoinsertgr(fullcrumptr, hintptr, isaptr)
          granf2.c:142  findisatoinsertmolecule(fullcrumptr, hintptr, isaptr)
        granf2.c:125  insertseq(fullcrumptr, isaptr, &locinfo)   ← one node, at isaptr only
```

---

### The one and only prerequisite check

`findisatoinsertgr` [granf2.c:130–156] branches on `hintptr->subtype`:

```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr(fullcrumptr, &hintptr->hintisa)) {   // granf2.c:136
        return (FALSE);          // document must exist
    }
    findisatoinsertmolecule(fullcrumptr, hintptr, isaptr); // granf2.c:142
```

The **only** guard is: *the parent document node must exist in the granfilade*. There is no check that any intermediate link addresses exist.

---

### How `findisatoinsertmolecule` allocates the address

`granf2.c:158–181`, condensed with comments:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

  // Compute the upper bound of this document's link subspace
  tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // line 162

  // Start lowerbound at zero — "nothing found yet"
  clear(&lowerbound, sizeof(lowerbound));                                        // line 163

  // Walk the B-tree to find the HIGHEST existing address below upperbound
  findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);      // line 164

  // LINKATOM branch (line 170–175)
  } else if (hintptr->atomtype == LINKATOM) {
      tumblerincrement(&hintptr->hintisa, 2, 2, isaptr);          // initial candidate
      if (tumblercmp(&lowerbound, isaptr) == LESS)
          tumblerincrement(isaptr, 1, 1, isaptr);                  // candidate + 1
      else
          tumblerincrement(&lowerbound, 0, 1, isaptr);             // lowerbound + 1
  }
```

The algorithm is:
1. Compute a candidate address (the "first" link slot for this document).
2. Find the **highest** address already in the granfilade below the link subspace's upper bound — via `findpreviousisagr`.
3. The new address is `max(candidate, lowerbound) + 1`.

**No iteration over intermediate positions.** If links exist at positions {3, 7, 15} inside the document's link subspace, `findpreviousisagr` returns 15, and the new link is allocated at 16. Positions 1, 2, 4–6, 8–14 are never mentioned, verified, or touched.

---

### What `findpreviousisagr` actually does

`granf2.c:255–278`:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
  ...
  if (crumptr->height == 0) {
      findlastisaincbcgr((typecbc*)crumptr, offset);   // leaf: grab last isa in this CBC
      return(0);
  }
  for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
      if (/* ptr spans or touches upperbound */ || !ptr->rightbro) {
          findpreviousisagr(ptr, upperbound, offset);  // recurse into last candidate child
          return(0);
      } else {
          tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  // accumulate width, skip subtree
      }
  }
}
```

This is a standard "find rightmost under bound" B-tree walk. It **skips entire sibling subtrees** by accumulating their widths, then recurses into only the last qualifying child. The granfilade B-tree is a sparse structure — nodes exist only where data has been inserted. `findpreviousisagr` simply finds whichever of those sparse nodes is the rightmost one under the bound. It has no knowledge of, and makes no claims about, any addresses in between.

---

### Insertion itself

After the address is computed, `createorglgr` [granf2.c:125] calls:

```c
insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);
```

`insertseq` places **exactly one new granfilade node** at `isaptr`. No surrounding or intermediate nodes are created as side effects.

---

### Summary

| Claim | Verdict | Evidence |
|---|---|---|
| Parent document must exist | **Yes** | `granf2.c:136` — `isaexistsgr` on `hintisa` |
| Intermediate link addresses must exist | **No** | `findisatoinsertmolecule` never enumerates them |
| Allocator walks gaps to fill them | **No** | `findpreviousisagr` skips subtrees; `insertseq` inserts one node |
| New address is contiguous with previous | **Only by +1 arithmetic** | `tumblerincrement(..., 0, 1, isaptr)` — adds 1 to the highest existing, but that highest existing may itself be non-contiguous with earlier ones |
| Any contiguity guard clause exists | **No** | Full search of allocation path found none |

The allocator deposits a link at `a = highestExistingLink + 1` and leaves all other addresses untouched. The granfilade is a **sparse** B-tree; vacancies are a normal structural condition, not an error state.
