## Question 1 [evidence]

> Does udanax-green's link-handling code (creation, traversal, type-based queries) treat a link with empty type endset Θ identically to one with non-empty Θ, or does empty Θ change downstream behavior?

## KB Synthesis

## Link Type Endset (Θ): Behavioral Analysis

### What the KB Establishes About Θ

[SS-LINK-ENDPOINT Finding 0024] defines link types as content references — VSpecs pointing into the bootstrap document's type registry at `1.0.2.x`. Θ is not a metadata field or enum; it is a full endset parallel to source and target, indexed in the spanf under LINKTHREESPAN=3 [SS-RETRIEVE-ENDSETS Finding 0035].

---

### Creation With Empty Θ: Not Answerable From KB

[PRE-LINK-CREATE Finding 0028] states the minimum valid endpoint width is ≥1, and zero-width endpoints crash (Bug 0017) — but this precondition is stated for **source and target only**. Whether it applies equally to Θ is not addressed in the KB. If Θ is passed as NOSPECS versus zero-width VSpec, these may behave differently. The KB cannot resolve this.

---

### Traversal With Empty or Ghost Θ

Once a link exists, [INV-ITOV-FILTERING Finding 0048] governs all I-to-V conversion uniformly across all three endsets: unreferenced I-addresses are **silently dropped** without error. FOLLOWLINK on an empty or ghost Θ succeeds and returns `[]` — indistinguishable from a link whose type content was deleted.

This is confirmed by [EC-ORPHANED-LINK Finding 0024]'s behavior matrix:

| Deleted | TYPE result |
|---------|-------------|
| Nothing | Works |
| Source only | Works |
| Target only | Works |
| Home doc text | Works |
| **Both source + target** | **Empty (unexpected\*)** |

The asterisk is significant: when both source and target are deleted, Θ returns empty despite the bootstrap type document being intact. The KB marks this as unexpected but does not explain the mechanism. This suggests some internal coupling between endpoint resolution and type endset resolution that is not captured in any KB entry.

---

### Type-Based Queries: Broken Regardless of Θ Content

[EC-TYPE-FILTER-NONFUNCTIONAL Finding 0029] documents that `find_links(source, NOSPECS, type_spec)` returns empty even when unfiltered search finds matching links. This is independent of whether Θ is populated — type filtering in `find_links` is non-functional for all links. [EC-FIND-LINKS-GLOBAL Finding 0069] reinforces this: the orgl-range parameter (which would scope by type) is ignored due to the `TRUE||` dead-code guard.

---

### RETRIEVEENDSETS With Empty Θ

[SS-RETRIEVE-ENDSETS Finding 0035] states the three-endset is searched by restricting LINKTHREESPAN=3 in the spanf. If Θ was never populated (no LINKTHREESPAN entries for this link), RETRIEVEENDSETS returns an empty three-endset. This is the same result as a ghost Θ via [INV-ITOV-FILTERING].

---

### Summary

For any link with empty or ghost Θ:
- **FOLLOWLINK(TYPE)** → `[]`, operation succeeds [INV-ITOV-FILTERING]
- **RETRIEVEENDSETS three-endset** → empty [SS-RETRIEVE-ENDSETS]
- **find_links by type** → empty regardless (type filter is broken for all links) [EC-TYPE-FILTER-NONFUNCTIONAL]
- **From/to endset behavior** → unaffected by Θ state per the orphan matrix [EC-ORPHANED-LINK]

The anomalous coupling (both-endpoints-deleted causes Θ to go empty) is documented but unexplained by the KB.

---

## Code Exploration

I now have everything needed for a complete analysis. Let me compile the answer.

---

## Answer: Does Empty Θ Change Downstream Behavior in udanax-green?

**Yes — empty Θ (the type endset) changes behavior in at least two ways: `followlink` on the three-endset fails, and queries behave asymmetrically. Here is the full trace.**

---

### 1. Definitions

From `backend/xanadu.h:36-38`:
```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
```
Θ is the "three" endset, stored at V-position 3 in the link's orgl.

---

### 2. Link Creation Path

