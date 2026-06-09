## Question 3 [evidence]

> When a COPY/transclusion span covers V-positions that have no current binding in the source arrangement, does udanax-green reject the operation, skip the unbound positions, or something else?

## KB Synthesis

The KB points consistently to **silent omission** of unbound positions — the operation does not reject, and it does not error; it simply produces nothing for the unbound portion.

The evidence chains through two interlocking mechanisms:

**V→I conversion silently drops gaps.** The COPY source path runs: specset → `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` against the source POOM. `retrieverestricted` finds all POOM entries within the requested V-range. If no entries exist in the range (unbound positions), the function returns NULL, and the sporgl accumulation loop in `vspanset2sporglset` simply produces nothing for that portion [SS-VSPAN-TO-SPORGL, SS-POOM-MULTIMAP].

**The I→V filtering invariant confirms the pattern.** [INV-ITOV-FILTERING] states this is universal: "unreferenced I-addresses are silently excluded from V-address results." [SS-FOLLOWLINK] makes it concrete — "`retrieverestricted` returns NULL and the I-address is silently dropped — no V-span is added to the result." The same `retrieverestricted` is in the V→I path; it returns empty when there is nothing to find.

**Boundary evidence.** [EC-SEARCH-SPEC-BEYOND-BOUNDS] shows the same pattern for `find_links`: a spec referencing deleted (thus unbound) positions does not error — "the backend clips the spec to the current V-stream extent." [PRE-ZERO-WIDTH] confirms queries over empty ranges return success with empty results.

**Consequence for the target.** Because the V→I conversion produces an empty or reduced ispanset, `insertpm` and `insertspanf(DOCISPAN)` in the target receive only the I-spans that actually existed at bound positions in the source [ST-COPY, ST-VCOPY]. The target's POOM and spanfilade are updated only for the positions that had content.

So a COPY specset spanning both bound and unbound source V-positions produces a partial transclusion of only the bound content, with no error and no indication of the omission.

---

## Code Exploration

## Answer: Unbound V-Positions Are Silently Skipped

udanax-green does **not** reject the operation. It silently skips any V-positions that have no current binding and returns success with only the bound portions transcluded.

---

### Call Chain

```
fns.c:copy → do1.c:docopy → do2.c:specset2ispanset
  → orglinks.c:vspanset2ispanset → orglinks.c:permute
    → orglinks.c:span2spanset → retrie.c:retrieverestricted
```

---

### Step-by-Step with Citations

**1. Entry point — `fns.c:35–47`**

```c
void copy(typetask *taskptr)
{
    if (   getcopy(taskptr, &docisa, &vsa, &localspecset)
        && docopy(taskptr, &docisa, &vsa, localspecset))
        putcopy(taskptr);
    else
        putrequestfailed(taskptr);
}
```

Success/failure flows entirely through `docopy`.

**2. `docopy` — `do1.c:54–65`**

```c
return (
   specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa(vsaptr, docorgl)
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)
&& insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
);
```

`specset2ispanset` converts V-spans to I-spans before `insertpm` runs.

**3. V→I conversion — `do2.c:30–36`**

```c
if (!(
  findorgl(taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
  && (ispansetptr = vspanset2ispanset(taskptr, docorgl,
                      ((typevspec *)specset)->vspanset, ispansetptr))
)) {
    return(FALSE);
}
```

This calls `vspanset2ispanset` → `permute` → `span2spanset` for each span.

**4. `span2spanset` — `orglinks.c:435–448` — the critical path**

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr,
                              restrictionindex, (typespan*)NULL,
                              targindex, (typeisa*)NULL);

for (c = context; c; c = c->nextcontext) {   // skipped if context==NULL
    context2span(c, ...);
    nextptr = (typespan *)onitemlist(taskptr, ...);
}
if (!context) {                               // guard for unbound case
    return(targspansetptr);                   // returns unchanged — no error
}
contextfree(context);
return (&nextptr->next);
```

When a V-position has no binding, `retrieverestricted` returns `NULL` (`retrie.c:84`). The `for`-loop at `orglinks.c:439` never executes. The `!context` guard at `orglinks.c:446` causes early return — **nothing is added to the result span set, no error is raised**.

**5. `retrieverestricted` — `retrie.c:83–84`**

```c
temp = retrieveinarea(fullcrumptr, &span1start, &span1end, index1,
                       &span2start, &span2end, index2, ...);
return(temp);   // NULL if no bindings found in that range
```

Returns `NULL` cleanly when no enfilade crums cover the requested V-range.

**6. `acceptablevsa` — `do2.c:110–113`**

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return(TRUE);
}
```

**No validation whatsoever.** The destination VSA is accepted unconditionally regardless of source coverage.

**7. `insertpm` — `orglinks.c:100–133`**

```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    // ... insertion code ...
}
return(TRUE);   // succeeds even if sporglset was NULL/empty
```

If the I-span set produced by the V→I conversion is empty (all positions unbound) or partial (some unbound), `insertpm` loops over whatever was produced and returns `TRUE`. Nothing forces it to fail.

---

### Conclusion

**When a COPY span covers V-positions with no binding in the source arrangement:**

| Stage | Behavior |
|---|---|
| `retrieverestricted` | Returns `NULL` — no context found |
| `span2spanset` | Silently skips the `for`-loop, returns unchanged |
| `specset2ispanset` | Produces a partial or empty I-span set — no error |
| `acceptablevsa` | Always returns `TRUE` — no coverage check |
| `insertpm` | Loops over what exists, returns `TRUE` even if empty |
| `docopy` | Returns `TRUE` — COPY succeeds |

The operation **silently skips** unbound V-positions. No error, no rejection — only the bound portions get transcluded into the destination. The caller receives a success response (`putcopy`) with no indication that any positions were skipped.
