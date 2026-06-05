## Question 13 [evidence]

> Does the order of VSpecs in the returned result follow the request specset's order, or is it re-sorted by V-address through incontextlistnd during tree traversal?

## KB Synthesis

Two separate ordering mechanisms apply at different levels and are not in conflict.

**SpecSet order governs inter-VSpec assembly** [INV-SPECSET-ORDER]: operations consuming a SpecSet (retrieve_contents, vcopy) process VSpecs in input sequence order and concatenate results accordingly. This is the order guarantee the client controls.

**`incontextlistnd` V-sorting governs intra-lookup ordering** [INV-RETRIEVAL-V-SORTED]: whenever the POOM is queried in the I→V direction via `findcbcinarea2d`, discovered contexts are insertion-sorted by V-address before being returned — independent of tree structure or discovery order.

These apply to different operation paths:

- **V→I direction** (retrieve_contents processing a SpecSet): the SpecSet's VSpec order is preserved in the output. `incontextlistnd` is not involved here.
- **I→V direction** (endset retrieval via `linksporglset2specset`, `follow_link`, `compare_versions`): results are V-sorted by `incontextlistnd`, regardless of any input specset ordering [SS-CONTEXT-LIST].

The consequence is most visible with multi-source transclusion [SS-LINK-ENDPOINT Finding 0037]: a link endset containing multiple sporgls returns V-spans in V-address order, not creation order. Similarly, `compare_versions` result pairs are V-sorted. Neither of these have a specset driving output order — they emerge purely from I→V POOM queries.

So: specset input order is preserved for retrieve/vcopy; I→V lookup results (endsets, follow-link, version comparison) are always V-sorted.

---

## Code Exploration

I now have the complete call chain traced. Here is the full analysis.

---

## Does `incontextlistnd` Re-Sort VSpecs by V-Address?

**Short answer:** Yes — but with precise scope. The POOM traversal re-sorts results by V-address *within each single input V-span*. The outer request-specset order (VSpec by VSpec, V-span by V-span) is preserved. The intra-span ordering is unconditionally overridden to V-address order by `incontextlistnd`.

---

## The Complete Call Chain for `retrievev`

The entry point is `fns.c:175–187`:

```c
void retrievev(typetask *taskptr) {
    ...
    getretrievev(taskptr, &specset)
    && doretrievev(taskptr, specset, &vstuffset)
    ...
}
```

`doretrievev` at `do1.c:338–346`:

```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr) {
    return
       specset2ispanset(taskptr, specset, &ispanset, READBERT)
    && ispanset2vstuffset(taskptr, granf, ispanset, vstuffsetptr);
}
```

Two phases: (1) convert VSpecs → I-spans via the POOM enfilade, (2) retrieve content from the granfilade using those I-spans.

---

### Phase 1: V→I Conversion and Where `incontextlistnd` Lives

**`specset2ispanset` (`do2.c:14–46`)** — iterates over the specset in input list order:

```c
for (; specset; specset = (typespec *)((typeitemheader *)specset)->next) {
    // for VSPECID items:
    vspanset2ispanset(taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr)
}
```

Each VSpec in request order calls into `vspanset2ispanset`.

**`vspanset2ispanset` (`orglinks.c:397–402`):**

```c
typeispanset *vspanset2ispanset(...) {
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

Passes `restrictionindex=V`, `targindex=I`.

**`permute` (`orglinks.c:404–422`)** — iterates each V-span in input order:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                  restrictionindex /*V*/, targspansetptr, targindex /*I*/);
}
```

**`span2spanset` (`orglinks.c:425–454`)** — calls into the POOM and iterates the context list it gets back:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex /*V*/,
                              (typespan*)NULL, targindex /*I*/, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

The context list from `retrieverestricted` is iterated in whatever order it was built. That order is determined by `incontextlistnd`.

**`retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` (`retrie.c:229–268`):**

`findcbcinarea2d` walks the POOM tree left-to-right by sibling (tree traversal order, not V-address order):

```c
for (; crumptr; crumptr = getrightbro(crumptr)) {
    if (!crumqualifies2d(...)) continue;
    if (crumptr->height != 0) {
        findcbcinarea2d(findleftson((typecuc*)crumptr), &localoffset, ...headptr, infoptr);
    } else {
        context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd(headptr, context, index1);   /* index1 = V */
    }
}
```

