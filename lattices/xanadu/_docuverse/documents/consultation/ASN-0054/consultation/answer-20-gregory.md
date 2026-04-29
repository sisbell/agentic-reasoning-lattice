## Question 20 [gregory]

> When a document contains both text entries (subspace 1.x) and link entries (subspace 0.2.x) in the same POOM tree, are these stored as interleaved siblings in shared loafs sorted by V-displacement, or does the tree naturally partition them into separate subtrees due to the tumbler ordering of `0.2.x < 1.x`?

## KB Synthesis

The KB does not describe explicit partitioning logic, but the answer emerges from the tumbler total order combined with how the POOM B-tree is built and traversed.

## Natural partitioning via tumbler ordering

Internally, link entries occupy V-positions `2.1`, `2.2`, ... and text entries occupy V-positions `1.1`, `1.2`, .... Since `1.x < 2.x` under the tumbler total order [INV-TUMBLER-TOTAL-ORDER], text entries consistently have smaller displacements than link entries. The POOM 2D enfilade sorts children by displacement, so text and links occupy different regions of the V-space key range. As the tree grows and splits, text entries tend toward left subtrees and link entries toward right subtrees — not by design, but as an emergent consequence of ordering.

The POOM split policy reinforces this: `splitcrumpm` peels off the child with the largest SPANRANGE displacement [ST-SPLIT-2D], which for a mixed document would be a link entry (largest V-position). Over time this pushes links further right.

## Rebalancing can theoretically mix them in a node

The `recombinend` diagonal sort uses `cdsp.dsas[0] + cdsp.dsas[1]` (V + I displacement sum) [ST-REBALANCE-2D]. This means two upper nodes — one covering text-range children, one covering link-range children — could be merged if their diagonal sums happen to be close. The B-tree does not prevent a parent node from holding pointers to both text-range and link-range child subtrees. So while complete subtree isolation is likely in practice (given the systematic gap between 1.x and 2.x), it is not enforced.

## The two-blade knife requires range-efficient traversal

The strongest structural evidence is [FC-SUBSPACE] / [SS-TWO-BLADE-KNIFE]: INSERT at `1.x` constructs a knife with `blade[1] = 2.1`, and `insertcutsectionnd` classifies link entries at `2.x` as case 2 (no shift) because they fall at or beyond `blade[1]`. This only works efficiently if the B-tree can locate entries by V-range without scanning the whole tree — which requires that the displacement ordering puts text entries and link entries in reliably different subtrees, at least above the loaf level.

## Summary

Text (1.x) and link (2.x) entries share the same POOM tree and the same loaf allocation pool [SS-UNIFIED-STORAGE]. They are NOT in structurally separate enfilades. However, tumbler ordering guarantees they occupy different V-ranges, which causes the B-tree to naturally partition them into separate subtrees as it grows. A single upper node (loaf) could theoretically contain pointers to both ranges — the KB has no finding that rules this out — but complete V-range interleaving within a single bottom crum (loaf) is impossible because each bottom crum covers a contiguous V-address interval [SS-POOM-BOTTOM-CRUM], and no single interval spans both `1.x` and `2.x`.

---

## Code Exploration

Now I have sufficient source-level evidence to answer the question definitively. Let me compile the full answer from the actual code.

---

## Storage of Text vs. Link Entries in the Same POOM Tree

### Short Answer

They live in the **same single POOM enfilade**, sorted by V-coordinate. There is no structural enforcement of subspace separation. Tumbler ordering causes the partition to emerge naturally — text entries always sort before link reference entries — but whether they occupy **shared loafs or separate subtrees** depends on document size: small documents share leaf loafs; larger documents partition into separate subtrees after splits.

---

### The V-Address Assignment Scheme

**Text entries** — `doinsert` → `appendpm` → `findvsatoappend` [`orglinks.c:29-48`]:

```c
int findvsatoappend(typecorecrum *ptr, tumbler *vsaptr)
{
  tumbler linkspacevstart;
    tumblerclear (&linkspacevstart);
    tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart); // linkspacevstart = 2
    prologuend (ptr, &offset, &grasp, &reach);
    if (
       iszerolock (...)
    || (tumblercmp (&grasp.dsas[V], &linkspacevstart) != LESS)) {
        tumblerincrement (vsaptr, 0, 1, vsaptr);  // vsaptr = 1
        tumblerincrement (vsaptr, 1, 1, vsaptr);  // vsaptr = 1.1  ← first text position
    } else if (tumblercmp (&reach.dsas[V], &linkspacevstart) == LESS) {
        movetumbler (&reach.dsas[V], vsaptr);     // no links: next = end of text
    } else {
        findnextaddressinvspace (ptr, &grasp, &linkspacevstart, vsaptr);
        // links present: find last text address before boundary at 2
    }
```

The first text append in an empty document goes to V = **1.1** (`{exp=0, mantissa=[1,1]}`). Each subsequent append extends from there (width is computed with `shift = tumblerlength(vsaptr) - 1` in `insertpm` [`orglinks.c:115`], encoding the character count at the second story). Text entries therefore occupy V ∈ **[1.1, 2)**.

**Link reference entries** — `docreatelink` → `findnextlinkvsa` [`do2.c:151-167`]:

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);  // firstlink = 2
    tumblerincrement (&firstlink, 1, 1, &firstlink);  // firstlink = 2.1
    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);  // first link → V = 2.1
    else
        movetumbler (&vspanreach, vsaptr); // subsequent links → append after previous
```

The first link reference placed in the document's POOM goes at V = **2.1** (`{exp=0, mantissa=[2,1]}`). Subsequent link references are placed at the current reach (end of the existing V-span), pushing each successive link reference further up into the **[2.1, ...)** range.

**The boundary is hard**: `findvsatoappend` sets `linkspacevstart = 2` and uses it as the cutoff. All V-addresses of text crums are strictly less than `2`; all V-addresses of link crums are `≥ 2.1`. The tumbler comparison `tumblercmp(&x, &y)` in `tumble.c:72-85` operates digit-by-digit, left-to-right, so `1.anything < 2 < 2.1`.

Note: the link's own POOM tree (its orgl) uses `setlinkvsas` [`do2.c:169-183`] to place **from-endpoint** data at V = 1.1 and **to-endpoint** data at V = 2.1 within the link object. This is a separate tree from the document's POOM.

---

### How the POOM Enfilade Actually Sorts Them

Both text crums and link-reference crums land in the **same POOM tree** via `insertnd` → `insertmorend` → `findsontoinsertundernd` [`insertnd.c:277-299`]:

```c
typecorecrum *findsontoinsertundernd(typecuc *father, typedsp *grasp,
                                     typewid *origin, typewid *width, INT index)
{
    tumbleradd (&origin->dsas[index], &width->dsas[index], &spanend);
    ptr = nearestonleft = findleftson (father);
    for (; ptr; ptr = findrightbro(ptr)) {
        tumbleradd(&grasp->dsas[index],&ptr->cdsp.dsas[index],&sonstart);
        if (
          tumblercmp (&sonstart, &origin->dsas[index]) != GREATER
        && tumblercmp (&ptr->cdsp.dsas[index], &nearestonleft->cdsp.dsas[index]) != LESS) {
            nearestonleft = ptr;
        }
        if (
          whereoncrum(ptr,grasp,&origin->dsas[index],index)>=ONMYLEFTBORDER
        && whereoncrum (ptr, grasp, &spanend, index) <= ONMYRIGHTBORDER)
            return (ptr);
    }
    return (nearestonleft);
}
```

When called with `index = V` (the V-dimension), this routes each insertion to the child whose V-interval contains the target address. There is **no check for subspace type** — it is purely a tumbler comparison. A text crum at 1.5 and a link crum at 2.1 are simply two points on the same number line, and the tree routes each to the correct position.

The leaf-level insertion, `insertcbcnd` [`insertnd.c:242-275`], first checks if the new crum is an extension of an existing one:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, ...);  // extend in place
        ...
    }
}
new = createcrum (0, (INT)father->cenftype);
adopt (new, SON, (typecorecrum*)father);              // or create sibling
```

If no extension is possible (different I-stream or non-contiguous), a new sibling crum is created. Text and link crums with different `homedoc` values will never satisfy `isanextensionnd` (line 305: `!tumblereq(&infoptr->homedoc, &ptr->c2dinfo.homedoc)` returns FALSE), so they always become distinct crums.

