## Question 1 [evidence]

> Does udanax-green's link query (findlinks/findlinksfromto) match the from-set by coverage/intersection rather than exact endset value, and does it answer reverse-direction (to-set-keyed) queries for every link type without any per-type opt-in?

## KB Synthesis

## Link Query: Intersection Matching and Reverse-Direction Queries

### 1. Intersection (not exact match) for the from-set

Yes, confirmed. The find_links mechanism is purely I-address set intersection, not exact endset comparison.

[SS-FIND-LINKS Finding 0028] states the postcondition explicitly:

> `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`

**Partial overlap is sufficient** — a search specset sharing even one I-address with a link endpoint discovers the link. The canonical example: a document containing only "link" (4 chars, I-addresses I.5–I.6) discovers a link whose source endpoint was "hyperlink text" (14 chars, I-addresses I.4–I.17). The intersection `{I.5, I.6}` is non-empty, so the link is returned. [SS-FOLLOW-LINK Finding 0028] confirms `follow_link` then returns the **full** original 14-char source, not the 4-char discovery fragment — the query is intersection-based but the link itself is immutable.

This holds because link endpoints are stored as I-spans in the spanfilade index, and `findlinksfromtothreesp` queries by I-address range restriction [SS-SPANF-OPERATIONS Finding 0012]. There is no mechanism for exact-match-only filtering.

### 2. Reverse-direction (to-set-keyed) queries without per-type opt-in

Yes. Both from and to endpoints are indexed symmetrically in the spanfilade with no per-link-type configuration.

[SS-LINK-ENDPOINT Finding 0005] is the direct evidence: `find_links(NOSPECS, target_specs)` finds links by target content identity, and the test `find_links_by_target` passes. The finding states: "Both endpoints participate symmetrically in discovery."

The underlying mechanism ([SS-RETRIEVE-ENDSETS Finding 0035], [INT-SPORGL-LINK-INDEX Finding 0035]) uses three independent ORGLRANGE subspace prefixes in the spanfilade:

| Constant | Value | Endpoint |
|----------|-------|----------|
| `LINKFROMSPAN` | 1 | from (source) |
| `LINKTOSPAN` | 2 | to (target) |
| `LINKTHREESPAN` | 3 | three (type reference) |

All three are inserted unconditionally at link creation time via `insertendsetsinspanf()` [ST-CREATE-LINK Finding 0012]. There is no per-link-type opt-in — every created link has all three endpoints indexed.

[SS-FIND-LINKS Finding 0029] provides the full behavioral matrix confirming asymmetric deletion effects on directional discoverability:

| Source State | Target State | Search by Source | Search by Target |
|---|---|---|---|
| Intact | Intact | Found | Found |
| Deleted | Intact | Not found | Found |
| Intact | Deleted | Found | Not found |

The AND semantics for multi-criterion search also hold: `find_links(source_spec, target_spec)` ≡ `find_links(source_spec) ∩ find_links(NOSPECS, target_spec)`.

### Caveat: the "three" (type) endpoint as a *filter* is broken

While all three endpoints are indexed uniformly, using the three-endpoint as a *query filter* — `find_links(source, NOSPECS, type_spec)` — returns empty results even when matching links exist [EC-TYPE-FILTER-NONFUNCTIONAL Finding 0029]. This is a separate bug from the indexing mechanism, likely in the `LINKTHREESPAN` query path. The indexing is symmetric; the type-as-filter query is not functional.

Additionally, [EC-FIND-LINKS-GLOBAL Finding 0069] notes the orgl-range (document scoping) parameter is silently discarded due to a `TRUE||!homeset` guard, making all queries effectively global across the entire orgl address space — reinforcing that there is no per-type scoping that would restrict which links are found.

---

## Code Exploration

The finding file wasn't written (no permission granted), but the full answer is below.

---

## Answer: Link Query Matching Semantics in udanax-green

### Question 1: Does `findlinks`/`findlinksfromto` match the from-set by intersection rather than exact endset value?

**Yes — the matching is intersection-based throughout. Exact endset equality is never tested.**

#### The Call Chain

```
fns.c:189        findlinksfromtothree()
do1.c:348        dofindlinksfromtothree()
spanf1.c:56      findlinksfromtothreesp()
sporgl.c:222     sporglset2linkset()
sporgl.c:239     sporglset2linksetinrange()
retrie.c:56      retrieverestricted()
retrie.c:87      retrieveinarea()
retrie.c:229     findcbcinarea2d()
retrie.c:270     crumqualifies2d()        ← overlap test here
```

#### The Overlap Test

`crumqualifies2d` [`retrie.c:270–305`] is the gate every stored span must pass. For the SPANRANGE dimension (where content spans live):

```c
endcmp = iszerotumbler(span1end) ? TOMYRIGHT :
         whereoncrum(crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER)      // query end falls at or before crum start → skip
    return(FALSE);

startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME)             // query start falls after crum end → skip
    return(FALSE);
```

`ONMYLEFTBORDER` is the left-touch position; `THRUME` is the right-interior position. The crum qualifies if and only if the two intervals share any point. This is the classic overlap predicate: **query_end > crum_start AND query_start ≤ crum_end**.

