## Question 11 [gregory]

> When a link's source endset contains multiple non-contiguous I-spans (e.g., from content that was rearranged after link creation), does RETRIEVEENDSETS return all spans as a single specset, and does the ordering of spans within that specset carry semantic meaning?

## KB Synthesis

## RETRIEVEENDSETS with Non-Contiguous I-Spans

**Does it return all spans as a single specset?**

Yes, for each endset type. RETRIEVEENDSETS returns three specsets simultaneously (from-endset, to-endset, three-endset), and within each, all resolvable I-spans are included [SS-RETRIEVE-ENDSETS]. The conversion path (`retrievesporglsetinrange` → `linksporglset2specset`) iterates over every sporgl in the endset and converts each I-span to V-addresses via the querying document's POOM. I-addresses with no current POOM mapping are **silently dropped** without error [SS-FOLLOWLINK], [INV-ITOV-FILTERING]. So the returned specset is the set of *resolvable* spans, which may be smaller than the full endset if content was deleted.

**Does ordering carry semantic meaning?**

Yes, with a caveat about fragmentation artifacts.

The I-to-V conversion path uses `incontextlistnd()`, which performs insertion-sort by V-address left boundary during B-tree traversal [INV-RETRIEVAL-V-SORTED]. This ordering is independent of tree structure — it holds regardless of how splits or rebalances arranged the internal nodes [INV-RETRIEVAL-TREE-INDEPENDENCE]. The returned specset spans are therefore **sorted in ascending V-address order**.

This ordering is semantically meaningful in the same way SpecSet ordering is generally meaningful: consuming operations (retrieve, vcopy) process VSpecs in sequence order [INV-SPECSET-ORDER], so a V-sorted endset specset reflects document position order.

**The fragmentation caveat**

When linked content has been rearranged, the endset can fragment and even produce **duplicated spans** [EC-PIVOT-LINK-FRAGMENTATION]. For example, a link on "CD" → pivot → four spans reported (1.2 for 0.1 twice, 1.5 for 0.1 twice). This duplication arises from the underlying sporgl structure: each contiguous I-address region becomes a separate sporgl [SS-LINK-ENDPOINT], and if rearrangement causes the same content to appear at multiple V-positions, the V-sorted result may contain multiple entries for logically the same content. The ordering within these duplicates still follows V-address sort, but the caller cannot treat the returned spans as a canonical non-redundant partition [EC-MULTISPAN-LINK-DUPLICATION].

**Summary**

| Property | Answer |
|---|---|
| All spans in one specset? | Yes (per endset type), silently filtered to resolvable I-addresses |
| Ordering guarantee | Ascending V-address left boundary (via `incontextlistnd` insertion-sort) |
| Ordering semantics | Yes — positional order in current document, used by consuming operations |
| Duplicates possible? | Yes, after rearrangement of linked content |

---

## Code Exploration

Now I have all the source I need. Here is the complete answer.

---

## RETRIEVEENDSETS and Multi-Span Endset Ordering

### 1. Does RETRIEVEENDSETS return all spans as a single specset?

**Yes.** For a link whose endset contains multiple non-contiguous I-spans from the same document, RETRIEVEENDSETS returns a single `typespecset` containing exactly **one `typevspec`** element whose `vspanset` holds all the V-spans.

The full call chain:

**`fns.c:350`** — `retrieveendsets` invokes `doretrieveendsets`:
```c
void retrieveendsets(typetask *taskptr) {
    if (
       getretrieveendsets (taskptr, &specset)
    && doretrieveendsets (taskptr, specset, &fromset, &toset, &threeset))
        putretrieveendsets (taskptr, fromset, toset, threeset);
```

**`do1.c:369`** — `doretrieveendsets` is a pure passthrough:
```c
bool doretrieveendsets(...) {
    return retrieveendsetsfromspanf(taskptr, specset, fromsetptr, tosetptr, threesetptr);
}
```

**`spanf1.c:190`** — `retrieveendsetsfromspanf` sets up three V-subspace probes (`fromspace` at mantissa[0]=LINKFROMSPAN=1, `tospace` at 2, `threespace` at 3) then executes the same pipeline for each endset:

```c
// spanf1.c:222-226
specset2sporglset (taskptr, specset, &sporglset, NOBERTREQUIRED)
&& retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset)
&& linksporglset2specset (taskptr, &((typevspec *)specset)->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
```

