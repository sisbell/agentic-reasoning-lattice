## Question 1 [evidence]

> When FINDDOCSCONTAINING (or its content-resolution path) receives a span whose depth is shallower than the source arrangement's positions, does udanax-green resolve it to the entire subtree under that prefix, reject it, or normalize it to the native granularity?

## KB Synthesis

The KB does not contain a direct finding testing FINDDOCSCONTAINING with depth-mismatched spans, but the answer is derivable from the tumbler arithmetic — and it points to **implicit subtree resolution**, not rejection or normalization.

## Why shallow spans act as subtree queries

From [INV-TUMBLER-TOTAL-ORDER] (Finding 0031), the total order compares mantissa digits lexicographically after exponent alignment. The KB gives the concrete example: `tumblercmp(1.1.0.2, 1.1.0.2.0.1) → LESS`. This means any address `A.0.X` (for X > 0) is strictly between `A` and `A`'s next-sibling `A+1` in the total order.

Concretely: if actual I-addresses are at `2.1.0.5.0.100` through `2.1.0.5.0.200`, and you query with span start=`2.1.0.5`, width=1 (reach=`2.1.0.6`), then:
- `2.1.0.5 < 2.1.0.5.0.100 < 2.1.0.6` (mantissa comparison at digit 3: `5 < 6`)
- `intervalcmp(2.1.0.5, 2.1.0.6, 2.1.0.5.0.100)` → **THRUME** — interior, matched

[SS-INTERVAL-CMP] confirms `intervalcmp` operates on this same total order and returns THRUME for points strictly inside the interval. The DOCISPAN entries (per-span, stored as `{stream: IAddress, width}` per [SS-DOCISPAN]) will overlap the shallow query range in exactly this way.

## No rejection or normalization

[PRE-SPECSET] (Finding 0001) explicitly states: the backend validates specsets at document granularity only and does not enforce element-level tumbler structure. A specset with shallower-than-stored addresses "is accepted without error."

[SS-SUBSPACE-CONVENTION] and multiple findings confirm there is no depth-checking in `retrieverestricted()` (described in Finding 0009 as "type-agnostic") or the POOM traversal path. `acceptablevsa()` always returns TRUE [PRE-INSERT Finding 0011].

## Caveat on width encoding

The subtree-capture behavior depends on the width being "aligned" to capture the relevant depth. A width of `0.1` at exp=-1 reaches `2.1.0.5.1`, which by the same lexicographic argument still encompasses `2.1.0.5.0.X` for all X. However, the precise arithmetic of cross-exponent tumbler addition is not exhaustively analyzed in the KB — [SS-TUMBLER] Finding 0055 notes `strongsub`'s exponent guard as a related edge case showing cross-exponent arithmetic can produce no-ops.

**Summary:** Udanax-green resolves a shallow span to the subtree under that prefix as an emergent consequence of the tumbler total order, with no explicit rejection or normalization. This is not a designed feature but a structural property of treating the address space as a numeric total order where parent addresses are numerically less than their children.

---

## Code Exploration

Now I have the complete picture. Let me write the full answer.

---

## FINDDOCSCONTAINING: Shallow Span Depth Handling

**Answer: The code resolves a shallow span to the entire subtree under that prefix — silently, via arithmetic, with no explicit normalization or rejection anywhere in the path.**

---

### Full Execution Trace

**`fns.c:20-32`** — entry point

```c
void finddocscontaining(typetask *taskptr) {
    if (
       getfinddocscontaining(taskptr, &specset)
    && dofinddocscontaining(taskptr, specset, &addressset))
        putfinddocscontaining(taskptr, (typeitemset)addressset);
    else
        putrequestfailed(taskptr);
}
```

**`do1.c:15-23`** — `dofinddocscontaining`

```c
bool dofinddocscontaining(typetask *taskptr, typespecset specset, typelinkset *addresssetptr)
{
    return (
       specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)   // do2.c:14
    && finddocscontainingsp(taskptr, ispanset, addresssetptr));          // spanf1.c:151
}
```

**`do2.c:14-46`** — `specset2ispanset` — the conversion gate

For a spec whose `itemid == ISPANID` (a directly-supplied internal span):

```c
// do2.c:24-26
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *ispansetptr = (typeispanset)specset;
    ispansetptr = (typeispanset *)&((typeitemheader *)specset)->next;
}
```

The span is threaded directly into the ispanset with **zero inspection of its depth**. No rejection, no normalization.

