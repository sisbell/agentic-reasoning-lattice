## Question 11 [gregory]

> When `vspanset2sporglset` walks the POOM to convert a V-span query into I-spans, how does it handle a single V-span that maps to multiple non-contiguous I-address ranges — does it emit one sporgl per contiguous I-run, and is the splitting purely driven by POOM crum boundaries?

## KB Synthesis

Yes, `vspanset2sporglset` emits one sporgl per contiguous I-run. The splitting is driven by POOM crum boundaries, with the important caveat that crum boundaries virtually always coincide with I-address discontinuities by construction.

## The Call Chain

The conversion path is [ST-LINK-CREATE] (Finding 0037):

```
V-span
  → vspanset2sporglset (sporgl.c:35-65)
    → vspanset2ispanset  (orgls.c:397-402)
      → permute           (orgls.c:404-422)
        → span2spanset    (orgls.c:425-454)
          → retrieverestricted  (retrie.c:56-85)
```

`retrieverestricted` discovers all POOM crums whose V-range overlaps the query span. Each qualifying crum produces one context entry in the returned list. Back up in `vspanset2sporglset`, the inner loop at `sporgl.c:49-58` iterates over every I-span in that list and emits one sporgl per entry — no consolidation step exists. So yes, one sporgl per contiguous I-run.

## Why Crum Boundaries = I-Address Discontinuities

The two are essentially the same thing, by [ST-VCOPY] (Finding 0046). During insertion, `isanextensionnd` merges a new POOM mapping into an existing crum **only when both** conditions hold: (1) same `homedoc` (I-address origin document), and (2) the new range starts exactly where the existing crum ends — contiguous in **both** V and I dimensions. Separate crums therefore always represent either different homedocs or non-contiguous I-addresses (or both). There is no steady-state where two adjacent crums have the same homedoc and contiguous I-addresses — the insertion path would have merged them.

The exception: REARRANGE can displace crums across the POOM without re-running `isanextensionnd` [ST-REARRANGE] (Finding 0056). After a pivot, you could theoretically have two adjacent crums that, after displacement, now abut in I-space even though they came from different sources. Those would still produce two separate sporgls.

## Concrete Confirmation

From [ST-LINK-CREATE] (Finding 0037), when document C contains "AABB" where "AA" was transcluded from A and "BB" from B:

```
Input: 1 V-span covering all of "AABB" (V 1.1 width 0.4)

POOM crums in C:
  crum₁: V[1.1..1.3) → I-addrs from A's permascroll  (homedoc = A)
  crum₂: V[1.3..1.5) → I-addrs from B's permascroll  (homedoc = B)

retrieverestricted returns: 2 context entries
inner loop emits:           2 sporgls
  sporgl₁: origin=I-addr(A,"AA"), width=0.2, doc=C
  sporgl₂: origin=I-addr(B,"BB"), width=0.2, doc=C
```

The front end sees one contiguous V-selection; the backend decomposes it into identity-preserving I-span segments via POOM crum structure. This same mechanism is why [EC-PIVOT-LINK-FRAGMENTATION] can produce multiple endset spans after a rearrange — pivot can create crum boundaries that weren't there before, multiplying the I-spans returned for any subsequent endset query on that region.

---

## Code Exploration

I now have everything needed to trace the full execution path. Here is the complete answer.

---

## How `vspanset2sporglset` splits one V-span into multiple I-address sporgls

### Entry point [`sporgl.c:35–65`]

```c
typesporglset *vspanset2sporglset(typetask *taskptr, typeisa *docisa,
    typevspanset vspanset, typesporglset *sporglsetptr, int type)
{
    ispanset = NULL;
    if (!findorgl(taskptr, granf, docisa, &orgl, type))   // [44]
        return (NULL);
    for (; vspanset; vspanset = vspanset->next) {         // [47] one V-span at a time
        (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset); // [48]
        for (; ispanset; ispanset = ispanset->next) {     // [49] one sporgl per ispan
            sporglset = ...
            movetumbler(docisa,           &sporglset->sporgladdress);  // [53]
            movetumbler(&ispanset->stream, &sporglset->sporglorigin);  // [54]
            movetumbler(&ispanset->width,  &sporglset->sporglwidth);   // [55]
        }
    }
}
```

The outer loop advances through the V-span set one span at a time. After the inner `for` loop exhausts `ispanset` to NULL, the next outer iteration starts with a fresh `ispanset = NULL`. **One sporgl is emitted unconditionally for each ispan returned from `vspanset2ispanset`.**

---

### V→I conversion chain

**`vspanset2ispanset`** [`orglinks.c:397–402`] just calls:
```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```
`V=1`, `I=0` are defined in `wisp.h:19–20`.

**`permute`** [`orglinks.c:404–422`] iterates over the restriction span list (in this call, one V-span) and calls `span2spanset` for each:
```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next)
    targspansetptr = span2spanset(..., restrictionspanset, V, targspansetptr, I);
return (save);  // returns pointer to head of ispan list
```

**`span2spanset`** [`orglinks.c:425–454`] is where the actual POOM walk happens:
```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, V,
                              (typespan*)NULL, I, (typeisa*)NULL);  // [435]
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, V, &foundspan, I);          // [443]
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan,
                                    (typeitemset*)targspansetptr);  // [444]
}
```

---

### The POOM tree walk: `findcbcinarea2d` [`retrie.c:229–268`]

