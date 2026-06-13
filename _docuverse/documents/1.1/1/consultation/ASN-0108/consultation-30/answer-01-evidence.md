## Question 1 [evidence]

> When the link-search builds its result list by insertion-sort during the index traversal, does the sort key it compares on resolve to the matched content's permanent I-address (immutable, surviving rearrangement and orphaning) or to that content's current V-position within the consulted document (which moves under K.μ~ and disappears under K.μ⁻)?

## KB Synthesis

## Sort Key in Link-Search Result Accumulation

The answer depends on which enfilade the traversal actually operates over.

### The Spanfilade Is an I-Address-Indexed Structure

`find_links` and `RETRIEVEENDSETS` traverse the **spanfilade** (SPAN enfilade), not the POOM. The spanfilade maps content I-addresses to link ISAs — it is constructed by `insertendsetsinspanf()` at link-creation time, recording the I-address ranges of each endpoint in the SPANRANGE dimension [INT-SPORGL-LINK-INDEX, SS-SPANF-OPERATIONS].

When `findcbcinarea2d()` traverses this 2D enfilade and calls `incontextlistnd()` to accumulate discovered contexts, the sort key is `totaloffset.dsas[index]` — the left boundary in the **queried dimension** [SS-CONTEXT-LIST, INV-RETRIEVAL-V-SORTED]. For a SPANRANGE-restricted spanfilade search, that dimension contains **content I-addresses**, not V-positions.

### Consequence: Permanent I-Address

The sort key resolves to the **permanent I-address** of the indexed content. This is stable under both cases the question raises:

- **Under rearrangement (K.μ~):** Rearrangement modifies only `cdsp.dsas[V]` in POOM crums [ST-REARRANGE, Finding 0056: `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], ...)`]. It never touches the spanfilade. The I-addresses stored in the SPANRANGE of the spanfilade are immutable [INV-IADDR-IMMUTABILITY], so the sort key is unaffected.

- **Under orphaning/deletion (K.μ⁻):** DELETE removes V→I mappings from the POOM but never touches the spanfilade [INV-SPANF-WRITE-ONLY, ST-DELETE, Finding 0057: `dodeletevspan` has no call to any spanf function]. The SPANRANGE I-address entry persists unconditionally. A link whose content has been entirely deleted from all POOMs still sits at its original sorted position in the spanfilade traversal with the same I-address key [EC-GHOST-LINK].

### Contrast With POOM Traversal

The statement in [INV-RETRIEVAL-V-SORTED] that `ispan2vspanset` returns a V-sorted sequence applies specifically to **POOM queries**, where the queried dimension is `V` and `totaloffset.dsas[V]` is the current V-address. For POOM traversal, the sort key *is* the current V-position — which moves under INSERT and vanishes under DELETE. This is a different code path from the spanfilade search.

### V-Position Resolution Happens After the Sort

The current V-position of matched content is not available during the spanfilade traversal at all. It is computed only in the post-processing step: `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()` consults the relevant document's POOM to convert the sorted I-addresses back into V-spans [SS-FOLLOWLINK, INV-ITOV-FILTERING]. This is the step that silently drops I-addresses with no current POOM mapping, producing empty endsets for orphaned links — **after** the sort has already been performed on permanent I-addresses.

### Summary

The insertion-sort in `incontextlistnd()` during link-search traversal sorts by the **content I-address** in the SPANRANGE dimension of the spanfilade. This sort key is the permanent identity of the indexed link endpoint content. It is immutable under rearrangement (K.μ~ shifts V-positions, not I-addresses), and it survives link orphaning (K.μ⁻ removes POOM mappings but not spanfilade entries, per [INV-SPANF-WRITE-ONLY]).

---

## Code Exploration

I now have the complete answer. Here is the full analysis with code citations.

---

## The Sort Key Is the Permanent I-Address (SPANRANGE), Not the V-Position

### The Insertion-Sort Is in `incontextlistnd`

The sort does not happen in `onlinklist`. It happens one level deeper, in the enfilade traversal itself, in `context.c:75`:

```c
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
```

