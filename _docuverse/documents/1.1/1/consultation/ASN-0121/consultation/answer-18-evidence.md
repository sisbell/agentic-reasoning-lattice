## Question 18 [evidence]

> Given FC-SPANFILADE-MONOTONIC and EC-STALE-SPANFILADE, will FINDLINKSFROMTOTHREE return a link whose matching endset content has been DELETEd from every document's POOM, since no `deletespanf` removes the DOCISPAN entries?

## KB Synthesis

**No.** Despite the spanfilade being monotonic, FINDLINKSFROMTOTHREE cannot return such a link. Here is why the stale-spanfilade reasoning does not apply here.

## The two spanfilade sub-indexes differ in how they are queried

[EC-STALE-SPANF-REFERENCE] documents the DOCISPAN stale-reference problem: `FINDDOCSCONTAINING` accepts I-addresses directly as its input, so it hits the persistent DOCISPAN entries even after the content is gone from every POOM. The caller bypasses the POOM entirely.

FINDLINKSFROMTOTHREE has a different input pipeline [SS-FIND-LINKS, SS-SPANF-OPERATIONS]:

1. Caller supplies FROM/TO/THREE as **VSpecs** (document ID + V-position + width)
2. System converts V-specs → I-addresses via the querying document's current POOM (`specset2ispanset` → `permute`)
3. Those I-addresses are used to search the link-endset portion of the spanfilade

Step 2 is the bottleneck. If the link's endpoint I-addresses α have been deleted from **every** document's POOM, then no V-spec in any open document maps to α. There are no I-addresses to present to the spanfilade search. The permanent spanfilade entries `α → L` exist [INV-SPANF-WRITE-ONLY], but the query pipeline never reaches them.

## Confirmed by the deletion × discoverability matrix

[EC-ORPHANED-LINK] and [SS-FIND-LINKS] Finding 0029 both confirm this directly: once source content is deleted from all documents, `find_links()` → `[]`. The link "exists in the link enfilade and can be traversed via `follow_link()` (returning empty content), but it cannot be discovered via `find_links()` because no document contains content identities matching its endpoints."

The stale spanfilade entries mean the link is **permanently stored** — [INV-LINK-PERMANENCE] holds, and `follow_link(link_id, ...)` still succeeds if you already have the link ID. But content-based search via FINDLINKSFROMTOTHREE fails because the V-spec → POOM → I-address conversion produces nothing.

## Summary

| Query operation | Input | Goes through POOM? | Stale spanfilade reachable? |
|---|---|---|---|
| FINDDOCSCONTAINING | I-addresses directly | No | **Yes** |
| FINDLINKSFROMTOTHREE | V-specs (VSpec) | **Yes** | No |

The stale-spanfilade problem [EC-STALE-SPANF-REFERENCE] is real but asymmetric: it only surfaces through operations whose callers can supply I-addresses without a POOM lookup. FINDLINKSFROMTOTHREE forces every query through the POOM, so deleted content leaves the link permanently orphaned and undiscoverable by content-based search [EC-ORPHANED-LINK].

---

## Code Exploration

I now have all the code evidence needed. Let me compile the full answer.

---

## Answer

**Short answer:** The stated reasoning contains a category error. `FINDLINKSFROMTOTHREE` does not use DOCISPAN entries at all. Whether the link is returned depends entirely on *how the caller encodes the query*, not on whether DOCISPAN entries are stale.

---

## The Spanfilade Has Two Distinct Entry Families

`insertspanf` is called with a `spantype` argument that determines the orgl-dimension prefix of each crum. There are two completely separate families:

**Family 1 — Content-location index (DOCISPAN):**
- Written by: `docopy` at `do1.c:62` and `doinsert` (via `docopy`)
  ```c
  insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
  ```
- Meaning: "document D contains I-addresses X"
- Read by: `finddocscontainingsp` (`spanf1.c:151`) → **FIND_DOCUMENTS only**

**Family 2 — Link endpoint index (LINKFROMSPAN / LINKTOSPAN / LINKTHREESPAN):**
- Written by: `insertendsetsinspanf` at `do2.c:116-128`, called from `docreatelink` (`do1.c:219`)
  ```c
  insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
  insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)
  insertspanf(taskptr, spanfptr, linkisaptr, threesporglset,LINKTHREESPAN)
  ```
- Meaning: "link L has its FROM/TO/THREE endpoint overlapping I-addresses X"
- Read by: `sporglset2linkset` (`sporgl.c:222`) called from `findlinksfromtothreesp` → **FIND_LINKS only**

`findlinksfromtothreesp` calls `sporglset2linkset` with `spantype` = `LINKFROMSPAN`, `LINKTOSPAN`, or `LINKTHREESPAN` (`spanf1.c:77,85,93`). It never touches DOCISPAN entries. The stated reasoning — that stale DOCISPAN entries cause the link to be found — is a category error.

---

## The Actual Execution Path of `findlinksfromtothreesp`