**Entry point:** `fns.c:100-112` → `do1.c:docreatelink` (lines 195–221).

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
    typespecset fromspecset, typespecset tospecset,
    typespecset threespecset, typeisa *linkisaptr)
```

**Step A — `specset2sporglset` with empty Θ** (`do1.c:216`):
```c
&& specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
```
In `sporgl.c:14-33`, if `threespecset` is NULL:
```c
*sporglsetptr = NULL;
for (; specset; ...)  { ... }  // loop body never executes
*sporglsetptr = NULL;
return (TRUE);
```
Result: `threesporglset = NULL`. Returns TRUE — no error.

**Step B — `setlinkvsas`** (`do1.c:217`):
```c
&& setlinkvsas(&fromvsa, &tovsa, &threevsa)
```
In `do2.c:169-183`, `&threevsa` is non-NULL (a local variable address), so `threevsa` gets populated with concrete tumbler values at V-position 3. This matters for Step C.

**Step C — `insertendsetsinorgl` with empty Θ** (`do1.c:218`, implemented in `do2.c:130-149`):
```c
if (threevsa && threesporglset) {       // do2.c:136
    insertpm(taskptr, linkisaptr, link, threevsa, threesporglset);
} else {
    // do2.c:141-146: logs debug message, falls through
}
return (TRUE);
```
Since `threevsa` is non-NULL (pointer to local var) but `threesporglset` is NULL, the condition is **false**. `insertpm` for the three-endset is never called. **No three-endset data enters the orgl (POOM).**

Also note: in non-DISTRIBUTION builds this hits `fprintf(stderr, "leaving INSERTENDSETSINORGL 4\n")` at `do2.c:142` — the code flags it as a notable case.

**Step D — `insertendsetsinspanf` with empty Θ** (`do1.c:219`, implemented in `do2.c:116-128`):
```c
if (!(
    insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
  && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)))
        return (FALSE);
if (threesporglset) {                   // do2.c:122 — false: NULL
    if (!insertspanf(..., LINKTHREESPAN)) return (FALSE);
}
return (TRUE);
```
**No LINKTHREESPAN entry is inserted into the spanfilade.** The from- and to-endsets are inserted normally.

**Creation conclusion:** A link with empty Θ is created successfully. The link node exists in the granfilade, and from/to entries exist in the spanfilade. But the three-endset slot is entirely absent from both the orgl and the spanfilade.

---

### 3. Traversal: `followlink` with `whichend = LINKTHREESPAN`

**Entry:** `fns.c:114-127` → `do1.c:dofollowlink` (lines 223–232):

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr,
    typespecset *specsetptr, INT whichend)
{
    return (
       link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset(...));
}
```

In `sporgl.c:67-95`, `link2sporglset` looks up the orgl at V-position `whichend`:
```c
tumblerincrement(&zero, 0, whichend, &vspan.stream);  // V-position = 3 for LINKTHREESPAN
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, NULL, I, NULL)) {
    // populate sporglset, return TRUE
} else {
    return (FALSE);         // sporgl.c:93
}
```
Since `insertpm` for three was never called in Step C, there is no data at V-position 3. `retrieverestricted` returns nothing. **`link2sporglset` returns FALSE.**

Therefore `dofollowlink` returns FALSE, and `fns.c:125` calls `putrequestfailed(taskptr)`. **The client receives an error for a `followlink` request on the three-endset of a link created with empty Θ.**

Followlink on the from- or to-endset (`whichend = LINKFROMSPAN/LINKTOSPAN`) works normally regardless.

---

### 4. Queries: `findlinksfromtothree` with Empty Θ in Query vs. Stored Link

**Entry:** `fns.c:189-202` → `do1.c:dofindlinksfromtothree` → `spanf1.c:findlinksfromtothreesp` (lines 56–103).

**Case A: Query with NULL `threevspecset` (caller passes empty Θ as filter)**

