## Question 1 [evidence]

> In the implementation's link-finding/intersection code (`sporglset2linksetinrange`, `intersectlinksets`), does type endset matching compare exact span structures, or is it computed over coverage (set of addresses)?

## KB Synthesis

The KB supports a clear answer with one caveat about direct code evidence for `intersectlinksets` internals.

## Type endset matching uses I-address coverage intersection, not exact span comparison

The entire spanfilade search architecture is built on range-based I-address intersection, and the THREE/type endset participates identically to source and target.

**The mechanism:**

`find_links` searches all three endset types using the same `retrievesporglsetinrange()` call with different ORGLRANGE prefixes: LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3. Each search returns the set of link ISAs whose stored endset I-spans have non-empty intersection with the query I-address range. [INT-SPORGL-LINK-INDEX]

The spanfilade model is `Map<IAddress, Set<LinkISA>>` — an I-address coverage index, not a span-equality index. `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.endpoint) ≠ ∅ }`. [SS-SPANF-OPERATIONS, SS-FIND-LINKS]

`intersectlinksets` then takes the three result sets (FROM hits, TO hits, THREE hits) and computes set intersection by link ISA — a link must appear in every non-empty search to be returned. The KB cites its complexity as O(n*m) or O(n*m*p) for two or three endset searches. [SS-FIND-LINKS Finding 0035]

**The type encoding matters here:**

Type endsets are stored as VSpec references to the bootstrap document's type registry at `1.0.2.x` [SS-LINK-ENDPOINT Finding 0024]. A caller querying `find_links(NOSPECS, NOSPECS, type_spec)` must pass I-addresses from the bootstrap document's type subspace — not content from user documents. EC-TYPE-FILTER-NONFUNCTIONAL shows this consistently returns empty in practice, likely because callers construct type_spec from user-document content rather than bootstrap document I-addresses. The matching mechanism itself is the same coverage intersection — it just fails to find intersections because the query addresses don't overlap with stored type endset addresses. [EC-TYPE-FILTER-NONFUNCTIONAL]

**What the KB does not cover:**

The internal comparison logic inside `intersectlinksets` (`spanf2.c:46-120`) beyond the complexity bound. The KB has no finding that examines whether it compares raw sporgl structs or extracts I-address sets first. Based on the architecture, coverage intersection is the only interpretation consistent with all other behavior, but I cannot cite a finding that reads those specific lines.

---

## Code Exploration

Now I have everything I need to give a complete and precise answer.

---

## Type Endset Matching: Coverage-Based (Range Intersection), Not Exact Span Equality

The implementation performs **coverage-based range intersection**, not exact span structure comparison, at every stage. Here is the full trace.

---

### Storage Layout in the Spanfilade

`insertspanf` [`spanf1.c:15-53`] stores each endset span as a 2D record in the spanfilade:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);   // spanf1.c:22
tumblerclear (&crumwidth.dsas[ORGLRANGE]);                        // spanf1.c:23
...
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);              // spanf1.c:49
movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);               // spanf1.c:50
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);  // spanf1.c:51
```

The two dimensions are:

| Dimension | Stored value | Width |
|---|---|---|
| `SPANRANGE` | `lstream` (I-space content address) | `lwidth` (nonzero span) |
| `ORGLRANGE` | `prefixtumbler(linkISA, spantype)` — type byte prepended to link ISA | **0** (a point, not a range) |

The `spantype` is one of `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` [`xanadu.h:36-38`]. So for a FROM endset, the ORGLRANGE coordinate is literally `1.linkISA`; for a TO endset, `2.linkISA`.

---

### Query: `sporglset2linksetinrange` [`sporgl.c:239-269`]

For each sporgl (I-span) in the input specset, this function calls `retrieverestricted` with two constraints:

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);   // sporgl.c:257
prefixtumbler(&orglrange->width,  0,        &range.width);    // sporgl.c:258
context = retrieverestricted(spanfptr,
    (typespan*)sporglset, SPANRANGE,   // constraint 1: query content range
    &range,              ORGLRANGE,    // constraint 2: type-prefixed link-ISA range
    (typeisa*)infoptr);                // sporgl.c:259
```

