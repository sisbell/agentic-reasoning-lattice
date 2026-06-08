## Question 13 [evidence]

> After DELETE removes a span, are surviving entries beyond the deleted region shifted left by the deletion width via `tumblersub`, and under what offset conditions does this produce a negative V-position tumbler?

## KB Synthesis

Yes, entries beyond the deleted region are shifted left. Here is the full picture.

## The Shift Mechanism

`deletend()` in `edit.c` has a Case 2 for entries positioned entirely after the deletion range. It applies:

```c
tumblersub(&ptr->cdsp.dsas[V], width, &ptr->cdsp.dsas[V])
```

with no bounds check [ST-DELETE, Finding 0053]. The subtraction is unconditionally attempted for all Case 2 entries.

## When Subtraction Is a No-Op: the `strongsub` Guard

`tumblersub` delegates to `strongsub`, which has a critical exponent guard [SS-TUMBLER, Finding 0055]:

> `if (bptr->exp < aptr->exp) { movetumbler(aptr, cptr); return(0); }`

If `width.exp < entry.vpos.exp`, `strongsub` returns `entry.vpos` unchanged — the subtraction never occurs.

**Practical consequence:** Text deletion widths carry exp=-1 (fractional). Link crum displacements at subspace `2.x` carry exp=0. Because `-1 < 0`, the guard fires for all link crums, making cross-subspace shifts impossible [INT-DELETE-SUBSPACE-ASYMMETRY]. This is how DELETE preserves subspace isolation — not via a deliberate structural guard (as INSERT uses its two-blade knife [FC-SUBSPACE]), but as an incidental arithmetic property.

## When Negative V-Positions Can Arise

A negative result requires both conditions to hold simultaneously:
1. **Same exponent**: `width.exp == entry.vpos.exp` — the `strongsub` guard does not fire
2. **Width exceeds position**: the numeric value of `width > entry.vpos`

Concretely, this means within-subspace, within-exponent deletions where the surviving entry sits at a V-position smaller than the deletion width. The result is a valid tumbler with `sign=1` (negative) stored back into the POOM [SS-TUMBLER, Finding 0053].

```
Text crum at V-displacement 0.4 (exp=-1), deletion width 0.6 (exp=-1):
  strongsub(0.4, 0.6): exp match → proceeds → sign=1, magnitude=0.2 → stored as -0.2
```

## Consequences of Negative V-Positions

Negative tumblers sort before all positive tumblers and zero [SS-TUMBLER, Finding 0053]. This places the affected POOM entry outside the valid V-address range — it exists in the tree but is unreachable by any positive V-span query. `tumblercmp(-0.2, 1.1) → LESS`, so no retrieval operation finds it [INV-POOM-BIJECTIVITY].

The entry becomes leaked state. It cannot be reached by a subsequent `DELETEVSPAN` call (which uses positive V-addresses), and `levelpull` is disabled so it persists structurally [SS-ENFILADE-TREE, Finding 0058]. Finding 0055 retracts the earlier claim that this affects link crums via cross-subspace deletion — for cross-subspace cases the exponent guard prevents it — but same-exponent within-subspace deletion creating negative positions remains possible [EC-DEEPLY-ORPHANED-LINK].

## Missing Precondition

The formal precondition for DELETE should include [PRE-DELETE, Finding 0053]:

> `∀ entry ∈ poom(doc) : entry.vpos > delete_end ∧ entry.vpos.exp = width.exp ⟹ entry.vpos - delete_width ≥ 0`

The implementation does not enforce this. The `deletevspanpm()` entry point only checks for zero width [PRE-DELETE, Finding 0040].

---

## Code Exploration

I now have everything needed to give a complete, cited answer. Let me compile the full analysis.

---

## DELETE Shift Mechanics and Negative V-Position Conditions

### 1. The Call Chain: FEBE → dodeletevspan → deletend

