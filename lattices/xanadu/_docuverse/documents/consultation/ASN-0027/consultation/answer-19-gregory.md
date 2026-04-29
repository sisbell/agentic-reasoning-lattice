## Question 19 [gregory]

> REARRANGE preserves I-addresses while changing V-addresses — when a pivot moves content from V:1.2 to V:1.4, does the POOM entry's I-displacement field remain bit-identical, or is it rewritten during the rearrangement even though the logical value is unchanged?

## KB Synthesis

The I-displacement field remains **bit-identical** after rearrangement. The KB is explicit on the mechanism.

[ST-REARRANGE] (Finding 0056) documents the exact code path:

> "The operation modifies V-addresses exclusively — it calls `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])` which updates the displacement's **V-address component**. No I-addresses are touched, no content is copied, no new permascroll entries are created."

The `index` variable selects the V dimension (SPANRANGE), not the I dimension (ORGLRANGE). The I-address component (`cdsp.dsas[I]`) is never passed to `tumbleradd` and never written.

[INV-REARRANGE-IDENTITY] (Finding 0056) states this as a formal invariant:

> "`∀ c ∈ content(doc): i_addr(c, doc_after) = i_addr(c, doc_before)`. This is what makes rearrange the **unique** identity-preserving move operation. A delete+insert would: (1) destroy the original I-address, (2) allocate a new I-address..."

The [SS-POOM-BOTTOM-CRUM] entry confirms the dual-field structure:

```
BottomCrum = {
  origin: { dsas[I]: Tumbler, dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler, dsas[V]: Tumbler }
}
```

Rearrangement touches only the `dsas[V]` component of `origin` (via `tumbleradd`). The `dsas[I]` components of both `origin` and `width` are untouched — same bits, same memory location, zero rewriting.

This is not a logical equivalence that happens to be preserved; it is literal non-modification of those memory words.

---

## Code Exploration

Now I have everything needed for a complete, code-grounded answer.

---

## Answer: REARRANGE and I-Displacement Bit-Identity

### The Short Answer

The I-displacement field (`cdsp.dsas[I]`) is **not touched by the rearrangement displacement step**, but **can be rewritten by tree-restructuring side effects** — specifically by `newpeelcrumoffnd` when a crum is moved to a new parent during cuts. The logical I-address is always preserved; the stored bits may change only when the crum's parent changes.

---

### The Data Structure

`wisp.h:19-20`:
```c
#define I  0
#define V  1
```

`wisp.h:48-54`:
```c
struct structwid {
    tumbler dsas[MAXLOXIZE];  /* MAXLOXIZE = 2 */
};
typedef struct structwid typewid;
typedef typewid typedsp;
```

`enf.h:47-48`:
```c
typewid cwid;
typedsp cdsp;
```

Every POOM crum carries a `cdsp` with two tumbler slots: `dsas[I]` (index 0) and `dsas[V]` (index 1). These are **parent-relative** displacements, not absolute addresses.

---

### The REARRANGE Call Chain

`do1.c:34-43` → `dorearrange` calls `rearrangepm`.

`orglinks.c:137-142`:
```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);   /* index = V = 1 */
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`rearrangepm` passes `V` as the `index` argument. This is the **only** call site for `rearrangend` [protos.h:445 confirms the signature].

---

### The Displacement-Modification Step

`edit.c:113-136`:
```c
for (ptr = (typecuc*)findleftson(father); ptr; ptr = (typecuc *)findrightbro((typecorecrum*)ptr)) {
    i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
    switch (i) {
      case 0:  case 4: /* these never move */
        break;
      case 1:  case 2:  case 3: /* 3 only moves in 4 cuts */
        tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
        ivemodified((typecorecrum*)ptr);
        break;
    }
}
```

With `index = V`, only `ptr->cdsp.dsas[V]` is written. `ptr->cdsp.dsas[I]` is never referenced here. This answers the primary case: **the rearrangement displacement-addition step leaves I-displacement bits untouched**.

---

### The Cut Phase: Where Bits Can Change

Before displacement-adjustment, `rearrangend` calls `makecutsnd` [edit.c:110] to split any crum that straddles a cut boundary. Two relevant paths:

#### 1. `slicecbcpm` — splitting a bottom crum at a V-cut

`ndcuts.c:373-449`. When a V-cut falls inside a bottom crum (THRUME), it's split in two:

```c
/* ndcuts.c:438-446 */
movewisp (&ptr->cwid, &newwid);
for (i = 0; i < widsize(enftype); i++) {  /* loops over I and V both */
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];
    tumblerjustify (&newwid.dsas[i]);
}
locksubtract ((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, (unsigned)widsize(enftype));
movewisp (&newwid, &ptr->cwid);
dspadd (&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);  /* new->cdsp = ptr->cdsp + left-half-cwid */
```

The existing crum `ptr` keeps its original `cdsp.dsas[I]` unchanged. The new right-half crum `new` gets `new->cdsp.dsas[I] = ptr->cdsp.dsas[I] + (left_half_I_width)`. This is a logically correct computed value, not a corruption. Note `localcut` is computed from the V dimension but applied to both `dsas[I]` and `dsas[V]` — this works because POOM bottom crums are 1-to-1 (equal V and I spans within a block).

#### 2. `newpeelcrumoffnd` — moving a crum to a new parent

`ndcuts.c:262-335`. When tree restructuring moves a crum to a sibling or new uncle node:

```c
/* ndcuts.c:287 */
dspadd(&father->cdsp, &ptr->cdsp, &origin, (INT)father->cenftype);
/* ... */
/* ndcuts.c:302 */
dspadd(&father->cdsp, &ptr->cdsp, &temp, (INT)ptr->cenftype);
/* ndcuts.c:311 */
dspsub(&temp, &newuncle->cdsp, &ptr->cdsp, (INT)ptr->cenftype);
```

`dspadd`/`dspsub` operate on the full `typedsp` (both I and V slots). At line 311, `ptr->cdsp` is **rewritten for both dimensions**. The absolute I-address is preserved: `new_cdsp_I = old_absolute_I - newuncle_cdsp_I`. The **stored bits in `cdsp.dsas[I]` change**, even though the logical content address is identical.

---

### Summary

| Operation | Writes `cdsp.dsas[I]`? | Logical I-address preserved? |
|-----------|----------------------|------------------------------|
| `rearrangend` displacement step (`tumbleradd`, `edit.c:125`) | **No** — `index=V` only | N/A |
| `slicecbcpm` on existing crum `ptr` | **No** — `ptr->cdsp` unchanged | Yes |
| `slicecbcpm` on new right-half crum | **Yes** — computed fresh | Yes |
| `newpeelcrumoffnd` reparenting | **Yes** — recalculated relative to new parent | Yes |

**The core rearrangement step never touches `dsas[I]`.** However, the cut-preparation phase (`makecutsnd`) can rewrite `cdsp.dsas[I]` bits in two cases: (a) when creating a new right-half crum from a split, and (b) when `newpeelcrumoffnd` reparents a crum during tree rebalancing. In both cases the absolute I-address is preserved — the displacement is always parent-relative, so the bits must change when the parent changes.

**The I-displacement field is NOT guaranteed to be bit-identical after REARRANGE** — it will be rewritten whenever the crum is reparented during cut-phase tree restructuring. The field stores a relative displacement, and maintaining that invariant requires recomputing it when the crum moves to a different parent node.
