## Question 16 [evidence]

> In what order are the spans returned within the spec-set — sorted by I-address via `incontextlistnd`, or in the stored order the endset was recorded at link creation?

## KB Synthesis

Spans within a returned specset are sorted by **V-address (left boundary), ascending**, via `incontextlistnd()` — not in the stored order from link creation.

Here is the full retrieval pipeline:

**From link orgl → I-addresses**

`link2sporglset()` reads the endset I-spans from the link orgl via `retrieverestricted()` on the GRAN (1D) enfilade. GRAN retrieval uses `oncontextlistseq()`, which appends in tree-traversal order — this corresponds to I-address order, since GRAN tree structure maintains sequential I-order [SS-CONTEXT-LIST].

**From I-addresses → V-addresses**

`linksporglset2specset()` → `sporglset2vspanset()` → `ispan2vspanset()` → `permute()` → `span2spanset()` → `findcbcinarea2d()`. The POOM is a 2D enfilade; its retrieval accumulates results via `incontextlistnd()`, which performs **explicit insertion-sort by V-address left boundary** regardless of the order contexts are discovered in the tree [INV-RETRIEVAL-V-SORTED].

**The postcondition** from [INV-RETRIEVAL-V-SORTED]:
```
forall j, k :: j < k ==> contexts[j].totaloffset.dsas[V] <= contexts[k].totaloffset.dsas[V]
```

This sort is **tree-structure independent** [INV-RETRIEVAL-TREE-INDEPENDENCE] — it overrides insertion order, split/rebalance shape, and diagonal ordering. The I-address order in which endset sporgls were stored at link creation time does not survive into the output.

The same applies to RETRIEVEENDSETS [SS-RETRIEVE-ENDSETS]: the final `linksporglset2specset()` step imposes the same V-sort.

**Summary:** the specset output is sorted by ascending V-address (left boundary), not by link-creation order.

---

## Code Exploration

I now have everything needed to answer definitively. Here is the complete answer with full code citations.

---

## Span Order in the Spec-Set: V-Address Sorted, Not I-Address Sorted

### Short answer

The spans returned in a spec-set after following a link are **sorted by V-address** (the endset's storage position), **not by I-address**. The `incontextlistnd` function is called with `index1 = V`, not `I`. Because V-address is assigned sequentially at link creation (in endset-recording order), the result coincidentally matches the recorded endset order — but the sort key is V, not I.

---

### Full trace

#### Step 1 — Entry point: `link2sporglset` [sporgl.c:83]

```c
if (context = retrieverestricted((typecuc*)orgl, &vspan ,V, (typespan*)NULL, I, (typeisa*)NULL)) {
```

The call signature of `retrieverestricted` is:
```
retrieverestricted(fullcrumptr, span1ptr, index1, span2ptr, index2, docisaptr)
```

So here:
- `span1ptr = &vspan`, `index1 = V` — restrict to this endset's V-range
- `span2ptr = NULL`, `index2 = I` — no restriction on I, but I is the target dimension

#### Step 2 — Forwarded to `retrieveinarea` [retrie.c:83]

```c
temp = retrieveinarea (fullcrumptr, &span1start, &span1end, index1, &span2start, &span2end, index2, ...);
```

`index1 = V` and `index2 = I` are passed through verbatim.

#### Step 3 — `retrieveinarea` dispatches to `findcbcinarea2d` [retrie.c:97]

```c
findcbcinarea2d ((typecorecrum*)fullcrumptr, &offset, span1start, span1end, index1, span2start, span2end, index2, &context, infoptr);
```

Again `index1 = V`, `index2 = I`.

#### Step 4 — The sort happens in `findcbcinarea2d` [retrie.c:262-263]

```c
context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
incontextlistnd (headptr, context, index1);
```

**`incontextlistnd` is called with `index1 = V`.** This is the decisive line.

#### Step 5 — `incontextlistnd` sorts by that index [context.c:74-110]

The comment and function body are explicit:

```c
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
    ...
    prologuecontextnd (c, &grasp, (typedsp*)NULL);
    ...
    if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
        /* insert at beginning */
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {
            if ((whereoncontext (clist, &grasp.dsas[index], index) > ONMYLEFTBORDER)
             && (whereoncontext (nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER)) {
                /* insert in middle */
            }
        }
    }
    /* on end */
```

`grasp.dsas[index]` is the new context's position in dimension `index`. With `index = V`, insertion position is determined by V-address. The result: the context list is sorted by **V-coordinate**, smallest to largest.

#### Step 6 — Why V-order equals endset-recorded order

In `insertendsetsinorgl` [do2.c:130-148], endsets are stored by calling `insertpm` for each. Inside `insertpm` (not shown here but called at do2.c:132-133), each span is assigned a V-address starting from the endset's base V-address, then incremented by the span width:

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
```

So V-addresses are assigned strictly in the order spans are presented at link creation. Retrieving in V-order is therefore equivalent to retrieving in endset-recorded order — but the **mechanism** is V-sort, not preservation of insertion order.

#### Step 7 — The contrast: `oncontextlistseq`

For comparison, `findcbcinspanseq` [retrie.c:307-329] — used for GRAN sequential enfilades — appends without sorting:

```c
context = makecontextfromcbc ((typecbc*)crumptr, &localoffset);
oncontextlistseq (headptr, context);        /* retrie.c:323 */
```

`oncontextlistseq` [context.c:113-123] simply appends to the tail:
```c
(*clistptr)->lastcontext->nextcontext = c;
(*clistptr)->lastcontext = c;
```

The 2D POOM case (links) does not use `oncontextlistseq`. It uses `incontextlistnd` with an explicit index sort. This is a deliberate design difference.

---

### Conclusion

| Sort key | Used? | Evidence |
|---|---|---|
| I-address | **No** | `incontextlistnd` called with `index1 = V` at retrie.c:263 |
| V-address (endset position) | **Yes** | `incontextlistnd` comment: "put c on clist in index order"; `index = V` |
| Endset-recorded order (coincidentally same) | **Effectively yes** | V-addresses are assigned sequentially at link creation in do2.c:132–133 |

**Spans are returned sorted by V-address via `incontextlistnd` [context.c:74]. Because V-addresses are assigned in endset-recording order at link creation, this is equivalent to recorded order — but it is a V-sort, not a preservation of insertion sequence, and it is absolutely not an I-address sort.**
