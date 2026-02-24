## KB Synthesis

# Answer: Yes, the link is discovered with partial fragment overlap

When REARRANGE fragments a link's endset, `find_links` using a VSpec covering **only one fragment** will still discover the link. The reason lies in how link discovery operates.

## The Mechanism

From **[ST-FIND-LINKS]** (Finding 0028):
> The postcondition for `find_links` is: return the set of all links whose source endpoint I-addresses have non-empty intersection with the search specset's I-addresses. Partial overlap suffices — a search specset that shares even one I-address with a link endpoint will discover that link.

The formal condition is:
```
find_links(search) = {link | I-addresses(search) ∩ I-addresses(link.endpoint) ≠ ∅}
```

## Why This Works After REARRANGE

From **[INV-REARRANGE-IDENTITY]** (Finding 0056):
> Rearrange preserves I-addresses exactly. The code modifies only `ptr->cdsp.dsas[index]` (the V-address component of the displacement). The I-address, stored separately, is never touched.

**Before REARRANGE:**
- Link created on content at V-position 1.3, width 0.4
- Content has I-addresses {i₁, i₂, i₃, i₄}

**After REARRANGE (fragmentation):**
- Same content now at multiple V-positions: fragment₁ at 1.2 (i₁, i₂) and fragment₂ at 1.5 (i₃, i₄)
- I-addresses unchanged: {i₁, i₂, i₃, i₄}
- Link endpoint still references: {i₁, i₂, i₃, i₄}

**Query covering only fragment₁:**
- Search VSpec converts to I-addresses: {i₁, i₂}
- Intersection check: {i₁, i₂} ∩ {i₁, i₂, i₃, i₄} = {i₁, i₂} ≠ ∅
- **Result: Link discovered** ✓

## Supporting Evidence

From **[INT-LINK-TRANSCLUSION]** (Finding 0028), there's a concrete example of partial overlap being sufficient:

> Document C transcludes "EF" from A via vcopy:
>   C's "EF" has I-addresses I.5, I.6 (shared with A)
> 
> find_links(specset covering C's "EF"):
>   I-addresses of search: {I.5, I.6}
>   I-addresses of link source: {I.4, I.5, I.6}
>   Intersection: {I.5, I.6} ≠ ∅
>   → Link returned (partial overlap is sufficient)

The same principle applies: a query covering ANY subset of the link's endpoint I-addresses will discover it.

## Conclusion

Link discovery is **I-address intersection-based**, not V-position-based. REARRANGE changes V-positions but preserves I-addresses **[INV-REARRANGE-IDENTITY]**. Since partial I-address overlap suffices for discovery **[ST-FIND-LINKS]**, querying any single fragment will discover the link.

## Code Exploration

Based on my thorough analysis of the udanax-green C source code, I can now provide a definitive answer to your question:

---

## Answer: YES, querying ONE fragment discovers the link

When REARRANGE fragments a link's endset across non-contiguous V-positions within the same document, subsequent `find_links` using a VSpec covering **only ONE** of the fragments **still discovers the link**. The query does **NOT** need to span all fragments.

## Code Evidence

### 1. Link Discovery Uses I-Span Intersection

The critical function is `sporglset2linksetinrange` [sporgl.c:239]:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
```

This retrieves from the spanfilade where:
- **SPANRANGE** matches the I-span (permascroll identity) from the query's V→I conversion
- **ORGLRANGE** matches the link's stored endset

The link is found if its endset **overlaps with ANY I-span** in the query.

### 2. REARRANGE Preserves I-Span Identity

The `rearrangend` function [edit.c:78-160] only modifies **V-displacements**:

```c
tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```
[edit.c:125]

This changes the V-position (`cdsp` in the V dimension) but **does NOT change** the I-position (permascroll identity). Each fragment retains its original I-span.

### 3. Query Processing Flow

When you call `find_links` with a VSpec covering one fragment:

1. **V→I Conversion**: `vspanset2ispanset` [orglinks.c:397] converts the VSpec to I-spans using the document's POOM
2. **Permutation Query**: `permute` [orglinks.c:404] calls `span2spanset` which calls `retrieverestricted` to find crums where the fragment's V-position maps to I-space
3. **Link Retrieval**: `sporglset2linksetinrange` [sporgl.c:259] queries the spanfilade for links whose endset overlaps the fragment's I-span
4. **Result**: The link is found because its endset in the spanfilade still references the fragment's I-span

### 4. Intersection Logic

The `findlinksfromtothreesp` function [spanf1.c:56-103] finds links for each endset independently, then **intersects** the results:

```c
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```
[spanf1.c:100]

However, this intersection is across **different endsets** (from/to/three), not across fragments within a single endset.

## Why This Works

**Key Insight**: Links are indexed by **I-spans** (permascroll identity), not V-spans (virtual positions).

- When you create a link with endset "BCDEFGH" at V-positions 1.2-1.8, the backend stores references to the **I-addresses** that those V-positions map to
- When REARRANGE splits "BCDEFGH" into fragments "BC" (at 1.2), "GH" (at 1.4), and "DEF" (at 1.20), each fragment **retains its I-address**
- The link's endset in the spanfilade **remains unchanged** — it still references the same I-addresses
- When you query with a VSpec covering "BC" at 1.2, the V→I conversion finds the I-addresses for "BC"
- Those I-addresses overlap with the link's endset in the spanfilade
- Therefore, the link is discovered

## Empirical Verification Needed

While the source code clearly indicates this behavior, I've created a test scenario (`find_links_after_endset_fragmentation`) that should be run to empirically verify. The test fragments a link's endset via REARRANGE and queries each fragment individually.

Would you like me to commit this test and run it to empirically confirm the behavior?
