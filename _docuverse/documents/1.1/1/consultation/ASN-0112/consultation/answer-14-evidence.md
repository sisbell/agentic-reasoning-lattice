## Question 14 [evidence]

> Is the width tumbler returned by RETRIEVEDOCVSPAN computed as root offset plus root displacement, and does it reflect logical V-extent independent of the physical tree shape per enfilade confluence?

## KB Synthesis

## Width Computation in RETRIEVEDOCVSPAN

**Short answer:** The width is read directly from `root.cwid.dsas[V]` — not computed as offset + displacement. The start position is `root.cdsp.dsas[V]`. For a 2D enfilade root at offset 0, `grasp(root) = 0 + root.cdsp = root.cdsp`, making the returned vspan `[root.cdsp, root.cdsp + root.cwid)`. This IS invariant under tree restructuring, but it is not a meaningful content width for mixed-content documents.

---

### How the Width is Computed

From [SS-VSPAN-VS-VSPANSET] (Finding 0035), RETRIEVEDOCVSPAN (opcode 14) delegates to `retrievevspanpm()` at `orglinks.c:165-172`, which performs a raw read of the root crum's V-dimension displacement and width — no subspace processing, no recursive traversal.

From [SS-ENFILADE-TREE] (Finding 0066), the root node of a 2D enfilade (POOM) has `cdsp` set to the minimum V-address across all content, maintained by `setwispnd`. The reach formula is `grasp + cwid`. Since the root's cumulative offset is 0, `grasp(root) = 0 + root.cdsp.dsas[V]`. So:

- **Start** = `root.cdsp.dsas[V]` (absolute minimum V-address in the tree)
- **Width** = `root.cwid.dsas[V]` (span from minimum to maximum V-address)
- **Reach** = start + width = maximum V-address

The width is the maximum-minus-minimum V-address, not recomputed on demand — it is maintained as a running summary updated by `setwispnd` after every modification.

---

### Independence from Tree Shape

Yes, per [INV-ENFILADE-CONFLUENCE] (Finding 0041), the widdative summary fields (`cwid`) maintain the same logical intervals regardless of insertion order or tree structure. Different sibling orderings, split points, or rebalancing paths all produce the same root-level `cwid`. This is the basis of [INV-ENFILADE-QUERY-INDEPENDENCE].

---

### The Critical Caveat: Misleading Width for Mixed Documents

Despite being tree-shape-independent, the returned width is structurally misleading for documents containing both text (internal V `1.x`) and links (internal V `2.x`). The root `cwid.dsas[V]` spans the gap between subspaces, yielding a value like `1.2` for "10 chars of text plus 1 link" — as documented in [EC-VSPAN-MISLEADING-SIZE] (Bug 0011). This is a bounding box, not a content extent.

The semantically correct operation is RETRIEVEDOCVSPANSET (opcode 1), which uses `retrievevspansetpm()` (`orglinks.c:173-221`) and decomposes content into per-subspace spans using the `is1story` check — see [SS-VSPAN-VS-VSPANSET] (Finding 0035).

CREATENEWVERSION avoids this problem by using the separate `retrievedocumentpartofvspanpm()` (`orglinks.c:155-162`), which reads only the text-subspace displacement and width, as documented in [ST-VERSION-CREATE] (Finding 0043).

---

## Code Exploration

---

## Width Tumbler in RETRIEVEDOCVSPAN: Code Analysis

### The Call Chain

**`fns.c:303-312`** — The FEBE handler:

```c
void retrievedocvspan(typetask *taskptr)
{
  typeisa docisa;
  typevspan vspan;
  bool getretrievedocvspan(), doretrievedocvspan();

    if (   getretrievedocvspan (taskptr, &docisa)
        && doretrievedocvspan (taskptr, &docisa, &vspan))
            putretrievedocvspan (taskptr, &vspan);
}
```

**`do1.c:312-320`** — The do function:

```c
bool doretrievedocvspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), retrievevspanpm();

    return
       findorgl (taskptr, granf, docisaptr, &docorgl, READBERT)
    && retrievevspanpm (taskptr, docorgl, vspanptr);
}
```

**`orglinks.c:165-172`** — Where the two tumblers are populated:

```c
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

Both values are **direct reads** from the root crum's stored fields — no arithmetic is performed at query time.

---

### What `cdsp` and `cwid` Mean

From `wisp.h:19-27`:

```c
#define I  0
#define V  1
#define DSPSIZEPM 2
#define WIDSIZEPM 2
```

POOM crums (document tree) carry a 2-element displacement+width pair, one slot per dimension. The V-dimension (index 1) is the version axis.

From `enf.h:47-48` and `enf.h:71-72`, every crum (both upper `typecuc` and bottom) stores:

```c
typewid cwid;   /* width — the extent in each dimension */
typedsp cdsp;   /* displacement — offset from parent's origin */
```

So:
- **`stream`** = `root->cdsp.dsas[V]` — the V-axis displacement of the document's root crum relative to the absolute origin
- **`width`** = `root->cwid.dsas[V]` — the V-axis extent stored in the root crum

Together they define the interval `[stream, stream + width]` in V-space.

---

### Is Width "Root Offset + Root Displacement"?

No — not in the sense of computed at retrieval time. The width is read directly from `cwid.dsas[V]`. However, the traversal semantics in `retrie.c:334-339` (`prologuend`) clarify the coordinate model:

```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);   /* grasp = offset + cdsp */
    if (reach)
        dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype); /* reach = grasp + cwid  */
}
```

During enfilade traversal, `reach = accumulated_offset + cdsp + cwid`. The root's accumulated offset is the zero tumbler, so the root's reach is `cdsp + cwid` — the absolute end address. But RETRIEVEDOCVSPAN does **not** expose this sum; it returns the two components separately as `stream` and `width`.

---

### Is Width a Logical V-Extent Independent of Tree Shape?

**Yes.** The `cwid` field is the enfilade's structural invariant, maintained by `setwispnd()` in `wisp.c:171-228`:

```c
bool setwispnd(typecuc *father)
{
    /* find new upper-left corner */
    movewisp (&ptr->cdsp, &mindsp);
    for (ptr = getrightbro(ptr); ptr; ptr = getrightbro (ptr))
        lockmin (&mindsp, &ptr->cdsp, &mindsp, dspsize(ptr->cenftype));
    /* normalize child displacements down by mindsp */
    ...
    /* find new cwid = max over children of (child->cdsp + child->cwid) */
    clear (&newwid, sizeof(newwid));
    for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)) {
        if (!lockiszerop)
            dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, (INT)ptr->cenftype);
        lockadd(&ptr->cdsp, &ptr->cwid, &tempwid, widsize(ptr->cenftype));
        lockmax(&newwid, &tempwid, &newwid, widsize(ptr->cenftype));
    }
    movewisp (&newdsp, &father->cdsp);   /* wisp.c:224 */
    movewisp (&newwid, &father->cwid);   /* wisp.c:225 */
```

The algorithm:
1. Finds the minimum `cdsp` across all children (the logical lower-left corner)
2. Normalizes all child displacements by subtracting that minimum
3. Sets `cwid` = max over children of `(child->cdsp + child->cwid)` — the farthest endpoint relative to the new origin

This propagates upward via `setwispupwards()` (`wisp.c:83-111`) after any structural modification. The result is that `root->cwid.dsas[V]` always equals the maximum V-extent of the entire document tree, computed bottom-up, regardless of how many internal nodes exist, where splits occurred, or how the tree was reorganized.

This **is** the widditive (confluence) property of nd-enfilades: the width of an internal node is the widditively-composed maximum-extent of its subtree, not a structural artifact of the physical layout.

---

### Summary

| Field | Source | Semantics |
|-------|--------|-----------|
| `stream` | `root->cdsp.dsas[V]` | V-axis origin of the document in absolute V-space |
| `width` | `root->cwid.dsas[V]` | V-axis logical extent from that origin to the farthest content endpoint |

The **width** is read directly from the pre-maintained `cwid` field — not computed at retrieval time as a sum of offset plus displacement. However, the invariant that `cwid` holds the true logical V-extent (independent of tree shape) is enforced by `setwispnd()`/`setwispupwards()`, which recalculate it bottom-up whenever the tree is modified. This satisfies the enfilade confluence condition: the root crum's width reflects the complete logical span of the document content in V-space regardless of the physical tree structure beneath it.
