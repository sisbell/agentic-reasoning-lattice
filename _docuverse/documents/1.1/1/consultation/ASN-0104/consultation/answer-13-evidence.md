## Question 13 [evidence]

> If a read targets a V-position that has no POOM entry (a gap in V-space), does the operation return empty, error, or silently skip — and does it distinguish "no mapping" from "zero-width span"?

## KB Synthesis

## V-Position Gap Reads: Empty, Not Error

The system returns an **empty result** and does **not error**. It also does **not distinguish** a gap from a zero-width span — both produce an empty successful return.

### Mechanism

`retrieve_contents` routes through `doretrievev` → `specset2ispanset` → `permute()` → `retrieverestricted()` [SS-DUAL-ENFILADE]. The B-tree traversal `findcbcinarea2d()` walks siblings looking for crums whose interval intersects the queried V-range [SS-ENFILADE-TREE, Finding 0041]. When no POOM crum covers the queried V-position, `retrieverestricted` returns NULL, and context accumulation via `incontextlistnd()` / `oncontextlistseq()` produces an empty linked list [SS-CONTEXT-LIST].

The same silent-drop behavior is explicitly confirmed on the I→V path: `span2spanset()` silently omits any I-address with no POOM mapping — no error raised [INV-ITOV-FILTERING, EC-GHOST-LINK]. The V→I path uses the same `retrieverestricted()` infrastructure and behaves identically.

### No-mapping vs. zero-width

`PRE-ZERO-WIDTH` establishes that `retrieve_contents(Span(1.1, 0.0))` returns `[]` successfully. A non-zero span over a gap also returns `[]` successfully [EC-SEARCH-SPEC-BEYOND-BOUNDS] — `find_links` with a spec exceeding document bounds "gracefully intersects with whatever content remains," returning what exists (nothing, if the range is entirely unmapped). The return value is indistinguishable from the zero-width case.

### What the spec must capture

The retrieval postcondition is: `result = { content | V-position ∈ query_range ∧ ∃ poom_entry mapping V-position → I-address }`. Gaps simply produce no matching entries. There is no sentinel, no error code, and no gap-indicator. A caller cannot determine from the return value alone whether a gap exists or whether the query was zero-width.

---

## Code Exploration

I have traced the complete execution path. Here is the full answer.

---

## Reading a V-Position With No POOM Entry: Gap Behavior in udanax-green

### Short Answer

A read targeting a V-position with no POOM entry **silently returns success with an empty result set** — opcode `RETRIEVEV` + item count 0. There is no error signal, no `putrequestfailed`, and no distinction between "no mapping" and "zero-width span." The system cannot tell you which of those conditions occurred.

---

### Full Execution Trace

#### Entry: `fns.c:175-187` — `retrievev`

```c
void retrievev(typetask *taskptr)
{
    if (getretrievev(taskptr, &specset)
     && doretrievev(taskptr, specset, &vstuffset))
        putretrievev(taskptr, &vstuffset);   // success path
    else
        putrequestfailed(taskptr);           // error path
}
```

The operation succeeds or fails at the level of `doretrievev`.

---

#### `do1.c:338-346` — `doretrievev`

```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr)
{
    typeispanset ispanset;
    return
       specset2ispanset(taskptr, specset, &ispanset, READBERT)
    && ispanset2vstuffset(taskptr, granf, ispanset, vstuffsetptr);
}
```

Two steps: (1) convert the V-spec to an I-span set via the POOM, then (2) fetch content from the granfilade using those I-spans.

---

#### `do2.c:14-46` — `specset2ispanset`

```c
*ispansetptr = NULL;
for (; specset; specset = ...) {
    if (...itemid == VSPECID) {
        if (!(
          findorgl(taskptr, granf, &docisa, &docorgl, type)
        && (ispansetptr = vspanset2ispanset(taskptr, docorgl,
                              vspanset, ispansetptr))))
              return (FALSE);
    }
}
return (TRUE);
```

`vspanset2ispanset` returns a pointer (either the original `ispansetptr` if nothing was found, or a pointer to the `next` field of the last found ispan). If it returns non-null, the `if(!(...))` guard is NOT triggered — the function continues and returns TRUE regardless of whether any I-spans were actually found.

---

#### `orglinks.c:397-454` — V→I Conversion Path

```c
typeispanset *vspanset2ispanset(...) {
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}

typespanset *permute(...) {
    save = targspansetptr;
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next)
        targspansetptr = span2spanset(..., targspansetptr, ...);
    return (save);   // returns the *original* pointer
}

typespanset *span2spanset(...) {
    context = retrieverestricted((typecuc*)orgl, restrictionspanptr,
                                  restrictionindex, NULL, targindex, NULL);
    for (c = context; c; c = c->nextcontext) {  // never runs if context==NULL
        context2span(...);
        nextptr = onitemlist(...);
    }
    if (!context) {
        return (targspansetptr);  // ← GAP: returns unchanged (empty)
    }
    ...
}
```

`orglinks.c:446-448` is the gap exit point. When `retrieverestricted` finds no POOM crum covering the V-span, it returns NULL, and `span2spanset` immediately returns `targspansetptr` unchanged — still pointing to a NULL ispan set.

