## Question 13 [gregory]

> When `vspanset2sporglset` walks the POOM to convert a V-span to I-spans, and the V-span crosses a boundary between two POOM entries with non-contiguous I-addresses, does it always produce exactly one sporgl per contiguous I-run — never merging across I-gaps or splitting within a contiguous I-run?

## KB Synthesis

## `vspanset2sporglset`: One Sporgl Per Contiguous I-Run

### The confirmed behavior

Yes — `vspanset2sporglset` produces exactly one sporgl per contiguous I-address run, neither merging across gaps nor splitting within a run. Here is what the KB supports for each half of that claim.

---

### Never merges across I-gaps

[ST-LINK-CREATE] (Finding 0037) provides the definitive confirmation via a concrete example:

> Document C contains "AABB" where "AA" came from document A and "BB" from document B — non-contiguous I-address regions.
>
> `create_link(source = V-span 1.1 width 0.4 in doc C)`
>
> Input: 1 V-span covering all of "AABB"  
> Output: **2 sporgls** — one for "AA"'s I-range, one for "BB"'s I-range

The conversion chain is:

```
V-span → vspanset2ispanset → permute → span2spanset
       → retrieverestricted → separate I-span per contiguous I-region
       → separate sporgl per I-span
```

The inner loop at `sporgl.c:49-58` creates one sporgl per I-span returned by `vspanset2ispanset` — it has no merging logic. Two non-contiguous I-regions in the POOM produce two I-spans, which produce two sporgls. The I-gap between "AA"'s permascroll addresses and "BB"'s permascroll addresses is preserved.

---

### Never splits within a contiguous I-run

This half is not explicitly confirmed in the KB but is well-supported by structural evidence:

1. **[INV-VSPAN-CONSOLIDATION]** (Finding 0028): "The enfilade consolidates logically contiguous V-space regions into a single span regardless of insertion history." Sequential inserts that receive contiguous I-addresses are stored compactly in the POOM — the enfilade is designed to avoid fragmentation.

2. **[SS-POOM-MULTIMAP]** (Finding 0039): The accumulation function `incontextlistnd()` collects POOM contexts sorted by V-address. For a query by V-span (V→I direction, via `permute`), each POOM crum that overlaps the V-span contributes one I-span. If two adjacent crums cover contiguous I-addresses, the resulting I-spans are contiguous — the KB identifies no merging step, but the phrase from [ST-LINK-CREATE] "separate I-span per **contiguous** I-address region" treats a contiguous region as a unit.

3. **[SS-VSPAN-TO-SPORGL]** (Finding 0013): "converts V-addresses to I-addresses via the document's enfilade (`vspanset2ispanset`)" — there is no documented consolidation step after the conversion, which means the POOM structure itself determines the I-span boundaries. Since [INV-VSPAN-CONSOLIDATION] confirms the POOM stores contiguous content compactly, a contiguous I-run maps to a compact POOM representation, producing a single I-span in output.

**Caveat**: The KB does not explicitly describe what happens when tree rebalancing or splitting (documented in [SS-ENFILADE-TREE] / Findings 0058, 0060) places adjacent POOM crums with contiguous I-addresses. Whether those produce one merged I-span or two adjacent I-spans from the `retrieverestricted` call chain is not confirmed. The KB cannot definitively rule out this edge case.

---

### Summary

| Case | KB support |
|------|-----------|
| Non-contiguous I-regions → separate sporgls | **Directly confirmed** by [ST-LINK-CREATE] (Finding 0037) |
| Contiguous I-region → single sporgl | **Inferred** from [INV-VSPAN-CONSOLIDATION] + [SS-VSPAN-TO-SPORGL]; not explicitly confirmed for tree-split crums |
| Merging across I-gaps | **Never** — no merging logic documented; inner loop is one-sporgl-per-I-span |

The KB is answerable on the non-contiguous case and directionally supported on the contiguous case, but the splitting-within-a-contiguous-run question for tree-internal crum boundaries is not explicitly addressed.

---

## Code Exploration

I now have everything needed for a complete answer. Here it is.

---

## Answer

**Yes — with a precise qualification.** `vspanset2sporglset` always produces exactly one sporgl per POOM leaf-crum contribution. It never merges across I-gaps, and it never splits within a single crum's contiguous I-range. However, it also never merges *across* adjacent crums that happen to be I-contiguous — so the guarantee is per-crum, not per maximal-contiguous-I-run across crum boundaries.

Here is the complete call chain traced from source.

---

### 1. The outer loop: one sporgl per I-span

`vspanset2sporglset` [sporgl.c:35–65]:

```c
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
        sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
        sporglset->itemid = SPORGLID;
        sporglset->next = NULL;
        movetumbler (docisa, &sporglset->sporgladdress);
        movetumbler(&ispanset->stream,&sporglset->sporglorigin);
        movetumbler (&ispanset->width, &sporglset->sporglwidth);
        *sporglsetptr = (typesporglset)sporglset;
        sporglsetptr = (typesporglset *)&sporglset->next;
    }
}
```

[sporgl.c:47–58]. The inner loop is a direct 1:1 traversal of `ispanset`: **one `typesporgl` allocated and filled per `ispanset` node, no merging, no skipping.** The question therefore reduces entirely to what `vspanset2ispanset` deposits into `ispanset`.

---

### 2. `vspanset2ispanset` → `permute` → `span2spanset`

[orglinks.c:397–402]:
```c
typeispanset *vspanset2ispanset(...) {
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` [orglinks.c:404–422] iterates over each V-span in the restriction set and calls `span2spanset` once per span, threading the tail pointer through so all results accumulate in one list.

