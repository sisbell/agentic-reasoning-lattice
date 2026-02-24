## KB Synthesis

Looking at the link discovery mechanism in the KB:

**YES, the link still appears in `find_links` results when querying by source or target.**

Here's why:

## Link Discovery is Per-Endset

[ST-FIND-LINKS] and [INT-SPORGL-LINK-INDEX] establish that `find_links` operates by searching the spanfilade independently for each endset type:

- FROM endsets indexed at LINKFROMSPAN=1  
- TO endsets indexed at LINKTOSPAN=2
- THREE (type) endsets indexed at LINKTHREESPAN=3

When you call `find_links(source_specs, NOSPECS, NOSPECS)`, the operation searches **only** the FROM endset indices. It performs an I-address intersection between your query and the link's source I-addresses. The TO and THREE endsets are not consulted at all during this search.

## Evidence from Orphaned Link Behavior

[EC-ORPHANED-LINK] Finding 0024 provides the critical behavior matrix:

| Deleted Content | `find_links` by source | `find_links` by target |
|----------------|----------------------|----------------------|
| Source only    | Empty               | Works               |
| Target only    | Works               | Empty               |
| Both endpoints | Empty               | Empty               |

This confirms that `find_links` results depend **only on the queried endpoint**, not on whether other endpoints are resolvable.

## Type Endset Independence

[SS-LINK-ENDPOINT] Finding 0024 shows the type anomaly: when calling `follow_link(link_id, LINK_TYPE)` after both source and target are deleted, the type endset ALSO returns empty (marked as "UNEXPECTED"). However, this is about `FOLLOWLINK` behavior, not `find_links` discovery.

The key distinction:
- `find_links` searches **only the specified endsets** via I-address intersection  
- `follow_link` retrieves **all endsets** and resolves them to V-addresses

## Mechanism Details

[PRE-FIND-LINKS] Finding 0029 states: "find_links() requires that the searched endpoint content exists in the V-stream (visible view) to discover a link." This applies to **the searched endpoint**, not to all endpoints.

Therefore: If source content remains referenced (I-addresses have V-positions), `find_links(source_specs)` will find the link, regardless of whether the type endset is resolvable. The type endset's ghost state only affects `follow_link(link_id, LINK_TYPE)` retrieval.

## Code Exploration

Based on my analysis of the source code, I can now answer your question:

## Answer: YES, the link still appears in find_links results

After DELETE removes content that a link's type endset references, making the type endset unresolvable to any V-address, **the link STILL appears in find_links results when querying by source or target content that is still referenced**.

## Code Analysis and Citations

### 1. How find_links Works

When `find_links` is called, it flows through:
- `dofindlinksfromtothree` [do1.c:348] → `findlinksfromtothreesp` [spanf1.c:56-103]

In `findlinksfromtothreesp` [spanf1.c:56-103]:

```c
if (fromvspecset)
    specset2sporglset (taskptr, fromvspecset, &fromsporglset,NOBERTREQUIRED);  // line 71
if (tovspecset)
    specset2sporglset (taskptr, tovspecset, &tosporglset,NOBERTREQUIRED);      // line 73
if (threevspecset)
    specset2sporglset (taskptr, threevspecset, &threesporglset,NOBERTREQUIRED); // line 75
```

**Critical observation**: When you query by source OR target (without specifying the type endset in the query), the `threevspecset` parameter is NULL, so line 75 never executes. The function doesn't attempt to resolve or validate the link's stored type endset.

### 2. Link Storage vs Query

When a link is created with `docreatelink` [do1.c:195-221]:
- Line 218: `insertendsetsinorgl` stores all three endsets (source, target, type) IN the link's granfilade
- Line 219: `insertendsetsinspanf` indexes all three endsets IN the spanfilade for searching

The spanfilade contains separate indices:
- `LINKFROMSPAN` (value 1) - for source endset
- `LINKTOSPAN` (value 2) - for target endset  
- `LINKTHREESPAN` (value 3) - for type endset

[spanf1.c:77,85,93]

### 3. Query Processing

When find_links searches by source [spanf1.c:77]:
```c
sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
```

This queries ONLY the `LINKFROMSPAN` dimension of the spanfilade. It retrieves all links whose source endset intersects with the query specset. **It never attempts to resolve or validate the link's type endset**.

### 4. Intersection Logic

After collecting matching links from each queried dimension [spanf1.c:100]:
```c
intersectlinksets(taskptr,fromlinkset,tolinkset,threelinkset,linksetptr);
```

In `intersectlinksets` [spanf2.c:46-120], lines 64-71:
```c
/* If only one linkset is non-null, then just use it */
if (linkset1 && !linkset2 && !linkset3)
    *linkset4ptr = linkset1;
else if (!linkset1 && linkset2 && !linkset3)
    *linkset4ptr = linkset2;
else if (!linkset1 && !linkset2 && linkset3)
    *linkset4ptr = linkset3;
```

**This confirms**: When querying by ONLY source (linkset1 non-NULL, others NULL), all links matching the source are returned, regardless of whether their type endset is resolvable.

## Verification in Existing Tests

The test suite already documents related behavior:
- `search_endpoint_removal.py` contains scenarios where source or target content is deleted
- `scenario_search_by_target_after_source_removed` [search_endpoint_removal.py:96-156] shows that deleting one endpoint doesn't prevent finding the link via the other endpoint
- However, **no existing test covers the specific case of an unresolvable type endset**

## Semantic Implication

The link's **type endset is metadata stored with the link**, not a filtering constraint during search. The find_links operation:
1. Queries the spanfilade indices for links matching the specified source/target criteria
2. Returns matching link ISAs
3. **Never validates** whether the link's type endset is still resolvable

The type endset would only matter if:
- You explicitly query by type endset (rare)
- You later call `follow_link(link_id, LINK_TYPE)` or `retrieve_endsets` on the link

## Conclusion

**Yes, the link remains discoverable** via source or target searches even when its type endset becomes unresolvable. The unresolvable type endset is "orphaned metadata" - it doesn't prevent the link from being found, it only affects operations that specifically try to access the type endset itself.

This behavior aligns with Xanadu's permanence philosophy: links are never deleted, only potentially "orphaned" when their referenced content disappears from the V-stream.
