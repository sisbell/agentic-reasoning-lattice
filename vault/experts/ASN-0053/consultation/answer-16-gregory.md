## Question 16 [gregory]

> In SpecSet composition, what ordering invariant do the component VSpecs maintain — must they be non-overlapping, sorted by start position, or can a SpecSet contain redundant or overlapping spans?

## KB Synthesis

## SpecSet Ordering and Overlap Invariants

The KB establishes the following, though the overlap question is only partially answered.

### Established: Order Is Significant, No Sort Required

[SS-SPECSET] defines `SpecSet = seq<VSpec>` — a **sequence**, not a set. The ordering is operationally significant: `retrieve` concatenates content in VSpec order, `vcopy` places content in VSpec order. [INV-SPECSET-ORDER] confirms all SpecSet-consuming operations preserve this sequence order as an invariant.

Crucially, no sorted-by-start-position requirement is stated anywhere. The system respects the caller-specified order; the backend is not documented to sort or reorder VSpecs before processing.

### Established: No Non-Overlap Requirement at the Backend

[PRE-SPECSET] specifies that backend validation checks only document existence — it does NOT validate element-level structure or structural relationships between VSpecs. The implementation does not enforce non-overlap between component spans.

[PRE-COPY] (Finding 0046) states explicitly that COPY **performs no duplicate checking** before inserting V→I mappings. The same I-address can intentionally appear at multiple V-positions via repeated COPY. [SS-POOM-MULTIMAP] confirms the POOM is a multimap: a single I-address can map to multiple V-positions.

### Inferred: Redundant/Overlapping Spans Are Accepted and Processed Redundantly

From [INV-IDENTITY-OVERLAP], overlapping transclusion regions are valid — overlapping characters in the destination share I-position identity with the source. [EC-SELF-TRANSCLUSION] confirms a document can transclude content from itself, producing duplicate I-address references.

Given no overlap check at any layer, a SpecSet with overlapping VSpecs would be accepted. On `retrieve`, the overlapping byte range would appear twice in the output (once per VSpec, in sequence order). On `vcopy`, the overlapping I-addresses would be placed at multiple V-positions in the destination.

### Summary

| Constraint | Status |
|------------|--------|
| Sequence order preserved | **Enforced** — all operations respect VSpec order [INV-SPECSET-ORDER] |
| VSpecs must be sorted by start position | **Not required** — no such precondition exists |
| VSpecs must be non-overlapping | **Not enforced** — backend validates only document existence [PRE-SPECSET] |
| Redundant spans cause errors | **Not documented** — POOM multimap and no-duplicate-check [PRE-COPY] imply they are processed as given |

The KB does not contain a direct test of overlapping-VSpec behavior in a single SpecSet, so the redundant-processing behavior above is inferred from the multimap structure and absence of any overlap guard, rather than directly observed.

---

## Code Exploration

Now I have everything I need. Here is the complete answer.

---

## SpecSet Composition: VSpec Ordering Invariants

### Data Structure

The relevant types are defined in `backend/xanadu.h`:

```c
// xanadu.h:73-74
typedef typespan typevspan;
typedef typevspan * typevspanset;

// xanadu.h:78-83
typedef struct structtypevspec{
        struct structtypevspec *next;
        typeitemid      itemid;
        typeisa docisa;          // which document
        typevspanset vspanset;   // linked list of VSpans within that doc
} typevspec;

// xanadu.h:85-89
typedef union {
        typevspec xxxvspec;
        typeispan xxxispan;
} typespec;
typedef typespec * typespecset;
```

A **SpecSet** is a singly-linked list of `typespec` items, each of which is either a VSpec (virtual specification: a document ISA + a set of V-space spans) or a raw ISpan. The two levels of structure — the SpecSet itself and the `vspanset` inside each VSpec — have completely different invariants.

---

### Level 1: Within a VSpec's `vspanset` — Strict Invariants Enforced

The only function that inserts a VSpan into a vspanset is `putvspaninlist` [`orglinks.c:329-387`]. It is the gatekeeper, and it enforces three invariants aggressively:

**1. Sorted by start position (`stream`)**

The function walks the list comparing the new span's start against each existing span's end:

```c
// orglinks.c:342
for (; ptr; last = ptr, ptr = ptr->next) {
    tumbleradd (&spanptr->stream, &spanptr->width, &newspanend);
    tumbleradd (&ptr->stream, &ptr->width, &oldspanend);
    spancmp = tumblercmp (&spanptr->stream, &oldspanend);
    ...
    } else if (spancmp == GREATER)
        continue;   // skip past spans that end before new one starts
```

It inserts at the correct position once it finds where the new span fits in the ordering [`orglinks.c:356-361`]:

```c
} else if (spancmp == GREATER) {
    if (ptr != *spansetptr)
        last->next = makevspan (taskptr, spanptr, ptr);
    else
        *spansetptr = makevspan (taskptr, spanptr, ptr);
    return(0);
}
```

**2. Non-overlapping — overlapping spans are merged, not stored separately**

When the new span overlaps an existing one, `putvspaninlist` mutates the existing node to subsume both spans rather than inserting a duplicate. The `startcmp`/`endcmp` switch at lines 363–384 covers all overlap cases:

- New span is **fully contained** in existing → early return, nothing added [`orglinks.c:365-366`]:
  ```c
  if (startcmp > LESS && endcmp < GREATER)
      return(0);
  ```
- Same start, new is longer → widen existing width [`orglinks.c:368-370`]
- New starts earlier, new ends earlier (partial left overlap) → extend start leftward and recompute width [`orglinks.c:372-377`]
- New starts later, new ends later (partial right overlap) → extend width rightward [`orglinks.c:379-382`]

**3. Adjacent (touching) spans are merged**

When the new span starts exactly where an existing span ends (`tumblercmp` returns 0), the widths are summed:

```c
// orglinks.c:346-348
spancmp = tumblercmp (&spanptr->stream, &oldspanend);
if (!spancmp) {
    tumbleradd (&ptr->width, &spanptr->width, &ptr->width);
    return(0);
```

Similarly, when an existing span starts exactly where the new span ends [`orglinks.c:352-355`]:
```c
spancmp = tumblercmp (&ptr->stream, &newspanend);
if (!spancmp) {
    movetumbler (&spanptr->stream, &ptr->stream);
    tumbleradd (&spanptr->width, &ptr->width, &ptr->width);
    return(0);
```

**Summary for `vspanset`:** VSpans within a single VSpec are always non-overlapping, non-adjacent, and sorted ascending by `stream`. This is not a convention — `putvspaninlist` actively enforces it by merging any new span that would violate these conditions.

---

### Level 2: Across VSpecs in a SpecSet — No Invariants

`specset2ispanset` [`do2.c:14-46`] is the primary consumer of a SpecSet. It iterates each element sequentially:

```c
// do2.c:23-39
for (; specset; specset = (typespec *)((typeitemheader *)specset)->next) {
    if (((typeitemheader *)specset)->itemid == ISPANID) {
        *ispansetptr = (typeispanset)specset;
        ispansetptr = (typeispanset *)&((typeitemheader *)specset)->next;
    } else if (((typeitemheader *)specset)->itemid == VSPECID) {
        ...
        ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr)
    }
}
```

There is no ordering check, no overlap check, and no deduplication between VSpecs. Each VSpec is processed independently. The SpecSet is consumed as a plain linked list in whatever order items were inserted.

`onitemlist` [`orglinks.c:464-537`], which appends items to a SpecSet, simply walks to the tail and links the new item — no sorting, no deduplication:

```c
// orglinks.c:521-534
for (temp = *itemsetptr;
     temp && ((typeitemheader *)temp)->next;
     temp = (typeitem *)((typeitemheader *)temp)->next)
    ;
((typeitemheader *)temp)->next = (typeitemheader *)newitem;
```

Multiple VSpecs in a SpecSet can therefore:
- Reference the same document (`docisa`) with overlapping or redundant V-spans
- Reference different documents in any order
- Contain ISpans interleaved with VSpecs in any sequence

---

### The Commented-Out Consolidation Evidence

The absence of cross-VSpec consolidation is not an accident. `orglinks.c` contains two traces of work that was explicitly abandoned:

**1. `consolidatespans` call disabled in `permute`** [`orglinks.c:412-413`]:
```c
/*consolidatespans(restrictionspanset);
foospanset("restrictionset after consolidation is ",restrictionspanset);    */
```

**2. `cleanupvspanlist` function and the entire alternative `retrievevspansetpm` implementation** are wrapped in `#ifdef UnDEFined` [`orglinks.c:263-313`]. The disabled `cleanupvspanlist` would have merged only *adjacent* vspans (using `tumblereq` equality at line 307), not overlapping ones — which tells us the active `putvspaninlist` is the more correct and complete approach.

**3. A `consolidatespanset` stub** (commented, never completed) appears at [`orglinks.c:455-462`]:
```c
/*
consolidatespanset(spanset);
  typespan *spanset;
{
    for(;spanset->next;spanset = spanset->next){
        if(
    }
}*/
```

This confirms cross-SpecSet consolidation was considered and deliberately left unimplemented.

---

### Summary Table

| Level | Invariant | Enforced? | Where |
|---|---|---|---|
| Within a VSpec's `vspanset` | Sorted ascending by `stream` | **Yes, enforced** | `putvspaninlist` `orglinks.c:342-361` |
| Within a VSpec's `vspanset` | Non-overlapping (merged) | **Yes, enforced** | `putvspaninlist` `orglinks.c:363-384` |
| Within a VSpec's `vspanset` | Non-adjacent (touching merged) | **Yes, enforced** | `putvspaninlist` `orglinks.c:346-355` |
| Between VSpecs in a SpecSet | Sorted by any criterion | **No** | `onitemlist` appends to tail `orglinks.c:521-534` |
| Between VSpecs in a SpecSet | Non-overlapping across docs | **No** | `specset2ispanset` iterates blindly `do2.c:23-39` |
| Between VSpecs in a SpecSet | No redundant entries | **No** | Consolidation code commented out `orglinks.c:412-413` |

**The invariants are strictly local**: a SpecSet can contain redundant or overlapping entries across its component VSpecs, but within each VSpec the vspanset is always a canonicalized, sorted, merged, non-overlapping sequence of V-space spans.
