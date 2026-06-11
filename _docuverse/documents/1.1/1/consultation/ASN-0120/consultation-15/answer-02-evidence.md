## Question 2 [evidence]

> When CREATELINK stores an endset via `vspanset2sporglset`/`permute`, is the resulting sporgl decomposition deterministic and canonical (e.g., always maximal contiguous I-runs in a fixed order), or can the same resolved I-address set be stored under different decompositions depending on input span structure?

## KB Synthesis

## Sporgl Decomposition: Deterministic but Not Canonically Maximally-Merged

The decomposition is **deterministic given fixed POOM state** but **not canonically maximally-merged in I-space**. The two questions need to be separated.

---

### Determinism

Given a fixed POOM state, the same V-span always produces the same sporgl decomposition. The path is:

`vspanset2sporglset` → `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` → `findcbcinarea2d`

`findcbcinarea2d` is a deterministic B-tree traversal [SS-DUAL-ENFILADE], and the context accumulation via `incontextlistnd` performs insertion-sort by V-position [INV-RETRIEVAL-V-SORTED], so results are always returned in the same V-sorted order regardless of tree shape [INV-RETRIEVAL-TREE-INDEPENDENCE]. No randomness participates.

---

### Granularity: POOM Crum Boundaries, Not I-Space Maximal Runs

The number of output sporgls equals the number of POOM crums that overlap the query V-span — one sporgl per crum, one I-span per crum [ST-LINK-CREATE, Finding 0037]:

> "The critical mechanism is the inner loop in `vspanset2sporglset` (sporgl.c:49-58), which iterates over every I-span returned by `vspanset2ispanset` and creates a separate sporgl for each."

Each POOM crum stores a single contiguous (V-origin, V-width) → (I-origin, I-width) mapping [SS-POOM-BOTTOM-CRUM]. If two adjacent crums happen to cover contiguous I-address ranges, they are still returned as two separate I-spans and become two separate sporgls. There is no post-hoc I-space merging step anywhere in this pipeline.

---

### When Does Merging Occur? Only at Insert Time

The `isanextensionnd` check in `insertnd` is the sole merging mechanism [ST-INSERT, Finding 0062]: when a new insertion's I-origin equals an existing crum's reach AND the homedoc matches, the crum is extended in place rather than creating a new one. This happens at COPY/INSERT time, not at link creation time. By the time `vspanset2sporglset` is called, the POOM's crum structure is fixed.

Consequence: two sequential inserts into a fresh document produce one merged crum → one sporgl. The same logical content after a DELETE+re-insert produces a new crum with different I-addresses → still one sporgl, but now a different one. The same logical content after a pivot that splits a crum can produce two crums → two sporgls.

---

### The Same Resolved I-Address Set CAN Be Stored Under Different Decompositions

Yes — the decomposition depends on POOM history, not purely on the set of I-addresses:

1. **REARRANGE breaks contiguity**: After a pivot, a previously single crum covering "ABCD" may be split into "AB" and "CD" at different V-positions [EC-PIVOT-LINK-FRAGMENTATION, Finding 0019]. A link created on the full content before vs. after pivot would have 1 sporgl vs. 2 sporgls — even though they reference identical I-addresses.

2. **Multi-span input can duplicate sporgls**: [EC-MULTISPAN-LINK-DUPLICATION] documents that links created with multiple source spans can produce duplicate spans in endset results, caused by the same crum being reached via multiple query paths.

3. **CREATELINK itself disrupts subsequent I-space contiguity** [INT-LINK-INSERT, Finding 0063]: a link orgl allocation between two text INSERTs creates a gap in the text I-address sequence, so those two INSERTs' content cannot be represented as one crum even if they are V-adjacent.

---

### Summary

| Property | Answer |
|----------|--------|
| Deterministic given fixed POOM | Yes — tree traversal + V-sorted accumulation is fully determined |
| Canonical maximally-merged in I-space | No — granularity is POOM-crum-level, not I-space maximal run |
| Same logical content always same decomposition | No — POOM history (pivot, delete+reinsert, interleaved link creation) affects crum structure, thus sporgl count |
| Order of sporgls | Fixed: V-sorted by `incontextlistnd` insertion-sort [INV-RETRIEVAL-V-SORTED] |

The formal spec for `create_link`'s endset must therefore state: `|endset| = |{crums ∈ poom(doc) | crum.vspan ∩ input_vspan ≠ ∅}|`, not `|endset| = |{maximal_contiguous_I_runs(input_vspan)}|`.

---

## Code Exploration

I now have all the source I need. Let me compile the complete answer.

---

## CREATELINK Sporgl Decomposition: Determinism and Canonicality

