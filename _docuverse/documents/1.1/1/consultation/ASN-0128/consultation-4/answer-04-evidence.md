## Question 4 [evidence]

> When udanax-green answers a link-discovery query (e.g., find-links with from-set and to-set patterns), does it match the from-side and to-side arguments symmetrically by span/I-address intersection, or does either side require exact-address (rather than containment) matching?

## KB Synthesis

## Link Discovery: Symmetric Intersection on Both Sides

The matching is **symmetric non-empty I-address intersection** on both the from-side and to-side. Neither side requires exact-address matching; partial overlap (even a single shared I-address) is sufficient for each side independently.

### The Core Mechanism

[SS-FIND-LINKS] (Finding 0028) states the postcondition directly:

> `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`

Partial overlap explicitly suffices. A search specset sharing even one I-address with a link endpoint discovers that link.

The same intersection semantics apply to the to-side. [SS-LINK-ENDPOINT] (Finding 0005) confirms:

> `find_links(NOSPECS, specset) = {link | content_ids(link.target) ∩ content_ids(specset) ≠ ∅}`

Both sides are structurally identical — non-empty intersection against the stored I-spans of the respective endpoint.

### The AND Combination

When both from and to specs are provided, [SS-FIND-LINKS] (Finding 0029) specifies AND semantics:

> `find_links(source_spec, target_spec) ≡ find_links(source_spec) ∩ find_links(target_spec)`

Each side is evaluated independently by intersection, then the results are intersected. There is no asymmetry between the from and to evaluation paths.

### Implementation Confirmation

[SS-RETRIEVE-ENDSETS] (Finding 0035) explains the spanfilade search structure: the three endpoint types (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3) are separate ORGLRANGE prefixes in the spanfilade, but the actual matching within each type uses the same SPANRANGE restriction — an I-address range query. Both sides go through the same `retrievesporglsetinrange()` path, parameterized only by the ORGLRANGE prefix distinguishing from vs to.

[INT-SPORGL-LINK-INDEX] (Finding 0013) confirms that at link creation time, endpoint I-address ranges are inserted into the spanfilade indexed by content I-address. The stored granularity is I-span (contiguous range), not individual addresses, so the retrieval is range-overlap, not point-exact.

### One Practical Asymmetry to Note

[PRE-FIND-LINKS] (Finding 0069) documents that the orgl-dimension filter (which would scope results to a specific home document) is effectively disabled by a `TRUE||` dead-code guard. This means both sides are searched globally across all documents — the only effective filter is the I-address intersection in the span dimension. This applies equally to from and to sides.

### Summary

Both from and to arguments use **non-empty I-address intersection** — containment/overlap, not exact match. The AND combination `find_links(from, to, three)` requires each provided side to independently satisfy its intersection predicate. No side has stricter (exact-address) requirements than the other.

---

## Code Exploration

I now have the complete picture. Here is the full answer.

---

## Link-Discovery Matching: Symmetric Span Intersection on Both Sides

### Execution Path

**1. Entry: `fns.c:189` — `findlinksfromtothree`**

```c
void findlinksfromtothree(typetask *taskptr)
{
  typespecset fromvspecset, tovspecset, threevspecset;
  typeispanset homeset;
  typelinkset linkset;
  ...
  if (
     getfindlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
  && dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset,
                              (typeispan*)NULL/*homeset*/, &linkset))
      putfindlinksfromtothree (taskptr, linkset);
```

Note: `homeset` is decoded but **immediately discarded** — the `NULL` comment reveals it was a known stub. The orgl-range restriction filter is not active.

**2. Dispatch: `do1.c:348` — `dofindlinksfromtothree`**

```c
bool dofindlinksfromtothree(..., typeispan *orglrangeptr, typelinkset *linksetptr)
{
  return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset,
                                 threevspecset, orglrangeptr, linksetptr);
}
```

**3. Core: `spanf1.c:56` — `findlinksfromtothreesp`**

```c
// Convert each V-specset to a sporglset (V→I address mapping)
if (fromvspecset)
    specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (tovspecset)
    specset2sporglset (taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);
if (threevspecset)
    specset2sporglset (taskptr, threevspecset, &threesporglset, NOBERTREQUIRED);

// Search spanfilade for each endpoint type independently
if (fromvspecset) {
    sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset,
                       orglrange, LINKFROMSPAN);
    if (!fromlinkset) { *linksetptr = NULL; return (TRUE); }   // short-circuit
}
if (tovspecset) {
    sporglset2linkset (taskptr, (typecuc*)spanfptr, tosporglset, &tolinkset,
                       orglrange, LINKTOSPAN);
    if (!tolinkset) { *linksetptr = NULL; return (TRUE); }     // short-circuit
}
if (threevspecset) {
    sporglset2linkset (taskptr, (typecuc*)spanfptr, threesporglset, &threelinkset,
                       orglrange, LINKTHREESPAN);
    if (!threelinkset) { *linksetptr = NULL; return (TRUE); }
}

// Intersect by link identity
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

`LINKFROMSPAN = 1`, `LINKTOSPAN = 2`, `LINKTHREESPAN = 3` [`xanadu.h:36-38`]. The two sides are passed through **the exact same code**, distinguished only by the `spantype` constant.

**4. Spanfilade search: `sporgl.c:239` — `sporglset2linksetinrange`**

```c
for (; sporglset; ...) {
    prefixtumbler(&orglrange->stream, spantype, &range.stream);
    prefixtumbler (&orglrange->width, 0, &range.width);
    context = retrieverestricted (spanfptr,
                                  (typespan*)sporglset, SPANRANGE,   // ← query span
                                  &range, ORGLRANGE,                 // ← link-type filter
                                  (typeisa*)infoptr);
    for (c = context; c; c = c->nextcontext) {
        beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
        onlinklist (taskptr, linksetptr, &linksa);
    }
}
```

The cast `(typespan*)sporglset` works because `typesporgl.sporglorigin` and `typesporgl.sporglwidth` align structurally with `typespan.stream` and `typespan.width` [`xanadu.h:65-70` and `xanadu.h:115-121`]:

```c
typedef struct structtypespan {
    struct structtypespan *next; typeitemid itemid;
    tumbler stream; tumbler width;           // ← aligns with
} typespan;

