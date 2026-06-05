## Question 14 [evidence]

> Because the spanfilade is write-only with no `deletespanf`, does the count include links whose endpoint content has been deleted from all POOMs — i.e., are ghost/orphaned links counted?

## KB Synthesis

**No — orphaned/ghost links are not counted.**

The count goes through the same path as `FINDLINKSFROMTOTHREE` [SS-FIND-LINKS, Finding 0035]: query V-spans → convert to I-addresses via the **current POOM state** → search the spanfilade for endpoint I-address intersection.

This is why deletion breaks discoverability even though the spanfilade is write-only. When a link's endpoint content has been deleted from all POOMs, the path breaks at the V→I conversion step: no current POOM maps any V-position to those I-addresses, so the query generates an empty (or non-overlapping) I-address set, and the spanfilade search finds no match. [EC-ORPHANED-LINK, Finding 0005] states this directly: fully deleted endpoint content means the link "cannot be discovered via `find_links()`."

The stale spanfilade entries **do** persist [INV-SPANF-WRITE-ONLY] — the link index entries for those orphaned I-addresses remain in the spanfilade forever. But they're unreachable through the normal query path, which anchors to live POOM content. The same asymmetry that makes `find_documents` over-report via stale DOCISPAN entries [EC-STALE-SPANF-REFERENCE] does *not* affect `find_links` in the same way, because `find_links` queries are initiated from the caller's current V-span content, not from the index directly.

The orphaned link remains accessible only via `follow_link(link_id)` — bypassing the spanfilade entirely and going directly to the link orgl by known ISA [INV-LINK-PERMANENCE, Finding 0029].

---

## Code Exploration

I now have everything needed for a complete, code-grounded answer.

---

## Answer: Do Ghost/Orphaned Links Get Counted?

**Short answer: It depends on which endpoint is deleted relative to the query direction. The spanfilade is provably write-only, but orphan links are not uniformly surfaced or suppressed — the behavior is asymmetric by design.**

---

### 1. The Spanfilade Is Write-Only — Confirmed

There is no `deletespanf` function anywhere in the codebase. Grep confirms zero matches. `spanf1.c` and `spanf2.c` expose only:

- `insertspanf` — adds entries [`spanf1.c:15`]
- `findlinksfromtothreesp`, `findnumoflinksfromtothreesp`, `retrieveendsetsfromspanf`, `finddocscontainingsp` — query-only

No removal mechanism exists.

---

### 2. `dodeletevspan` Never Touches the Spanfilade

`do1.c:158–167`:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    /*&& TRUE*/ /* ht stuff */ );
}
```

`orglinks.c:145–152`:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` operates only on `docorgl`, the document's POOM in `granf`. The spanfilade (`spanf`) is not touched. The V→I mapping vanishes from the POOM; the I-address→link-ISA entry in the spanfilade persists forever.

---

### 3. The Count Path: POOM Consulted for Query Input, Not for Found Links

The call chain for `findnumoflinksfromtothreesp` is:

```
fns.c:findnumoflinksfromtothree()
  → do1.c:dofindnumoflinksfromtothree()                         [do1.c:355–359]
    → spanf1.c:findnumoflinksfromtothreesp()                    [spanf1.c:105–115]
      → spanf1.c:findlinksfromtothreesp()                       [spanf1.c:56–103]
        → sporgl.c:specset2sporglset() [POOM lookup on QUERY]   [sporgl.c:14–33]
        → sporgl.c:sporglset2linkset()                          [sporgl.c:222–237]
          → sporgl.c:sporglset2linksetinrange()                 [sporgl.c:239–269]
            → retrie.c:retrieverestricted() [on spanf only]
            → beheadtumbler → onlinklist → link ISA in count
```

`sporglset2linksetinrange` at `sporgl.c:239–269`:
```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                              &range, ORGLRANGE, (typeisa*)infoptr);
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
    onlinklist(taskptr, linksetptr, &linksa);  // just adds to count
}
```

The POOM is only consulted when translating the **query's V-address specset** into I-address sporgls (`vspanset2sporglset` → `vspanset2ispanset` → `permute` → `retrieverestricted` on the POOM). Once a link ISA is extracted from the spanfilade, it is added to the linkset and counted **with no cross-validation against any POOM**.

