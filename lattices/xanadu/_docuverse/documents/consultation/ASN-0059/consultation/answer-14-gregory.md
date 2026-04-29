## Question 14 [gregory]

> Does `makegappm` shift POOM entries by adding the insertion width to their V-displacement using `tumbleradd`, and if so, does it operate on the relative displacement stored in each crum or on the absolute V-address computed during traversal?

## KB Synthesis

Yes on both counts, and the answer is **relative displacement**.

## `makegappm` shifts relative `cdsp` directly

From [SS-TWO-BLADE-KNIFE] and [ST-INSERT] (Finding 0054), `makegappm` uses a two-blade knife to classify POOM crums into three cases via `insertcutsectionnd`:

- Case 0: crum is before `blade[0]` — no shift
- Case 1: crum is between `blade[0]` and `blade[1]` — **shifted**
- Case 2: crum is at or beyond `blade[1]` — no shift

The shift is applied at [ST-INSERT] (Finding 0054), citing `insertnd.c:162`:

```c
tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V])
```

This operates directly on `ptr->cdsp.dsas[V]` — the **relative displacement** stored in each crum, not the absolute V-address.

## Why relative, not absolute

From [SS-ENFILADE-TREE] (Finding 0066), 2D enfilades (POOM and SPAN) use coordinate-transform-based displacement. Each crum's `cdsp` is stored **relative to its parent's grasp**, not as an absolute V-address. The root's `cdsp` holds the minimum address across all content; children store offsets relative to that. During retrieval, `prologuend` computes `grasp = offset + ptr->cdsp` by accumulating ancestor displacements ([SS-ENFILADE-TREE] Finding 0066, `retrie.c:334-339`).

Since `cdsp` is relative, adding `width` to `cdsp` correctly shifts the crum's absolute position without needing to know the full ancestor chain. After modification, `setwispupwards` recalculates the root's displacement from the new minimum across all children, adjusting relative displacements accordingly ([ST-INSERT] Finding 0066).

## The second blade enforces subspace isolation

From [SS-TWO-BLADE-KNIFE] (Finding 0054), `blade[1]` is always `(N+1).1` for an insertion at `N.x`. This means:

- INSERT at `1.x` → `blade[1] = 2.1` → only crums with `cdsp` in `[1.x, 2.1)` are shifted
- Crums at `2.x` (link subspace) have absolute positions ≥ `2.1`, so `whereoncrum` returns `ONMYLEFTBORDER` or `TOMYRIGHT` relative to `blade[1]`, classifying them as case 2 — **no shift**

This is the structural mechanism behind [FC-SUBSPACE]: INSERT at `1.x` cannot shift link crums at `2.x`. [FC-SUBSPACE] (Finding 0055) notes that DELETE achieves the same isolation incidentally through `strongsub`'s exponent guard, but INSERT's isolation is deliberate by design.

## Summary

`makegappm` adds `width->dsas[V]` to `ptr->cdsp.dsas[V]` (the stored **relative** displacement) for every crum classified as case 1 (between the two blades). Crums outside the blade range — including all crums in other subspaces — are untouched. After all shifts, `setwispupwards` re-anchors the tree by recalculating the root displacement from the new minimum.

---

## Code Exploration

I now have all the data needed. Here is the full answer.

---

## Does `makegappm` shift POOM entries with `tumbleradd`, and on what does it operate?

### Short answers

1. **Yes**, `makegappm` uses `tumbleradd` to shift POOM entries — but only a narrow subset of them (case-1 crums, defined precisely below).
2. It operates on the **relative displacement** stored in each crum (`ptr->cdsp.dsas[V]`), not on the absolute V-address. The absolute position (`fgrasp`) is computed and used only for **classification**, not for the arithmetic of the shift.

---

### Walking the code

#### 1. `prologuend` computes absolute positions from relative displacements

`retrie.c:334-338`:
```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd(offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd(grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```
`grasp = offset + ptr->cdsp`. The parent's absolute position (`offset`) plus the crum's stored relative displacement (`ptr->cdsp`) gives the crum's absolute grasp. This confirms that `ptr->cdsp.dsas[V]` is always a **relative** offset from the parent.

#### 2. `whereoncrum` uses the relative displacement to compute the absolute left boundary

`retrie.c:355-362` (SPAN/POOM branch):
```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
cmp = tumblercmp(address, &left);
if (cmp == LESS)       return(TOMYLEFT);
else if (cmp == EQUAL) return(ONMYLEFTBORDER);
```
`left = offset + ptr->cdsp.dsas[V]` — the absolute left boundary. This is purely for locating the crum; it does not modify `ptr->cdsp`.