```c
fromlinkset = tolinkset = threelinkset = NULL;   // spanf1.c:69
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (tovspecset)
    specset2sporglset(taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);
if (threevspecset)                               // spanf1.c:74 — false: skipped
    specset2sporglset(...);

if (fromvspecset) {
    sporglset2linkset(..., LINKFROMSPAN);         // runs
}
if (tovspecset) {
    sporglset2linkset(..., LINKTOSPAN);           // runs
}
if (threevspecset) {                             // spanf1.c:92 — false: skipped
    sporglset2linkset(..., LINKTHREESPAN);
}
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```
`threelinkset` remains NULL. In `spanf2.c:intersectlinksets` (lines 63-78), when exactly one or two of the three are non-null, the function short-circuits:
```c
if (linkset1 && !linkset2 && !linkset3)  *linkset4ptr = linkset1;     // line 64
else if (!linkset1 && linkset2 && !linkset3) *linkset4ptr = linkset2;  // line 66
...
```
And when both from and to are non-null but three is null, the `if (!linkset3)` path (line 95) does a pairwise intersection. **Empty Θ in the query means "no filter on type" — the query matches any link whose from/to endsets overlap the given spans, regardless of Θ.**

**Case B: Querying with a non-empty Θ for a link that was stored with empty Θ**

`sporglset2linkset(..., LINKTHREESPAN)` searches the spanfilade for LINKTHREESPAN entries overlapping the query Θ. Since the link was stored with no LINKTHREESPAN entries, none are found. `threelinkset` is NULL after this lookup, causing `intersectlinksets` to return an empty set (line 71: `*linkset4ptr = NULL` when all three are null). **The link will not appear in query results.**

**Query asymmetry summary:**
- Query with empty Θ → no three-endset constraint → broader match (finds links regardless of their Θ)
- Link stored with empty Θ → querying for any specific Θ will not match it (nothing in LINKTHREESPAN to intersect)

---

### 5. Retrieve Endsets on an Empty-Θ Link

**Entry:** `fns.c:350-362` → `do1.c:doretrieveendsets` → `spanf1.c:retrieveendsetsfromspanf` (lines 190–235).

After retrieving from/to, the function checks:
```c
if (threesetptr) {          // spanf1.c:229
    temp = (retrievesporglsetinrange(taskptr, sporglset, &threespace, &threesporglset)
        && linksporglset2specset(taskptr, ..., threesetptr, NOBERTREQUIRED));
    return(temp);
}
```
`retrievesporglsetinrange` finds no LINKTHREESPAN entries; returns with `threesporglset = NULL`. `linksporglset2specset` in `sporgl.c:97-123` does nothing (loop body never executes with NULL sporglset), sets `*threesetptr = NULL`, returns TRUE. **`retrieveendsets` succeeds, returning NULL for the three-endset.** No error.

---

### 6. Complete Summary

| Operation | Non-empty Θ | Empty Θ |
|---|---|---|
| `createlink` | Stores LINKTHREESPAN in orgl and spanfilade | Skips both; logs debug warning [do2.c:142]; returns TRUE |
| `followlink` (whichend=1 or 2) | Works | Works normally |
| `followlink` (whichend=3) | Returns the Θ endset | **Returns request failure** [sporgl.c:93] |
| `findlinksfromtothree` (empty Θ in query) | N/A | Omits three-endset filter; broader match [spanf1.c:74,92] |
| `findlinksfromtothree` (specific Θ in query, link has empty Θ) | Matches if Θ overlaps stored three-endset | **Link not found** (no LINKTHREESPAN entry to intersect) |
| `retrieveendsets` | Returns populated three-endset | Returns NULL three-endset; succeeds [spanf1.c:229-233] |

**Empty Θ is not the same as non-empty Θ.** The two substantive behavioral differences are:

1. **`followlink` on whichend=3 fails** — `link2sporglset` at `sporgl.c:92-94` returns FALSE when no orgl data exists at V-position 3, propagating failure to the client.

2. **Queries with specific Θ don't find empty-Θ links** — no LINKTHREESPAN entries exist to produce a non-empty `threelinkset` for intersection in `intersectlinksets` (`spanf2.c:46-120`).

Empty Θ in a *query* (as opposed to in the stored link) is a distinct case that acts as "wildcard" — it simply omits the three-endset constraint rather than matching links that have an empty Θ.
