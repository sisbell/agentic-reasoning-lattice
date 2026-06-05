## Question 17 [evidence]

> Does the read path traverse the height-1 granfilade leaf as a 1:1 pass-through given MAXBCINLOAF=1, and does the read result depend in any way on the physical tree height after prior growth (EC-EMPTY-DELETE-TREE)?

## KB Synthesis

## Read Path Through Height-1 Granfilade: Yes, Pass-Through

**MAXBCINLOAF=1 makes height-1 a structural pass-through.**

From [SS-GRAN-BOTTOM-SINGLETON] and [SS-GRAN-MB-ONE]: every height-1 non-root granfilade node holds exactly one bottom crum. `splitcrumseq` always creates pairs of height-1 nodes each with one child, and `levelpull` is permanently disabled [SS-ENFILADE-TREE / Finding 0058], so this structure never collapses. The formal characterization from [SS-GRAN-MB-ONE] is direct: *"treat the height-1 layer of a GRAN enfilade as a trivial 1:1 mapping layer, not a branching layer."*

During read traversal (`findcbcseqcrum`, `oncontextlistseq`), the height-1 node contributes exactly one descendant to the context list — no branching decision occurs there. The granfilade is therefore always at least one level taller than a POOM holding equivalent leaf count [SS-GRAN-MB-ONE], and that extra level is observable only in traversal depth, not in read results.

---

## Read Result vs. Prior Tree Height: Independent

From [INV-ENFILADE-QUERY-INDEPENDENCE]: *"Query operations return results independent of the physical tree structure. Different insertion orderings produce different tree shapes but identical query results."*

The widdative (`cwid`) summaries correctly reflect content at any height. An emptied-by-deletion tree at height H and a never-filled tree at height 1 both return empty content on retrieve — the traversal finds no bottom crums with non-zero width in either case.

**However, there is an important caveat for writes post-delete:**

[EC-EMPTY-DOC / Finding 0058] distinguishes two structurally non-equivalent "empty" states:

| State | Height | Bottom nodes | Retrieve | INSERT |
|---|---|---|---|---|
| Never-filled (`createenf`) | 1 | 1 (zero-width) | empty | ✓ works |
| After delete-everything | H (prior growth) | 0 | empty | ✗ **crashes** (Bug 0019) |

After delete-everything, `firstinsertionnd()` calls `findleftson()` which returns NULL (no bottom crums exist). The code then dereferences that null pointer — a crash. So tree height after growth **is** observable, but only through subsequent write operations, not through reads.

**Formal statement:** `read_result(doc) ⊥ enf.height(doc)` — reads are tree-height-independent. But `write_precondition(doc)` implicitly requires `has_bottom_node(enf(doc))`, which the delete-everything state violates regardless of height.

---

## Code Exploration

Now I have everything I need for a complete, citation-backed answer.

---

## Read Path and Tree Height in the Granfilade: A Code-Level Analysis

### Question Decomposed

1. Does the read path traverse the height-1 granfilade layer as a 1:1 pass-through, given `MAXBCINLOAF=1`?
2. Does the read result depend on physical tree height after prior growth followed by full deletion (the "EC-EMPTY-DELETE-TREE" state)?

---

## Part 1: Height-1 Granfilade Layer as 1:1 Pass-Through

### The Constant

`enf.h:27`:
```c
#define MAXBCINLOAF    1        /* so text will fit *//* as you wish */
```

`MAXBCINLOAF=1` applies only to GRAN-type enfilades, as tested by `is2dcrum()` in `genf.c:19-22`:
```c
bool is2dcrum(typecorecrum *ptr)
{
    return (ptr->cenftype != GRAN);
}
```

### The Enforcement in `toomanysons`

`genf.c:239-245`:
```c
bool toomanysons(typecuc *ptr)
{
    if (ptr->height) {
        findleftson(ptr);
    }
    return (ptr->numberofsons > (ptr->height > 1 ? MAXUCINLOAF : (is2dcrum((typecorecrum*)ptr)?MAX2DBCINLOAF:MAXBCINLOAF)));
}
```

