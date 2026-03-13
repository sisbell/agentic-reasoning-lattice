## Question 16 [gregory]

> When `findisatoinsertmolecule` or `findisatoinsertnonmolecule` searches for the current maximum I-address, does the search scope itself to the node's address range, or does it walk the entire granfilade and rely on hierarchical tumbler sorting to land in the right region?

## KB Synthesis

Both functions use an **upper-bound constraint** passed to `findpreviousisagr` — the search is bounded, not a global walk.

The mechanism, from [SS-ADDRESS-ALLOC] (Finding 0021):

1. Compute `upperbound = tumblerincrement(hintisa, depth-1, 1)` — this is the *next sibling* of the parent address. For a parent at `1.1.0.1.0.1`, upperbound is `1.1.0.1.0.2`.
2. Call `findpreviousisagr(upperbound)` — finds the highest existing address in the granfilade **strictly below** that bound.
3. Verify the found address actually falls under the parent via tumbler containment check (added to fix Bug 0013, per [PRE-ADDRESS-ALLOC]).
4. If nothing is under the parent: allocate first child at `hintisa.0.1`. Otherwise: truncate-and-increment the found address.

The same pattern holds for `findisatoinsertmolecule` (content allocation), per [SS-ADDRESS-ALLOC] Finding 0065:

> `tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound)` sets document-scoped bound — e.g., upper bound `docISA.2.3` for link allocation within document `docISA`.

So the scoping is **arithmetic**, not structural. The granfilade is a single flat B-tree containing all addresses — document orgls, text atoms, link orgls, version addresses — all interleaved. There is no separate subtree per namespace [SS-ADDRESS-SPACE] Finding 0077:

> Both query the same granfilade tree but search different subtrees [via different upper bounds].

The B-tree traversal in `findpreviousisagr` uses the upper bound to descend into the correct region — it relies on the total tumbler order ([INV-TUMBLER-TOTAL-ORDER]) to efficiently find the maximum below the bound. But without the containment check, the search *can* return an address from an adjacent namespace (the original Bug 0013: searching under account `1.1.0.2` found `1.1.0.1.0.1` because it was the highest address below the computed upper bound, even though it belonged to a different account). The fix added an explicit `tumblertruncate`/`tumblereq` containment check after `findpreviousisagr` returns. [PRE-ADDRESS-ALLOC], [SS-TUMBLER-CONTAINMENT]

---

## Code Exploration

I now have a complete picture. Here is the full answer.

---

## How `findisatoinsertmolecule` / `findisatoinsertnonmolecule` Scope Their Search

**Short answer: neither function scopes itself to the node's address range. Both walk the entire granfilade from the root and rely on hierarchical tumbler sorting—guided by a computed `upperbound`—to land in the right region. Scoping is implicit, not explicit, and can fail (as Bug Fix #2 in the code documents).**

---

### The Core Primitive: `findpreviousisagr`

Both functions delegate the actual search to `findpreviousisagr` [`granf2.c:255–278`]:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);   // leaf: store the last I-addr here
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if (
         (tmp= whereoncrum (ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
        || tmp == ONMYRIGHTBORDER
        || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);   // recurse DOWN
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  // skip this child
        }
    }
}
```

`crumptr` is always the **apex of the full granfilade**, passed down unchanged from the callers (`inserttextgr` [`granf2.c:83–109`] and `createorglgr` [`granf2.c:111–128`]), which both receive it directly as the `fullcrumptr` argument. There is no subtree-scoping step before the call.

The traversal:

1. Iterates through child nodes left-to-right at each level.
2. For each child, calls `whereoncrum` [`retrie.c:345–398`] to compare `upperbound` against the child's I-address interval `[offset, offset + node_width)`. The five results are `TOMYLEFT (-2)`, `ONMYLEFTBORDER (-1)`, `THRUME (0)`, `ONMYRIGHTBORDER (1)`, `TOMYRIGHT (2)` [`common.h:86–90`].
3. If `upperbound` is **within** the child (`THRUME`), **at its right boundary** (`ONMYRIGHTBORDER`), or the child is the **last sibling** (`!ptr->rightbro`), it recurses into that child.
4. Otherwise it adds the child's width to `offset` and moves right.

This is a pure **enfilade descent guided by a target address**. The tree is sorted by I-address; following `upperbound` down the tree routes to the rightmost leaf at or before that bound. No address-range guard is applied to the root call or at any level.

---

### How Each Caller Computes `upperbound`

#### `findisatoinsertmolecule` [`granf2.c:158–181`]

Called for `ATOM` types (text and links inside a document). The upper bound is:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
```

`tumblerincrement(a, rightshift, bint, c)` [`tumble.c:599–623`] finds the last non-zero digit of `a` and adds `bint` at `rightshift` positions further right. So for a document at address `D` with `atomtype = TEXTATOM (1)`:

- `upperbound = D.0.0.(TEXTATOM+1)` = one unit past the last possible text-atom address under this document.

`findpreviousisagr` then descends the entire granfilade following this bound, and returns whatever leaf I-address it hits. No explicit check confirms the result falls under document `D`. The correctness relies entirely on the tumbler ordering placing all of `D`'s atoms strictly below `upperbound`, and nothing from a *different* document being between `D`'s last atom and `upperbound`.

#### `findisatoinsertnonmolecule` [`granf2.c:203–242`]

Called for non-atom types (DOCUMENT, ACCOUNT, NODE). The upper bound is:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
```

For the common case (depth=2, e.g., creating a document under an account at `A`), this is `A.0.1` — one level to the right of `A`'s direct child space, i.e., just past all of `A`'s direct children.

Again, `findpreviousisagr` descends from the root following this bound with no hard scope guard.

---

### The Proof That Scoping Is Not Enforced: Bug Fix #2

The code itself documents the failure mode. In `findisatoinsertnonmolecule` [`granf2.c:219–233`]:

```c
/* BUG FIX #2: Also check if lowerbound is actually under hintisa. If the
   found item is from a different account (e.g., 1.1.0.1.0.1 when creating
   under 1.1.0.2), treat it as if nothing was found. Otherwise documents
   get created under the wrong account. */
lowerbound_under_hint = FALSE;
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
}
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    /* Nothing under this hint - create first child as hintisa.0.1 */
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
} else { ...
```

When creating a document under account `1.1.0.2`, `findpreviousisagr` (starting from the root) could return `1.1.0.1.0.1` — the last document under a *different* account — because that is the rightmost item below `upperbound = 1.1.0.2.0.1`. The post-search truncate-and-compare guard was added specifically because the tree walk does not stay within the hint's subtree.

**`findisatoinsertmolecule` has no equivalent post-search check.** It relies purely on `upperbound` arithmetic being tight enough to exclude other documents' atoms.

---

### Summary

| Function | Starting point | Scope guard | Relies on |
|---|---|---|---|
| `findpreviousisagr` | Root of full granfilade | None | Tumbler total order |
| `findisatoinsertmolecule` | (via above) | None | `upperbound` arithmetic |
| `findisatoinsertnonmolecule` | (via above) | Explicit post-search `lowerbound_under_hint` check | `upperbound` + explicit verification |

The search is a **whole-tree descent guided by an `upperbound`**, not a scoped subtree walk. The hierarchical tumbler sort causes the descent to naturally route toward the target region, but this is an emergent property of the address ordering — not an explicit scope constraint on the traversal. The `findisatoinsertnonmolecule` bug fix is direct evidence that this reliance on ordering alone is insufficient when the target region is empty.
