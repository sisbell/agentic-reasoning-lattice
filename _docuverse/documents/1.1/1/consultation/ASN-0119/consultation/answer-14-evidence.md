## Question 14 [evidence]

> When a swap moves region `[c,d)` to where `[a,b)` was, can the resulting V-positions of the two regions overlap or collide, or does `rearrangecutsectionnd`'s region classification guarantee a disjoint partition of the new V-space?

## KB Synthesis

## Swap V-Position Overlap Analysis

`rearrangecutsectionnd` guarantees a disjoint partition of the **old** V-space — each POOM crum is assigned to exactly one of the five regions (before, A, M, B, after) and receives the corresponding offset. The question is whether those offsets produce a disjoint partition of the **new** V-space.

### Pivot (3 cuts): disjoint, always

From [ST-REARRANGE] Finding 0056, pivot offsets are:
- Region A (old `[cut0, cut1)`): `diff[1] = cut2 - cut1` → new `[cut0 + size(M2), cut2)`
- Region B (old `[cut1, cut2)`): `diff[2] = -(cut1 - cut0)` → new `[cut0, cut0 + size(M2))`

Region B ends at `cut0 + size(M2)`, which equals region A's new start. Adjacent and non-overlapping regardless of relative sizes.

### Swap (4 cuts): disjoint **only when** `size(A) = size(B)`

The offsets from [ST-REARRANGE] Finding 0056:
- Region A: `diff[1] = cut2 - cut0` → lands at `[cut2, cut2 + size(A))`
- Middle M: `diff[2] = size(B) − size(A)` → lands at `[cut0 + size(B), cut0 + size(B) + size(M))`
- Region B: `diff[3] = -(cut2 − cut0)` → lands at `[cut0, cut0 + size(B))`

**Overlap condition — middle M vs region A:**

M ends at `cut0 + size(B) + size(M)`. A starts at `cut2 = cut0 + size(A) + size(M)`.

Overlap iff `cut0 + size(B) + size(M) > cut0 + size(A) + size(M)`, i.e., **`size(B) > size(A)`**.

Concrete example: cuts at 2, 4, 6, 9 (A = "BC" size 2, M = "DE" size 2, B = "FGH" size 3):
- M "DE" shifts to `[5, 7)` — diff[2] = +1
- A "BC" shifts to `[6, 8)` — diff[1] = +4
- **Overlap at `[6, 7)`**

The KB's own example ([ST-REARRANGE] Finding 0056) uses equal-sized regions (`1.2, 1.4, 1.6, 1.8`), masking this issue.

### Why the implementation permits this

[EC-REARRANGE-CROSS-SUBSPACE] notes that offsets are "computed purely from tumbler arithmetic with no... validation." The `rearrangecutsectionnd` classification is correct; the fault is that `diff[1]` uses `cut2 − cut0` (= `size(A) + size(M)`) rather than the geometrically correct `cut3 − cut1` (= `size(B) + size(M)`). These coincide only when `size(A) = size(B)`.

When `size(B) > size(A)`, the result violates [INV-POOM-BIJECTIVITY] — multiple POOM entries occupy the same V-address range — in the same way DELETE can produce invalid states [INV-POOM-BIJECTIVITY]. The KB does not document this as an explicit precondition on swap.

**Summary:** `rearrangecutsectionnd` guarantees disjoint old-V classification. For swaps, disjoint new-V positions are only guaranteed when the two swapped regions are equal in size; unequal sizes can produce overlapping V-assignments between the middle region and the displaced region A.

---

## Code Exploration

Now I have all the source data I need. Let me write the complete analysis.

---

## Answer: V-Position Overlap in `rearrangecutsectionnd` Swaps

### The Short Answer

`rearrangecutsectionnd` **guarantees a disjoint partition of pre-move crums** (each crum falls in exactly one region), but the resulting V-positions after the move are collision-free **only if the two swapped regions have equal length**. If `[a,b)` and `[c,d)` have different sizes, the offset arithmetic produces collisions or gaps.

---

### What `rearrangecutsectionnd` Actually Does

`backend/edit.c:191–204`:

```c
INT rearrangecutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
  INT i, cmp;
    for (i = knives->nblades -1; i >= 0 ; --i) {
        cmp = whereoncrum (ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp == THRUME) {
            return (-1);                      // crum spans a cut — fatal
        } else if (cmp <= ONMYLEFTBORDER) {
            return (i+1);                     // crum is in region i+1
        }
    }
    return (0);                               // crum is in region 0 (before all cuts)
}
```

With N sorted cuts C₀ < C₁ < … < Cₙ₋₁, this creates **N+1 disjoint regions** of the original V-space:

| Region | V-interval (before move) |
|--------|--------------------------|
| 0 | (−∞, C₀) |
| 1 | [C₀, C₁) |
| 2 | [C₁, C₂) |
| … | … |
| N | [Cₙ₋₁, +∞) |

