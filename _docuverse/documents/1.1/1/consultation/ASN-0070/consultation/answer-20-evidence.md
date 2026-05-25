## Question 20 [evidence]

> Does `retrieveendsets` apply the same V-address insertion-sort ordering used by `incontextlistnd` to the returned positions, or does it preserve the I-address order from the link's endset specset?

## KB Synthesis

`retrieveendsets` goes through the same insertion-sort path as any other POOM query and does **not** preserve I-address order from the endset specset.

## The Path

From [SS-RETRIEVE-ENDSETS], the call chain terminates with `linksporglset2specset()` using the querying document's docid to resolve V-addresses. [SS-FOLLOWLINK] confirms the shared mechanism: `linksporglset2specset()` calls `span2spanset()` which calls `retrieverestricted()` against the querying document's POOM orgl.

`retrieverestricted()` on a 2D POOM enfilade routes through `findcbcinarea2d()`, which accumulates results via `incontextlistnd()` [INV-RETRIEVAL-V-SORTED]. That function performs explicit insertion-sort by V-address regardless of discovery order. [INV-RETRIEVAL-TREE-INDEPENDENCE] confirms this ordering is independent of the underlying B-tree structure.

## Consequence

The I-address order from the link's endset specset is discarded during the I→V conversion step. Results emerge V-sorted by position in the querying document's POOM, not by endset creation order or I-address sequence.

**Caveat:** When an endset contains multiple sporgls (e.g., from transcluded content spanning multiple sources [SS-LINK-ENDPOINT, Finding 0037]), each sporgl produces its own sorted sub-list via `incontextlistnd`. How `linksporglset2specset` combines these sub-lists is not explicitly documented in the KB — [EC-MULTISPAN-LINK-DUPLICATION] and [EC-PIVOT-LINK-FRAGMENTATION] show that duplicate and unexpected spans can appear in multi-sporgl cases, suggesting the per-sporgl sub-lists are concatenated rather than merged into a single sorted sequence.

---

## Code Exploration

I now have all the evidence needed. Here is the complete answer.

---

## Does `retrieveendsets` Apply V-Address Insertion-Sort Order or Preserve I-Address Order?

**Answer: `retrieveendsets` returns positions in I-address (SPANRANGE) order — not V-address order. The same `incontextlistnd` function is called, but with a different index constant, making the sort key intrinsic-address rather than virtual-address.**

---

### Dimension Constants

`wisp.h:12–20` defines the dimension indices for each enfilade type:

```c
// gran:
#define WIDTH     0

// sp (spanfilade):
#define ORGLRANGE 0   // link-endpoint-type / document-origin dimension
#define SPANRANGE 1   // I-address (intrinsic) dimension

// pm (POOM / V↔I enfilade):
#define I  0          // intrinsic address dimension
#define V  1          // virtual address dimension
```

Crucially: `SPANRANGE = 1` and `V = 1` are the same integer, but they refer to **dimension 1 in different enfilades with opposite semantics**. In the spanfilade, dimension 1 (`SPANRANGE`) is the I-address of the endpoint span. In a POOM enfilade, dimension 1 (`V`) is the virtual (document) address.

---

### The `retrieveendsets` Call Chain

**`fns.c:350` `retrieveendsets`** → **`do1.c:369` `doretrieveendsets`** → **`spanf1.c:190` `retrieveendsetsfromspanf`**:

```c
// spanf1.c:222-226
specset2sporglset(taskptr, specset, &sporglset, NOBERTREQUIRED)
// converts client V-spec → I-addresses via V→I POOM traversal

retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset)
// queries the spanfilade for from-endsets matching those I-addresses

linksporglset2specset(taskptr, &docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
// converts result I-addresses back to V-space
```

**`spanf1.c:245` `retrievesporglsetinrange`** is the sort-determining call:

