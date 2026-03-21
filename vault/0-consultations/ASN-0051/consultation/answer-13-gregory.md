## Question 13 [gregory]

> After REARRANGE with a 3-cut pivot splits a contiguous endset span across two non-adjacent V-regions in the same document, does `RETRIEVEENDSETS` followed by I-to-V conversion via `span2spanset` return a two-VSpec specset reflecting both V-positions, or does the conversion lose one of the fragments?

## KB Synthesis

## Answer: Both V-positions Are Returned — With Possible Duplication

After a pivot, the I-to-V conversion returns a multi-VSpec specset covering both V-regions. The conversion does **not** lose fragments.

### Mechanism

**Step 1 — Pivot preserves I-addresses, changes V-mapping** [INV-REARRANGE-IDENTITY]: A pivot displaces V-positions but leaves I-addresses unchanged. If the endset originally covered a contiguous I-address range α..β at V-region R₁, after the pivot those I-addresses now map to two disjoint V-regions (e.g., part at R₁, part at R₂).

**Step 2 — POOM is a multimap** [SS-POOM-MULTIMAP]: The POOM accumulates every matching leaf via `findcbcinarea2d()`, which traverses all siblings and descends into all qualifying subtrees. `incontextlistnd()` inserts each found context into a V-sorted linked list, never replacing. This means `ispan2vspanset(poom, α..β)` returns **all** V-positions that contain I-addresses in that range — both R₁ and R₂.

**Step 3 — RETRIEVEENDSETS conversion path** [SS-RETRIEVE-ENDSETS]: The call chain is `linksporglset2specset()` → `sporglset2vspanset()` → `span2spanset()` → `retrieverestricted()`. The result is sorted by V-position [INV-RETRIEVAL-V-SORTED]. Unreferenced I-addresses are silently dropped, but both V-regions are active in the POOM after the pivot, so nothing is filtered.

**Step 4 — Result** [INV-RETRIEVAL-TREE-INDEPENDENCE]: The conversion returns a specset with (at least) two VSpecs: one for each V-region containing the endset's I-addresses. The V-ordering invariant guarantees they appear in ascending V-address order.

### The Duplication Caveat

[EC-PIVOT-LINK-FRAGMENTATION] reports that after a pivot swapping "BC" and "DE" within a document containing a link on "CD", the endsets report **four spans** (`1.2 width 0.1` twice, `1.5 width 0.1` twice), and `find_links` returns the same link **twice**. The duplication arises because the spanfilade stores multiple sporgls for the link endset (one per contiguous I-span, per [SS-SPORGL] and [ST-LINK-CREATE]), and each sporgl independently resolves to its V-address — the same V-position can be discovered via multiple sporgl entries in the index.

### Summary

| Question | Answer |
|---|---|
| Does `span2spanset` return both V-positions? | **Yes** — POOM multimap semantics accumulate all matches [SS-POOM-MULTIMAP] |
| Can conversion lose a fragment? | **No** — `findcbcinarea2d` traverses all qualifying subtrees [SS-POOM-MULTIMAP] |
| Are results V-sorted? | **Yes** — `incontextlistnd` maintains sorted order [INV-RETRIEVAL-V-SORTED] |
| Any anomaly? | **Duplication** — same V-position may appear multiple times [EC-PIVOT-LINK-FRAGMENTATION] |

---

## Code Exploration

Now I have enough to trace the full execution path. Let me compile the complete analysis.

---

## Full Answer

### 1. What REARRANGE Does to the POOM

`dorearrange` [do1.c] → `rearrangepm` [orglinks.c:137–142] → `rearrangend` [edit.c:78–160].

For a 3-cut pivot (`nblades == 3`), `makeoffsetsfor3or4cuts` [edit.c:177–181] computes:

```c
diff[1] = blades[2] - blades[1];      // forward shift for section 1
diff[2] = -(blades[1] - blades[0]);   // backward shift for section 2 (negate)
diff[3] = 0;                           // (unused for 3 cuts)
```

`makecutsnd` splits POOM crums at the knife positions. Then [edit.c:113–135]:

```c
for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
    i = rearrangecutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
      case 1: case 2: case 3:
        tumbleradd(&ptr->cdsp.dsas[V], &diff[i], &ptr->cdsp.dsas[V]);
        ivemodified(ptr);
        break;
    }
}
```

The POOM crum's V-displacement (`cdsp.dsas[V]`) is updated in place. After a 3-cut pivot, a contiguous I-span that previously mapped to one contiguous V-region now maps to **two non-adjacent V-regions**. The spanfilade is **not touched** by any of this.

---

### 2. The Spanfilade Stores I-Spans — Immutable Under REARRANGE

When a link is created, `insertspanf` [spanf1.c:15–54] inserts POOM crums into the spanfilade indexed by:
- `SPANRANGE` = I-space content address
- `ORGLRANGE` = link's orgl address with `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN` prefix

REARRANGE calls `rearrangend` only on the document orgl (POOM), not the spanfilade. The I-span stored in the spanfilade remains exactly as inserted at `CREATELINK` time.

---

### 3. RETRIEVEENDSETS Execution Path

`retrieveendsets` [fns.c:350–362] →
`doretrieveendsets` [do1.c:369–374] →
`retrieveendsetsfromspanf` [spanf1.c:190–235]:

```c
specset2sporglset(taskptr, specset, &sporglset, NOBERTREQUIRED)
&& retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset)
&& linksporglset2specset(taskptr, &docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
```