**Short answer:** The decomposition is **deterministic for a given fixed input vspanset + fixed enfilade state**, but is **not canonical** — the same resolved I-address set can be stored under different sporgl decompositions depending on the input V-span structure and the state of the POOM enfilade at the time of insertion. There is no maximally-merged, fixed-order canonical form.

---

### The Full Execution Path

#### 1. Entry: `fns.c:100–112` → `do1.c:195–221`

`createlink()` calls `docreatelink()`:

```c
// fns.c:100
void createlink(typetask *taskptr)
{
    if (getcreatelink(taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
    &&  docreatelink(taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa))
        putcreatelink(taskptr, &linkisa);
```

`docreatelink()` [do1.c:195–221] calls `specset2sporglset()` three times (from, to, three), then `insertendsetsinorgl()` and `insertendsetsinspanf()`:

```c
// do1.c:214–219
   && specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset,&threesporglset,NOBERTREQUIRED)
&& setlinkvsas (&fromvsa, &tovsa, &threevsa)
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, ...)
&& insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, ...)
```

---

#### 2. `sporgl.c:14–65` — V-spec to sporgl conversion

`specset2sporglset()` [sporgl.c:14–33] dispatches on item type:

```c
for (; specset; specset = ...) {
    if (itemid == ISPANID) {
        *sporglsetptr = (typesporglset)specset;   // pass through unchanged
        sporglsetptr = ...;
    } else if (itemid == VSPECID) {
        sporglsetptr = vspanset2sporglset(taskptr,
            &((typevspec*)specset)->docisa,
            ((typevspec*)specset)->vspanset,
            sporglsetptr, type);
    }
}
```

`vspanset2sporglset()` [sporgl.c:35–65] does the V→I resolution:

```c
ispanset = NULL;
findorgl(taskptr, granf, docisa, &orgl, type);
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
        sporglset = (typesporgl *) taskalloc(taskptr, sizeof(typesporgl));
        sporglset->itemid = SPORGLID;
        movetumbler(docisa, &sporglset->sporgladdress);      // home doc ISA
        movetumbler(&ispanset->stream, &sporglset->sporglorigin);  // I-addr start
        movetumbler(&ispanset->width, &sporglset->sporglwidth);    // I-addr width
        *sporglsetptr = sporglset;
        sporglsetptr = &sporglset->next;
    }
}
```

Each `typesporgl` is: `{sporgladdress = docISA, sporglorigin = I-stream, sporglwidth = I-width}`.

---

#### 3. `orglinks.c:389–454` — V→I permutation via POOM traversal

`vspanset2ispanset()` [orglinks.c:397–402] is a thin wrapper:

```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```

`permute()` [orglinks.c:404–422] iterates the input V-span list and accumulates I-spans:

```c
typespanset *save = targspansetptr;
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                  restrictionindex, targspansetptr, targindex);
}
return (save);
```

`span2spanset()` [orglinks.c:425–454] queries the POOM enfilade and collects contexts:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan,
                                     (typeitemset*)targspansetptr);
}
return (&nextptr->next);  // pointer past last appended item
```

`onitemlist()` [orglinks.c:464–537] appends each found span to the tail of the list — **no merging of adjacent spans**:

```c
for (temp = *itemsetptr; temp && ((typeitemheader*)temp)->next;
     temp = ((typeitem*)((typeitemheader*)temp)->next))
    ;
