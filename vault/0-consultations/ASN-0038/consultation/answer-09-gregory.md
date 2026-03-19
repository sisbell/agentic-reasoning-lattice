## Question 9 [gregory]

> Is the set of baptized positions at any given level always a contiguous prefix (1 through N with no gaps), or can gaps exist between baptized positions?

## KB Synthesis

## Baptized Positions: Contiguous Prefix or Gapped?

Within a **single, homogeneous allocation namespace**, baptized positions always form a contiguous prefix 1 through N with no gaps. Within **mixed-type namespaces**, gaps can appear.

---

### Why contiguous within a homogeneous namespace

The allocation algorithm in [SS-ADDRESS-ALLOC] / [ST-ADDRESS-ALLOC] (Finding 0021) guarantees this structurally:

1. **First allocation is always `.1`** — if nothing exists under the parent, `findisatoinsertnonmolecule` places the first child at `parent.0.1`
2. **Each subsequent allocation is `max_existing + 1`** — `findpreviousisagr` finds the highest existing address under the parent, then `tumblerincrement` steps it by 1
3. **Truncation handles deeper entities** — if the highest address found is a sub-entity (e.g., content within document 1), it is truncated to the target depth before incrementing, so it yields the correct sibling, not a gap

For example, allocating version 2 of `1.1.0.2.0.1` when version 1 already has content at `1.1.0.2.0.1.1.3.0.1.5`:
- Found max: `1.1.0.2.0.1.1.3.0.1.5`
- Truncated to version depth (length 6): `1.1.0.2.0.1.1`
- Incremented: `1.1.0.2.0.1.2` — no gap

[INV-MONOTONIC] (Findings 0033, 0061, 0065, 0068) and [INV-NO-IADDR-REUSE] (Finding 0061) reinforce this: the granfilade is append-only ([FC-GRANF-ON-DELETE]), so all previously baptized addresses remain in the tree permanently and continue to anchor the allocation sequence. There is no free-list and no address reuse, so the sequence cannot develop retroactive holes.

Version addresses specifically: "[d]eleting a version does not remove its address from the granfilade... the next version will be allocated after the deleted one" — creating `.1`, deleting it, then creating again yields `.2`, not `.1` reused. [SS-VERSION-ADDRESS] (Finding 0068).

---

### Where gaps do appear

Gaps exist when **different entity types share the same bounded allocation subspace**. The canonical case is documented in [INT-LINK-INSERT] (Finding 0063):

- INSERT "ABC" → text I-addresses `I.1, I.2, I.3`
- CREATELINK → link orgl allocated at `~I.2.0` (same granfilade region, different element field)
- INSERT "DEF" → text I-addresses `I.2.1+` (non-contiguous with ABC)

`compare_versions` reports two span pairs because the text-only I-address subsequence has a gap caused by the intervening link orgl allocation.

This occurs because `findisatoinsertmolecule` searches the granfilade maximum regardless of entity type — it sees the link orgl's address as the new maximum and allocates above it. [SS-ADDRESS-ALLOC] (Finding 0077): "Both query the same granfilade tree but search different subtrees" — but only when allocation bounds are properly partitioned. Text and link content I-addresses have separate bounds (`docISA.3.x` vs `docISA.2.x`) per Finding 0065, which prevents cross-type pollution for link-vs-text allocation within a document.

---

### Summary

| Namespace | Contiguous? | Evidence |
|-----------|-------------|----------|
| Document addresses under an account | Yes | [ST-ADDRESS-ALLOC] (0021), [INV-MONOTONIC] |
| Version addresses under a document | Yes | [SS-VERSION-ADDRESS] (0068), [INV-NO-IADDR-REUSE] |
| Link I-addresses under a document | Yes | [SS-ADDRESS-ALLOC] (0065) — bounded to `docISA.2.x` |
| Text content I-addresses (when no links created) | Yes | [INV-MONOTONIC] (0033) |
| Text content I-addresses (when links interleaved) | **No** | [INT-LINK-INSERT] (0063) — link orgl allocation creates gaps |

---

## Code Exploration

I now have everything needed for a complete answer. Here is the full analysis with code citations:

---

## Answer: Baptized Positions Are Always a Contiguous Prefix — No Gaps

The set of baptized positions at any given level is **always a contiguous prefix 1 through N**. The allocation algorithm guarantees this by construction, and there is no mechanism that could produce gaps.

---

### What "Baptism" Is

In udanax-green, "baptizing" a position means assigning a new ISA (Internal Storage Address, represented as a tumbler) to a new object (document, link, text atom, etc.) in the granfilade. The assignment is permanent — once an ISA is issued, it is never revoked or reused.

There are two allocation paths depending on the kind of object being created.

---

### Path 1: Non-atom objects (documents, nodes, versions)

