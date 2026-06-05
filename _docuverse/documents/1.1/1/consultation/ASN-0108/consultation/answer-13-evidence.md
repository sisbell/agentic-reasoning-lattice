## Question 13 [evidence]

> Since `findlinksfromtothreesp` performs full materialization into a transient list before truncating, is the complete result list rebuilt from the spanfilade on every windowed call, or is any state retained across calls?

## KB Synthesis

The complete result list is rebuilt from the spanfilade on every windowed call. No state is retained across calls.

[SS-PAGINATE-LINKS] (Finding 0035) is explicit on this point:

> FINDNEXTNLINKSFROMTOTHREE implements **stateless cursor-based pagination**. On each call it: (1) **re-executes the full `findlinksfromtothreesp()` search**, (2) linearly scans the materialized list for the cursor tumbler, (3) truncates at N items.

The code path is `findnextnlinksfromtothreesp()` at `backend/spanf1.c:117-149`. Every invocation re-traverses the spanfilade from scratch, materializes the full matching list as a transient linked list, walks it to find the cursor position, then truncates. No server-side cursor object, no cached list, no generation counter.

The postcondition is: `result = take(N, dropUntilAfter(cursor, fullSearchResult))` where `fullSearchResult` is identical to what a concurrent FINDLINKSFROMTOTHREE call would return at that instant.

The consequence (also noted in [EC-CURSOR-INVALIDATION]): if a link is created or its endpoint content changes between two paginated calls, the rebuilt list differs, and a cursor pointing to a now-absent link returns empty rather than an error.

---

## Code Exploration

I now have the complete picture from the source. Here is the full answer:

---

## Answer: Full Rematerialization on Every Windowed Call — No State Retained

### The Call Chain

The FEBE `FINDNEXTNLINKSFROMTOTHREE` request dispatches through:

```
fns.c:219  findnextnlinksfromtothree (FEBE handler)
  → fns.c:230  dofindnextnlinksfromtothree
    → do1.c:366  findnextnlinksfromtothreesp
      → spanf1.c:124  findlinksfromtothreesp   ← full rebuild here
```

### What `findlinksfromtothreesp` Does (spanf1.c:56–103)

Every call unconditionally:

1. Converts each non-null specset to a `sporglset` via `specset2sporglset` [`spanf1.c:71–75`]
2. Calls `sporglset2linkset` for each endpoint role (FROM/TO/THREE) [`spanf1.c:77, 85, 93`], which calls `sporglset2linksetinrange` [`sporgl.c:235`], which calls `retrieverestricted` on the spanfilade tree for **every sporgl in the set** [`sporgl.c:259–261`], walking the enfilade and calling `onlinklist` to append results into a fresh heap-allocated linked list [`sporgl.c:263–266`]
3. Calls `intersectlinksets` to build the final materialized result list [`spanf1.c:100`]

There is no cursor, no saved position, no lazy enumeration. The result is a fully-materialized, heap-allocated linked list constructed entirely from scratch.

### What `findnextnlinksfromtothreesp` Does (spanf1.c:117–149)

This is the windowed call. It:

```c
// spanf1.c:124 — complete rebuild, unconditionally
if (!findlinksfromtothreesp (taskptr, spanf, fromvspecset, tovspecset, threevspecset, orglrangeptr, &linkset))
    return (FALSE);
```

Then implements pagination entirely in the caller by **linearly scanning the rebuilt list**:

```c
// spanf1.c:126–134 — find resume point by scanning from the head
if (iszerotumbler (lastlinkisaptr)) {
    *nextlinksetptr = linkset;          // first page: start at head
} else {
    for (; linkset; linkset = linkset->next) {
        if (tumblereq (&linkset->address, lastlinkisaptr)) {
            *nextlinksetptr = linkset->next;  // resume after last-seen
            break;
        }
    }
}
```

Then truncates by mutating the list in-place:

```c
// spanf1.c:141–146 — destructively truncate at window boundary
for (linkset = *nextlinksetptr; linkset; linkset = linkset->next) {
    if (++n >= *nptr) {
        linkset->next = NULL;   // truncate here
        break;
    }
}
```

### The Windowing Mechanism

The only state that persists across calls is the **`lastlinkisa` tumbler**, which is passed by the client in the FEBE request — it is the address of the last link returned in the previous window. There is no server-side cursor object, no task-scoped iterator, and no cached list between requests.

On each windowed call:

| Step | What happens |
|------|-------------|
| 1 | Spanfilade traversal: `retrieverestricted` called for each sporgl — fresh enfilade walk |
| 2 | `onlinklist` builds a new heap list of all matching link addresses |
| 3 | `intersectlinksets` builds the full intersection from scratch |
| 4 | The full list is scanned linearly from the head to find `lastlinkisa` |
| 5 | The next `n` items are returned; the list is truncated and the rest discarded |

### Conclusion

**The complete result list is rebuilt from the spanfilade on every windowed call.** No state whatsoever is retained across calls. The pagination is entirely client-driven via the `lastlinkisa` cursor tumbler, and every call pays the full cost of spanfilade traversal, `retrieverestricted` for all sporgls, list construction, intersection, and a linear scan to the resume point. For large result sets with many windows, this means O(N × W) total work where N is the full result count and W is the number of windows — the early pages are re-traversed and discarded on every subsequent call.
