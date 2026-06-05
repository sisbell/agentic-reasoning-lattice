## Question 11 [evidence]

> When RETRIEVECONTENTS is given a multi-span SpecSet, does it return content in spec-set order or re-sort the spans by V-address via `incontextlistnd` before delivering bytes?

## KB Synthesis

RETRIEVECONTENTS returns content in **SpecSet order**, not re-sorted by V-address. Two KB entries converge on this:

**[SS-SPECSET]** (Finding 0003) is the primary authority:
> "The ordering of VSpecs within a SpecSet is significant — results reflect the order in which VSpecs are specified... retrieve concatenates in VSpec order."

**[INV-SPECSET-ORDER]** (Finding 0003) restates this as an invariant:
> "Retrieve concatenates content in VSpec order... The formal spec must model SpecSet as a sequence (not a set or bag) and all SpecSet-consuming operations must process VSpecs in sequence order."

**[INV-RETRIEVAL-V-SORTED]** (Finding 0078) operates at a different level — it describes how `incontextlistnd` accumulates contexts in ascending V-address order *during internal POOM B-tree traversal for a single span query*. This guarantees bytes within one VSpec's resolution are returned in V-order, but it does not govern the ordering across VSpecs in the SpecSet.

The data flow is layered:
1. Each VSpec is resolved independently against the POOM via `specset2ispanset` → `findorgl` → `incontextlistnd` (V-sorted internally)
2. The resulting byte sequences are concatenated in SpecSet order

So a SpecSet with VSpec₁ at V:1.10 and VSpec₂ at V:1.1 returns the content of VSpec₁ first, then VSpec₂ — regardless of V-address order. The `incontextlistnd` sort is invisible at the SpecSet level.

---

## Code Exploration

Now I have all the evidence needed. Here is the complete answer.

---

## Does RETRIEVECONTENTS sort by V-address or preserve spec-set order?

**Short answer:** Spec-set order is preserved at the per-V-span level. Within each V-span's results, `incontextlistnd` sorts by V-address — but there is no global re-sort across the full multi-span spec-set.

---

### Full Call Chain

**Entry point — `fns.c:175`:**
```c
void retrievev(typetask *taskptr) {
    if (getretrievev(taskptr, &specset)
     && doretrievev(taskptr, specset, &vstuffset))
         putretrievev(taskptr, &vstuffset);
}
```

**`do2.c:14` — `specset2ispanset`:** iterates the specset linked list; for each `VSPECID` span calls `vspanset2ispanset` (line 36), passing the V-spans forward to the permutation machinery.

**`orglinks.c:397` — `vspanset2ispanset`:**
```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```
Passes `restrictionindex = V`, `targindex = I`.

**`orglinks.c:404` — `permute`:** The outer loop processes V-spans **in spec-set (linked-list) order**, one at a time:
```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                  restrictionindex, targspansetptr, targindex);
}
```
There is no sorting here — each V-span's results are appended sequentially.

**`orglinks.c:425` — `span2spanset`:**
```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr,
                              restrictionindex, (typespan*)NULL,
                              targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan,
                                    (typeitemset*)targspansetptr);
}
```
It iterates the context list in whatever order `retrieverestricted` returns it, then appends each I-span.

**`retrie.c:56` → `retrie.c:87` → `retrie.c:229` — `findcbcinarea2d`:**
This is where the sort happens. For every matching leaf node in the SPAN/POOM enfilade:
```c
context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr);
incontextlistnd(headptr, context, index1);   // retrie.c:263
```
`index1` is the **V-axis** (passed through from `restrictionindex = V`).

**`context.c:74` — `incontextlistnd`:** The comment says it plainly:
```c
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
```
It does an insertion-sort into the linked list using `whereoncontext(..., &grasp.dsas[index], index)` — sorting contexts by their position on the **V-axis**. So the context list returned for a single V-span is **V-address sorted**.

---

### Second leg: I-span → bytes

**`granf1.c:57` — `ispanset2vstuffset`:**
```c
for (; ispanset; ispanset = ispanset->next) {
    vstuffsetptr = ispan2vstuffset(taskptr, granfptr, ispanset, vstuffsetptr);
}
```
Iterates I-spans in the order they were assembled — spec-set order for outer V-spans, V-address sorted within each.

**`retrie.c:112` — `retrieveinspan`:** For GRAN enfilades (the text/content enfilade), uses `findcbcinspanseq` + `oncontextlistseq` — a simple sequential append that preserves I-address order.

**`context.c:113` — `oncontextlistseq`:**
```c
/* on end */
(*clistptr)->lastcontext->nextcontext = c;
(*clistptr)->lastcontext = c;
```
No sorting — appends to the end. This preserves the order content is encountered during the sequential granfilade traversal.

---

### What this means for a multi-span SpecSet

Given a spec-set with two non-adjacent V-spans, e.g. `[vspan_B = 100–110, vspan_A = 10–20]`:

1. `permute` processes `vspan_B` first (spec-set order), calls `findcbcinarea2d`, which via `incontextlistnd(..., V)` returns contexts sorted by V-address **within that span**.
2. The resulting I-spans for `vspan_B` are appended to `ispanset`.
3. `permute` then processes `vspan_A`, same thing.
4. `ispanset2vstuffset` walks the assembled `ispanset` in that order.

**Output byte order: `[content of 100–110][content of 10–20]`** — spec-set order is honored, not globally sorted by V-address.

The `incontextlistnd` V-address sort operates **locally within a single V-span's retrieval call**. It sorts the I-span fragments that a single input V-span maps to — which for a contiguous V-span is just the natural V-order of those fragments. It does **not** perform a global re-sort across the whole spec-set.

---

### Summary table

| Function | File:Line | Ordering behavior |
|---|---|---|
| `permute` outer loop | `orglinks.c:414` | Spec-set order, no sort |
| `span2spanset` → `findcbcinarea2d` | `retrie.c:263` | Calls `incontextlistnd` with `index1 = V` |
| `incontextlistnd` | `context.c:75` | **Sorts by V-address** (within one V-span's context) |
| `ispanset2vstuffset` | `granf1.c:67` | Iterates assembled I-spans, no re-sort |
| `findcbcinspanseq` → `oncontextlistseq` | `context.c:113` | Sequential append, preserves I-address order |

**Bottom line:** RETRIEVECONTENTS delivers bytes in spec-set order (per-V-span level). `incontextlistnd` re-sorts by V-address only within the fragments that a single input V-span maps onto — a local, not global, sort. The spec-set ordering of the input spans is not disturbed.
