## Question 19 [evidence]

> For a zero-width or empty from/to/type specset, does the count return 0 cleanly, and does a specset whose I-spans match no spanfilade entry also return 0 without error?

## KB Synthesis

Both scenarios resolve cleanly based on the KB evidence, though the KB documents them indirectly rather than with a direct test of zero-width specsets against FINDNUMOFLINKSFROMTOTHREE.

**Zero-width / empty specset → count 0, no error**

[PRE-ZERO-WIDTH] establishes the query/mutation asymmetry explicitly: `retrieve_contents(Span(1.1, 0.0))` and `retrieve_contents(SpecSet())` both return empty lists with success. `find_links` is a query, not a mutation, so the same permissive behavior applies. An empty specset produces no I-spans; the I-address intersection with any spanfilade entries is vacuously empty.

[SS-FIND-LINKS] (Finding 0035) confirms FINDNUMOFLINKSFROMTOTHREE works by calling the full `findlinksfromtothreesp()` search and then walking the result list to count. An empty input specset means zero I-spans enter the spanfilade search, the search returns NULL/empty, and the count walk yields 0. That is a clean zero, not an error path.

**Valid I-spans, no spanfilade match → count 0, no error**

This is the ordinary case when searched content has no links on it. [ST-FIND-LINKS] (Finding 0029) documents normal behavior: "When multiple links share a target, deleting one source removes only that link from source-based search" — after deletion the search returns `[]`, not an error. [EC-SEARCH-SPEC-BEYOND-BOUNDS] further confirms that specs referencing positions that don't exist in the V-stream cause `find_links` to return empty results rather than errors.

**One caveat**

[PRE-ZERO-WIDTH] also establishes that zero-width specsets passed to *mutations* (specifically `create_link`) crash the backend (Bug 0017). So the safe zero-width path is confirmed only for query operations. If the specset is being assembled for a `create_link` call rather than a search, the behavior is undefined/crashing.

---

## Code Exploration

I now have everything I need. Here is the complete traced answer.

---

## Count Behavior for Zero-Width/Empty Specsets

### Entry Point

The count operation enters through `findnumoflinksfromtothreesp` [spanf1.c:105-115], which calls `findlinksfromtothreesp` [spanf1.c:56-103] and counts the resulting linked list:

```c
for (n = 0; linkset; linkset = linkset->next, ++n);
*numptr = n;
return (TRUE);
```

If `linkset` is NULL, the loop never executes, `n = 0`, and the function returns TRUE. The counter never fails — the question is whether `findlinksfromtothreesp` returns cleanly.

---

### Case 1: NULL specset (empty / no constraint for a slot)

`findlinksfromtothreesp` [spanf1.c:69-103] guards every specset slot:

```c
fromlinkset = tolinkset = threelinkset = NULL;      // line 69
if (fromvspecset)                                    // line 70 — skipped if NULL
    specset2sporglset(...);
if (fromvspecset) {                                  // line 76 — skipped if NULL
    sporglset2linkset(...);
    if (!fromlinkset) {
        *linksetptr = NULL;
        return (TRUE);                               // line 81 — clean 0
    }
}
```

**When exactly one of the three specsets is non-NULL and produces results**, the other two stay NULL. At `intersectlinksets` [spanf2.c:64-69], the "only one non-null" branch fires and returns that single linkset directly:

```c
if (linkset1 && !linkset2 && !linkset3)
    *linkset4ptr = linkset1;          // line 65
```

**When the non-NULL specset finds no matches**, `fromlinkset` (or whichever was queried) stays NULL. The early-return guard at [spanf1.c:78-81] fires:

```c
if (!fromlinkset) {
    *linksetptr = NULL;
    return (TRUE);       // count = 0, success
}
```

**Result: returns 0 cleanly.**

---

### Case 2: Non-NULL specset with zero-width spans

`specset2sporglset` [sporgl.c:14-33] iterates over the specset items. A zero-width ispan or vspan is still processed — it produces a sporgl with `sporglwidth = 0`.

