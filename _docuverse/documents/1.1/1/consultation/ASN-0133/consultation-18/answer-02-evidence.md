## Question 2 [evidence]

> Is `coverage_G(x)` the (infinite) downward closure `⋃{t : a ≼ t}` of the denoted addresses under the containment order — i.e., non-finite and usable only as a membership test — as distinct from the finite denoted endset `addrs_G(x)`?

## KB Synthesis

Yes. The KB supports this distinction cleanly, though it doesn't use those names explicitly.

**`coverage_G(x)` is the infinite downward closure**

[SS-TUMBLER-CONTAINMENT] gives the membership test directly:

```
contains(B, A)  ⟺  tumblertruncate(A, tumblerlength(B)) = B
```

Because tumblers are digit sequences of fixed internal precision but unbounded conceptual depth ([SS-TUMBLER] Finding 0031: `NPLACES = 16` mantissa, but hierarchy encoded by zero-digit separators), for any address `x` there are infinitely many valid descendant addresses `x.0.1`, `x.0.1.0.1`, `x.0.2`, `x.1`, etc. The set `{t : x ≼ t}` is not enumerable — it can only be tested for membership via truncation-plus-equality, which is exactly what the implementation does. You cannot iterate it.

**`addrs_G(x)` is finite — what `findpreviousisagr` can return**

[SS-ADDRESS-ALLOC] (Finding 0021) shows the allocation algorithm operates on the *finite intersection* of `coverage_G(parent)` with actually-allocated addresses:

1. Compute `upperbound = tumblerincrement(hintisa, depth-1, 1)` — the next sibling of `x`, giving the half-open interval `[x, next_sibling(x))`
2. Call `findpreviousisagr` to find the highest *existing* address in that interval
3. Apply the containment membership test to confirm the result is actually in `coverage_G(x)`

Step 3 is the bug-fix described in [PRE-ADDRESS-ALLOC]: without the membership test, `findpreviousisagr` returns `1.1.0.1.0.1` when allocating under account `1.1.0.2`, because the tumbler order puts `1.1.0.1.0.1 < 1.1.0.2.0.1` yet `1.1.0.1.0.1 ∉ coverage_G(1.1.0.2)`. The fix is to test membership in `coverage_G`, not to enumerate it.

**The allocation invariant makes `addrs_G(x)` finite**

[INV-MONOTONIC] + [INV-NO-IADDR-REUSE]: allocated addresses grow monotonically and are never freed. At any moment `addrs_G(x) = { a ∈ granfilade | x ≼ a }` is finite and enumerable by tree traversal. [SS-ADDRESS-ALLOC] (Finding 0077) also distinguishes two independent finite families partitioned by tumbler range: document addresses via `findisatoinsertnonmolecule` and content I-addresses via `findisatoinsertmolecule` — both finite subsets of their respective `coverage_G` regions.

**Summary**

| | `coverage_G(x)` | `addrs_G(x)` |
|---|---|---|
| Size | Infinite | Finite (grows monotonically) |
| Access | Membership test only (`tumblertruncate + tumblereq`) | Enumerable via `findpreviousisagr` tree traversal |
| Implementation role | Search bound / allocation domain | Actual allocated set |
| KB locus | [SS-TUMBLER-CONTAINMENT] | [SS-ADDRESS-ALLOC], [INV-MONOTONIC] |

The allocation algorithm in [SS-ADDRESS-ALLOC] is best read as: "find `max(addrs_G(x))` and increment" — where `coverage_G(x)` appears only as the domain constraint enforced by the membership test, not as anything enumerated.

---

## Code Exploration

I now have a thorough enough picture of the code to answer. Here is my full analysis:

---

## Answer: `coverage_G(x)` vs `addrs_G(x)` in the udanax-green source

### What the question is really asking

The question distinguishes:

- **`addrs_G(x)`** — the *finite* set of ISA tumbler addresses where bottom crums actually sit in the granfilade
- **`coverage_G(x)`** — the *infinite* downward closure under the containment (prefix) order: `⋃{t : a ≼ t, a ∈ addrs_G(x)}` — all tumblers that have some stored address as a prefix

The short answer is **yes, they are distinct, and the code treats them differently** — but the relationship is more subtle than "coverage = just use a prefix test," because linear tumbler order and containment order are aligned in a way that lets coverage be computed as a linear interval.

---

### 1. `addrs_G(x)` — the finite explicitly-stored set

The granfilade is a sequential (`GRAN`-type) enfilade over ISA space. Each bottom crum (`typecbc`) sits at a specific ISA address, accumulated by summing preceding `cwid.dsas[WIDTH]` values. This finite set of starting offsets **is** `addrs_G(x)`.

Retrieval against `addrs_G` uses **strict equality**:

**`fetchorglgr` — granf2.c:36–40:**
```c
if (!tumblereq((tumbler*)&context->totaloffset, address)) {
    crumcontextfree(context);
    return (NULL);
}
```

**`isaexistsgr` — granf2.c:244–252:**
```c
context = retrieve (crumptr, isaptr, WIDTH);
ret = tumblereq ((tumbler*)&context->totaloffset, isaptr);
contextfree (context);
return (ret);
```

`retrievecrums` / `findcbcseqcrum` (retrie.c:167–188) will navigate to the crum whose linear interval contains the query address, but both callers immediately require `tumblereq` — exact address equality. If the query falls anywhere in the crum's width beyond the crum's starting offset, they return NULL.

This is a lookup into `addrs_G`, not `coverage_G`.

