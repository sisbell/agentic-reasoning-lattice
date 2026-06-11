## Question 2 [evidence]

> Does any udanax-green read operation enumerate, filter, or aggregate over link types (e.g., return the set of types occurring among matched links, or count links grouped by type), or do types appear in the read path solely as caller-supplied type-set parameters to queries like findlinksfromtothree?

## KB Synthesis

Based on a synthesis of the KB, **link types appear in the read path solely as caller-supplied type-set parameters — no read operation enumerates, aggregates, or groups links by type.**

## Evidence

**Types as caller-supplied filter parameters**

`FINDLINKSFROMTOTHREE` (and its count wrapper `FINDNUMOFLINKSFROMTOTHREE`) accept a THREE spec parameter [SS-FIND-LINKS, Finding 0035]. This works exactly like the from/to parameters: the caller supplies a type specset, which is converted to I-addresses, and results are filtered by I-address intersection in the spanfilade. The caller must already know which type to search for; the operation does not return a type vocabulary or enumerate types across matches.

`FINDNUMOFLINKSFROMTOTHREE` counts total matching links for the caller-supplied query — it does not group by type or return per-type counts [SS-FIND-LINKS, Finding 0035].

**Types as returned endsets (value, not aggregation)**

`RETRIEVEENDSETS` (opcode 28) returns three specsets simultaneously: from-endset, to-endset, and three-endset [SS-RETRIEVE-ENDSETS, Finding 0035]. The three-endset is the type endpoint value for whatever links intersect the queried content region — but this is a per-link endset resolution, not a set of distinct types across a result set. The caller still receives raw specset data that resolves via `FOLLOWLINK` to the bootstrap document addresses like `1.0.2.2` (JUMP), `1.0.2.6` (FOOTNOTE), etc. [SS-LINK-ENDPOINT, Finding 0024].

`FOLLOWLINK` with whichend=3 (TYPE/THREE) returns the type endset for a single known link [SS-FOLLOW-LINK, Finding 0028; SS-FOLLOWLINK, Finding 0048]. Requires knowing the link ID; provides no across-link enumeration.

**Type filter is broken anyway**

[EC-TYPE-FILTER-NONFUNCTIONAL, Finding 0029] confirms that even the caller-supplied type filter is non-functional: `find_links(source, NOSPECS, type_spec)` returns empty results even when unfiltered search finds links of those types.

## Summary

The type endpoint participates in the read path in two roles only:

1. **Filter input** — caller-supplied THREE spec passed to `findlinksfromtothree` (currently broken per [EC-TYPE-FILTER-NONFUNCTIONAL])
2. **Endset output** — returned alongside from/to endsets by `RETRIEVEENDSETS`, or individually by `FOLLOWLINK(link_id, THREE)`

No operation enumerates distinct types occurring among a matched link set, groups results by type, or produces any type-level aggregation. The system has no vocabulary-query capability and no type-axis traversal — types are opaque content references (VSpecs into the bootstrap document) treated identically to source and target endpoints.

---

## Code Exploration

I have a complete picture. Here is the full answer.

---

## Answer

No read operation in udanax-green enumerates, filters over, aggregates, or groups by link type as a first-class activity. **The "three" endpoint — which represents link type in Xanadu's model — appears in the read path in exactly two ways, and both are structurally per-link, not set-aggregating.**

---

### Background: What "type" means in udanax-green

In Xanadu's link model a link has three endpoints stored at fixed V-space positions within the link's own orgl:

```
LINKFROMSPAN = 1   [xanadu.h:36]
LINKTOSPAN   = 2   [xanadu.h:37]
LINKTHREESPAN = 3  [xanadu.h:38]
```

A link's "type" is the content stored at its THREE endpoint (V-position 3.x). There is no separate categorical type field. The type is just another span of permascroll content, treated symmetrically with FROM and TO. The spanfilade indexes all three endpoint kinds under a prefixed key: `prefixtumbler(&orglrange->stream, spantype, &range.stream)` [`sporgl.c:257`], where `spantype` is one of the three constants above.

---

### Use 1 — Caller-supplied filter parameter (read INPUT)

Three query entry points all accept `threevspecset` as an **input filter** specifying what content must appear at the THREE endpoint for a link to match:

```
findlinksfromtothree        [fns.c:189]
findnumoflinksfromtothree   [fns.c:204]
findnextnlinksfromtothree   [fns.c:219]
```

All three delegate to `dofindlinksfromtothree` → `findlinksfromtothreesp` [`do1.c:348–352`, `spanf1.c:56–103`]. That function converts each specset to a sporglset and calls `sporglset2linkset` separately for each endpoint, then **intersects** the three resulting link sets:

```c
// spanf1.c:56–103
if (fromvspecset)
    sporglset2linkset(taskptr, spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
if (tovspecset)
    sporglset2linkset(taskptr, spanfptr, tosporglset, &tolinkset,    orglrange, LINKTOSPAN);
if (threevspecset)
    sporglset2linkset(taskptr, spanfptr, threesporglset, &threelinkset, orglrange, LINKTHREESPAN);
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

`sporglset2linkset` [`sporgl.c:222–237`] calls `sporglset2linksetinrange` [`sporgl.c:239–269`], which calls `retrieverestricted` with `spantype`-prefixed range keys to find all link ORGLs that have the caller's content indexed at that endpoint. The result is a flat list of link addresses. There is no type in the output — only the link ISA tumblers that survived the intersection.

`findnumoflinksfromtothree` just counts the resulting list [`spanf1.c:112`]; `findnextnlinksfromtothree` pages through it [`spanf1.c:130–147`]. Neither operation adds type information to the response.

The caller must already know the type content address they are filtering by. The backend performs the match but returns only link ISAs — no type labels, no type distribution, no grouping.

---

### Use 2 — Per-link endpoint retrieval (read OUTPUT, for one specific link)

**`followlink`** [`fns.c:114–127`] takes a specific link ISA and an integer `whichend` chosen by the caller, and returns the content at that endpoint. `dofollowlink` [`do1.c:223–232`] calls:

```c
link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
```

Inside `link2sporglset` [`sporgl.c:67–95`]:

```c
tumblerincrement(&zero, 0, whichend, &vspan.stream);   // whichend selects which V-position
tumblerincrement(&zero, 0, 1, &vspan.width);
context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, ...);
```

So passing `whichend = 3` (equal to `LINKTHREESPAN`) retrieves the THREE endpoint content from one specific link's orgl. The caller can thus read the type address for a link they already know. `linksporglset2specset` then converts the raw I-space result back to a specset for the client [`do1.c:230`, `sporgl.c:97–123`].

**`retrieveendsets`** [`fns.c:350–362`] is similar but returns all three endpoints at once for a specified link (identified by specset). `retrieveendsetsfromspanf` [`spanf1.c:190–235`] looks up the spanfilade at each of the three V-range slices (`LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN`) and reconstructs specsets for all three endpoints. This is the closest thing to "reading the type" of a link, but it still applies to **one named link** at a time, not to a set.

---

### What does NOT exist

There is no operation anywhere in the codebase that:

- Takes a set of link ISAs and returns a set of their THREE endpoint contents (type-of-each)
- Groups a link result set by type and returns counts per type
- Enumerates all distinct type addresses occurring among a set of matched links
- Returns the distribution or histogram of types

Scanning for any aggregation over type across the full source confirms this: the words "group", "aggregate", "count by type", and any notion of collecting THREE endpoints across a result set are entirely absent. `findnumoflinksfromtothree` counts *matching links* not *distinct types*. `intersectlinksets` [`spanf2.c:46–120`] intersects link sets on link-address identity, making no reference to type content.

---

### Summary

| Role in read path | Operation | What "three" does |
|---|---|---|
| **Input filter** | `findlinksfromtothree`, `findnumoflinksfromtothree`, `findnextnlinksfromtothree` | Caller supplies a specset; backend uses it to restrict which links match; type is not returned |
| **Per-link output** | `followlink` (whichend=3) | Returns THREE-endpoint content for one specific link |
| **Per-link output** | `retrieveendsets` | Returns from/to/three specsets for one specific link |

Types appear in the read path only as (a) a caller-supplied filter specset matched against the spanfilade's LINKTHREESPAN index, or (b) directly-addressed content retrieved for one specific known link. There is no backend operation that inspects a collection of links and reports back what types appear among them.