That sporgl is then cast as a `typespan*` and passed to `retrieverestricted` [sporgl.c:259]:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, ...);
```

In `retrieverestricted` [retrie.c:63-65]:

```c
if (span1ptr) {
    movetumbler(&span1ptr->stream, &span1start);
    tumbleradd(&span1start, &span1ptr->width, &span1end);  // end = start when width=0
}
```

With zero width: `span1end = span1start = P`.

In `crumqualifies2d` [retrie.c:282-290]:

```c
endcmp = iszerotumbler(span1end) ? TOMYRIGHT
                                 : whereoncrum(crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER) return(FALSE);          // line 283-285
startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME) return(FALSE);                 // line 287-290
```

Because `span1start = span1end = P`, both calls probe the same point. A crum with span [L, R] qualifies **only if `L < P < R`** (strictly interior). The `ONMYLEFTBORDER` boundary condition at line 283 (`endcmp <=`) rejects any crum where P lands exactly at its left edge; `ONMYRIGHTBORDER > THRUME` at line 287 rejects exact right-edge hits.

Stored link spans represent ranges of real content and have non-zero width; a zero-width query span from an empty selection is vanishingly unlikely to land strictly inside one. In practice `context` comes back NULL, the inner loop [sporgl.c:263] does not execute, `*linksetptr` stays NULL (initialized at [sporgl.c:226]), and the count = 0 path triggers via [spanf1.c:78-81].

**Note:** `unpacksporgl` [sporgl.c:195-202] contains an explicit zero-width assertion (`qerror("zero width in unpacksporgl")`), but `unpacksporgl` is **not called** in the retrieval/count path — only in `sporglset2linksetinrange` → `retrieverestricted`, which casts the sporgl directly as a span pointer. So that assertion is not triggered.

**Result: returns 0 cleanly, no crash.**

---

### Case 3: Non-NULL specset whose I-spans match no spanfilade entry

This is the normal no-matches case. The sporgl is valid (non-zero width, valid position), but the spanfilade simply has no crums whose stored link spans overlap the query span.

`crumqualifies2d` returns FALSE for every crum → `retrieveinarea` / `findcbcinarea2d` [retrie.c:87-110, 229-268] build no context nodes → `context` is NULL → the for loop at [sporgl.c:263] is skipped → `contextfree(NULL)` at [sporgl.c:267] is a no-op → `*linksetptr` stays NULL.

Back in `findlinksfromtothreesp`, `fromlinkset` is NULL, the guard at [spanf1.c:78-81] fires:

```c
if (!fromlinkset) {
    *linksetptr = NULL;
    return (TRUE);
}
```

**Result: returns 0 cleanly, no error.**

---

### `acceptablevsa` — Always Returns TRUE

`acceptablevsa` [do2.c:110-113] is a stub:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

No validation occurs here regardless of specset content.

---

### Edge Case: All Three Specsets NULL

If all three from/to/type specsets are NULL, none of the `if (specset)` guards fire, all three linksets remain NULL, and `intersectlinksets(NULL, NULL, NULL, ...)` [spanf2.c:46] is called. Lines 64-71 correctly set `*linkset4ptr = NULL` via the `else` branch. The function then falls through to line 83, where `temp1` is never assigned (the `if (linkset1)` guard at line 83 is FALSE). The loop at line 96 — `for (; temp1; temp1 = temp1->next)` — iterates on **uninitialized** `temp1`. This is technically undefined behaviour in C.

However, this degenerate case (all three NULL) is not a valid FEBE call — the protocol requires at least one specset — and in practice `temp1` on the stack is likely zero or a near-zero address, so the loop body (which appends to `linkset4`) never executes. The function returns with `*linkset4ptr = NULL` (set at line 71), which propagates as count = 0. Risky but incidentally correct for typical stack layouts.

---

### Summary

| Input | Returns cleanly? | Count |
|-------|-----------------|-------|
| NULL specset (one or two of three null, at least one non-null) | Yes [spanf1.c:78-81] | 0 |
| Zero-width span, matches nothing | Yes [spanf1.c:78-81] | 0 |
| Valid spans, no spanfilade entry matches | Yes [spanf1.c:78-81] | 0 |
| All three specsets NULL | Technically UB on `temp1`, but returns 0 in practice | 0 |