**Step A: `specset2sporglset`** [sporgl.c:14–33]  
Converts the input specset (identifying the link, typically a VSPECID) to a sporglset in I-space via `vspanset2sporglset` → `vspanset2ispanset` → `permute` → `span2spanset`. This produces the link's I-span identity.

**Step B: `retrievesporglsetinrange`** [spanf1.c:237–267]  
Queries the spanfilade:

```c
context = retrieverestricted((typecuc*)spanf, sporgl_as_ispan, SPANRANGE,
                              whichspace, ORGLRANGE, NULL);
for (c = context; c; ...) {
    contextintosporgl((type2dcontext*)c, NULL, sporglset, SPANRANGE);
    // extracts: sporglorigin = totaloffset.dsas[SPANRANGE] (I-span start)
    //            sporglwidth = contextwid.dsas[SPANRANGE]  (I-span width)
    //            sporgladdress = context2dinfo.homedoc
```

The spanfilade is unchanged by REARRANGE, so this finds the original single I-span entry for the endpoint. `fromsporglset` gets one sporgl whose `sporglorigin`/`sporglwidth` is the original (pre-REARRANGE) I-span.

---

### 4. I-to-V Conversion: `linksporglset2specset` → `ispan2vspanset` → `span2spanset`

`linksporglset2specset` [sporgl.c:97–123] →
`linksporglset2vspec` [sporgl.c:127–137] →
`sporglset2vspanset` [sporgl.c:141–176]:

```c
ispan.stream = sporglptr->sporglorigin;
ispan.width  = sporglptr->sporglwidth;
vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);
```

`ispan2vspanset` [orglinks.c:389–394]:

```c
return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
```

`permute` [orglinks.c:404–422] calls `span2spanset` once per input span.

`span2spanset` [orglinks.c:425–454]:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, I,
                              NULL, V, NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, I, &foundspan, V);
    nextptr = onitemlist(taskptr, &foundspan, targspansetptr);
}
```

`retrieverestricted` [retrie.c:56–85] → `retrieveinarea` [retrie.c:87–110] → `findcbcinarea2d` [retrie.c:229–268]:

```c
for (; crumptr; crumptr = getrightbro(crumptr)) {
    if (!crumqualifies2d(..., span1start, span1end, I, span2start, span2end, V, ...))
        continue;
    if (crumptr->height != 0) {
        dspadd(offsetptr, &crumptr->cdsp, &localoffset, crumptr->cenftype);
        findcbcinarea2d(findleftson(crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc((typecbc*)crumptr, offsetptr);
        incontextlistnd(headptr, context, I);  // inserts sorted by I-address
    }
}
```

This recursively walks the **rearranged POOM**. After the 3-cut REARRANGE, there are (at minimum) two groups of leaf crums covering the original I-span `[I₁, I₁+N)`:
- Group A: crums with `cdsp.dsas[I]` ∈ `[I₁, I₁+M)`, V-displacement → region A
- Group B: crums with `cdsp.dsas[I]` ∈ `[I₁+M, I₁+N)`, V-displacement → region B

`crumqualifies2d` [retrie.c:270–305] returns `TRUE` for crums in **both groups** because the I-span restriction covers `[I₁, I₁+N)`. Both groups produce context records. `incontextlistnd` [context.c:75–111] inserts them in I-sorted order.

Back in `span2spanset`, `context2span` [context.c:176–212] is called for each context:

```c
// clips the crum's I-range to the query restriction
// then maps the clipped I-range to V via totaloffset.dsas[V] / contextwid.dsas[V]
movetumbler(&grasp.dsas[V], &foundspanptr->stream);
tumblersub(&reach.dsas[V], &grasp.dsas[V], &foundspanptr->width);
```

Group A contexts map to VSpan for V-region A. Group B contexts map to VSpan for V-region B.

`onitemlist` [orglinks.c:464–537] → `putvspaninlist` [orglinks.c:329–387] accumulates both VSpans. Since V-region A and V-region B are non-adjacent, the adjacency-merge check (`spancmp == 0`) never fires [orglinks.c:346–348], and they remain as **two separate entries** in the vspanset.

---

### 5. Shape of the Returned Specset

The result is **one VSPEC** (not two), with a **two-entry `vspanset`** — one VSpan per V-region. `linksporglset2vspec` [sporgl.c:127–137] wraps the entire multi-fragment vspanset into a single VSPECID item:

```c
specptr->itemid = VSPECID;
specptr->vspanset = NULL;
sporglset2vspanset(taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
```

The client receives (for the `fromset`): one VSPECID node whose `vspanset` field is a linked list of two VSpans.

---

### 6. Verdict

**The conversion does NOT lose either fragment.** `span2spanset` operates by querying the post-REARRANGE POOM with the original I-span. The rearranged POOM has been split (by `makecutsnd` during REARRANGE) at the knife positions, so `findcbcinarea2d` locates leaf crums in both V-regions. Each leaf crum produces a context; each context maps through `context2span` to a VSpan; `putvspaninlist` preserves both non-adjacent VSpans as distinct entries.

The returned specset for each endset (from/to/three) is a single VSPECID containing a two-fragment vspanset — one VSpan per non-adjacent V-region. Both V-positions are faithfully reflected in the output.

**One structural caveat**: the system returns one VSPEC with two VSpans in its `vspanset`, not two separate VSPEC items. If the caller assumes a single-VSpan vspanset and only reads `vspanset->stream`/`vspanset->width` without following `vspanset->next`, it will see only one of the two V-regions. The data is complete in the response; whether the client faithfully iterates the vspanset is a client-side concern.
