## Question 12 [evidence]

> If the request specset contains overlapping V-spans, does the combined result return duplicated fragments, or does the system coalesce them into a single covering VSpec?

## KB Synthesis

## Overlapping V-Spans in a SpecSet: Duplication, Not Coalescing

The KB does not contain a direct test scenario for this exact question, but the answer is inferrable from several entries: **the system returns duplicated fragments, not a coalesced result**.

### Why duplication follows from design

**[SS-SPECSET]** establishes that a SpecSet is a `seq<VSpec>` — a sequence, not a set. Order is operationally significant; retrieve concatenates in VSpec order and vcopy places content in VSpec order.

**[INV-SPECSET-ORDER]** confirms this: "Retrieve concatenates content in VSpec order. Vcopy places content in VSpec order. This is consistent across all multi-span operations tested."

The call chain for retrieve is `specset2ispanset` → `ispanset2vstuffset` [PRE-RETRIEVE-CONTENTS, ST-INSERT]. Each VSpec is independently converted to I-spans and looked up in the permascroll. Nothing in the KB describes a deduplication or coalescing step across VSpecs in this pipeline.

### INV-VSPAN-CONSOLIDATION does not apply here

**[INV-VSPAN-CONSOLIDATION]** says the enfilade consolidates contiguous V-space regions into a single span — but this invariant describes the **POOM's internal representation of a document's own content after insertions**, not how an input specset is processed. It is a property of the data structure, not of specset consumers.

### Supporting evidence for duplication

**[EC-MULTISPAN-LINK-DUPLICATION]** (Finding 0019) directly observes that "creating a link with multiple source spans works, but `retrieve_endsets` may return duplicate spans" when a multi-span specset is used. The duplicate arises from the per-VSpec independent processing path.

**[INV-IDENTITY-OVERLAP]** (Finding 0028) shows that when overlapping regions are separately transcluded:

```
vcopy(src, Span(1.1, 0.4), dst, end)  — "ABCD"
vcopy(src, Span(1.3, 0.4), dst, end)  — "CDEF"
Result: "ABCDCDEF" — "CD" appears twice
```

Both appearances of "CD" share I-addresses with the source — the content is identity-duplicated, not coalesced.

### Consequence for vcopy with overlapping specset

If vcopy uses a specset whose VSpecs overlap, **[ST-VCOPY]** places content in VSpec order. The overlapping region is inserted twice into the destination. Each insertion share the same I-addresses per **[INV-IDENTITY-OVERLAP]** — both copies are content-identical in I-space — but both V-positions exist in the destination POOM independently, as the POOM is a multimap **[SS-POOM-MULTIMAP]**.

### Summary

The system produces **duplicated fragments** for each overlapping VSpec, preserving VSpec ordering throughout. No coalescing occurs at the specset processing layer. The consolidation invariant **[INV-VSPAN-CONSOLIDATION]** applies only to the enfilade's internal structure after placement, and only for content that is both contiguous in V-space and shares the same home document — not to input specset semantics.

---

## Code Exploration

Now I have everything needed to give a complete, code-cited answer.

---

## Answer: Overlapping V-Spans in a Request Specset

**The system returns duplicated fragments. No coalescing occurs.**

---

### Execution Path

The retrieve request enters at `retrievev` [`fns.c:175`], which calls `doretrievev` [`do1.c:338`]:

```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr)
{
  typeispanset ispanset;
  return
     specset2ispanset (taskptr, specset, &ispanset, READBERT)
  && ispanset2vstuffset (taskptr, granf, ispanset, vstuffsetptr);
}
```

Two stages: (1) convert the specset's V-spans into I-spans, (2) retrieve content from those I-spans.

---

### Stage 1: V→I Conversion — Where Coalescing Was Designed to Happen (But Doesn't)

**`specset2ispanset`** [`do2.c:14`] iterates over each specset item. For each `VSPECID` item it calls `vspanset2ispanset`, which calls `permute` [`orglinks.c:397–422`]:

```c
typespanset *permute(typetask *taskptr, typeorgl orgl, typespanset restrictionspanset,
                     INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
    /*consolidatespans(restrictionspanset);                     ← COMMENTED OUT
    foospanset("restrictionset after consolidation is ",restrictionspanset); */
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
        targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                      restrictionindex, targspansetptr, targindex);
    }
    return (save);
}
```

**`consolidatespans` is commented out** [`orglinks.c:412–413`]. This was the designed pre-merger that would have collapsed overlapping input V-spans into a single covering span before processing. With it disabled, each V-span in the input is processed independently, even if they overlap.

---

### Stage 1a: Each Span Processed Separately — No I-Span Deduplication

**`span2spanset`** [`orglinks.c:425–453`] is called once per V-span. It calls `retrieverestricted` to find all POOM crums intersecting that V-span, then accumulates results:

```c
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan,
                                     (typeitemset*)targspansetptr);
}
```

**`onitemlist`** [`orglinks.c:464–537`] simply walks to the end of the existing list and appends:

```c
((typeitemheader *)temp)->next = (typeitemheader *)newitem;
```

There is no comparison, no merge, no deduplication. Every I-span fragment found is appended unconditionally.

Consequence: for a pair of overlapping V-spans (e.g., `[1.1, 1.5]` and `[1.3, 1.8]`), the region `[1.3, 1.5]` is traversed during processing of *both* spans. The POOM crums covering that overlap region are found twice and emit two sets of I-span entries for the same underlying content.

---

### Stage 2: Content Retrieval — No Deduplication Either

**`ispanset2vstuffset`** [`granf1.c:58–74`] iterates through the I-span list and chains the results:

```c
*vstuffsetptr = NULL;
for (; ispanset; ispanset = ispanset->next) {
    vstuffsetptr = ispan2vstuffset (taskptr, granfptr, ispanset, vstuffsetptr);
}
```

**`ispan2vstuffset`** [`granf2.c:286–318`] calls `retrieveinspan` for each I-span and appends all matching granfilade crums to the output:

```c
for (temp = context; temp; temp = temp->nextcontext) {
    if (context2vstuff (taskptr, temp, ispanptr, &vstuffset)) {
        *vstuffsetptr = vstuffset;
        vstuffsetptr = (typevstuffset *)&((typeitemheader *)vstuffset)->next;
    }
}
```

No comparison against previously retrieved vstuff items. The overlapping content emits duplicated vstuff entries in the result.

---

### Dead Code: Coalescing Was Intended But Disabled

Three pieces of evidence show the design intended coalescing, but it was deactivated:

**1. `consolidatespans` call, commented out** [`orglinks.c:412–413`] — would have merged overlapping input V-spans before `permute` processed them.

**2. `cleanupvspanlist`** [`orglinks.c:297–312`] — inside `#ifdef UnDEFined` (fully dead), this function merges adjacent V-spans in the result set (where `end == start` of next span via `tumblereq`). It was designed for the `walkorglonvpm` path, also dead.

**3. `consolidatespanset` stub** [`orglinks.c:456–462`] — the comment body of an unimplemented consolidation function, never compiled.

By contrast, **`putvspaninlist`** [`orglinks.c:329–387`] — used only in `retrievevspansetpm` for reporting a document's own V-span extent — *does* have full overlap-handling logic (checking `spancmp`, adjusting starts and widths). But this function is **not in the retrieve pipeline** and is never called during `doretrievev`.

---

### Summary

| Location | Behavior |
|---|---|
| `permute` [`orglinks.c:412`] | `consolidatespans` **commented out** — overlapping input V-spans not pre-merged |
| `span2spanset` → `onitemlist` [`orglinks.c:444, 464`] | Appends I-spans to list with **no coalescing** |
| `ispanset2vstuffset` [`granf1.c:67`] | Chains all I-span results with **no deduplication** |
| `ispan2vstuffset` [`granf2.c:302`] | Appends all content crums with **no deduplication** |
| `putvspaninlist` [`orglinks.c:329`] | Has coalescing logic, but **not in this path** |

**When a request specset contains overlapping V-spans, the system returns duplicated fragments** — the overlapping region is retrieved once per input V-span that covers it. No covering VSpec is constructed. The coalescing machinery was designed (three dead-code sites) but is not active in the shipping code.
