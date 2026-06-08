## Question 18 [evidence]

> For a sporgl built from multiple non-contiguous source spans, does each contiguous I-span produce its own DOCISPAN entry, making destination storage O(span count) rather than O(byte count)?

## KB Synthesis

Yes, confirmed. Each contiguous I-span produces exactly one DOCISPAN entry, making destination storage O(span count).

The mechanism chain:

1. **V-spans → I-spans** (`vspanset2ispanset` / `permute`): A V-span covering non-contiguous I-address regions is decomposed into one `typeispan` per contiguous region [SS-SPORGL]. This is the same splitting that happens during link creation [ST-LINK-CREATE], Finding 0037.

2. **I-spans → DOCISPAN**: `insertspanf` loops over the `ispanset` linked list and calls `insertnd` once per `typeispan` [SS-DOCISPAN], Finding 0047:
   > "each `typeispan` represents a contiguous range of I-addresses, so inserting 10 contiguous bytes creates 1 DOCISPAN entry, not 10"

3. **COPY with fragmented source**: Explicitly confirmed in [ST-COPY], Finding 0047:
   > "COPY of fragmented source content (e.g., 3 non-contiguous regions) creates 3 DOCISPAN entries"

The system invariant is [INV-SPANF-GROWTH]: `|DOCISPAN| ≤ Σ_{all INSERT/COPY ops} |ispanset(op)|` — storage tracks editorial operations, not byte volume.

**Concrete consequence**: If you vcopy 5 non-contiguous V-spans each mapping to distinct I-address regions, `docopy` receives an ispanset of 5 entries and `insertspanf` makes 5 `insertnd` calls → 5 DOCISPAN entries at the destination, regardless of how many bytes those spans contain.

---

## Code Exploration

I now have enough from the source to give a complete, verified answer.

---

## Answer: Yes — DOCISPAN Storage Is O(Span Count), Not O(Byte Count)

Each contiguous I-span in a sporgl produces exactly one DOCISPAN entry in the spanfilade. The evidence is a direct chain through the source.

---

### The Copy Path

`docopy` at `do1.c:45–65` is the entry point for all copy operations:

```c
/* do1.c:53-64 */
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa (vsaptr, docorgl)
&& asserttreeisok(docorgl)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)   // ← line 62
&& asserttreeisok(docorgl)
```

The call chain for spanfilade storage is:
```
docopy → specset2ispanset → vspanset2ispanset → permute → span2spanset
                                                                 ↓
                               insertspanf ← (ispanset: one node per I-span)
```

---

### V→I Conversion: One Node Per Contiguous I-Span

`specset2ispanset` at `do2.c:14–46` iterates over each vspec, calling `vspanset2ispanset`, which is a thin wrapper `orglinks.c:397–402`:

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl,
    typevspanset vspanptr, typeispanset *ispansetptr)
{
    typespanset *permute();
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` at `orglinks.c:404–422` loops over the V-span restriction set and calls `span2spanset` once per V-span. `span2spanset` at `orglinks.c:425–449` queries `retrieverestricted` against the POOM and emits one output span per context entry (each context entry = one contiguous I-region). For **non-contiguous** source content, the POOM returns multiple context entries — one per disjoint I-segment — yielding multiple I-spans in the output list.

---

### Spanfilade Insertion: One `insertnd` Call Per I-Span

`insertspanf` at `spanf1.c:15–54` contains a single loop over the input list, calling `insertnd` once per iteration:

```c
/* spanf1.c:25–52 */
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    if (((typeitemheader *)sporglset)->itemid == ISPANID) {
        movetumbler (&((typeispan *)sporglset)->stream, &lstream);   // line 27
        movetumbler (&((typeispan *)sporglset)->width,  &lwidth);    // line 28
        movetumbler (isaptr, &linfo.homedoc);
    }
    // ... SPORGLID and TEXTID cases ...
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);   // line 49
    movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);    // line 50
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);  // line 51
}
```

There is no merging, coalescing, or batching inside `insertspanf`. One I-span in → one `insertnd` call → one spanfilade node.

---

### DOCISPAN Definition

`xanadu.h:39`:

```c
#define DOCISPAN  4
```

DOCISPAN is the span-type constant passed to `insertspanf`. Every `insertnd` call from within `insertspanf` during a copy operation stamps its node with this type.

The only two call sites for `insertspanf(..., DOCISPAN)` are:
- `do1.c:62` — `docopy`
- `do1.c:79` — `docopyinternal` (same logic, used by `docreatenewversion`)

---

### Storage Complexity

For a copy from N non-contiguous source V-spans that map to M total contiguous I-span segments (M ≥ N because each V-span may straddle multiple I-segments if the source was itself assembled from fragments):

- `permute` produces M I-span list nodes
- `insertspanf` calls `insertnd` exactly M times
- M DOCISPAN nodes are written to the spanfilade

**Storage is O(M) = O(span count).** It is entirely independent of the byte volume of content in any span. A single 10 MB clip from one source produces one DOCISPAN entry. Ten 1-byte clips from ten sources produce ten entries.

---

### Implication

This is the correct and intended design: the enfilade represents content as a set of address intervals, not as copied bytes. The cost of building a sporgl from N source fragments is exactly N spanfilade nodes. Byte count is irrelevant to storage overhead at the meta-level — only fragmentation matters.
