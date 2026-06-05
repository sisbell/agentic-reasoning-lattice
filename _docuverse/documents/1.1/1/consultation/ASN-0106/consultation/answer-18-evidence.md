## Question 18 [evidence]

> Does a zero-width span included in a multi-span request contribute an empty fragment to the result, or is it silently dropped from the combined output?

## KB Synthesis

The KB gives a partial answer but cannot fully resolve this.

**What is known:**

[PRE-ZERO-WIDTH] documents the query/mutation asymmetry for zero-width spans:
- `retrieve_contents(Span(1.1, 0.0))` → returns an empty list, no error
- `retrieve_contents(SpecSet())` (empty specset) → returns an empty list, no error
- Zero-width endpoints in `create_link` → crash (Bug 0017)

So for a single zero-width span in a query, the backend returns an empty result successfully rather than erroring.

**What is not answerable from the KB:**

The KB contains no finding that tests a zero-width VSpec *embedded within a multi-span SpecSet* — e.g., `[Span(1.1, 0.5), Span(1.7, 0.0), Span(2.1, 0.3)]`. Neither [SS-SPECSET] nor [ST-VCOPY] nor [ST-SPECSET-COMPARE] address this boundary case. Whether the zero-width component contributes a structurally empty fragment (maintaining its positional slot in the result sequence) or is silently elided before processing is not empirically established in the KB.

Given [INV-SPECSET-ORDER] (VSpec ordering is preserved in results) and the single-span behavior (zero-width → empty list), the most defensible inference is that the zero-width VSpec contributes nothing to the concatenated output — but this is not directly confirmed. The spec should flag this as requiring an explicit test.

---

## Code Exploration

I now have all the code I need. Let me trace the complete execution path.

---

## Answer: Zero-Width Spans Are Silently Dropped

A zero-width span in a multi-span request contributes **nothing** to the combined output. It is silently dropped — no empty fragment appears in the result. Here is the full code trace.

---

### Entry point: `retrievev` → `doretrievev`

`fns.c:175-187` dispatches to `doretrievev`:

```c
void retrievev(typetask *taskptr)
{
    if (
       getretrievev (taskptr, &specset)
    && doretrievev (taskptr, specset, &vstuffset))
        putretrievev (taskptr, &vstuffset);
```

`do1.c:338-346`:

```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr)
{
    return
       specset2ispanset (taskptr, specset, &ispanset, READBERT)
    && ispanset2vstuffset (taskptr, granf, ispanset, vstuffsetptr);
}
```

Two stages: V→I conversion, then I→text retrieval. The zero-width span is filtered out in the second stage, or often never makes it past the first.

---

### Stage 1: V→I Conversion — `vspanset2ispanset` → `permute` → `span2spanset`

`orglinks.c:397-401` delegates via `permute`:

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, typeispanset *ispansetptr)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` (`orglinks.c:404-422`) iterates over each span in the input set and calls `span2spanset` for each. This is the iteration point for a multi-span request: **each span is processed independently**, including zero-width ones.

`span2spanset` (`orglinks.c:425-454`) calls `retrieverestricted` on the POOM enfilade with the V-span as the restriction, then calls `context2span` for each returned context.

`retrieverestricted` (`retrie.c:56-85`) computes:
```c
movetumbler (&span1ptr->stream, &span1start);
tumbleradd (&span1start, &span1ptr->width, &span1end);
```

For a zero-width span (width = 0): `span1end = span1start = P`.

The POOM search uses `crumqualifies2d` (`retrie.c:270-305`):

```c
endcmp = iszerotumbler (span1end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span1end, index1);
if ( endcmp <=/*=*/ ONMYLEFTBORDER){
    return(FALSE);
}
startcmp = whereoncrum (crumptr, offset, span1start, index1);
if( (startcmp > THRUME)){
    return (FALSE);
}
```

Since `span1start == span1end == P`, evaluating `whereoncrum` with P:

| P position relative to crum [left, right) | `endcmp` | pass? | `startcmp` | pass? | result |
|---|---|---|---|---|---|
| P < left | TOMYLEFT ≤ ONMYLEFTBORDER | **FALSE** | — | — | not qualified |
| P == left | ONMYLEFTBORDER ≤ ONMYLEFTBORDER | **FALSE** | — | — | not qualified |
| left < P < right | THRUME > ONMYLEFTBORDER | pass | THRUME, not > THRUME | pass | qualified |
| P == right | ONMYRIGHTBORDER > ONMYLEFTBORDER | pass | ONMYRIGHTBORDER > THRUME | **FALSE** | not qualified |
| P > right | TOMYRIGHT > ONMYLEFTBORDER | pass | TOMYRIGHT > THRUME | **FALSE** | not qualified |

A POOM crum qualifies only when P is **strictly interior** to the crum's V-extent. If P lands on any crum boundary — including the start or end of a text chunk — **no crum qualifies** and `context` is NULL:

```c
// span2spanset, orglinks.c:446-448
if(!context){
    return(targspansetptr);  // early return, nothing added to ispanset
}
```

If P happens to be strictly inside a crum (e.g., between two character positions within the same POOM leaf), a context IS found. Then `context2span` (`context.c:176-212`) clips the corresponding I-span to the requested V-window:

```c
movetumbler (&restrictionspanptr->stream, &lowerbound);   // P
tumbleradd (&lowerbound, &restrictionspanptr->width, &upperbound);  // P + 0 = P