For a height-1 GRAN-type node: `MAXBCINLOAF=1`. Any node with 2 children triggers `toomanysons → TRUE`.

### How Height-1 Nodes Get Their Exactly-1 Child

When the height-1 fullcrum would overflow, `splitcrumupwards` (`split.c:27-30`) calls:
```c
if (isfullcrum((typecorecrum*)father)) {
    levelpush(father);
    splitcrum((typecuc*)findleftson(father));
    return(TRUE);
}
```

`levelpush` (`genf.c:279-286`) inserts a new node at the old height:
```c
new=(typecuc *)createcrum ((INT)fullcrumptr->height,(INT)fullcrumptr->cenftype);
...
transferloaf (fullcrumptr, new);
fullcrumptr->height++;
adopt ((typecorecrum*)new, SON, (typecorecrum*)fullcrumptr);
```

Then `splitcrumseq` (`split.c:70-93`) splits that single child (which has 2 CBCs) into two sibling nodes each holding 1 CBC. After this operation:

```
Fullcrum (height=2, numberofsons=2)
  ├── Node1 (height=1, numberofsons=1)
  │     └── CBC-A (height=0)
  └── Node2 (height=1, numberofsons=1)
        └── CBC-B (height=0)
```

Every height-1 non-root node has **exactly 1 CBC child**, always. `roomformoresons` at `genf.c:255-261` returns `numberofsons < MAXBCINLOAF = 1`, meaning TRUE only when a height-1 node has 0 children — which cannot persist stably (it would be an empty intermediate node, cleaned up by `recombine`).

### The Read Path

`findorgl()` (`granf1.c:17`) → `fetchorglgr()` (`granf2.c:22`) → `retrievecrums()` (`retrie.c:15`) → `findcbcseqcrum()` (`retrie.c:167`):

```c
typecrumcontext *findcbcseqcrum(typecorecrum *ptr, typedsp *offsetptr, tumbler *address)
{
    if (!ptr)
        gerror ("findcbcseqcrum called with NULL ptr.");
    for (; getrightbro (ptr); ptr = ptr->rightbro) {
        if (whereoncrum (ptr, offsetptr, address, WIDTH) <= THRUME)
            break;
        dspadd (offsetptr, &ptr->cwid, offsetptr, (INT)ptr->cenftype);
    }
    if (ptr->height != 0) {
        ptr = findleftson ((typecuc*)ptr);
        return (findcbcseqcrum (ptr, offsetptr, address));
    } else {
        return (createcrumcontext (ptr, offsetptr));
    }
}
```

At the height-1 layer, execution is:

1. **Sibling scan** (the `getrightbro` loop): walks height-1 nodes left-to-right until the one whose width covers the target address is found.
2. **Found**: `ptr->height != 0` (height-1, not 0) → call `findleftson((typecuc*)ptr)`.
3. **`findleftson` returns the single CBC child** — because `numberofsons=1` and there is exactly one child to return. `genf.c:206-232` shows `findleftson` returns `ptr->leftson` (the one-and-only left/only child).
4. **Recurse** with the CBC: `ptr->height == 0` → `return createcrumcontext(ptr, offsetptr)`.

**The step from height-1 CUC → height-0 CBC is the 1:1 pass-through.** There is no lateral scan at the CBC level — the recursive call enters with the leaf directly. One `findleftson` call, one recursive `findcbcseqcrum` call, one `createcrumcontext` return. No branching.

**Verdict: YES — the height-1 layer is a 1:1 pass-through.** Each height-1 CUC is a transparent envelope around exactly one CBC.

---

## Part 2: Read Result Dependence on Tree Height After EC-EMPTY-DELETE-TREE

### What EC-EMPTY-DELETE-TREE Is

After content is deleted, `levelpull` (`genf.c:318`) is **disabled**:

```c
int levelpull(typecuc *fullcrumptr)
{
/*  typecuc *ptr; */
return(0);
/* ... commented-out collapse logic ... */
}
```

