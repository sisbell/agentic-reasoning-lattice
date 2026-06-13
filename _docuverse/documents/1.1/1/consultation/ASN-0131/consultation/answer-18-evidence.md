## Question 18 [evidence]

> Because the spanfilade is write-only and never has DOCISPAN/endset entries removed [FC-SPANFILADE-MONOTONIC], can this query return an endset whose content was deleted from every V-stream, making its answer reflect historical rather than current anchoring state?

## KB Synthesis

Yes — with an important qualification about which layer exhibits the staleness.

## The Discovery Layer: Genuinely Historical

The spanfilade is monotonically append-only [INV-SPANF-WRITE-ONLY]: `∀ t₁ < t₂ : spanf_entries(t₁) ⊆ spanf_entries(t₂)`. No DELETE ever removes spanfilade entries [INT-DELETE-SPANF-DIVERGENCE]. This means the *discovery phase* of any spanfilade-based query can find links whose endpoints index I-addresses that no longer appear in any V-stream.

For FIND_DOCUMENTS this is directly observable: `actual_docs(i) ⊆ find_documents(i)` — the query returns a historical superset [EC-STALE-SPANF-REFERENCE]. Documents from which content was deleted still appear.

## The Resolution Layer: Filtered to Current POOM State

RETRIEVEENDSETS has two phases [SS-RETRIEVE-ENDSETS]:

1. **Search phase** (spanfilade, SPANRANGE + ORGLRANGE): Can locate link endpoint I-addresses registered by historical CREATELINK calls, even if that content is now deleted everywhere.
2. **Resolution phase** (I→V conversion via querying document's POOM): `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()` silently drops any I-address with no current POOM mapping [INV-ITOV-FILTERING].

The resolution phase acts as a real-time filter. If the endset's I-addresses are not in the querying document's current POOM — whether because the content was deleted, or because it lives in a different document's POOM — those I-addresses produce no V-spans. They are dropped silently, not returned at historical positions.

## The Practical Outcome: Ghost Links, Not Stale Positions

When endset content has been deleted from every V-stream, RETRIEVEENDSETS does not return historical V-positions — it returns an empty endset. The link is still discoverable (spanfilade is permanent [INV-LINK-PERMANENCE]), but its endpoints resolve to nothing. This is the "ghost link" state [EC-GHOST-LINK]:

```
Before deletion:
  RETRIEVEENDSETS(content_region) → from-endset: [V 1.4 for 0.5]

After all endset content deleted from every POOM:
  RETRIEVEENDSETS(content_region) → from-endset: []   (works: true)
```

The link orgl is intact in I-space (permanent), the spanfilade still indexes it, but the I→V filter silently excludes all its endpoint I-addresses.

## The Asymmetry with FOLLOWLINK

FOLLOWLINK [SS-FOLLOWLINK] exposes the same mechanism but more visibly: you supply the link ISA directly, and it reads the endset I-addresses from the link orgl, then resolves them through the specified document's POOM. If those I-addresses have no current POOM mapping, the result is empty — success, no error, no historical positions.

RETRIEVEENDSETS and FOLLOWLINK both reflect **current POOM state applied to permanent I-addresses**. The permanence is in I-space; the currency is in the resolution step.

## Summary

| Layer | Exhibits Staleness? | Mechanism |
|-------|--------------------|-|
| Spanfilade discovery | **Yes** | Write-only, entries never removed [INV-SPANF-WRITE-ONLY] |
| FIND_DOCUMENTS result | **Yes** | Returns historical superset [EC-STALE-SPANF-REFERENCE] |
| RETRIEVEENDSETS V-spans | **No** | I→V filter clamps to current POOM [INV-ITOV-FILTERING] |
| Ghost link endsets | **Empty, not stale** | Unresolvable I-addresses dropped silently [EC-GHOST-LINK] |

The spanfilade's monotonicity creates staleness at the discovery level, but the I→V resolution step prevents that staleness from propagating into returned V-positions. What you receive instead of historical anchoring data is absence — empty endsets where historical content once lived.

---

## Code Exploration

I have all the evidence. Here is the complete analysis with source citations.

---

## Analysis: Can `retrieve_endsets` Return a Stale (Fully-Deleted) Endset?

**Short answer: No.** The spanfilade is indeed monotonic and retains endset entries after deletion, but two POOM-based filters — one on the input path, one on the output path — prevent stale endsets from surfacing.

---

### 1. Confirming FC-SPANFILADE-MONOTONIC

`dodeletevspan` [do1.c:158–167] calls only `deletevspanpm` [orglinks.c:145–152]:

```c
// orglinks.c:145-152
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr) {
    if (iszerotumbler(&vspanptr->width)) return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

The `fullcrumptr` passed to `deletend` [edit.c:31] is `docorgl` — the **document's POOM** — never `spanf`. The spanfilade is never touched. Every DOCISPAN and LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN entry inserted by `insertspanf` [spanf1.c:22–52] persists permanently.

---

### 2. Spanfilade Data Layout

The spanfilade is a 2D SPAN enfilade (wisp.h:15–17: `ORGLRANGE=0, SPANRANGE=1`). `insertspanf` [spanf1.c:22–52] stores each endset as:

```
ORGLRANGE = prefixtumbler(linkISA, spantype)   // = 1.linkISA for LINKFROMSPAN
SPANRANGE = I-span of endset content            // permascroll address
homedoc   = docISA of document containing the content
```

For LINKFROMSPAN, LINKTOSPAN, LINKTHREESPAN the stored span type prefixes place entries in disjoint ORGLRANGE bands: [1,2), [2,3), [3,4) respectively [xanadu.h:36–39].

---

### 3. The `retrieve_endsets` Execution Path

Command 28 → `retrieveendsets` [fns.c:350–362] → `doretrieveendsets` [do1.c:369–374] → `retrieveendsetsfromspanf` [spanf1.c:190–235].

The function has three sequential steps:

#### Step 1 — Input gate: V-spec → I-spans via POOM

```c
// spanf1.c:222
specset2sporglset(taskptr, specset, &sporglset, NOBERTREQUIRED)
```

`specset2sporglset` [sporgl.c:14–33] → `vspanset2sporglset` [sporgl.c:35–65] → `vspanset2ispanset` [orglinks.c:397–402]:

```c
// orglinks.c:397-402
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, typeispanset *ispansetptr) {
    typespanset *permute();
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

This queries the document's POOM orgl. `deletend` [edit.c:63] subtracts deleted widths from subsequent crums, confirming the POOM is cumulative and reflects current state. **Only surviving V-positions map to I-spans.** Content deleted via `dodeletevspan` has no V→I entries in the POOM, so its I-spans are never placed into `sporglset`.

#### Step 2 — Spanfilade query

```c
// spanf1.c:223,245
retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset)

// inside retrievesporglsetinrange — spanf1.c:245
context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE, whichspace, ORGLRANGE, NULL);
```

`fromspace` is `{stream.mantissa[0]=LINKFROMSPAN=1, width.mantissa[0]=1}` [spanf1.c:210–211], restricting ORGLRANGE to [1,2) — the LINKFROMSPAN band.

`sporglptr` cast to `typespan*` aligns `sporglptr->sporglorigin` with `typespan->stream` (both are at the same struct offset per xanadu.h:65–121). So the SPANRANGE restriction = the surviving content I-spans from Step 1.

`crumqualifies2d` [retrie.c:270–305] independently tests both SPANRANGE and ORGLRANGE. A LINKFROMSPAN crum qualifies only if its SPANRANGE (= endset content I-span) **overlaps** with the query SPANRANGE (= surviving content I-spans from Step 1). Endset content that was fully deleted is not in `sporglset` at all, so its crum is never reached by the query.

#### Step 3 — Output gate: I-spans → V-spans via POOM

```c
// spanf1.c:224
linksporglset2specset(taskptr, &((typevspec*)specset)->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
```

`linksporglset2specset` [sporgl.c:97–123] → `linksporglset2vspec` [sporgl.c:127–137] → `sporglset2vspanset` [sporgl.c:141–176] → `ispan2vspanset` [orglinks.c:389–394]:

```c
// orglinks.c:389-394
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr) {
    typespanset *permute();
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

This converts found I-spans back to V-spans through the POOM. Any I-span portion deleted from the POOM produces no V-span. This is confirmed by the golden test `endsets_after_source_delete.json`: after deleting "right " from "right here", the returned endset shrinks from `{start:1.7, width:0.10}` to `{start:1.7, width:0.4}` — the surviving "here" (4 chars) appears, the deleted "right " (6 chars) does not.

---

### 4. After Complete Deletion from All V-Streams

For content deleted from every V-stream:

- **Step 1 fails silently:** `vspanset2ispanset` traverses the current POOM. With no surviving V-positions for the deleted content, `permute`/`span2spanset` [orglinks.c:404–454] → `retrieverestricted` on the POOM finds nothing. `sporglset` is empty or contains only unrelated content.
- **Step 2 is never reached for that I-span:** The empty/unrelated sporglset never includes the deleted endset's I-span, so the LINKFROMSPAN spanfilade entry (which persists forever) is never matched.
- **Step 3 would return empty anyway:** Even if a raw I-span were injected as ISPANID [sporgl.c:20–22] bypassing Step 1's POOM filter, `ispan2vspanset` through the document POOM returns nothing because no V-mapping for the deleted I-span exists.

---

### 5. The Invariant

The spanfilade's monotonicity [FC-SPANFILADE-MONOTONIC] is real and confirmed by the code. But `retrieve_endsets` never exposes raw I-spans to callers — the result is always a VSPECID (or empty). The two POOM gates enforce that the answer reflects **current** anchoring state:

| Path | Guard | Effect on deleted content |
|------|-------|--------------------------|
| Input: `vspanset2ispanset` [orglinks.c:397] | Current document POOM | Deleted V-positions produce no I-spans — they never enter the query |
| Output: `ispan2vspanset` [orglinks.c:389] | Current document POOM | Deleted I-spans produce no V-spans — they never reach the caller |

The retained spanfilade entries are inert with respect to this query. They serve the forward-direction query (`find_links`, command 30 via `sporglset2linkset` [sporgl.c:222–237]) — given a *surviving* content I-span, find which links have it as an endset — a query for which monotonicity is a correctness property, not a hazard.

**Conclusion:** `retrieve_endsets` cannot return an endset whose content has been deleted from every V-stream. The answer always reflects current anchoring state. Historical I-span entries in the spanfilade are effectively inert for this query because the POOM, which is authoritative about what exists, gates both the input and output of the spanfilade lookup.