if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS)
    tumblerincrement (&grasp.dsas[idx2], 0, tumblerintdiff(&lowerbound, &grasp.dsas[idx1]), &grasp.dsas[idx2]);
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER)
    tumblerincrement (&reach.dsas[idx2], 0, -tumblerintdiff(&reach.dsas[idx1], &upperbound), &reach.dsas[idx2]);

tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

With P strictly inside [grasp_V, reach_V): both adjustments apply. The resulting I-width:

```
width = (reach_I − (reach_V − P)) − (grasp_I + (P − grasp_V))
      = (reach_I − grasp_I) − (reach_V − grasp_V)
      = V-width − V-width   =   0
```

A zero-width I-span is produced and placed in the ispanset. This ispan then flows into Stage 2.

---

### Stage 2: I→text retrieval — `ispan2vstuffset`

`granf1.c:58-74` iterates over each I-span, calling `ispan2vstuffset` for each:

```c
for (; ispanset; ispanset = ispanset->next) {
    vstuffsetptr = ispan2vstuffset (taskptr, granfptr, ispanset, vstuffsetptr);
}
```

`ispan2vstuffset` (`granf2.c:286-318`) calls `retrieveinspan` on the granfilade:

```c
movetumbler (&ispanptr->stream, &lowerbound);
tumbleradd(&lowerbound, &ispanptr->width, &upperbound);   // S + 0 = S
context = retrieveinspan ((typecuc*)fullcrumptr, &lowerbound, &upperbound, WIDTH);
```

`retrieveinspan` calls `findcbcinspanseq` (`retrie.c:307-329`), which tests each granfilade crum with `crumintersectsspanseq` (`retrie.c:423-430`):

```c
bool crumintersectsspanseq(typecorecrum *crumptr, tumbler *offsetptr, tumbler *spanstart, tumbler *spanend)
{
    if (iszerotumbler (&crumptr->cwid.dsas[WIDTH])) {
        return(FALSE);
    }
    return ((whereoncrum (crumptr, (typewid*)offsetptr, spanstart, WIDTH) < ONMYRIGHTBORDER)
             && (whereoncrum (crumptr, (typewid*)offsetptr, spanend, WIDTH) >/*=*/ ONMYLEFTBORDER));
}
```

For a zero-width I-span (spanstart == spanend == S), the same analysis applies: a GRAN crum qualifies only if S is **strictly inside** it (not on either border).

If a GRAN crum does qualify (S is strictly between two character positions), `context2vstuff` (`context.c:240-275`) is called. For text crums it calls `context2vtext` (`context.c:277-309`):

```c
vtlength = textlength;
if (tumblercmp (&crumistart, &ispanstart) == LESS) {
    i = tumblerintdiff (&ispanstart, &crumistart);   // S - crumistart
    vtlength -= i;
}
if (tumblercmp (&crumiend, &ispanend) == GREATER) {
    vtlength -= tumblerintdiff (&crumiend, &ispanend); // crumiend - S
}
```

For S strictly inside [crumistart, crumiend):

```
vtlength = textlength − (S − crumistart) − (crumiend − S)
         = textlength − (crumiend − crumistart)
         = textlength − textlength   =   0
```

And then — the **explicit drop guard** at `context.c:261`:

```c
if (((typetext *)vstuffset)->length == 0)
    return (FALSE);
```

`context2vstuff` returns FALSE. In `ispan2vstuffset`:

```c
if (context2vstuff (taskptr, temp, ispanptr, &vstuffset)) {
    *vstuffsetptr = vstuffset;     // only executed if TRUE
    vstuffsetptr = ...;
}
```

Nothing is appended to the output. The zero-width span produces no vstuff entry.

---

### Summary of drop points

There are two places a zero-width span can be dropped:

1. **`crumintersectsspanseq` / `crumqualifies2d`**: If the zero-width span point P falls exactly on a crum boundary (or outside all crums), no context is found and `span2spanset` or `ispan2vstuffset` returns without producing any output.

2. **`context2vstuff` (`context.c:261`)**: Even when P is strictly interior to a crum and a context is found, `context2vtext` always computes `vtlength = 0`, which triggers the explicit guard `if (length == 0) return FALSE`. This is the definitive, unconditional backstop.

**A zero-width span always produces zero output text.** No empty fragment appears in the combined result at the position of the zero-width span; it is silently omitted from the `vstuffset`. The multi-span response looks exactly as if the zero-width span was never included in the request.
