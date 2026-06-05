## Question 15 [evidence]

> Given FC-SPANFILADE-MONOTONIC, can a link enumerated in an earlier window ever disappear from a later window — for instance if its endpoint content is deleted from all POOMs between calls?

## KB Synthesis

**Yes, a link can disappear from a later pagination window**, despite [INV-SPANF-WRITE-ONLY].

The reason involves two independent mechanisms that the question conflates.

---

## The Spanfilade Is Append-Only — But That's the Index Side

[INV-SPANF-WRITE-ONLY] guarantees that once a link's endpoint I-addresses are recorded in the spanfilade, those records are never removed. No `deletespanf` function exists. This is unconditional.

But the spanfilade monotonicity invariant governs the **index** side of the search, not the **query** side.

---

## The Query Side Depends on POOM State

[ST-FIND-LINKS] (Finding 0028, 0029): `find_links` operates by:
1. Converting the caller's search specset → I-addresses via the **querying document's POOM**
2. Intersecting those I-addresses against the spanfilade

If the endpoint content of the search specset is deleted from all POOMs between calls, step 1 produces an empty I-address set. Empty I-addresses intersect nothing. The link vanishes from results — not because the spanfilade lost the entry, but because the query generates no keys to find it with.

[EC-CURSOR-INVALIDATION] / [SS-PAGINATE-LINKS] makes this concrete: each pagination call **re-runs the full `findlinksfromtothreesp()` search** with the original specsets. The operation is stateless. If the re-run produces a different result set (because POOM state changed), and the cursor ISA no longer appears in it, the call returns empty with count=0.

---

## The Link Itself Is Permanent, But Not Discoverable

[INV-LINK-PERMANENCE] still holds: the link orgl exists in I-space, its spanfilade entries remain, and `follow_link(link_id)` continues to succeed [EC-GHOST-LINK]. The link is a "ghost link" — permanently accessible by ID but absent from content-based discovery.

[EC-ORPHANED-LINK] documents exactly this state: link exists, `follow_link` returns empty or partial spans, `find_links` returns nothing.

---

## Summary

The append-only spanfilade guarantees the **index entries** survive. It says nothing about whether a given search query can still **reach** those entries. Deleting endpoint content from all POOMs between pagination calls collapses the query I-address set, making the link disappear from subsequent windows while the spanfilade retains its records intact.

---

## Code Exploration

---

## Can a Link Enumerated in an Earlier Window Disappear from a Later Window?

**Yes — but through a mechanism that is orthogonal to FC-SPANFILADE-MONOTONIC.** The two layers involved operate independently, and deletion breaks the query path before it ever reaches the spanfilade.

---

### FC-SPANFILADE-MONOTONIC: What It Actually Guarantees

From `knowledge-base/kb-synthesis.md:734`:

> **FC-SPANFILADE-MONOTONIC**: Operations never shrink the granfilade or spanfilade. The invariant `∀ t₁ < t₂ : spanf_entries(t₁) ⊆ spanf_entries(t₂)` holds.

This is confirmed structurally. `spanf1.c` has `insertspanf` but **no deletion function exists**:

```
// spanf1.c and spanf2.c — the complete write API:
bool insertspanf(...)          // ✅ exists
// bool deletespanf(...)       // ❌ does not exist
```

The guarantee is real. Every spanfilade entry written by `insertspanf` [spanf1.c:15] persists permanently. `dodeletevspan` [do1.c:158-167] calls only `deletevspanpm` → `deletend` on the POOM (granf); there is no corresponding spanf cleanup [do1.c:163-167, orglinks.c:145-152].

**But FC-SPANFILADE-MONOTONIC is a claim about the structure of the spanfilade index — not about what `find_links()` returns to callers.** The two are decoupled by the POOM-dependent query path.

---

### The Query Path for `find_links()` — Two Independent Layers

`findnextnlinksfromtothreesp` [spanf1.c:117] (the windowed pagination entry point) delegates directly to `findlinksfromtothreesp` [spanf1.c:56] on every call. There is no persistent cursor or snapshot — each window call re-executes the full query from scratch:

```c
// spanf1.c:124
if (!findlinksfromtothreesp (taskptr, spanf, fromvspecset, tovspecset, threevspecset, orglrangeptr, &linkset))
    return (FALSE);
// ... then skip to lastlink in the fresh result
```

Inside `findlinksfromtothreesp` [spanf1.c:56-103], the query proceeds in two physically separate stages:

**Stage 1 — V-spec → I-address via POOM (mutable layer):**

```c
// spanf1.c:70-75
if (fromvspecset)
    specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
```

`specset2sporglset` [sporgl.c:14-33] dispatches to `vspanset2sporglset` [sporgl.c:35-65], which:
1. Calls `findorgl(taskptr, granf, docisa, &orgl, type)` [sporgl.c:44] — opens the document's POOM
2. Calls `vspanset2ispanset` [orglinks.c:397-402] → `permute` [orglinks.c:404-422] → `span2spanset` [orglinks.c:425-453] — walks the POOM to map V-positions to I-addresses via `retrieverestricted`

