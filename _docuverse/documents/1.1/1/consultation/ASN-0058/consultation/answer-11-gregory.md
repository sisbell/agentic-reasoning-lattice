## Question 11 [gregory]

> When `isanextensionnd` detects that a new mapping's I-displacement equals the reach (origin + width) of an existing crum, does it extend the existing crum's V-width and I-width in lockstep, or does it only grow one dimension and recompute the other?

## KB Synthesis

The KB does not fully resolve this question at the code level.

What the KB establishes:

**For new-crum creation** (`SS-INSERT-VWIDTH-ENCODING` / Finding 0076), the process is asymmetric — the I-width is set directly (`movetumbler(&lwidth, &crumwidth.dsas[I])`), and the V-width is *derived* from it via a re-encoding step (extract integer value, re-encode at V-space precision via `tumblerincrement`). The two widths start with numerically equal values but different tumbler representations.

**For the extension path** (`ST-INSERT` / Finding 0062, `ST-VCOPY` / Finding 0046), the KB only records that the existing crum's width is extended in place at `insertnd.c:243`, without detailing whether both `dsas[V]` and `dsas[I]` in the width field are updated, or whether one is primary and the other recomputed.

**The invariant** (`INV-WIDTH-VALUE-EQUIVALENCE` / Finding 0076) states that after every operation that creates or modifies bottom crums, `tumblerintdiff(crum.width.dsas[V]) == tumblerintdiff(crum.width.dsas[I])`. This constrains what the extension must produce — both dimensions must encode the same numeric value — but does not specify the mechanism.

The KB is silent on whether the extension path mirrors the creation path (derive V-width from updated I-width) or updates both dimensions explicitly in lockstep. Answering definitively would require reading `insertnd.c:243` and the surrounding extension logic directly.

---

## Code Exploration

I now have everything needed to answer the question completely.

---

## Answer

### Short Answer

When `isanextensionnd` recognizes a new mapping as an extension, the caller (`insertcbcnd`) grows **both V-width and I-width simultaneously and independently** via a single `dspadd` call. Neither dimension is derived from or recomputed in terms of the other — each axis gets its own component of `width` added to it in lockstep.

---

### Full Trace

#### 1. Type layout — `cwid` is 2D for POOM crums

`wisp.h:53-55`:
```c
typedef struct structwid typewid;
typedef typewid typedsp;
typedef typewid typewisp;
```

The struct holds an array of tumblers:
```c
tumbler dsas[MAXLOXIZE];
```

For POOM (the 2D enfilade type used here), both `widsize` and `dspsize` equal 2 (`wisp.h:26-27`):
```c
#define DSPSIZEPM 2
#define WIDSIZEPM 2
```

The two slots are indexed by (`wisp.h:19-20`):
```c
#define I  0    /* I-space (ispace) dimension */
#define V  1    /* V-space (vspace) dimension */
```

So `ptr->cwid.dsas[I]` is the I-width and `ptr->cwid.dsas[V]` is the V-width.

---

#### 2. `prologuend` computes both dimensions of `reach`

`retrie.c:334-339`:
```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd(offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd(grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```

`dspadd` is (`wisp.c:15-18`):
```c
int dspadd(typedsp *a, typewisp *b, typedsp *c, INT enftype)
{
    lockadd(a->dsas, b->dsas, c->dsas, (unsigned)dspsize(enftype));
}
```

And `lockadd` (`wisp.c:269-272`) iterates `loxize` times — for POOM, 2 times:
```c
int lockadd(tumbler *lock1, tumbler *lock2, tumbler *lock3, unsigned loxize)
{
    while (loxize--)
        tumbleradd(lock1++, lock2++, lock3++);
}
```

Result: `reach.dsas[I] = grasp.dsas[I] + ptr->cwid.dsas[I]` and `reach.dsas[V] = grasp.dsas[V] + ptr->cwid.dsas[V]`. Both I and V components of `reach` are computed independently.

---

#### 3. `isanextensionnd` checks **all** `dspsize` dimensions simultaneously

`insertnd.c:301-309`:
```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
    typedsp grasp, reach;
    bool lockeq();
    if (!tumblereq(&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq(reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

`lockeq` (`wisp.c:261-267`) iterates `loxize = dspsize(POOM) = 2` times, comparing each element:
```c
bool lockeq(tumbler *lock1, tumbler *lock2, unsigned loxize)
{
    while (loxize--)
        if (!tumblereq(lock1++, lock2++))
            return(FALSE);
    return(TRUE);
}
```

So the adjacency test is: **`reach.dsas[I] == originptr->dsas[I]` AND `reach.dsas[V] == originptr->dsas[V]`**. Both dimensions must match. This is a strict 2D coincidence check — the new mapping must abut the existing crum on both axes simultaneously.

---

#### 4. When the check passes, `dspadd` grows both widths in lockstep

`insertcbcnd` at `insertnd.c:250-252`:
```c
if (isanextensionnd((typecbc*)ptr, grasp, origin, infoptr)) {
    dspadd(&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
    ivemodified(ptr);
```

`dspadd(&ptr->cwid, width, &ptr->cwid, father->cenftype)` expands to:
```c
lockadd(ptr->cwid.dsas, width->dsas, ptr->cwid.dsas, dspsize(POOM));
// i.e., 2 iterations:
ptr->cwid.dsas[I] += width->dsas[I];   // I-width grows by width's I-component
ptr->cwid.dsas[V] += width->dsas[V];   // V-width grows by width's V-component
```

No recomputation, no cross-axis dependency. Each component of `cwid` is incremented by the matching component of `width`.

---

### Summary

**`isanextensionnd` and its caller grow V-width and I-width in lockstep, each by its own independent component of `width`.**

- The adjacency test (`insertnd.c:308`) uses `lockeq` over `dspsize(cenftype) = 2` slots — both I and V components of `reach` must exactly equal `originptr`. This is a joint 2D check; a crum that abuts on only one axis does not pass.
- The mutation (`insertnd.c:251`) uses `dspadd` → `lockadd` over the same 2 slots — it adds `width->dsas[I]` to `cwid.dsas[I]` and `width->dsas[V]` to `cwid.dsas[V]` in a single pass, independently. No dimension is derived from or capped by the other.

The design relies entirely on the invariant that a matching extension has equal-width in both axes (since the same `width` value is threaded through the entire FEBE protocol call chain and stored in both slots when the original mapping was created). The code does not enforce this invariant locally — it simply passes `width` straight into `dspadd` as-is.
