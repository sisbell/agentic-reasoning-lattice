## Question 18 [gregory]

> If a document has two non-contiguous POOM crums mapping to I-addresses `[.0.1.1, .0.1.3]` and `[.0.1.7, .0.1.9]`, and a DELETE removes the first crum entirely, does the second crum shift left by exactly the V-width of the first crum, and is the resulting V-position computed by `tumblersub(original_vpos, deleted_width)` or by some other mechanism?

## KB Synthesis

## Delete Mechanics for Two Non-Contiguous Crums

Synthesizing from the KB:

### Phase 1 — Cutting

[PRE-DELETE] Finding 0075 and [SS-WHEREONCRUM]: `makecutsbackuptohere` only calls `slicecbcpm` when `whereoncrum() == THRUME` (strictly interior). If the deletion boundaries align exactly with Crum A's grasp and reach, both return `ONMYLEFTBORDER` and `ONMYRIGHTBORDER` respectively — no cutting occurs. Crum A is handled whole in Phase 2.

### Phase 2 — Classification and Action

[ST-DELETE] Finding 0075 and edit.c:31-76: `deletend` applies a two-case classification to each crum:

- **Crum A** (entirely within deletion range): **Case 1** → `disown` + `subtreefree`. The crum and its children are physically removed from the tree and freed.
- **Crum B** (entirely after the deletion range): **Case 2** → the shift is applied:
  ```c
  tumblersub(&ptr->cdsp.dsas[V], width, &ptr->cdsp.dsas[V])
  ```
  where `width` is the deletion's V-span width.

### The Exponent Guard — Critical Caveat

[ST-DELETE] Finding 0055 corrects Finding 0053: `tumblersub` delegates to `strongsub`, which has an exponent guard:

> `if (bptr->exp < aptr->exp) { movetumbler(aptr, cptr); return(0); }`

So the shift **only occurs when** `width.exp >= crum_B.vpos.exp`.