`fns.c:333-347` — `deletevspan()` calls `getdeletevspan()`, immediately sends `putdeletevspan()` (pre-acknowledges), then calls `dodeletevspan()`. This is the "kluged unix version for speed" pattern (compare the commented-out strict version at lines 317-331).

`do1.c:158-167` — `dodeletevspan()`:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    typeorgl docorgl;
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

`orglinks.c:145-152` — `deletevspanpm()`:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

**No bounds check here.** This is the first important observation.

---

### 2. `deletend` — How Case-2 Crums Are Classified and Shifted

`edit.c:31-76` — the full delete implementation:

```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    clear (&offset, sizeof(offset));  /* fullcrum always has zero offset */
    prologuend ((typecorecrum*)fullcrumptr, &offset, &grasp, &reach);
    movetumbler (origin, &knives.blades[0]);
    tumbleradd (origin, width, &knives.blades[1]);
    knives.nblades = 2;
    knives.dimension = index;
    makecutsnd (fullcrumptr, &knives);
    newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);
    prologuend ((typecorecrum*)father, &foffset, &fgrasp, (typedsp*)NULL);
    for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
        next = (typecuc *) findrightbro((typecorecrum*)ptr);
        switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
          case 0: break;                              // left of origin — no action
          case 1:
            disown ((typecorecrum*)ptr);
            subtreefree ((typecorecrum*)ptr);         // within [origin, origin+width] — delete
            break;
          case 2:
            tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
            break;                                    // right of origin+width — shift left
          ...
        }
    }
    setwispupwards (father,1);
    recombine (father);
}
```

**Yes — surviving entries beyond the deleted region ARE shifted left by `tumblersub` at `edit.c:63`.**

---

### 3. `deletecutsectionnd` — Which Zone a Crum Is In

`edit.c:235-248`:

```c
INT deletecutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
    for (i = knives->nblades-1; i >= 0; --i) {
        cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp == THRUME)  return (-1);
        else if (cmp <= ONMYLEFTBORDER)  return (i+1);
    }
    return (0);
}
```

With `blades[0]=origin`, `blades[1]=origin+width`, and `whereoncrum` computing `left = offset.dsas[V] + ptr->cdsp.dsas[V]`:

- **case 0**: crum ends before `origin` — left of deletion, no action  
- **case 1**: crum starts between `origin` and `origin+width` — inside deletion zone, deleted  
- **case 2**: crum starts at or after `origin+width` — right of deletion, shifted by `tumblersub`

`retrie.c:345-398` — `whereoncrum` for POOM:
```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
// left = offset.dsas[V] + ptr->cdsp.dsas[V]  = absolute V-start of this crum
```

---

### 4. The Stub — `newfindintersectionnd` Always Returns Root

`ndinters.c:38-42`:
```c
int newfindintersectionnd(typecuc *fullcrumptr, typeknives *knives, typecuc **ptrptr, typewid *offset)
{
    *ptrptr = fullcrumptr;      // ALWAYS the root
    clear (offset,sizeof(*offset)); // offset = 0
}
```

The commented-out original at `ndinters.c:18-37` would have descended the tree to find the deepest node containing all cuts. **The current code is a stub: `father` is always the POOM root, `foffset` is always zero.**

Consequence: `prologuend(father=root, foffset=0, fgrasp, NULL)` gives:

```
fgrasp.dsas[V] = root->cdsp.dsas[V]
```

And `root->cdsp.dsas[V]` is the document's starting V-address — confirmed by `orglinks.c:159`:
```c
movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
```

---

### 5. `tumblersub` — When It Goes Negative

`tumble.c:406-440`:

```c
int tumblersub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
    if (iszerotumbler (bptr))
        movetumbler (aptr, cptr);
    else if (tumblereq (aptr, bptr))
        tumblerclear (cptr);
    else if (iszerotumbler (aptr)) {
        movetumbler (bptr, cptr);
        cptr->sign = !cptr->sign;       // 0 - b = -b  (NEGATIVE)
    } else {
        movetumbler (bptr, &temp);
        temp.sign = !temp.sign;         // temp = -b
        tumbleradd (aptr, &temp, cptr); // c = a + (-b)
    }
    tumblerjustify (cptr);
}
```

