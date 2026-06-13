## Question 1 [evidence]

> Can udanax-green create a link with empty from and to endsets that still appears in link-search results (matching via its type endset), and if so, what I-address positions such a link in the spanfilade/`onlinklist` result order — i.e., is every returned link guaranteed a non-empty covered I-address on the slot that drives ordering?

## KB Synthesis

## Can udanax-green create a link with empty from/to that appears in link-search results via its type endset?

The KB allows a precise answer on each sub-question.

---

### 1. Can such a link be created?

Probably yes, but the KB is silent on the exact case.

[PRE-ZERO-WIDTH] and [PRE-LINK-CREATE] (Finding 0028) document that providing a **zero-width span** in the source or target specset crashes the backend (Bug 0017). However, NOSPECS (an *empty* specset — no VSpecs at all) is structurally different from "a VSpec whose width = 0." The `vspanset2sporglset` path that causes the crash is reached via span iteration; an empty specset produces no iterations, so the crash path is not entered.

If NOSPECS is passed for both source and target:
- `insertendsetsinspanf` receives empty sporglsets for LINKFROMSPAN and LINKTOSPAN → inserts zero entries in those subspaces [INT-SPORGL-LINK-INDEX]
- The link orgl is still created in the granfilade [ST-CREATE-LINK, SS-DUAL-ENFILADE]
- Only type-endset I-addresses (LINKTHREESPAN subspace) are registered in the spanfilade

The KB contains no golden test for this exact creation scenario, so behaviour is inferred, not confirmed.

---

### 2. Would such a link appear in `find_links` results?

**No — it is effectively invisible through all search paths.**

**Path A — FROM-driven search** (`find_links(from_spec, …)`):  
The spanfilade is searched in the LINKFROMSPAN=1 subspace [SS-RETRIEVE-ENDSETS, Finding 0035]. The link has no entries there, so it cannot be returned. The intersection with the FROM result-set yields empty. [SS-FIND-LINKS, Finding 0028]

**Path B — TO-driven search** (`find_links(NOSPECS, to_spec, …)`):  
Same logic: no LINKTOSPAN=2 entries → not found. [SS-FIND-LINKS, Finding 0029]

**Path C — TYPE-driven search** (`find_links(…, type_spec)`):  
This is the only slot where the link *does* have spanfilade entries (LINKTHREESPAN=3). However, [EC-TYPE-FILTER-NONFUNCTIONAL] (Finding 0029) documents that type filtering is broken: `find_links(source, NOSPECS, type_spec)` returns empty even when unfiltered search finds links of those types. The `intersectlinksets` intersection collapses to empty because the THREE search contributes nothing usable. The KB offers no evidence this failure mode is limited to the combination with a non-NOSPECS source — it appears to reflect a defect in the THREE-dimension search path itself.

**Path D — Full NOSPECS (`find_links(NOSPECS, NOSPECS, NOSPECS)`):**  
With all dimensions NOSPECS, the call returns *all* links by effectively running no constraint. Such a call would include the link — but this is not "appearing via its type endset," it is appearing because nothing is filtered out. It tells us nothing about the type-slot mechanism.

**Conclusion:** a link with empty from/to endsets is unreachable by any content-identity-based search. It is accessible only via direct `follow_link(link_id, …)` if the link ISA is already known [INV-LINK-PERMANENCE, SS-FOLLOWLINK].

---

### 3. What I-address positions such a link in the spanfilade / `onlinklist` result order?

The `findlinksfromtothreesp` result is a linked list of `typelinkset` structs built by spanfilade traversal in I-address (SPAN-dimension) order. [SS-PAGINATE-LINKS, Finding 0035]

For the FROM-driven case: the ordering position of any returned link is the I-address in the LINKFROMSPAN subspace that matched the query range. For the type-only link this I-address does not exist, so the link has no position in FROM-driven results — it is simply absent.