**It is not an equality test.** A link stored on I-span [A, B] is found by query span [B−ε, C], as long as they share one I-address.

#### How the Query Reaches That Code

`sporglset2linksetinrange` [`sporgl.c:239–269`] calls:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                              &range, ORGLRANGE, (typeisa*)infoptr);
```

The query sporgl (the content region to search) is passed as the **SPANRANGE** target. `retrieverestricted` [`retrie.c:56–85`] computes `(span1start, span1end)` from the sporgl's `stream` and `stream+width`, then sends both into `findcbcinarea2d`, which descends the 2D enfilade calling `crumqualifies2d` on every node.

The consequence: querying with a specset covering any part of a content region finds all links whose stored endspan shares even a single I-address with that region. The match is "touches or overlaps," not "equals" or "is contained by."

---

### Question 2: Does the system answer reverse-direction (to-set-keyed) queries for every link type without per-type opt-in?

**Yes — reverse queries are native, uniform, and require no per-type opt-in. There are no link types in the relevant sense.**

#### How the Spanfilade Stores Endsets

`insertendsetsinspanf` [`do2.c:116–128`] calls `insertspanf` once per endset:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // do2.c:119
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)     // do2.c:120
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN) // do2.c:123
```

The constants (`xanadu.h:36–38`):

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
```

Inside `insertspanf` [`spanf1.c:22`]:

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

The link's ISA is prefixed with the integer span-type and stored as the **ORGLRANGE** coordinate of a 2D crum. The content span is stored as the **SPANRANGE** coordinate. All three endsets from every link live in the **same** 2D spanfilade, separated only by the leading digit of their ORGLRANGE key.

#### How the Query Works for Any End

`findlinksfromtothreesp` [`spanf1.c:56–103`]:

```c
if (fromvspecset)
    sporglset2linkset(taskptr, spanfptr, fromsporglset,
                      &fromlinkset, orglrange, LINKFROMSPAN);   // spanf1.c:77
if (tovspecset)
    sporglset2linkset(taskptr, spanfptr, tosporglset,
                      &tolinkset, orglrange, LINKTOSPAN);       // spanf1.c:85
if (threevspecset)
    sporglset2linkset(taskptr, spanfptr, threesporglset,
                      &threelinkset, orglrange, LINKTHREESPAN); // spanf1.c:93
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

The ORGLRANGE filter is built identically for all three by `sporglset2linksetinrange` [`sporgl.c:257–258`]:

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);
prefixtumbler(&orglrange->width, 0, &range.width);
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                              &range, ORGLRANGE, ...);
```

Only `spantype` differs (1, 2, or 3). The search mechanics — the same `retrieverestricted` → `findcbcinarea2d` → `crumqualifies2d` path — are identical for all three.

**A reverse-direction query is therefore obtained simply by passing `tovspecset` while leaving `fromvspecset = NULL`.** `findlinksfromtothreesp` skips the from-constraint and applies only the to-constraint search.

`intersectlinksets` [`spanf2.c:64–69`] short-circuits immediately when only one of the three lists is non-null:

```c
if (!linkset1 && linkset2 && !linkset3)
    *linkset4ptr = linkset2;
```

A pure to-set query returns the to-linkset directly at O(1) intersection cost.

#### No Link Types, No Opt-In

Links have no "type" attribute. `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN` are not link types — they are ORGLRANGE-dimension slot labels shared by every link in the database. There is no per-link discriminator and no per-type registration. Every link created by `docreatelink` [`do1.c:195–221`] writes entries into all three slots. Any of the three can be queried independently, in combination, or as the sole constraint.

---

### One Caveat: homeset Is Always Discarded

`fns.c:198` passes `NULL` for the homeset, overriding what was parsed:

```c
dofindlinksfromtothree(taskptr, fromvspecset, tovspecset, threevspecset,
                        (typeispan*)NULL /*homeset*/, &linkset)
```

And `sporglset2linkset` [`sporgl.c:227`] further overrides any non-null homeset with a hardcoded width-100 span:

```c
if (TRUE||!homeset) {          // always-true: parameter is dead
    nullhomeset.width.mantissa[0] = 100;
    homeset = &nullhomeset;
}
```

This does not change the intersection-vs-equality conclusion — it only means the ORGLRANGE search is always global (all orgl addresses ≤ 100), not scoped to a document. See Finding 0069 for that bug.

---

### Summary

| Property | Result | Evidence |
|---|---|---|
| From-span matching | Intersection (overlap) | `crumqualifies2d` at `retrie.c:282–300` |
| To-span matching | Intersection (same code, `LINKTOSPAN` prefix) | `sporglset2linksetinrange` at `sporgl.c:259` |
| Reverse-direction query (to-keyed) | Yes — pass `tovspecset` only | `findlinksfromtothreesp` at `spanf1.c:84–90` |
| Per-link-type opt-in required | No | Span type = ORGLRANGE prefix only |
| Link type discriminator | None exists | No type field on any link struct |
| Orgl-range scoping | Dead code (`TRUE||!homeset`) | `sporgl.c:227`; `fns.c:198` |