`common.h:86-90` defines the return values:
```c
#define TOMYLEFT        -2
#define ONMYLEFTBORDER  -1
#define THRUME           0
#define ONMYRIGHTBORDER  1
#define TOMYRIGHT        2
```

#### 3. `insertcutsectionnd` classifies each child of `father`

`edit.c:207-233`, with `knives->nblades == 2`, `blade[0] = origin`, `blade[1] = origin+ε`:

```c
// Check blade[1] = origin+ε first
i = 1;
cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
if (cmp == THRUME)           return(-1);   // spans blade[1] — should be impossible after cuts
else if (cmp <= ONMYLEFTBORDER) return(2); // crum's left boundary >= origin+ε → RIGHTWARD

// Then check blade[0] = origin
i = 0;
cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
if (cmp == THRUME)           return(-1);   // spans blade[0] — impossible after cuts
else if (cmp <= ONMYLEFTBORDER) return(1); // crum's left boundary ∈ [origin, origin+ε) → AT the slot

return(0);  // crum's right boundary <= origin → LEFTWARD
```

Meaning:
| Return | Condition on crum's absolute left | Semantic |
|--------|-----------------------------------|---------|
| 0 | `left < origin` | entirely to the left of the insertion point |
| 1 | `origin ≤ left < origin+ε` | sitting in the slot carved by the two cuts |
| 2 | `left ≥ origin+ε` | entirely to the right of both cuts |
| −1 | spans a cut | impossible after `makecutsnd`, causes `gerror` |

#### 4. `makegappm`: the shift is on the stored relative displacement

`insertnd.c:124-172`. The relevant logic after `makecutsnd` and `newfindintersectionnd`:

```c
prologuend((typecorecrum*)father, &foffset, &fgrasp, (typedsp*)NULL);  // line 150
for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
    i = insertcutsectionnd(ptr, &fgrasp, &knives);                      // line 152
    switch (i) {
      case 0:
      case 2:
        break;   // no shift
      case -1:
        gerror("makegappm can't classify crum\n");
      case 1:   /* 9-17-87 fix */
        tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);  // line 162
        ivemodified(ptr);
        break;
    }
}
```

Line 162 in full:
```c
tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
```

The three operands are:
- `ptr->cdsp.dsas[V]` — the **relative** V-displacement stored in the crum (input and output)
- `width->dsas[V]` — the insertion width in V-space

`fgrasp` does not appear in this expression. The absolute position is computed at line 150 and passed to `insertcutsectionnd` at line 152 only for the purpose of classifying whether the child falls in case 0, 1, or 2. Once classification is done, `fgrasp` plays no further role: the shift is computed and stored entirely in the crum's own `cdsp` field.

#### 5. Why only case 1, not case 2?

The two cuts at `origin` and `origin+ε` are designed so that case-1 crums are exactly those with their absolute left boundary AT the insertion slot — content that, before the cut, began at `origin`. These are the crums that were split off from whatever spanned `origin`, and they must move rightward to open space for the new content. Case-2 crums (already starting at `origin+ε` or beyond) lie outside the insertion range because, in the POOM's V-space model, `origin+ε` is already guaranteed to be past the new content's V-extent. The second cut position computed by `findaddressofsecondcutforinsert` (`insertnd.c:145`, `insertnd.c:174-183`) is specifically chosen to create this boundary.

---

### Definitive answers

**Q1: Does `makegappm` shift POOM entries using `tumbleradd`?**

Yes — at `insertnd.c:162` — but only for case-1 crums: those whose absolute left boundary (`fgrasp + ptr->cdsp.dsas[V]`) falls in the half-open interval `[origin, origin+ε)`. Case-0 (left of origin) and case-2 (right of `origin+ε`) crums are untouched.

**Q2: Does it operate on the stored relative displacement or the computed absolute address?**

It operates on the **relative displacement** `ptr->cdsp.dsas[V]` stored directly in the crum. The `tumbleradd` at line 162 has the form:

```
new_cdsp_V = old_cdsp_V + width_V
```

`fgrasp` (the absolute V-position of the father node) is computed at line 150 and used at line 152 solely to let `insertcutsectionnd → whereoncrum` compute each child's absolute left boundary for classification. It is never added to or subtracted from during the shift arithmetic. The stored relative displacement is what gets modified, in place.
