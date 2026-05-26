## Question 11 [gregory]

> When `isanextensionnd` detects the ONMYRIGHTBORDER case and coalesces a new insert into an existing crum, does it modify the existing crum's V-width and I-width in place, or does it replace the crum with a new one carrying the extended range?

## KB Synthesis

The KB is explicit on this: `isanextensionnd` triggers **in-place modification** of the existing crum — no replacement occurs.

From [ST-INSERT] (Finding 0062):

> When `isanextensionnd()` returns TRUE (same `homedoc`, `reach == origin`), **the existing crum's width is extended in place** at `insertnd.c:243`. No new crum is allocated.

The postcondition stated there is:

> `crum.width' = crum.width + content.width ∧ crum.grasp' = crum.grasp ∧ num_crums' = num_crums`

So the grasp (left boundary) is unchanged, the width grows rightward, and the total crum count is unaffected (`Δ = 0`). A new crum is only created at `insertnd.c:252-260` when `isanextensionnd` returns FALSE.

Since POOM bottom crums carry dual-space coordinates ([SS-POOM-BOTTOM-CRUM]), both the V-width and I-width fields of the existing crum must be updated to reflect the larger range, consistent with [INV-WIDTH-VALUE-EQUIVALENCE] (both encode the same integer value at different tumbler precisions). The [SS-INSERT-VWIDTH-ENCODING] entry describes how the V-width is re-encoded from the I-width's integer value, so the in-place update applies the same encoding logic used at original crum creation.

---

## Code Exploration

I now have a complete picture of the execution path. Here is the full answer.

---

## Answer: `isanextensionnd` and the ONMYRIGHTBORDER Coalescing Case

The existing crum is **modified in place**. No new crum is allocated. No replacement occurs.

---

### 1. What `isanextensionnd` actually tests

**`insertnd.c:301-309`**:
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

`prologuend` (`retrie.c:334-339`) computes:
- `grasp = offset + ptr->cdsp` — absolute start of the crum
- `reach = grasp + ptr->cwid` — absolute end of the crum (its right border)

Then `lockeq(reach.dsas, originptr->dsas, dspsize(enftype))` (`wisp.c:261-267`) performs element-wise tumbler equality across all dimensions. For SPAN and POOM, `dspsize = 2` (`wisp.h:24-27`), so both the I and V tumbler components must match.

The function returns TRUE only when the new insertion's origin equals the crum's right border — i.e., the new content begins exactly where the existing crum ends. This is the ONMYRIGHTBORDER condition.

---

### 2. What happens when it returns TRUE

The caller is `insertcbcnd` (`insertnd.c:249-258`):

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // line 251
        ivemodified (ptr);                                               // line 252
        setwispupwards (father,1);                                       // line 253
        if(!isfullcrum((typecorecrum*)father)){
            return(setwispupwards(findfather((typecorecrum*)father),1));
        }
        return(FALSE);
    }
}
```

**Line 251** — `dspadd`:

```c
// wisp.c:15-18
int dspadd(typedsp *a, typewisp *b, typedsp *c, INT enftype)
{
    lockadd (a->dsas, b->dsas, c->dsas, (unsigned)dspsize(enftype));
}
```

Called as `dspadd(&ptr->cwid, width, &ptr->cwid, ...)`. This is `c = a + b` with `c == a` — the destination is the same as the first operand. `lockadd` iterates across `dspsize` tumblers, adding each component of `width` to the corresponding component of `ptr->cwid` and writing the result back into `ptr->cwid`. For SPAN/POOM (`dspsize = 2`, `wisp.h:24-27`), both the I-width (`dsas[0]`) and V-width (`dsas[1]`) are extended simultaneously by the incoming width's respective components.

**Line 252** — `ivemodified(ptr)` marks the existing crum as dirty so it gets flushed to disk.

**No new crum is created.** `createcrum` at `insertnd.c:260` is only reached when the `for` loop exhausts all siblings without finding an extension match:

```c
new = createcrum (0, (INT)father->cenftype);   // line 260 — NOT reached on extension
reserve (new);
adopt (new, SON, (typecorecrum*)father);
...
```

---

### 3. What is and is not changed on the existing crum

| Field | Changed? |
|-------|----------|
| `ptr->cwid` (V-width and I-width) | **Yes** — extended by `dspadd` |
| `ptr->cdsp` (displacement / start position) | **No** — not touched |
| `ptr->c2dinfo.homedoc` (home document) | **No** — equality was the gate |
| Crum identity / tree position | **No** — same node, same siblings |

The crum's right edge moves outward (its width grows); its left edge (encoded in `cdsp`, relative to parent grasp) stays fixed. The crum is neither replaced nor moved in the sibling chain.

---

### Summary

`isanextensionnd` detects the ONMYRIGHTBORDER case by checking `lockeq(reach, origin)` — that the new insertion begins exactly at the existing crum's right edge. When it matches, `insertcbcnd` performs a **direct in-place field update**: `dspadd(&ptr->cwid, width, &ptr->cwid, ...)` widens both I and V components of the existing crum's width in a single operation, marks it modified, and returns without allocating any new crum. The crum is extended, not replaced.
