## Question 15 [gregory]

> If a 3-cut pivot is issued where cut `a` is in text subspace `1.x` and cut `c` crosses into link subspace `2.x`, does `rearrangend` proceed and relocate link POOM entries into text V-positions (or vice versa), or does some other guard prevent this?

## KB Synthesis

Yes — `rearrangend` proceeds unconditionally and will relocate POOM entries across subspace boundaries. No guard prevents this.

## What happens

`rearrangend` in `edit.c:78-160` executes the same pipeline regardless of cut geometry [ST-REARRANGE/Finding 0056]:

1. **Sort cuts** — `sortknives()` normalizes to ascending order
2. **Compute offsets** — `makeoffsetsfor3or4cuts()` derives tumbler displacements purely arithmetically from cut positions:
   - `diff[1] = c - b` (region between cuts a and b moves forward)
   - `diff[2] = -(b - a)` (region between cuts b and c moves backward)
3. **Classify spans** — `rearrangecutsectionnd()` assigns each POOM entry to a section
4. **Apply offsets** — `tumbleradd(&ptr->cdsp.dsas[V], &diff[i], ...)` — no subspace check anywhere

## Concrete consequence

With cuts at `[1.1, 1.4, 2.5]` [PRE-REARRANGE/Finding 0051]:

```
diff[1] = 2.5 - 1.4 = 1.1   → text "ABC" at V:1.1–1.3 displaced to V:2.2–2.4
diff[2] = -(1.4 - 1.1) = -0.3 → link orgl at V:2.1 displaced down into 1.x range
```

Text bytes end up in the link subspace; link orgl references end up in the text subspace. `retrieve_contents` at `2.x` returns text bytes [EC-REARRANGE-CROSS-SUBSPACE].

## Why no guard stops this

The two mechanisms that protect INSERT and DELETE do not apply here:

- **INSERT** uses a deliberate two-blade knife with `blade[1]` at `(N+1).1`, structurally confining shifts to one subspace [FC-SUBSPACE/Finding 0054, SS-TWO-BLADE-KNIFE]
- **DELETE** accidentally benefits from `strongsub`'s exponent guard, which returns the minuend unchanged when `width.exp < entry.vpos.exp` [FC-SUBSPACE/Finding 0055, INT-DELETE-SUBSPACE-ASYMMETRY]

REARRANGE uses `tumbleradd`, which has no equivalent cross-exponent guard. The offset arithmetic crosses subspace digit-0 boundaries without restriction [ST-REARRANGE/Finding 0056].

## Missing precondition

The spec requires a precondition not implemented in the code [PRE-REARRANGE/Finding 0051]:

```
requires ∀ orgl ∈ affected(cuts):
  subspace(vpos(orgl) + diff[section(orgl)]) == subspace(vpos(orgl))
```

Without it, a pivot spanning `1.x` and `2.x` produces a well-formed (no crash) but semantically invalid document state, violating `INV-SUBSPACE-CONVENTION` [INV-SUBSPACE-CONVENTION/Finding 0051].

---

## Code Exploration

Here is the complete answer.

---

## Cross-Subspace Pivot in `rearrangend`: Full Analysis

### Short Answer

`rearrangend` has **no guard whatsoever** against cross-subspace pivots. When cut `a` is in text subspace `1.x` and cut `c` is in `2.x`, the operation proceeds normally, relocates POOM entries by pure tumbler arithmetic, and leaves content stranded in the wrong subspace. This is confirmed by a golden test.

---

### Call Chain

The FEBE `REARRANGE` command arrives at:

**`do1.c:34-43`** — `dorearrange` passes directly to `rearrangepm` with no pre-flight checks:
```c
bool dorearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && rearrangepm (taskptr, docisaptr, docorgl, cutseqptr)
    );
}
```

