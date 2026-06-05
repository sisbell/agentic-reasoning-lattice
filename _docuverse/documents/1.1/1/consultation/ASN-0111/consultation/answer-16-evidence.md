## Question 16 [evidence]

> For an endset that spans non-contiguous I-addresses (e.g., after a pivot fragmented the linked content), does a direct read return multiple sporgl entries per endset, and does it preserve their I-address ordering?

## KB Synthesis

## Endset Sporgl Multiplicity and Ordering

**Multiple sporgls per endset: yes.** The endset is stored as a set of I-spans (sporgls) in the link orgl, one per contiguous I-address region. `link2sporglset()` calls `retrieverestricted()` against the link orgl to extract them [SS-LINK-ENDPOINT, Finding 0037]. When a V-span at link creation time covered content from multiple sources (via transclusion), `vspanset2sporglset()` split it into one sporgl per contiguous I-region [ST-LINK-CREATE, Finding 0037]. Those multiple sporgls are what is stored and what a direct read returns.

**I-address ordering is preserved.** The link orgl lives in the GRAN enfilade. Retrieval from a 1D GRAN enfilade uses `oncontextlistseq()`, which appends contexts in tree traversal order [SS-CONTEXT-LIST, Finding 0078]. Because the GRAN tree maintains sequential I-address order by construction, the sporgls come back in ascending I-address order.

**The pivot case is a V-space phenomenon, not an endset mutation.** Pivot is I-address-preserving — `rearrangend()` modifies only `cdsp.dsas[V]` (V-dimension displacement), never I-addresses [INV-REARRANGE-IDENTITY, Finding 0056]. So the endset's stored I-address sporgls are unchanged after pivot. The "four spans with duplicates" in [EC-PIVOT-LINK-FRAGMENTATION] is a V-address artifact: RETRIEVEENDSETS resolves the endset I-addresses back through the current POOM (which now maps those I-addresses to different, potentially fragmented V-positions) via the `linksporglset2specset()` path. A direct FOLLOWLINK read returns the same sporgls as before the pivot, in the same I-address order.

---

## Code Exploration

I now have all the pieces needed to answer definitively.

---

## Answer

### The call chain for `retrieveendsets`

```
retrieveendsets [fns.c:350]
  → doretrieveendsets [do1.c:369]
    → retrieveendsetsfromspanf [spanf1.c:190]
      → specset2sporglset           (link → I-addr sporgl)
      → retrievesporglsetinrange    (sporgl + endpoint range → fragment sporgls)
      → linksporglset2specset       (sporgls → output specset)
```

---

### Q1: Does a direct read return multiple sporgl entries per endset?

**Yes.** Each contiguous I-address fragment is stored as a separate leaf crum in the 2D spanfilade. `findcbcinarea2d` [retrie.c:229] iterates every qualifying crum:

```c
// retrie.c:260-264
} else {
    context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
    incontextlistnd (headptr, context, index1);
}
```

One context entry is emitted per qualifying leaf crum. Back in `retrievesporglsetinrange` [spanf1.c:248–252], each context entry becomes exactly one `typesporgl`:

```c
// spanf1.c:249-252
sporglset = (typesporgl*) taskalloc(taskptr, sizeof(typesporgl));
contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglset, SPANRANGE);
*sporglsetptr = (typesporglset)sporglset;
sporglsetptr = (typesporglset*)&sporglset->next;
```

`contextintosporgl` [sporgl.c:205] extracts the I-address origin and width from the context:

```c
// sporgl.c:211,219
movetumbler(&context->totaloffset.dsas[index], &sporglptr->sporglorigin);
movetumbler(&context->contextwid.dsas[index],  &sporglptr->sporglwidth);
```

So N non-contiguous I-address fragments → N context entries → N sporgl entries in the returned `fromsporglset`/`tosporglset`.

---

### Q2: Does it preserve their I-address ordering?

**Yes, ascending I-address order is enforced by `incontextlistnd`.** The function comment is explicit [context.c:74]:

```c
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
```

It calls `prologuecontextnd` to compute the absolute I-address position of the new entry [context.c:80], then does a sorted insertion using `whereoncontext` comparisons [context.c:90–105]:

```c
// context.c:90-95  (insert before head)
if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
    c->nextcontext = clist;
    *clistptr = c;
    return(0);
} else {
    for (; nextc = clist->nextcontext; clist = nextc) {
        // context.c:98-103 (insert in middle)
        if ((whereoncontext (clist, ...) > ONMYLEFTBORDER)
            && (whereoncontext (nextc, ...) < ONMYLEFTBORDER)) {
            c->nextcontext = nextc;
            clist->nextcontext = c;
            return(0);
        }
    }
}
// context.c:109-110 (append at end)
clist->nextcontext = c;
```

`index1` passed to `findcbcinarea2d` [retrie.c:97] → `incontextlistnd` [retrie.c:263] is `SPANRANGE` — the I-address dimension — because `retrievesporglsetinrange` calls `retrieverestricted` with `SPANRANGE` as the first index [spanf1.c:245]:

```c
context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE,
                              whichspace, ORGLRANGE, (typeisa*)NULL);
```

The ordered context list drains sequentially in `retrievesporglsetinrange` [spanf1.c:248], so sporgl entries are produced in ascending I-address order. `linksporglset2specset` [sporgl.c:103] iterates the sporgl list without reordering, appending each to the output specset:

```c
// sporgl.c:103-121
for (; sporglset; sporglset = (typesporglset)((typeitemheader*)sporglset)->next) {
    specset = (typespecset) taskalloc(...);
    // ... fill from sporgl ...
    *specsetptr = specset;
    specsetptr = (typespecset *)&((typeitemheader *)specset)->next;
}
```

---

### Summary

| Claim | Verdict | Key cite |
|---|---|---|
| Multiple sporgl entries per fragmented endset | **Yes** | `retrie.c:262`, `spanf1.c:249` |
| Sorted in ascending I-address order | **Yes** | `context.c:74-110` |
| Order preserved through `linksporglset2specset` | **Yes** | `sporgl.c:103-121` |

**One caveat:** the sorted guarantee applies per-input-sporgl. `retrievesporglsetinrange` has an outer loop over its input sporgl list [spanf1.c:244]. Fragments from successive input sporgls are **appended** rather than merge-sorted. If the original endset was specified as a single `typevspec` (the common case after pivot), there is only one input sporgl and the output is globally sorted. If the specset contains multiple distinct `typevspec`/`typeispan` entries with non-monotone I-address ranges, the global order of the output matches the input specset ordering within each entry but not necessarily across entries.
