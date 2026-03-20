## Question 13 [gregory]

> Can a single POOM bottom crum map a V-span to a non-contiguous I-span, or is there a strict invariant that each bottom crum represents a contiguous-to-contiguous mapping where both V and I ranges are unbroken?

## KB Synthesis

Each POOM bottom crum encodes a **strict contiguous-to-contiguous linear mapping**. There is no mechanism for a single crum to represent a non-contiguous I-span.

## Structural evidence

[SS-POOM-BOTTOM-CRUM] (Finding 0076) shows the bottom crum structure directly:

```
BottomCrum = {
  origin: { dsas[I]: Tumbler, dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler, dsas[V]: Tumbler }
}
```

A single `origin` and `width` per dimension. There is no field for a set of I-ranges or a scatter list — the representation structurally cannot express non-contiguity within a single crum.

[INV-WIDTH-VALUE-EQUIVALENCE] (Finding 0076) establishes that `value(crum.width.dsas[V]) == value(crum.width.dsas[I])` — the V-width and I-width encode the same integer. This enforces a 1:1 linear mapping: a V-span of width *w* maps to exactly *w* consecutive I-addresses.

## Extension invariant confirms both dimensions must be contiguous

[ST-VCOPY] / [ST-INSERT] (Finding 0046) describe `isanextensionnd()` at `insertnd.c:293-301`: a new mapping is merged into an existing crum only when (1) same `homedoc` **and** (2) the new content starts exactly where the existing crum ends — contiguous in **both** V and I simultaneously. If either dimension is non-contiguous, a new separate crum is created instead.

This means two adjacent V-positions mapping to I-addresses from different source documents (transcluded content) always produce **two crums**, not one crum with a non-contiguous I-range.

## What happens with transcluded content from multiple sources

[SS-SPORGL] (Finding 0013) and [ST-LINK-CREATE] (Finding 0037) document exactly this case. When a V-span covers content transcluded from two documents (e.g., "AA" from A and "BB" from B), `vspanset2ispanset` → `permute` → `span2spanset` walks the POOM and returns **one I-span per contiguous I-address region**. The POOM itself stores two separate crums — one per contiguous I-block — not a single crum spanning both.

[SS-POOM-MULTIMAP] (Finding 0039) confirms the multimap semantics: multiple V-positions can reference the same I-address, but this is achieved through **multiple crums** each with their own linear (V, I) pair, never through a single crum with a non-contiguous I-range.

## Summary

The invariant is strict: **every POOM bottom crum is a length-preserving 1:1 linear mapping from a contiguous V-range `[v, v+w)` to a contiguous I-range `[i, i+w)`**. Non-contiguous I-spans in a V-region are always represented as multiple crums, never as a single crum. The data structure, the extension check, and the width-equivalence invariant all enforce this together.

---

## Code Exploration

Now I have everything I need for a complete answer.

---

## Answer: POOM Bottom Crum Contiguity Invariant

**The invariant is strict: each POOM bottom crum encodes exactly one contiguous I-span and one contiguous V-span, of equal integer width, in a unit-ratio bijection. Non-contiguous mappings are represented at the tree level by multiple bottom crums, never within a single one.**

Here is the code-by-code proof.

---

### 1. Data Structure

The fundamental types are defined in `backend/wisp.h` and `backend/enf.h`.

`backend/wisp.h:50-54`:
```c
struct structwid {
    tumbler dsas[MAXLOXIZE];
};
typedef struct structwid typewid;
typedef typewid typedsp;
```

`backend/wisp.h:19-21` (the index constants):
```c
#define I  0
#define V  1
```

`backend/wisp.h:25-27` (sizes):
```c
#define DSPSIZEPM 2
#define WIDSIZEPM 2
```

`backend/enf.h:109-131` (the POOM bottom crum type):
```c
struct struct2dcbc {
    ...
    typewid cwid;   /* width in both I and V dimensions */
    typedsp cdsp;   /* displacement (origin) in both I and V dimensions */
    type2dbottomcruminfo c2dinfo;  /* homedoc: the source document ISA */
};
typedef struct struct2dcbc type2dcbc;
```

