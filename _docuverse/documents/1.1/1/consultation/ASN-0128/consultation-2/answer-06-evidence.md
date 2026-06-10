## Question 6 [evidence]

> Does udanax-green contain any operation that transitively traverses link structures (following links-to-links to a closure or endpoint), or is every link query strictly single-step set intersection over endsets?

## KB Synthesis

Every link query in udanax-green is strictly single-step. The system contains no built-in transitive closure or link-chain traversal operation.

## What the operations actually do

**`find_links` (FINDLINKSFROMTOTHREE)** [SS-FIND-LINKS, PRE-FIND-LINKS] performs a single set-intersection pass: the query specset is converted to I-addresses, the spanfilade is searched for entries whose ORGLRANGE prefix matches, and the matching link ISAs are returned. The operation terminates after one pass — it does not re-query using the returned links as new input.

**`follow_link` / FOLLOWLINK** [SS-FOLLOWLINK, SS-FOLLOW-LINK] is a direct orgl lookup: given a link ID, retrieve the stored endset I-addresses, convert through the home document's POOM, and return the resulting specset. The postcondition is `follow_link(L, SOURCE) == L.source_specset` — it returns what was stored at link creation, nothing more.

**`retrieve_endsets` (RETRIEVEENDSETS)** [SS-RETRIEVE-ENDSETS] similarly performs a single spanfilade search by content identity, returning from/to/three endsets in one pass.

**`find_links` with pagination** [SS-PAGINATE-LINKS] re-executes the same single-pass search each call; pagination is cursor-based over one result set, not recursive traversal.

## Why no transitive traversal exists

The architecture makes this clear. The backend is a single-threaded run-to-completion event loop [INV-ATOMICITY, INV-SEQUENTIAL-DISPATCH] — each FEBE request executes atomically and returns. There is no opcode with a "depth" or "hops" parameter in the request dispatch table. The only mechanism for multi-hop traversal is client-side: the caller applies `follow_link` to the results of `find_links`, then issues another `find_links` using the returned specset as a new query. This is explicitly documented as a caller-driven three-phase pattern: discover → follow → resolve [INT-LINK-FOLLOW-LIFECYCLE].

[EC-LINK-TOPOLOGY] confirms the consequence — circular link topologies (`A → B → C → A`) do not cause infinite loops or errors in `find_links` because the operation never recurses into the graph it returns. It finds links whose endpoints intersect the query content identity; what those links themselves point to is irrelevant to the query.

## Summary

The link subsystem is a single-level index: `find_links(specset) = {L | endpoint_iaddrs(L) ∩ iaddrs(specset) ≠ ∅}` [SS-FIND-LINKS]. Any transitive closure over the link graph is application-layer responsibility, built by the client issuing repeated single-step queries.

---

## Code Exploration

The finding is drafted but not yet saved (permission denied). Here is my complete answer:

---

## Answer: Link Traversal in udanax-green Is Strictly Single-Step

After reading all relevant source code and tracing every execution path, I find **no transitive link traversal** anywhere in the backend. Every link query is a flat, single-step set intersection or a direct one-hop endpoint read.

---

### The complete protocol surface for links

`requests.h` defines exactly six link-related opcodes:

| Opcode | # | Operation |
|--------|---|-----------|
| `CREATELINK` | 27 | Store a link with three endsets |
| `FOLLOWLINK` | 18 | Read one endset of a named link |
| `RETRIEVEENDSETS` | 28 | Read all three endsets of a named link |
| `FINDLINKSFROMTOTHREE` | 30 | Find all links whose endsets intersect given specsets |
| `FINDNUMOFLINKSFROMTOTHREE` | 29 | Count variant |
| `FINDNEXTNLINKSFROMTOTHREE` | 31 | Paginated variant |

`NAVIGATEONHT` (opcode 9) is registered in `init.c:50` but its handler body in `fns.c:236-248` is entirely commented out — only an error call remains. It does not run.

