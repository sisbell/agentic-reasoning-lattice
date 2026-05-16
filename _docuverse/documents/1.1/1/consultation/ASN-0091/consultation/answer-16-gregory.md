## Question 16 [gregory]

> What happens in `rearrangend` when the supplied cut points are outside the document's current V-span — does the function detect this and abort, silently produce a no-op, or apply offsets to whatever entries happen to be in range?

## KB Synthesis

The KB doesn't have a finding that directly probes this specific scenario, but the behavior is fully derivable from what's documented.

## No detection or abort — silent no-op for out-of-range cuts

**Step 1: No bounds validation exists.** [PRE-REARRANGE] (Finding 0056) documents only two precondition checks: `|cuts| ∈ {3,4}` (enforced with abort) and `sortknives()` which silently reorders misordered cuts. There is no check that cut points fall within the document's V-span. [ST-REARRANGE] (Finding 0056) confirms the algorithm is pure offset arithmetic — `rearrangend()` calls `makeoffsetsfor3or4cuts()` then classifies each orgl via `rearrangecutsectionnd()` and applies `tumbleradd()`. No bounds comparison occurs before this loop.

**Step 2: Classification handles out-of-range content correctly.** `rearrangecutsectionnd()` assigns each POOM orgl a section number based on its V-position relative to the sorted cuts. For a pivot `[c0, c1, c2]`:

- Orgls with `vpos < c0` → section 0, diff = 0 (no movement)
- Orgls with `c0 ≤ vpos < c1` → section 1, diff = `c2 - c1`
- Orgls with `c1 ≤ vpos < c2` → section 2, diff = `-(c1 - c0)`
- Orgls with `vpos ≥ c2` → exterior, diff = 0 (no movement)

If cuts are entirely beyond the document's V-span, every orgl falls in section 0 (diff = 0). If cuts are entirely before the document's V-span, every orgl falls in the exterior (diff = 0). In both cases: no orgl is modified.

**Step 3: Empty regions are explicitly handled.** [EC-REARRANGE-EMPTY-REGION] states: "If a region `[cutN, cutN+1)` contains no content, it contributes to offset computation but doesn't move anything. The algorithm operates per-span, and empty regions simply have no spans to process." When cuts are entirely outside the document, every region between the cuts is also empty — the offsets are computed (diff[1], diff[2] get nonzero values) but there are no orgls classified into those sections to receive them.

**Step 4: No cross-section contamination.** The two-blade knife used by INSERT would normally guard subspace boundaries, but rearrange uses a different mechanism (`rearrangecutsectionnd`). As documented in [ST-REARRANGE] (Finding 0056), the exterior of the cut range always receives diff = 0 regardless of arithmetic — the offset table only contains nonzero entries for the interior sections.

## Summary

`rearrangend` produces a silent no-op when all cut points fall outside the document's V-span. The function computes offsets, iterates all orgls, classifies each as exterior (section 0 or terminal), applies diff = 0, and exits with the POOM unmodified. No error is returned, no backend abort occurs, and the front end receives a success response (per the response-before-check pattern documented in [EC-RESPONSE-BEFORE-CHECK]).

---

## Code Exploration

Now I have everything I need. Here is the complete analysis.

---

## What `rearrangend` does when cut points are outside the document's V-span

### Call chain (no bounds checking anywhere)

```
fns.c:159    rearrange()
do1.c:39     → dorearrange() → rearrangepm()
orglinks.c:137-142  → rearrangepm() calls rearrangend((typecuc*)docorgl, cutseqptr, V) then returns TRUE
edit.c:78    → rearrangend()
```

`rearrangepm` [orglinks.c:137-142] is a literal one-liner that passes the cut sequence straight through:

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

There is **no validation of cut positions against the document's V-span at any level**: not in `fns.c`, not in `do1.c`, not in `rearrangepm`, and not in `rearrangend` itself.

---

### Step 1: `makecutsnd` — splitting crums at the cut positions

`rearrangend` [edit.c:110] calls `makecutsnd(fullcrumptr, &knives)`, which calls `makecutsdownnd` [ndcuts.c:33], which calls `makecutsbackuptohere` [ndcuts.c:69].

The critical inner test is in `makecutsbackuptohere` [ndcuts.c:77-91]:

```c
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
            // only splits when THRUME
            slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], ...);
```

`whereoncrum` [retrie.c:355-373] for POOM/SPAN computes:

```
left  = offset.dsas[index] + ptr->cdsp.dsas[index]
right = left + ptr->cwid.dsas[index]
```

and returns one of `{TOMYLEFT, ONMYLEFTBORDER, THRUME, ONMYRIGHTBORDER, TOMYRIGHT}`. A split (call to `slicecbcpm`) **only happens when the return is `THRUME`**, i.e., when the cut address strictly falls inside a crum's extent.

**If a cut point is outside the document's V-span, it will be either `TOMYRIGHT` (past the right end) or `TOMYLEFT` (before the left start) for every crum. `slicecbcpm` is never called for that cut. No crum is split at that position.** Out-of-span cuts produce no structural changes to the enfilade in phase 1.

---

### Step 2: `newfindintersectionnd` — the stub that changed everything

`rearrangend` [edit.c:111] calls `newfindintersectionnd`. The old traversal-based `findintersectionnd` that descended to the common-ancestor crum is entirely commented out [ndinters.c:18-37]. The current implementation [ndinters.c:38-42] is a stub:

```c
int newfindintersectionnd(typecuc *fullcrumptr, typeknives *knives, typecuc **ptrptr, typewid *offset)
{
    *ptrptr = fullcrumptr;
    clear(offset, sizeof(*offset));
}
```

