## Question 6 [evidence]

> How does the udanax-green type-matching machinery (e.g., the `same_type` pathway used by typed link queries) treat a link with an empty type-endset — does it skip such links, return false on all comparisons, or treat all empty-Θ links as equivalent?

## KB Synthesis

The KB does not document a `same_type` pathway by name, so I cannot answer that specific mechanism. Here is what the KB does establish about type-endset matching:

## What Is Documented

**Type filtering in `find_links` is entirely non-functional.** [EC-TYPE-FILTER-NONFUNCTIONAL] `find_links(source, NOSPECS, type_spec)` returns empty for any type_spec, even when unfiltered queries return links of those types. The three-endset is indexed at `LINKTHREESPAN=3` in the spanfilade [SS-RETRIEVE-ENDSETS], but the actual search is effectively global and ignores orgl-range scoping anyway [EC-FIND-LINKS-GLOBAL].

**Empty type-endset resolution follows the universal INV-ITOV-FILTERING rule.** [INV-ITOV-FILTERING] Any operation that performs I-to-V conversion silently drops unreferenced I-addresses. A link whose type-endset I-addresses have no current POOM mapping returns `[]` from `FOLLOWLINK(link, TYPE)` — not an error, just an empty result.

**There is an anomalous dependency: when both source AND target are fully deleted, `FOLLOWLINK(link, TYPE)` also returns empty** — even though the type references the immutable bootstrap document at `1.0.2.x`, which was never deleted. [EC-ORPHANED-LINK, Finding 0024] The KB marks this as "either a bug or an undocumented dependency of type resolution on endpoint resolution." The mechanism is unresolved in the findings.

## Bottom Line

The KB cannot tell you whether empty-Θ links are skipped, return false, or are treated as equivalent by a `same_type` test — that code path is not documented. What is documented: type filtering via `find_links` is broken (always empty), and `FOLLOWLINK` on a type-endset uses the same silent-drop I→V filtering as all other endpoints.

---

## Code Exploration

I now have everything needed for a complete, cited answer.

---

## How udanax-green Handles Links with Empty Type-Endsets

### Background: The Three-Endset Link Model

In udanax-green, links have three endsets stored at fixed virtual-space addresses (VSAs) within the link document:
- **from** (endset 1, VSA `0.1.1`)
- **to** (endset 2, VSA `0.2.1`)
- **three/Θ** (endset 3, VSA `0.3.1`) — this is the **type** endset

### 1. What "empty type-endset" means at creation

The FEBE handler `createlink` [backend/fns.c:100] reads three specsets and calls `docreatelink` [backend/do1.c:195]:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
    typespecset fromspecset, typespecset tospecset,
    typespecset threespecset, typeisa *linkisaptr)
```

The first thing that happens is conversion of each specset to a sporglset via `specset2sporglset` [backend/do1.c:214–216]:

```c
   && specset2sporglset (taskptr, fromspecset,   &fromsporglset, NOBERTREQUIRED)
   && specset2sporglset (taskptr, tospecset,     &tosporglset,   NOBERTREQUIRED)
   && specset2sporglset (taskptr, threespecset,  &threesporglset,NOBERTREQUIRED)
```

Looking at `specset2sporglset` itself [backend/sporgl.c:14–33]:

```c
bool specset2sporglset(typetask *taskptr, typespecset specset,
    typesporglset *sporglsetptr, int type)
{
    *sporglsetptr = NULL;
    for (; specset; specset = (typespecset)((typeitemheader*)specset)->next) {
        // iterate items in specset
    }
    *sporglsetptr = NULL;
    return (TRUE);
}
```

When `threespecset` is NULL:
- The loop body never executes (NULL guard)
- `*sporglsetptr` is set to NULL on both sides of the loop
- Returns `TRUE` — the call succeeds; `threesporglset = NULL`

### 2. Empty Θ-endset: not stored in the orgl

After VSA assignment via `setlinkvsas` [backend/do2.c:169–183], which **always** sets `threevsa` to tumbler `0.3.1`:

```c
   if (threevsaptr) {
       tumblerclear (threevsaptr);
       tumblerincrement (threevsaptr, 0, 3, threevsaptr);
       tumblerincrement (threevsaptr, 1, 1, threevsaptr);
   }
```

The orgl insertion guard in `insertendsetsinorgl` [backend/do2.c:136]:

```c
   if (threevsa && threesporglset) {
       if (!insertpm (taskptr, linkisaptr, link, threevsa, threesporglset)){
           return (FALSE);
       }
   } else {
       // debug message only
   }
