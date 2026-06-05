## Question 15 [evidence]

> Are the DEL5 unreferenced I-addresses (silently filtered during I→V conversion in retrieval) filtered before counting, or does the count include links that would resolve to empty endsets?

## KB Synthesis

The count is NOT filtered. It includes links that would resolve to empty endsets.

**The two operations are at different abstraction levels:**

FINDNUMOFLINKSFROMTOTHREE works by calling `findlinksfromtothreesp()` — a pure I-address intersection against the spanfilade — then linearly counting the resulting list [SS-PAGINATE-LINKS]. The spanfilade is write-only and never pruned [INV-SPANF-WRITE-ONLY], so stale entries from deleted content remain indexed and participate in the count.

DEL5 filtering (silent I→V exclusion) only fires during endpoint *retrieval* — specifically inside `span2spanset()` → `retrieverestricted()` when converting I-addresses back to V-addresses via a document's POOM [INV-ITOV-FILTERING]. FINDNUMOFLINKSFROMTOTHREE never performs this I→V step; it stops at the spanfilade match.

**Consequence:** A link whose endpoint I-addresses are unreferenced in any POOM (a "ghost link" [EC-GHOST-LINK]) will still be counted if the query specset's I-addresses intersect the link's stored I-addresses in the spanfilade. The same link, when subsequently followed via FOLLOWLINK, returns empty endset spans — but the count already included it.

The only way a link is *not* counted is if the query specset itself converts to empty I-addresses (e.g., the queried content was deleted from all POOMs, so the V→I step on the query side returns nothing) [PRE-FIND-LINKS, Finding 0029].

---

## Code Exploration

---

## Answer

### The Question Restated

DEL5 (EWD-030) defines an *unreferenced* I-address as one that exists in ispace but has no current POOM mapping in any document:

```
unreferenced(a) ≡ a ∈ dom.ispace ∧ ¬(∃d, v : poom.d(v) = a)
```

DEL5(f) adds: link endsets in the spanfilade may contain such addresses — "ghost links". The question is whether FINDNUMOFLINKS counts these before or after the I→V filtering that happens in FOLLOWLINK.

---

### The Count Comes BEFORE the Filter

**`findnumoflinksfromtothreesp` at `backend/spanf1.c:105–115`:**

```c
bool findnumoflinksfromtothreesp(...)
{
  typelinkset linkset;
  INT n;

  if (!findlinksfromtothreesp (..., &linkset))
      return(FALSE);
  for (n = 0; linkset; linkset = linkset->next, ++n);   // [spanf1.c:112]
  *numptr = n;
  return (TRUE);
}
```

This is a raw traversal of the linkset returned by `findlinksfromtothreesp`. There is no POOM check, no I→V conversion, no liveness test on the found link ISAs.

---

### How Links Are Found: The Spanfilade Is Never Cleaned

`findlinksfromtothreesp` (`spanf1.c:56–103`) works as follows:

1. Convert the *query* V-specsets to I-sporglsets via `specset2sporglset` → `vspanset2sporglset` → `ispan2vspanset` (V→I on the query side only).
2. Call `sporglset2linksetinrange` (`sporgl.c:239–269`) to search the spanfilade for links whose endset I-spans overlap the query I-spans.
3. Extract link ISAs from the ORGLRANGE dimension via `beheadtumbler` [`sporgl.c:264`] and add to linkset via `onlinklist`.

At step 2, `retrieverestricted` matches purely on I-span overlap — it has no mechanism to check whether the *link's* endset I-addresses are currently referenced in any POOM:

```c
// sporgl.c:259
context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE,
                               &range, ORGLRANGE, (typeisa*)infoptr);
```

Critically, the `infoptr` path that was intended to filter by homedoc is dead code — note the explicit `FALSE` guard in `sporglset2linksetinrange` at `sporgl.c:251`:

```c
if (FALSE/*trying to kluge links followable thru versions */
    && ((typeitemheader *)sporglset)->itemid == SPORGLID) {
    infoptr = &linfo;
    ...
} else
    infoptr = NULL;   // always takes this branch
```

And the spanfilade is write-only. From Finding 0057 (confirmed by code inspection of `backend/spanf1.c` and `backend/spanf2.c`): **no `deletespanf` function exists**. When `dodeletevspan` (`do1.c:162–171`) removes a V→I mapping from the POOM via `deletend`, it makes no corresponding call to remove the I-address→link entry from the spanfilade. The same is true of link deletion (Finding 0024). So ghost-link entries accumulate indefinitely.

---

### The Filter Happens During FOLLOWLINK, Not Counting

The DEL5 filtering is at `orglinks.c:425–449`, inside `span2spanset`, which is only reached during I→V conversion when *following* a link:

```
dofollowlink (do1.c:223)
  -> link2sporglset (sporgl.c:67)      — extract I-addresses from link orgl
  -> linksporglset2specset (sporgl.c:97)
       -> sporglset2vspanset (sporgl.c:141)
            -> ispan2vspanset (orglinks.c:389)
                 -> permute -> span2spanset (orglinks.c:425)
                      -> retrieverestricted()  -- POOM lookup
                      if (!context) {
                          return(targspansetptr);  // [orglinks.c:446] silent drop
                      }
```

At `orglinks.c:446`, if the POOM has no entry for the I-address (because it's DEL5-unreferenced), `span2spanset` returns the current target pointer unchanged — zero V-spans are added. This is the silent filter. But **this code is never reached during `findnumoflinksfromtothreesp`** — the counting path does not call `ispan2vspanset` on the found links' endsets at all.

---

### Concrete Scenario

1. Content C at I-address `a` is in document D1's POOM at V-position 1.5; also transcluded into D2 at V-position 1.5.
2. Link L is created with TO-endset referencing C. The spanfilade records: I-span `a` → link L (LINKTOSPAN).
3. D2 deletes the transcluded content. `deletevspanpm` removes `poom.D2(1.5) = a`. The spanfilade entry for D2→`a` is NOT removed.
4. Query: `FINDNUMOFLINKS` with TO = D1's V-span 1.5.
   - V→I on D1's V-span 1.5 → I-span `a` (still in D1's POOM).
   - Spanfilade lookup: I-span `a` → finds L.
   - Count: **1**. L is counted.
5. Client calls `FOLLOWLINK(L, TO)`.
   - L's TO endset has I-span `a` in D2 (D2 is the "homedoc" from the sporgl).
   - D2's POOM has no entry for `a` (deleted).
   - `span2spanset` at `orglinks.c:446`: context is NULL → no V-span added.
   - Result: **[]** (empty), operation succeeds (`works: true`).

The count of 1 is correct that L exists. But the client following L sees an empty TO endset — the ghost-link filtering only kicks in at FOLLOWLINK time.

---

### Summary

| Operation | I→V Conversion on Link Endsets? | DEL5 Filter Applied? |
|-----------|--------------------------------|----------------------|
| `FINDNUMOFLINKS` (`findnumoflinksfromtothreesp`, `spanf1.c:105`) | No | **No — count is raw** |
| `FOLLOWLINK` (`dofollowlink`, `do1.c:223`) | Yes (via `ispan2vspanset`) | **Yes — at `orglinks.c:446`** |
| `RETRIEVEENDSETS` (`retrieveendsetsfromspanf`, `spanf1.c:190`) | Yes (via `linksporglset2specset`) | **Yes — same path** |

The count **includes links that would resolve to empty endsets**. The spanfilade is never cleaned (no `deletespanf` exists anywhere in the codebase), so ghost-link entries persist indefinitely. The only place DEL5 unreferenced addresses are silently dropped is during the I→V POOM lookup inside `span2spanset` at `orglinks.c:446`, which is on the FOLLOWLINK/RETRIEVEENDSETS path only — not the counting path.