- **Same exponent (typical text crums):** `deleted_width.exp = crum_B.vpos.exp = -1` → condition false → subtraction proceeds → result = `original_vpos - deleted_width` (exact shift by Crum A's V-width)
- **Cross-exponent (e.g., link crum at exp=0 vs text deletion at exp=-1):** condition true → `strongsub` returns Crum B's position unchanged — no shift. This is the mechanism behind [FC-SUBSPACE] subspace isolation for DELETE.

### Relative Addressing

[INV-ENFILADE-RELATIVE-ADDRESSING] Finding 0066: The `tumblersub` operates on `ptr->cdsp.dsas[V]` — the **relative** displacement stored in the crum node, not an absolute V-position. After all crums are processed, `setwispupwards` recalculates the root's minimum displacement across all remaining children, adjusting the absolute interpretation accordingly.

### Summary

For two same-exponent text crums where the first is removed entirely:

1. Crum A → Case 1 → physically freed from tree
2. Crum B → Case 2 → `tumblersub(original_cdsp, deleted_width)` shifts it left by exactly Crum A's V-width
3. The mechanism is `tumblersub` (via `strongsub`) on the relative `cdsp.dsas[V]` field
4. `setwispupwards` + `recombine` finalize tree structure

The `original_vpos - deleted_width` result holds precisely when both operands share the same exponent. Cross-exponent cases produce a no-op shift — not a different computation, but `strongsub` short-circuiting to return the original value unchanged [SS-TUMBLER] Finding 0055.

---

## Code Exploration

Now I have everything I need. The code is fully traced. Here is the complete answer.

---

## How V-Positions Shift After Deletion in the POOM Enfilade

### The Short Answer

Yes. The second crum shifts left by **exactly** the V-width of the deleted region. The mechanism is:

```c
tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```
— `edit.c:63`

This is a direct application of `tumblersub`, not a relative mechanism.

---

### Step-by-Step Trace

#### 1. Entry: `deletend` — `edit.c:31-76`

`dodeletevspan` calls into `deletend(fullcrumptr, origin, width, index)` where `index` is the V dimension.

```c
movetumbler(origin, &knives.blades[0]);           // knife[0] = start of delete
tumbleradd(origin, width, &knives.blades[1]);     // knife[1] = start + width
knives.nblades = 2;
makecutsnd(fullcrumptr, &knives);                  // split crums at both boundaries
newfindintersectionnd(fullcrumptr, &knives, &father, &foffset); // find common parent
```
— `edit.c:40-45`

`makecutsnd` ensures no crum straddles either knife. After this call, every node in the tree lies **entirely within one inter-knife interval**: before `origin`, between `origin` and `origin+width`, or after `origin+width`.

#### 2. Classification: `deletecutsectionnd` — `edit.c:235-248`

The loop then iterates direct children of `father` and classifies each:

```c
for (ptr = (typecuc*)findleftson(father); ptr; ptr = next) {
    switch (deletecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives)) {
      case 0: break;                                    // before delete range — unchanged
      case 1: disown(ptr); subtreefree(ptr); break;    // inside delete range — freed
      case 2:
        tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
        break;                                          // after delete range — shifted
    }
}
```
— `edit.c:47-72`

`deletecutsectionnd` works by iterating knives from last to first and calling `whereoncrum`:

```c
for (i = knives->nblades-1; i >= 0; --i) {
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME) return (-1);
    else if (cmp <= ONMYLEFTBORDER) return (i+1);
}
return (0);
```
— `edit.c:239-247`

#### 3. `whereoncrum` — `retrie.c:345-398`

For POOM nodes (and SPAN), this computes:

```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);  // absolute V-start
tumbleradd(&left, &ptr->cwid.dsas[index], &right);                 // absolute V-end
```
— `retrie.c:356, 364`

The return codes are defined in `common.h:87-89`:

```c
#define ONMYLEFTBORDER  -1    // knife == crum's left edge
#define THRUME           0    // knife is inside crum
#define ONMYRIGHTBORDER  1    // knife == crum's right edge
// TOMYLEFT = <-1 (knife is left of crum)
// TOMYRIGHT = >1 (knife is right of crum)
```

So `cmp <= ONMYLEFTBORDER` means the knife is **at or left of** the crum's left edge — i.e., the crum starts **at or after** this knife.

With two knives (`blades[0]` = `origin`, `blades[1]` = `origin + width`):

| i | Knife | `cmp <= ONMYLEFTBORDER` means | Returns |
|---|-------|-------------------------------|---------|
| 1 | `origin+width` | crum starts at or after end of delete | 2 — **after delete range** |
| 0 | `origin` | crum starts at or after start but before end | 1 — **inside delete range** |
| — | (neither) | crum is before `origin` | 0 — **before delete range** |

#### 4. The Position Update — `edit.c:63`

For **case 2** (crum is after the deleted region):

```c
tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

`ptr->cdsp.dsas[index]` is the crum's **V-displacement relative to its parent**. Subtracting `width` from it reduces the crum's contribution to the accumulated absolute V-address by exactly `width`. When the tree is subsequently traversed to compute an absolute address via `prologuend`:

```c
dspadd(offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);   // grasp = offset + cdsp
```
— `retrie.c:336`

the accumulated result is now `width` smaller — exactly as if the crum shifted left by the deleted V-width.

#### 5. `tumblersub` — `tumble.c:406-440`

```c
int tumblersub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
    if (iszerotumbler(bptr))
        movetumbler(aptr, cptr);
    else if (tumblereq(aptr, bptr))
        tumblerclear(cptr);
    else if (iszerotumbler(aptr)) {
        movetumbler(bptr, cptr);
        cptr->sign = !cptr->sign;
    } else {
        movetumbler(bptr, &temp);
        temp.sign = !temp.sign;
        tumbleradd(aptr, &temp, cptr);     // c = a + (-b)
    }
    tumblerjustify(cptr);
}
```
— `tumble.c:406-440`

This is full arbitrary-precision tumbler subtraction implemented as negated addition. No special-casing for the enfilade structure — it is purely arithmetic on the tumbler representation.

#### 6. Post-deletion cleanup — `edit.c:74-75`

```c
setwispupwards(father, 1);
recombine(father);
```

These revalidate the tree's **width** (`cwid`) fields bottom-up and may merge underfull nodes. They do **not** re-adjust V-positions — that already happened at `edit.c:63`.

---

### Applied to Your Scenario

Given:
- Crum A: I-addresses `[.0.1.1, .0.1.3]`, V-displacement `V_A` (relative to parent), V-width `W_A`
- Crum B: I-addresses `[.0.1.7, .0.1.9]`, V-displacement `V_B` (relative to parent)
- DELETE removes crum A entirely (origin = absolute V-start of A, width = `W_A`)

After `makecutsnd`, the tree has clean split points. In `deletend`'s loop:
- Crum A → `case 1` → `disown` + `subtreefree` (deleted) — `edit.c:59-60`
- Crum B → `case 2` → `tumblersub(&B->cdsp.dsas[V], W_A, &B->cdsp.dsas[V])` — `edit.c:63`

Crum B's stored displacement becomes `V_B − W_A`. Its observable absolute V-address decreases by exactly `W_A`. The shift is **computed by `tumblersub`** applied to `cdsp.dsas[V]` directly, not by any relative-offset cascade or parent node adjustment.

If Crum B is not a direct child of `father` but is a descendant of one, the same `tumblersub` is applied to its **ancestor** that is a direct child of `father`, which shifts the entire subtree — and Crum B's position within that subtree is unchanged, but its absolute V-address shifts by exactly `W_A` regardless.

---

### Summary Table

| Claim | Source |
|-------|--------|
| Delete range set up as 2-knife cut | `edit.c:40-44` |
| Crums split at knife boundaries before iteration | `edit.c:44` (`makecutsnd`) |
| Parent node of affected region located | `edit.c:45` (`newfindintersectionnd`) |
| Case 2 = crum is after the delete range | `edit.c:243-244`, `retrie.c:356-372` |
| V-position adjusted by `tumblersub` on `cdsp.dsas[V]` | `edit.c:63` |
| `width` argument is the exact V-width of the deleted region | `edit.c:31` (parameter), `edit.c:41` |
| `tumblersub(a, b, c)` computes `c = a − b` via negated `tumbleradd` | `tumble.c:426-428` |
| `cdsp.dsas[V]` is V-displacement relative to parent | `retrie.c:336` (`prologuend`: `grasp = offset + cdsp`) |
| No further adjustment during `setwispupwards`/`recombine` | `edit.c:74-75` (these fix widths, not positions) |