```

`threevsa` is non-NULL (always set), but `threesporglset` is NULL → **the condition is false**. The type endset is **not written into the orgl at all**.

### 3. Empty Θ-endset: not indexed in the spanfilade

`insertendsetsinspanf` [backend/do2.c:116–128] is equally guarded:

```c
bool insertendsetsinspanf(..., typesporglset threesporglset)
{
    if (!(
        insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
      && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,  LINKTOSPAN)))
            return (FALSE);
    if (threesporglset) {                          // ← guard
        if (!insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)){
            return (FALSE);
        }
    }
    return (TRUE);
}
```

`if (threesporglset)` is false → **the link is never indexed under `LINKTHREESPAN`**. From and to are indexed unconditionally; the type slot simply has no entry.

### 4. Querying: the type-matching pathway

The query function `findlinksfromtothreesp` [backend/spanf1.c:56–103] is the core of typed link queries:

```c
bool findlinksfromtothreesp(typetask *taskptr, typespanf spanfptr,
    typespecset fromvspecset, typespecset tovspecset,
    typespecset threevspecset, typeispan *orglrange,
    typelinkset *linksetptr)
{
    fromlinkset = tolinkset = threelinkset = NULL;
    if (fromvspecset)
        specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
    if (tovspecset)
        specset2sporglset (taskptr, tovspecset,   &tosporglset,   NOBERTREQUIRED);
    if (threevspecset)
        specset2sporglset (taskptr, threevspecset, &threesporglset, NOBERTREQUIRED);
    ...
    if (threevspecset) {
        sporglset2linkset (taskptr, (typecuc*)spanfptr, threesporglset,
                           &threelinkset, orglrange, LINKTHREESPAN);  // spanf1.c:93
        if (!threelinkset) {
            *linksetptr = NULL;               // early-out: no matches
            return (TRUE);                    // spanf1.c:95–97
        }
    }
    intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
    return (TRUE);
}
```

**Case A — query has a non-NULL `threevspecset` (typed query):**
- `sporglset2linkset(..., LINKTHREESPAN)` searches for links indexed under those type spans
- Links with empty Θ-endsets were **never indexed under `LINKTHREESPAN`** → they are absent from `threelinkset`
- If `threelinkset` comes back empty (no typed links match), the function returns `*linksetptr = NULL` immediately [spanf1.c:94–97]
- If other typed links are found, `intersectlinksets` is called; empty-Θ links are still absent from `threelinkset` and cannot survive the intersection

**Result: empty-Θ links are silently excluded. They do not "compare false" — they simply do not exist in the type index.**

**Case B — query has a NULL `threevspecset` (untyped query):**
- The `if (threevspecset)` guard [spanf1.c:92] is false → no three-span search at all
- `threelinkset` remains NULL
- `intersectlinksets` with a NULL third argument [spanf2.c:64–71] short-circuits and returns whatever from/to intersection finds:
  ```c
  if (linkset1 && !linkset2 && !linkset3)
      *linkset4ptr = linkset1;
  else if (!linkset1 && linkset2 && !linkset3)
      *linkset4ptr = linkset2;
  ```
- Empty-Θ links **are** returned if they match the from/to constraints

### 5. "All empty-Θ links equivalent" — does that exist?

There is no function named `same_type`, no type-equality predicate, and no code path that groups or compares links by the presence or absence of a Θ-endset. The term does not appear anywhere in the backend source.

The intersect function `intersectlinksets` [backend/spanf2.c:46–120] only ever tests link address equality via `tumblereq` [spanf2.c:98, 109–110] — it carries no type semantics whatsoever.

---

## Summary

| Scenario | Behavior | Mechanism |
|---|---|---|
| Link created with empty Θ-endset | Type data never stored | `insertendsetsinspanf` guard [do2.c:122]; `insertendsetsinorgl` guard [do2.c:136] |
| Typed query (non-NULL `threevspecset`) against empty-Θ link | Link **excluded** (silently skipped) | Absent from `LINKTHREESPAN` index → not in `threelinkset` → missing from intersection |
| Untyped query (NULL `threevspecset`) | Link **included** normally | `if (threevspecset)` guard [spanf1.c:92] never fires; link found via from/to index |
| "All empty-Θ links are equivalent" | **Does not exist** | No `same_type` function; no equivalence grouping; no concept in the code |

The design is an **absence-of-indexing** model, not a false-comparison model. An empty Θ-endset means no type entry in the spanfilade. A typed query simply cannot find such a link because there is nothing to find. An untyped query ignores the type dimension entirely and sees the link normally.
