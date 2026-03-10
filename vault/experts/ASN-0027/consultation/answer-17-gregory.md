## Question 17 [gregory]

> When `isanextensionnd` coalesces a new insertion into an existing POOM crum by extending its width, does this change the I-displacement of the existing crum, or only the width — and can coalescing ever cause an adjacent crum's displacement to shift?

## KB Synthesis

When `isanextensionnd` coalesces a new insertion into an existing crum, **only the width changes — neither the I-displacement nor the V-displacement of the existing crum is modified**. Coalescing never causes adjacent crums to shift.

## Mechanics

The key is the interaction between `makegappm`'s early-exit and `isanextensionnd`'s width-extension path.

**Step 1: `makegappm` exits early before constructing a knife.**

From [SS-WHEREONCRUM] and [ST-INSERT] (Finding 0062), `makegappm` has this guard at `insertnd.c:137-143`:

```c
if (...|| tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS) return(0);
```

When the insertion point equals an existing crum's reach (`ONMYRIGHTBORDER`), `origin >= reach`, so `makegappm` returns 0 immediately. No knife is constructed, `makecutsnd` is never called, and `insertcutsectionnd` — the function that shifts subsequent crums — is never invoked. **No adjacent crum's displacement is touched.**

**Step 2: `isanextensionnd` extends width in place.**

With no shifting having occurred, `insertnd` proceeds to the extension check (`insertnd.c:293-301`). When both conditions hold — same `homedoc` AND new content's I-origin equals the existing crum's I-reach — the existing crum is extended at `insertnd.c:243`. Per [SS-POOM-BOTTOM-CRUM] (Finding 0076), each POOM bottom crum stores:

```
BottomCrum = {
  origin: { dsas[I]: Tumbler, dsas[V]: Tumbler },   ← UNCHANGED
  width:  { dsas[I]: Tumbler, dsas[V]: Tumbler }    ← ONLY THIS CHANGES
}
```

Both the V-origin and I-origin remain at their prior values. The new content's I-addresses are contiguous with the crum's existing I-range (that was the extension precondition), so extending width is sufficient — the crum's start point doesn't move.

**Step 3: Parent widths update, but parent displacements are unchanged.**

After extension, `setwispupwards` propagates the larger `cwid` up the tree per [ST-INSERT] (Finding 0066). Because the extended crum's origin (displacement) didn't change, `setwispnd`'s minimum-displacement recalculation produces the same `cdsp` as before. Parent nodes gain larger widths but retain the same displacements. Per [INV-ENFILADE-RELATIVE-ADDRESSING], relative addressing invariants are preserved.

## Summary

| What changes | What doesn't change |
|---|---|
| Existing crum's V-width | Existing crum's V-origin |
| Existing crum's I-width | Existing crum's I-origin |
| Ancestor `cwid` fields | Ancestor `cdsp` fields |
| — | All other crums (no shifting) |

This is precisely why [ST-INSERT] (Finding 0062) documents the coalescing cost as `Δcrums = 0` and `Δshifts = 0` for sequential interior typing after the first character at a new position. The ONMYRIGHTBORDER classification makes `makegappm` a no-op, and `isanextensionnd` handles the rest purely through in-place width mutation.

---

## Code Exploration

I now have everything needed. Here is the complete analysis:

---

## `isanextensionnd`: Coalescing, Displacement, and Adjacent Crums

### The predicate itself — `insertnd.c:301-309`

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

Two conditions must hold:

1. `homedoc` of the new insertion equals `homedoc` of the existing crum.
2. `reach == origin` in **all dsp dimensions**.

`prologuend` computes `reach = offset + cdsp + cwid` [retrie.c:334-339]. The `dspsize(POOM) = DSPSIZEPM = 2` [wisp.h:26], so `lockeq` runs over **both** `dsas[I]` (index 0) and `dsas[V]` (index 1) [wisp.h:19-20, 26]. The new insertion must be contiguous in **both** I-space and V-space simultaneously for coalescing to fire.

---

