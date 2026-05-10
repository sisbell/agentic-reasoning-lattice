# Revision Consultation — ASN-0006

**Review:** review-1.md
**Date:** 2026-03-06 21:40

## Summary

6 REVISE items analyzed: 5 internal, 1 consulted (0 nelson, 1 gregory)

## Consultation Results

### Issue 5: `discoverable_links` and `endsets` are not defined

**Category:** GREGORY
**Reason:** The definition of `discoverable_links` requires knowing what the link search mechanism actually checks. The ambiguity in `endsets(L)` — whether all three endsets (from, to, type) participate in discovery or only from/to — depends on what the implementation's search function inspects.

**Gregory question:** When the link search function checks for intersecting endsets, does it match against all three endsets (from, to, type) or only specific ones — and does the type endset participate in span-index-based discovery the same way as from and to?

**Gregory's Answer:**

## KB Synthesis

## Link Search: Endset Matching in the Spanf

The answer has two layers: structural (what's indexed) and behavioral (what actually works).

### All Three Endsets Are Indexed

When `CREATELINK` executes, `insertendsetsinspanf()` indexes all three endsets into the spanfilade under separate ORGLRANGE subspaces: `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`. The type (three) endset participates in the spanf index on equal structural footing with from and to. [INT-SPORGL-LINK-INDEX]

This is confirmed by `RETRIEVEENDSETS` (opcode 28), which issues three independent spanfilade searches — one per endset type — using these ORGLRANGE prefixes to retrieve all matching content. [SS-RETRIEVE-ENDSETS]

### But find_links Only Works on From and To

`FINDLINKSFROMTOTHREE` accepts three spec parameters (from, to, three), but:

1. **From and to** participate fully. When both are provided, AND semantics apply: `find_links(source_spec, target_spec) = find_links(source_spec) ∩ find_links(target_spec)`. Either alone performs a single-endpoint I-address intersection. [SS-FIND-LINKS]

2. **The three/type parameter is broken.** `find_links(source, NOSPECS, type_spec)` returns empty results even when unfiltered searches find links of those types. The type filter is accepted syntactically but produces no results. [EC-TYPE-FILTER-NONFUNCTIONAL]

3. **The orgl range parameter is also ignored.** A `TRUE||` guard in `sporglset2linkset()` replaces any caller-provided orgl range with a hardcoded unbounded range, making all `find_links` searches global across the orgl dimension. [EC-FIND-LINKS-GLOBAL]

### Summary

| Mechanism | From | To | Type (Three) |
|-----------|------|----|--------------|
| Indexed in spanf | ✓ | ✓ | ✓ |
| `find_links` discovery | ✓ | ✓ | ✗ (broken) |
| `RETRIEVEENDSETS` retrieval | ✓ | ✓ | ✓ |

The type endset is stored and retrievable via `RETRIEVEENDSETS`, but cannot be used as a filter criterion in `find_links`. Link discovery is effectively a two-dimensional operation: from-endset and to-endset I-address intersection only.

---

## Code Exploration

I have all the source I need. Here is the complete answer.

---

## How the Link Search Checks Endsets: A Source-Level Trace

### 1. The Constants (`xanadu.h:36–38`)

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

These integer tags discriminate endset type in the spanfilade's 2D key space. The "third" endset — historically the _type_ endset in Xanadu's from/to/type model — is `LINKTHREESPAN = 3`.

---

### 2. How Links Are Stored in the Spanfilade (`spanf1.c:15–54`, `insertspanf`)

Each endset is stored as a crum in the spanfilade with a **two-dimensional key**:

- **ORGLRANGE axis**: `prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE])` — the link's ISA prefixed with `spantype` (1, 2, or 3). This is _which link_ and _which endset role_.
- **SPANRANGE axis**: the sporgl's `sporglorigin`/`sporglwidth` — _what content address_ is referenced by that endset.

At insertion time (`do2.c:116–128`, `insertendsetsinspanf`):

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // always
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)     // always
if (threesporglset) {
    insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN) // only if non-null
}
```

The three endset is stored under the same spanfilade using the same mechanism as from and to; it just carries a different prefix tag.

---

### 3. The Search Function: `findlinksfromtothreesp` (`spanf1.c:56–103`)

This is the core of link discovery. Its structure is:

```c
// Step 1: convert each non-null vspecset to a sporglset (I-space addresses)
if (fromvspecset)   specset2sporglset(..., &fromsporglset, ...);
if (tovspecset)     specset2sporglset(..., &tosporglset, ...);
if (threevspecset)  specset2sporglset(..., &threesporglset, ...);

