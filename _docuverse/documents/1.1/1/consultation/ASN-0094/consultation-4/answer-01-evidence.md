## Question 1 [evidence]

> Does udanax-green enforce an at-most-one-to-slot-per-from-slot constraint on attribute-like relations beyond simple slot-pair distinctness?

## KB Synthesis

The KB contains no evidence of any such constraint, and several entries directly contradict its existence.

**No uniqueness enforcement at creation time.** [PRE-LINK-CREATE] gives the full precondition for `create_link`: source content exists, target content exists, both endpoint widths ≥ 1, home_doc is valid. There is no predicate excluding duplicate from-to pairs or limiting how many links may share a source endpoint.

**Multiple outgoing links from the same slot are valid.** [EC-SELF-LINK] explicitly notes that "same span can have multiple links to different targets" (`links/overlapping_links_different_targets`). [EC-LINK-TOPOLOGY] confirms star-outgoing topology (`Hub → P1`, `Hub → P2`, `Hub → P3`) works correctly with all links discoverable.

**The link store is append-only with no deduplication.** [INV-LINK-PERMANENCE] and [FC-LINK-PERSISTENCE] establish that the link set is monotonically growing. [SS-SPANF-OPERATIONS] models the spanfilade as `Map<IAddress, Set<LinkISA>>` — a multimap that accumulates entries without any uniqueness check on the (from, to) pair.

**Discovery returns sets, not singletons.** [ST-FIND-LINKS] returns all links whose endpoint I-addresses intersect the query, implying the result cardinality is unbounded per source span.

In short, udanax-green treats links as pure graph edges in a multigraph: any number of links may share identical from-slots, identical to-slots, or both, with no slot-level arity constraint enforced anywhere in the backend.

---

## Code Exploration

I now have a complete picture. Here is the full answer.

---

## Does udanax-green enforce at-most-one-to-slot-per-from-slot on attribute-like relations?

**No. There is no such constraint anywhere in the system.** The backend is a pure-append link store. Multiple links may share an identical from-span while pointing to entirely different to-spans, and nothing in any insertion or validation path prevents or detects this.

---

### Evidence: the complete creation path

#### 1. FEBE entry point — `fns.c:100-112`

```c
void createlink(typetask *taskptr)
{
  typeisa docisa, linkisa;
  typespecset fromspecset, tospecset, threespecset;
  ...
  if (
     getcreatelink (taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
  && docreatelink (taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)){
      putcreatelink (taskptr, &linkisa);
  }else
      putrequestfailed (taskptr);
}
```

`getcreatelink` deserializes the wire request. There is no pre-flight query to discover whether the from-span is already mapped to a to-span.

#### 2. Core operation — `do1.c:195-221`

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
    typespecset fromspecset, typespecset tospecset, typespecset threespecset,
    typeisa *linkisaptr)
{
  ...
  return (
       createorglingranf (taskptr, granf, &hint, linkisaptr)   /* line 209 */
    && tumbler2spanset   (taskptr, linkisaptr, &ispanset)
    && findnextlinkvsa   (taskptr, docisaptr, &linkvsa)
    && docopy            (taskptr, docisaptr, &linkvsa, ispanset)
    && findorgl          (taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
    && specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED) /* line 214 */
    && specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED) /* line 215 */
    && specset2sporglset (taskptr, threespecset,&threesporglset,NOBERTREQUIRED) /* line 216 */
    && setlinkvsas       (&fromvsa, &tovsa, &threevsa)
    && insertendsetsinorgl(...)    /* line 218 */
    && insertendsetsinspanf(...)   /* line 219 */
  );
}
```

Steps: allocate a fresh link ISA → convert from/to specsets to sporglsets → store endsets in the link's own orglink → index them in the spanfilade. **No step queries the spanfilade for pre-existing links from the same from-span.**

#### 3. VSA validation — `do2.c:110-113`

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

The acceptability check for a virtual-space address is a stub that unconditionally succeeds. There is no opportunity here to enforce cardinality.

#### 4. Endset storage — `do2.c:116-128` and `do2.c:130-149`

```c
bool insertendsetsinspanf(...) {
    insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
    && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)
    ...
}

