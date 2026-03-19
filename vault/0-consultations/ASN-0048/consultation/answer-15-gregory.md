## Question 15 [gregory]

> INSERT at V-position `v` in an empty document creates the first POOM entry — does this initial insertion also trigger `makegappm` (finding nothing to shift), or is there a fast path that skips the gap-making machinery when the POOM has no existing entries?

## KB Synthesis

The KB gives a clear answer from two converging sources.

**Fast path exists: `makegappm`'s zero-width early exit**

From [ST-INSERT] / [SS-WHEREONCRUM] (Finding 0062), `makegappm` contains an explicit triple-condition early exit at `insertnd.c:137-143`:

```c
if (iszerotumbler(&fullcrumptr->cwid.dsas[V]) ||
    tumblercmp(&origin->dsas[V], &grasp.dsas[V]) == LESS ||
    tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);
```

The **first condition** — `iszerotumbler(cwid.dsas[V])` — fires immediately for an empty document. From [SS-ENFILADE-TREE] (Finding 0058), `createenf(POOM)` produces a height-1 fullcrum with a single height-0 bottom node having **zero width**. So for any first insertion, `makegappm` returns 0 without constructing a knife, without calling `makecutsnd`, and without running `insertcutsectionnd`. No shifting machinery executes.

**What happens instead**

The actual first-entry path is `firstinsertionnd`, documented in [ST-INSERT] (Finding 0066): it sets the new child's `cdsp` to the absolute insertion V-position, then calls `setwispnd` on the parent to absorb that displacement into the root. From that finding:

> For first child, `firstinsertionnd` sets child `cdsp = insertion_position` (absolute), then `setwispnd` absorbs it: `root.cdsp = insertion_position`, `child.cdsp = 0` (relative).

**Summary**

| Condition | Mechanism | Result |
|-----------|-----------|--------|
| Empty POOM (cwid = 0) | `makegappm` zero-width guard | Returns 0 immediately — no knife, no shifts |
| First entry insertion | `firstinsertionnd` | Absolute position set, `setwispnd` updates root displacement |

The zero-width check in `makegappm` is the fast path. It is structurally necessary — for an empty crum with grasp=0, reach=0, any positive insertion address falls at `TOMYRIGHT` anyway (per [SS-WHEREONCRUM]), so the third condition would also fire. But the zero-width test catches it first, before tumbler comparisons are even attempted.

---

## Code Exploration

I now have everything needed. Here is the full answer.

---

## Answer: `makegappm` Is Called but Returns Immediately for an Empty POOM

There is **no fast path that bypasses the `makegappm` call** for the empty-document case. However, `makegappm` itself contains a guard condition that causes it to exit immediately when the POOM has zero width — which is exactly the state of a fresh document.

### Call chain

```
doinsert (do1.c:87)
  → inserttextingranf + docopy
    → insertpm (orglinks.c:75)
      → insertnd (orglinks.c:130)
        → makegappm (insertnd.c:54)  ← always called for POOM
        → doinsertnd (insertnd.c:57)
          → firstinsertionnd (insertnd.c:192)  ← empty-enfilade fast path
```

### Step 1 — `insertnd` unconditionally calls `makegappm` for POOM

`insertnd.c:51-61`:
```c
switch (fullcrumptr->cenftype) {
  case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);   /* line 54 — no guard */
    checkspecandstringbefore();
    setwispupwards(fullcrumptr,0);
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);
    ...
```

There is no `if (!isempty...)` wrapper around this call. `makegappm` is always entered for POOM.

### Step 2 — `makegappm` returns immediately for an empty POOM

`makegappm` (`insertnd.c:124`) begins with a three-condition early exit at lines 140–143:

```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

For a document that has never had content, `fullcrumptr->cwid.dsas[V]` is the zero tumbler. `iszerotumbler` fires on the very first clause, and the function returns `0` without executing any of the cut machinery (`makecutsnd`, `newfindintersectionnd`, the `for` loop over children, `setwidnd`, `setwispupwards`). The comment — *"this [is] for extensions to bc without calling cut"* — is the authors' label for this class of no-op early return.

### Step 3 — `doinsertnd` routes to `firstinsertionnd`, not `insertmorend`

Back in the `case POOM` block, `doinsertnd` is called (`insertnd.c:57`). Its first act (`insertnd.c:191–193`):

```c
if (isemptyenfilade (father)) {
    firstinsertionnd (father, origin, width, infoptr);
    return(FALSE);
}
```

`isemptyenfilade` for POOM (`genf.c:105–108`) checks that both `cwid` and `cdsp` tumblers are all-zero:

```c
case POOM :
    return (
       iszerolock(ptr->cwid.dsas, (unsigned)widsize(ptr->cenftype))
    && iszerolock(ptr->cdsp.dsas, (unsigned)dspsize(ptr->cenftype)));
```

An empty document satisfies both conditions, so `firstinsertionnd` is called (`insertnd.c:199`). It reuses or creates the single bottom crum, writes the origin/width/info directly into it, and returns. The full `insertmorend` → `insertcbcnd` → `splitcrumupwards` path is never entered.

### Summary

| Phase | Empty document | Non-empty document |
|---|---|---|
| `insertnd` calls `makegappm`? | **Yes, always** | Yes |
| `makegappm` does real work? | **No — exits at line 143** (`iszerotumbler` fires) | Yes — cuts, shifts, updates |
| `doinsertnd` path taken | `firstinsertionnd` | `insertmorend` |

The "fast path" is not a bypass of the `makegappm` call — it is the `iszerotumbler` guard inside `makegappm` (`insertnd.c:140`) combined with `isemptyenfilade` inside `doinsertnd` (`insertnd.c:191`). Both checks are O(1) tumbler comparisons. The gap-making machinery (cuts, sibling iteration, displacement adjustments) is entirely skipped for the first insertion.
