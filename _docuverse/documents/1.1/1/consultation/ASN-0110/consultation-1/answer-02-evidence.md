## Question 2 [evidence]

> For a store mixing links of different arities, what does the udanax-green RETRIEVEENDSETS return as its result shape, and does it include positions for roles whose endset set is empty?

## KB Synthesis

## RETRIEVEENDSETS Result Shape and Empty Roles

### Fixed Three-Specset Shape

RETRIEVEENDSETS always returns **three specsets simultaneously** — from-endset, to-endset, and three-endset — one per ORGLRANGE prefix [SS-RETRIEVE-ENDSETS]:

> `retrieveendsetsfromspanf()` defines three search spaces using ORGLRANGE prefixes (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3), then for each endset type calls `retrievesporglsetinrange()` independently.

The result is structurally fixed at three slots regardless of what link arities are present in the queried content region.

### Empty Roles for 2-Ary Links

For a standard 2-ary link (from+to only), no LINKTHREESPAN=3 entry is inserted into the spanfilade at creation time. When RETRIEVEENDSETS searches the ORGLRANGE for prefix 3, it finds nothing and returns an empty (NULL) specset for that slot [ST-RETRIEVE-ENDSETS], [SS-LINK-ENDPOINT].

The same applies to the from- and to-slots: if the queried content region doesn't intersect a given role's endset I-addresses, that slot returns empty [SS-LINK-ENDPOINT] Finding 0019:
> "Target specsets are often empty when querying from the source document, suggesting the API returns only endpoints that intersect the query specset."

### The Conditional Flag

The KB notes "the three-endset is conditionally retrieved (only if requested)" [SS-RETRIEVE-ENDSETS] — there is apparently a FEBE-level flag to skip the three-endset search entirely as an optimization. But when requested, the slot is always present in the result, empty or not.

### Summary

The result shape is always `(from_specset, to_specset, three_specset)`. Roles with no contributing links in the queried region — including the three-slot for any 2-ary link — return empty specsets rather than being omitted from the result.

---

## Code Exploration

I now have everything needed. Here is the complete answer.

---

## `RETRIEVEENDSETS` Result Shape and Empty-Role Behavior

### Call Chain

```
fns.c:350  retrieveendsets()
  → do1.c:369  doretrieveendsets()
    → spanf1.c:190  retrieveendsetsfromspanf()
      → sporgl.c:97   linksporglset2specset()   (×3, once per role)
  → putfe.c:356  putretrieveendsets()
    → putfe.c:124  putitemset()                 (×3, unconditionally)
```

---

### Result Shape

**Always exactly three itemsets, in fixed order: fromset · toset · threeset.**

`putretrieveendsets` [putfe.c:356-362] calls `putitemset` unconditionally for all three:

```c
int putretrieveendsets(typetask *taskptr, typespecset fromset, typespecset toset, typespecset threeset)
{
    putnumber (taskptr->outp, RETRIEVEENDSETS);
    putitemset (taskptr, (typeitemset)fromset);   // always
    putitemset (taskptr, (typeitemset)toset);     // always
    putitemset (taskptr, (typeitemset)threeset);  // always
}
```

There is no conditional — the caller `fns.c:357` always passes `&fromset`, `&toset`, and `&threeset`:

```c
doretrieveendsets (taskptr, specset, &fromset, &toset, &threeset)
```

---

### Empty Roles Are Included

`putitemset` [putfe.c:124-141] writes a count first:

```c
int putitemset(typetask *taskptr, typeitemset itemset)
{
  INT i;
  typeitemset temp;
    for (temp = itemset, i = 0; temp; temp = ..., ++i) { ... }
    putnumber (taskptr->outp, i);          // writes 0 if itemset is NULL
    for (; itemset; ...) { ... }           // loop body never executes for NULL
}
```

An empty endset writes count=`0~` and no item data. The slot is always present on the wire.

**How an empty sporglset becomes NULL:** `linksporglset2specset` [sporgl.c:97-123] sets `*specsetptr = NULL` at line 102, then loops over the sporglset. If the sporglset is empty (no content found at that role's prefix in the spanfilade), the loop never runs and `*specsetptr` stays NULL:

```c
bool linksporglset2specset(..., typesporglset sporglset, typespecset *specsetptr, ...)
{
    *specsetptr = NULL;                    // line 102: initialized to NULL
    for (; sporglset; sporglset = ...) {   // never enters if sporglset is NULL
        ...
    }
    return (TRUE);                         // returns TRUE — not an error
}
```

---

### Mixed-Arity: What Gets Searched

`retrieveendsetsfromspanf` [spanf1.c:190-235] defines three search windows in the spanfilade's ORGLRANGE dimension:

```c
fromspace.stream.mantissa[0]  = LINKFROMSPAN;   // 1
tospace.stream.mantissa[0]    = LINKTOSPAN;     // 2
threespace.stream.mantissa[0] = LINKTHREESPAN;  // 3
```

Then calls `retrievesporglsetinrange` for each. That function [spanf1.c:237-267] does `retrieverestricted` against the spanfilade indexed by SPANRANGE-in, ORGLRANGE-out — it retrieves every link I-address whose stored span intersects the query. Links with no type endset simply have no LINKTHREESPAN entry in the spanfilade, so they contribute nothing to `threesporglset`.

This is confirmed by how links are created. `insertendsetsinspanf` is called from `docreatelink` [do1.c:219]:

```c
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

And `insertspanf` [spanf1.c:15-53] iterates over a sporglset — if the sporglset is NULL (empty type endpoint), the inner loop `for (; sporglset; ...)` never runs, so nothing is written at LINKTHREESPAN for that link. There is nothing to retrieve later.

---

### Mixed-Arity Summary

The three endsets are **flat per-role unions across all matching links**, not per-link tuples:

| Role | What it contains |
|------|-----------------|
| fromset | union of from-spans across all matching links |
| toset | union of to-spans across all matching links |
| threeset | union of type-spans across only links that have a type endset |

For a store with both 2-arity links (no type) and 3-arity links (with type):
- The from and to endsets include contributions from all links.
- The type endset includes spans only from the 3-arity links.
- The type endset may be non-empty, empty, or have entries from only a subset of the links.
- In all cases **the type-endset slot is present in the response** — it is never omitted, only count-zero.

There is no per-link structure: you cannot determine from RETRIEVEENDSETS alone which from-span corresponds to which to-span. To correlate endpoints by link, you must use `FINDLINKSFROMTOTHREE` to get individual link IDs, then `FOLLOWLINK` per link.
