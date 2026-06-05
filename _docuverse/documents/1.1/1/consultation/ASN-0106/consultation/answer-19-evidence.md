## Question 19 [evidence]

> Across the combined result, does the operation guarantee that the union of returned V-widths equals the sum of requested span widths (no overlap, no gap), preserving a V-space bijection?

## KB Synthesis

No, the system does not guarantee a full V-space bijection. The answer has two distinct parts:

## Width Conservation in V-Space (no gap, no overlap)

Within a single subspace for a well-formed document, width is approximately conserved:

- **No gap**: INSERT shifts all entries after the insertion point by exactly the insertion width [ST-INSERT Finding 0054], and DELETE shifts entries after the deletion range [ST-DELETE Finding 0055]. This maintains V-space contiguity within each subspace. [INV-VSPAN-CONSOLIDATION] confirms spans are always maximally consolidated.
- **No overlap in V-space**: Each V-position maps to at most one I-address — this is the `poom_d` injectivity property [INV-POOM-BIJECTIVITY].

So for non-overlapping requested V-spans within the text subspace of a document not subject to pathological DELETE sequences, the union of returned widths equals the sum of requested widths.

## V-Space Bijection Is Not Preserved

Two mechanisms break the full bijection:

**1. The POOM is explicitly a multimap** [SS-POOM-MULTIMAP]: A single I-address can map to *multiple* V-positions within the same document. Self-transclusion (and general internal transclusion) creates N:1 mappings from V-space to I-space. `ispan2vspanset` returns a *set* of V-spans for a given I-span, and the return cardinality may be > 1. This means I→V is not injective — the sum of V-widths can exceed the unique I-address range.

**2. DELETE can produce negative V-positions** [INV-POOM-BIJECTIVITY, Finding 0053]: When the deletion width exceeds the shifted entry's V-position, `tumblersub` produces a negative tumbler that is stored back into the POOM. These entries occupy tree space but are unreachable by any positive-valued V-space query. The invariant is therefore weakened: "`poom_d` restricted to non-negative V-addresses is a bijection" — but the stored map is not a bijection over its full domain.

[Finding 0055] partially corrects this: the `strongsub` exponent guard prevents cross-subspace negative shifts, so the violation is confined to same-exponent, same-subspace DELETE sequences.

**Frame conditions also matter**: [FC-SUBSPACE] shows INSERT at 1.x cannot shift 2.x entries, and vice versa — so width conservation across subspaces is not guaranteed; requests spanning subspace boundaries (as [EC-VSPAN-MISLEADING-SIZE] shows for `RETRIEVEDOCVSPAN`) return a meaningless bounding box, not true content coverage.

**Summary**: Width conservation holds within a single subspace for well-formed documents [INV-VSPAN-CONSOLIDATION, FC-SUBSPACE]. Full V-space bijection does not hold because the POOM is a multimap [SS-POOM-MULTIMAP] and DELETE can corrupt V→I injectivity [INV-POOM-BIJECTIVITY].

---

## Code Exploration

Now I have everything needed for a complete answer. Let me synthesize directly from the source.

---

## Does doretrieve guarantee a V-space bijection? (No overlap, no gap, sum of widths preserved)

**Short answer: The bijection holds conditionally — when the POOM is well-formed and the requested V-span lies entirely within content-bearing V-space — but the code enforces none of those preconditions and contains at least one deliberate correctness gap.**

---

### The retrieval pipeline

The operation in question is `doretrievev` (`do1.c:338-346`):

```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr)
{
    return
       specset2ispanset (taskptr, specset, &ispanset, READBERT)
    && ispanset2vstuffset (taskptr, granf, ispanset, vstuffsetptr);
}
```

The V-space bijection question lives entirely in `specset2ispanset` → `vspanset2ispanset` → `permute` → `span2spanset` → `context2span`. Here is how each layer handles width.

---

### Layer 1: `permute` — iterates over input spans

`orglinks.c:404-422`:
```c
typespanset *permute(...) {
    /*consolidatespans(restrictionspanset);   ← COMMENTED OUT */
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
        targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, ...);
    }
    return (save);
}
```

**`consolidatespans` is dead code** (`orglinks.c:412-413`). If the caller provides overlapping or abutting V-spans, they are processed independently, potentially visiting the same POOM crums twice and producing duplicate I-regions. The code offers no protection against this.

---

### Layer 2: `span2spanset` — the gap-creation point

`orglinks.c:435,446-448`:
```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
...
if(!context){
    return(targspansetptr);   // ← EARLY RETURN — no span added
}
```

If `retrieverestricted` returns NULL for a requested V-span — meaning no POOM crums intersect that region — the function returns silently **without contributing any output span**. The output I-span set is simply shorter than the input V-span set demands. This is the primary gap mechanism. It occurs for:

