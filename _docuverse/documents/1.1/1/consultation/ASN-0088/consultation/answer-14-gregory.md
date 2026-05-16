## Question 14 [gregory]

> When `find_links` is called with the three-way filter (from/to/three), how does the spanfilade search combine the three endset constraints — does it intersect candidate sets from each endset type independently, or does it search one endset and then filter by the others?

## KB Synthesis

## Three-Way Filter: Independent Search Then Intersection

The spanfilade searches each endset type independently and then intersects the resulting candidate sets.

### How the spanfilade is structured for this

The spanfilade indexes link endpoints across three distinct ORGLRANGE subspaces, differentiated by a prefix value:
- `LINKFROMSPAN = 1` — from-endset entries
- `LINKTOSPAN = 2` — to-endset entries  
- `LINKTHREESPAN = 3` — type/three-endset entries

[SS-RETRIEVE-ENDSETS] (Finding 0035) documents this directly: `retrieveendsetsfromspanf()` "defines three search spaces using ORGLRANGE prefixes... then for each endset type calls `retrievesporglsetinrange()` which searches the spanfilade with SPANRANGE and ORGLRANGE restrictions." Each of the three searches is independent — the SPANRANGE dimension carries the content I-address, while ORGLRANGE partitions by endpoint type.

### The intersection step

[SS-FIND-LINKS] (Finding 0035) names the combining function: `intersectlinksets()` at `backend/spanf2.c:46-120`, with complexity **O(n·m) or O(n·m·p)** depending on how many non-NOSPECS arguments are supplied. The O(n·m·p) form confirms three independent candidate lists being intersected pairwise.

[SS-FIND-LINKS] (Finding 0029) documents the AND semantics:

> When both source and target specs are provided, both endpoints must have V-stream presence for the link to be found. Single-endpoint search (passing NOSPECS for the other) requires only that endpoint's presence.

And formalizes it: `find_links(source_spec, target_spec)` ≡ `find_links(source_spec) ∩ find_links(target_spec)`.

### Summary

The mechanism is:
1. For each non-NOSPECS argument, convert the V-spec to I-addresses (sporglset)
2. Search the spanfilade restricted to the corresponding ORGLRANGE subspace (LINKFROMSPAN, LINKTOSPAN, or LINKTHREESPAN), producing a candidate link set for each
3. Intersect the resulting sets via `intersectlinksets()` — links must appear in **all** supplied candidate sets to be returned

Passing NOSPECS for an argument skips that search entirely; the absent constraint does not contribute a candidate set and thus does not constrain the intersection. [SS-FIND-LINKS] (Finding 0029) also notes that `find_links` with a zero-tumbler cursor (NOSPECS) starts from the beginning of whichever sets were searched.

One important caveat: the orgl-range dimension filter (intended to scope searches to a specific home document) is effectively disabled — `sporglset2linkset()` replaces whatever orgl range the caller passes with a hardcoded global range [EC-FIND-LINKS-GLOBAL] (Finding 0069). So while the three-endset intersection works correctly, there is no functional scoping by document.

---

## Code Exploration

## How `find_links` Combines Three Endset Constraints

The answer is: **it searches each endset independently, then intersects the three candidate sets.** It does not search one endset and filter by the others.

---

### Execution Path

**`fns.c` (entry point)**

`findlinksfromtothree()` [fns.c:189-202] receives three specsets and delegates:

```c
getfindlinksfromtothree(taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
&& dofindlinksfromtothree(taskptr, fromvspecset, tovspecset, threevspecset, ...)
```

**`do1.c` (delegation)**

`dofindlinksfromtothree()` [do1.c:348-353] is a pure pass-through to the spanfilade:

```c
return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, threevspecset, orglrangeptr, linksetptr);
```

---

### Core Algorithm: `findlinksfromtothreesp()` [spanf1.c:56-103]

This is the key function. It operates in two distinct phases:

**Phase 1 — Three independent spanfilade searches:**

```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (tovspecset)
    specset2sporglset(taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);
if (threevspecset)
    specset2sporglset(taskptr, threevspecset, &threesporglset, NOBERTREQUIRED);

if (fromvspecset) {
    sporglset2linkset(taskptr, spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
    if (!fromlinkset) { *linksetptr = NULL; return(TRUE); }  // early exit
}
if (tovspecset) {
    sporglset2linkset(taskptr, spanfptr, tosporglset, &tolinkset, orglrange, LINKTOSPAN);
    if (!tolinkset) { *linksetptr = NULL; return(TRUE); }    // early exit
}
if (threevspecset) {
    sporglset2linkset(taskptr, spanfptr, threesporglset, &threelinkset, orglrange, LINKTHREESPAN);
    if (!threelinkset) { *linksetptr = NULL; return(TRUE); } // early exit
}
```

Each call to `sporglset2linkset()` passes a different endset-type flag — `LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN` — so each search queries a distinct index region of the spanfilade. The three searches produce three independent link candidate sets.

Note the **short-circuit early exit**: if any intermediate result is empty, the whole result is immediately empty. This is an optimization, not a filter.

**Phase 2 — Intersection:**

```c
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

---

### Intersection Logic: `intersectlinksets()` [spanf2.c:46-120]

With all three sets non-null, it uses triple-nested loops:

```c
for (; temp1; temp1 = temp1->next) {
    for (temp2 = linkset2; temp2; temp2 = temp2->next) {
        for (temp3 = linkset3; temp3; temp3 = temp3->next) {
            if (tumblereq(&temp1->address, &temp2->address)
                && tumblereq(&temp2->address, &temp3->address)) {
                linkset4 = makelinkitem(taskptr, &temp1->address);
                *linkset4ptr = linkset4;
                linkset4ptr = &linkset4->next;
            }
        }
    }
}
```

A link is included in the final result only if its tumbler address appears in **all three** independent search results. The condition `temp1==temp2 && temp2==temp3` (via `tumblereq`) enforces this. `intersectlinksets()` also handles degenerate cases where only one or two filters were specified [spanf2.c:65-73], returning the sole non-null set directly without looping.

---

### Answer

The spanfilade search performs **three independent scans** — one per endset type, using the type-specific index — and then **intersects the three resulting link sets**. It does not search one endset and filter by the others. The three `sporglset2linkset()` calls are fully independent; only `intersectlinksets()` combines them, via an O(n³) triple-nested loop that requires a link to appear in all three candidate sets.
