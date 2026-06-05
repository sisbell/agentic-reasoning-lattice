## Question 15 [evidence]

> When a SpecSet references V-positions with no backing POOM entry (a gap or deleted range), are those positions silently filtered during I→V resolution, or does delivery fail?

## KB Synthesis

Silent filtering — positions with no POOM entry are dropped, not rejected.

## V→I Resolution for Absent POOM Entries

The core mechanism is `retrieverestricted()`, which walks the POOM tree for the requested V-range. When a V-position has no backing POOM crum — because the content was deleted or the range is a gap — `retrieverestricted()` returns no contexts for that position. The resulting I-span set is simply smaller; no error is raised and the operation continues with whatever positions did resolve.

This is confirmed by three converging pieces of evidence:

**[EC-SEARCH-SPEC-BEYOND-BOUNDS]** directly tests this case: after deleting content that shrinks a document, `find_links()` called with a specset covering the original (now-deleted) V-range "gracefully intersects with whatever content remains" — the backend clips to the current V-stream extent rather than rejecting.

**[INV-ITOV-FILTERING]** establishes the universal principle through `[SS-FOLLOWLINK]`: `retrieverestricted()` returns NULL for absent POOM mappings, and "the I-address is silently dropped — no V-span is added to the result." The same `retrieverestricted()` call handles both V→I and I→V directions, so the silent-drop behavior is shared.

**[PRE-RETRIEVE-CONTENTS]** (Finding 0027) identifies the *actual* failure condition: the **document** must be open. If `findorgl()` can't find the document's orgl in the open list, the entire `retrieve_contents` call fails with a backend error. This is a document-level precondition, not a position-level one — absent positions within an open document are silently omitted.

## Summary

| Situation | Result |
|---|---|
| V-position gap / deleted content, document open | Position silently omitted from I-span result; partial delivery |
| Referenced document not open | Operation fails (`findorgl` returns FALSE) `[PRE-RETRIEVE-CONTENTS]` |
| V-position in link subspace (2.x) treated as text | Garbage bytes returned (link ISA dereferenced in permascroll) `[PRE-RETRIEVE-CONTENTS]` Finding 0010 |

---

## Code Exploration

I now have enough to answer definitively. Here is the complete trace:

---

## I→V Resolution with Missing POOM Entries: Silent Filtering, Not Failure

### Entry Point: `specset2ispanset` [do2.c:14–46]

When `doretrievev` [do1.c:338–346] processes a SpecSet, it calls `specset2ispanset` to convert V-specs to I-spans, then passes those I-spans to `ispanset2vstuffset` for content retrieval.

For each `VSPECID` item in the SpecSet, `specset2ispanset` calls:

```c
ispansetptr = vspanset2ispanset (taskptr, docorgl,
    ((typevspec *)specset)->vspanset, ispansetptr)
```
[do2.c:36]

### The Permutation Path

`vspanset2ispanset` [orglinks.c:397–402] delegates immediately:

```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```

`permute` [orglinks.c:404–422] saves the original output pointer and loops over each V-span:

```c
save = targspansetptr;
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                  restrictionindex, targspansetptr, targindex);
}
return (save);
```

It **always returns `save`** — the original (non-null) pointer to the output accumulator. This means `vspanset2ispanset` never returns NULL, so the boolean guard in `specset2ispanset` [do2.c:34–38] never triggers a `return FALSE` on this path.

### The POOM Search: `span2spanset` [orglinks.c:425–454]

`span2spanset` calls `retrieverestricted` to find POOM crums covering the requested V-span:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr,
                              restrictionindex, (typespan*)NULL,
                              targindex, (typeisa*)NULL);
```
[orglinks.c:435]

This chains to `retrieveinarea` [retrie.c:87–110] → `findcbcinarea2d` [retrie.c:229–268].

### The Crum Walk: `findcbcinarea2d` [retrie.c:229–268]

`findcbcinarea2d` walks the POOM node tree and applies `crumqualifies2d` [retrie.c:270–305] to each crum. `crumqualifies2d` tests whether the crum's V-dimension intersects the requested span:

```c
endcmp = iszerotumbler (span1end) ? TOMYRIGHT :
         whereoncrum (crumptr, offset, span1end, index1);
if ( endcmp <=/*=*/ ONMYLEFTBORDER){ return(FALSE); }

startcmp = whereoncrum (crumptr, offset, span1start, index1);
if( (startcmp > THRUME)){ return (FALSE); }
```
[retrie.c:282–290]

**If no POOM crum covers the requested V-address range** — because it's a gap, never-inserted, or deleted range — every crum in the walk fails `crumqualifies2d` and the loop at retrie.c:252 completes without writing anything to `*headptr`. The function returns with `*headptr` (the context accumulator) still NULL.

### The NULL Context Branch: `span2spanset` [orglinks.c:439–453]

Back in `span2spanset`, the returned context is NULL:

```c
for (c = context; c; c = c->nextcontext) {        // never entered
    context2span (c, restrictionspanptr, ...);
    nextptr = (typespan *)onitemlist (...);
}
if(!context){
    return(targspansetptr);  // returns unchanged — no spans added
}
```
[orglinks.c:439–448]

The for-loop body never executes. The `if(!context)` guard is hit, and the function **returns the target spanset pointer unchanged**. No entry is added to the I-span accumulator. No error.

### The Empty I-Span Result

`permute` returns `save` (the original pointer). `vspanset2ispanset` returns it. `specset2ispanset` gets a non-NULL return, evaluates the boolean `&&` as true, and continues — returning `TRUE` [do2.c:45].

`ispanset2vstuffset` [granf1.c:58–74] receives `ispanset = NULL` (empty). Its loop body:

```c
for (; ispanset; ispanset = ispanset->next) {
    vstuffsetptr = ispan2vstuffset (...);
}
return (TRUE);
```
[granf1.c:67–73]

never fires. It sets `*vstuffsetptr = NULL` [granf1.c:66] and returns `TRUE`.

`doretrievev` [do1.c:343–345] returns `TRUE` with `*vstuffsetptr == NULL`.

---

## Answer

**V-positions with no backing POOM entry are silently filtered. Delivery does not fail.**

The full chain — `findcbcinarea2d` → `span2spanset` → `permute` → `vspanset2ispanset` → `specset2ispanset` → `ispanset2vstuffset` — completes successfully (`TRUE`) at every level. The unreachable V-addresses simply produce no I-spans and no content. The caller receives a successful return with an empty vstuffset (`*vstuffsetptr == NULL`), indistinguishable from a retrieve over a legitimately empty region.

The only error path that touches this chain — the `return(FALSE)` at [do2.c:37] — fires only if `findorgl` fails (document not found) or `vspanset2ispanset` returns NULL; neither happens when the document exists but the V-positions are gaps.
