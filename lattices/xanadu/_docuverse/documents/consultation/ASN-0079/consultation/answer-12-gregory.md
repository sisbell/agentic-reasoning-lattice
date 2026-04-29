## Question 12 [gregory]

> In `findlinksfromtothreesp`, what is the exact overlap predicate between the query I-spans and a link's endset I-spans — must there be any byte-level intersection, or does the spanfilade store coarser granularity entries that could miss partial-span overlaps?

## KB Synthesis

## Overlap Predicate in `findlinksfromtothreesp`

The predicate is **range intersection at I-address granularity** — any non-empty overlap between the query I-span and a stored link endset I-span is sufficient to return the link. There is no coarser-granularity approximation that would cause missed partial-span overlaps.

### What the spanfilade stores

[SS-DOCISPAN] (Finding 0047) establishes that `insertspanf` makes one `insertnd` call per `typeispan` struct, where each `typeispan` represents a contiguous range (start, width). So a link endpoint corresponding to k contiguous bytes is stored as one B-tree entry covering `[start, start+width)` — not k individual byte entries. When a V-span maps to non-contiguous I-addresses (e.g., content transcluded from multiple sources), [ST-LINK-CREATE] (Finding 0037) shows this produces multiple separate sporgls — one per contiguous I-address region — each independently indexed.

### How the search works

[INT-SPORGL-LINK-INDEX] (Finding 0035) describes the call chain: the query specset is converted to I-spans (V→I translation via sporgl conversion), then `retrievesporglsetinrange()` searches the 2D spanfilade using SPANRANGE and ORGLRANGE restrictions. The B-tree traversal (`findcbcinarea2d`) uses `whereoncrum` / `intervalcmp` [SS-INTERVAL-CMP] to classify each crum against the query range — a five-way predicate (`TOMYLEFT`, `ONMYLEFTBORDER`, `THRUME`, `ONMYRIGHTBORDER`, `TOMYRIGHT`). Any crum whose stored I-span interval has **any overlap** with the query interval is descended into and returned.

The overlap criterion is therefore: `stored_start < query_end AND query_start < stored_end` (standard half-open interval intersection). Even a single overlapping I-address triggers a match.

### Confirmed by partial-overlap examples

[SS-FIND-LINKS] (Finding 0028) provides the definitive empirical confirmation:

```
Link source: "DEF" stored as I-span [I.4, I.7)
Query (document transcluding "EF"): I-span [I.5, I.7)
Intersection: [I.5, I.7) ≠ ∅  → link returned
```

"Partial overlap suffices — a search specset that shares even one I-address with a link endpoint will discover that link."

### No coarser-granularity miss scenario

The per-contiguous-region storage granularity does **not** cause misses. If a link endpoint spans bytes 4–6 stored as a single range `[4, 7)`, a query for byte 5 only (`[5, 6)`) still intersects `[4, 7)` and returns the link. The only scenario where a partial query fails to find a link is if the query I-span genuinely does not overlap any stored endset I-span — which is semantically correct, not a granularity artifact.

The one caveat is [EC-FIND-LINKS-GLOBAL] (Finding 0069): the ORGLRANGE filter parameter is effectively ignored due to a `TRUE||` bug in `sporglset2linkset`, so the orgl-dimension restriction never narrows results. The span-dimension (I-address content) filter is the only operative predicate.

---

## Code Exploration

Now I have a complete, precise picture. Here is the full answer.

---

## `findlinksfromtothreesp`: Exact Overlap Predicate Analysis

### Call Chain

`findlinksfromtothreesp` (spanf1.c:56–103) converts up to three endpoint specsets to I-span–based sporglsets, calls `sporglset2linkset` for each, then intersects the three resulting linksets:

```c
// spanf1.c:71–99
specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
sporglset2linkset(taskptr, spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
...
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

`sporglset2linksetinrange` (sporgl.c:239–269) is where the actual spanfilade query fires:

```c
// sporgl.c:257–259
prefixtumbler(&orglrange->stream, spantype, &range.stream);
prefixtumbler(&orglrange->width, 0, &range.width);
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, ...);
```

This calls `retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` (retrie.c:229–268), which traverses the spanfilade tree and tests each subtree with `crumqualifies2d`.

---

### The Exact Overlap Predicate — `crumqualifies2d` (retrie.c:270–305)

The predicate runs in two passes, one per axis.

**SPANRANGE axis (index1) — query I-span vs. stored I-span:**

```c
// retrie.c:282–290
endcmp = iszerotumbler(span1end) ? TOMYRIGHT
                                  : whereoncrum(crumptr, offset, span1end, index1);
