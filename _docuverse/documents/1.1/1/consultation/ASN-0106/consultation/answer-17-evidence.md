## Question 17 [evidence]

> When the combined read walks the POOM via vspanset2sporglset, does it emit one sporgl per contiguous I-span, automatically splitting a single requested V-span at non-contiguous I-address boundaries?

## KB Synthesis

Yes. `vspanset2sporglset` automatically emits one sporgl per contiguous I-span, splitting a single input V-span at every non-contiguous I-address boundary.

## Mechanism

The conversion chain is documented in [ST-LINK-CREATE] (Finding 0037) and [SS-VSPAN-TO-SPORGL] (Finding 0013):

1. `vspanset2sporglset` calls `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted`
2. `retrieverestricted` walks the POOM, collecting all context entries (crums) that cover the requested V-range
3. Each contiguous I-address run in the POOM becomes a separate `typeispan`
4. The inner loop at `sporgl.c:49-58` iterates over every returned I-span and creates a distinct sporgl for each, attaching the source document ISA as provenance

The splitting is entirely automatic — the caller supplies a single V-span and the function produces as many sporgls as there are disjoint I-address regions underneath it.

## Concrete evidence

[ST-LINK-CREATE] (Finding 0037) gives the canonical example: document C contains "AABB" at V 1.1–1.4, where "AA" came from document A and "BB" from document B (non-contiguous I-address regions). A single `create_link` call with that one V-span produces **two** sporgls in the endset — one per source.

[SS-LINK-ENDPOINT] (Finding 0037) states this as a structural property: "A single user-visible V-span may correspond to multiple I-spans in the endset when the V-span covers content transcluded from multiple sources. Each I-span independently tracks its content identity."

## Downstream effects

- The cardinality of the sporgl output is determined by the I-address fragmentation of the V-span's content, not by the number of input V-spans [SS-LINK-ENDPOINT]
- The same splitting occurs for any operation that routes through `vspanset2sporglset`: link creation, endset retrieval, and version comparison all share this path [INT-SPORGL-LINK-INDEX], [INT-SPORGL-TRANSCLUSION], [INT-SPORGL-VERSION-COMPARE]
- Pivot rearrangement can increase fragmentation post-hoc, causing previously single-sporgl endsets to split on subsequent retrieval [EC-PIVOT-LINK-FRAGMENTATION]

---

## Code Exploration

I now have all the evidence needed. Here is the complete answer.

---

## `vspanset2sporglset`: Does it split one V-span into multiple sporgls?

**Yes, unambiguously.** `vspanset2sporglset` emits one sporgl per contiguous I-span, and the splitting at non-contiguous I-address boundaries is automatic — it falls out of the POOM tree walk, not from any explicit splitting code.

---

### The full call chain

#### 1. `vspanset2sporglset` — sporgl.c:35–65

```c
for (; vspanset; vspanset = vspanset->next) {          // outer: one V-span at a time
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {      // inner: one sporgl per I-span
        sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
        ...
        movetumbler(&ispanset->stream, &sporglset->sporglorigin);
        movetumbler(&ispanset->width,  &sporglset->sporglwidth);
        *sporglsetptr = (typesporglset)sporglset;
        sporglsetptr = (typesporglset *)&sporglset->next;
    }
}
```

The inner loop at `sporgl.c:49` allocates **one `typesporgl` per element of `ispanset`**. The question collapses to: how many I-spans can a single V-span produce?

---

#### 2. `vspanset2ispanset` → `permute` → `span2spanset` — orglinks.c:397–454

`vspanset2ispanset` (orglinks.c:397) calls `permute` (orglinks.c:404) with direction V→I. `permute` loops over its restriction span set — but since the outer loop in `vspanset2sporglset` passes one V-span at a time, `permute` calls `span2spanset` exactly once per V-span (orglinks.c:414–415).

`span2spanset` (orglinks.c:425) is the pivotal function:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);  // line 435

for (c = context; c; c = c->nextcontext) {          // line 439: one I-span per context
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`retrieverestricted` returns a **linked list of contexts** — potentially more than one. Each context represents a distinct, contiguous leaf node in the POOM. The for-loop at `orglinks.c:439` converts each context to one I-span and appends it. So **one V-span can produce N I-spans**, one per non-contiguous I-region.

---

#### 3. `retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` — retrie.c:56–268

`retrieverestricted` (retrie.c:56) calls `retrieveinarea` (retrie.c:87), which dispatches to `findcbcinarea2d` (retrie.c:229) for `POOM`-type enfilades.

`findcbcinarea2d` (retrie.c:252–265) recursively walks the full POOM tree:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, ...)) {
        continue;
    }
    if (crumptr->height != 0) {
        ...
        findcbcinarea2d (findleftson ((typecuc*)crumptr), ...);   // descend
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);               // collect leaf
    }
}
```

Every **leaf node** (`height == 0`) that passes `crumqualifies2d` produces its own `context` via `makecontextfromcbc`. **A POOM leaf node represents a single maximal contiguous V-to-I mapping.** If the requested V-span covers content that, in the document's history, was assembled from two separate I-locations, those will be two different leaf nodes — two contexts, two I-spans, two sporgls.

---

#### 4. Context ordering — `incontextlistnd` — context.c:75–111

The comment says it all: *"put c on clist in index order"* (context.c:74). Insertion is sorted by V-position. The resulting context list is therefore ordered by V-address, so the emitted I-spans (and sporgls) come out in document V-order, not arbitrary tree-walk order.

---

#### 5. I-span clipping — `context2span` — context.c:176–212

For leaf nodes that only partially overlap the requested V-span, `context2span` clips the I-extent proportionally:

```c
if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS)
    tumblerincrement (&grasp.dsas[idx2], 0,
        (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]), &grasp.dsas[idx2]);
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER)
    tumblerincrement (&reach.dsas[idx2], 0,
        -tumblerintdiff (&reach.dsas[idx1], &upperbound), &reach.dsas[idx2]);
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

It advances the I-start by the amount the V-start undercuts the restriction's lower bound, and truncates the I-end by the amount the V-end exceeds the restriction's upper bound. This gives the exactly correct I-subspan for each contiguous chunk, even at the boundary leaf nodes.

---

### Summary

The splitting is not explicit — it is **structural**. The POOM is a 2-dimensional enfilade whose leaf nodes each record one maximal (V-region, I-region) pair. A requested V-span may span multiple such leaf nodes. `findcbcinarea2d` collects all qualifying leaves; `span2spanset` converts each to one I-span; `vspanset2sporglset` allocates one sporgl per I-span.

| Step | File | Lines | What happens |
|------|------|--------|------|
| Outer V-span loop | sporgl.c | 47 | One V-span at a time |
| POOM tree walk | retrie.c | 229–265 | Collects all qualifying leaf nodes |
| Context sorted insert | context.c | 75–111 | Sorted by V-position |
| I-span clipping | context.c | 176–212 | Adjusts I-extent at V-span boundaries |
| Sporgl allocation | sporgl.c | 49–58 | **One sporgl per I-span** |

So yes: `vspanset2sporglset` automatically emits one sporgl per contiguous I-span, splitting a single requested V-span at every non-contiguous I-address boundary it encounters in the POOM.
