## Question 17 [evidence]

> How does the reader detect exhaustion — does a final window return fewer than N links, an explicit terminal marker, or an empty window on the call after the last full one?

## KB Synthesis

From `[SS-PAGINATE-LINKS]`, the page-size parameter is **input/output**: the caller supplies the requested page size N; the operation returns the actual count in `*nptr`. Exhaustion manifests in two stages:

1. **Partial final window** — when fewer than N links remain after the cursor, the returned count is `< N`. This is the soft signal.

2. **Empty window** — when the cursor is the last link (or the list is fully exhausted), the scan finds the cursor, no items follow, and count=0 is returned. This is the hard termination signal.

There is no explicit terminal marker. The caller must observe `count < N` on the partial page, then `count = 0` on the subsequent call (with the last-returned link as cursor) to confirm exhaustion.

One complication noted in `[EC-CURSOR-INVALIDATION]`: `count = 0` is **ambiguous** — it also occurs when the cursor link no longer appears in the re-executed search (e.g., deleted between calls). The KB provides no way to distinguish normal exhaustion from cursor invalidation; both return TRUE with an empty result.

---

## Code Exploration

I now have everything needed to answer definitively. Here is my complete analysis:

---

## How the Reader Detects Exhaustion in Windowed Link Retrieval

### The Command

Command 31 (`FINDNEXTNLINKSFROMTOTHREE`, `requests.h:40`) is the windowed link reader. The non-windowed command 30 (`FINDLINKSFROMTOTHREE`) is what the Python client's `find_links` method actually uses — it reads all matching links in a single shot. **The Python client does not expose command 31 at all.**

### What the Backend Sends

`putfe.c:290-295`:
```c
int putfindnextnlinksfromtothree(typetask *taskptr, INT n, typelinkset nextlinkset)
{
    putnumber (taskptr->outp, FINDNEXTNLINKSFROMTOTHREE);   // echo code 31
    putitemset (taskptr, (typeitemset)nextlinkset);
}
```

**`n` is silently dropped.** Despite `n` being computed and passed to this function, the frontend wire encoder does not transmit it. Compare `put.c:190-193` (the text/debug version that *does* print `n`):
```c
fprintf(taskptr->outp, "next number of links: %d\n", n);
```
That line does not exist in `putfe.c`.

`putitemset` (`putfe.c:124-133`) sends:
1. A count `i` — the number of items in the linked list
2. Then `i` link addresses

So the only information the reader receives is: **command echo code 31**, then **item-count**, then **items**.

---

### The Algorithm

`spanf1.c:117-149` — `findnextnlinksfromtothreesp`:

```c
bool findnextnlinksfromtothreesp(..., typeisa *lastlinkisaptr, typelinkset *nextlinksetptr, INT *nptr)
{
  INT n = 0;
  typelinkset linkset;

  *nextlinksetptr = NULL;
  // Re-queries all matching links on every call
  if (!findlinksfromtothreesp (..., &linkset))
      return (FALSE);

  // Position: if lastlink is zero, start from the beginning
  if (iszerotumbler (lastlinkisaptr)) {
      *nextlinksetptr = linkset;                          // [spanf1.c:127]
  } else {
      // Scan forward to find lastlink, set nextlinksetptr to the node after it
      for (; linkset; linkset = linkset->next) {
          if (tumblereq (&linkset->address, lastlinkisaptr)) {
              *nextlinksetptr = linkset->next;            // [spanf1.c:131]
              break;
          }
      }
  }

  // If lastlink was not found, or nothing comes after it
  if (!linkset) {
      *nextlinksetptr = NULL;
      *nptr = 0;
      return (TRUE);                                      // [spanf1.c:136-140]
  }

  // Truncate: sever the list at N items
  for (linkset = *nextlinksetptr; linkset; linkset = linkset->next) {
      if (++n >= *nptr) {
          linkset->next = NULL;                           // [spanf1.c:143]
          break;
      }
  }
  *nptr = n;                                              // [spanf1.c:147]
  return (TRUE);
}
```

Key structural facts:
- The function **re-queries the full link set on every call** via `findlinksfromtothreesp` (`spanf1.c:124`). The `linkset->next = NULL` truncation only affects the temporary list for this call, not persistent state.
- Positioning is by **scanning for `lastlink` by tumbler equality**, then taking `linkset->next`.
- The truncation loop counts `n` up to `*nptr`; when `++n >= *nptr`, it severs and breaks.

---

### Exhaustion Detection: The Three Cases

Because `n` is not transmitted over the wire, the reader can only observe the item count from `putitemset`. Let's trace what that count is:

**Case 1 — Normal window (more links remain):**  
Say N=3, links are A→B→C→D→E.  
Truncation loop: n=1 (A), n=2 (B), n=3≥3 → sever, break.  
`*nptr = 3`, `putitemset` sends count=3.  
Reader sees **count == requested_N** → call again with lastlink=C.

**Case 2 — Short final window (fewer than N remain):**  
Second call, lastlink=C. Rebuilt list is A→B→C→D→E; positions to D.  
Truncation loop: n=1 (D), n=2 (E); E→next is NULL, loop terminates naturally.  
`*nptr = 2`, `putitemset` sends count=2.  
Reader sees **count < requested_N** → stop.

**Case 3 — Exactly-N final window (edge case):**  
Say N=3, links are exactly A→B→C.  
First call: n=3, sever at C (C→next was already NULL). `putitemset` sends count=3.  
Reader sees count=3 == N → must call again.  
Second call, lastlink=C: rebuilds A→B→C, scans to C, sets `*nextlinksetptr = C→next = NULL`.  
`if (!linkset)` at `spanf1.c:136`: `linkset` = C (found), condition is FALSE.  
Truncation loop: `linkset = *nextlinksetptr = NULL` → loop body never executes.  
`*nptr = 0`, `putitemset` sends count=0.  
Reader sees **count == 0 < requested_N** → stop.

---

### Summary

| Signal on the wire | Meaning |
|---|---|
| `count < requested_N` | Last batch (may be zero) — stop |
| `count == requested_N` | Window is full — call again with lastlink=last-received-link |
| `count == 0` | Exhausted — always stop |

**The exhaustion detection mechanism is: a final window returning fewer than N links.**

- There is **no explicit terminal marker** beyond the item count.
- The empty window (`count == 0`) is a special case of "fewer than N" and occurs when the total link count happens to be an exact multiple of N — the reader requires one extra probe call in that case.
- The Python client never exercises this code path. `find_links` (`client.py:749-758`) issues command 30, not 31, and reads all links atomically with `for i in range(self.xc.Number())`.
