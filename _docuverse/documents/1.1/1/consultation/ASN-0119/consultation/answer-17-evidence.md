## Question 17 [evidence]

> Does `makeoffsetsfor3or4cuts` apply any guard against a computed offset pushing a `1.x` text crum's V-position across the `2.x` link subspace boundary, or is cross-subspace displacement possible as in [EC-REARRANGE-CROSS-SUBSPACE]?

## KB Synthesis

No guard exists. `makeoffsetsfor3or4cuts` computes displacements as pure tumbler arithmetic — `diff[i] = cut[i+1] - cut[i]` with sign-adjusted variants — and `rearrangend` applies them via `tumbleradd` with no subspace validation at any point.

The evidence from the KB is consistent across multiple entries:

**[ST-REARRANGE]** (Finding 0056): "The operation modifies V-addresses exclusively — it calls `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], ...)`. No content is copied, no new permascroll entries are created." The offset arithmetic has no awareness of the leading mantissa digit that encodes subspace.

**[ST-REARRANGE]** (Finding 0051) provides the canonical counterexample: cuts at `[1.1, 1.4, 2.5]` produce `diff[1] = 2.5 - 1.4 = 1.1`, which displaces content at `V:1.1–1.3` to `V:2.2–2.4`. Text bytes end up in the link subspace; `retrieve_contents` at `2.x` returns "ABC". No error is raised.

**[PRE-REARRANGE]** (Finding 0051) identifies this as a missing precondition: the spec would need `requires ∀ orgl ∈ affected(cuts): subspace(vpos(orgl) + diff[section(orgl)]) == subspace(vpos(orgl))`, but the implementation enforces nothing.

**[EC-REARRANGE-CROSS-SUBSPACE]** (Finding 0056) summarizes: "The rearrange operation lacks a precondition check: there is no `pre_rearrange_subspace` guard."

Contrast this with [FC-SUBSPACE] / [ST-INSERT] (Finding 0054), where INSERT uses a *deliberate* two-blade knife with `blade[1]` set to `(N+1).1` — explicitly bounding shifts to one subspace. REARRANGE has no equivalent mechanism. [INT-DELETE-SUBSPACE-ASYMMETRY] (Finding 0055) notes that even DELETE's subspace isolation is only an *incidental* consequence of `strongsub`'s exponent guard, not a structural guard. REARRANGE doesn't benefit from even that: `tumbleradd` has no exponent guard.

**Answer:** Cross-subspace displacement by REARRANGE is possible and empirically confirmed. `makeoffsetsfor3or4cuts` applies no guard.

---

## Code Exploration

I now have everything needed to answer definitively.

---

## Answer

`makeoffsetsfor3or4cuts` applies **no guard** against cross-subspace displacement. The function is pure tumbler arithmetic with no awareness of the `1.x`/`2.x` subspace boundary. Cross-subspace displacement is fully possible, identical in mechanism to what EC-REARRANGE-CROSS-SUBSPACE documents.

---

### The Function in Full

**`backend/edit.c:164-184`**

```c
int makeoffsetsfor3or4cuts(typeknives *knives, tumbler diff[])
{
  tumbler a, b;

    /* diff[0] is simply ignored */
    if (knives->nblades == 4) {
        tumblersub (&knives->blades[2], &knives->blades[0], &(diff[1]));
        tumblersub (&knives->blades[1], &knives->blades[0], &a);
        tumblersub (&knives->blades[3], &knives->blades[2], &b);
        tumblersub (&b, &a, &(diff[2]));
        movetumbler (&diff[1], &diff[3]);
        diff[3].sign = !diff[1].sign;
    } else if (knives->nblades == 3) {
        tumblersub (&knives->blades[2], &knives->blades[1], &diff[1]);
        tumblersub (&knives->blades[1], &knives->blades[0], &diff[2]); /* should be negative */
        diff[2].sign = !diff[2].sign;
        tumblerclear (&(diff[3]));
    } else
        gerror ("Wrong number of cuts.");
}
```

The only inputs are the sorted cut positions (`knives->blades[]`). The only operations are `tumblersub` (pure signed tumbler subtraction, `tumble.c:406-430`) and `movetumbler` (copy). There is no:
- inspection of digit-0 (the subspace digit)
- clamping or rejection when a computed diff would cause a V-position to cross a subspace boundary
- range check of any kind

---

### Where the Offset Is Applied

**`backend/edit.c:124-127`** (inside `rearrangend`):

```c
case 1:  case 2:  case 3: /* 3 only moves in 4 cuts */
    tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
    ivemodified((typecorecrum*)ptr);
    break;
```

`tumbleradd` is the macro at **`backend/common.h:197`**:

```c
#define tumbleradd(x,y,z) functiontumbleradd(x,y,z)
```

`functiontumbleradd` (**`backend/tumble.c:365-404`**) performs signed arbitrary-precision tumbler addition — purely arithmetic, no boundary semantics.

---

### Why Cross-Subspace Displacement Occurs

For a 3-cut pivot with cuts at `1.1`, `1.4`, `2.5` (spanning the `1.x`/`2.x` boundary):

- `diff[1] = blade[2] - blade[1] = 2.5 - 1.4 = 1.1` (edit.c:178)
- Content in slice 1 (between cut 0 and cut 1, i.e., at `1.1–1.4`) receives `tumbleradd(vpos, 1.1, ...)`.
- A crum at V-position `1.1` moves to `1.1 + 1.1 = 2.2` — crossing from the `1.x` text subspace into the `2.x` link subspace.

This is not an overflow or edge case: it is the direct mathematical result of the unconstrained arithmetic.

---

### Confirmation from Finding

**`findings/0051-rearrange-crosses-subspace-boundaries.md`** (validated via golden test) documents exactly this:

> Content "ABC" is retrievable from 2.x subspace: `retrieve_after_2x: ['ABC']`  
> vspanset after shows: `at 0 for 0.2, at 1 for 1`

The finding confirms the behavior and notes that `makeoffsetsfor3or4cuts` is the site where a subspace-aware guard would need to be introduced if such a guard were desired.

---

### Summary

There is **no guard** anywhere in the call chain — not in `makeoffsetsfor3or4cuts` (edit.c:164-184), not in `tumblersub` (tumble.c:406-430), not in `functiontumbleradd` (tumble.c:365-404), and not in the `rearrangend` loop (edit.c:113-136) that applies the offsets. Cross-subspace displacement is arithmetically possible and has been empirically confirmed whenever cut positions span the `1.x`/`2.x` boundary.