And `type2dbottomcruminfo` (`backend/wisp.h:107-109`):
```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

So each bottom crum stores: `cdsp.dsas[I]` (I-origin), `cwid.dsas[I]` (I-width), `cdsp.dsas[V]` (V-origin), `cwid.dsas[V]` (V-width), and `c2dinfo.homedoc` (source document). That is four tumblers — two intervals, one per dimension. There is no mechanism to store more than one contiguous interval per dimension in a single crum.

---

### 2. Creation: Equal-Width Bijection Is Enforced at Insertion Time

`insertpm` in `backend/orglinks.c:75-134` is the entry point for inserting content into the POOM. For each item in the sporgl set, it builds `crumorigin` and `crumwidth` then calls `insertnd`:

```c
// orglinks.c:105-130
movetumbler (&lstream, &crumorigin.dsas[I]);      // I-origin = lstream
movetumbler (&lwidth, &crumwidth.dsas[I]);         // I-width = lwidth
movetumbler (vsaptr, &crumorigin.dsas[V]);         // V-origin = vsaptr
shift = tumblerlength (vsaptr) - 1;
inc = tumblerintdiff (&lwidth, &zero);             // integer count of I-width
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);  // V-width = same count
...
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  // advance vsaptr for next iteration
```

Key observations:
- `inc = tumblerintdiff(&lwidth, &zero)` extracts the integer count of the I-span.
- `tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V])` constructs a V-width with the **same integer count**, just expressed at the tumbler depth of `vsaptr`.
- Both `crumorigin.dsas[I]` and `crumorigin.dsas[V]` are single tumblers (single points), so each is a single contiguous interval start.

The V and I widths are always equal in integer count. The mapping is a unit-ratio bijection: one I-position per V-position.

---

### 3. Bottom Crum Allocation: One Origin and Width Per Crum

`insertcbcnd` in `backend/insertnd.c:242-275` is where the actual bottom crum is created or extended:

```c
// insertnd.c:260-268
new = createcrum (0, (INT)father->cenftype);
...
adopt (new, SON, (typecorecrum*)father);
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);   // sets both cdsp[I] and cdsp[V]
...
movewisp (width, &new->cwid);                                  // copies both cwid[I] and cwid[V]
move2dinfo (infoptr, &((type2dcbc *)new)->c2dinfo);
```

`dspsub` subtracts the parent's grasp from `origin` across all dimensions of the POOM (`dspsize(POOM) = 2`), giving the crum's displacement relative to its parent in both I and V simultaneously. `movewisp` copies the full 2-dimensional width. One call → one crum → one I-interval and one V-interval. There is no way to construct a crum with more than one interval per dimension.

The extension path (merging into an adjacent existing crum) uses `isanextensionnd` at `insertnd.c:301-309`:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

`lockeq` with `dspsize(POOM) = 2` checks that **both** `reach.dsas[I] == origin->dsas[I]` AND `reach.dsas[V] == origin->dsas[V]` simultaneously. That is, both dimensions must be exactly adjacent. If they are, the width is extended at `insertnd.c:251`:

```c
dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
```

Again, `dspsize(POOM) = 2` — both dimensions are extended together. An existing crum can only be extended by a region that is simultaneously adjacent in both I and V. This preserves the contiguous-to-contiguous invariant.

---

### 4. Retrieval: Single-Dimension Interval Test Confirms One Interval Per Dimension

`whereoncrum` in `backend/retrie.c:345-398` is the workhorse for navigating the tree:

```c
// retrie.c:355-373
case SPAN:
case POOM:
    tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
    ...
    tumbleradd (&left, &ptr->cwid.dsas[index], &right);
    cmp = tumblercmp(address, &right);
    if(cmp == LESS){
        return(THRUME);
    }else if (cmp == EQUAL){
        return (ONMYRIGHTBORDER);
    }else{
        return(TOMYRIGHT);
    }