If type-based search *were* functional, the ordering position would be determined by the LINKTHREESPAN I-addresses of the type endset content. Those I-addresses are non-empty by construction (the link was created with a valid type specset), so the link would have a well-defined, non-empty ordering position in that slot.

---

### 4. Is every returned link guaranteed a non-empty covered I-address on the slot driving result order?

**Yes, tautologically**, for any functional search path:

The spanfilade maps `I-address → {LinkISA}` [SS-SPANF-OPERATIONS]. A link ISA appears in the FROM-driven result only because the spanfilade found it indexed at some I-address in the LINKFROMSPAN subspace. That I-address is the coverage entry that placed it in the traversal. A link with no LINKFROMSPAN entries cannot be reached by FROM-driven traversal at all. The result list therefore cannot contain a link whose ordering slot has empty coverage — the coverage is the precondition for inclusion. [INV-RETRIEVAL-V-SORTED, SS-CONTEXT-LIST]

The same logic applies to TO-driven and — were the type filter functional — THREE-driven searches.

---

### Summary

| Question | Answer | Key KB entries |
|---|---|---|
| Can a link be created with NOSPECS from/to? | Probably yes (NOSPECS ≠ zero-width span) | [PRE-ZERO-WIDTH], [PRE-LINK-CREATE] |
| Does it appear in `find_links` results? | No — FROM/TO searches miss it; type search is broken | [EC-TYPE-FILTER-NONFUNCTIONAL], [SS-FIND-LINKS] |
| What I-address slots it in result order? | Type-endset I-addresses (LINKTHREESPAN), but unreachable | [SS-RETRIEVE-ENDSETS], [SS-PAGINATE-LINKS] |
| Is every returned link guaranteed non-empty coverage on its ordering slot? | Yes — coverage is the necessary condition for appearing in the result list at all | [SS-SPANF-OPERATIONS], [INV-RETRIEVAL-V-SORTED] |

---

## Code Exploration

Now I have everything I need. Let me compile the full answer.

---

## Full Analysis

### Can a link with empty from and to endsets be created?

**YES.** Here is the complete code path.

#### `docreatelink` — `do1.c:195`

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr, typespecset fromspecset, typespecset tospecset, typespecset threespecset, typeisa *linkisaptr)
{
  ...
  return (
       createorglingranf (...)
    && tumbler2spanset (...)
    && findnextlinkvsa (...)
    && docopy (...)
    && findorgl (...)
    && specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)   // [do1.c:214]
    && specset2sporglset (taskptr, tospecset, &tosporglset, NOBERTREQUIRED)       // [do1.c:215]
    && specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED) // [do1.c:216]
    && setlinkvsas (&fromvsa, &tovsa, &threevsa)
    && insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset)
    && insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
  );
}
```

#### Step 1 — `specset2sporglset` with NULL specset — `sporgl.c:14`

```c
bool specset2sporglset(typetask *taskptr, typespecset specset, typesporglset *sporglsetptr, int type)
{
  *sporglsetptr = NULL;
  for (; specset; ...)   // loop body never runs when specset == NULL
    { ... }
  *sporglsetptr = NULL;
  return (TRUE);         // returns TRUE unconditionally
}
```

With `fromspecset==NULL` and `tospecset==NULL`, both calls set their output sporglset to NULL and return `TRUE`. The `&&`-chain continues.

#### Step 2 — `setlinkvsas` — `do2.c:169`

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
  tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);
  tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);   // fromvsa = 1.1
  tumblerincrement(tovsaptr,   0, 2, tovsaptr);
  tumblerincrement(tovsaptr,   1, 1, tovsaptr);     // tovsa   = 2.1
  if (threevsaptr) {
    tumblerincrement(threevsaptr, 0, 3, threevsaptr);
    tumblerincrement(threevsaptr, 1, 1, threevsaptr); // threevsa = 3.1
  }
  return (TRUE);
}
```

All three VSAs are set to non-zero tumblers.