- Empty V-regions not yet populated (never inserted)
- Regions after `dodeletevspan` (`orglinks.c:145-152`) removes crums from the POOM
- The link subspace (`V ≥ 2.x`) if a retrieval mistakenly crosses subspace boundaries

---

### Layer 3: `context2span` — width is preserved within a qualifying crum

`context.c:176-212`:
```c
int context2span(typecontext *context, typespan *restrictionspanptr, INT idx1,
                 typespan *foundspanptr, INT idx2)
{
    movetumbler (&restrictionspanptr->stream, &lowerbound);
    tumbleradd (&lowerbound, &restrictionspanptr->width, &upperbound);
    prologuecontextnd (context, &grasp, &reach);

    if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS)
        tumblerincrement (&grasp.dsas[idx2], 0,
                          (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
                          &grasp.dsas[idx2]);   // clip I-start up by V-overhang [line 194]

    if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER)
        tumblerincrement (&reach.dsas[idx2], 0,
                          -tumblerintdiff(&reach.dsas[idx1], &upperbound),
                          &reach.dsas[idx2]);   // clip I-end down by V-overhang [line 200]

    tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width); // [line 207]
}
```

Within a single POOM crum the mapping is 1:1 by construction (a permutation matrix). `tumblerintdiff` computes the same integer delta for both the V-axis clipping test and the I-axis adjustment (`context.c:194, 200`). Therefore: **clipped I-width = clipped V-width, per crum**. Width is conserved here provided the crum is well-formed.

---

### Layer 4: `crumqualifies2d` — the boundary condition

`retrie.c:282-300`:
```c
endcmp = iszerotumbler(span1end) ? TOMYRIGHT : whereoncrum(crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER) { return(FALSE); }   // span1end ≤ crum_left → skip [283]

startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME) { return(FALSE); }           // span1start ≥ crum_right → skip [287]
```

A crum qualifies iff `span1start < crum_right AND span1end > crum_left` — a strict half-open overlap check. For a POOM whose crums tile V-space with no gaps, every V-position in the requested span is covered by exactly one qualifying crum. The strict inequalities are self-consistent: a crum ending exactly at the span's start (`crum_right == span1start`) is excluded by `endcmp > ONMYLEFTBORDER` being false, while the next crum starting there satisfies `startcmp ≤ THRUME`. So at exact crum boundaries, no position is double-counted or omitted — **provided the POOM crums are contiguous with no gaps**.

---

### Layer 5: `putvspaninlist` — the silent-subsumption problem

`orglinks.c:365-366`:
```c
if (startcmp > LESS && endcmp < GREATER)
    return(0);   // new span completely inside existing span → silently dropped
```

When building the output V-span list, any new span that falls entirely within an already-recorded span is discarded without adjusting widths. If two different code paths produce overlapping V-spans for the same region (possible when `consolidatespans` is disabled), the overlap is silently absorbed. The total reported width will be **less than** the true union width. There is no error and no correction.

---

### `acceptablevsa` — validation that doesn't validate

`do2.c:110-113`:
```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

This function is called at the entry of `docopy` (`do1.c`) to validate a V-space address before use. It unconditionally returns TRUE. Any out-of-range or semantically invalid VSA passes through without rejection, potentially generating crums at nonsensical V-positions.

---

## Synthesis

| Property | Status | Root cause |
|---|---|---|
| **No overlaps in output** | Not guaranteed | `consolidatespans` commented out (`orglinks.c:412`); `putvspaninlist` subsumption at `orglinks.c:365` silently drops content instead of merging |
| **No gaps in output** | Not guaranteed | `span2spanset` early-return at `orglinks.c:446` when no crums match; deleted or never-inserted V-regions produce silence |
| **Width sum preserved** | Conditionally yes | `context2span` (`context.c:194,200,207`) preserves width per crum via symmetric `tumblerintdiff` clipping, but only for crums that were found |
| **V-space bijection** | Not formally guaranteed | Depends on POOM integrity; no post-condition check exists; `acceptablevsa` (`do2.c:112`) validates nothing |

**The bijection holds in the common case**: a well-formed POOM with no deleted regions, queried with non-overlapping V-spans that lie entirely within content-bearing V-space. In that case, `crumqualifies2d` finds every crum covering the span, `context2span` clips each symmetrically, and the union of returned I-widths equals the sum of requested V-widths exactly.

**The bijection fails silently** whenever: (a) any sub-span of the requested range has no backing POOM crums (`span2spanset:446`), (b) the input V-spans are contiguous or overlapping and `consolidatespans` is not running (`orglinks.c:412`), or (c) the POOM itself contains overlapping crums, which `putvspaninlist:365` can partially mask.

There is no assert, no post-condition verification, and no protocol-level acknowledgment of partial retrieval. The caller receives whatever spans happened to match, with no indication of whether the result covers the full request.
