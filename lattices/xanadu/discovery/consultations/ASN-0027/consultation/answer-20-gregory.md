## Question 20 [gregory]

> After CREATELINK advances the I-address allocation counter past the text range, subsequent text inserts receive non-contiguous I-addresses — does this gap in the I-address space have any effect on `findpreviousisagr` performance or correctness, and can the gap ever be reclaimed?

## KB Synthesis

## CREATELINK I-Address Gap: Performance, Correctness, and Reclamation

### Performance Effect on `findpreviousisagr`

No meaningful effect. From [SS-ADDRESS-SPACE] (Finding 0061), `findpreviousisagr` performs a B-tree traversal to find the highest existing I-address below an upper bound. The link orgl's I-address occupies exactly one granfilade node — structurally identical to a text character entry. The traversal is O(log N) regardless of whether the maximum found is a text atom or link orgl. The gap between text I-addresses doesn't create any additional nodes to traverse; it's just empty address space that the traversal skips over by going directly to the tree maximum.

### Correctness Effect

No correctness issue. From [INV-MONOTONIC] (Finding 0063), the monotonic invariant `∀ alloc_a, alloc_b : time(a) < time(b) ⟹ iaddr(b) > iaddr(a)` spans all entity types — text characters and link orgls share the same monotonic sequence. When the next text INSERT calls `findpreviousisagr`, it correctly finds the link orgl as the highest existing address and allocates one above it. This is the intended behavior.

The observable consequence — `compare_versions` returning two shared span pairs instead of one for INSERT + CREATELINK + INSERT sequences [INT-LINK-INSERT] — is a semantic artifact, not a data corruption. The I-addresses are allocated correctly; they're just non-contiguous in the text subsequence.

### Can the Gap Be Reclaimed?

No. Three converging properties make this permanent:

1. **Append-only granfilade**: From [FC-GRANF-ON-DELETE] (Finding 0061), DELETE and REARRANGE never modify the granfilade. The link orgl's I-address persists regardless of subsequent operations.

