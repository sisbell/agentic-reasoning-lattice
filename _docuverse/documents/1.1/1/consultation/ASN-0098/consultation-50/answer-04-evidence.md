## Question 4 [evidence]

> Does the allocator guarantee that the set of emitted chain indices for a given origin sub-allocator is always a contiguous initial segment {1, …, m} with no gaps, so that m being the allocated maximum entails 1..m all allocated?

## KB Synthesis

**Short answer: Yes for any single-typed sub-allocator, but no for the text-content sub-allocator when CREATELINK operations intervene.**

## Mechanism

The allocator is stateless query-and-increment. Every allocation call:
1. Runs `findpreviousisagr` to find the highest existing address below a computed upper bound
2. Returns `max + 1`

No address is ever freed from the granfilade (see [INV-NO-IADDR-REUSE], [FC-GRANF-ON-DELETE]). Since each allocation step produces `prev_max + 1` and no addresses are removed, any sub-allocator whose bounded search sees only its own prior allocations will produce the contiguous initial segment {1, …, m}.

## The per-typed sub-allocators

**Link sub-allocator (`docISA.0.2.x`):** [SS-ADDRESS-ALLOC] Finding 0065 shows the upper bound is set to `docISA.2.3`, restricting `findpreviousisagr` to the link element subspace. No other entity type is allocated in this range, so links within a document strictly produce {1, 2, …, m} with no gaps. [INV-MONOTONIC] Finding 0065 confirms monotonicity holds independently per document.

**Document/version sub-allocator:** [SS-ADDRESS-ALLOC] Finding 0021 and Finding 0068 show the same search-and-increment scoped to the parent namespace. [INV-MONOTONIC] Finding 0077 confirms VERSION does not contaminate text allocation (different allocation function: `findisatoinsertnonmolecule` vs. `findisatoinsertmolecule`).

## The gap case: text content interrupted by CREATELINK

[INT-LINK-INSERT] Finding 0063 is the exception. CREATELINK calls `createorglingranf`, which allocates a link orgl via `findisatoinsertnonmolecule`. This allocation advances the granfilade maximum that `findpreviousisagr` will observe when the next text INSERT runs. The concrete result:

```
INSERT "ABC" → I.1, I.2, I.3
CREATELINK   → link orgl consumes space up to ~I.2.0
INSERT "DEF" → allocates I.2.1+ (gap at I.1.4–I.2.0 in text-only subsequence)
```

`compare_versions` returns **2 span pairs** instead of 1, confirming the gap is real and observable. This means the *text-content* sub-allocator does **not** guarantee a contiguous initial segment when CREATELINK intervenes — [INV-MONOTONIC] Finding 0063 explicitly notes: `text_contiguous(insert_a, insert_b) ⟺ ¬∃ alloc_c : time(a) < time(c) < time(b) ∧ alloc_c ∈ content_allocations`.

## Summary

| Sub-allocator | Contiguous {1,…,m}? |
|---|---|
| Link addresses in doc D (`docD.0.2.x`) | **Yes** — bounded search excludes other types |
| Document addresses under account A | **Yes** — uses separate `findisatoinsertnonmolecule` path |
| Text content in doc D, no CREATELINK | **Yes** — monotonic append only |
| Text content in doc D, with CREATELINK | **No** — link orgl allocation creates observable gaps |

---

## Code Exploration

I now have everything I need. Let me compile the complete answer.

---

## Answer: Contiguity of Chain Indices for a Given Origin Sub-Allocator

### The Short Answer

**Yes, the allocator does guarantee a contiguous initial segment {1, …, m} with no gaps**, subject to the single-threaded architecture of the backend. This is not a separately maintained invariant — it is a structural consequence of how `findisatoinsertnonmolecule` works. The proof is in three facts: indices start at 1, each new index is exactly max+1, and ISA addresses are never deleted.

---

### Where "Chain Index" Assignment Happens

All document/link/node ISA allocation passes through:

