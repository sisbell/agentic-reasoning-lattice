## KB Synthesis

Yes, the three endsets (source, target, type) are resolved **independently** during FOLLOWLINK — each endset's resolution depends solely on whether its specific I-addresses have POOM mappings, not on the resolution status of other endsets.

## Evidence for Independent Resolution

**[EC-ORPHANED-LINK]** provides the definitive evidence through a behavior matrix showing asymmetric outcomes:

| Deleted Content | source endset | target endset | type endset |
|----------------|---------------|---------------|-------------|
| Source text only | Empty | Works | Works |
| Target text only | Works | Empty | Works |
| Both source & target | Empty | Empty | Empty* |

The first two rows prove independence: deleting source content makes only the source endset empty while target remains functional, and vice versa. If endsets were coupled, source deletion would affect target resolution.

## Resolution Mechanism

**[SS-FOLLOWLINK]** and **[INV-ITOV-FILTERING]** describe the underlying mechanism:

1. FOLLOWLINK retrieves I-addresses from the link orgl at the requested endset position (0.1 for source, 0.2 for target, 0.3 for type)
2. Each I-address is independently converted to V-addresses via `linksporglset2specset()` using the querying document's POOM
3. At `span2spanset()`, `retrieverestricted()` searches for each I-address in the POOM
4. If an I-address has no POOM mapping, it is silently dropped — no error, just omitted from results
5. This filtering is **per-I-address**, not per-endset

**[EC-GHOST-LINK]** confirms three possible outcomes per endset: (1) all I-addresses live → full result, (2) some unreferenced → partial result, (3) all unreferenced → empty result `[]`.

## Anomaly with Type Endset

There is one exception: when BOTH source and target are deleted, the type endset returns empty even though type references the bootstrap document (which was not deleted). **[EC-ORPHANED-LINK]** marks this with an asterisk as unexpected behavior — either a bug or an undocumented dependency of type resolution on endpoint resolution.

## Conclusion

Yes, endsets resolve independently under normal conditions. The source endset can return empty while target returns valid spans, and vice versa, based solely on which content exists in POOMs. The type endset anomaly when both endpoints are deleted is an edge case requiring further investigation.

## Code Exploration

Based on my analysis of the source code, I can now answer your question about whether the three endsets are resolved independently during operations like FOLLOWLINK and RETRIEVEENDSETS.

## RETRIEVEENDSETS: Sequential but Partially Independent

The three endsets are **NOT** fully independent. Looking at `retrieveendsetsfromspanf` [spanf1.c:190-235], the resolution uses a short-circuit boolean chain:

```c
if (!(specset2sporglset (taskptr, specset, &sporglset, NOBERTREQUIRED)
    && retrievesporglsetinrange(taskptr,sporglset,&fromspace,&fromsporglset)
    && linksporglset2specset (taskptr,&((typevspec *)specset)->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
    && retrievesporglsetinrange (taskptr, sporglset, &tospace, &tosporglset)
    && linksporglset2specset (taskptr, &((typevspec*)specset)->docisa, tosporglset, tosetptr, NOBERTREQUIRED))){
            return (FALSE);
}
```

**However**, there's a critical distinction between **failure** and **empty results**:

### Failure Modes (Returns FALSE):

1. If the link document doesn't exist [sporgl.c:44-46]:
```c
if (!findorgl (taskptr, granf, docisa, &orgl,type)){
    return (NULL);  // Propagates to specset2sporglset failure
}
```

2. If any document referenced in an endset doesn't exist, `specset2sporglset` fails [sporgl.c:25-27]

### Success with Empty Result (Returns TRUE):

If a document exists but the content at an endset has been deleted, the resolution **succeeds** and returns an empty specset. Looking at `linksporglset2specset` [sporgl.c:97-123]:

```c
*specsetptr = NULL;  // Line 102
for (; sporglset; sporglset = ...) {
    // Process sporgls - loop doesn't execute if sporglset is empty
}
return (TRUE);  // Line 122 - Always returns TRUE
```

And `retrievesporglsetinrange` [spanf1.c:237-267] also always returns TRUE [line 266], even if no content is found.

**Answer to your specific question:** **Yes**, the source endset can resolve successfully (returning content) while the target endset returns empty (NULL specset) because the target's content was deleted from all POOMs. The resolution succeeds as long as all referenced **documents exist**, regardless of whether their **content** has been deleted.

## FOLLOWLINK: Different Behavior

In contrast, `dofollowlink` [do1.c:223-232] calls `link2sporglset` [sporgl.c:67-95], which **fails** if an endset is empty:

```c
if (context = retrieverestricted((typecuc*)orgl, &vspan ,V, (typespan*)NULL, I, (typeisa*)NULL)) {
    // Process context...
    return (TRUE);
} else{
    return (FALSE);  // Line 92-93: Fails if no content found
}
```

So **FOLLOWLINK fails** if the requested endset is empty, while **RETRIEVEENDSETS succeeds** and returns an empty specset for that endset.

## Summary

The endsets are resolved **sequentially** in a short-circuit chain, not fully independently. But:

- **Document-level failures** (document doesn't exist) fail the entire operation
- **Content-level emptiness** (deleted content) succeeds with empty results in RETRIEVEENDSETS
- **Content-level emptiness** fails in FOLLOWLINK