((typeitemheader*)temp)->next = (typeitemheader*)newitem;
```

---

#### 4. `retrie.c:56–268` — POOM enfilade traversal

`retrieverestricted()` [retrie.c:56–85] → `retrieveinarea()` → `findcbcinarea2d()` [retrie.c:229–268]:

```c
// retrie.c:252-265
for (; crumptr; crumptr = getrightbro(crumptr)) {
    if (!crumqualifies2d(crumptr, offsetptr, span1start, span1end, index1,
                          span2start, span2end, index2, infoptr))
        continue;
    if (crumptr->height != 0) {
        dspadd(offsetptr, &crumptr->cdsp, &localoffset, crumptr->cenftype);
        findcbcinarea2d(findleftson(crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd(headptr, context, index1);  // <-- sorted insertion
    }
}
```

**Critical detail:** `incontextlistnd()` [context.c:75–111] inserts each bottom crum into the context list in **sorted I-address order**:

```c
// context.c:75 — "put c on clist in index order"
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index) {
    prologuecontextnd(c, &grasp, NULL);
    // ... sorted insertion by grasp.dsas[index] ...
    if (whereoncontext(clist, &grasp.dsas[index], index) < THRUME) {
        c->nextcontext = clist; *clistptr = c;  // insert at front
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {
            if (whereoncontext(clist, ...) > ONMYLEFTBORDER
            &&  whereoncontext(nextc, ...) < ONMYLEFTBORDER) {
                c->nextcontext = nextc; clist->nextcontext = c;  // insert in middle
            }
        }
        clist->nextcontext = c;  // append at end
    }
}
```

---

### Why the Decomposition Is NOT Canonical

#### Reason 1: No consolidation of adjacent I-spans

The commented-out `cleanupvspanlist()` [orglinks.c:297–313] inside `#ifdef UnDEFined` [orglinks.c:263] would have merged adjacent spans. It is **dead code**:

```c
#ifdef UnDEFined
// ...
int cleanupvspanlist(typetask *taskptr, typevspanset *vspansetptr)
{
    for (; ptr && ptr->next; ptr = ptr->next) {
        tumbleradd(&ptr->stream, &ptr->width, &spanend);
        if (tumblereq(&spanend, &ptr->next->stream)) {
            tumbleradd(&ptr->width, &ptr->next->width, &ptr->width);  // merge!
```

Because `UnDEFined` is not defined, `cleanupvspanlist()` is never called. The active code path (`permute` → `span2spanset` → `onitemlist`) never merges adjacent I-spans.

#### Reason 2: Output granularity is determined by POOM crum boundaries

`findcbcinarea2d()` descends to bottom crums (height == 0) and emits **one context per bottom crum**. A single V-span that maps to N crums produces N separate ispans and thus N separate sporgl items.

The number of crums covering a logical I-range depends on the order and manner of original insertions (via `insertnd` in `orglinks.c:130` / `insertpm`). After different insertion histories, the same logical content may reside in different crum configurations, yielding different sporgl fragmentation for identical V-span input.

#### Reason 3: V-span boundary × crum boundary interaction

Consider two different vspanset inputs that resolve to the same I-address range [IA, IA+10], where the POOM has a crum boundary at IA+4:

- **Input A**: one vspan [VA, VA+10]  
  → `findcbcinarea2d` returns 2 contexts: [IA, IA+4), [IA+4, IA+10]  
  → 2 sporgl items

- **Input B**: two vspans [VA, VA+4] and [VA+4, VA+6]  
  → first vspan: 1 context [IA, IA+4) → 1 sporgl  
  → second vspan: 1 context [IA+4, IA+10] → 1 sporgl  
  → 2 sporgl items with the same boundaries as A

- **Input C**: two vspans [VA, VA+2] and [VA+2, VA+8] (split at a non-crum-boundary V-position)  
  → first vspan: 1 context [IA, IA+2) → 1 sporgl  
  → second vspan: 2 contexts [IA+2, IA+4), [IA+4, IA+10] → 2 sporgls  
  → **3 sporgl items** for the same logical content as A and B

The V-span split at VA+2 (which maps to IA+2, a mid-crum position) does NOT create a crum boundary; but because `permute()` treats each V-span independently and emits a distinct context per crum intersection, the resulting sporgl fragments differ.

#### Reason 4: Order follows V-input order, not I-order globally

`permute()` [orglinks.c:414–416] processes V-spans in linked-list order:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(...);
}
```

Within each V-span, `incontextlistnd` guarantees ascending I-order (context.c:75). But **across** V-spans, the sporgl list reflects V-input order. If the V→I mapping is non-monotone (e.g., after `rearrange()`), the sporgl list is in non-monotone I-order. No post-sort step exists.

---

### Summary Table

| Property | Verdict | Evidence |
|---|---|---|
| Deterministic given same input + same enfilade | **Yes** | `findcbcinarea2d` is a pure tree traversal; `incontextlistnd` sorts deterministically |
| Canonical (maximal contiguous I-runs) | **No** | No consolidation path in active code; `cleanupvspanlist` is `#ifdef UnDEFined` [orglinks.c:263] |
| Output count depends on crum boundaries | **Yes** | `findcbcinarea2d` emits one context per bottom crum [retrie.c:261–264] |
| Same I-set, different V-spans → different sporgl | **Yes** | V-span split at non-crum boundary produces extra fragments |
| Within one V-span: I-order preserved | **Yes** | `incontextlistnd` does sorted insertion by I-index [context.c:75] |
| Across V-spans: I-order preserved globally | **No** | `permute()` appends in V-input order without cross-span sort |

The bottom line: CREATELINK stores endsets via sporgl decompositions that faithfully reflect the caller's V-span granularity multiplied by the enfilade's crum boundaries. There is no canonical normalization pass. The same logical set of I-addresses can be stored as a different number of sporgl fragments, with different boundaries, depending entirely on how the input vspanset was structured and on the crum layout of the document's POOM enfilade at insertion time.