typedef struct structsporgl {
    struct structsporgl *next; typeitemid itemid;
    tumbler sporglorigin; tumbler sporglwidth; typeisa sporgladdress;
} typesporgl;
```

So the query is: "find all crums in the spanfilade whose SPANRANGE (stored I-address) overlaps [sporglorigin, sporglorigin+sporglwidth)."

**5. The matching predicate: `retrie.c:270` — `crumqualifies2d`**

This is the decisive function. For a stored endpoint crum occupying SPANRANGE interval [L, R):

```c
// Where does query-end fall relative to [L, R)?
endcmp = iszerotumbler (span1end) ? TOMYRIGHT
                                  : whereoncrum (crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER)        // span1end <= L → query ends before crum starts
    return (FALSE);

// Where does query-start fall relative to [L, R)?
startcmp = whereoncrum (crumptr, offset, span1start, index1);
if (startcmp > THRUME)               // span1start >= R → query starts after crum ends
    return (FALSE);

return (TRUE);
```

Position constants [`common.h:86-90`]:
```c
#define TOMYLEFT         -2
#define ONMYLEFTBORDER   -1
#define THRUME            0
#define ONMYRIGHTBORDER   1
#define TOMYRIGHT         2
```

For a query I-span [A, B) and stored endpoint I-span [L, R):

| Condition | Meaning | Decision |
|-----------|---------|----------|
| `B ≤ L` (`endcmp ≤ ONMYLEFTBORDER`) | Query ends before stored span starts | Reject |
| `A ≥ R` (`startcmp > THRUME`, i.e., ≥ ONMYRIGHTBORDER) | Query starts at or after stored span ends | Reject |
| Otherwise | Intervals overlap | Accept |

This is the **standard half-open interval intersection test**: accept iff `A < R AND B > L`, equivalently `[A,B) ∩ [L,R) ≠ ∅`.

This same function qualifies both internal nodes (for pruning) and leaf nodes (for inclusion). At the leaf, the crum's extent is exactly the stored endpoint span. **A partial overlap suffices — neither containment nor exact equality is required.**

**6. Final intersection: `spanf2.c:46` — `intersectlinksets`**

After three independent I-span intersection searches produce `fromlinkset`, `tolinkset`, `threelinkset`, they are combined by **exact tumbler equality on the link ISA**:

```c
for (; temp1; temp1 = temp1->next) {
    for (temp2 = linkset2; temp2; temp2 = temp2->next) {
        if (tumblereq (&temp1->address, &temp2->address)) {  // exact match on link identity
            linkset4 = makelinkitem (taskptr, &temp1->address);
            ...
        }
    }
}
```

There is one special case [`spanf2.c:64-69`]: if exactly one endpoint list is non-null (i.e., only from, or only to, or only three is specified), that list is returned directly without any intersection. The "intersection" of one set with nothing is the set itself.

---

## Answer

**Matching is symmetric and intersection-based on both sides.** The from-side and to-side are handled by exactly the same code path (`sporglset2linksetinrange` → `retrieverestricted` → `findcbcinarea2d` → `crumqualifies2d`). The distinguishing argument is only `LINKFROMSPAN` vs `LINKTOSPAN` [`xanadu.h:36-37`], which selects a prefix in the ORGLRANGE dimension of the spanfilade — the actual matching logic over I-address spans is byte-for-byte identical.

A link qualifies for an endpoint query iff the I-address span stored for that endpoint **intersects** (overlaps at all) with the I-address span derived from the query's V-span. The predicate is `[A,B) ∩ [L,R) ≠ ∅` [`retrie.c:282-299`]. Exact equality is one case of intersection, as is containment in either direction, but partial overlap also matches.

Neither side requires exact-address matching. There is no asymmetry between from and to in the matching rule. The only asymmetry in the entire path is the `(typeispan*)NULL/*homeset*/` at `fns.c:198`, which discards the caller-supplied orgl-range restriction and leaves all links in the spanfilade as candidates regardless of their home document.