### What changes during coalescing — `insertnd.c:249-258`

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
        ivemodified (ptr);
        setwispupwards (father,1);
        ...
        return(FALSE);
    }
}
```

`dspadd` [wisp.c:15-18] is `lockadd` over `dspsize` tumblers:

```c
int dspadd(typedsp *a, typewisp *b, typedsp *c, INT enftype) {
    lockadd(a->dsas, b->dsas, c->dsas, (unsigned)dspsize(enftype));
}
```

This is `ptr->cwid = ptr->cwid + width` — component-wise tumbler addition across both I and V slots.

**`ptr->cdsp` is not touched.** Not by `dspadd`, not anywhere in the coalescing branch. The I-displacement (and V-displacement) of the coalesced crum are unchanged.

---

### Why `makegappm` is a no-op for extensions — `insertnd.c:124-172`

For POOM insertions, `makegappm` is called **before** `doinsertnd` [insertnd.c:54]. Its early-return guard is:

```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

The comment is explicit. Because `isanextensionnd` requires `reach == origin`, the condition `tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS` evaluates to `EQUAL != LESS` → TRUE. `makegappm` returns 0 immediately, performing no cuts and no shifts.

The only place in `makegappm` that modifies a crum's cdsp is the `case 1` displacement shift [insertnd.c:161-165]:

```c
case 1:   /*9-17-87 fix */
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
    ivemodified(ptr);
    break;
```

This loop — which shifts rightward siblings' V-displacements to make room — **never executes** for a coalescing extension because `makegappm` returns before reaching it.

---

### Why `makeroomonleftnd` is also a no-op — `makeroom.c:13-49`

```c
for (i = 0; i < widsize(father->cenftype); ++i) {
    if (tumblercmp(&origin->dsas[i], &grasp->dsas[i]) == LESS) {
        ...
        expandcrumleftward(...);
    }
}
```

`expandcrumleftward` [makeroom.c:52-74] shifts **all** sons' `cdsp.dsas[index]` by adding a base offset. But for an extension, `origin >= grasp` in all dimensions (we are appending to the right end), so the condition `origin < grasp` is never true. `makeroomonleftnd` does nothing.

---

### Why `setwispupwards` cannot shift adjacent crums — `wisp.c:171-228`

After coalescing, `setwispupwards(father, 1)` calls `setwispnd(father)` [wisp.c:171]. The critical section:

```c
/* find new upper-left corner */
movewisp(&ptr->cdsp, &mindsp);
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro(ptr))
    lockmin((tumbler*)&mindsp, (tumbler*)&ptr->cdsp, (tumbler*)&mindsp, ...);
lockiszerop = iszerolock((tumbler*)&mindsp, (unsigned)dspsize(father->cenftype));
if (!lockiszerop) {
    somethingchangedp = TRUE;
    dspadd(&father->cdsp, &mindsp, &newdsp, (INT)father->cenftype);
} ...
for (ptr = findleftson(father); ptr; ptr = getrightbro(ptr)) {
    if (!lockiszerop) {
        ptr->modified = TRUE;
        dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, (INT)ptr->cenftype);  // ← shifts ALL sons
    }
    ...
}
```

This normalization loop at [wisp.c:208-215] would subtract `mindsp` from every son's `cdsp` — which would shift adjacent crums. But it only fires when `!lockiszerop`, i.e., when `mindsp != 0`. Since coalescing does not modify any `cdsp`, and a valid enfilade always has its leftmost son at `cdsp = {0, 0}` (the minimum is zero before and after), `mindsp` stays zero, `lockiszerop = TRUE`, and the subtraction loop is skipped. Only `cwid` propagation happens upward.

---

### Summary

| Field | Effect of coalescing |
|-------|---------------------|
| `ptr->cwid` (width, both I and V) | **Increased** by `dspadd` [insertnd.c:251] |
| `ptr->cdsp` (I-displacement and V-displacement) | **Unchanged** — not touched |
| Adjacent siblings' `cdsp` | **Unchanged** — `makegappm` returns early [insertnd.c:140-143]; `makeroomonleftnd` no-ops [makeroom.c:26]; `setwispnd` skips normalization when `mindsp==0` [wisp.c:197] |

**The I-displacement of the coalesced crum does not change.** Only its width grows. And because the extension path bypasses every mechanism (`makegappm` cuts, `expandcrumleftward` shifts, `setwispnd` normalization) that would alter a sibling's displacement, **coalescing can never cause an adjacent crum's displacement to shift.**