```
findlinksfromtothreesp(taskptr, spanf, fromvspecset, ...) [spanf1.c:56]
  │
  ├─ specset2sporglset(taskptr, fromvspecset, &fromsporglset) [spanf1.c:71]
  │    │
  │    ├─ if ISPANID item: pass through unchanged              [sporgl.c:20-22]
  │    └─ if VSPECID item: vspanset2sporglset()                [sporgl.c:25]
  │           │
  │           ├─ findorgl(granf, docisa, &orgl)                [sporgl.c:44]
  │           └─ vspanset2ispanset(orgl, vspan, &ispanset)     [sporgl.c:48]
  │                 └─ [queries the POOM for V→I mappings]
  │
  ├─ sporglset2linkset(spanf, fromsporglset, &fromlinkset, LINKFROMSPAN) [spanf1.c:77]
  │    │
  │    ├─ override orglrange: always width=100                  [sporgl.c:227-233]
  │    └─ sporglset2linksetinrange()                            [sporgl.c:239]
  │           └─ retrieverestricted(spanf, sporglset, SPANRANGE, range, ORGLRANGE)
  │                 └─ [searches LINKFROMSPAN entries in spanfilade]
  │
  └─ intersectlinksets(fromlinkset, tolinkset, threelinkset, linksetptr) [spanf1.c:100]
```

---

## Case 1: Caller Provides V-Specsets (`VSPECID`)

If the caller encodes the search content as V-spans in a document:

1. `vspanset2sporglset` calls `vspanset2ispanset` on the document's POOM (`sporgl.c:48`)
2. The content has been DELETEd from every POOM — `deletevspanpm` removed all V→I entries via `deletend` (`orglinks.c:149`)
3. `vspanset2ispanset` returns an empty `ispanset` — no V→I mapping exists
4. `fromsporglset` is empty — no crum addresses to search against
5. `sporglset2linksetinrange` iterates over an empty `sporglset` loop (`sporgl.c:250`) — `fromlinkset = NULL`
6. Back at `spanf1.c:78-82`:
   ```c
   if (!fromlinkset) {
       *linksetptr = NULL;
       return (TRUE);
   }
   ```

**Result: The link is NOT returned.** The stale DOCISPAN entries are never consulted.

---

## Case 2: Caller Provides I-Spans Directly (`ISPANID`)

If the caller provides I-address spans directly (not routed through any POOM):

1. `specset2sporglset` hits the `ISPANID` branch and passes items through unchanged (`sporgl.c:20-22`)
2. `sporglset2linksetinrange` calls `retrieverestricted` on the spanfilade with the provided I-addresses and `LINKFROMSPAN` range
3. The LINKFROMSPAN entries written by `insertendsetsinspanf` at link-creation time are **never removed** — no `deletespanf` exists (`spanf1.c` and `spanf2.c` — confirmed in Finding 0057)
4. Those stale LINKFROMSPAN entries match the queried I-addresses
5. `retrieverestricted` returns the link's orgl address; `beheadtumbler` strips the orgl prefix yielding the link ISA (`sporgl.c:264`); `onlinklist` adds it to `fromlinkset`

**Result: The link IS returned** — but because of stale **LINKFROMSPAN** entries, not DOCISPAN entries.

---

## What FOLLOWLINK Returns for That Ghost Link

Even when the link is returned via Case 2, `dofollowlink` (`do1.c:223-232`) produces empty endsets:

```c
link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)  // reads link's orgl
linksporglset2specset(...)   // calls sporglset2vspanset → ispan2vspanset
```

`ispan2vspanset` looks up the I-addresses in the document's POOM. Since the content has been deleted from every POOM, the lookup returns nothing. The returned V-specset is empty or NULL. This is the behavior documented in **Finding 0048** — ghost links return empty/partial endsets after I→V conversion fails.

---

## Summary Table

| Query form | fromsporglset resolved? | DOCISPAN consulted? | LINKFROMSPAN consulted? | Link returned? |
|---|---|---|---|---|
| V-specset, content deleted from all POOMs | Empty (POOM lookup fails) | Never | Never | **No** |
| I-span directly | Passed through | Never | Yes (stale entries match) | **Yes** |

---

## Conclusion

**`FINDLINKSFROMTOTHREE` does not use DOCISPAN entries under any circumstances.** The stale DOCISPAN entries left by deleted content are read only by `finddocscontainingsp` (`FIND_DOCUMENTS`), a completely separate code path.

The correct invariant governing `FINDLINKSFROMTOTHREE` is: stale **LINKFROMSPAN/LINKTOSPAN** entries persist in the spanfilade because no `deletespanf` exists (`do2.c:116-128`, `spanf1.c` — no removal function). Whether the link is found depends on the query encoding:

- **V-specset query:** The POOM is the gating oracle. Content deleted from every POOM means no I-addresses are resolved — sporglset is empty — `fromlinkset = NULL` — link not returned. The stale DOCISPAN entries have zero effect here.
- **I-span direct query:** The POOM is bypassed. Stale LINKFROMSPAN entries match — link IS returned. But when subsequently followed, FOLLOWLINK returns empty endsets because `ispan2vspanset` finds no V→I mappings in any POOM.

This is precisely **EC-STALE-SPANFILADE**: consumers of spanfilade results may receive stale entries, but FOLLOWLINK filters unreferenced I-addresses during I→V conversion, producing empty endsets. The ghost link is discoverable if and only if the caller already possesses its endpoint I-addresses directly.
