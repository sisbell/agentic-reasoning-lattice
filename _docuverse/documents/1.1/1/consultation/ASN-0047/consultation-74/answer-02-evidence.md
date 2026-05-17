## Question 2 [evidence]

> Does udanax-green expose any link-subspace operation (followlink, endsetqueries, or similar) that traverses a contiguous run of link V-positions as a structural unit, analogous to content-subspace span operations?

## KB Synthesis

No. The KB reveals a fundamental asymmetry: link-specific operations work through I-space (ISA or content I-address), never by traversing a contiguous run of link V-positions as a structural unit.

**What link operations actually use:**

- **FOLLOWLINK** takes a single link ISA directly; it reads the link orgl by ISA from the granfilade, then converts endset I-addresses to V-addresses via a target document's POOM. No link V-position traversal occurs. [SS-FOLLOWLINK]
- **RETRIEVEENDSETS** takes a content specset, converts it to I-addresses, and searches the spanfilade. The entry point is content identity, not link V-position. [SS-RETRIEVE-ENDSETS]
- **FINDLINKS / FINDNUMOFLINKSFROMTOTHREE / FINDNEXTNLINKSFROMTOTHREE** all operate by converting query specsets to I-addresses and intersecting against the spanfilade. Pagination uses link ISA tumblers as cursors, not V-positions. [SS-FIND-LINKS, SS-PAGINATE-LINKS]

**What can touch link V-positions generically:**

Generic V-span operations (DELETEVSPAN, RETRIEVEDOCVSPANSET, RETRIEVE-CONTENTS) can be applied to the `2.x` subspace, but they treat link ISAs as opaque data — they neither aggregate multiple link entries as a semantic unit nor trigger any link-specific traversal. A `retrieve_contents` on a link V-position returns a raw `link_id` field [SS-ADDRESS-SPACE, Finding 0024], not resolved endsets. RETRIEVEDOCVSPANSET returns a bounding span descriptor for the link subspace, not a traversal of it. [SS-VSPAN-VS-VSPANSET, SS-DUAL-ENFILADE]

**Why this design follows from the architecture:**

Links at V-positions 2.1, 2.2, … are just ISA tumblers in the POOM — structurally identical to text I-addresses at 1.x positions. The system has no "span of links → batch endset resolution" operation because link structure lives in I-space (link orgls in the granfilade, indexed by the spanfilade), while V-positions are just one document's local view. The two-blade knife that enforces subspace isolation [SS-TWO-BLADE-KNIFE, FC-SUBSPACE] reflects this: subspaces are isolated storage regions, not units of semantic operation. [SS-THREE-LAYER-MODEL, SS-LINK-SPACE]

---

## Code Exploration

I now have everything needed for a definitive answer. Here is the complete analysis.

---

## Answer

**No.** Udanax-green exposes no link-subspace operation that traverses a contiguous run of link V-positions as a structural unit. The architecture provides a clear asymmetry: content-subspace spans are first-class V-range objects at the API surface, while link-subspace V-positions are internal bookkeeping addresses that never appear as the *argument* to any traversal operation.

---

### 1. What "link V-positions" actually are

There are **two distinct link-V-position contexts**, both internal:

**Within the containing document's POOM (granfilade):**  
When `docreatelink` stores a link reference into its home document, `findnextlinkvsa` [do2.c:151–166] places it in the link subspace starting at V = 2.1, then 2.2, 2.3, etc.:

```c
tumblerincrement (&firstlink, 0, 2, &firstlink);  // → 2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // → 2.1  [do2.c:157–158]
```

**Within the link's own POOM:**  
The link's three endset payload slots are pegged to hardcoded V-addresses by `setlinkvsas` [do2.c:169–183]:

```c
// from-endset at V = 1.1
tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);
tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);
// to-endset at V = 2.1
tumblerincrement (tovsaptr, 0, 2, tovsaptr);
tumblerincrement (tovsaptr, 1, 1, tovsaptr);
// three-endset at V = 3.1
tumblerincrement (threevsaptr, 0, 3, threevsaptr);
tumblerincrement (threevsaptr, 1, 1, threevsaptr);
```

These three slots are **fixed, named positions** — not a run — and are only accessed discretely.

---

### 2. `follow_link` — point query, not span traversal

`followlink` [fns.c:114–127] takes a single link ISA and a `whichend` integer. It delegates to `link2sporglset` [sporgl.c:67–95]:

```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);  // V = whichend (1, 2, or 3)
tumblerincrement (&zero, 0, 1, &vspan.width);          // width = 1
context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, ...);
                                                        // [sporgl.c:83]
```

This issues a `retrieverestricted` call against the link's own granfilade covering exactly one named V-slot: [1,2), [2,3), or [3,4). It is a **point lookup**, not a range traversal. You cannot ask `follow_link` for "all endsets in link V-positions [1.1, 3.1]" — the API takes `whichend ∈ {1,2,3}` and returns one slot.

---

### 3. `retrieve_endsets` — content-V-driven lookup through the spanfilade

`retrieve_endsets` (FEBE opcode 28) [fns.c:350–362] delegates to `retrieveendsetsfromspanf` [spanf1.c:190–235]. Its input is a **content** specset (text V-spans), not link V-positions. Internally it uses three fixed ORGLRANGE "spaces" as discriminators:

```c
fromspace.stream.mantissa[0] = LINKFROMSPAN;   // = 1  [xanadu.h:36]
fromspace.width.mantissa[0]  = 1;
tospace.stream.mantissa[0]   = LINKTOSPAN;     // = 2  [xanadu.h:37]
threespace.stream.mantissa[0] = LINKTHREESPAN; // = 3  [xanadu.h:38]
                                               // [spanf1.c:210–217]
```

These constants are **ORGLRANGE discriminators in the spanfilade**, not link-POOM V-addresses. `retrievesporglsetinrange` [spanf1.c:237–267] calls `retrieverestricted` against the spanfilade with the content V-span as SPANRANGE input and the discriminator as ORGLRANGE filter:

```c
context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE,
                              whichspace, ORGLRANGE, ...);
                                                    // [spanf1.c:245]
```

The spanfilade indexes **content V-spans → link ISAs**; the operation flows from content outward to link metadata, not from link V-positions inward. No link-subspace V-range is traversed.

---

### 4. `find_links` / `find_num_links` / `find_next_n_links` — content-driven

All three variants [fns.c:189–234] call `findlinksfromtothreesp` [spanf1.c:56–103], which converts the caller's content specsets to sporglsets and queries the spanfilade by SPANRANGE:

```c
sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset,
                  &fromlinkset, orglrange, LINKFROMSPAN);
                                              // [spanf1.c:77]
```

Again: the input is content identity (V-spans in the text subspace); the output is link ISAs. The link subspace V-positions (2.x in the containing document) are never the query argument.

---

### 5. `delete`/`remove` — structural, not semantic

`dodeletevspan` [do1.c:158–167] calls `deletevspanpm` → `deletend` on the POOM [orglinks.c:145–151]. A caller could in principle supply a V-span encompassing 2.x positions, which would excise link references from the containing document's POOM. But this is **structural deletion** — it removes POOM crums without returning link metadata. It is not a semantic traversal.

---

### 6. The content analogy that has no link counterpart

In the content subspace, `retrievev` / `retrieve_contents` (opcode 5) [fns.c:175–187] takes any V-span over 1.x, calls `doretrievev` → `ispanset2vstuffset`, and returns the bytes/content for that entire range as a unit. A caller can say "give me everything from V=1.3 to V=1.15" and get back a coherent, ordered result.

**There is no link-subspace analog to this operation.** No exposed API accepts a V-span over the link subspace (e.g., "give me all link references in V-range [2.1, 2.5]") and returns a structured result — a list of link ISAs, their endsets, etc. — treating that range as a meaningful unit.

---

### Summary

| Dimension | Content subspace | Link subspace |
|-----------|-----------------|---------------|
| V-positions exposed | Yes — 1.x spans are API arguments to insert, retrieve, delete | No — 2.x (containing-doc) and 1.1/2.1/3.1 (link-POOM) are internal only |
| Span traversal | `retrievev` / `retrieve_contents` — any V-range | None |
| Point access | `retrievev` with single-char span | `follow_link` by ISA + whichend (1/2/3) |
| Discovery direction | V-span → content bytes | Content V-span → link ISAs (via spanfilade) — never link-V-span → result |

The link subspace V-positions are the storage mechanism, not the access interface. Links are found by their content endpoints via the spanfilade [spanf1.c], not by navigating their V-position range. The FEBE protocol has no opcode that accepts a link-subspace V-span and walks it as a structural unit.