2. **No I-address reuse**: From [INV-NO-IADDR-REUSE], the allocator never backfills gaps. Allocation is purely `findpreviousisagr + 1` — it always advances forward from the current maximum, never returns to fill space vacated by the link orgl (which can't be vacated anyway).

3. **No free list**: From [SS-ADDRESS-SPACE] (Finding 0077), "there is no single global 'next' counter (no Σ.next). Allocation is stateless query-and-increment." There is no free-list mechanism, no gap-tracking, and no garbage collection.

The gap is a permanent structural feature of the granfilade. All future text inserts continue upward from above the link orgl's I-address. The only way to avoid the gap would have been to not call CREATELINK between the two text inserts — once made, the allocation cannot be undone.

---

## Code Exploration

Now I have all the information needed to give a complete, code-cited answer. Let me synthesize.

---

## Full Answer

### 1. How CREATELINK Allocates its I-address

`docreatelink` (`do1.c:207`) calls:
```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
createorglingranf(taskptr, granf, &hint, linkisaptr)
```
This reaches `findisatoinsertmolecule` (`granf2.c:158`) with `atomtype=LINKATOM=2` (`xanadu.h:146`). The upper bound for the link search is:
```c
tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
// LINKATOM+1 = 3 → upperbound = docisa.0.3
```
`findpreviousisagr` (`granf2.c:255`) is called with this `docisa.0.3` upper bound, which traverses the entire atom range (text and links both fall below `docisa.0.3`). The first link then lands at `docisa.0.2.1`, the second at `docisa.0.2.2`, and so on (`granf2.c:170-175`).

For **text insertion**, `doinsert` (`do1.c:117`) uses `TEXTATOM=1` (`xanadu.h:145`), and the upper bound is:
```c
tumblerincrement(&hintptr->hintisa, 2, TEXTATOM + 1, &upperbound);
// TEXTATOM+1 = 2 → upperbound = docisa.0.2
```

---

### 2. The Premise Is Incorrect: There Is No Cross-Contamination

The text and link I-address subspaces are **structurally disjoint**:

- Text atoms live at `docisa.0.1.N` (mantissa `[..., 0, 1, N, ...]`)
- Link atoms live at `docisa.0.2.N` (mantissa `[..., 0, 2, N, ...]`)

Because link ISAs are at `docisa.0.2.N` (where `N ≥ 1`), they are all **numerically ≥ `docisa.0.2`** (`tumblercmp` [tumble.c:72] compares mantissa digit-by-digit: `[...,0,2,1,...]` > `[...,0,2,0,...]`). The text-insertion upper bound is exactly `docisa.0.2`.

In `findpreviousisagr` (`granf2.c:267-276`):
```c
for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
    if ((tmp = whereoncrum(ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
    || tmp == ONMYRIGHTBORDER || !ptr->rightbro) {
        findpreviousisagr(ptr, upperbound, offset);
        return(0);
    } else {
        tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);
    }
}
```

`whereoncrum` (`retrie.c:345-398`) computes:
```c
right = offset + ptr->cwid.dsas[WIDTH];
return intervalcmp(offset, right, address=docisa.0.2);
```

Any granfilade crum whose interval begins at `docisa.0.2.1` or later will return `TOMYLEFT` for the text upper bound (`docisa.0.2`), meaning `docisa.0.2 < left_boundary_of_crum`. That crum will **not** have its width accumulated, and traversal never enters the link subspace.

**CREATELINK does not advance the text I-address counter at all.** After a link is created at `docisa.0.2.1`, the text `findpreviousisagr` call (upperbound=`docisa.0.2`) will find the last *text* atom and return that as `lowerbound`. Text allocation continues sequentially within `docisa.0.1.*`, completely unaffected.

---

### 3. How WIDTH Values Encode Gaps — and Why Gaps Don't Add Nodes

`insertseq` (`insert.c:17-70`) encodes item boundaries as **tumbler differences** in `cwid.dsas[WIDTH]`:
```c
if (iszerotumbler(&ptr->cwid.dsas[WIDTH])) {  /* last crum in granf */
    tumblerclear(&new->cwid.dsas[WIDTH]);
    tumblersub(&nextaddress, &offset.dsas[WIDTH], &ptr->cwid.dsas[WIDTH]);
} else {
    dspadd(&offset, &ptr->cwid, &reach, GRAN);
    tumblersub(&reach.dsas[WIDTH], &nextaddress, &new->cwid.dsas[WIDTH]);
    tumblersub(&nextaddress, &offset.dsas[WIDTH], &ptr->cwid.dsas[WIDTH]);
}
```

Each granfilade crum's WIDTH is the tumbler distance from its left boundary to the next item. A large gap (e.g., the "jump" from text subspace `docisa.0.1.*` to link subspace `docisa.0.2.*`) is encoded entirely within the WIDTH of the **crum immediately preceding the gap** — it does not create any additional nodes in the enfilade tree.

Because `findpreviousisagr` accumulates these WIDTH values (`tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset)`) to reconstruct absolute ISA positions, and because gap width is folded into one crum's WIDTH field, **no extra traversal steps occur for gaps**. Performance is strictly O(height of enfilade), which grows logarithmically with the number of inserted **items** — not with the size of any gap between them.

---

### 4. The Asymmetry: Link Search *Does* Traverse Text Subspace

The reverse is true for link allocation. CREATELINK uses upperbound `docisa.0.3`, which **does** span the entire text subspace. A document with N text chunks will cause `findpreviousisagr` to traverse those text crums when allocating each subsequent link. However, this is also O(height) due to the enfilade structure, so it does not degrade performance pathologically; it just means link-space `findpreviousisagr` touches more of the tree than text-space `findpreviousisagr` does.

---

### 5. Gap Reclamation: Impossible by Design

There is no ISA-reclamation or renumbering operation anywhere in the codebase. The granfilade is purely additive. `dodeletevspan` (`do1.c:158`) removes content from the POOM (V-space document tree), not from the granfilade (I-space). The permascroll's permanent-address guarantee means once an ISA is allocated — and the WIDTH of the preceding crum is adjusted to account for the gap — that gap is structurally fixed forever.

Gaps in I-space are not "wasted" in the sense of consuming extra storage: they exist only as larger WIDTH tumbler values in the preceding crum, which is a fixed-size field. Reclaiming them would require re-assigning ISAs globally, which would invalidate every link, span, and cross-document reference in the system — a foundational violation of the Xanadu model.

---

### Summary

| Question | Answer | Citation |
|---|---|---|
| Does CREATELINK advance the text I-address counter? | No. Text search upper bound is `docisa.0.2`; link ISAs at `docisa.0.2.*` are ≥ that bound, invisible to text search. | `granf2.c:162`, `granf2.c:168-169` |
| Does any gap affect `findpreviousisagr` performance? | No. Gap magnitude is encoded in a preceding crum's WIDTH field; no extra tree nodes. | `insert.c:53-60`, `granf2.c:255-278` |
| Does any gap affect `findpreviousisagr` correctness? | No. WIDTH-based offset accumulation gives correct absolute ISA regardless of gap size. | `granf2.c:275`, `tumble.c:365-404` |
| Can gaps be reclaimed? | No. The granfilade is insert-only; no ISA-delete or renumber operation exists. Gaps are permanent Width values in predecessor crums. | `insert.c:17-70`, `do1.c:158-167` |