---

### Loaf Occupancy: Shared vs. Separate Subtrees

A loaf holds up to `MAX2DBCINLOAF` bottom crums (leaf level) or `MAXUCINLOAF` internal crums (checked via `toomanysons` in `genf.c:239-245`). There is no subspace filtering on loaf membership.

**Small document** (e.g., one text crum + one link crum): Both crums sit in the same leaf loaf under the root. They are siblings ordered by V-address, with the text crum on the left and the link crum on the right — interleaved in the same loaf.

**Larger document**: When `splitcrumupwards` fires (triggered from `insertcbcnd` line 272), the loaf splits at its midpoint. Because text crums cluster at V ∈ [1.1, 2) and link crums cluster at V ∈ [2.1, ...) with a genuine gap between them, any split that separates the two groups will produce:
- Left child: contains only text crums (V < 2)
- Right child: contains only link crums (V ≥ 2.1)

This partition then propagates upward through `setwispupwards` and `recombine` [`insertnd.c:76`, `genf.c` recombine]. Once split, subsequent insertions will route text to the left subtree and links to the right subtree — they never need to share a loaf again.

---

### The `istextcrum` / `islinkcrum` Classification

After retrieval, `maxtextwid` in `orglinks.c:224-245` needs to distinguish text from link crums within a POOM traversal. It uses these heuristics [`orglinks.c:246-261`]:

```c
bool istextcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[1] == 0  && is1story(&crumptr->cwid.dsas[V])){ 
        return TRUE;
    }
    return FALSE;
}

bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0){
        return TRUE;
    }
    return FALSE;
}
```

`istextcrum` checks that the crum's V-displacement has zero second digit and 1-story width — consistent with a single contiguous text run whose width encodes character count in `mantissa[0]`.

`islinkcrum` checks that the crum's V-displacement starts with `1` and has a non-zero second digit (`1.n` for n≠0). This identifies crums within the V-range `1.1–1.∞`, which in the link object's own POOM corresponds to from-endpoint data. Note this is operating on the relative **displacement** (`cdsp`), not the absolute V-address.

These are **detection heuristics**, not enforcement. The POOM tree itself imposes no type constraint.

---

### The `filter_vspanset_to_text_subspace` Guard

`do1.c:386-411` adds an explicit filter when computing version relations:

```c
typevspanset filter_vspanset_to_text_subspace(typetask *taskptr, typevspanset vspanset)
{
    tumblerclear(&text_subspace_start);
    tumblerincrement(&text_subspace_start, 0, 1, &text_subspace_start); // = 1
    for (; vspanset; vspanset = vspanset->next) {
        if (tumblercmp(&vspanset->stream, &text_subspace_start) >= EQUAL) {
            // keep: span is in text subspace (V >= 1)
        }
        // skip: link subspace (V < 1) — not applicable to doc POOM,
        //        but relevant for the link POOM's from-endpoint (V = 0.something)
    }
```

The boundary here is V ≥ 1 (not 2), which confirms that the overall V-space has:
- `V < 1`: some lower subspace (not directly used by either text or doc-level links)
- `V ∈ [1, 2)`: text subspace in the document POOM
- `V ≥ 2.1`: link-reference subspace in the document POOM

---

### Conclusion

**The POOM tree uses a single shared enfilade for both text and link entries.** There is no structural separation — no separate trees, no subspace-aware routing logic in the insertion path.

The **effective partition** arises from the V-address assignment scheme:
- `findvsatoappend` places text at V ∈ [1.1, 2)
- `findnextlinkvsa` places link references at V ≥ 2.1

Because tumbler ordering (`tumblercmp`) is total and consistent, text entries always sort strictly below link entries in the enfilade. In a **small document**, they coexist as siblings in the same leaf loaf — they are genuinely interleaved in a shared loaf, separated only by their V-address ordering. As the document grows and loafs split, they partition into **separate left and right subtrees**, but this is a side-effect of the B-tree mechanics, not an explicit architectural decision. The tree does not "know about" the subspace boundary — it only knows tumbler ordering.