---

### 4. The Critical Asymmetry

**Case A — Content deleted from all POOMs, and you query FROM that deleted content:**

- `specset2sporglset` → `vspanset2sporglset` → `vspanset2ispanset` → POOM returns no I-addresses → empty sporglset
- `sporglset2linkset` is called with empty input → `fromlinkset = NULL`
- `findlinksfromtothreesp` hits the early exit at `spanf1.c:78–82`:
  ```c
  if (fromvspecset) {
      sporglset2linkset(taskptr, spanfptr, fromsporglset, &fromlinkset, ...);
      if (!fromlinkset) { *linksetptr = NULL; return TRUE; }  // exits
  }
  ```
- **Count = 0.** Ghost links are not surfaced — but only because the query itself fails to resolve, not because the links were removed.

**Case B — You query FROM a live endpoint, and the link's OTHER endpoint content has been deleted from all POOMs:**

- `specset2sporglset` on the live specset succeeds → I-address range for live content
- `sporglset2linksetinrange` queries spanfilade for link ISAs at that I-address range
- Spanfilade still has entries for links whose FROM (or TO) endpoint covers that I-address (written at link creation, never deleted)
- Link ISA is extracted and added to linkset via `beheadtumbler` + `onlinklist`
- **Count includes that link.** The fact that the link's other endpoint content has vanished from all POOMs is invisible to the counting function.

**Case C — Direct I-span query (bypasses POOM entirely):**

`specset2sporglset` in `sporgl.c:19–22`:
```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *sporglsetptr = (typesporglset)specset;  // no POOM lookup
```

Any caller passing a raw `ISPANID` rather than a `VSPECID` bypasses the POOM entirely. Ghost links whose I-address is known directly ARE found and counted.

---

### 5. `intersectlinksets` — All-NULL Behavior

`spanf2.c:63–71`:
```c
if (linkset1 && !linkset2 && !linkset3)      *linkset4ptr = linkset1;
else if (!linkset1 && linkset2 && !linkset3) *linkset4ptr = linkset2;
else if (!linkset1 && !linkset2 && linkset3) *linkset4ptr = linkset3;
else                                          *linkset4ptr = NULL;
```

If all three specsets are NULL (or yield empty linksets), `intersectlinksets` returns NULL. This means completely orphaned links — where every endpoint has been deleted from all POOMs and no live content can be used to query from — are unreachable via V-spec queries.

---

### 6. Direct Confirmation: `findlinksfromtothree` Discards the Homeset

`fns.c:198`:
```c
dofindlinksfromtothree(taskptr, fromvspecset, tovspecset, threevspecset,
                        (typeispan*)NULL/*homeset*/, &linkset)
```

The homeset parameter — which would restrict the ORGL range searched — is hardcoded to `NULL`. This means even the range-restriction mechanism is inactive.

---

### Verdict

**The spanfilade is write-only. Ghost/orphaned links accumulate indefinitely. Whether they appear in the count depends entirely on the query direction:**

| Deleted endpoint role | Query form | Ghost link counted? |
|---|---|---|
| **FROM** endpoint deleted from all POOMs | V-spec FROM query | No — query fails to produce sporgls |
| **TO** endpoint deleted from all POOMs | V-spec FROM live content | **Yes** — spanfilade returns link ISA, no POOM cross-check |
| **FROM** endpoint deleted from all POOMs | Direct I-span query | **Yes** — POOM bypassed |
| All endpoints deleted from all POOMs | Any V-spec query | No — no live content to query from |
| All endpoints deleted from all POOMs | Direct I-span query | **Yes** — spanfilade entries persist |

The spanfilade acts as a **permanent historical journal** of which I-addresses a link was ever associated with, not a current index of live links. The only natural filter is the POOM lookup on the *query input* side. The *found* link ISAs are never validated. `dodeletevspan` [`do1.c:158–167`] and `deletevspanpm` [`orglinks.c:145–152`] leave the spanfilade entirely untouched. There is no `deletespanf` anywhere in the codebase.