#### Step 3 — `insertendsetsinorgl` — `do2.c:130`

```c
bool insertendsetsinorgl(typetask *taskptr, tumbler *linkisaptr, typeorgl link,
    tumbler *fromvsa, typesporglset fromsporglset,
    tumbler *tovsa,   typesporglset tosporglset,
    tumbler *threevsa, typesporglset threesporglset)
{
  if (!( insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)    // [do2.c:132] always called
      && insertpm(taskptr, linkisaptr, link, tovsa, tosporglset)))       // [do2.c:133] always called
    return (FALSE);
  if (threevsa && threesporglset) {
    if (!insertpm(taskptr, linkisaptr, link, threevsa, threesporglset))  // [do2.c:137]
      return (FALSE);
  }
  return (TRUE);
}
```

Inside `insertpm` (orglinks.c:75):

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, tumbler *vsaptr, typesporglset sporglset)
{
  if (iszerotumbler(vsaptr)) {   // [orglinks.c:86] — fromvsa=1.1 is NOT zero, passes
    return (FALSE);
  }
  logbertmodified(orglisa, user);
  for (; sporglset; sporglset = sporglset->xxxxsporgl.next) {   // [orglinks.c:100]
    // loop body — never runs when sporglset==NULL
    unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
    insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
  }
  return (TRUE);
}
```

With NULL `fromsporglset`/`tosporglset`, the loop body never executes but `insertpm` still returns `TRUE`. Nothing is inserted into the link's POOM for those slots. The three-endset POOM insertion proceeds normally (if non-NULL).

#### Step 4 — `insertendsetsinspanf` — `do2.c:116`

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
    typesporglset fromsporglset, typesporglset tosporglset, typesporglset threesporglset)
{
  if (!(
    insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // [do2.c:119]
  &&insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)))   // [do2.c:120]
    return (FALSE);
  if (threesporglset) {                                                        // [do2.c:122]
    if (!insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN))
      return (FALSE);
  }
  return (TRUE);
}
```

