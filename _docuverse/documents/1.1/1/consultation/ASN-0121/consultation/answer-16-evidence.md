## Question 16 [evidence]

> Does the operation distinguish directionality — i.e., would a link whose source references the to-set content and whose target references the from-set content be excluded because the from/to slots are matched positionally rather than symmetrically?

## KB Synthesis

Yes, the operation is **positional, not symmetric**.

The spanfilade is a 2D structure where the ORGLRANGE dimension encodes endpoint type as three distinct subspaces: LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3 [INT-SPORGL-LINK-INDEX, SS-RETRIEVE-ENDSETS]. When `find_links(from=X, to=Y)` is called:

- X's I-addresses are matched against LINKFROMSPAN entries (orgl=1)
- Y's I-addresses are matched against LINKTOSPAN entries (orgl=2)
- The result is the intersection of both matches [ST-FIND-LINKS Finding 0029]

A link created with source=Y and target=X stores its endpoints under LINKFROMSPAN keyed by Y's I-addresses and LINKTOSPAN keyed by X's I-addresses. Querying with from=X, to=Y would find no intersection in either slot — X doesn't appear in LINKFROMSPAN (Y does), and Y doesn't appear in LINKTOSPAN (X does). That link would be excluded.

This is confirmed by the single-endpoint search behavior: `find_links(NOSPECS, target_specs)` explicitly searches *only* LINKTOSPAN, and a source-based query searches *only* LINKFROMSPAN [SS-LINK-ENDPOINT Finding 0005]. The slots are not interchangeable.

---

## Code Exploration

I have all the evidence needed. Here is the complete answer.

---

## Yes — Link Direction Is Strictly Positional

The from/to slots are matched by their **stored slot index**, not by content identity. A link whose source-argument references the to-set content and whose target-argument references the from-set content would be excluded from any query that passes those arguments in the same positional order, because the index is keyed on slot number.

---

### How Link Endpoints Are Stored

#### Constants — `xanadu.h:36-38`
```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
```

These are the discriminating values baked into the spanfilade index.

#### At creation — `do1.c:195` → `do2.c:116-128`

`docreatelink` converts `fromspecset` and `tospecset` into sporgl sets and calls `insertendsetsinspanf`:

```c
// do2.c:119-120
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
  && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)
```

Inside `insertspanf` (`spanf1.c:22`):

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

This prepends the `spantype` constant (`LINKFROMSPAN=1` or `LINKTOSPAN=2`) to the link's ISA tumbler as the ORGL-dimension key. The index entry for each content address looks like:

```
SPANRANGE key = content I-span
ORGLRANGE key = (spantype . linkISA)
```

So for a link `L` created with `from=A, to=B`:
- A's content spans are indexed under `(LINKFROMSPAN=1, L)`
- B's content spans are indexed under `(LINKTOSPAN=2, L)`

---

### How Link Lookup Enforces Position — `spanf1.c:56`

`findlinksfromtothreesp` runs two independent spanfilade lookups and intersects them:

```c
// spanf1.c:77
sporglset2linkset(taskptr, spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
// spanf1.c:85
sporglset2linkset(taskptr, spanfptr, tosporglset,  &tolinkset,   orglrange, LINKTOSPAN);
// spanf1.c:100
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

Inside `sporglset2linksetinrange` (`sporgl.c:256-261`):

```c
if (orglrange) {
    prefixtumbler(&orglrange->stream, spantype, &range.stream);
    context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                                 &range, ORGLRANGE, (typeisa*)infoptr);
} else {
    context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                                 (typespan*)NULL, ORGLRANGE, (typeisa*)infoptr);
}
```

The retrieval query is: *find entries where the SPAN-dimension overlaps the candidate content, AND the ORGL-dimension is prefixed with `spantype`*. The `spantype` discriminates from-slot from to-slot at the index level.

---

### The Directional Exclusion

Given link `L` created with `from=A, to=B`, a query with `from=B, to=A`:

1. **from-query on B with `LINKFROMSPAN=1`:** The spanfilade has B indexed under `LINKTOSPAN=2`. No entries match under prefix `1`. `fromlinkset = NULL`. The function returns immediately (early-exit at `spanf1.c:78-82`):
   ```c
   if (!fromlinkset) {
       *linksetptr = NULL;
       return (TRUE);
   }
   ```

2. **L is excluded entirely** — the search never even reaches the to-query for A.

The reversed query `(from=B, to=A)` returns no links. There is no fallback, no symmetric search.

---

### The Follow Operation Also Uses Position — `do1.c:223`, `sporgl.c:67`

`dofollowlink` takes a `whichend` parameter:

```c
// do1.c:228-230
link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
```

Inside `link2sporglset` (`sporgl.c:80-83`):

```c
tumblerclear(&zero);
tumblerincrement(&zero, 0, whichend, &vspan.stream);  // offset = whichend
tumblerincrement(&zero, 0, 1, &vspan.width);
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, ...))
```

`whichend` is a V-space offset into the link document, set by `setlinkvsas` (`do2.c:169-183`):

```c
// fromvsa at V-offset 1 (0.1.1)
tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);
tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);

// tovsa at V-offset 2 (0.2.1)
tumblerincrement(tovsaptr, 0, 2, tovsaptr);
tumblerincrement(tovsaptr, 1, 1, tovsaptr);
```

Following with `whichend=1` retrieves what was passed as `fromspecset`; `whichend=2` retrieves `tospecset`. The caller must know which end they want — there is no symmetric traversal.

---

### Summary

The from/to slots are positional at two independent levels:

| Level | Mechanism | Source |
|-------|-----------|--------|
| Spanfilade index | Content stored under `LINKFROMSPAN=1` vs `LINKTOSPAN=2` prefix | `xanadu.h:36-37`, `do2.c:119-120`, `spanf1.c:22` |
| Link V-space | From-endpoint at V-offset 1, to-endpoint at V-offset 2 | `do2.c:171-176`, `sporgl.c:81` |

A link whose source argument references the to-set content and whose target argument references the from-set content would be **excluded** from a search that passes those content addresses in the reversed positional slots. The system does not attempt symmetric matching at any point in the call chain.
