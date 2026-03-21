## Question 15 [gregory]

> When `deletend` calls `subtreefree` on fully-contained crums, does it free only the POOM tree nodes (upper crums and bottom crums), or does it also touch the granfilade leaf nodes those bottom crums pointed to — and is there any reference-counting mechanism that tracks how many POOMs reference a given I-address range?

## KB Synthesis

`subtreefree` frees only the POOM tree nodes — the in-memory crum structures themselves — and does not touch the granfilade.

## What `subtreefree` frees

When `deletend` classifies a bottom crum as fully within the deletion range (Case 1), it calls `disown` to remove the crum from its parent/sibling pointers, then `subtreefree` to recursively free memory (`credel.c:413-436`). These are POOM crums: upper crums and bottom crums that store the V→I displacement/width mappings. Freeing them removes the document's V-address-to-I-address mappings. [ST-DELETE, Finding 0064]

The granfilade leaf nodes the bottom crums point to are untouched. The granfilade is strictly append-only — no deletion function exists anywhere in the granf codebase. DELETE modifies only the spanfilade's POOM layer; `dodeletevspan` makes no call to any granf removal function. [FC-GRANF-ON-DELETE, INV-IADDR-IMMUTABILITY]

The canonical statement from the KB: "DELETE frees the POOM bottom crums that *reference* I-addresses, but the I-addresses themselves persist in the granfilade unconditionally." [INV-IADDR-IMMUTABILITY, Finding 0064]

## Reference counting

The disk loaf header structure does include a `refcount` field, described in the source as "For subtree sharing / GC":

```c
typedef struct structdiskloafhedr {
    ...
    SINT refcount;  // For subtree sharing / GC
    ...
} typediskloafhedr;
```
[SS-UNIFIED-STORAGE, Finding 0059]

However, the KB contains no finding documenting this field being used to track how many POOMs reference a given I-address range. The behavioral evidence points the other way: multiple documents can reference the same I-addresses via transclusion with no documented coordination between their POOMs [FC-DELETE-CROSS-DOC], and there is no garbage collection of I-addresses — the monotonic allocation invariant means every allocated I-address persists forever regardless of how many (or zero) POOMs currently reference it [INV-NO-IADDR-REUSE, INV-MONOTONIC].

The `refcount` field appears to have been intended infrastructure for subtree sharing or GC that was never implemented in a way that affects I-address lifetime. This is consistent with the broader pattern in the codebase of intended-but-unimplemented enforcement (e.g., `acceptablevsa` always returning TRUE [SS-SUBSPACE-CONVENTION], `levelpull` being disabled [SS-ENFILADE-TREE]).

## Summary

- `subtreefree` frees POOM crum nodes only (in-memory tree structures storing V→I mappings)
- Granfilade leaf nodes are not touched — they are permanent by design
- No active reference-counting mechanism tracks how many POOMs reference a given I-address range; the `refcount` field exists structurally but has no documented behavioral role in managing I-address reachability

---

## Code Exploration

I now have all the information I need. Let me compile the complete answer from the source code evidence.

---

## Answer: `subtreefree` scope and reference counting in POOM deletion

### 1. What `subtreefree` actually frees

`deletend` calls `subtreefree` for case 1 — crums fully inside the knife cuts — at `edit.c:59-61`:

```c
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);
    break;
```

The implementation is at `credel.c:413-432`:

```c
/* assumes crum is disowned */
void subtreefree(typecorecrum *ptr)
{
  typecorecrum *p, *right;

    if (!ptr)
        gerror ("boom in subtreefree called with ptr == NULL");
    if (ptr->height > 0) {
        for (p = ((typecuc *)ptr)->leftson; p; p = right) {
            right = p->rightbro;
            disown (p);
            subtreefree (p);
        }
    } else if (ptr->cenftype == GRAN && ((typecbc *)ptr)->cinfo.infotype == GRANORGL && ((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglincore)
        orglfree (((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglptr);
    freecrum (ptr);
}
```

The logic branches on `height`:

- **Height > 0 (upper crums)**: Recursively `disown` + `subtreefree` every child, then `freecrum(ptr)`.
- **Height == 0 (bottom crums)**: Enters the `else if` only when **all three** conditions hold: `cenftype == GRAN`, `infotype == GRANORGL`, and `orglincore == TRUE`. Otherwise calls only `freecrum(ptr)`.

**POOM bottom crums always miss this branch.** A POOM bottom crum is `type2dcbc` with `cenftype == POOM` (`enf.h:113`). The condition `ptr->cenftype == GRAN` is false, so execution goes directly to `freecrum(ptr)`.