For a spec whose `itemid == VSPECID` (a virtual span needing V→I conversion), the path goes through `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` in `orglinks.c` — see the V→I section below. Even in that path there is no depth guard.

**`spanf1.c:151-188`** — `finddocscontainingsp` — the two-dimensional retrieval

```c
// spanf1.c:167-171
clear(&docspace, sizeof(typespan));
tumblerincrement(&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement(&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted(
        (typecuc*)spanf,
        &docspace, ORGLRANGE,    // dimension 1: scan all documents
        ispanset, SPANRANGE,     // dimension 2: the user's span
        (typeisa*)NULL);
```

The user-supplied ispan is passed directly as the `span2ptr` argument. `SPANRANGE` is the content-address dimension of the spanfilade.

---

### How the Span Boundaries Are Materialized

**`retrie.c:56-85`** — `retrieverestricted`

```c
// retrie.c:70-72  (for span2 = the user's input span)
movetumbler(&span2ptr->stream, &span2start);
tumbleradd(&span2start, &span2ptr->width, &span2end);
```

`span2start` = the span's stream tumbler verbatim.
`span2end` = `tumbleradd(stream, width)` — pure arithmetic, no depth normalization.

**`retrie.c:87-110`** → **`retrie.c:229-268`** — `findcbcinarea2d` — recursive tree descent

```c
// retrie.c:252-259
for (; crumptr; crumptr = getrightbro(crumptr)) {
    if (!crumqualifies2d(crumptr, offsetptr,
            span1start, span1end, index1,
            span2start, span2end, index2, ...))
        continue;
    if (crumptr->height != 0) {
        dspadd(offsetptr, &crumptr->cdsp, &localoffset, crumptr->cenftype);
        findcbcinarea2d(findleftson((typecuc*)crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd(headptr, context, index1);
    }
}
```

When a node qualifies, the algorithm recurses into its children. This is the mechanism that produces subtree expansion — every qualifying intermediate node fans out to all descendants.

---

### The Core: `crumqualifies2d` and `whereoncrum`

**`retrie.c:270-305`** — `crumqualifies2d`

