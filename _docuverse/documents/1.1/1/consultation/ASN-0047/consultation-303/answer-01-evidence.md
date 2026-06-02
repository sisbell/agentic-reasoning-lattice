## Question 1 [evidence]

> Does `docreatenewversion` (via `doretrievedocvspanfoo`/`retrievedocumentpartofvspanpm`) reproduce the source's content-subspace POOM with V-positions in the same order and with duplicate I-addresses retained at distinct positions, or can it collapse or reorder entries?

## KB Synthesis

## `docreatenewversion` POOM Reproduction: Synthesis

### Scope of the Copy

Only the **text subspace** (V 1.x) is reproduced. `retrievedocumentpartofvspanpm` extracts `cdsp.dsas[V]` and `cwid.dsas[V]` from the source root, which points to position `1` (text start). The link subspace (V 2.x) is structurally outside this vspan and is **not copied**. [ST-VERSION-CREATE, Findings 0043, 0046]

### V-Position Order: Preserved

`docopyinternal` → `specset2ispanset` → `permute` walks the source POOM, and contexts are accumulated via `incontextlistnd()`, which performs explicit insertion-sort by V-address as leaf nodes are discovered. The I-spans fed to `insertpm` for the new version arrive in **ascending V-order regardless of tree sibling structure**. [INV-RETRIEVAL-V-SORTED, Finding 0078]

### Duplicate I-Addresses at Distinct V-Positions: Retained

When the source document contains internal transclusion — the same I-address range appearing at multiple V-positions (e.g., V 1.10→I.5..9 and V 1.20→I.5..9) — both crums are retrieved by `findcbcinarea2d()`, which accumulates **all** matching leaf nodes via `incontextlistnd`. [SS-POOM-MULTIMAP, Finding 0039]

When inserting into the version's POOM, `isanextensionnd()` merges only if `new_I_origin == existing_crum.I_reach` **and** homedoc matches. For the second occurrence of the same I-span (I-origin = I.5 again, not I.9+1), the extension check fails — a **separate crum is created**. The multimap structure is faithfully reproduced. [ST-VCOPY, Finding 0046]

### Natural Adjacency Collapsing: Semantically Neutral

Source crums that are simultaneously V-adjacent and I-adjacent **may** be merged by `isanextensionnd` during insertion. This does not lose information — it reflects the same logical content in fewer crums. The observable V→I mapping is identical before and after such merging.

### What Cannot Happen

- **Reordering**: Impossible — V-sorted retrieval guarantees insertion order. [INV-RETRIEVAL-V-SORTED]
- **Loss of distinct I-address occurrences**: Impossible — non-contiguous I-origins always create new crums. [SS-POOM-MULTIMAP]
- **Cross-subspace copying**: Impossible — `retrievedocumentpartofvspanpm` scope excludes V 2.x. [FC-SUBSPACE, ST-VERSION-CREATE Finding 0043]

### Summary

The version POOM faithfully reproduces the source text-subspace mapping: same V-position order, same duplicate I-address occurrences at distinct V-positions, no collapsing of structurally distinct entries. Only naturally contiguous (V-adjacent, I-adjacent, same-homedoc) segments may be merged — which is a representation detail with no semantic consequence. [ST-VERSION, Finding 0077; PRE-COPY; INV-IADDR-PROVENANCE]

---

## Code Exploration

I now have all the source needed. Let me trace the full execution path and write the answer.

---

## Answer

### The execution chain

`docreatenewversion` [do1.c:260–299] reproduces the source document's content-subspace POOM through a five-stage pipeline. Here is the precise trace.

---

### Stage 1 — What V-span does `doretrievedocvspanfoo` / `retrievedocumentpartofvspanpm` actually return?

`doretrievedocvspanfoo` [do1.c:301–309] is a thin wrapper:

```c
return (
   findorgl(taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)
&& retrievedocumentpartofvspanpm(taskptr, docorgl, vspanptr));
```

`retrievedocumentpartofvspanpm` [orglinks.c:155–162] (self-described as "a kluge") reads exactly two fields from the **root CUC** of the source POOM:

```c
movetumbler(&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
movetumbler(&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
```

The root CUC's `cdsp.dsas[V]` is the minimum absolute V-address and `cwid.dsas[V]` is the total V-extent of the tree. Crucially, **this returns a single contiguous bounding-box interval** — it does not enumerate the individual leaf crums. For a document whose text starts at V = 1.0.1, this returns `{stream: 1.0.1, width: total_text_width}`. Gaps, permutations, and multi-segment structure inside the POOM are invisible to this call; you get one span covering the outermost V-range.

---

### Stage 2 — How `docreatenewversion` builds the specset

[do1.c:285–293]:

```c
vspec.next = NULL;
vspec.itemid = VSPECID;
movetumbler(isaptr, &vspec.docisa);   // source document ISA
vspec.vspanset = &vspan;              // the single bounding-box V-span
...
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

The `vspec` says: "content of source document `isaptr` at V-positions `[vspan.stream, vspan.stream + vspan.width]`." The VSA passed to the new document is `vspan.stream` (the source's V-start).

---

### Stage 3 — V→I translation via `specset2ispanset` / `vspanset2ispanset`

`specset2ispanset` [do2.c:14–46] handles the `VSPECID` case by calling:

```c
findorgl(taskptr, granf, &((typevspec*)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset(taskptr, docorgl, ((typevspec*)specset)->vspanset, ispansetptr))
```

`vspanset2ispanset` [orglinks.c:397–402]:

```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```

`permute` [orglinks.c:404–422] iterates over each V-span and calls `span2spanset`, which calls:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, V, (typespan*)NULL, I, (typeisa*)NULL);
```

`retrieverestricted` [retrie.c:56–85] → `retrieveinarea` [retrie.c:87–110] → `findcbcinarea2d` [retrie.c:229–268].

`findcbcinarea2d` does a recursive left-to-right DFS over the POOM tree. At each leaf crum that qualifies, it calls:

```c
context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr);
incontextlistnd(headptr, context, index1);   // index1 = V
```

---

### Stage 4 — `incontextlistnd` imposes V-sorted order on the context list

[context.c:74–111], beginning with the comment **"put c on clist in index order"**:

```c
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
  typecontext *clist, *nextc;
  typedsp grasp;

    prologuecontextnd(c, &grasp, (typedsp*)NULL);
    c->nextcontext = NULL;
    clist = *clistptr;
    if (!clist) { *clistptr = c; return(0); }        // first insertion
    if (whereoncontext(clist, &grasp.dsas[index], index) < THRUME) {
        c->nextcontext = clist; *clistptr = c; return(0); // prepend
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {
            if ((whereoncontext(clist, ...) > ONMYLEFTBORDER)
             && (whereoncontext(nextc, ...) < ONMYLEFTBORDER)) {
                c->nextcontext = nextc; clist->nextcontext = c; return(0); // insert middle
            }
        }
    }
    clist->nextcontext = c;  // append end
}
```

This is an **insertion sort keyed on `index = V`**. Every leaf crum found by `findcbcinarea2d` is placed in the context list at the position corresponding to its absolute V-address. The resulting context list is in strictly ascending V-order.

Two distinct crums that map the **same I-address range** to **different V-addresses** (i.e., transcluded content, the same permascroll content appearing at two V-positions) produce two separate contexts. `incontextlistnd` inserts both, sorted by their respective V-starts. There is no deduplication on I-address.

---

### Stage 5 — `span2spanset` converts contexts to I-spans without collapsing

Back in `span2spanset` [orglinks.c:425–454]:

```c
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, V, &foundspan, I);
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`context2span` [context.c:176–212] clips the leaf crum's I-range to the restriction span and emits an `ISPANID` span. `onitemlist` [orglinks.c:464–537] is a **plain append** — it walks the list to the end and links the new item:

```c
for (temp = *itemsetptr; temp && ((typeitemheader*)temp)->next; temp = ...)
    ;
((typeitemheader*)temp)->next = (typeitemheader*)newitem;
```

No sort, no merge, no deduplication on I-address. Two I-spans with the same stream value (same permascroll origin) are appended as two distinct list entries. The list order mirrors the V-order imposed by `incontextlistnd`.

---

### Stage 6 — `insertpm` assigns fresh, sequential V-positions

[orglinks.c:75–134]:

```c
for (; sporglset; sporglset = (typesporglset)sporglset->xxxxsporgl.next) {
    unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
    movetumbler(&lstream, &crumorigin.dsas[I]);
    movetumbler(&lwidth,  &crumwidth.dsas[I]);
    movetumbler(vsaptr,   &crumorigin.dsas[V]);
    shift = tumblerlength(vsaptr) - 1;
    inc   = tumblerintdiff(&lwidth, &zero);          // character count
    tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);
    insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);  // advance VSA
}
```

`vsaptr` starts at `vspan.stream` (= source root's `cdsp.dsas[V]`). After each crum is inserted, `vsaptr` is advanced by the crum's V-width. V-widths are computed from I-widths (character counts) at the same tumbler level as `vsaptr`, **not** copied from the source's actual V-widths.

For the extension/merge check inside `insertcbcnd` [insertnd.c:242–275], `isanextensionnd` [insertnd.c:301–309] tests:

```c
return (lockeq(reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
```

This compares `reach` (both I and V) to `origin` across all dimensions. For two crums with the **same I-stream** (duplicate I-address): the first crum's I-reach is `I_stream + I_width`, while the second crum's I-origin is `I_stream`. Since `I_width > 0`, `I_stream + I_width ≠ I_stream`. `lockeq` returns FALSE; the crums are **not merged**.

---

### Conclusions

**V-position order is preserved — strictly.**  
`incontextlistnd` [context.c:75] sorts contexts by V-index before they reach `insertpm`. `insertpm` assigns new V-addresses in iteration order, which is V-ascending order from the source. The relative V-ordering of the new POOM exactly mirrors the source's V-ordering.

**Duplicate I-addresses are retained at distinct V-positions — they are not collapsed.**  
`onitemlist` [orglinks.c:464] is a plain append with no deduplication. `isanextensionnd` [insertnd.c:301] requires coincidence in *both* I and V dimensions to merge — two crums with the same I-start address cannot be I-adjacent (since `I_stream + I_width ≠ I_stream` when width > 0), so they survive as separate POOM entries at distinct sequential V-positions.

**However, V-address values are freshly reassigned — not copied verbatim.**  
`retrievedocumentpartofvspanpm` [orglinks.c:155] reads only the root's bounding box, discarding the internal V-structure. `insertpm` recomputes V-widths from I-widths and packs them contiguously from `vspan.stream`. Any gaps that existed in the source's V-space are eliminated in the copy. The *order* is faithfully reproduced; the *numeric V-values* are re-derived.