// Step 2: query the spanfilade for each non-null endset
if (fromvspecset) {
    sporglset2linkset(..., fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
    if (!fromlinkset) { *linksetptr = NULL; return TRUE; }  // early exit
}
if (tovspecset) {
    sporglset2linkset(..., tosporglset, &tolinkset, orglrange, LINKTOSPAN);
    if (!tolinkset)  { *linksetptr = NULL; return TRUE; }   // early exit
}
if (threevspecset) {
    sporglset2linkset(..., threesporglset, &threelinkset, orglrange, LINKTHREESPAN);
    if (!threelinkset) { *linksetptr = NULL; return TRUE; } // early exit
}

// Step 3: intersect results
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

**The three endset uses exactly the same span-index-based discovery as from and to.** It calls `sporglset2linkset` with `LINKTHREESPAN`, and that function runs through `sporglset2linksetinrange` (`sporgl.c:239–269`), which issues a `retrieverestricted` call on the spanfilade:

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);  // range prefixed with 1, 2, or 3
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, ...);
```

The spantype prefix is the filter that separates from-links, to-links, and three-links in the same index. All three roles use the same underlying enfilade retrieval machinery.

---

### 4. The Intersection (`spanf2.c:46–120`, `intersectlinksets`)

`intersectlinksets` receives three linksets (any can be `NULL`):

- **If only one is non-null**, it's used directly — no intersection computed.
- **If two are non-null**, a nested O(n²) loop compares ISAs with `tumblereq`.
- **If all three are non-null**, a nested O(n³) triple loop requiring `temp1 == temp2 == temp3`.

A link must appear in _every_ queried linkset to survive. NULL linksets (i.e., omitted endsets) are treated as unconstrained — they don't filter.

---

### 5. The FEBE Layer Bypasses `homeset` (`fns.c:198`)

At the FEBE handler level, `homeset` is parsed but then explicitly discarded:

```c
dofindlinksfromtothree(taskptr, fromvspecset, tovspecset, threevspecset,
    (typeispan*)NULL/*homeset*/, &linkset)
```

This means `orglrange` is always `NULL` when entering `sporglset2linkset`. The function handles this in `sporgl.c:222–237` by constructing a hardcoded fallback:

```c
nullhomeset.width.mantissa[0] = 100;  // covers all link ISAs in space
homeset = &nullhomeset;
```

So there is no orglrange restriction in practice — the search always scans all links in the full ISA space, filtered only by the spantype prefix and the content-address intersection.

---

### Summary

| Question | Answer |
|----------|--------|
| Does the type/three endset participate in span-index-based discovery? | **Yes.** It uses `sporglset2linkset` with `LINKTHREESPAN = 3`, the same `retrieverestricted` path as from and to. |
| Does the type endset use a different index or mechanism? | **No.** Same spanfilade, same retrieval function, differentiated only by the integer prefix tag (1/2/3). |
| Is the type endset queried only when non-null? | **Yes.** `if (threevspecset)` guards the entire block at `spanf1.c:92–99`. If you pass `NULL` for the type specset, no type constraint is applied and three-endset links are invisible to the filter. |
| Does a missing type endset result in "match any type"? | **Yes** — via `intersectlinksets`: a `NULL` linkset is treated as unconstrained. |
| Can a type-only query (from/to both null) return results? | **Yes.** If only `threevspecset` is non-null, `intersectlinksets` short-circuits and returns the three-linkset directly (`spanf2.c:68–69`). |
