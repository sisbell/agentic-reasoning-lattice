## Question 8 [evidence]

> If udanax-green's follow-equivalent returns results spanning multiple subspaces, in what order are the per-subspace components emitted?

## KB Synthesis

The KB has a direct answer via the retrieval sorting invariant.

All I-to-V conversion paths in udanax-green — including those used by FOLLOWLINK and RETRIEVEENDSETS — funnel through `ispan2vspanset()` → `permute()` → `span2spanset()` → `findcbcinarea2d()`, which accumulates discovered contexts via `incontextlistnd()` [SS-CONTEXT-LIST].

`incontextlistnd()` performs insertion-sort by the left V-boundary (`totaloffset.dsas[index]`) as each leaf is discovered during B-tree traversal, regardless of tree structure [INV-RETRIEVAL-V-SORTED]. The result is a list sorted in **ascending V-address order**.

By the tumbler total order [INV-TUMBLER-TOTAL-ORDER], text subspace addresses (1.x) are strictly less than link subspace addresses (2.x). Therefore, when a follow-equivalent operation resolves I-addresses that map to both subspaces, **text-subspace (1.x) components are emitted before link-subspace (2.x) components**.

This ordering is guaranteed independent of tree structure, insertion history, or split/rebalance operations [INV-RETRIEVAL-TREE-INDEPENDENCE].

**Note:** The KB does not contain a finding that directly tests a follow-equivalent call returning spans from both subspaces simultaneously; the ordering derivation is from the general retrieval invariant, not from a dedicated multi-subspace endset scenario.

---

## Code Exploration

I now have all the source I need. Let me compile the complete answer.

---

## Answer: Per-Subspace Emission Order in Follow-Equivalent

### Call Chain

```
followlink()          [fns.c:114]
  dofollowlink()      [do1.c:223]
    link2sporglset()  [sporgl.c:67]
    linksporglset2specset() [sporgl.c:97]
```

---

### Step 1 — Retrieve Link Endpoint Contexts: `link2sporglset` [sporgl.c:67–95]

```c
// sporgl.c:81-89
tumblerincrement(&zero, 0, whichend, &vspan.stream);   // V = 1.x (from) or 2.x (to)
tumblerincrement(&zero, 0, 1, &vspan.width);
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) {
        contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
        ...
    }
```

`retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` [retrie.c:229–268].

The call passes `index1 = V`. At `retrie.c:263`:

```c
incontextlistnd(headptr, context, index1);   // index1 == V
```

---

### Step 2 — Sorting: `incontextlistnd` [context.c:75–111]

Comment at line 74: **"put c on clist in index order"**

This is an insertion sort on the **V-index** of each context. The position check [context.c:90]:

```c
if (whereoncontext(clist, &grasp.dsas[index], index) < THRUME) {
    c->nextcontext = clist;
    *clistptr = c;    // insert at beginning if new V-position is smaller
```

`whereoncontext` [context.c:124–148] extracts `ptr->totaloffset.dsas[index]` (the context's V-start) and runs `intervalcmp`. So contexts emerge from `retrieverestricted` in **ascending V-address order**.

Because V-addresses are assigned at link-creation time by sequential `tumblerincrement` calls in `insertpm` [orglinks.c:131]:

```c
tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);   // advances VSA after each insert
```

…the V-order is exactly the **insertion order** of endpoint spans at link-creation time.

---

### Step 3 — Sporgl Construction [sporgl.c:84–89]

Each context in V-sorted order becomes a sporgl [sporgl.c:205–219]:

```c
movetumbler(&context->context2dinfo.homedoc, &sporglptr->sporgladdress);  // which doc/subspace
movetumbler(&context->totaloffset.dsas[I], &sporglptr->sporglorigin);     // I-position
movetumbler(&context->contextwid.dsas[I], &sporglptr->sporglwidth);       // I-width
```

`sporgladdress` (= `homedoc`) identifies the subspace. Sporgls are chained in V-sorted order.

---

### Step 4 — Sporgl → Specset: `linksporglset2specset` [sporgl.c:97–123]

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader*)sporglset)->next) {
    ...
    linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
    ...
}
```

`sporglset2vspanset` [sporgl.c:141–176] groups consecutive sporgls with the **same `sporgladdress`** into one VSPEC:

```c
// sporgl.c:160-164
if (!sporglptr
 || !(sporglptr->itemid == SPORGLID)
 || !tumblereq(&((typesporgl*)sporglptr)->sporgladdress,
               &((typesporgl*)(*sporglsetptr))->sporgladdress))
    return(0);   // different subspace: stop grouping
```

Within each group, `ispan2vspanset` → `permute` → `span2spanset` [orglinks.c:389–454] converts I-spans back to V-spans. The inner `retrieverestricted` call there uses `index1 = I` and `targindex = V`, so **within-subspace V-spans are sorted by ascending I-position** (content order).

---

### Step 5 — Final Output Order in `dofollowlink` [do1.c:223–232]

```c
link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
&& linksporglset2specset(taskptr, &((typesporgl*)sporglset)->sporgladdress,
                         sporglset, specsetptr, NOBERTREQUIRED);
```

---

## Answer

**Per-subspace components are emitted in ascending V-address order of the link endpoint spans.** V-addresses are assigned sequentially at link-creation time (`insertpm` [orglinks.c:131]), so the subspace that was added first to the link endpoint appears first in the output.

- The sort is performed by `incontextlistnd` [context.c:75–111] with `index = V`, called from `findcbcinarea2d` [retrie.c:263].
- Consecutive sporgls sharing a `sporgladdress` (homedoc) are merged into one VSPEC by `sporglset2vspanset` [sporgl.c:158–175].
- Within each VSPEC, V-spans are in ascending I-position order (content order in that document).

**There is a code defect for the multi-subspace case.** The `homedoc` passed to `linksporglset2specset` is always `&((typesporgl*)sporglset)->sporgladdress` — the address of the **first** sporgl [do1.c:230]. `linksporglset2vspec` uses this same `homedoc` for every VSPEC's `docisa` [sporgl.c:134]:

```c
movetumbler(homedoc/*&sporglset->sporgladdress*/, &specptr->docisa);
```

The commented-out alternative `&sporglset->sporgladdress` would have used each group's actual subspace address. For endpoints spanning multiple documents, every VSPEC in the output will carry the **first document's address** as its `docisa`, and the V-span conversion (`sporglset2vspanset` calling `findorgl` with the same wrong homedoc [sporgl.c:152]) will apply the wrong enfilade, yielding incorrect V-spans for all but the first subspace.