**`orglinks.c:137-142`** — `rearrangepm` is a one-liner that passes the cut sequence straight to `rearrangend`:
```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

No validation at either layer.

---

### Inside `rearrangend` [`edit.c:78-160`]

The function takes the cuts and dimension index:

```c
// edit.c:102-107 — copy cuts into knives array; no subspace check
knives.dimension = index;
knives.nblades = cutseqptr->numberofcuts;
for (i = 0; i < knives.nblades; i++) {
    movetumbler (&cutseqptr->cutsarray[i], &knives.blades[i]);
}
sortknives (&knives);                          // line 107 — pure numeric sort
makeoffsetsfor3or4cuts (&knives, diff);        // line 108 — pure arithmetic
makecutsnd (fullcrumptr, &knives);             // line 110 — makes the cuts
```

Then for every crum under the pivot root:

```c
// edit.c:113-135
for (ptr = (typecuc*)findleftson(father); ptr; ...) {
    i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
    switch (i) {
      case 1:  case 2:  case 3:
        tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]); // line 125
        ivemodified((typecorecrum*)ptr);
        break;
    }
}
```

Line 125 blindly adds the computed offset to every crum in the affected regions — text POOM, link POOM, SPAN, all treated identically.

---

### Offset Arithmetic [`edit.c:164-184`]

For a 3-cut pivot with cuts `a`, `b`, `c`:

```c
// edit.c:177-181
tumblersub (&knives->blades[2], &knives->blades[1], &diff[1]);   // diff[1] = c - b
tumblersub (&knives->blades[1], &knives->blades[0], &diff[2]);   // diff[2] = b - a
diff[2].sign = !diff[2].sign;                                     // diff[2] = -(b - a)
```

With your specific case — `a = 1.1`, `b = 1.4`, `c = 2.5`:
- `diff[1] = 2.5 − 1.4 = 1.1` — region 1 (between `a` and `b`) moves forward by 1.1
- `diff[2] = −(1.4 − 1.1) = −0.3` — region 2 (between `b` and `c`) moves backward by 0.3

A crum at V-position `1.2` (in region 1) would be relocated to `1.2 + 1.1 = 2.3`. It is now in the `2.x` subspace. `tumbleradd` [tumble.c:365-404] is purely positional addition with no awareness that `1.x` and `2.x` are semantically distinct subspaces.

---

### Why `whereoncrum` Cannot Save It

`rearrangecutsectionnd` uses `whereoncrum` [retrie.c:345-398] to classify each crum:

```c
// retrie.c:354-372 — SPAN and POOM case
case SPAN:
case POOM:
    tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
    cmp = tumblercmp(address, &left);
    if (cmp == LESS)   return(TOMYLEFT);
    if (cmp == EQUAL)  return(ONMYLEFTBORDER);
    tumbleradd (&left, &ptr->cwid.dsas[index], &right);
    cmp = tumblercmp(address, &right);
    // ...
```

`tumblercmp` [tumble.c:72-85] compares `exp` then `mantissa[i]` lexicographically — it treats the entire V-space as a single ordered line. Comparing `1.2` vs `2.5` works numerically; there is no concept of a subspace boundary encoded in that comparison. The crum will be classified as `TOMYLEFT` of cut `c` and thereby assigned to region 1, and its V-position will be offset.

---

### What Happens to Link POOM Entries

Links are stored with V-positions in `0.x` (confirmed by `do1.c:377-411`, the `filter_vspanset_to_text_subspace` fix, which identifies link positions as those with stream `< 1.0`). In the scenario described:

- Cut `a = 1.1` is above `0.x`, so link POOM crums at `0.x` are entirely **to the left of all cuts** — they fall into region 0 (`case 0` at `edit.c:122`), which is the "these never move" branch.
- Text POOM crums between `1.1` and `1.4` fall into region 1 and are relocated into `2.x`.

So the specific cross-contamination is: **text content moves into link subspace `2.x`**, not the reverse. Link entries at `0.x` are unaffected because they lie outside the cut window entirely.

---

### Confirmed by Golden Test

Finding `0051-rearrange-crosses-subspace-boundaries.md` (status: **Validated**) documents exactly this:

> Pivot with cuts at 1.1, 1.4, 2.5  
> Content "ABC" is retrievable from 2.x subspace: `retrieve_after_2x: ['ABC']`  
> vspanset after shows: `at 0 for 0.2, at 1 for 1`

The golden test file is `golden/rearrange/pivot_cross_subspace_boundary.json`.

---

### The Contrast: Where Subspace *Is* Filtered

The only subspace guard in the codebase is in `do1.c:377-426` (`filter_vspanset_to_text_subspace`, `filter_specset_to_text_subspace`), applied only in `doshowrelationof2versions` [do1.c:428]. That fix was added reactively (Bug 009) for the compare-versions query path. It was **not** applied to `rearrangend`, and there is no analogous check anywhere in the rearrange path.

---

### Summary

| Question | Answer |
|---|---|
| Does `rearrangend` guard against cross-subspace pivots? | No. Zero validation at any level. |
| Where would a guard need to go? | Before `edit.c:125`, or in `makeoffsetsfor3or4cuts`, checking that `diff[i]` applied to crums in that region stays within the same top-level digit of V-space. |
| Does the operation corrupt POOM? | Yes — text POOM entries in the `1.x` region between cuts `a` and `b` are relocated into `2.x` by pure `tumbleradd` arithmetic. |
| Do link POOM entries (`0.x`) get relocated into text V-positions? | Not by this specific pivot (cuts `1.x`→`2.x`), because `0.x` falls outside all cut windows. But a pivot whose `a` cut is placed at `0.x` would drag link POOM entries into text space. |
| Is this an implementation bug or intended behavior? | Finding 0051 leaves it open. The spec question is whether REARRANGE is supposed to respect CD0 or operate purely spatially. The code is purely spatial. |
