## Question 14 [gregory]

> When multiple characters are inserted one at a time at successive V-positions (simulating typing), does each single-character INSERT trigger a full `splitcrumupwards` cycle, or does the ONMYRIGHTBORDER case in `isanextensionnd` handle the entire sequence without any splits or tree height changes?

## KB Synthesis

## Sequential Single-Character Inserts at Successive Positions

**The short answer:** Only the **first** insert at a new interior position triggers a `splitcrumupwards` cycle. All subsequent inserts at successive V-positions are handled entirely by the ONMYRIGHTBORDER + `isanextensionnd` path — no splits, no tree height changes, zero net crum creation.

---

### Phase 1 — First Insert (e.g., "A" at interior position 1.3)

`whereoncrum(crum, 1.3)` returns `THRUME` (strictly inside the existing crum's interval). `makegappm()` proceeds:

1. Constructs a two-blade knife: `blade[0] = 1.3`, `blade[1] = 2.1` (next subspace boundary via `findaddressofsecondcutforinsert`) [SS-TWO-BLADE-KNIFE]
2. `slicecbcpm` cuts the existing crum at 1.3, producing two crums
3. A new crum is created for "A" at `[1.3, 1.4)` with I-address allocated from granfilade
4. The father's `numberofsons` increments → `toomanysons` may trigger → `splitcrumupwards` may run

**Net: Δcrums = +2** (the original splits into two halves, plus the new content crum). [ST-INSERT Finding 0062]

---

### Phase 2 — Second Insert ("B" at 1.4)

The new crum from Phase 1 covers `[1.3, 1.4)`, so its reach = 1.4.

`makegappm()` runs its early-exit guard first:
```c
if (... || tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS) return(0);
```

Since `1.4 == reach`, `tumblercmp` returns `EQUAL`, which is `!= LESS` → **`makegappm` returns 0 immediately**. No knife constructed, no crum split. [SS-WHEREONCRUM, PRE-INSERT Finding 0062]

Then `isanextensionnd()` checks two conditions:
1. `homedoc` matches (same document) ✓
2. `new_content.origin == existing_crum.reach` — the fresh I-address for "B" is allocated as `prev_max_iaddr + 1`, which is exactly where the previous crum's I-range ended ✓

Both hold → **the existing crum is extended in place**: `crum.width' = crum.width + 0.1`. No new crum node is allocated, no parent `numberofsons` change, `toomanysons` is never evaluated, `splitcrumupwards` is never called. [ST-INSERT Finding 0062]

**Net: Δcrums = 0**

---

### Phase 3…N — Each Subsequent Character

Identical to Phase 2. The crum's reach advances by one position each time (1.4 → 1.5 → 1.6 → …). Each insert arrives at `origin == reach`, hits the `makegappm` early exit, and is absorbed by `isanextensionnd` extension.

**Net: Δcrums = 0 per character, indefinitely.**

---

### The Bound

This is exactly what [ST-CRUM-BOUND] documents:

```
c ≤ 1 + 2C + 3R + 3P
```

where C = number of distinct cursor repositionings. Sequential typing at successive positions is **one cursor repositioning** (the first interior insert). All N characters after that contribute nothing. So typing 1000 characters in sequence at a single cursor location costs exactly **1 initial split (+2 crums)**, not 1000 splits.

[INV-MONOTONIC] confirms this works because I-addresses are allocated contiguously — each sequential character gets `prev + 1`, which is precisely what `isanextensionnd` requires to coalesce. The only thing that would break the chain is a `CREATELINK` between characters, which advances the I-address allocator past a non-text orgl and destroys contiguity [ST-CRUM-BOUND Finding 0063, INT-LINK-INSERT].

---

## Code Exploration

I now have complete information. Here is the full analysis:

---

## Answer: Consecutive Single-Character Insertions — No Splits, `isanextensionnd` Handles the Whole Sequence

The short answer: **`isanextensionnd` handles the entire consecutive-typing sequence without any splits, new crums, or tree height changes.** `splitcrumupwards` is never reached. Here is the full trace.

---

### 1. Entry Point: `doinsert` → `insertnd` (POOM Path)

Each keystroke calls `doinsert` [`do1.c:87`], which:

1. Calls `inserttextingranf` to allocate an I-address `lsa` in the granfilade and returns an `ispanset` with `stream=lsa, width=1`.
2. Calls `docopy` → `insertpm` → `insertnd` to stitch that I-span into the POOM at the requested V-address.

In `insertnd`, the POOM case is [`insertnd.c:53-61`]:
```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);
    setwispupwards(fullcrumptr,0);
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);
    setwispupwards(fullcrumptr,1);
    break;
```

---

### 2. `makegappm` Exits Immediately for Right-Edge Appends

`makegappm` [`insertnd.c:124`] opens a gap in the V-space for mid-document insertions. Its early-exit guard is [`insertnd.c:140-143`]:
```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

When typing appends at the end: `origin.V == reach.V` (the new character starts exactly where existing content ends). The condition `origin.V < reach.V` is `FALSE`, so `!FALSE = TRUE` → `return(0)`. **No cuts, no gap creation.**

---

### 3. First Character: `firstinsertionnd`

When the enfilade is empty, `doinsertnd` [`insertnd.c:191-194`] takes the `isemptyenfilade` branch:
```c
if (isemptyenfilade (father)) {
    firstinsertionnd (father, origin, width, infoptr);
    return(FALSE);
}
```

`firstinsertionnd` [`insertnd.c:199`] populates the existing (or freshly-created) bottom crum:
- `cdsp = (V=V₁, I=lsa₁)`
- `cwid = (V=1, I=1)`

Returns `FALSE` — no split.

---

### 4. Characters 2, 3, … N: `isanextensionnd` Fires Every Time

For subsequent characters, control reaches `insertmorend` → `insertcbcnd` [`insertnd.c:242`]:
```c
INT insertcbcnd(typecuc *father, typedsp *grasp, typewid *origin, typewid *width, type2dbottomcruminfo *infoptr)
{
    for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
        if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
            dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
            ivemodified (ptr);
            setwispupwards (father,1);
            if(!isfullcrum((typecorecrum*)father)){
                return(setwispupwards(findfather((typecorecrum*)father),1));
            }
            return(FALSE);           // ← no split, returns here
        }
    }
    // ... new crum creation + splitcrumupwards only reached if no extension found
