## Question 15 [gregory]

> In the 2D POOM enfilade, the root displacement tracks the minimum child address via `setwispnd` — does this minimum track independently in V and I dimensions, or is there a single combined displacement that couples the two?

## KB Synthesis

The V and I dimensions track **independently**. The `cdsp` displacement field is a multi-dimensional structure with separate `dsas[V]` and `dsas[I]` components; `setwispnd` operates on each dimension autonomously.

**Evidence from the KB:**

[SS-POOM-BOTTOM-CRUM] (Finding 0076) shows the crum structure directly:
```
BottomCrum = {
  origin: { dsas[I]: Tumbler, dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler, dsas[V]: Tumbler }
}
```
Each dimension carries its own tumbler value with its own precision. The V and I origins and widths are stored and manipulated as separate fields.

[ST-REARRANGE] (Finding 0056) is the clearest proof: "The code modifies only `ptr->cdsp.dsas[index]` (the V-address component of the displacement). The I-address, stored separately, is never touched." A rearrange operation on `dsas[V]` leaves `dsas[I]` completely unchanged — impossible if they were coupled.

[INV-ENFILADE-RELATIVE-ADDRESSING] (Finding 0066) states `absolute_grasp(node) = absolute_grasp(parent) + node.cdsp`, where the `cdsp` addition (`dspadd`) operates on each dimension's component. The `setwispnd` algorithm at `wisp.c:196` absorbs `mindsp` into the parent and subtracts it from children — but `mindsp` is computed per-dimension: the minimum V-displacement across children is absorbed into `cdsp.dsas[V]`, and the minimum I-displacement independently into `cdsp.dsas[I]`.

[ST-INSERT] (Finding 0054) confirms the operational independence: the two-blade knife shifts `cdsp.dsas[V]` for entries within the knife range, leaving `cdsp.dsas[I]` untouched. INSERT in the V-dimension does not disturb I-dimension displacements at all.

**Summary:** The POOM root's `cdsp` is a 2D displacement vector. `setwispnd` finds the per-dimension minimum independently — the V-component minimum is absorbed into `cdsp.dsas[V]` while the I-component minimum is absorbed into `cdsp.dsas[I]`. Children's relative displacements are adjusted dimension-by-dimension. The two dimensions are structurally parallel but have no coupling in the displacement tracking mechanism.

---

## Code Exploration

I now have everything I need. Here is the full answer:

---

## POOM Displacement: Independent Per-Dimension, Not Combined

The displacement in the 2D POOM enfilade tracks **I and V independently** — there is no single combined scalar. They share a single struct, but that struct contains **two separate tumblers** that are operated on in lockstep by array iteration, never collapsed into one value.

---

### The Data Structure

Every POOM node (both upper `typecuc` and bottom crums) carries two fields [`enf.h:47-48`, `enf.h:71-72`, `enf.h:102-103`]:

```c
typewid cwid;
typedsp cdsp;
```

Both `typewid` and `typedsp` are the same struct [`wisp.h:50-55`]:

```c
struct structwid {
    tumbler dsas[MAXLOXIZE];   /* MAXLOXIZE = 2 */
};
typedef struct structwid typewid;
typedef typewid typedsp;
```

For POOM, `dspsize` and `widsize` both return **2** [`wisp.h:26-27`, `wisp.h:60-61`]:

```c
#define DSPSIZEPM 2
#define WIDSIZEPM 2
#define dspsize(A) ((A)==GRAN?DSPSIZEGR:((A)==SPAN?DSPSIZESP:DSPSIZEPM))
```

The two slots are named by index [`wisp.h:19-20`]:

```c
#define I  0
#define V  1
```

So `cdsp.dsas[I]` is the I-stream displacement and `cdsp.dsas[V]` is the V-stream displacement. They coexist in one struct but are two independent tumbler values.

---

### How `setwispnd` Operates

`setwispnd` is the POOM/SPAN variant of the widditive recalculation, dispatched from `setwisp` when `cenftype` is `POOM` or `SPAN` [`wisp.c:126-131`]:

```c
case SPAN:
case POOM:
    return (setwispnd ((typecuc*)ptr));
```

Inside `setwispnd` [`wisp.c:171-228`], the critical operations are:

**Step 1 — Find the minimum child displacement (upper-left corner):**

