## Question 19 [evidence]

> Does the operation guarantee completeness — that every link whose three endsets jointly fall within the four criteria is returned regardless of which document originally created it — and is this realized as a pure I-address set intersection over the spanfilade?

## KB Synthesis

## FINDLINKSFROMTOTHREE: Completeness and Mechanism

**Yes to both**, with one structural caveat.

### Realization: Spanfilade I-address intersection

The operation works in three phases [SS-SPANF-OPERATIONS, SS-FIND-LINKS/Finding 0035]:

1. **V-to-I conversion** — each specset (from/to/three) is converted to I-spans via the document's POOM (V-space → sporglset → I-spans)
2. **Per-endpoint spanfilade lookup** — the spanfilade is queried separately for each endpoint type using ORGLRANGE subspace prefixes: `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` [INT-SPORGL-LINK-INDEX/Finding 0035]
3. **Set intersection** — `intersectlinksets()` computes the conjunction across whichever criteria were supplied; AND semantics apply [SS-FIND-LINKS/Finding 0029]: `find_links(from, to) ≡ find_links(from) ∩ find_links(to)`

When a criterion is NOSPECS, it is omitted from the intersection, not treated as empty.

### Completeness guarantee

The guarantee holds because the spanfilade is **append-only** [INV-SPANF-WRITE-ONLY]: every link endpoint ever indexed remains in the spanfilade permanently. `ST-CREATE-LINK` establishes that link creation writes all three endsets to the spanfilade atomically. No subsequent operation — including DELETE — removes spanfilade entries [INT-DELETE-SPANF-DIVERGENCE]. Therefore, for any I-address range in the query, the spanfilade lookup is exhaustive over all links ever created.

Formally: given query I-address sets F, T, P derived from the specsets, the operation returns exactly:
```
{ L | L.from ∩ F ≠ ∅ } ∩ { L | L.to ∩ T ≠ ∅ } ∩ { L | L.three ∩ P ≠ ∅ }
```

No qualifying link can be absent.

### Structural caveat: orgl-range filter is non-functional

The parameter intended to scope results by document origin is permanently disabled by a dead-code guard `TRUE||!homeset` in `sporglset2linkset()` [EC-FIND-LINKS-GLOBAL/Finding 0069]. The caller's orgl range is silently replaced with a hardcoded width-100 range from zero. The operation is therefore **unconditionally global** across the entire address space — there is no way to restrict results to links originating from a specific document. This makes the completeness claim stronger (no accidental scoping exclusions), but it means the orgl dimension of the intended 2D spanfilade query is never exercised.

### Secondary caveat: query I-address resolution depends on POOM state

Completeness is relative to the I-addresses the query resolves to. If specset content has been deleted from the document's V-stream, V-to-I conversion via the POOM yields no I-addresses, producing an empty query — not a completeness failure of the spanfilade, but a precondition gap upstream [SS-FIND-LINKS/Finding 0029, PRE-FIND-LINKS]. The spanfilade is complete; the V-to-I conversion layer is not guaranteed to expose all historically relevant I-addresses.

---

## Code Exploration

Now I have everything I need to give a precise answer.

---

## Completeness Guarantee and I-Address Set Intersection in `findlinksfromtothreesp`

The operation in question is the FEBE `find` command, realized as `findlinksfromtothreesp` in `spanf1.c`. Here is the full analysis.

---

### 1. The global spanfilade is the sole index