bool insertendsetsinorgl(...) {
    insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)
    && insertpm(taskptr, linkisaptr, link, tovsa, tosporglset)
    ...
}
```

Both functions unconditionally insert. Neither looks at what is already present.

#### 5. Permutation-matrix insertion — `orglinks.c:75-134`

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl,
              tumbler *vsaptr, typesporglset sporglset)
{
    if (iszerotumbler(vsaptr)) { ... return(FALSE); }   /* null VSA guard */
    if (tumblercmp(vsaptr, &zero) == LESS) gerror(...); /* negative VSA guard */
    logbertmodified(orglisa, user);
    for (; sporglset; sporglset = ...) {
        unpacksporgl(sporglset, ...);
        insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V); /* line 130 */
    }
    return (TRUE);
}
```

The only guards are: VSA is non-null and non-negative. There is no check for existing mappings from the same from-span.

#### 6. Leaf-node insertion — `insertnd.c:242-275`

```c
INT insertcbcnd(typecuc *father, typedsp *grasp, typewid *origin,
                typewid *width, type2dbottomcruminfo *infoptr)
{
    for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
        if (isanextensionnd((typecbc*)ptr, grasp, origin, infoptr)) {
            dspadd(&ptr->cwid, width, &ptr->cwid, ...); /* merge adjacent span */
            ...
            return(FALSE);
        }
    }
    new = createcrum(...);   /* otherwise: create a new bottom crum */
    ...
}
```

`isanextensionnd` at `insertnd.c:301-309` merges a new entry into an existing bottom crum **only if**:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
    if (!tumblereq(&infoptr->homedoc, &((type2dcbc*)ptr)->c2dinfo.homedoc))
        return(FALSE);   /* different home document → no merge */
    prologuend((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return(lockeq(reach.dsas, originptr->dsas, ...)); /* adjacent? */
}
```

The two conditions are: (a) same `homedoc` (same link ISA), and (b) the new span is exactly adjacent to the existing crum's reach. This is a **span-consolidation optimization**, not a cardinality constraint. Two distinct links with the same from-span will have different `homedoc` values (distinct ISAs), so they will never be merged here — they will each create an independent bottom crum.

#### 7. Exhaustive keyword search — all `.c` files in `backend/`

A search for `duplicate|unique|conflict|already.exist|at.most|one.to.one|constraint|atmost|injective|functional` across all C source files returns no hits related to link cardinality. The only relevant match is a comment in `do1.c:381` noting that link ISAs are unique identifiers (each link object has a distinct ISA) — which is about object identity, not relational constraints between endsets.

---

### Architectural explanation

udanax-green's link model is **polysemous by design**. A link is a first-class object in the granfilade with its own tumbler ISA. Its from-endset and to-endset are indexed in the spanfilade for bidirectional traversal (via `findlinksfromtothree`), but the spanfilade is a multimap: it associates spans with all link ISAs that touch them. Multiple links can share an identical from-span while mapping to entirely different to-spans, and the query operations (`dofindlinksfromtothree`, `sporglset2linkset`) return **sets** of matching link ISAs — the return type `typelinkset` is a list, not a scalar, precisely because many-to-many is the expected case.

There is no special "attribute link" subtype with enforced functional-dependency semantics. If a client needs attribute-like behavior (at most one to-slot value per from-slot), it must enforce that invariant itself by querying before creating.

---

### Summary

| Constraint | Enforced? | Where you'd expect it | What's actually there |
|---|---|---|---|
| New link gets unique ISA | **Yes** | `createorglingranf` [do1.c:209] | Allocates fresh tumbler ISA |
| From-span maps to at most one to-span | **No** | `docreatelink`, `insertpm`, `insertcbcnd` | Pure append, no pre-query |
| VSA validity (non-zero, non-negative) | **Yes** | `insertpm` [orglinks.c:86-98] | Two guard checks only |
| Span adjacency merge | **Yes** | `isanextensionnd` [insertnd.c:301] | Same homedoc + adjacency → merge |