**`sporgl.c:97`** — `linksporglset2specset` converts the sporglset to a specset. For each sporgl with a non-zero `sporgladdress` (every content sporgl has a homedoc), it calls `linksporglset2vspec`:
```c
for (; sporglset; sporglset = ...) {
    specset = taskalloc(taskptr, sizeof(typevspec));
    if (iszerotumbler(&sporglset->sporgladdress)) {
        // stores as raw ISPANID
    } else {
        linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
    }
    ((typeitemheader*)specset)->next = NULL;
    *specsetptr = specset;
    specsetptr = (typespecset*)&((typeitemheader*)specset)->next;
}
```

**`sporgl.c:141`** — `sporglset2vspanset` (called from `linksporglset2vspec`) consumes **all consecutive sporgls with the same `sporgladdress`** in one pass:
```c
for (;;) {
    sporglptr = sporglptr->next;
    if (
       !sporglptr
    || !(sporglptr->itemid == SPORGLID)
    || !tumblereq (&sporglptr->sporgladdress, &(*sporglsetptr)->sporgladdress))
        return(0);   // ← breaks when homedoc changes
    *sporglsetptr = (typesporglset)sporglptr;   // ← advances outer loop pointer
    ...
    vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);
}
```

Because all I-spans in a single endset share the same document (same `sporgladdress`), this inner loop consumes all of them, folding their corresponding V-spans into a single `vspanset`. The outer loop in `linksporglset2specset` then advances past the last consumed sporgl (via the pointer update), so the result is **a single `typevspec` element** in the returned specset.

---

### 2. Does the ordering of spans within that specset carry semantic meaning?

**The ordering is mechanically determined by I-space address, not by document reading order.** Specifically:

#### Source of Ordering: `incontextlistnd` sorts by SPANRANGE

**`spanf1.c:237`** — `retrievesporglsetinrange` calls `retrieverestricted` to query the spanfilade for the link's I-span content entries, with `index1 = SPANRANGE`:
```c
context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE, whichspace, ORGLRANGE, ...);
```

**`retrie.c:87`** — `retrieveinarea` calls `findcbcinarea2d`, which at each leaf calls:
```c
// retrie.c:262-263
context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr);
incontextlistnd(headptr, context, index1);
```

**`context.c:75`** — `incontextlistnd` has an explicit comment and sorts insertion-position by `grasp.dsas[index]` (the SPANRANGE coordinate):
```c
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
    prologuecontextnd(c, &grasp, (typedsp*)NULL);
    ...
    if (whereoncontext(clist, &grasp.dsas[index], index) < THRUME) {
        c->nextcontext = clist;
        *clistptr = c;   // ← insert at front if grasp is less
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {
            // insert in sorted position
        }
    }
}
```

So the **context list — and thus the sporglset** — is in ascending I-space address order.

#### How V-spans are ordered within the vspanset

Each sporgl's I-span is converted to V-span(s) via:

**`orglinks.c:389`** → **`orglinks.c:404`** → **`orglinks.c:425`**:
```c
typevspanset *ispan2vspanset(...) {
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
// permute calls span2spanset for each restriction span:
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                             (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan*)onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`onitemlist` (`orglinks.c:464`) **appends to the tail** — no sorting. The ordering of V-spans in the vspanset is therefore the POOM traversal order for each I-span restriction, which is again driven by `findcbcinarea2d` + `incontextlistnd` — i.e., **I-space order within each I-span lookup**.

Note: `putvspaninlist` (the V-tumbler-sorted insertion used in other contexts like `retrievevspansetpm`) is **not called here**. The endset V-spans are appended in I-space traversal order, not sorted by V-tumbler.

---

### Summary

| Property | Answer |
|---|---|
| All spans returned as single specset? | **Yes** — one `typevspec` whose `vspanset` contains all V-spans |
| Ordering mechanism | `incontextlistnd` sorts contexts by **SPANRANGE (I-space address)** |
| What "I-space order" means | Permascroll position of the original content fragment at time of insertion |
| After rearrangement | I-span order ≠ V-span (document) order; returned V-spans reflect **current V-positions** for those I-addresses, but ordered by their I-space origin, not current document reading order |
| Explicit semantic meaning of order | **None defined** — the ordering is a mechanical artifact of the enfilade traversal (ascending I-space), not a semantic guarantee like "primary span first" |

**Practical consequence:** If a link's source endset was created over content at V-positions [A, B, C] and content was subsequently rearranged so those positions moved to [C, A, B], RETRIEVEENDSETS returns all three spans in a single vspec but their order within the vspanset reflects the original **I-space addresses** (permascroll order), not the new document reading order. No semantic priority is encoded in position.