```c
context = retrieverestricted(
    (typecuc*)spanf,
    (typespan*)sporglptr,  // span1: the I-address range to search
    SPANRANGE,             // index1 = 1 = I-address dimension of spanfilade
    whichspace,            // span2: fromspace/tospace/threespace
    ORGLRANGE,             // index2 = 0 = orgl dimension
    (typeisa*)NULL
);
```

`retrieverestricted` (retrie.c:56–85) → `retrieveinarea` (retrie.c:87–110) → `findcbcinarea2d` (retrie.c:229–268). At the leaf level, retrie.c:263:

```c
context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr);
incontextlistnd(headptr, context, index1);   // index1 = SPANRANGE = 1
```

**`incontextlistnd` (context.c:75–111)** does an insertion-sort keyed on `dsas[index]`:

```c
// context.c:80
prologuecontextnd(c, &grasp, (typedsp*)NULL);
// grasp = c->totaloffset

// context.c:90  — "insert before clist?"
if (whereoncontext(clist, &grasp.dsas[index], index) < THRUME) { ... }
```

**`whereoncontext` (context.c:138–139)** for POOM/SPAN:

```c
movetumbler(&ptr->totaloffset.dsas[index], &left);
tumbleradd(&left, &ptr->contextwid.dsas[index], &right);
```

With `index = SPANRANGE = 1`, the sort key is `totaloffset.dsas[SPANRANGE]` — **the I-address of each found context in the spanfilade**. The context list built by `findcbcinarea2d` is therefore sorted in ascending I-address order.

Back in `retrievesporglsetinrange` (spanf1.c:248–252):

```c
for (c = context; c;) {
    contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglset, SPANRANGE);
    *sporglsetptr = (typesporglset)sporglset;
    sporglsetptr = (typesporglset*)&sporglset->next;   // append in order
    ...
}
```

`contextintosporgl` (sporgl.c:211) extracts `totaloffset.dsas[SPANRANGE]` as `sporglorigin`. Items are appended in the order they appear in the context list — **preserving I-address order**. No re-sort occurs. `linksporglset2specset` (sporgl.c:97–123) then converts each sporgl to a V-spec in list order, again without sorting.

---

### Contrast: Where `incontextlistnd` Does Apply V-Address Order

`link2sporglset` (sporgl.c:83) retrieves from the **POOM** enfilade (an orgl), not the spanfilade:

```c
context = retrieverestricted(
    (typecuc*)orgl,
    &vspan,   // span1: a V-address range
    V,        // index1 = V = 1 = V-address dimension of POOM
    (typespan*)NULL,
    I,        // index2 = I = 0
    (typeisa*)NULL
);
// ...
contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
```

Here `incontextlistnd` is called with `index = V = 1`, so it sorts by `totaloffset.dsas[V]` — the **V-address** dimension of the POOM. This is what the question calls the "V-address insertion-sort ordering used by `incontextlistnd`".

---

### Summary

| Call site | Enfilade | `index1` passed to `incontextlistnd` | Sort order |
|---|---|---|---|
| `retrievesporglsetinrange` (spanf1.c:245) | spanfilade (sp) | `SPANRANGE = 1` (I-address in sp) | **I-address** |
| `link2sporglset` (sporgl.c:83) | POOM (pm) | `V = 1` (V-address in pm) | **V-address** |

`retrieveendsets` goes through `retrievesporglsetinrange`, so it uses `index1 = SPANRANGE`. The `incontextlistnd` call at retrie.c:263 sorts by the spanfilade's I-address dimension. The resulting `fromsporglset`/`tosetptr`/`threesetptr` are in **I-address (SPANRANGE) order** — the physical ordering of endpoint records in the spanfilade — not in V-address order.

There is no post-retrieval V-address sort anywhere in the `retrieveendsets` → `retrieveendsetsfromspanf` → `retrievesporglsetinrange` → `linksporglset2specset` pipeline. The returned specsets preserve the I-address order of the link's stored endpoints.