if (endcmp <=/*=*/ ONMYLEFTBORDER) return FALSE;    // line 283

startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME) return FALSE;                 // line 287
```

`whereoncrum` (retrie.c:345–398) computes where a tumbler address falls relative to a crum's half-open interval `[left, right)` where `left = offset[index] + crum.cdsp[index]` and `right = left + crum.cwid[index]`:

```
TOMYLEFT        (-2)  address < left
ONMYLEFTBORDER  (-1)  address == left
THRUME          ( 0)  left < address < right
ONMYRIGHTBORDER (+1)  address == right
TOMYRIGHT       (+2)  address > right
```

The two guards reduce to:
- `endcmp <= ONMYLEFTBORDER` disqualifies → i.e., `query_end ≤ crum_left` → return false
- `startcmp > THRUME` disqualifies → i.e., `query_start ≥ crum_right` → return false

**Surviving condition is therefore:**

```
query_start < crum_right   AND   query_end > crum_left
```

This is standard **strict half-open interval overlap**. Expressed in span terms, a query I-span `[Q, Q+Qw)` overlaps a stored entry `[E, E+Ew)` iff:

```
Q < E + Ew   AND   Q + Qw > E
```

Adjacency (where `Q + Qw == E`, i.e., spans touch but share no byte) is **excluded** — the `<=` at line 283 catches `endcmp == ONMYLEFTBORDER`, meaning "query ends exactly at the crum's left edge" → no match. There is no off-by-one that would accidentally include touching-but-not-overlapping spans.

**ORGLRANGE axis (index2) — link type + document ISA filter:**

```c
// retrie.c:292–300
endcmp = iszerotumbler(span2end) ? TOMYRIGHT
                                  : whereoncrum(crumptr, offset, span2end, index2);
if (endcmp < ONMYLEFTBORDER) return FALSE;   // note: < not <=

startcmp = whereoncrum(crumptr, offset, span2start, index2);
if (startcmp > THRUME) return FALSE;
```

This axis filters by link type (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3) and document ISA range. Notably this uses `< ONMYLEFTBORDER` (strict, not `<=`), so ORGLRANGE is slightly more inclusive at the boundary — a stored link whose ISA exactly equals `span2end` is not excluded.

---

### Granularity: What Is Stored in the Spanfilade?

In `insertspanf` (spanf1.c:15–53), each sporgl (I-span of an endset) is inserted as **one crum**:

```c
// spanf1.c:27–51
movetumbler(&((typeispan*)sporglset)->stream, &lstream);    // exact stream origin
movetumbler(&((typeispan*)sporglset)->width, &lwidth);      // exact width
...
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

There is **no coarsening, no aggregation**. The SPANRANGE coordinates of the stored crum are the exact tumbler stream and width of the link's endset I-span. One link endset I-span → one leaf crum in the spanfilade.

Interior nodes of the enfilade tree carry a `cwid` that is the **bounding box** of all descendants — used only to prune whole subtrees during `findcbcinarea2d`'s recursion (retrie.c:252–259). This pruning is strictly conservative: it can skip subtrees that definitely don't overlap, but cannot miss any crum that qualifies. No false negatives are possible.

---

### Tumbler Precision

A tumbler is a fixed-point number with 16 mantissa digits (`NPLACES = 16`, common.h:53). The smallest nonzero unit is tumbler `0.0...01` (one in the least-significant place). Text bytes in udanax-green are addressed as consecutive integer tumblers (each character increments by 1). Therefore the granularity of the overlap predicate is exactly **one character / one addressable byte**.

---

### Summary

| Question | Answer |
|---|---|
| Overlap predicate | `query_start < entry_end AND query_end > entry_start` — strict half-open interval intersection at tumbler precision |
| Adjacent (touching) spans | **Not considered overlapping** — `<=` at retrie.c:283 excludes `query_end == entry_start` |
| Stored granularity | One crum per link endset I-span; exact (stream, width) stored with no coarsening |
| Could coarser storage miss partial-span overlaps? | **No.** Leaf crums store I-spans exactly; interior bounding boxes only prune, never discard qualifying entries |
| Byte-level intersection required? | Yes — any two I-spans sharing at least one byte will match; sub-byte overlap is impossible since the addressable unit is one character |
