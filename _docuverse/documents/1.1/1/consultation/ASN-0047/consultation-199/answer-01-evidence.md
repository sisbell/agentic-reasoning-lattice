## Question 1 [evidence]

> Does the udanax-green reorder operation permute content among a document's existing V-positions at fixed depth, or can it emit V-positions whose depth differs from the pre-reorder arrangement?

## KB Synthesis

REARRANGE applies pure tumbler arithmetic to V-displacements with no depth guard, so the answer is conditional on cut geometry.

## Normal case: depth is preserved

When all cut points lie within the same subspace (e.g., all in `1.x`), `makeoffsetsfor3or4cuts()` produces offsets by subtracting cut-point pairs ([ST-REARRANGE], Finding 0056):

```
diff[1] = cut2 - cut1
diff[2] = -(cut1 - cut0)
```

These differences are tumblers of the same magnitude as the operands. Applying them via `tumbleradd(&ptr->cdsp.dsas[V], &diff[i], ...)` shifts content within the same subspace — V-positions stay at the same tumbler length and first digit. Content at `1.3` moves to `1.5`, not to `2.2` or `1.3.1`.

## Exceptional case: depth/subspace CAN change

REARRANGE has no knife-blade guard equivalent to INSERT's two-blade boundary ([SS-TWO-BLADE-KNIFE]) or DELETE's `strongsub` exponent guard ([FC-SUBSPACE], Finding 0055). When cut points straddle the `1.x`/`2.x` boundary, the arithmetic silently produces cross-subspace V-positions:

> Pivot with cuts `[1.1, 1.4, 2.5]`: content at V:1.1–1.3 is displaced by `diff[1] = 2.5 - 1.4 = 1.1`, ending up at V:2.2–2.4. ([EC-REARRANGE-CROSS-SUBSPACE], Finding 0051)

This violates [INV-SUBSPACE-CONVENTION] — text bytes end up in the link subspace. The missing precondition is documented in [PRE-REARRANGE] (Finding 0051): "all cut points must lie within the same subspace, OR the resulting displacements must preserve subspace membership for every affected orgl."

## What REARRANGE always preserves

Despite the depth/subspace risk, [INV-REARRANGE-IDENTITY] holds unconditionally: I-addresses are never touched — only `cdsp.dsas[V]` is modified. The multiset of content identities is invariant; only their V-positions change.

---

## Code Exploration

I don't have write permission for findings yet — I'll deliver the answer directly and can write the finding once you grant it.

---

## Answer: V-Position Depth After Rearrange

**Short answer:** Rearrangement does NOT permute content among existing V-positions. It translates sections to new V-addresses by adding computed offsets. The depth of those new addresses is **not invariant** — it can increase when cut positions share a common hierarchical prefix.

---

### Call chain

```
do1.c:34    dorearrange()     → findorgl + rearrangepm
orglinks.c:137  rearrangepm() → rearrangend(docorgl, cutseqptr, V)
edit.c:78   rearrangend()     → makeoffsetsfor3or4cuts + per-node tumbleradd
```

---

### 1. Offset computation — `makeoffsetsfor3or4cuts` [edit.c:164–184]

For a 3-cut rearrange with sorted blade positions b0 < b1 < b2:

```c
tumblersub(&knives->blades[2], &knives->blades[1], &diff[1]);  // b2 − b1
tumblersub(&knives->blades[1], &knives->blades[0], &diff[2]);  // b1 − b0 (negated)
diff[2].sign = !diff[2].sign;
```

`tumblersub` dispatches to `strongsub` when |a| > |b| [tumble.c:534–565]:

```c
answer.exp = aptr->exp;
for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) {
    --answer.exp;           // ← decrements for each shared prefix digit
    ...
}
answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];
for (j = 1; j < NPLACES && i < NPLACES;)
    answer.mantissa[j++] = aptr->mantissa[i++];  // copies remaining digits of a only
```

When the two cut positions share k leading components, `answer.exp` ends up `k` lower than `cut.exp`. Because `tumblerlength = nstories(t) − t.exp` [tumble.c:259–262], a lower `exp` means a **longer, deeper** tumbler. The diff is thus at finer granularity than the cuts themselves.

---

### 2. Offset application — `rearrangend` [edit.c:125]

```c
tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```

`tumbleradd` → `absadd` [tumble.c:444–485] when both are positive. The critical branch when `old_pos.exp > diff.exp`:

```c
} else if (aptr->exp > bptr->exp) {
    answer.exp = aptr->exp;
    temp = aptr->exp - bptr->exp;
    while (i < temp) ansmant[j++] = amant[i++];  // high digits from old_pos
    ansmant[j++] = amant[i++] + bmant[0];          // sum at overlap
    i = 1;
}
while (j <= NPLACES - 1) {
    ansmant[j++] = bmant[i++];  // ← appends diff's finer digits verbatim
}
```

`diff`'s sub-integer components — the ones that sit below the granularity of `old_pos` — are appended into the result's lower mantissa slots. `nstories` grows, so `tumblerlength` of the new position exceeds that of the original. **The translated position is deeper.**

---

### 3. No normalization on retrieval — `context2span` [context.c:206–207]

```c
movetumbler(&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

The stream address is copied straight from the modified POOM node coordinate. No depth normalization. The depth increase is visible to the client.

---

### Depth table

| Cut relationship | `diff.exp` vs `old_pos.exp` | Emitted depth |
|---|---|---|
| Cuts at different top-level positions (no shared prefix) | equal | same as pre-reorder |
| Cuts share k-component common prefix | `old_pos.exp − k` (finer) | deeper by k |
| Cuts are identical | diff = 0 (zero tumbler, no-op) | same as pre-reorder |

---

### Practical consequence

After a rearrange where the cut positions share k prefix components, the translated sections have `tumblerlength = L + k` while the untouched sections (cases 0 and 4 in `rearrangecutsectionnd`, [edit.c:122–123]) remain at depth `L`. A single rearrange can leave the document's content at two different V-address depths simultaneously. There is no code in the rearrange path that enforces or restores a uniform depth.