This is the critical line: `incontextlistnd(headptr, context, index1)` at `retrie.c:263`.

**`incontextlistnd` (`context.c:74–111`):**

```c
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
    prologuecontextnd(c, &grasp, (typedsp*)NULL);
    ...
    /* 1st insertion */
    if (!clist) { *clistptr = c; return(0); }

    /* on beginning — insert before head if address falls before it */
    if (whereoncontext(clist, &grasp.dsas[index], index) < THRUME) {
        c->nextcontext = clist;
        *clistptr = c;
        return(0);
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {
            /* in middle — find correct sorted insertion point */
            if ((whereoncontext(clist, ...) > ONMYLEFTBORDER)
             && (whereoncontext(nextc, ...) < ONMYLEFTBORDER)) {
                c->nextcontext = nextc;
                clist->nextcontext = c;
                return(0);
            }
        }
    }
    /* on end */
    clist->nextcontext = c;
}
```

The comment is authoritative: **"put c on clist in index order"**. The insertion sort compares `grasp.dsas[index]` — which is `dsas[V]` since `index1=V` in the V→I conversion path — against the left and right boundaries of existing contexts. New contexts are placed in ascending V-address order, not in tree-traversal order.

**The contrast with `oncontextlistseq` (`context.c:113–123`):**

```c
int oncontextlistseq(typecontext **clistptr, typecontext *c) {
    c->nextcontext = NULL;
    if (!*clistptr) {           /* 1st insertion */
        *clistptr = c;
        c->lastcontext = c;
    } else {                    /* on end */
        (*clistptr)->lastcontext->nextcontext = c;
        (*clistptr)->lastcontext = c;
    }
}
```

This is a pure FIFO append — no sorting. Used by `findcbcinspanseq` (`retrie.c:323`) for the granfilade (I-axis sequential retrieval). The two functions serve distinct roles: `incontextlistnd` for 2D POOM traversal (V-sorted output), `oncontextlistseq` for 1D sequential traversal (storage-order output).

---

### Phase 2: I-Spans → Content (`ispanset2vstuffset`)

`granf1.c:57–74` iterates the ispanset in its built order:

```c
for (; ispanset; ispanset = ispanset->next) {
    vstuffsetptr = ispan2vstuffset(taskptr, granfptr, ispanset, vstuffsetptr);
}
```

Each `ispan2vstuffset` (`granf2.c:286–318`) calls `retrieveinspan` which uses `findcbcinspanseq` → `oncontextlistseq` — **sequential I-address order** — for the granfilade traversal. Content within a single I-span comes back in storage/insertion order.

---

## Summary of Ordering at Each Level

| Level | Ordering Mechanism | Order |
|---|---|---|
| VSpec to VSpec | `specset2ispanset` loop at `do2.c:23` | **Input request specset order** |
| V-span to V-span within VSpec | `permute` loop at `orglinks.c:414` | **Input vspanset order** |
| POOM crums within a single V-span | `incontextlistnd` at `retrie.c:263` with `index=V` | **V-address ascending** (re-sorted) |
| Content within a single I-span | `oncontextlistseq` at `retrie.c:323` | **I-address (storage/insertion) order** |

---

## Definitive Answer

**The outer structure (VSpec order, V-span order) follows the request specset order.** `specset2ispanset` iterates `specset->next` in input order (`do2.c:23`), and `permute` iterates `restrictionspanset->next` in input order (`orglinks.c:414`).

**Within each individual V-span, the POOM traversal re-sorts by V-address.** `findcbcinarea2d` walks the tree in left-to-right sibling order (tree storage order), which is not guaranteed to be V-address order. `incontextlistnd` at `retrie.c:263` corrects this by insertion-sorting every bottom-level crum into the context list by `dsas[V]` position. The resulting I-spans — and therefore the text content in the vstuffset — emerge in V-ascending order within each requested V-span, regardless of the tree's internal storage topology.

This is a deliberate design: the POOM is a two-dimensional structure, and `incontextlistnd` enforces a canonical sorted order along the restriction dimension so that callers receive a well-ordered I-span set regardless of how the permutation matrix happens to be laid out on disk.