`father` is always set to `fullcrumptr` (the document root) and `foffset` is always zero. `prologuend(father, &foffset, &fgrasp, NULL)` [retrie.c:334-339] then computes `fgrasp = foffset + father->cdsp = fullcrumptr->cdsp` — the root's own displacement (zero for a well-formed full crum).

**Consequence:** The loop at [edit.c:113] always iterates over the direct children of the document root, not over a narrowed subtree.

---

### Step 3: `rearrangecutsectionnd` — classifying each crum

For each child `ptr`, `rearrangecutsectionnd` [edit.c:191-204] is called:

```c
for (i = knives->nblades -1; i >= 0; --i) {
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME)      return (-1);           // error — cut passes through, should have been split
    else if (cmp <= ONMYLEFTBORDER) return (i+1);  // knife is left of or at crum's left border
}
return (0);   // all knives are to the right of this crum
```

The logic is: iterate knives from highest to lowest. Return the index of the rightmost knife that is **at or to the left of** the crum's start. Return 0 if no knife qualifies (all knives are `TOMYRIGHT`).

---

### Step 4: `makeoffsetsfor3or4cuts` — the displacement table

The precomputed displacement table [edit.c:164-184] for sorted blades b0 < b1 < b2 (3-cut case):

```c
diff[1] = b2 - b1      // moves section 1 forward to the destination
diff[2] = -(b1 - b0)   // moves section 2 back by selection length (negated)
diff[3] = 0            // explicit tumblerclear
```

For 4-cut:
```c
diff[1] = b2 - b0
diff[2] = (b3 - b2) - (b1 - b0)
diff[3] = -(b2 - b0)   // negated diff[1]
case 4 → explicitly "never moves"
```

---

### Behavior for the three out-of-bounds cases

#### Case A: All cuts are **beyond the document's right end** (all blades `> right_end`)

For any crum `ptr`:
- `whereoncrum(ptr, offset, blade[i], V)` returns `TOMYRIGHT` for all `i` — the blade is to the right of the crum
- In `rearrangecutsectionnd`: all iterations return `TOMYRIGHT` (not `<= ONMYLEFTBORDER`), loop falls through → **returns 0**
- In `rearrangend` [edit.c:122-123]: `case 0` → **no displacement applied**
- `makecutsnd` made no splits
- **Result: complete silent no-op.** The enfilade is structurally unchanged. `setwispupwards` and `recombine` run but find nothing to do.

#### Case B: All cuts are **before the document's left start** (all blades `< left_start`)

For any crum `ptr`:
- `whereoncrum(ptr, offset, blade[i], V)` returns `TOMYLEFT` for all `i`
- In `rearrangecutsectionnd`: i starts at `nblades-1`; first knife is `TOMYLEFT` → `<= ONMYLEFTBORDER` → returns `nblades`
  - **3-blade cut**: returns 3 → `diff[3] = 0` (explicitly cleared by `tumblerclear`) → displacement added is zero → **no-op**
  - **4-blade cut**: returns 4 → `case 4` is grouped with `case 0` as "these never move" [edit.c:122-123] → **no-op**
- **Result: complete silent no-op.**

#### Case C: **Partial overlap** — some cuts in-span, some outside

This is the dangerous case.

`makecutsnd` will split crums at the in-span cut positions but produce **no splits** at the out-of-span positions. The enfilade is thus partially restructured: cut boundaries exist at some of the blade positions but not all.

`makeoffsetsfor3or4cuts` performs **pure tumbler arithmetic** on all the blade values with no awareness of document bounds [edit.c:164-184]. For example, in a 3-cut rearrangement where blade[2] (the destination) is outside the document's right end:

```
diff[1] = blade[2] - blade[1]
```

This is computed as a large positive tumbler value. In the classification loop, crums classified as section 1 (between blade[0] and blade[1], i.e., the selected region) receive:

```c
tumbleradd(&ptr->cdsp.dsas[V], &diff[1], &ptr->cdsp.dsas[V]);  // edit.c:125
ivemodified((typecorecrum*)ptr);                                  // edit.c:127
```

The displacement is applied unconditionally. The crums are moved to a V-address that is outside the document's current span — or into negative/undefined tumbler space if the blade was before the left start.

**There is no check, no abort, no rollback.** The `ivemodified` call marks each such crum as dirty, causing them to be written back to disk in the corrupted state.

---

### Summary

| Situation | `makecutsnd` | `rearrangecutsectionnd` result | Effect |
|---|---|---|---|
| All cuts past right end | No splits | 0 for all crums | Silent no-op |
| All cuts before left start | No splits | `nblades` for all crums → `diff[nblades] = 0` (3-cut) or case 4 (4-cut) | Silent no-op |
| Partial overlap (some in, some out) | Splits only at in-span cuts | In-span section crums classified normally; get `diff[i]` applied using out-of-span blade arithmetic | **Blindly applies offset; corrupts crum displacements; no error** |

`rearrangend` contains **no bounds detection of any kind**. The function trusts entirely that the caller has validated cut points against the document's V-span. When that assumption is violated:

- **Pure out-of-bounds inputs** happen to produce a no-op, not through any defensive logic, but as an accidental consequence of `whereoncrum` returning `TOMYRIGHT`/`TOMYLEFT` on every crum, which maps to case 0 or cases that apply a zero displacement.
- **Mixed in/out-of-bounds inputs** bypass the accidental safety entirely — the in-span portion of the operation proceeds while the out-of-span blade values are fed raw into tumbler arithmetic, producing structurally invalid crum displacements without any indication of failure.