### 2. What POOM bottom crums actually contain

`type2dcbc` is defined at `enf.h:109-131`. Its payload field is:

```c
type2dbottomcruminfo c2dinfo;
```

And `type2dbottomcruminfo` is defined at `wisp.h:107-109`:

```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

That's it — a single `tumbler` value stored **by value** inside the struct. There is no pointer to any granfilade node. The `homedoc` tumbler records the I-address of the home document (the document this V→I mapping belongs to), but it is a coordinate by value, not a heap pointer. `freecrum` releases only the crum struct itself.

This is confirmed by the extension check in `insertnd.c:305`:

```c
if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
    return (FALSE);
```

Both sides are tumblers compared by value — no pointer dereferencing into the granfilade.

### 3. When would `subtreefree` reach the granfilade?

Only when freeing a **GRAN** bottom crum with `infotype == GRANORGL` and `orglincore == TRUE`. In that case, `orglfree` (`credel.c:470-490`) is called:

```c
void orglfree(typecuc *ptr)
{
    ...
    ((typecbc *)ptr->leftbroorfather)->cinfo.granstuff.orglstuff.orglincore = FALSE;
    ((typecbc *)ptr->leftbroorfather)->cinfo.granstuff.orglstuff.orglptr = NULL;
    subtreefree ((typecorecrum*)ptr);
}
```

This clears the `orglincore`/`orglptr` fields on the back-pointer (the granfilade bottom crum), then recursively calls `subtreefree` on the POOM enfilade that was stored inside the GRAN orgl crum. **This POOM enfilade is the per-document orgl.** But this path is entered from the GRAN side, not from a POOM deletion. When `deletend` operates on a POOM (version enfilade), none of the POOM crums it frees have `cenftype == GRAN`, so `orglfree` is never called and the granfilade is never touched.

**The call chain that would touch the granfilade is**:  
`deleteseq` (edit.c:16) → `freecrum(granfilade bottom crum)` — or — any path that reaches `subtreefree` on a GRAN bottom crum directly.

### 4. Reference counting for I-address ranges

**In-core: None exists.**

The `typecorecrum` / `typecuc` / `typecbc` structs (all defined in `enf.h:31-131`) have no `refcount` or `usecount` field. The closest thing is a deliberate TODO comment in `freecrum` at `credel.c:450`:

```c
/*zzz should it decrement usecount here sometimes?*/
```

This comment sits between the grimreaper circular-list unlinking and the `efree()` call. It is a dead stub — the field was never added and the decrement was never implemented.

**On-disk: A reference count exists, but for loaf sharing, not I-address tracking.**

`typediskloafhedr` in `coredisk.h:18` has:

```c
SINT refcount;      /* for subtree sharing, */
                    /* disk garbage collecting */
```

The functions `changerefcount` and `changeunterrefcount` in `disk.c:60-154` increment or decrement this when disk loafs are shared during write-out (`corediskout.c:336`, `corediskout.c:397`, `corediskout.c:485`). This tracks shared disk blocks so the disk garbage collector can free them only when the last referent is gone.

This on-disk ref count is at the **loaf level** (groups of crums packed together on disk), not at the I-address level. It answers "how many on-disk subtrees share this serialized loaf block", not "how many POOMs reference a given I-address range."

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Does `subtreefree` touch granfilade nodes when freeing POOM crums? | **No.** POOM bottom crums (`cenftype == POOM`) skip the `else if ... GRAN` branch entirely. | `credel.c:423-431` |
| What do POOM bottom crums contain that `subtreefree` must clean up? | Only a `tumbler homedoc` stored by value. No heap pointer. `freecrum()` suffices. | `wisp.h:107-109`, `enf.h:109-131` |
| Is there in-core reference counting for I-address ranges? | **No.** The `/*zzz should it decrement usecount here sometimes?*/` comment in `freecrum` marks an unimplemented idea. No `refcount` field exists in any crum struct. | `credel.c:450`, `enf.h:31-131` |
| Is there any reference counting at all? | On-disk only: `typediskloafhedr.refcount` tracks shared serialized loaf blocks for disk GC. Managed by `changerefcount`/`changeunterrefcount` in `disk.c`. | `coredisk.h:18`, `disk.c:60-154` |

The net consequence: when `deletend` calls `subtreefree` on fully-contained POOM nodes, it performs a pure in-memory free of those POOM tree nodes (upper and bottom). The granfilade is left entirely undisturbed. Nothing tracks how many POOMs reference a given I-address range, because POOM bottom crums carry that information as a plain tumbler value — a coordinate, not a counted pointer.