`findisatoinsertnonmolecule` [**granf2.c:203–242**] handles documents, accounts, and nodes.

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound, truncated;
  INT depth, hintlength;
  bool lowerbound_under_hint;

    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;   // [209]
    hintlength = tumblerlength (&hintptr->hintisa);            // [211]
    tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound); // [213]
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound); // [217]

    lowerbound_under_hint = FALSE;
    if (!iszerotumbler(&lowerbound)) {
        tumblertruncate(&lowerbound, hintlength, &truncated);  // [231]
        lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa); // [232]
    }

    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr); // [237]: first child → hintisa.0.1
    } else {
        tumblertruncate (&lowerbound, hintlength + depth, isaptr);  // [239]
        tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr); // [240]: max+1
    }
}
```

The two branches are:
- **Empty tree**: first baptized position is `hintisa.0.1` [granf2.c:237] — i.e., position 1 under the hint.
- **Items exist**: new position is `truncate(highest_existing, depth) + 1` [granf2.c:239–240] — i.e., the next sequential value after the current maximum.

The inner search is `findpreviousisagr` [**granf2.c:255–278**], which walks the granfilade tree to find the strict maximum under the upper bound:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);  // [264]: bottom: report ISA
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if ((tmp = whereoncrum(ptr, offset, upperbound, WIDTH)) == THRUME
        ||  tmp == ONMYRIGHTBORDER
        ||  !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset); // [272]: descend into rightmost child
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset); // [275]: accumulate width
        }
    }
}
```

This recursively descends into the rightmost child at each level [granf2.c:272], accumulating widths [granf2.c:275] until it reaches the bottom crum, where `findlastisaincbcgr` [granf2.c:280–284] returns the address of the rightmost atom:

```c
int findlastisaincbcgr(typecbc *ptr, typeisa *offset)
{
    if (ptr->cinfo.infotype == GRANTEXT)
        tumblerincrement (offset, 0, (INT) ptr->cinfo.granstuff.textstuff.textlength - 1, offset); // [283]
}
```

The result is the true maximum ISA in the subtree. There is no case where a value is skipped.

---

### Path 2: Atom objects (text content, links)

`findisatoinsertmolecule` [**granf2.c:158–181**] handles text atoms and link atoms. It also calls `findpreviousisagr` [granf2.c:164] to find the current maximum, then increments from it:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound); // [162]
findpreviousisagr (..., &upperbound, &lowerbound);                            // [164]
if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);             // [166]
    tumblerincrement (isaptr, 1, 1, isaptr);                                  // [167]: +1
} ...
```

Again: find current maximum, add 1.

---

### The Increment Primitive

`tumblerincrement` [**tumble.c:599–623**] always adds a fixed integer `bint` (always `1` in the allocation calls) at a specific digit position — never randomly, never with gaps:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    ...
    for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);  // [611]: find last non-zero
    cptr->mantissa[idx + rightshift] += bint;  // [621]: add 1 at next position
    tumblerjustify (cptr);
}
```

---

### Why No Gaps Can Appear

**1. Allocation is always max+1.** Every new ISA is computed as: find the current highest, add 1 at the correct depth. There is no skipping, no random assignment, no reservation.

**2. Granfilade objects are never deleted.** The FEBE protocol has no `deletedocument`, `deletelink`, or equivalent operation. `dodeletevspan` [do1.c] removes virtual content from a document's POOM/spanfilade, not the document's ISA entry from the granfilade. Since granfilade entries are never removed, `findpreviousisagr` always returns the true historical maximum, never a value below it.

**3. The `lowerbound_under_hint` check prevents false maxima.** The bug fix at [granf2.c:228–233] ensures that if `findpreviousisagr` returns an address from a different parent (e.g., from account 1.1.0.1 when allocating under 1.1.0.2), it is ignored and the first-child address (.0.1) is used instead. This prevents contamination but does not create gaps — it produces the correct position 1 in a fresh namespace.

**4. No free-list, no recycling.** There is no data structure that tracks available or freed position slots. No function searches for holes to fill.

---

### Concrete Example

Under account `1.1`:
- `docreatenewdocument` calls `makehint(ACCOUNT, DOCUMENT, ...)` [do1.c:239], setting depth=2
- First document: `findpreviousisagr` finds nothing → first address is `1.1.0.1` [granf2.c:237]
- Second document: `findpreviousisagr` finds `1.1.0.1` → new address is `1.1.0.2` [granf2.c:239–240]
- Third document: `findpreviousisagr` finds `1.1.0.2` → new address is `1.1.0.3`

The document namespace under any account is always `1.1.0.1`, `1.1.0.2`, ..., `1.1.0.N` — a perfect contiguous prefix. Versions follow the same pattern under their parent document address.

---

### Conclusion

**Baptized positions at every level are always a contiguous prefix `1` through `N` with no gaps.**

The allocation algorithm (`findisatoinsertnonmolecule`, `findisatoinsertmolecule`) invariably finds the current maximum and assigns max+1. No mechanism exists to skip positions, and no mechanism exists to reclaim or free positions once assigned. The granfilade never loses a baptized entry, so the maximum is always accurately reported to subsequent allocations.
