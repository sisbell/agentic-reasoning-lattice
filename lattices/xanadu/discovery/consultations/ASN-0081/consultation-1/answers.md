# Revision Consultation — ASN-0081

**Review:** review-1.md
**Date:** 2026-04-09 18:19

## Summary

5 REVISE items analyzed: 4 internal, 1 consulted (0 nelson, 1 gregory)

## Consultation Results

### Issue 2: Missing contiguity precondition for V_S(d)

**Category:** GREGORY
**Reason:** Whether V-positions within a subspace are contiguously allocated (no gaps) depends on how the allocator works in practice. The ASN references "sequential allocation" informally but needs implementation evidence to justify a contiguity axiom.

**Gregory question:** Within a single subspace of a document's V-stream, does the green allocator guarantee that allocated V-positions are contiguous — i.e., if positions at ordinals k and k+2 exist, must ordinal k+1 also be allocated?

**Gregory's Answer:**

## KB Synthesis

No. The allocator does not guarantee V-position contiguity within a subspace. The system permits gaps.

## Why gaps are structurally possible

V-positions for text are **caller-specified**, not auto-allocated by the backend. The frontend provides `vsaptr` to `doinsert`, and the only validation gate is `acceptablevsa()`, which unconditionally returns `TRUE` [PRE-INSERT, Finding 0049]. A frontend that inserts at 1.1, then at 1.100, leaves V-positions 1.2–1.99 unoccupied in the POOM. The backend has no mechanism to reject or fill this gap.

The two-blade knife in INSERT [SS-TWO-BLADE-KNIFE] shifts existing POOM entries within `[insertion_point, next_subspace_boundary)`, but it only shifts — it does not fill gaps, and it operates only on entries that already exist.

## What INV-VSPAN-CONSOLIDATION actually says

[INV-VSPAN-CONSOLIDATION] (Finding 0028) states that 100 sequential single-character inserts produce `span_count: 1`. This describes **storage compaction of already-contiguous insertions** via the `isanextensionnd` extension check [ST-INSERT, Finding 0062]: when each successive insert's I-address origin equals the prior crum's reach, the crum extends in place rather than splitting. This invariant holds because the test inserts sequentially — it does not assert that the system enforces contiguity against non-sequential callers.

## The one auto-allocated case: link positions

The only V-addresses auto-computed by the backend are link positions, via `findnextlinkvsa()` [SS-LINK-SUBSPACE, Finding 0052]. This function initializes the first link at `2.1` and thereafter uses `vspanreach` (the current document end). Links therefore are always appended contiguously at the end of the link subspace — no gaps arise from that path.

## DELETE closes gaps; INSERT can create them

DELETE shifts remaining entries left by the deletion width [ST-DELETE, Finding 0056], collapsing whatever gap the deletion opened. There is no inverse: INSERT can open a gap if the caller targets a position beyond the current document extent, and nothing closes it. The only compaction that occurs is the `isanextensionnd` merge of crum-adjacent content at the *storage level*, which presupposes the logical gap was never there.

## Bottom line

Within a single subspace, contiguity of V-positions depends entirely on the frontend placing inserts at adjacent positions. The backend offers no guarantee and no enforcement. `retrieve_vspanset` would expose any such gap as multiple disjoint spans rather than a single consolidated span [SS-VSPAN-VS-VSPANSET].

---

## Code Exploration

Now I have all the evidence needed. Let me compile the complete answer.

---

## Answer: V-Position Contiguity within a Subspace

**No, the allocator does not universally guarantee contiguous V-position allocation within a subspace.** Whether the guarantee holds depends on which code path allocates the V-positions. Here is the full trace.

---

### What Is a Subspace?

The V-stream uses tumblers for positions. From `findvsatoappend` [orglinks.c:36-37]:

```c
tumblerclear (&linkspacevstart);
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);
```

This sets `linkspacevstart = 2.0` (mantissa[0] = 2). The two subspaces of the document V-stream are:

- **Text subspace**: V-positions in range `[1.1, 2.0)` — normal document content
- **Link subspace**: V-positions `>= 2.0` — link endpoint metadata

`islinkcrum` [orglinks.c:255-261] identifies link crums by `mantissa[0] == 1 && mantissa[1] != 0` (i.e., 1.x for x≠0). `istextcrum` [orglinks.c:246-253] identifies text crums by `mantissa[1] == 0` with a 1-story width. These are structurally distinct.

---

### Path 1: `doappend` — Contiguity Is Guaranteed

`doappend` [do1.c:25-32] → `appendpm` [orglinks.c:17-27] → `findvsatoappend` [orglinks.c:29-49]:

```c
int findvsatoappend(typecorecrum *ptr, tumbler *vsaptr)
{
    tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);  // linkspacevstart = 2.0
    prologuend (ptr, &offset, &grasp, &reach);
    if (iszerolock((tumbler*)&ptr->cwid, widsize(POOM))
    || (tumblercmp (&grasp.dsas[V], &linkspacevstart) != LESS)) {
        tumblerincrement (vsaptr, 0, 1, vsaptr);   // empty doc → start at 1.1
        tumblerincrement (vsaptr, 1, 1, vsaptr);
    } else if (tumblercmp (&reach.dsas[V], &linkspacevstart) == LESS) {
        movetumbler (&reach.dsas[V], vsaptr);       // no links → append at current end
    } else {
        findnextaddressinvspace (ptr, &grasp, &linkspacevstart, vsaptr);
    }
}
```