`retrieverestricted` [`retrie.c:56-85`] converts both constraints to `[start, end)` intervals and calls `retrieveinarea` → `findcbcinarea2d` → **`crumqualifies2d`** [`retrie.c:270-305`].

#### `crumqualifies2d` — the actual matching predicate

```c
// SPANRANGE check:
endcmp   = whereoncrum(crumptr, offset, span1end,   index1);
if (endcmp <= ONMYLEFTBORDER) return(FALSE);          // retrie.c:283-285
startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME) return(FALSE);                 // retrie.c:287-290

// ORGLRANGE check (same pattern):
endcmp   = whereoncrum(crumptr, offset, span2end,   index2);
if (endcmp < ONMYLEFTBORDER) return(FALSE);           // retrie.c:292-296
startcmp = whereoncrum(crumptr, offset, span2start, index2);
if (startcmp > THRUME) return(FALSE);                 // retrie.c:297-300
```

This is a classic **half-open interval overlap test** — a stored span qualifies if it intersects `[start, end)`. There is no equality test anywhere in `crumqualifies2d`. A link whose FROM endset covers even one address in common with the query I-span is returned.

#### What the ORGLRANGE constraint actually does

`sporglset2linkset` [`sporgl.c:222-237`] always sets `orglrange` to a nullhomeset:

```c
if (TRUE||!homeset) {                         // sporgl.c:227 — TRUE forces this branch always
    tumblerclear(&nullhomeset.stream);         // stream = 0
    nullhomeset.width.mantissa[0] = 100;      // width = 100
    homeset = &nullhomeset;
}
```

After `prefixtumbler(stream=0, spantype=1, ...)`, the ORGLRANGE query range becomes `[1.0, 1.100)` — i.e., all records with a leading `1` (FROM type) digit, covering all possible link ISAs within that range. This is a **type filter**, not a value equality check. It says: "return only entries of this endset type."

The link ISA is then extracted from the ORGLRANGE coordinate by stripping the type prefix:

```c
beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);  // sporgl.c:264
onlinklist(taskptr, linksetptr, &linksa);                  // sporgl.c:265
```

---

### Intersection: `intersectlinksets` [`spanf2.c:46-120`]

After running three separate endset queries (from/to/three), `findlinksfromtothreesp` [`spanf1.c:100`] calls:

```c
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

The intersection uses:

```c
if (tumblereq(&temp1->address, &temp2->address)) {  // spanf2.c:98, 109-110
    linkset4 = makelinkitem(taskptr, &temp1->address);
```

This compares **link ISAs** (the tumbler address of the link object), not span structures. A link appears in the result if and only if its ISA was found in all non-null input sets. This is set intersection over link identifiers.

---

### Answer

**`sporglset2linksetinrange` is entirely coverage-based.** A link's endset matches a query specset if the stored endset I-span *overlaps* (intersects) the query I-span in `SPANRANGE` — by the `crumqualifies2d` range-overlap test [`retrie.c:283-300`]. There is no exact span equality check anywhere in retrieval.

**`intersectlinksets` compares exact tumbler equality — but of link ISAs, not span structures** [`spanf2.c:98, 109`]. It asks "did this link ISA appear in all three endset searches?" — not "do the stored spans match the query spans exactly."

The overall semantics of a `dofollow` call therefore are:
1. Convert specsets to I-spans (coverage)
2. For each endset role (from/to/three): find all links whose registered I-spans in that role **overlap** the query I-spans — pure coverage test
3. Return the link ISAs that appeared in all requested roles — set intersection by identity

Exact span structure is never compared at any step. The system asks only "do any stored addresses overlap the query addresses?"