Inside `insertspanf` (spanf1.c:15):

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr, typesporglset sporglset, INT spantype)
{
  prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
  tumblerclear(&crumwidth.dsas[ORGLRANGE]);
  for (; sporglset; sporglset = ...) {   // [spanf1.c:25] — never runs when sporglset==NULL
    ...
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
  }
  return (TRUE);   // always TRUE
}
```

With NULL `fromsporglset`/`tosporglset`, no crums are inserted into the spanfilade for `LINKFROMSPAN` or `LINKTOSPAN`. Only if `threesporglset` is non-NULL (the type endset is non-empty) does `insertspanf` insert any crums — for `LINKTHREESPAN`.

**Conclusion on creation**: A link with empty from and to endsets can be created without error. The `&&`-chain completes. The link gets an ISA, is placed in the document's V-space at `findnextlinkvsa`'s position, and the type-endset crums are indexed in the spanfilade under `LINKTHREESPAN`. No crums exist for `LINKFROMSPAN` or `LINKTOSPAN`.

---

### Does such a link appear in link-search results via its type endset?

**YES.** The controlling function is `findlinksfromtothreesp` (spanf1.c:56):

```c
bool findlinksfromtothreesp(typetask *taskptr, typespanf spanfptr,
    typespecset fromvspecset, typespecset tovspecset, typespecset threevspecset,
    typeispan *orglrange, typelinkset *linksetptr)
{
  fromlinkset = tolinkset = threelinkset = NULL;            // [spanf1.c:69]

  if (fromvspecset)                                         // [spanf1.c:70] FALSE → skipped
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);

  if (tovspecset)                                           // [spanf1.c:72] FALSE → skipped
    specset2sporglset(taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);

  if (threevspecset)                                        // [spanf1.c:74] TRUE
    specset2sporglset(taskptr, threevspecset, &threesporglset, NOBERTREQUIRED);

  if (fromvspecset) {                                       // [spanf1.c:76] FALSE → fromlinkset stays NULL
    sporglset2linkset(taskptr, spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
    if (!fromlinkset) { *linksetptr = NULL; return(TRUE); }
  }
  if (tovspecset) {                                         // [spanf1.c:84] FALSE → tolinkset stays NULL
    sporglset2linkset(taskptr, spanfptr, tosporglset, &tolinkset, orglrange, LINKTOSPAN);
    if (!tolinkset) { *linksetptr = NULL; return(TRUE); }
  }
  if (threevspecset) {                                      // [spanf1.c:92] TRUE
    sporglset2linkset(taskptr, spanfptr, threesporglset, &threelinkset, orglrange, LINKTHREESPAN);
    if (!threelinkset) { *linksetptr = NULL; return(TRUE); }
  }
  intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);  // [spanf1.c:100]
  return (TRUE);
}
```

With `fromvspecset=NULL`, `tovspecset=NULL`, `threevspecset=<type content>`:
- `fromlinkset` and `tolinkset` remain NULL (their `if` guards are never entered)
- `threelinkset` gets all links whose type endset overlaps the searched I-span
- `intersectlinksets(NULL, NULL, threelinkset, linksetptr)` is called

In `intersectlinksets` (spanf2.c:63):

```c
int intersectlinksets(typetask *taskptr, typelinkset linkset1, typelinkset linkset2,
    typelinkset linkset3, typelinkset *linkset4ptr)
{
  if (linkset1 && !linkset2 && !linkset3)
    *linkset4ptr = linkset1;
  else if (!linkset1 && linkset2 && !linkset3)
    *linkset4ptr = linkset2;
  else if (!linkset1 && !linkset2 && linkset3)   // [spanf2.c:68] ← this branch
    *linkset4ptr = linkset3;
  else
    *linkset4ptr = NULL;

  if (*linkset4ptr) {    // [spanf2.c:73] TRUE → returns immediately
    return(0);
  }
  // ... pairwise intersection (not reached) ...
}
```

Since only `linkset3` (`threelinkset`) is non-NULL, `intersectlinksets` takes the single-non-null branch at `[spanf2.c:68]`, assigns `*linkset4ptr = linkset3`, and returns immediately. **The search result is the set of links found via the type endset — with no filtering by from or to.** A link with empty from and to endsets appears in the result.

---

### What I-address positions the link in the result order?

#### How crums are inserted — `insertspanf` — `spanf1.c:49`

For the type endset, `insertspanf` inserts into the spanfilade with:

```c
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);   // [spanf1.c:49] I-address of type content
movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);    // width of type content
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

Where `lstream` and `lwidth` come from `sporglset->sporglorigin` and `sporglset->sporglwidth` — the permascroll I-address and width of the type endset content (extracted at `spanf1.c:31-32`). The `ORGLRANGE` dimension is `prefixtumbler(linkisa, LINKTHREESPAN)` — the link's own ISA prefixed with the slot number.

So each type-endset crum in the spanfilade is a 2D entry:

| Dimension | Value |
|-----------|-------|
| `SPANRANGE` | I-address of the type content (permascroll origin + width) |
| `ORGLRANGE` | `LINKTHREESPAN prefix` ++ `link ISA` |

#### How the search produces ordered contexts — `findcbcinarea2d` — `retrie.c:229`

When `sporglset2linksetinrange` searches the spanfilade:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
    &range, ORGLRANGE, (typeisa*)infoptr);   // [sporgl.c:259]
