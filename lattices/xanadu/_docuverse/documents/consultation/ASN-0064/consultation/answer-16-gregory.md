## Question 16 [gregory]

> When resolving a discovered link's endsets back to V-addresses via `linksporglset2specset`, how does the I→V conversion handle an I-address that maps to multiple V-positions within the same document (e.g., after self-transclusion) — does it return all V-positions or just the first found?

## KB Synthesis

## I→V Conversion Returns All V-Positions

The conversion returns **all** V-positions, not just the first found.

### The Mechanism

`linksporglset2specset` follows the call chain documented in [SS-FOLLOWLINK]:

```
link2sporglset() → linksporglset2specset() → span2spanset() → retrieverestricted()
```

`retrieverestricted()` drives the POOM B-tree traversal via `findcbcinarea2d()`. The critical property is in [SS-POOM-MULTIMAP]: this traversal **iterates all siblings at each level and recurses into all qualifying subtrees**, accumulating every matching leaf node. The accumulation function `incontextlistnd()` performs insertion-sort into a linked list and **never replaces existing entries** — it only appends new ones. There is no early-exit after the first match.

The POOM is explicitly a multimap (`Multimap<(VPosition, IAddress)>`), and `ispan2vspanset` has return type `Set<VSpan>` with the postcondition `|result| >= 1` when the I-address exists [SS-POOM-MULTIMAP].

### Concrete Confirmation

From [SS-POOM-MULTIMAP] (Finding 0039), for a document with "B" at V-positions 1.2, 1.4, and 1.5 all referencing I-address `i_B`:

```
ispan2vspanset(poom, i_B) = {
  VSpan(1.2, width=0.1),
  VSpan(1.4, width=0.1),
  VSpan(1.5, width=0.1)
}
```

All three V-positions are returned.

### Ordering

The result is sorted by V-address via `incontextlistnd`'s insertion-sort [INV-RETRIEVAL-V-SORTED], and this ordering is independent of tree structure [INV-RETRIEVAL-TREE-INDEPENDENCE].

### Implication for Link Endset Resolution

When `linksporglset2specset` resolves a link endset containing an I-address that was self-transcluded N times within the home document, it produces N V-spans — one per V-position referencing that I-address. This is precisely the behavior noted in [INV-LINK-IDENTITY-DISCOVERY]: links are discoverable from *all* V-positions sharing an I-address, and the endset resolution mirrors this by reporting all of them.

The silent-drop behavior noted in [SS-FOLLOWLINK] (when `retrieverestricted` returns NULL) only applies when **no** POOM entry exists for the I-address — not as a cardinality limit on multiple entries.

---

## Code Exploration

Now I have everything needed. Here is the complete answer:

---

## I→V Conversion in `linksporglset2specset`: All V-Positions Are Returned

The conversion returns **all** V-positions, not just the first. The full call chain is exhaustive at every layer. Here is the trace.

---

### Layer 1 — `linksporglset2specset` [`sporgl.c:97–123`]

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader*)sporglset)->next) {
    specset = (typespecset) taskalloc(taskptr, sizeof(typevspec));
    if (iszerotumbler(&((typesporgl *)sporglset)->sporgladdress)) {
        // pure I-span: zero address means no home doc
        ((typeitemheader *)specset)->itemid = ISPANID;
        ...
    } else {
        linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
    }
    ((typeitemheader *)specset)->next = NULL;
    *specsetptr = specset;
    specsetptr = (typespecset *)&((typeitemheader *)specset)->next;  // [sporgl.c:120]
}
```

Every sporgl item in the input list produces one output `specset` item. The `specsetptr` pointer is advanced at line 120, building a linked list. **No early exit.**

For sporgls with a non-zero `sporgladdress` (the normal case — the endset has a known home document in I-space), conversion delegates to `linksporglset2vspec` → `sporglset2vspanset` [`sporgl.c:141`] → `ispan2vspanset` [`orglinks.c:389`].

---

### Layer 2 — `ispan2vspanset` / `permute` [`orglinks.c:389–422`]

```c
typevspanset *ispan2vspanset(...) {
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);  // [orglinks.c:393]
}

