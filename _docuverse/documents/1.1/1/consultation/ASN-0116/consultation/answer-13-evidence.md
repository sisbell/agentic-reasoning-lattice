## Question 13 [evidence]

> Does the second-blade computation in `findaddressofsecondcutforinsert` classify POOM entries at or beyond the next subspace boundary as case 2 (no shift), so a text insert at 1.x never displaces link positions at 2.x?

## KB Synthesis

Yes, exactly — and the mechanism is fully documented across several KB entries.

**The knife construction** [SS-TWO-BLADE-KNIFE]: `findaddressofsecondcutforinsert()` takes the insertion point `N.x` and computes `blade[1] = (N+1).1` via three tumbler arithmetic steps. For a text insert at any `1.x` position, `blade[1] = 2.1` unconditionally, regardless of the fractional part.

**The classification** [FC-SUBSPACE] (Finding 0054): `insertcutsectionnd()` runs each POOM crum through `whereoncrum()` against `blade[1]` first. A link crum sitting at V-position `2.1` gets classified as `ONMYLEFTBORDER` (−1) because `2.1 == blade[1]`. The case dispatch treats any result `<= ONMYLEFTBORDER` as **case 2 — no shift** — so the `blade[0]` check is never even reached for that crum.

**The postcondition** [ST-INSERT] (Finding 0054): The shift is bounded to `[blade[0], blade[1])`. Entries at or beyond `blade[1]` satisfy the frame condition `entry.vpos' = entry.vpos`. This generalizes: insert at `2.x` confines shifts to `[2.x, 3.1)`, protecting type-endpoint entries at `3.x`.

**Important contrast** [INT-DELETE-SUBSPACE-ASYMMETRY]: INSERT's subspace isolation is a *deliberate structural guard* — the source code contains explanatory comments about the second-blade design. DELETE achieves the same observable result accidentally via `strongsub`'s exponent guard, which is a fragile arithmetic invariant rather than an intentional boundary. These require different proof strategies in formal verification.

**Empirical confirmation** [FC-SUBSPACE] (Finding 0038, 0067): After inserting text at `1.x` in a document with a link at `2.x`, `find_links` and `follow_link` on the link continue to work — the link's V-position is unchanged.

---

## Code Exploration

---

## Answer: Second-Blade Computation in `findaddressofsecondcutforinsert`

**Yes — the second blade is placed at (N+1).1 for any insert at N.x, and POOM entries whose V-span begins at (N+1).1 or later always receive case 2 (no shift).**

---

### Step-by-step trace of `findaddressofsecondcutforinsert` [`insertnd.c:174–183`]

```c
int findaddressofsecondcutforinsert(tumbler *position, tumbler *secondcut)
{    /*needs this to give it a place to find intersectionof for text is 2.1*/
  tumbler zero, intpart;

       tumblerclear (&zero);
       tumblerincrement (position, -1, 1, secondcut);          // line 179
       beheadtumbler (position, &intpart);                      // line 180
       tumblerincrement(secondcut,0,-tumblerintdiff(&intpart,&zero),secondcut); // line 181
       tumblerincrement (secondcut, 1, 1, secondcut);           // line 182
}
```

**`tumblerincrement(aptr, rightshift, bint, cptr)` [`tumble.c:599–623`]** finds the index `idx` of the last non-zero digit in the mantissa and does `cptr->mantissa[idx + rightshift] += bint`. A `rightshift` of -1 moves one story toward the more-significant (integer) end; +1 moves one story toward the fractional end.

**`beheadtumbler(aptr, bptr)` [`tumble.c:673–683`]** increments `exp` by 1 and zeroes `mantissa[0]` if `exp` was 0, then justifies. This strips the leading story, returning the sub-address.

**Worked example for `position = 1.5`** (mantissa = `[1, 5, 0…]`, exp = 0):

| Line | Operation | Intermediate value |
|------|-----------|-------------------|
| 179 | `tumblerincrement(1.5, -1, 1, secondcut)` | last non-zero idx=1; add 1 to mantissa[1+(-1)]=mantissa[0]; result **2.5** |
| 180 | `beheadtumbler(1.5, &intpart)` | strips integer part 1; `intpart` = **5** |
| 181 | `tumblerincrement(2.5, 0, -5, secondcut)` | last non-zero idx=1; add -5 to mantissa[1]; 5-5=0; result **2** (integer only) |
| 182 | `tumblerincrement(2, 1, 1, secondcut)` | last non-zero idx=0; add 1 to mantissa[0+1]=mantissa[1]; result **2.1** |

