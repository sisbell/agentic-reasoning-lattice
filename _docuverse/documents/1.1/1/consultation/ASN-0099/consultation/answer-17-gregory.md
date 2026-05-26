## Question 17 [gregory]

> For a link whose source endset spans a range of I-addresses and only a subset of those I-addresses appear in the querying document's POOM, does `find_links` still return that link, or must the entire endset I-range be present for the link to match?

## KB Synthesis

**Yes, partial overlap suffices.** A link is returned by `find_links` whenever the query's I-address set has a non-empty intersection with the link's endpoint I-addresses — there is no requirement for the full endset to be present.

This is stated explicitly in [SS-FIND-LINKS] (Finding 0028):

> The search is purely set-intersection on I-addresses: `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`. **Partial overlap suffices** — a search specset that shares even one I-address with a link endpoint will discover that link.

The concrete example there makes this precise: a link whose source covers I-addresses `{I.4, I.5, I.6}` is returned when the querying document contains only `{I.5, I.6}` (transcluded "EF" from a 14-char source "hyperlink text"). The two-address intersection is sufficient.

The mechanism works through the spanfilade. Each I-address (or contiguous I-span) in a link's endset is individually indexed in the spanf at link creation time [SS-SPANF-OPERATIONS], [INT-SPORGL-LINK-INDEX]. When `find_links` runs, it converts the query specset to I-spans via V→I conversion, then searches the spanfilade for any overlap. A single matching I-span triggers the link's inclusion in the result.

Importantly, `follow_link` on a link discovered this way returns the **complete original endset**, not just the subset that enabled discovery [SS-FOLLOW-LINK] (Finding 0028):

> Even when a link is found via partial I-address overlap from a transclusion, `follow_link` returns the full endpoint as it was specified at link creation time.

This behavior also appears in [EC-SEARCH-SPEC-BEYOND-BOUNDS] — after content is partially deleted from a document, `find_links` still returns links whose remaining content overlaps the query, confirming that partial endset coverage is the normal operating model.

---

## Code Exploration

I have traced the complete execution path. Here is the full answer.

---

## Does `find_links` Require the Full Endset I-Range or Only Overlap?

**Short answer:** Partial overlap is sufficient. `find_links` returns the link if **any** I-address contributed by the querying document's POOM overlaps with any I-address in the link's stored endset range. The entire endset I-range does not need to be present.

---

## Execution Path

### Entry point: `fns.c:189` → `do1.c:348` → `spanf1.c:56`

`findlinksfromtothree` [fns.c:189] dispatches to `dofindlinksfromtothree` [do1.c:348], which is a thin wrapper:

```c
bool dofindlinksfromtothree(typetask *taskptr, typespecset fromvspecset, ...)
{
    return findlinksfromtothreesp(taskptr, spanf, fromvspecset, ...);
}
```

The real work happens in `findlinksfromtothreesp` [spanf1.c:56–103].

---

### Step 1: V → I Translation via the Querying Document's POOM

`findlinksfromtothreesp` [spanf1.c:70–71]:

```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
```

`specset2sporglset` [sporgl.c:14] calls `vspanset2sporglset` [sporgl.c:35] which:

1. Opens the querying document's POOM via `findorgl` [sporgl.c:44]
2. For each V-span, calls `vspanset2ispanset` [sporgl.c:48] → `permute` [orglinks.c:404] → `span2spanset` [orglinks.c:425]
3. `span2spanset` calls `retrieverestricted` on the POOM to find what I-addresses correspond to those V-positions

This V→I translation is **bounded by what the querying document's POOM actually maps**. If the querying document's POOM covers only a subset of the link's endset I-range, the resulting `fromsporglset` contains only those partial I-addresses — e.g., `[A, A+x]` where the link's endset is `[A, B]` with `x < B−A`.

---

### Step 2: Spanfilade Lookup — Overlap, Not Containment

`findlinksfromtothreesp` [spanf1.c:76–83]:

```c
if (fromvspecset) {
    sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
    if (!fromlinkset) { *linksetptr = NULL; return (TRUE); }
}
```

`sporglset2linkset` [sporgl.c:222] creates a broad default `orglrange` with width=100 (covering all links) and calls `sporglset2linksetinrange` [sporgl.c:239] for each I-span in the query:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                             &range, ORGLRANGE, (typeisa*)infoptr);
```

This asks the spanfilade: *"find all entries whose SPANRANGE (= the link's stored endset I-range) intersects with my query SPANRANGE (= the querying document's I-addresses)."*

The spanfilade stores, for each link endset, entries of the form `(SPANRANGE=link_endset_I_range, ORGLRANGE=link_ISA)` — inserted at link creation time by `insertspanf` [spanf1.c:15].

---

### Step 3: The Overlap Predicate in `crumqualifies2d`

`retrieverestricted` [retrie.c:56] → `retrieveinarea` [retrie.c:87] → `findcbcinarea2d` [retrie.c:229] → **`crumqualifies2d` [retrie.c:270]**.

```c
bool crumqualifies2d(typecorecrum *crumptr, typedsp *offset,
                     tumbler *span1start, tumbler *span1end, INT index1,
                     tumbler *span2start, tumbler *span2end, INT index2, ...)
{
    endcmp = iszerotumbler(span1end) ? TOMYRIGHT
           : whereoncrum(crumptr, offset, span1end, index1);
    if (endcmp <= ONMYLEFTBORDER) return (FALSE);   // [retrie.c:282-284]

    startcmp = whereoncrum(crumptr, offset, span1start, index1);
    if (startcmp > THRUME) return (FALSE);           // [retrie.c:286-290]
    ...
    return (TRUE);
}
```

In plain terms, a spanfilade crum (representing the link's endset I-range `[A, B]`) passes if and only if:

> `query_end > A` **AND** `query_start < B`

That is: the query range **overlaps** the crum's range. There is no containment requirement in either direction. The check is symmetric overlap.

So if the querying document contributes I-range `[A, A+x]` (a strict subset of the link's `[A, B]`):

- `query_end = A+x > A` (crum start) → passes the first check
- `query_start = A < B` (crum end) → passes the second check
- The crum **qualifies** → the link ISA is extracted and added to `fromlinkset`

---

### Step 4: Per-Endset Sets Are Intersected, Not Unioned

After collecting `fromlinkset`, `tolinkset`, and optionally `threelinkset`, `findlinksfromtothreesp` calls:

```c
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);  // spanf1.c:100
```

`intersectlinksets` [spanf2.c:46] computes the **set intersection**: a link is in the result only if it appears in all provided non-null endset link-sets. But the per-endset lookup itself uses overlap, so a link whose source endset I-range partially overlaps the query will appear in `fromlinkset`, and therefore can survive the intersection.

---

## Conclusion

`find_links` uses **I-address overlap** — not containment — as its matching criterion. The determination is made in `crumqualifies2d` [retrie.c:270–305], which applies:

```
query_end > link_endset_start  AND  query_start < link_endset_end
```

If a link's source endset spans I-addresses `[A, B]` and the querying document's POOM maps only a subset `[A, A+x]` (with `x < B−A`) of that range to V-addresses, then:

- The V→I translation produces a sporglset covering only `[A, A+x]`
- The spanfilade overlap check finds the link's `[A, B]` entry, because `A+x > A` and `A < B`
- **The link is returned**

The entire endset I-range does **not** need to be present in the querying document's POOM. Any non-empty intersection between the querying document's I-addresses and the link's endset I-range is sufficient for the link to be found.