`retrieverestricted` [`retrie.c:56–85`] is called with `span2ptr = NULL`, making `span2start = span2end = 0`. It calls `retrieveinarea` which dispatches to `findcbcinarea2d` since `cenftype == POOM`.

`findcbcinarea2d` walks all sibling crums recursively:

```c
for (; crumptr; crumptr = getrightbro(crumptr)) {          // [252]
    if (!crumqualifies2d(crumptr, offsetptr,
          span1start, span1end, V,                         // V-span restriction
          span2start(=0), span2end(=0), I, NULL))          // I: unconstrained
        continue;
    if (crumptr->height != 0) {
        dspadd(offsetptr, &crumptr->cdsp, &localoffset, POOM);
        findcbcinarea2d(findleftson((typecuc*)crumptr), &localoffset, ...); // [259] recurse
    } else {
        context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr); // [262]
        incontextlistnd(headptr, context, V);               // [263] sort by V
    }
}
```

**`crumqualifies2d`** [`retrie.c:270–305`] checks the V-span constraint strictly, and the I-span constraint leniently:

```c
endcmp = iszerotumbler(span2end) ? TOMYRIGHT : ...;  // [292] span2end==0 → TOMYRIGHT always
// → I-dimension filter always passes
startcmp = whereoncrum(crumptr, offset, span2start(0), I);
// span2start==0 → every crum qualifies (origin ≥ 0)
```

So **the I-dimension filter is a no-op** (zero spans are treated as "match everything"). The qualifying filter is entirely driven by the V-span bounds. Every leaf POOM crum whose V-extent overlaps the query V-span produces exactly one context. 

**`incontextlistnd`** [`context.c:75–111`] inserts contexts into a V-ordered list (by `grasp.dsas[V]`), so the returned list is in increasing V-address order.

---

### Per-crum context → I-span: `context2span` [`context.c:176–212`]

Each context captures the crum's 2D accumulated displacement. `makecontextfromcbc` [`context.c:151–174`] records:
- `context->totaloffset`: `typedsp` = `typewid` = struct with `tumbler dsas[MAXLOXIZE]`
  - `dsas[I=0]` = I-address of this crum's origin
  - `dsas[V=1]` = V-address of this crum's origin
- `context->contextwid`: the crum's 2D width in both I and V dimensions

`context2span` clips both ends proportionally:

```c
// [186] lowerbound = query V-start, upperbound = query V-end
prologuecontextnd(context, &grasp, &reach);  // [188] grasp/reach = abs 2D crum bounds

// Clip I-start if crum starts before query V-start
if (tumblercmp(&grasp.dsas[V], &lowerbound) == LESS) {      // [191]
    tumblerincrement(&grasp.dsas[I], 0,
        (INT)tumblerintdiff(&lowerbound, &grasp.dsas[V]),    // [194]
        &grasp.dsas[I]);
}
// Clip I-end if crum extends past query V-end
if (tumblercmp(&reach.dsas[V], &upperbound) == GREATER) {   // [197]
    tumblerincrement(&reach.dsas[I], 0,
        -tumblerintdiff(&reach.dsas[V], &upperbound),        // [200]
        &reach.dsas[I]);
}
movetumbler(&grasp.dsas[I], &foundspanptr->stream);          // [206]
tumblersub(&reach.dsas[I], &grasp.dsas[I], &foundspanptr->width); // [207]
```

The clipping is proportional integer arithmetic: the I-offset shift equals exactly the V-overflow (this works because the POOM stores content with V-width and I-width locked together by construction via `insertnd` at `orglinks.c:130`).

---

### No merging pass exists

Back in `span2spanset` [`orglinks.c:444`], the function `onitemlist` simply appends the new ispan to the end of the list — there is no adjacency check, no consolidation. A `cleanupvspanlist` / `consolidatespans` function is visible in `orglinks.c:297–312` and `orglinks.c:412–413`, but both are **dead code** — wrapped in `#ifdef UnDEFined` and commented out respectively:

```c
// orglinks.c:412–413 (commented out):
/*consolidatespans(restrictionspanset);
foospanset("restrictionset after consolidation is ",restrictionspanset); */

// orglinks.c:263–312 (inside #ifdef UnDEFined block):
int cleanupvspanlist(typetask *taskptr, typevspanset *vspansetptr)
{ ... adjacent-span merging ... }
```

---

### Summary

**Yes — one sporgl per contiguous I-run, and the splitting is purely driven by POOM crum boundaries.**

The mechanism in detail:

1. `findcbcinarea2d` traverses the POOM tree recursively, testing each crum against the query V-span via `crumqualifies2d`. Every leaf crum whose V-extent overlaps the query yields exactly one context [`retrie.c:262–263`].

2. If a single V-span's address range spans content from *N* distinct POOM leaf crums (because that content was originally inserted from *N* non-contiguous I-address ranges), `retrieverestricted` returns a context list of length *N*.

3. `context2span` converts each context to one I-span, applying proportional clipping at both ends where the crum overflows the query V-bounds [`context.c:191–207`].

4. `vspanset2sporglset` emits one `typesporgl` per I-span, with no merging [`sporgl.c:50–57`]. Adjacent I-runs that happen to be consecutive at the tumbler level are **not** coalesced — consolidation code exists but is disabled.

The grain of splitting is therefore the POOM bottom-crum boundary. Two positions that are adjacent in V-space but were inserted from non-contiguous I-addresses will always appear as separate sporgls, each carrying its own `sporglorigin`/`sporglwidth` pair.