The same algebra holds for any `position = N.F`:
1. Line 179 → **(N+1).F**
2. Line 180 → intpart = **F**
3. Line 181 → subtract F from the fractional slot → **(N+1)** (bare integer)
4. Line 182 → append .1 → **(N+1).1**

The function comment confirms this: *"needs this to give it a place to find intersectionof for text is 2.1"* [`insertnd.c:175`].

---

### How the two blades are used in `makegappm` [`insertnd.c:124–172`]

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);          // blade[0] = insertion point
findaddressofsecondcutforinsert(&origin->dsas[V],&knives.blades[1]); // blade[1] = (N+1).1
knives.nblades = 2;
knives.dimension = V;
makecutsnd (fullcrumptr, &knives);
```

After `makecutsnd` splits the tree at both blade positions, the loop over sons calls `insertcutsectionnd` to classify each child [`insertnd.c:151–168`]:

```c
case 0:
case 2:
    break;                // no shift
case 1:
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
    ivemodified(ptr);
    break;                // shifted right by insertion width
```

---

### Classification logic in `insertcutsectionnd` [`edit.c:207–233`]

```c
if (knives->nblades == 2) {
    i = 1;
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME)              return (-1);   // straddles blade — error
    else if (cmp <= ONMYLEFTBORDER) return (2);    // at/right-of blade[1] → no shift
}
i = 0;
cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
if (cmp == THRUME)              return (-1);
else if (cmp <= ONMYLEFTBORDER) return (1);        // at/right-of blade[0] → shift
return (0);                                         // left of blade[0] → no shift
```

**`whereoncrum` for POOM** [`retrie.c:345–373`] computes:
- `left = offset->dsas[V] + ptr->cdsp.dsas[V]` — the absolute V-address of the crum's left border
- Returns `TOMYLEFT` if `address < left`, `ONMYLEFTBORDER` if `address == left`, `THRUME` if `left < address < right`, etc.

So `cmp <= ONMYLEFTBORDER` is true when **the blade address is ≤ the crum's left V-address** — i.e., the entire crum lies at or to the right of the blade.

---

### Applying this to links at 2.x

For an insert at **1.F** (blade[0] = 1.F, blade[1] = 2.1):

| POOM entry left border | vs. blade[1] = 2.1 | Result |
|------------------------|-------------------|--------|
| 2.1 (exactly) | 2.1 == 2.1 → ONMYLEFTBORDER | **case 2 — no shift** |
| 2.2, 2.5, 2.9, … | 2.1 < 2.x → TOMYLEFT | **case 2 — no shift** |
| 1.F (insertion point itself, after cut) | 1.F == 1.F → ONMYLEFTBORDER | case 1 — shift |
| 1.G where G > F | 2.1 > 1.G, TOMYRIGHT; 1.F < 1.G, TOMYLEFT | case 1 — shift |
| 1.G where G < F | left of blade[0] | case 0 — no shift |

Blade[1] is checked **first** [`edit.c:212–221`]. Any POOM crum whose V-span left border is ≥ 2.1 satisfies `cmp <= ONMYLEFTBORDER` on that first check and returns 2 immediately, before blade[0] is ever examined.

The only crums that can fall through to the blade[0] check (and potentially case 1) are those whose left borders lie strictly between 1.F and 2.1 — i.e., within subspace 1, after the insertion point.

---

### Why the boundary is 2.1, not 2.0

The tumbler addressing convention places the first usable content address in subspace N at **N.1**, not N.0. Address 2.0 is the subspace floor, not a real V-location for stored content. Placing the second blade at 2.1 (rather than 2.0) aligns exactly with the first protectable content address in subspace 2 and leaves the gap between the insertion point and 2.1 open for the new content to occupy. A hypothetical entry at 2.0 would fall in the gap between blades and would be classified as case 1 (shift) — but such an entry cannot exist under normal content addressing rules.

---

### Conclusion

**Yes.** `findaddressofsecondcutforinsert` [`insertnd.c:174–183`] always places blade[1] at **(N+1).1** for an insert at N.x. `insertcutsectionnd` [`edit.c:207–221`] checks blade[1] first: any POOM entry whose left V-address is ≥ 2.1 returns **case 2 (no shift)** immediately. A text insert at 1.x therefore never displaces link or content entries whose V-spans begin at 2.x. Only entries within subspace 1 that lie at or after the insertion point (and before 2.1) are shifted.
