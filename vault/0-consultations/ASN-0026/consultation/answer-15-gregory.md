## Question 15 [gregory]

> When `isanextensionnd` coalesces a new insertion into an existing POOM bottom crum (the ONMYRIGHTBORDER case), does it verify that the new I-address is exactly `existing_I_end + 1`, or could it coalesce I-addresses that are close but not strictly adjacent?

## KB Synthesis

The KB is explicit: `isanextensionnd` requires **exact** adjacency, not approximate closeness. It is a strict equality check in both dimensions.

From [ST-INSERT] (Finding 0062):

> `isanextensionnd()` checks two conditions: (1) the new content has the same `homedoc` as the existing crum, and (2) the new content's origin **equals** the existing crum's reach.

The condition is `reach == origin` — equality, not proximity. The crum's reach is `grasp + width` (its exclusive upper bound in both V and I space). The new insertion's origin must be that exact value. If the new I-address is `existing_I_end + 2` (a gap) or `existing_I_end - 1` (an overlap), `isanextensionnd` returns FALSE and a new crum is allocated instead.

[ST-VCOPY] (Finding 0046) confirms the same condition applies to COPY:

> `isanextensionnd()` at `insertnd.c:293-301` checks ... the new mapping starts **exactly** where the existing crum ends (contiguous in both V and I dimensions).

This is why [ST-INSERT] (Finding 0063) documents the CREATELINK-breaks-coalescing effect: after CREATELINK allocates a link orgl in I-space, the next text INSERT's I-address origin is no longer equal to the previous text crum's I-address reach — there is a gap (the link orgl's allocation). `isanextensionnd` returns FALSE, a new crum is created, and `compare_versions` shows two disjoint I-span pairs instead of one.

The concrete example from [ST-INSERT] (Finding 0062) makes the exact-equality semantics clear:

```
Crum covers [1.3, 1.4) in V; corresponding I-addresses have reach I_r

INSERT "Y" at v+1, new I-address = I_r exactly → isanextensionnd TRUE → coalesce
INSERT "Y" at v+1, new I-address = I_r + 1     → isanextensionnd FALSE → new crum
```

No tolerance for "close but not adjacent" exists in the implementation.

---

## Code Exploration

I now have all the necessary pieces. Let me compile the full answer.

---

## Answer

`isanextensionnd` requires **exact equality** — the new I-address must be precisely `existing_I_start + existing_I_width` (i.e., `existing_I_end + 1`). There is no tolerance for "close but not strictly adjacent."

---

### Full trace

#### 1. `isanextensionnd` — `insertnd.c:301`

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
  typedsp grasp, reach;
  bool lockeq();
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Three things happen:

1. **Homedoc guard** [`insertnd.c:305`]: the home document of the new insertion must match the existing crum's home document — or coalescing is refused unconditionally.

2. **`prologuend`** [`retrie.c:334–339`] computes `grasp` and `reach`:

   ```c
   int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
   {
       dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
       if (reach)
           dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
   }
   ```

   - `grasp = offset + ptr->cdsp` — absolute start address of the crum in all dimensions
   - `reach = grasp + ptr->cwid` — absolute end address (exclusive endpoint) in all dimensions

   For POOM, this operates on **both** the V-dimension and I-dimension simultaneously via `dspadd`, which calls `lockadd` over `dspsize(POOM) = 2` tumblers [`wisp.h:26`, `wisp.c:17`].

3. **`lockeq`** [`insertnd.c:308`] checks strict equality:

   ```c
   bool lockeq(tumbler *lock1, tumbler *lock2, unsigned loxize)
   {
       while (loxize--)
           if (!tumblereq (lock1++, lock2++))
               return(FALSE);
       return(TRUE);
   }
   ```
   [`wisp.c:261–267`]

   For POOM: `loxize = dspsize(POOM) = 2` [`wisp.h:26`, `wisp.h:61`], so it calls `tumblereq` on **both** `reach.dsas[V]` and `reach.dsas[I]`.

#### 2. `tumblereq` — `tumble.c:24–36`

```c
bool tumblereq(tumbler *a, tumbler *b)
{
  register INT i;
    if (a->xvartumbler != b->xvartumbler) return FALSE;
    if (a->varandnotfixed != b->varandnotfixed) return FALSE;
    if (a->sign != b->sign) return FALSE;
    if (a->exp != b->exp) return FALSE;
    for (i = 0; i < NPLACES; i++) {
        if (a->mantissa[i] != b->mantissa[i]) return FALSE;
    }
    return TRUE;
}
```

This is a **field-by-field bitwise equality** check — every bit of every field of the tumbler must match. There is no rounding, no delta tolerance, no approximation.

#### 3. What `reach.dsas[I]` actually is

For a POOM bottom crum with:
- I-start = `ptr->cdsp.dsas[I]` (stored in the crum's DSP)
- I-width = `ptr->cwid.dsas[I]` (stored in the crum's width)

After `prologuend`:
```
reach.dsas[I] = (offset.dsas[I] + ptr->cdsp.dsas[I]) + ptr->cwid.dsas[I]
              = absolute_I_start + I_width
              = existing_I_end + 1
```

`isanextensionnd` then returns `TRUE` only if `origin.dsas[I]` equals `reach.dsas[I]` exactly — i.e., if the new insertion starts at exactly `existing_I_end + 1`.

An I-address that is "close but not strictly adjacent" (e.g., `existing_I_end + 2`) would make `tumblereq` return `FALSE`, `lockeq` return `FALSE`, and `isanextensionnd` return `FALSE`, so no coalescing occurs and a new bottom crum is created instead [`insertnd.c:260–274`].

#### 4. The ONMYRIGHTBORDER question

The term "ONMYRIGHTBORDER" appears in `whereoncrum` [`retrie.c:367–371`] and `findsontoinsertundernd` [`insertnd.c:293–296`] — that is, in the logic that selects *which* crum to insert into at internal node height. Once the tree traversal reaches the bottom layer (`father->height == 1`), control passes to `insertcbcnd` [`insertnd.c:242–275`], which iterates over bottom crums and calls `isanextensionnd` on each one [`insertnd.c:250`]. The ONMYRIGHTBORDER classification in the upper layers only controls tree traversal; the actual coalescing decision is entirely inside `isanextensionnd`, which uses strict `lockeq` equality — not ONMYRIGHTBORDER — as its acceptance criterion.

---

### Summary

`isanextensionnd` performs **strict exact-adjacency verification**. It computes `reach = existing_start + existing_width` across all POOM dimensions (both V and I), then uses `lockeq` → `tumblereq` for field-by-field bit equality. The new I-address must be exactly `existing_I_start + existing_I_width` — which is precisely `existing_I_end + 1`. I-addresses that are close but not strictly adjacent cannot coalesce.