`span2spanset` [orglinks.c:425–454]:
```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

**One context → one I-span via `context2span` → appended via `onitemlist`.**

---

### 3. Context collection: `retrieveinarea` → `findcbcinarea2d`

`retrieverestricted` [retrie.c:56–85] delegates to `retrieveinarea` [retrie.c:87–110], which for POOM calls `findcbcinarea2d` [retrie.c:229–268]:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1,
                          span2start, span2end, index2, infoptr))
        continue;
    if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);
    }
}
```

[retrie.c:252–264]. This is a recursive descent that visits every POOM leaf crum (`height == 0`) whose V-range overlaps the restriction span. **Each qualifying leaf crum produces exactly one context**, inserted into a sorted list by `incontextlistnd`.

`incontextlistnd` [context.c:75–111] sorts contexts in `index1` (V) order — it does not deduplicate or merge. Each context records the crum's `totaloffset` and `contextwid` in both V and I dimensions, copied verbatim from `makecontextfromcbc` [context.c:151–174]:

```c
context = createcontext(crumptr->cenftype);
movewisp(offsetptr, &context->totaloffset);
movewisp(&crumptr->cwid, &context->contextwid);
...
dspadd(&context->totaloffset, &crumptr->cdsp, &context->totaloffset, (INT)crumptr->cenftype);
```

[context.c:159–167]. The context's I-range is `[totaloffset.dsas[I], totaloffset.dsas[I] + contextwid.dsas[I])` — exactly the leaf crum's I-range.

---

### 4. Clipping within a crum: `context2span`

[context.c:176–212]:
```c
movetumbler (&restrictionspanptr->stream, &lowerbound);
tumbleradd (&lowerbound, &restrictionspanptr->width, &upperbound);
prologuecontextnd (context, &grasp, &reach);

if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {
    tumblerincrement (&grasp.dsas[idx2], 0,
        (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
        &grasp.dsas[idx2]);
}
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER) {
    tumblerincrement (&reach.dsas[idx2], 0,
        - tumblerintdiff (&reach.dsas[idx1], &upperbound),
        &reach.dsas[idx2]);
}
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2],&grasp.dsas[idx2],&foundspanptr->width);
```

[context.c:186–207]. This clips the crum's I-range (`idx2`) proportionally to the portion of the V-span (`idx1`) restriction that overlaps the crum. If the crum's left V-edge extends left of the V-span start, the I-origin is shifted right by the same integer amount. If the crum's right V-edge extends past the V-span end, the I-reach is shifted left. **Both adjustments are integer differences applied isometrically** (via `tumblerintdiff` which returns a scalar delta). The result is one contiguous I-span — a prefix/suffix/interior clip of the crum's I-range. No splitting.

---

### 5. Appending without merging: `onitemlist`

[orglinks.c:464–537]:
```c
((typeitemheader *)newitem)->next = NULL;
if (*itemsetptr == NULL) {
    *itemsetptr = newitem;
} else {
    for (temp = *itemsetptr; temp && ((typeitemheader *)temp)->next;
         temp = (typeitem *)((typeitemheader *)temp)->next) ;
    ((typeitemheader *)temp)->next = (typeitemheader *)newitem;
}
return (newitem);
```

[context.c:517–534]. This walks to the end of the existing list and appends. **There is no contiguity check, no tumbler comparison between the new span and the last span in the list, and no merging.** Two I-spans that happen to be adjacent in I-space produce two separate list nodes.

*(Note: `putvspaninlist` in orglinks.c:329–387 does have merge/sort logic, but that function is used for V-span lists in `walkorglonvpm`, not in this pipeline. `onitemlist` is what `span2spanset` calls.)*

---

### 6. What the scenario produces

When a V-span crosses the boundary between two POOM leaf crums A and B with non-contiguous I-addresses:

| Step | What happens |
|------|-------------|
| `findcbcinarea2d` | Finds both crums A and B (both qualify); creates two contexts, sorted by V via `incontextlistnd` |
| `context2span` (A) | Clips A's I-range to the portion of the V-span overlapping A → one contiguous I-span |
| `onitemlist` (A) | Appends that I-span to `ispanset` |
| `context2span` (B) | Clips B's I-range to the portion of the V-span overlapping B → one contiguous I-span |
| `onitemlist` (B) | Appends that I-span; **no check against A's I-span endpoint** |
| `vspanset2sporglset` | Iterates `ispanset`: allocates sporgl for A's I-span, then sporgl for B's I-span |

**Result: two sporgls, one per POOM crum, one per I-run.** Since the I-addresses are non-contiguous by premise, these are genuinely separate I-runs, and each gets exactly one sporgl. The I-gap between them is neither bridged nor collapsed.

---

### 7. The critical caveat

The guarantee holds exactly at **POOM leaf-crum granularity**:

- **One crum → one sporgl**, always. `context2span` clips proportionally without splitting [context.c:191–207].
- **No merging across crums**, ever. `onitemlist` has no merge logic [orglinks.c:517–534].

This means: if two adjacent POOM crums happen to have *contiguous* I-addresses (their I-ranges abut), the pipeline still produces **two separate sporgls** — a spurious split at the crum boundary in I-space. The function does not detect or collapse adjacent I-spans from different crums.

In the specific scenario the question asks about (two POOM entries with **non-contiguous** I-addresses), this caveat is irrelevant: both sporgls represent genuinely disjoint I-runs, so "one sporgl per contiguous I-run" holds exactly. The code never merges across I-gaps (no such logic exists) and never splits within a single crum's I-contribution (clipping is proportional and linear).