```c
movewisp (&ptr->cdsp, &mindsp);                           /* line 193 — seed with first child */
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro (ptr)) {
    lockmin ((tumbler*)&mindsp, (tumbler*)&ptr->cdsp,
             (tumbler*)&mindsp, (unsigned)dspsize(ptr->cenftype));  /* line 195 */
}
```

`lockmin` at [`wisp.c:281-287`] iterates over the `loxize` (= `dspsize` = **2** for POOM) tumblers independently:

```c
int lockmin(tumbler *lock1, tumbler *lock2, tumbler *lock3, unsigned loxize)
{
    while (loxize--){
        macrotumblermin (lock1, lock2, lock3);   /* per-tumbler min */
        lock1++; lock2++; lock3++;
    }
}
```

And `macrotumblermin` is a simple component-wise comparison [`common.h:144`]:

```c
#define macrotumblermin(a,b,c) \
    ((*(tumbler*)(c)) = (tumblercmp((a),(b))==LESS) ? (*(tumbler*)(a)) : (*(tumbler*)(b)))
```

This means `mindsp` ends up as **`{ min(all children's dsas[I]), min(all children's dsas[V]) }`** — the minimums are computed **per-dimension and independently**.

**Step 2 — Update father's displacement:**

```c
dspadd (&father->cdsp, &mindsp, &newdsp, (INT)father->cenftype);   /* line 200 */
```

`dspadd` [`wisp.c:15-18`] calls `lockadd` over all `dspsize` tumblers:

```c
int dspadd(typedsp *a, typewisp *b, typedsp *c, INT enftype)
{
    lockadd (a->dsas, b->dsas, c->dsas, (unsigned)dspsize(enftype));
}
```

Again component-wise: `newdsp.dsas[I] = father->cdsp.dsas[I] + mindsp.dsas[I]` and `newdsp.dsas[V] = father->cdsp.dsas[V] + mindsp.dsas[V]`.

**Step 3 — Compensate each child to preserve absolute positions:**

```c
dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, (INT)ptr->cenftype);   /* line 211 */
```

Same component-wise structure. Each child's I is reduced by `mindsp.dsas[I]`; each child's V is reduced by `mindsp.dsas[V]`.

**Step 4 — Find the maximum corner (width):**

```c
lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid, (tumbler*)&tempwid,
        (unsigned)widsize(ptr->cenftype));                         /* line 213 */
lockmax((tumbler*)&newwid, (tumbler*)&tempwid, (tumbler*)&newwid,
        (unsigned)widsize(ptr->cenftype));                         /* line 214 */
```

`lockmax` mirrors `lockmin` — independent per-dimension max. Father's `cwid` becomes `{ max(cdsp[I]+cwid[I]), max(cdsp[V]+cwid[V]) }` across children.

---

### Evidence of Independent Tracking in Insertion

`insertnd.c` directly indexes the dimensions by name at points where only one axis is being adjusted. For example, at [`insertnd.c:162`]:

```c
tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
```

Only `dsas[V]` is modified — `dsas[I]` is left untouched. This is only coherent if the two dimensions are tracked independently; a combined representation would require both to be updated together.

Similarly, insertion cuts are made exclusively on V [`insertnd.c:140-145`]:

```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    ...
movetumbler (&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
```

The I dimension is not consulted for this cut, confirming they live independently.

---

### Summary

| Property | Answer |
|---|---|
| **Storage** | Single `typedsp` struct, but containing `dsas[2]` — two separate tumblers |
| **Index `[I]` (dsas[0])** | I-stream displacement, independent |
| **Index `[V]` (dsas[1])** | V-stream displacement, independent |
| **`setwispnd` min** | `lockmin` iterates both slots separately — finds independent minimum per axis |
| **`setwispnd` add/sub** | `dspadd`/`dspsub` via `lockadd`/`locksubtract` — both axes shifted together by their respective per-axis minima |
| **Coupling** | None — the min for I doesn't affect V and vice versa; `lockmin` at `wisp.c:284` processes each tumbler slot in its own comparison |

The displacement is **two coupled scalars stored together, not a single combined value**. `setwispnd` computes a per-axis minimum independently across children, then adjusts the father's `cdsp` and each child's `cdsp` by that per-axis minimum. There is no cross-dimension coupling: the minimum I displacement does not influence the V adjustment, and vice versa.