When the document has mixed text and link content, it calls `findnextaddressinvspace` [orglinks.c:51-72]:

```c
int findnextaddressinvspace(typecorecrum *crumptr, typewid *offsetptr,
                             tumbler *nextvspacestartptr, tumbler *vsaptr)
{
    tumblerclear (&maxt);
    for (; ptr; ptr = findrightbro(ptr)) {
        prologuend (ptr, offsetptr, &grasp, &reach);
        if (whereoncrum(ptr,offsetptr,nextvspacestartptr,V) == THRUME) {
            findnextaddressinvspace (ptr, &grasp, nextvspacestartptr, vsaptr);  // descend
            return(0);
        } else if (tumblercmp(&grasp.dsas[V],nextvspacestartptr) != GREATER) {
            tumblermax (&reach.dsas[V], &maxt, &maxt);  // track max reach of text crums
        }
    }
    movetumbler (&maxt, vsaptr);  // return maximum reach found
}
```

This walks the entire enfilade tree, collects the maximum `reach` of all text crums (those with V < 2.0), and returns it as the new insertion point. Because `reach` is the **end** of the last existing text crum, appending from there creates strictly contiguous allocation: no ordinal is skipped.

So within the text subspace, **`doappend` guarantees that if k and k+2 are both allocated positions, k+1 was also allocated** — because each append starts exactly at the current maximum reach.

---

### Path 2: `doinsert` with Explicit VSA — No Contiguity Guarantee

`doinsert` [do1.c:87-123] accepts an explicit `vsaptr` from the caller:

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset)
    );
    return(ret);
}
```

`docopy` [do1.c:45-65] calls `acceptablevsa` to validate the requested position:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

`acceptablevsa` [do2.c:110-113] is a **stub that unconditionally returns TRUE**. There is no boundary check, no contiguity check, no verification that the requested V-position is adjacent to existing content. A caller can pass any V-position and the backend will accept it, potentially creating a gap.

The comment at `insertpm` [orglinks.c:88-90] corroborates: the only check before inserting is:

```c
if (iszerotumbler (vsaptr)){
    return (FALSE);
}
```

Zero is rejected. Negative is flagged in debug builds only [orglinks.c:93-98]. Any positive non-zero tumbler is accepted and used directly.

---

### Path 3: `dodeletevspan` — No Gaps Created

`dodeletevspan` [do1.c:158-167] → `deletevspanpm` [orglinks.c:145-152] → `deletend` [edit.c:31-76]:

```c
for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
    switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
      case 0: break;                                       // before range: unchanged
      case 1:
        disown ((typecorecrum*)ptr);
        subtreefree ((typecorecrum*)ptr);                  // in range: deleted
        break;
      case 2:
        tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);  // after range: shifted back
        break;
    }
}
```

Crums entirely within the deletion range are removed. Crums **after** the range are shifted backward by `width` via `tumblersub`. The deletion **compacts** V-space — it does not create gaps. If k+1 was allocated and then deleted, k+2 becomes the new k+1 after the shift.

---

### Path 4: `docreatenewversion` — Gap Risk

`docreatenewversion` [do1.c:260-298] copies the entire prior version into a newly allocated document using `docopyinternal`, which also calls `acceptablevsa` [do1.c:76]. Same stub — no contiguity enforcement.

---

### `tumblerincrement` Does Not Enforce Subspace Boundaries

`tumblerincrement` [tumble.c:599-623] performs position arithmetic:

```c
for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
cptr->mantissa[idx + rightshift] += bint;
tumblerjustify (cptr);
```

It finds the last non-zero mantissa digit and adds at `idx + rightshift`. There is no check preventing the result from crossing into the link subspace (crossing mantissa[0] from 1 to 2). Overflow from 1.9999... to 2.0 is arithmetically possible. There is no guard.

---

### Summary

| Path | Contiguity Guaranteed? | Mechanism |
|------|----------------------|-----------|
| `doappend` → `findvsatoappend` | **Yes** | Finds max `reach` of text crums; appends from there |
| `doinsert` with explicit VSA | **No** | `acceptablevsa` is a stub returning `TRUE` unconditionally [do2.c:110-113] |
| `dodeletevspan` | **N/A (no new allocation)** | Shifts post-deletion positions down; compacts V-space |

**Precise answer to the question:** Within the text subspace, if V-positions were allocated exclusively through `doappend`, then contiguity holds — ordinal k+1 must exist if k and k+2 do, because each append begins at `findnextaddressinvspace`'s maximum-reach result [orglinks.c:71]. But this invariant is not enforced at the storage layer: `acceptablevsa` [do2.c:110-113] is a no-op, and `doinsert` accepts arbitrary V-positions. **The allocator provides contiguity as a behavioral consequence of the append path, not as a structural guarantee.** A caller using explicit VSAs via `doinsert` or `docopy` can produce sparse (non-contiguous) V-allocations within a subspace, and the backend will not detect or reject this.