```

This calls `findcbcinarea2d` with `index1=SPANRANGE`, which calls:

```c
incontextlistnd(headptr, context, index1);   // [retrie.c:263] — sorted insertion by SPANRANGE
```

In `incontextlistnd` (context.c:75):

```c
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
  prologuecontextnd(c, &grasp, (typedsp*)NULL);  // grasp = c->totaloffset
  ...
  /* on beginning */
  if (whereoncontext(clist, &grasp.dsas[index], index) < THRUME) {
    c->nextcontext = clist; *clistptr = c; return(0);
  } else {
    for (; nextc = clist->nextcontext; clist = nextc) {
      /* in middle */
      if ((whereoncontext(clist, &grasp.dsas[index], index) > ONMYLEFTBORDER)
       && (whereoncontext(nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER)) {
        c->nextcontext = nextc; clist->nextcontext = c; return(0);
      }
    }
  }
  /* on end */
  clist->nextcontext = c;
}
```

This is an in-order insertion sort keyed on `grasp.dsas[SPANRANGE]` — the I-address (permascroll position) of the type endset content. **The context list produced by `retrieverestricted` is ordered by ascending SPANRANGE — i.e., by the permascroll I-address of the content in the type endset.**

Then `sporglset2linksetinrange` processes contexts in this order:

```c
for (c = context; c; c = c->nextcontext) {
  beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);  // [sporgl.c:264] — strip slot prefix → link ISA
  onlinklist(taskptr, linksetptr, &linksa);                  // [sporgl.c:265] — append to result list
}
```

And `onlinklist` (spanf2.c:26) appends to the end (after dedup), preserving the SPANRANGE order.

**The I-address that positions a link in the result order is the SPANRANGE position of the type endset content: the permascroll I-address (`sporglorigin`) of the type/anchor content stored in that link's `LINKTHREESPAN` spanfilade crum.** Multiple links can share the same SPANRANGE region (if their type endsets reference the same permascroll I-span), in which case they appear grouped by I-address and sub-ordered by the sequence that `retrieverestricted` walks the tree.

---

### Is every returned link guaranteed a non-empty covered I-address on the ordering slot?

**YES**, enforced by two chained invariants:

**Invariant 1 — insertion rejects zero-width spans.** `unpacksporgl` (sporgl.c:195):

```c
if (iszerotumbler(widthptr)) {
  qerror("zero width in unpacksporgl\n");   // aborts
}
```

And `insertpm` (orglinks.c:121):

```c
if (iszerotumbler(&crumwidth.dsas[V]))
  gerror("crum width 0 in insertpm\n");     // aborts
```

No zero-width crum can be stored. Every `LINKTHREESPAN` spanfilade crum has a non-zero `SPANRANGE` width.

**Invariant 2 — retrieval only returns crums that overlap the query span.** `crumqualifies2d` (retrie.c:270) filters crums by span overlap on both index1 (SPANRANGE) and index2 (ORGLRANGE). A crum is returned only if the search query's I-span intersects the crum's SPANRANGE. Since both the query span and the crum have non-zero width (invariant 1), their intersection is non-empty.

Therefore: every link returned from a type-endset search has a non-empty (positive-width) covered I-address in the `SPANRANGE` slot that drives the result ordering. There is no code path by which a zero-width SPANRANGE crum could be inserted or returned.

---

### Summary

| Question | Answer | Key lines |
|----------|--------|-----------|
| Can a link with empty from/to be created? | **Yes** | `specset2sporglset(NULL)` → TRUE [sporgl.c:18], `insertspanf(NULL, ...)` → loop skips, TRUE [spanf1.c:25] |
| Does it appear via type-endset search? | **Yes** | `intersectlinksets(NULL, NULL, threelinkset)` → returns `threelinkset` directly [spanf2.c:68] |
| What I-address drives ordering? | `sporglorigin` of the type endset's permascroll span — the SPANRANGE coord in the `LINKTHREESPAN` spanfilade crum | `insertspanf` [spanf1.c:49], `incontextlistnd(..., SPANRANGE)` [retrie.c:263, context.c:75] |
| Non-empty I-address guaranteed? | **Yes** — zero-width crums are rejected at insertion and at retrieval | `unpacksporgl` [sporgl.c:195], `insertpm` [orglinks.c:121], `crumqualifies2d` [retrie.c:270] |