typespanset *permute(...) {
    save = targspansetptr;
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
        targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                     restrictionindex, targspansetptr, targindex);
    }
    return (save);  // [orglinks.c:421]
}
```

`permute` iterates over all restriction spans in the input set (in this case the single I-span), accumulating results into `targspansetptr`.

---

### Layer 3 — `span2spanset` [`orglinks.c:425–454`]

This is the critical function:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr,
                             restrictionindex, (typespan*)NULL, targindex, (typeisa*)NULL);
// [orglinks.c:435]

for (c = context; c; c = c->nextcontext) {          // [orglinks.c:439]
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan,
                                    (typeitemset*)targspansetptr);
}
if (!context) {
    return(targspansetptr);   // [orglinks.c:447] — only on empty result
}
contextfree(context);
return (&nextptr->next);      // [orglinks.c:453]
```

`retrieverestricted` returns a **linked list** of contexts — one per matching enfilade crum. The `for` loop at line 439 processes **every context** in that list. `onitemlist` at line 444 appends each converted V-span to the growing result list. The only early return (line 447) fires only when `retrieverestricted` finds **nothing** at all.

---

### Layer 4 — `retrieverestricted` → `findcbcinarea2d` [`retrie.c:56–268`]

`retrieverestricted` [`retrie.c:56`] → `retrieveinarea` [`retrie.c:87`] → `findcbcinarea2d` [`retrie.c:229`]:

```c
for (; crumptr; crumptr = getrightbro(crumptr)) {  // [retrie.c:252]
    if (!crumqualifies2d(crumptr, ...)) {
        continue;
    }
    if (crumptr->height != 0) {
        findcbcinarea2d(findleftson((typecuc*)crumptr), &localoffset, ...);  // recursive
    } else {
        context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd(headptr, context, index1);  // [retrie.c:263] — APPEND
    }
}
```

This recursively traverses the entire POOM enfilade. At every **leaf crum** (`height == 0`) that passes `crumqualifies2d`, a context is created and **appended** to `*headptr` via `incontextlistnd`. The traversal is exhaustive: no crum is skipped once qualified, and there is no early `return` after the first match.

After self-transclusion, the same I-range appears as a mapping source in **multiple** crums (the original insertion and the transcluded copy), each at a different V-position. `findcbcinarea2d` finds all of them.

---

### Layer 5 — `incontextlistnd` [`context.c:75–111`]

```c
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
    ...
    if (!clist) { *clistptr = c; return(0); }          // first item
    if (whereoncontext(...) < THRUME) {                 // insert at head
        c->nextcontext = clist; *clistptr = c; return(0);
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {  // insert in middle
            if (...) { ...; return(0); }
        }
    }
    clist->nextcontext = c;   // [context.c:110] — insert at tail
}
```

`incontextlistnd` maintains a **sorted linked list**. It always inserts — it never discards a result. Every context created by `findcbcinarea2d` ends up in the list.

---

### Answer

**All V-positions are returned.** When an I-address maps to N distinct V-positions (e.g., after self-transclusion: the original at V=1.0.1 and the copy at V=1.0.3), `findcbcinarea2d` finds both leaf crums, `incontextlistnd` appends both to the context list, and `span2spanset`'s `for (c = context; c; c = c->nextcontext)` loop at [`orglinks.c:439`] converts both to V-spans and appends both to the result via `onitemlist`. The final `vspanset` handed back through `ispan2vspanset` → `sporglset2vspanset` → `linksporglset2vspec` is a linked list with one entry per V-position.

The only coalescing that could reduce this count is `putvspaninlist` [`orglinks.c:329`], which merges adjacent/overlapping spans. But `span2spanset` uses `onitemlist` (not `putvspaninlist`), which does **no merging** — it simply appends. So distinct V-positions from self-transclusion emerge as distinct entries in the returned set.