This is a true insertion-sort: it walks the existing context list and splices `c` in order relative to `grasp.dsas[index]`. The `index` parameter is the dimension being sorted on.

### What `index` Is Passed

The call site is `retrie.c:263`:

```c
incontextlistnd (headptr, context, index1);
```

inside `findcbcinarea2d`, which is called from `retrieveinarea` → `retrieverestricted`. The value of `index1` is whatever was passed to `retrieverestricted` as its third argument.

In link-search, `retrieverestricted` is called from `sporglset2linksetinrange` at `sporgl.c:259`:

```c
context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
```

So `index1 = SPANRANGE`.

### What SPANRANGE Means

From `wisp.h:15-16`:

```c
/* wid and dsp indexes for sp */
#define ORGLRANGE 0
#define SPANRANGE 1
```

The spanfilade (`sp`-type enfilade) has two dimensions:

| Constant | Value | Contains |
|----------|-------|----------|
| `ORGLRANGE` | 0 | The link's ISA, prefixed with the endpoint type (`LINKFROMSPAN`=1, `LINKTOSPAN`=2, `LINKTHREESPAN`=3) via `prefixtumbler` |
| `SPANRANGE` | 1 | The **I-address** of the content the link endpoint covers |

The insertion path in `insertspanf` (`spanf1.c:22-51`) confirms what each dimension stores at write time:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  /* link ISA with type prefix */
...
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);            /* content I-address */
movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
```

`lstream` comes from `ispanset->stream` (for `ISPANID` items) or `sporglset->sporglorigin` (for `SPORGLID` items) — both of which are I-coordinates, not V-coordinates.

### The Sort Key Therefore Resolves to the I-Address

The insertion-sort in `incontextlistnd` sorts the context list by `grasp.dsas[SPANRANGE]` — the permanent permascroll I-address of the content. The `whereoncontext` function at `context.c:124` does the comparison:

```c
case SPAN:
case POOM:
    movetumbler (&ptr->totaloffset.dsas[index], &left);
    tumbleradd (&left, &ptr->contextwid.dsas[index], &right);
    break;
```

with `index = SPANRANGE`. This extracts and compares the I-address coordinate.

### The Link ISA Is Extracted Afterwards, Without Re-sorting

Once `retrieverestricted` returns the context list (sorted by SPANRANGE/I-address), `sporglset2linksetinrange` (`sporgl.c:263-265`) extracts the link identity from the other dimension:

```c
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
    onlinklist (taskptr, linksetptr, &linksa);
}
```

`beheadtumbler` strips the `spantype` prefix from `ORGLRANGE` to yield `linksa` — the link's own ISA. `onlinklist` (`spanf2.c:26-44`) is then a plain append-to-tail with duplicate detection and **no sorting of its own**:

```c
for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
    if (tumblereq (&temp->address, linkisaptr))
        return(0);  /* duplicate: skip */
}
temp->next = linkset;  /* append */
```

The link list's order is inherited directly from the insertion-sorted context list.

### Why Not V-Position

The spanfilade is a `SPAN`-type enfilade, not a `POOM`-type. It has no V-dimension; there is no way to store or compare V-positions in it. V↔I translation only occurs in the POOM enfilade (the granfilade, accessed via `vspanset2ispanset` in `orglinks.c`). By the time `sporglset2linkset` is called, the query specset has already been converted to I-addresses via `specset2sporglset` (`sporgl.c:14-33`), which calls `vspanset2sporglset` → `vspanset2ispanset`. The spanfilade traversal sees only I-addresses from that point forward.

### Consequences

- **K.μ~ (rearrangement)**: V-positions of existing content change, but I-addresses do not. The spanfilade index is unaffected. The sort order of link-search results is stable across rearrangements.
- **K.μ⁻ (deletion)**: The V-position of deleted content disappears, but the I-address survives in the spanfilade. A link whose endpoint covered now-deleted content will still appear in search results, sorted by the original I-address of that content. The sort key does not "disappear" — it remains frozen at the permascroll address.

**The sort key is the matched content's permanent I-address (SPANRANGE = 1 in `wisp.h:16`), immutable and independent of any document's current V-layout.**