For dimension 2 (the content-address dimension, i.e., the user's span):

```c
// retrie.c:292-300
endcmp = iszerotumbler(span2end) ? TOMYRIGHT :
         whereoncrum(crumptr, offset, span2end, index2);
if (endcmp < ONMYLEFTBORDER) return FALSE;

startcmp = whereoncrum(crumptr, offset, span2start, index2);
if (startcmp > THRUME) return FALSE;

return TRUE;
```

**`retrie.c:345-373`** — `whereoncrum` — how the comparison actually works

```c
INT whereoncrum(typecorecrum *ptr, typewid *offset, tumbler *address, INT index) {
  tumbler left, right;
  INT cmp;
  // case SPAN or POOM:
    tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);  // node's abs start
    cmp = tumblercmp(address, &left);
    if (cmp == LESS) return TOMYLEFT;
    else if (cmp == EQUAL) return ONMYLEFTBORDER;

    tumbleradd(&left, &ptr->cwid.dsas[index], &right);                 // node's abs end
    cmp = tumblercmp(address, &right);
    if (cmp == LESS) return THRUME;
    else if (cmp == EQUAL) return ONMYRIGHTBORDER;
    else return TOMYRIGHT;
}
```

The query span's start and end tumblers are compared directly against each node's absolute start and end. **No depth normalization before the comparison.**

---

### Why Shallow Spans Produce Subtree Expansion: Tumbler Arithmetic

**`tumble.c:72-111`** — `tumblercmp` and `abscmp`

```c
INT tumblercmp(tumbler *aptr, tumbler *bptr) { ... return abscmp(aptr,bptr); }

static INT abscmp(tumbler *aptr, tumbler *bptr)
{
    if (aptr->exp != bptr->exp) {  // tumble.c:92
        if (aptr->exp < bptr->exp) return LESS;
        else return GREATER;
    } else {
        a = (INT *) aptr->mantissa;
        b = (INT *) bptr->mantissa;
        for (i = NPLACES; i--;) {  // tumble.c:101 — ALL NPLACES positions
            if (!(cmp = *a++ - *b++)) {
            } else if (cmp < 0) return LESS;
            else return GREATER;
        }
    }
    return EQUAL;
}
```

The mantissa is a **fixed-size array of `NPLACES` elements**. There is no concept of "depth" in the comparison — it iterates the full array. A shallow tumbler like `1.2` has mantissa `[1, 2, 0, 0, 0, ...]`. A deep position like `1.2.3.4` has mantissa `[1, 2, 3, 4, 0, ...]`.

Comparing `span_start = 1.2` against position `1.2.3.4`:
- Position 0: `1 - 1 = 0` → equal, continue
- Position 1: `2 - 2 = 0` → equal, continue
- Position 2: `0 - 3 = -3 < 0` → **LESS**

So `1.2 < 1.2.3.4` → span start is to the LEFT of the stored position → qualifies.

Comparing `span_end = 1.3` against position `1.2.3.4`:
- Position 0: `1 - 1 = 0` → equal, continue
- Position 1: `3 - 2 = 1 > 0` → **GREATER**

So `1.3 > 1.2.3.4` → span end is to the RIGHT of the stored position → qualifies.

**The span `[1.2, 1.3)` includes every address of the form `1.2.*`.** All children of the node addressed by `1.2` satisfy both comparisons. This is pure mathematical consequence of trailing-zero mantissas — no explicit logic is needed or present.

---

### Depth Check in `ndcuts.c` — Only for Insertion, Not Query

```c
// ndcuts.c:431
if (tumblerlength(cut) != tumblerlength(&ptr->cwid.dsas[index]))
```

This check (`tumblerlength` comparison) appears only in the rearrangement/cut-sequence path, not in retrieval. The query path — `retrieverestricted` → `findcbcinarea2d` → `crumqualifies2d` → `whereoncrum` — has **no depth check** anywhere.

---

### The `tumbler2spanset` Contrast (`do2.c:48-60`)

This is instructive for what normalization *would* look like if the code intended it:

```c
bool tumbler2spanset(typetask *taskptr, typeisa *tumblerptr, typespanset *spansetptr) {
    movetumbler(tumblerptr, &spanptr->stream);
    tumblerclear(&spanptr->width);
    tumblerincrement(&spanptr->width,
        tumblerlength(tumblerptr)-1,   // do2.c:58 — depth-aware increment level
        1, &spanptr->width);
    *spansetptr = spanptr;
    return TRUE;
}
```

When the system itself creates a span from a tumbler (e.g., for link address lookup), it explicitly uses `tumblerlength() - 1` as the level argument to `tumblerincrement` — ensuring the width occupies exactly one unit at the tumbler's native depth. This is NOT done for user-supplied spans in FINDDOCSCONTAINING.

---

### V→I Conversion Path (for VSPECID inputs)

When the input spec is a virtual span (not an ispan), `specset2ispanset` calls `vspanset2ispanset` (`orglinks.c:397`) → `permute` (`orglinks.c:404`) → `span2spanset` (`orglinks.c:425`) → `retrieverestricted`. The retrieved contexts are then clipped via `context2span` (`context.c:176`):

```c
// context.c:191-196 — clipping at lower bound
if (tumblercmp(&grasp.dsas[idx1], &lowerbound) == LESS) {
    tumblerincrement(&grasp.dsas[idx2], 0,
        (INT)tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
        &grasp.dsas[idx2]);
}
// context.c:197-202 — clipping at upper bound
if (tumblercmp(&reach.dsas[idx1], &upperbound) == GREATER) {
    tumblerincrement(&reach.dsas[idx2], 0,
        -tumblerintdiff(&reach.dsas[idx1], &upperbound),
        &reach.dsas[idx2]);
}
```

Even here, the comparison is between the already-computed shallow tumbler (`lowerbound`, `upperbound`) and the stored `grasp`/`reach`. The same `tumblercmp` arithmetic applies: the shallow query boundaries naturally encompass all deeper stored addresses.

---

### Summary

There are exactly **three possible behaviors** for a shallow span:
1. **Reject it** — no guard clause exists anywhere in the path
2. **Normalize it to native granularity** — no depth normalization code exists in the retrieval path
3. **Resolve it to the entire subtree** — ✓ what actually happens

The resolution is **implicit and arithmetic**: because `abscmp` (`tumble.c:101`) iterates the full fixed `NPLACES` mantissa array without any depth adjustment, a shallow tumbler `X.Y` (with trailing zeros) compares LESS than all `X.Y.a.b.c...` addresses (any positive suffix). The span `[X.Y, X.Z)` for any Z > Y therefore matches the entire `X.Y.*` subtree.

The system was designed this way intentionally — the Xanadu address space is hierarchical, and a prefix address naturally denotes its subtree. No explicit code is needed: the tumbler arithmetic is the implementation of that semantic.