`findlinksfromtothreesp` [`spanf1.c:56`] is called with the global `spanf` variable. Every link ever created inserts three entries into this single global structure via `insertspanf` [`do2.c:116-128`, called from `do2.c:118-126`]:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
    typesporglset fromsporglset, typesporglset tosporglset, typesporglset threesporglset)
{
  if (!(
    insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
    &&insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))
        return (FALSE);
  if (threesporglset) {
    if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN)){
        return (FALSE); } }
  return(TRUE);
}
```

Each `insertspanf` call [`spanf1.c:15`] inserts a 2D node into the spanfilade. The two dimensions of each node are:
- **SPANRANGE**: the I-address span of the endset content
- **ORGLRANGE**: the link's ISA prefixed by the spantype (`LINKFROMSPAN`=1, `LINKTOSPAN`=2, `LINKTHREESPAN`=3)

There is **no document tag** in the index key. The `homedoc` field in the `type2dbottomcruminfo` stored in each leaf node [`spanf1.c:29,33`] is the link's own ISA, not the creating document.

---

### 2. Document-based filtering is architecturally disabled — and enforced with an abort

The call chain from `findlinksfromtothreesp` to `sporglset2linkset` to `sporglset2linksetinrange` [`sporgl.c:239`] always passes `infoptr = NULL`:

```c
/* sporgl.c:251-255 */
if (FALSE/*trying to kluge links followable thru versions */
    &&((typeitemheader *)sporglset)->itemid == SPORGLID) {
    infoptr = &linfo;
    movetumbler (&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
} else
    infoptr = NULL;
```

The `FALSE&&...` guard unconditionally sets `infoptr = NULL`. The comment reveals this was a deliberate rollback of a per-document filtering kluge.

Deeper still, `findcbcinarea2d` in `retrie.c:229` includes a hard check:

```c
/* retrie.c:243-251 */
#ifndef DISTRIBUTION
if(infoptr){
    fprintf(stderr,"not NULL infoptr versions mumble specialcase 11/27/84 shouldent happen till we try something fancier\n");
    gerror("findcbcinarea2d");
}
#else
    if (infoptr)
        gerror("!NULL");
#endif
```

In both debug and release builds, a non-NULL `infoptr` causes an immediate fatal error. This means the per-document discrimination guard in `crumqualifies2d` [`retrie.c:274`]:

```c
if ((crumptr->height == 0) && infoptr && !tumblereq (&infoptr->homedoc,
    &(((type2dcbc *)crumptr)->c2dinfo.homedoc))){
    return (FALSE);
}
```

...is **dead code for any spanfilade search**. The system will abort before ever reaching it with a non-NULL `infoptr`.

---

### 3. The orglrange criterion is also unconditionally widened

In `sporglset2linkset` [`sporgl.c:222`]:

```c
if (TRUE||!homeset) {
    tumblerclear (&nullhomeset.stream);
    tumblerclear (&nullhomeset.width);
    nullhomeset.width.mantissa[0] = 100;
    nullhomeset.next = NULL;
    homeset = &nullhomeset;
}
```

The `if (TRUE||!homeset)` expression unconditionally replaces whatever orglrange the caller passed with a zero-origin, width-100 span. This is the fourth "criterion" (the link ISA range) — and it is structurally bypassed. The range `[0..100]` in the ORGLRANGE dimension is wide enough to cover all practical link ISAs.

---

### 4. The core search: pure 2D range query with no document discrimination

`retrieverestricted` [`retrie.c:56`] converts spans to tumbler bounds and calls `retrieveinarea` → `findcbcinarea2d` [`retrie.c:229`]. The 2D search walks the enfilade tree and collects every leaf node where:

- The leaf's SPANRANGE intersects the query I-address span
- The leaf's ORGLRANGE intersects the `[spantype_prefix .. spantype_prefix+100]` range

No other filter is applied. Every matching leaf yields a link ISA via `beheadtumbler` [`sporgl.c:264`]:

```c
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE],&linksa);
    onlinklist (taskptr, linksetptr, &linksa);
}
```

---

### 5. The intersection is a pure set intersection on link ISAs

`findlinksfromtothreesp` collects three link-ISA lists — one per endset — then calls `intersectlinksets` [`spanf2.c:46`]:

```c
/* spanf1.c:76-100 */
if (fromvspecset)
    sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset,
        &fromlinkset, orglrange, LINKFROMSPAN);
if (tovspecset)
    sporglset2linkset (taskptr, (typecuc*)spanfptr, tosporglset,
        &tolinkset, orglrange, LINKTOSPAN);
if (threevspecset)
    sporglset2linkset (taskptr, (typecuc*)spanfptr, threesporglset,
        &threelinkset, orglrange, LINKTHREESPAN);
intersectlinksets(taskptr,fromlinkset,tolinkset,threelinkset,linksetptr);
```

`intersectlinksets` [`spanf2.c:46`] is a straightforward nested loop:

```c
/* spanf2.c:95-104: two-set case */
for (; temp1; temp1 = temp1->next) {
    for (temp2 = linkset2; temp2; temp2 = temp2->next) {
        if (tumblereq (&temp1->address, &temp2->address)) {
            linkset4 = makelinkitem (taskptr, &temp1->address);
            ...
        }
    }
}

/* spanf2.c:105-118: three-set case */
for (; temp1; temp1 = temp1->next)
    for (temp2 = linkset2; ...)
        for (temp3 = linkset3; ...)
            if (tumblereq (&temp1->address, &temp2->address)
                && tumblereq (&temp2->address, &temp3->address))
```

This is a pure set intersection: a link ISA appears in the result if and only if it appears in every non-null input list.

---

### 6. `acceptablevsa` is a no-op

```c
/* do2.c:110-113 */
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

No additional filtering occurs here.

---

### Conclusion

**Yes, the operation guarantees completeness in the sense asked.** Every link whose endset I-address spans satisfy the query criteria will be returned, regardless of which document originally created it. This guarantee holds because:

1. **The index is global**: `spanf` is a single structure holding all links from all documents; the only key is the I-address of the endset content [`spanf1.c:15-53`].

2. **Document filtering is architecturally eliminated**: `infoptr = NULL` is enforced at `sporgl.c:255`, and `findcbcinarea2d` aborts on any non-NULL `infoptr` [`retrie.c:243-251`], making per-document restriction permanently disabled.

3. **The orglrange criterion is bypassed**: `TRUE||!homeset` at `sporgl.c:227` forces a maximally wide link-ISA range unconditionally.

4. **The mechanism is a pure I-address set intersection**: The V→I conversion (`vspanset2sporglset` via `orglinks.c`) translates specset addresses into I-address spans; the spanfilade search collects all link ISAs whose stored endset I-spans overlap; `intersectlinksets` performs a straightforward ISA-tumbler equality intersection [`spanf2.c:96-118`].

The key architectural insight is that I-addresses are content-permanent: the same document content at the same I-address is the identity-preserving key, so a link indexed by the I-address of its endset content is findable from any V-address context that encompasses that content — this is what makes the completeness claim hold across document boundaries.