```
do1.c:makehint()  →  createorglingranf()  →  createorglgr()
  →  findisatoinsertgr()  →  findisatoinsertnonmolecule()  [granf2.c:203]
```

The sub-allocator's "origin" is the `hintisa` field of `typehint` [xanadu.h:152], and the "chain index" is the last significant digit appended to it.

---

### The First Allocation: Always Index 1

`findisatoinsertnonmolecule` [granf2.c:203–242]:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;        // [granf2.c:209]
hintlength = tumblerlength (&hintptr->hintisa);                // [granf2.c:211]
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound); // [granf2.c:213]
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound); // [granf2.c:217]
```

When nothing exists under the hint (fresh sub-allocator):

```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);     // [granf2.c:237]
}
```

`tumblerincrement(aptr, rightshift, bint, cptr)` [tumble.c:599–623] adds `bint` to the position `rightshift` places right of the last non-zero digit:

```c
for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
cptr->mantissa[idx + rightshift] += bint;                      // [tumble.c:621]
```

So for `hintisa = [1,1,0,1]` (e.g., account `1.1.0.1`) with `depth=2`:
- Last non-zero at idx=3, `mantissa[3+2] += 1` → `[1,1,0,1,0,1]`
- First document gets address `1.1.0.1.0.1` — index **1**.

---

### Subsequent Allocations: Always max+1

When a previous address exists under the hint:

```c
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);  // [granf2.c:239]
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr); // [granf2.c:240]
}
```

`lowerbound` is the **greatest** existing address below `upperbound`, found by `findpreviousisagr` [granf2.c:255–278], which recursively traverses the enfilade to find the rightmost entry:

```c
for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
    if (... == THRUME || ... == ONMYRIGHTBORDER || !ptr->rightbro) {
        findpreviousisagr (ptr, upperbound, offset);             // [granf2.c:272]
        return(0);
    } else {
        tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);     // [granf2.c:275]
    }
}
```

So with `lowerbound = [1,1,0,1,0,k]` (current max = k):
- `tumblertruncate` to length 6: unchanged
- `tumblerlength(isaptr)=6 != hintlength=4`, so rightshift=0
- `tumblerincrement(..., 0, 1, ...)` increments last digit: index becomes **k+1**

The pattern is strictly 1, 2, 3, …, m.

---

### ISA Addresses Are Never Deleted

A search across all `.c` files finds no `deleteorgl`, `removeisa`, or granfilade deletion function. The only mutation is `insertseq` [granf2.c:125], which adds entries. Once inserted, an orgl record at an ISA is permanent. Since `findpreviousisagr` scans actual granfilade state, it always sees the true current maximum — there is no way to create a hole by removing index k < m while index m remains.

---

### Digit Type and Overflow Bound

`tdigit` is `typedef UINT` [common.h:57] and `NPLACES` is 16 [common.h:53]. Each digit is a 32-bit unsigned integer. The `+=` at [tumble.c:621] is a raw addition with no carry propagation (only `tumblerjustify` is called after, which normalizes leading zeros, not overflow). Overflow of a single digit would violate contiguity, but only after UINT_MAX ≈ 4×10⁹ allocations under a single origin — practically impossible.

---

### Summary

| Property | Mechanism | Location |
|----------|-----------|----------|
| First index is 1 | `tumblerincrement(hintisa, depth, 1, ...)` when tree is empty | `granf2.c:237` |
| Next index is max+1 | `findpreviousisagr` finds current max; `tumblerincrement(..., 0, 1, ...)` | `granf2.c:217, 240` |
| No gaps from deletion | No delete-orgl function exists anywhere in the codebase | — |
| No skip-allocation | All ISA creation paths go through `findisatoinsertnonmolecule` | `granf2.c:130–156` |

The allocator emits indices strictly as 1, 2, …, m. Knowing m is the maximum entails that all of 1..m have been allocated. The granfilade tree IS the allocation state — there is no separate counter, no freelist, no bitmap for ISA addresses. The contiguity property is not separately maintained; it is structurally entailed by the algorithm.