The critical guard in `span2spanset` [orglinks.c:446-448]:

```c
// orglinks.c:446-448
if(!context){
    return(targspansetptr);  // nothing added — silently return empty-handed
}
```

If the V-span is not found in the POOM — because `dodeletevspan` already removed it via `deletend` [orglinks.c:149] — `retrieverestricted` returns NULL, `span2spanset` returns without adding anything, and `specset2sporglset` produces an empty sporglset.

**Stage 2 — I-address search in the spanfilade (permanent layer):**

```c
// spanf1.c:76-83
if (fromvspecset) {
    sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
    if (!fromlinkset) {
        *linksetptr = NULL;
        return (TRUE);  // ← returns empty, not an error
    }
}
```

`sporglset2linkset` [sporgl.c:222-237] queries the spanfilade using the I-addresses from Stage 1. If Stage 1 returned nothing — which it does when the V-spec content is deleted — this function is called with an empty input and returns an empty link set. The spanfilade's permanent entry for that link is never reached.

**The consequence**: FC-SPANFILADE-MONOTONIC ensures the spanfilade entry exists, but `find_links()` cannot reach it when the V→I bridge is broken. The window call returns `[]`.

---

### The Scenario: Endpoint Content Deleted from All POOMs

Concretely, for a link created with from-endpoint at V-positions `p..q` in document D:

1. **Window call 1** — content at `p..q` is in D's POOM:
   - Stage 1: `vspanset2ispanset` maps `p..q` → I-addresses `a..b`
   - Stage 2: `sporglset2linkset` finds the link indexed at `a..b` in spanf
   - **Link is returned**

2. **Between calls** — `dodeletevspan` removes `p..q` from D:
   - `deletevspanpm` calls `deletend` on D's POOM [orglinks.c:149]
   - Spanfilade entry at `a..b` is **not touched** (no `deletespanf` exists)

3. **Window call 2** — content at `p..q` is gone from all POOMs:
   - Stage 1: `vspanset2ispanset` on D's POOM → `retrieverestricted` → NULL → empty sporglset
   - Stage 2: `sporglset2linkset` gets empty input → returns empty → `find_links()` returns `[]`
   - **Link is absent** — even though the spanfilade entry is still there

If content was transcluded to a second document D′ before being deleted from D, and D′ still has it: Stage 1 would succeed for D′'s POOM. But the scenario specifies deletion from **all POOMs** — so every document's POOM returns empty for those I-addresses, and `find_links()` returns empty.

---

### `follow_link()` Behaves Differently

`dofollowlink` [do1.c:223-232] bypasses the POOM-first path entirely:

```c
// do1.c:228-231
return (
   link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
&& linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress, sporglset, specsetptr, NOBERTREQUIRED));
```

`link2sporglset` [sporgl.c:67-95] reads I-addresses **directly from the link's own orgl** via `retrieverestricted` on `granf` at the link's V-position (0.1, 0.2, or 0.3) [sporgl.c:83]. It does not go through the document's POOM. The link's orgl is permanent and unaffected by content deletion.

Then `linksporglset2specset` [sporgl.c:97-123] → `sporglset2vspanset` [sporgl.c:141-176] → `ispan2vspanset` [orglinks.c:389-394] → `permute` → `span2spanset` → `retrieverestricted` on the **home doc's POOM**. If all POOMs are empty at those I-addresses, `span2spanset` returns empty (orglinks.c:446-448). The operation **succeeds** (`return TRUE` at sporgl.c:91) but returns empty endsets.

So `follow_link()` never loses visibility of the link (the link orgl is permanent), but it does return empty endsets once all content is removed from all POOMs — confirmed by the golden test `golden/links/orphaned_link_target_all_deleted.json` and Finding 0048.

---

### Summary

| Property | Guarantor | Survives all-POOM deletion? |
|---|---|---|
| Spanfilade entry for link | FC-SPANFILADE-MONOTONIC | ✅ Never removed |
| `find_links()` returns the link | V→I POOM bridge (Stage 1) | ❌ Fails if search-spec content deleted |
| `follow_link()` finds the link | Link orgl in granf (permanent) | ✅ Always succeeds |
| `follow_link()` returns non-empty endsets | POOM at home doc (mutable) | ❌ Empty if all POOMs lack those I-addresses |

FC-SPANFILADE-MONOTONIC is a correct and strong invariant about the index structure. But `find_links()` is not a pure spanfilade query — it is a **V-spec → POOM → I-address → spanfilade** pipeline. Deletion breaks the first segment of that pipeline, stranding the permanent spanfilade entry unreachable from above. A link enumerated in window 1 can therefore vanish from window 2 if its endpoint content is deleted from all POOMs between calls, with no violation of the monotonicity invariant.

The specification must therefore model `find_links()` as returning a subset of links whose endpoint I-addresses currently have V-mappings in at least one POOM — not as returning all links ever indexed in the spanfilade. FC-SPANFILADE-MONOTONIC is a structural lower bound on the index, not a behavioral lower bound on query results.