---

### FOLLOWLINK — one hop, period

`fns.c:114-127` dispatches to `dofollowlink`. The full implementation at `do1.c:223-232`:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  bool link2sporglset(), linksporglset2specset();
    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset(taskptr, &((typesporgl *)sporglset)->sporgladdress,
                             sporglset, specsetptr, NOBERTREQUIRED));
}
```

`link2sporglset` at `sporgl.c:67-95` calls `findorgl` to open the link's enfilade, then `retrieverestricted` once over the V-position range corresponding to `whichend` (which is just a fixed coordinate: 1 = FROM, 2 = TO, 3 = THREE per `do2.c:169-183`). It walks the returned context list and builds a sporglset. No link-query function is called. No loop re-enters the lookup.

`linksporglset2specset` at `sporgl.c:97-123` converts each sporgl to a `typevspec` via `linksporglset2vspec` → `sporglset2vspanset` → `ispan2vspanset`. None of these call any link operation.

---

### FINDLINKSFROMTOTHREE — set intersection only

`do1.c:348-352` delegates to `findlinksfromtothreesp` in `spanf1.c:56-103`:

1. Convert each of the up-to-three input specsets to sporglsets via `specset2sporglset` (`sporgl.c:14-33`).
2. For each non-null constraint, call `sporglset2linkset` → `sporglset2linksetinrange` (`sporgl.c:239-269`). That function calls `retrieverestricted` on the spanfilade for the appropriate `ORGLRANGE` band (`LINKFROMSPAN`, `LINKTOSPAN`, or `LINKTHREESPAN`) and walks the context list to collect matching link ISAs — `sporgl.c:263-265`:
   ```c
   for (c = context; c; c = c->nextcontext) {
       beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
       onlinklist(taskptr, linksetptr, &linksa);
   }
   ```
3. Intersect up to three linksets with `intersectlinksets` at `spanf2.c:46-120` — a nested linear scan over ISA tumblers.

The result is a flat set of link ISAs. No link in that set is automatically followed. There is no second call to `findlinksfromtothreesp` or `dofollowlink` inside the function.

---

### RETRIEVEENDSETS — direct lookup, no chaining

`retrieveendsetsfromspanf` at `spanf1.c:190-235` calls `retrievesporglsetinrange` three times (once per endset band), then calls `linksporglset2specset` on each result. The returned specsets are raw content addresses. No link query is made on those addresses.

---

### No transitive wrapper exists anywhere

A grep across all 30 C source files for `transitive`, `closure`, `recursive`, and for any call to `dofollowlink` inside a loop finds nothing. The only callers of `dofollowlink` are `fns.c:123` (the top-level dispatch) and `fns.c:119` (the `bool` forward declaration). No backend function wraps `FOLLOWLINK` in iteration.

---

### Architectural conclusion

The split is architecturally intentional:

- Links are **first-class documents** stored as `LINKATOM` orgl nodes in the granfilade (`do1.c:207`, `do1.c:180`).
- Their endsets are stored as separate `LINKFROMSPAN` / `LINKTOSPAN` / `LINKTHREESPAN` bands in the spanfilade (`do2.c:116-128`, `spanf1.c:15-54`).
- All link *queries* are set-intersection operations over the spanfilade bands.
- All link *reads* are one-hop enfilade retrievals inside a named link orgl.

**Transitive closure is entirely a client responsibility.** Walking A→L1→B→L2→C requires the client to issue four separate protocol calls:
1. `FINDLINKSFROMTOTHREE` on A's specset → get {L1}
2. `FOLLOWLINK` on L1 with whichend=TO → get B's specset
3. `FINDLINKSFROMTOTHREE` on B's specset → get {L2}
4. `FOLLOWLINK` on L2 with whichend=TO → get C's specset

The backend never performs steps 2–4 as a consequence of step 1.