The guard at `edit.c:197–198` is the enforcement mechanism: if `whereoncrum` returns `THRUME` (meaning the cut address falls *inside* the crum's interval, `retrie.c:367`), the function returns `−1`, which `rearrangend` treats as a fatal error (`edit.c:118`: `gerror("rearrangend can't classify crum")`). This pre-condition — that cuts were placed at crum boundaries by `makecutsnd` — ensures the classification is exhaustive and disjoint over the existing crums.

---

### The Offset Arithmetic — Where Collision Risk Lives

The V-movement is computed in `backend/edit.c:164–183`:

```c
int makeoffsetsfor3or4cuts(typeknives *knives, tumbler diff[])
{
    if (knives->nblades == 4) {
        tumblersub (&knives->blades[2], &knives->blades[0], &(diff[1]));  // diff[1] = C₂ - C₀
        tumblersub (&knives->blades[1], &knives->blades[0], &a);           // a = C₁ - C₀ (len of R1)
        tumblersub (&knives->blades[3], &knives->blades[2], &b);           // b = C₃ - C₂ (len of R3)
        tumblersub (&b, &a, &(diff[2]));                                   // diff[2] = (C₃-C₂)−(C₁-C₀)
        movetumbler (&diff[1], &diff[3]);
        diff[3].sign = !diff[1].sign;                                      // diff[3] = −(C₂−C₀)
    }
}
```

Applied in `rearrangend` (`edit.c:124–126`) to each crum by region:

```c
case 1: case 2: case 3:
    tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```

So the three moving regions shift by:

| Region | Before | Shift | After |
|--------|--------|-------|-------|
| R1 = [C₀, C₁) | length = L₁ | +diff[1] = +(C₂−C₀) | [C₂, C₂+L₁) |
| R2 = [C₁, C₂) | length = G | +diff[2] = +(C₃−C₂)−L₁ | [C₁+(C₃−C₂−L₁), C₂+(C₃−C₂−L₁)) |
| R3 = [C₂, C₃) | length = L₃ | +diff[3] = −(C₂−C₀) | [C₀, C₀+L₃) |

For R2_new to be adjacent to R1_new (no gap, no overlap):

```
end(R2_new) = C₁ + (C₃−C₂−L₁) + G
            = C₁ + C₃ − C₂ − L₁ + (C₂−C₁)
            = C₀ + C₃ − C₂
            = C₀ + L₃

start(R1_new) = C₂
```

These are equal only when **C₀ + L₃ = C₂**, i.e., **L₃ = C₂ − C₀**. But C₂ − C₀ = C₁ − C₀ + C₂ − C₁ = L₁ + G, so:

> **Disjointness requires L₃ = L₁ + G**, which for adjacent regions (G=0, C₁=C₂) reduces to **L₁ = L₃**.

---

### Concrete Proof of Collision with Unequal Regions

Let `[a,b)=[0,3)` and `[c,d)=[5,9)` — L₁=3, L₃=4, gap=2.

```
diff[1] = 5−0 = 5
diff[2] = (9−5)−(3−0) = +1
diff[3] = −5
```

New positions:
- R1 [0,3) → [5, 8)
- R2 [3,5) → [4, 6)
- R3 [5,9) → [0, 4)

**R1_new [5,8) and R2_new [4,6) overlap at [5,6). Collision confirmed.**

With the reverse (L₁=5, L₃=2, `[0,5)` and `[7,9)`):

```
diff[1]=7, diff[2]=2−5=−3, diff[3]=−7
```
- R1 [0,5) → [7, 12)
- R2 [5,7) → [2, 4)
- R3 [7,9) → [0, 2)

R2_new ends at 4, R1_new starts at 7 — **gap at [4,7)**. No overlap here, but V-space is not contiguous.

---

### What the Classification Guarantee Covers vs. Does Not Cover

| Property | Guaranteed by `rearrangecutsectionnd`? |
|----------|----------------------------------------|
| Each pre-move crum classified into exactly one region | **Yes** — enforced by the `THRUME` guard at `edit.c:197` |
| No crum straddles a cut after `makecutsnd` | **Yes** — `makecutsnd` splits crums at cut points before classification |
| Post-move V-positions are disjoint (equal-length swap) | **Yes** — offset formula produces perfect rotation |
| Post-move V-positions are disjoint (unequal-length swap) | **No** — offset formula produces collisions or gaps |

---

### Conclusion

`rearrangecutsectionnd` guarantees a **disjoint partition of crums over the pre-move V-space**: every crum is assigned to exactly one region, and the `THRUME` guard (`edit.c:197–198`) makes it a hard error if any crum straddles a cut. This is an ironclad invariant maintained by `makecutsnd` + `rearrangecutsectionnd` together.

However, the disjointness of the **post-move V-space** is a property of the offset values computed in `makeoffsetsfor3or4cuts` (`edit.c:169–176`), not of the classification function itself. The offsets implement a cyclic rotation, which is collision-free only when the two swapped regions `[C₀,C₁)` and `[C₂,C₃)` have equal length. When they differ, `diff[2]` (the middle-gap correction) is either not enough or too much, causing R1_new and R2_new to overlap or leave a gap. The code imposes no explicit constraint on equal lengths before invoking the swap — callers are responsible for that invariant.