```

For a given `index` (either `I` or `V`), the crum occupies the interval `[left, right)` where `left = offset[index] + cdsp[index]` and `right = left + cwid[index]`. This is a single closed interval. The function returns one of five positions (TOMYLEFT, ONMYLEFTBORDER, THRUME, ONMYRIGHTBORDER, TOMYRIGHT). There is no branching for "non-contiguous sub-ranges" because the crum has exactly one interval per dimension.

The 2D area query `findcbcinarea2d` (`retrie.c:229-268`) and `crumqualifies2d` (`retrie.c:270-305`) test the two dimensions independently by calling `whereoncrum` twice with different `index` values. This is checking that the crum's rectangular region intersects a query rectangle — not that any single crum has a non-contiguous span.

---

### 5. Split Operations Preserve the Invariant

`splitcrumpm` in `backend/split.c:117-128`:

```c
int splitcrumpm(typecuc *father)
{
    typecorecrum *ptr, *correctone;
    for(correctone=ptr=findleftson(father);ptr;ptr = findrightbro(ptr)) {
        if (tumblercmp (&ptr->cdsp.dsas[SPANRANGE], &correctone->cdsp.dsas[SPANRANGE]) == GREATER)
            correctone = ptr;
    }
    peelcrumoffnd(correctone);
}
```

When a POOM upper crum has too many sons, the split peels one son into its own new parent via `peelcrumoffnd`. This is purely a tree restructuring — no bottom crum's `cdsp` or `cwid` is changed, so the contiguous-to-contiguous property of each bottom crum is preserved across splits.

`peelcrumoffnd` at `split.c:130-169` does:
```c
movewisp(&father->cdsp, &new->cdsp);   // new parent inherits father's cdsp
adopt(ptr, LEFTMOSTSON, new);           // peeled crum becomes new parent's only son
```

The peeled bottom crum's own `cdsp` and `cwid` are never touched.

---

### 6. The `homedoc` Field and Multi-Document POOM

The `c2dinfo.homedoc` field in each bottom crum (`wisp.h:107-109`) is the ISA (address) of the source document for that crum's I-span. `crumqualifies2d` checks at `retrie.c:274-279`:

```c
if ((crumptr->height == 0) && infoptr && !tumblereq (&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc))){
    return (FALSE);
}
```

This means that in a multi-document context, `homedoc` disambiguates which document's I-space the crum belongs to. But even then, each crum still has one contiguous I-span within one document's I-space, and one contiguous V-span.

---

### Summary

| Property | Enforced? | Where |
|----------|-----------|-------|
| Each bottom crum has exactly one I-interval | Yes, structurally | `enf.h:109-131` — one `cdsp.dsas[I]` + `cwid.dsas[I]` |
| Each bottom crum has exactly one V-interval | Yes, structurally | `enf.h:109-131` — one `cdsp.dsas[V]` + `cwid.dsas[V]` |
| I-width == V-width (integer count) | Yes, at insertion | `orglinks.c:115-117` — `inc` used for both |
| Extension requires simultaneous adjacency in both dimensions | Yes | `insertnd.c:308` — `lockeq` with `dspsize(POOM)=2` |
| Splits do not fragment bottom crums | Yes | `split.c:130-169` — no `cdsp`/`cwid` mutation |

**A single POOM bottom crum cannot map a V-span to a non-contiguous I-span.** The data structure physically stores only one origin and one width per dimension. The enforcement is:

1. **Structural** — only two tumblers per dimension in `cwid`/`cdsp`
2. **At insertion** — `insertpm` derives both widths from the same integer count; `insertcbcnd` stores one origin and one width from a single call
3. **At extension** — `isanextensionnd` requires simultaneous adjacency in all dimensions via `lockeq(reach.dsas, origin->dsas, dspsize(POOM)=2)`

Non-contiguous mappings at the document level are represented by **multiple bottom crums** across the tree, each individually encoding a simple, contiguous, unit-ratio piece. The enfilade tree structure is what allows an arbitrarily complex permutation to be encoded efficiently — not any internal complexity within a single leaf.