---

#### `retrie.c:56-110` — Why `retrieverestricted` Returns NULL for a Gap

```c
typecontext *retrieverestricted(typecuc *fullcrumptr, typespan *span1ptr, ...)
{
    // sets span1start/span1end from V-span
    temp = retrieveinarea(..., span1start, span1end, index1, ...);
    return (temp);
}

typecontext *retrieveinarea(...) {
    context = NULL;
    findcbcinarea2d(..., span1start, span1end, index1, ..., &context, ...);
    return (context);
}
```

`findcbcinarea2d` at `retrie.c:229-268` walks POOM crums and calls `crumqualifies2d`. For each crum, the check at `retrie.c:282-304`:

```c
endcmp = iszerotumbler(span1end) ? TOMYRIGHT
                                 : whereoncrum(crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER) return(FALSE);   // crum is past the query span

startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME) return(FALSE);           // crum is before the query span
```

If no POOM crum covers the queried V-span, no crum passes both checks, `headptr` is never written, and `context` remains NULL throughout. `retrieverestricted` returns NULL.

---

#### `granf1.c:58-74` — `ispanset2vstuffset` With Empty Set

```c
bool ispanset2vstuffset(..., typeispanset ispanset, typevstuffset *vstuffsetptr)
{
    *vstuffsetptr = NULL;
    for (; ispanset; ispanset = ispanset->next)   // never runs: ispanset is NULL
        vstuffsetptr = ispan2vstuffset(...);
    return (TRUE);   // ← always TRUE, even with empty set
}
```

Returns TRUE with `*vstuffsetptr = NULL`.

---

#### `putfe.c:124-141` and `270-275` — Wire Encoding of Empty Result

```c
int putretrievev(typetask *taskptr, typevstuffset *vstuffsetptr) {
    putnumber(taskptr->outp, RETRIEVEV);
    putitemset(taskptr, (typeitemset)*vstuffsetptr);  // *vstuffsetptr is NULL
}

int putitemset(typetask *taskptr, typeitemset itemset) {
    for (temp = itemset, i = 0; temp; ..., ++i) {}  // i stays 0
    putnumber(taskptr->outp, i);                     // emits 0
    for (; itemset; ...) {}                          // never runs
}
```

Wire output: `RETRIEVEV` opcode, then `0` (item count). No FAILFLAG. Success.

---

### Zero-Width Span: Distinct Path, Same Result

A zero-width retrieve (`{stream: P, width: 0}`) takes a slightly different path through `crumqualifies2d`.

With `span1start = span1end = P` (both equal since width is zero):
- A crum qualifies only if `whereoncrum(P) == THRUME` — P must be **strictly inside** the crum's V-interval.
- If P equals `ONMYLEFTBORDER` exactly: `endcmp = ONMYLEFTBORDER ≤ ONMYLEFTBORDER` → **does not qualify** (`retrie.c:283`). So a zero-width query at a POOM crum's own left-border address finds nothing.
- If P is strictly inside a crum, a zero-width I-span is produced. In `context2vtext` (`context.c:277-309`), the intersection logic clips `vtlength` to zero or negative. Then `context2vstuff` at `context.c:261-263`:

```c
if (((typetext *)vstuffset)->length == 0)
    return (FALSE);
```

The zero-length text item is **discarded**. Final result: empty vstuffset, success.

---

### The `acceptablevsa` Stub

`do2.c:110-113`:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

No V-address validation exists. Any tumbler is accepted before the POOM lookup begins.

---

### Delete Is Different: Has an Explicit Zero-Width Guard

`orglinks.c:145-152`:

```c
bool deletevspanpm(..., typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);    // ← triggers putrequestfailed
    deletend(...);
}
```

**Delete of a zero-width span returns an explicit failure.** Retrieve of a zero-width span does not have this guard and succeeds silently with empty content.

---

### Summary Table

| Condition | Operation result | Wire |
|---|---|---|
| V-span fully covered by POOM crums | Success, content returned | `RETRIEVEV` + N items |
| V-span partially in a gap | Success, partial content | `RETRIEVEV` + N items (clipped) |
| V-span entirely in a gap (no POOM entry) | **Success, empty** | `RETRIEVEV` + `0` |
| Zero-width V-span in a gap | **Success, empty** | `RETRIEVEV` + `0` |
| Zero-width V-span inside a POOM crum | **Success, empty** (vtlength clamped to 0) | `RETRIEVEV` + `0` |
| Zero-width V-span at a POOM crum's left border | **Success, empty** (border excluded at `retrie.c:283`) | `RETRIEVEV` + `0` |
| Zero-width delete | **Failure** (`orglinks.c:147`) | `FAILFLAG` |

**The system makes no distinction between "no mapping" and "zero-width span" at the retrieve level.** Both produce `RETRIEVEV` + 0 items. The only observable difference is at delete time, where zero-width is explicitly rejected. A caller receiving an empty retrieve result cannot determine whether the V-address is unmapped, whether it mapped to zero-width content, or whether it hit a left-border edge case — all are indistinguishable at the protocol level.