In `functiontumbleradd` (invoked by the last branch):
```c
} else {
    weaksub (bptr, aptr, cptr);
    cptr->sign = bptr->sign;   // sign of (-width) = TRUE = negative
}
```

This path is taken when `|a| < |b|`, i.e., `ptr->cdsp.dsas[V] < width`. The commented-out debug block at lines 432-438 shows developers observed this occurring:

```c
/*
if (cptr->sign) {
    fprintf(stderr,"TUMBLERSUB NEGATIVE OUTPUT\n");
    dumptumbler(cptr);
}
*/
```

---

### 6. The Offset Condition for Negative Displacement

For a case-2 child (absolute V >= `origin + width`):
```
fgrasp.dsas[V] + ptr->cdsp.dsas[V]  >=  origin + width
```

So:
```
ptr->cdsp.dsas[V]  >=  origin + width - fgrasp.dsas[V]
```

`tumblersub(ptr->cdsp.dsas[V], width)` goes negative when `ptr->cdsp.dsas[V] < width`, which requires:

```
origin + width - fgrasp.dsas[V]  <  width
  =>  origin  <  fgrasp.dsas[V]
```

**The condition is: `origin < fgrasp.dsas[V] = root->cdsp.dsas[V]`**  
i.e., the deletion start is *before* the document's V-origin.

More precisely, both inequalities must hold simultaneously:
```
origin  <  fgrasp.dsas[V]  <=  origin + width
```

The deletion zone starts before the document's V-start but extends into it. The surviving crum nearest the right edge of the deletion has `cdsp = (origin + width) - fgrasp.dsas[V]`, which is less than `width`, making `tumblersub` underflow to negative.

**Normal operation** (deletion within document bounds, `origin >= fgrasp.dsas[V]`):
```
ptr->cdsp.dsas[V]  >=  origin + width - fgrasp.dsas[V]  >=  width
tumblersub result  >=  0         (never negative)
```

---

### 7. The Missing Bounds Check — Delete vs. Insert Asymmetry

INSERT (`makegappm`, `insertnd.c:140-143`) validates:
```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS    // origin < doc start → reject
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)   // origin >= doc end → reject
    return(0);
```

DELETE (`deletevspanpm`, `orglinks.c:145-152`) — no equivalent check. Only a zero-width guard:
```c
if (iszerotumbler(&vspanptr->width))
    return (FALSE);
```

This asymmetry means an out-of-bounds deletion (with `origin` before `root->cdsp.dsas[V]`) reaches `deletend` unchecked, triggering the negative-displacement path. The resulting negative `cdsp.dsas[V]` has `cptr->sign = TRUE` (set by `tumblersub` at `tumble.c:426`). `tumblercheck` (`tumble.c:169-227`) does NOT flag a negative tumbler per se — it only flags "negative zero" (`sign=1, mantissa=0`) — but the invariant that V-positions are non-negative is violated, and `insertpm` would reject any subsequent use of such an address (`orglinks.c:93-96`).

---

### Summary

| Condition | Result |
|---|---|
| `origin >= root->cdsp.dsas[V]` (normal, in-bounds) | `tumblersub` always ≥ 0; no negative tumblers |
| `origin < root->cdsp.dsas[V]` AND `origin + width <= root->cdsp.dsas[V]` | All crums are case-0 or case-1; no case-2 to shift; no negative tumblers |
| **`origin < root->cdsp.dsas[V] <= origin + width`** | **Case-2 crums have `cdsp < width`; `tumblersub` at `edit.c:63` produces negative tumbler with `sign=1`** |

The negative displacement represents the surviving crum's new absolute V-position falling below the root's V-origin — which only happens when a deletion is issued with a start address before the document's V-space begins, an invalid operation that `deletevspanpm` does not guard against (unlike its insert counterpart `makegappm`).