`levelpull` is called from `recombineseq` (`recombine.c:66-68`) and `recombinend` (`recombine.c:129-131`) at the end of every recombine cycle — but since it immediately returns 0, tree height **never decreases**. A tree that grew to height H via `levelpush` stays at height H forever, even after all content is deleted.

After delete-all, the tree looks like:

```
Fullcrum (height=H, cwid.dsas[WIDTH]=0)
  ├── Height-(H-1) node (numberofsons=0, leftson=NULL)
  └── Height-(H-1) node (numberofsons=0, leftson=NULL)
```

(As documented in Finding 0058 and confirmed by `edit.c:59-60`'s `disown + subtreefree` on every bottom crum.)

### The Width Guard in `fetchorglgr`

`granf2.c:31-35`:
```c
if (tumblercmp (&((typecuc*)fullcrumptr)->cwid.dsas[WIDTH], address) == LESS)
    return (NULL);
```

After delete-all, `setwispupwards` (`genf.c` / `makeroom.c`) propagates the zeroed widths upward from each disowned CBC. The fullcrum's `cwid.dsas[WIDTH]` becomes the zero tumbler.

For any non-zero ISA address lookup: `tumblercmp(zero, address) == LESS` → TRUE → `fetchorglgr` returns `NULL` **immediately**, before `retrievecrums` or `findcbcseqcrum` is ever called.

**The read result (NULL) is therefore independent of tree height.**

Whether the tree is at height 2 or height 10 post-delete, the width guard fires first. `findcbcseqcrum` never executes. The physical structure left over from growth is unreachable and irrelevant to the result.

### The Important Caveat

This guarantee holds **only if wid maintenance is correct** — i.e., if `setwispupwards` correctly propagates zero widths after delete-all. If wid accounting were to fail (leaving the fullcrum's WIDTH non-zero when the tree has no leaves), then `findcbcseqcrum` would be called on a leafless tree and would hit the null-pointer check at `retrie.c:172-177` when `findleftson` returns NULL for an empty CUC. This scenario was the root cause of **Bug 0019** (Finding 0064), where INSERT/VCOPY after delete-all crashed because `firstinsertionnd` assumed a CBC always existed.

For **reads** (not writes), the same path applies: a wid-accounting failure post-delete would expose the traversal to a NULL `findleftson` dereference at height-dependent depth. The height would then matter — a taller tree means more recursive levels before hitting the NULL crash. But under correct wid maintenance (the normal case), the height is irrelevant.

### Summary of Height Dependence

| Scenario | Read Result | Height Matters? |
|---|---|---|
| Empty after delete-all, wids correct | `fetchorglgr` returns NULL at `granf2.c:31` | **No** |
| Empty after delete-all, wid bug | `findcbcseqcrum` crashes at NULL `findleftson` | **Yes** (crash depth = H) |
| Partially populated after delete | Normal traversal via wids | **No** (wids route correctly at any height) |

---

## Final Answers

**1. 1:1 pass-through at height-1 layer — YES.**

With `MAXBCINLOAF=1` (`enf.h:27`), every height-1 non-root GRAN node holds exactly 1 CBC. `findcbcseqcrum` (`retrie.c:183-188`) descends from the height-1 CUC to its sole child via one `findleftson` call, then immediately returns the leaf context. No branching, no lateral scan at the leaf step. The height-1 node is a pure structural wrapper.

**2. Read result does NOT depend on physical tree height after EC-EMPTY-DELETE-TREE — under correct wid maintenance.**

`fetchorglgr` (`granf2.c:31`) guards the entire traversal with a pre-check against the fullcrum's `cwid.dsas[WIDTH]`. For a logically empty tree (all content deleted), this width is zero. Any non-zero address query short-circuits to NULL before `findcbcseqcrum` is invoked. The elevated height left over from prior growth (due to `levelpull` being disabled at `genf.c:318`) is unreachable by the read path and has no effect on the result. Height affects only traversal depth (performance), not correctness — provided wid accounting is sound.