---

### 2. `coverage_G(x)` — the infinite downward closure, expressed as a linear interval

Tumbler addresses have a hierarchical structure. The address `1.1.0.2.0.1` is a *prefix* of `1.1.0.2.0.1.0.3` — the shorter address is the "parent" in the containment order. The `tumblerlength` function measures this depth:

**tumble.c:259–262:**
```c
INT tumblerlength(tumbler *tumblerptr)
{
    return (nstories (tumblerptr) - tumblerptr->exp);
}
```

Because the tumbler linear ordering is compatible with the prefix hierarchy — all descendants of address `a` lie in the linear interval `[a, a')` where `a'` is `a`'s right sibling at its depth — the infinite downward closure collapses to a *finite linear interval* for navigation purposes. The code exploits this in `findisatoinsertnonmolecule`:

**granf2.c:209–240:**
```c
hintlength = tumblerlength (&hintptr->hintisa);
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);  // a'= right sibling of hint
...
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
...
tumblertruncate (&lowerbound, hintlength + depth, isaptr);
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
```

`upperbound` = `hintisa + 1` at one level up = the right sibling of `hintisa`. The range `[hintisa, upperbound)` is exactly `coverage_G(hintisa)` expressed as a linear interval. `findpreviousisagr` searches this interval for the largest existing ISA address, then `tumblertruncate` + `tumblerincrement` derive the next allocation point.

`findisatoinsertmolecule` does the same thing for atom addresses:

**granf2.c:162–163:**
```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

Here `upperbound` = `hintisa` extended 2 levels, incremented — again bounding the scan to addresses within `hintisa`'s coverage.

The code never *enumerates* `coverage_G` — it uses it only to define a search bound for `findpreviousisagr`. The infinite set is never materialized.

---

### 3. The direct containment membership test: `tumbleraccounteq`

There is one function that implements the prefix/containment test directly:

**tumble.c:38–70:**
```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    // aptr = document address, bptr = account address
    // returns TRUE if document is "under" account
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) {
                return(TRUE);  /* Account terminated — document is a descendant */
            }
        } else {
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

This is `b ≼ a` in the containment order — "is `a` in the coverage of `b`?" — and it is called from `bert.c` for access control (`checkforopen`), not from the granfilade retrieval path. It is a **membership test for `coverage_G`**, never an enumeration.

---

### 4. GRANORGL crum width and why it doesn't collapse the distinction

A GRANORGL bottom crum inserted at address `A` does **not** get width 1. It inherits the right portion of the split crum's width:

**insert.c:49–60:**
```c
if (iszerotumbler (&ptr->cwid.dsas[WIDTH])) {  /* last crum in granf */
    tumblerclear (&new->cwid.dsas[WIDTH]);           // new gets width 0 (now last)
    tumblersub (&nextaddress, &offset.dsas[WIDTH], &ptr->cwid.dsas[WIDTH]);
} else {
    dspadd (&offset, &ptr->cwid, &reach, GRAN);
    tumblersub (&reach.dsas[WIDTH], &nextaddress, &new->cwid.dsas[WIDTH]); // new gets [A, old_end)
    tumblersub (&nextaddress, &offset.dsas[WIDTH], &ptr->cwid.dsas[WIDTH]); // old gets [old_start, A)
}
```

A GRANORGL crum at `A` has `cwid = [A, next_crum_start)` — a linear gap, not the containment interval. `whereoncrum` (retrie.c:351–353) tests `address ∈ [offset, offset+cwid)` using linear `intervalcmp`. This linear interval is **not** `coverage_G(A)` — `coverage_G(A)` = `[A, rightSibling(A))` which is determined by the depth of `A`, not by the gap to the next stored address.

That is: two adjacent crums at ISA addresses `1.1.0.1` and `1.1.0.1.0.1` would have the first crum's cwid = exactly `1.1.0.1.0.1 - 1.1.0.1`. `whereoncrum` would return THRUME for the query `1.1.0.1.0.1` when scanning that first crum — but `fetchorglgr` rejects it anyway with the `tumblereq` guard. The cwid is a physical gap, not the hierarchical coverage.

---

### Summary

| Concept | Code implementation | Finite? | Enumerable? |
|---|---|---|---|
| `addrs_G(x)` | `context->totaloffset` for each bottom crum; tested with `tumblereq` | Yes | Yes (tree walk) |
| `coverage_G(x)` | The linear interval `[a, tumblerincrement(a, depth-1, 1))` for each `a ∈ addrs_G`; tested with `tumbleraccounteq` or bounded by `tumblerincrement`-derived `upperbound` in `findpreviousisagr` | No (infinite in principle; bounded by `NPLACES=16` in practice) | No — used only as membership test |

**`coverage_G(x)` is indeed conceptually infinite and non-enumerable.** The granfilade code never walks or materializes it. Instead, it uses `coverage_G` in exactly two ways:

1. **Insertion bounds** — `findisatoinsertnonmolecule` / `findisatoinsertmolecule` compute `upperbound = tumblerincrement(hintisa, depth-1, 1)` to bound `findpreviousisagr` to addresses within `hintisa`'s coverage interval (granf2.c:190, 213).

2. **Membership test** — `tumbleraccounteq` tests `b ≼ a` (is address `a` in the coverage of `b`?) for access control (tumble.c:38).

Neither operation enumerates `coverage_G`. The retrieval path uses only `addrs_G` (exact `tumblereq` match). The distinction is real and operationally enforced.