```

The split path at [`insertnd.c:272`]:
```c
splitsomething = splitcrumupwards (father);
```
is **only reached when `isanextensionnd` returns FALSE for every son**. For consecutive typing, it never returns FALSE.

---

### 5. Why `isanextensionnd` Returns TRUE for Every Appended Character

The function [`insertnd.c:301-309`]:
```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    typedsp grasp, reach;
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Two conditions must hold:

**Condition A — same `homedoc`:** All typed characters share the same document ISA, so this is always TRUE.

**Condition B — `reach == origin` in ALL dimensions:** `prologuend` computes [`retrie.c:334-339`]:
```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```
So: `grasp = offset + cdsp`, `reach = grasp + cwid`.

For POOM, `DSPSIZEPM = 2` [`wisp.h:26`], meaning `lockeq` compares **both** V and I dimensions:

- **V dimension:** After character `n` is stored (width 1 each), `cwid.V = n`, so `reach.V = V₁ + n`. Character `n+1` has `origin.V = V₁ + n`. ✓ Equal.

- **I dimension:** The granfilade allocates I-addresses consecutively. In `inserttextgr` [`granf2.c:83`], `findisatoinsertgr` → `findisatoinsertmolecule` [`granf2.c:158`] calls `findpreviousisagr` to find the last allocated address `A + (n-1)`, then for TEXTATOM computes [`granf2.c:169`]:
  ```c
  tumblerincrement (&lowerbound, 0, 1, isaptr);  // isaptr = lowerbound + 1
  ```
  So each successive character gets I-address `A, A+1, A+2, …`. After `n` chars, `cwid.I = n`, `reach.I = A + n`, and char `n+1` has `origin.I = A + n`. ✓ Equal.

Both dimensions match → `lockeq` returns TRUE → **`isanextensionnd` fires on every appended character.**

---

### 6. What Happens in the Extension Branch

When `isanextensionnd` returns TRUE [`insertnd.c:251-258`]:
```c
dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
ivemodified (ptr);
setwispupwards (father,1);
...
return(FALSE);
```

- The single bottom crum is **widened** in both V and I: `cwid.V++`, `cwid.I++`
- `ivemodified` marks it dirty for flushing
- `setwispupwards` propagates the new width upward
- Returns `FALSE` (`bothertorecombine = FALSE`)

No new crums are created. No `splitcrumupwards`. No `adopt`. No height change.

---

### 7. `recombine` Is Also Skipped

Back in `insertnd` [`insertnd.c:70`]:
```c
if(/*TRUE||*/bothertorecombine||(fullcrumptr->height != oldheight)){
    recombine (fullcrumptr);
}
```

The commented-out `TRUE||` reveals that recombination was once unconditional. Now it only runs if a split happened (`bothertorecombine=TRUE`) or height changed. For extension insertions: `bothertorecombine = FALSE` and height is unchanged → **`recombine` is skipped entirely.**

---

### 8. `splitcrumupwards` Internals (Never Reached for Typing)

For completeness: `splitcrumupwards` [`split.c:16`] iterates upward while `toomanysons(father)`, splitting overfull crums and potentially calling `levelpush` to grow tree height. Since the extension path never adds a new son and never calls `splitcrumupwards`, this machinery is entirely inert during consecutive typing.

---

### Summary

| Insertion | `makegappm` | New crum | `splitcrumupwards` | Tree height | Effect |
|-----------|-------------|----------|---------------------|-------------|--------|
| Char 1 (empty doc) | Early exit | — | No | Unchanged | `firstinsertionnd` populates single bottom crum |
| Chars 2…N (append) | Early exit (origin ≥ reach) | No | No | Unchanged | `isanextensionnd` widens the single bottom crum |

For the entire typing sequence, the POOM enfilade maintains exactly **one bottom crum** that grows in width (both V and I) by 1 per keystroke. The B-tree structure is never reorganized. The `ONMYRIGHTBORDER` semantics — the origin falls exactly on the right edge of the existing crum (`reach == origin` in both dimensions) — is precisely the condition `lockeq` tests in `isanextensionnd` [`insertnd.c:308`], and it fires unconditionally for all consecutive appends sharing the same `homedoc`.
