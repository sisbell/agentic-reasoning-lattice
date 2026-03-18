## Question 13 [gregory]

> The second blade in `findaddressofsecondcutforinsert` computes the boundary tumbler at the next subspace — is this always `2.0` regardless of document structure, or does it dynamically compute the boundary based on the actual next occupied subspace in the POOM?

## KB Synthesis

The second blade is computed by **pure tumbler arithmetic from the insertion V-address alone** — it does not examine the POOM at all.

[SS-TWO-BLADE-KNIFE] (Finding 0054) documents the algorithm in `findaddressofsecondcutforinsert()` at `insertnd.c:174-183`:

1. Increment the first digit of the insertion address: `N.x → (N+1).x`
2. Behead to isolate the fractional tail: `N.x → 0.x`
3. Subtract the fractional part: `(N+1).x - 0.x = (N+1).0`
4. Add 1 at the second digit: `(N+1).0 → (N+1).1`

The result is always `(N+1).1` where `N` is the leading digit of the insertion point. The source comment embedded in the finding — *"needs this to give it a place to find intersectionof for text is 2.1"* — confirms the design intent: for text subspace (N=1), the hardcoded answer is `2.1`.

[FC-SUBSPACE] and [INV-SUBSPACE-CONVENTION] both state the resulting invariant:

> `∀ N ∈ {1,2,3}, ∀ op = INSERT(N.x) : shift_region(op) ⊆ [N.1, (N+1).1)` holds for all insertions.

Concrete examples from [SS-TWO-BLADE-KNIFE]:
```
INSERT at V-position 1.3:  blade[1] = 2.1  (always, regardless of whether 2.x is occupied)
INSERT at V-position 2.5:  blade[1] = 3.1  (always)
```

The function takes only the insertion V-address as input. There is no call to `findorgl`, no POOM traversal, no inspection of what actually occupies adjacent subspaces. The boundary is geometrically fixed to `(N+1).1` by the first digit of the insertion point.

This is what makes subspace isolation structurally guaranteed for INSERT (as opposed to DELETE, where isolation is accidental via the `strongsub` exponent guard — see [INT-DELETE-SUBSPACE-ASYMMETRY]): the knife boundary is determined before any POOM is consulted, making it independent of document content.

---

## Code Exploration

Now I have all the evidence needed. Let me trace the algorithm fully and confirm with the link VSA setup code.

---

## Answer

The second blade in `findaddressofsecondcutforinsert` is **dynamically computed from the integer (subspace) part of `position`** — it is not hardcoded to `2.0`. Furthermore, it produces `(subspace+1).1`, not `(subspace+1).0`.

---

### The Function

```c
// insertnd.c:174-183
int findaddressofsecondcutforinsert(tumbler *position, tumbler *secondcut)
{    /*needs this to give it a place to find intersectionof for text is 2.1*/
  tumbler zero, intpart;
       tumblerclear (&zero);
       tumblerincrement (position, -1, 1, secondcut);
       beheadtumbler (position, &intpart);
       tumblerincrement(secondcut,0,-tumblerintdiff(&intpart,&zero),secondcut);
       tumblerincrement (secondcut, 1, 1, secondcut);
}
```

---

### Step-by-Step Trace

V-space positions are two-story tumblers `s.n` where `s` is the subspace digit and `n` is the offset within that subspace. Text lives at `1.n`, link from-ends at `2.n`, link to-ends at `3.n` — confirmed by `setlinkvsas` [`do2.c:169-183`] and `findnextlinkvsa` [`do2.c:151-167`].

Given `position = 1.5` (text subspace 1, offset 5): mantissa = `[1, 5, 0, …]`, exp=0.

**Step 1** — `tumblerincrement(position, -1, 1, secondcut)` [`tumble.c:599-623`]:
- `idx` = index of last non-zero digit = 1 (mantissa[1]=5)
- copy position → secondcut; then `secondcut->mantissa[1 + (-1)] += 1`, i.e., `mantissa[0] += 1`
- secondcut = `[2, 5, 0, …]` = **2.5**

**Step 2** — `beheadtumbler(position, &intpart)` [`tumble.c:673-683`]:
- `++exp`, clear mantissa[0] since `exp==0` was; after `tumblerjustify`, left-shift by 1
- intpart = `[5, 0, …]` = **5** (the offset-only tail)

**Step 3** — `tumblerincrement(secondcut, 0, -tumblerintdiff(&intpart, &zero), secondcut)`:
- `tumblerintdiff(intpart, zero)` [`tumble.c:591-597`] returns `intpart.mantissa[0]` = 5
- `tumblerincrement([2,5,…], 0, -5, …)`: idx=1, `mantissa[1+0] += -5` → mantissa[1] = 0
- secondcut = `[2, 0, …]` = **2**

**Step 4** — `tumblerincrement(secondcut, 1, 1, secondcut)`:
- idx=0 (mantissa[0]=2); `mantissa[0+1] += 1` → mantissa[1] = 1
- secondcut = `[2, 1, 0, …]` = **2.1**

The same arithmetic for any `1.n` input cancels the offset `n` and produces **2.1** — matching the comment verbatim: `/*needs this to give it a place to find intersectionof for text is 2.1*/`.

For `position = 2.n` (link subspace), the same algebra yields **3.1**, and so on.

---

### The General Formula

For any two-story position `s.n`, the four steps implement:

1. `secondcut = (s+1).n` — bump the subspace digit up by 1, keeping the offset
2. `intpart = n` — extract just the offset
3. `secondcut = (s+1).0` — subtract the offset, zeroing it
4. `secondcut = (s+1).1` — add `.1` to get the first addressable position in the next subspace

Result: **`(s+1).1`** — always the first position of the next subspace, not its zero boundary.

---

### Why `.1` and Not `.0`?

The `.1` is not accidental. The convention throughout the codebase is that all subspaces start at `.1`, never `.0`. From `findvsatoappend` [`orglinks.c:42-43`]:

```c
tumblerincrement (vsaptr, 0, 1, vsaptr); /* no text in doc */
tumblerincrement (vsaptr, 1, 1, vsaptr);
```

This creates `1.1` as the first insertion address. And `setlinkvsas` [`do2.c:169-179`] creates `1.1`, `2.1`, `3.1` for the three link-endpoint subspaces. The cut needs to fall at a real, addressable position that `newfindintersectionnd` can find in the enfilade tree. A cut at `2.0` — a position that is never occupied — could fail to find a valid intersection node.

---

### No POOM Lookup — Pure Arithmetic

The function receives only `position` (the V-address of the insertion point). It does **not** walk the POOM, call `findpreviousisagr`, or inspect what actually occupies the next subspace. The derivation is entirely arithmetic: strip the offset, increment the subspace, re-attach `.1`. If the next subspace is empty in this particular document, the cut still lands at the right geometric position for the gap operation in `makegappm` [`insertnd.c:124-172`].

---

### Summary

| Question | Answer |
|---|---|
| Is the second blade always `2.0`? | No — it is `(subspace+1).1` |
| Is it hardcoded for text? | For text (`s=1`), it always produces `2.1`, but by arithmetic, not by literal constant |
| Does it check the actual next occupied subspace in the POOM? | No — it is pure tumbler arithmetic on `position`, no data structure lookup |
| What happens for link subspaces? | `position = 2.n` → `3.1`; `position = 3.n` → `4.1` |

The comment `"for text is 2.1"` is a concrete example of the general rule: the second blade is always the first address of the next subspace above the insertion position.
