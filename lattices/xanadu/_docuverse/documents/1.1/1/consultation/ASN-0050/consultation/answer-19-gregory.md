## Question 19 [gregory]

> If content at I-address range `[.0.1.1, .0.1.5]` is DELETEd from document A, then later a COPY transcludes those same I-addresses from document B (which still holds them) back into document A, does `find_links` rediscover links whose endsets reference that I-address range, and does document A's stale DOCISPAN entry in the spanfilade coexist with the new DOCISPAN entry from the re-transclusion?

## KB Synthesis

## After DELETE + Re-transclusion COPY

### Part 1: `find_links` Rediscovery

**Yes — links are fully rediscovered after the COPY.**

The key is that DELETE never touched either the link index (spanfilade) or the link orgls themselves [FC-LINK-DELETE-ISOLATION], [INV-SPANF-WRITE-ONLY]. The link endset entries mapping `[.0.1.1, .0.1.5]` → link ISAs were written when the links were created and persist unconditionally — the spanfilade is append-only.

The intermediate state after DELETE but before COPY: `find_links` on doc A would *not* find those links, because `find_links` converts a V-specset to I-addresses via the POOM before searching the spanfilade [INT-SPORGL-LINK-INDEX]. With the V→I mappings deleted from doc A's POOM, the conversion yields nothing — there are no V-positions in doc A that resolve to those I-addresses.

After COPY re-transcludes from doc B: `docopy` calls both `insertpm` (restores V→I mappings in doc A's POOM) and `insertspanf(..., DOCISPAN)` [ST-COPY], [ST-INSERT]. Doc A's POOM once again maps V-positions to `[.0.1.1, .0.1.5]`. Now `find_links` with a query covering those V-positions converts them to the I-addresses, intersects against the still-intact link index, and returns the links. Discovery is fully restored.

This follows from [FC-LINK-PERSISTENCE]: links exist independently of any document's POOM state. [INT-TRANSCLUSION-LINK-SEARCH] confirms: transclusion restores discoverability because it restores I-address presence in the POOM.

---

### Part 2: DOCISPAN Coexistence

**Yes — both DOCISPAN entries coexist.**

The spanfilade is strictly write-only [INV-SPANF-WRITE-ONLY]. DELETE calls only `deletend` on the POOM and never touches the spanfilade [ST-DELETE], [INT-DELETE-SPANF-DIVERGENCE]. The original DOCISPAN entry `[.0.1.1, .0.1.5]` → doc A survives as a stale reference.

When COPY re-transcludes from doc B, `insertspanf(..., DOCISPAN)` inserts a new entry via `insertnd` [SS-DOCISPAN]. There is no deduplication check — `isanextensionnd` checks contiguity, not existence [PRE-COPY]. The result: the spanfilade contains (at minimum) two entries:

- **Stale entry** (pre-DELETE): `[.0.1.1, .0.1.5]` → doc A
- **Fresh entry** (post-COPY): `[.0.1.1, .0.1.5]` → doc A

This is non-pathological. As [EC-STALE-SPANF-REFERENCE] documents, `find_documents` returns a *superset* of documents with live POOM mappings: `actual_docs(i) ⊆ find_documents(i)`. Duplicate entries may cause doc A to appear twice in raw results, but [INV-ITOV-FILTERING] handles the rest — I-to-V conversion at query time filters through the current POOM state, so only live V-positions are returned regardless of how many spanfilade entries point there.

---

### Summary

| Layer | After DELETE | After COPY from B |
|-------|-------------|-------------------|
| Doc A POOM | I-addresses removed | I-addresses restored (at new V-positions) |
| Spanfilade DOCISPAN | Stale entry persists | Stale + fresh entry coexist |
| Link index (LINKFROMSPAN etc.) | Unchanged | Unchanged |
| `find_links` on doc A | Not found (V→I fails) | **Rediscovered** (V→I restored) |

---

## Code Exploration

Now I have everything I need. Here is the complete, cited answer.

---

## Full Answer: DELETE + re-COPY, link rediscovery, and DOCISPAN coexistence

### Background: Two separate data structures

The backend maintains two independent persistent structures:

- **Permutation matrix** (`granf`, per-document orgl): the V→I address mapping. It is mutable — content can be inserted and deleted.
- **Spanfilade** (`spanf`): a global, write-only append index of which I-spans live in which documents, and which I-spans are link endpoints. Nothing is ever deleted from it.

---

### The DELETE path touches only the permutation matrix

`dodeletevspan` [do1.c:158–167]:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), deletevspanpm();

    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr));
}
```

`deletevspanpm` [orglinks.c:145–152]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` operates on `docorgl`, which is the document's permutation matrix node found via `granf`. The global `spanf` (spanfilade) is never referenced. There is no call to anything touching `spanf` anywhere in the delete chain. The spanfilade receives no write of any kind during a DELETE.

---

### The COPY path writes to BOTH structures

`docopy` [do1.c:45–65]:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
  ...
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && asserttreeisok(docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)    // line 60 — writes permutation matrix
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN) // line 62 — writes spanfilade
    && asserttreeisok(docorgl));
}
```

`insertspanf` [spanf1.c:15–54] appends a new leaf crum to the spanfilade:

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr,
                 typesporglset sporglset, INT spantype)
{
    prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]); // line 22 — key prefix
    ...
    movetumbler (isaptr, &linfo.homedoc);          // line 29 — stamps home document
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE); // line 51
}
```

`insertnd` appends a new leaf. **There is no counterpart `deletend` on the spanfilade anywhere in the codebase.** The spanfilade is write-only.

---

### Question 2: Do the stale and new DOCISPAN entries coexist?

**Yes, unconditionally.**

Timeline:
1. **Original COPY/INSERT of I-range `[.0.1.1, .0.1.5]` into doc A** → `insertspanf(..., DOCISPAN)` writes leaf crum L1 to spanfilade.
2. **DELETE of that range from doc A** → `deletend` on doc A's permutation matrix only. L1 remains in spanfilade, untouched.
3. **Re-COPY of same I-range from doc B into doc A** → `insertspanf(..., DOCISPAN)` writes a second leaf crum L2 to spanfilade.

Both L1 and L2 are now leaf crums in the enfilade tree rooted at `spanf`. The enfilade is never pruned. Both crums carry the same I-address range in their `SPANRANGE` dimension and doc A's ISA in their `ORGLRANGE` dimension (prefix) and `linfo.homedoc` field.

---

### Question 1: Does `find_links` rediscover links referencing that I-range?

**Yes, unconditionally.**

Link endpoints are stored in the spanfilade via `insertendsetsinspanf` [do2.c:116–128], called from `docreatelink` [do1.c:219]:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
                           typesporglset fromsporglset, typesporglset tosporglset,
                           typesporglset threesporglset)
{
    insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
    && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)
    [optional LINKTHREESPAN]
}
```

These `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN` crums are permanent spanfilade entries. DELETE never removes them.

The link search path is:

`dofindlinksfromtothree` [do1.c:348–353] → `findlinksfromtothreesp` [spanf1.c:56–103]:

```c
bool findlinksfromtothreesp(typetask *taskptr, typespanf spanfptr, ...)
{
    ...
    if (fromvspecset)
        sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN); // line 77
    if (tovspecset)
        sporglset2linkset (taskptr, (typecuc*)spanfptr, tosporglset, &tolinkset, orglrange, LINKTOSPAN);       // line 85
    ...
    intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr); // line 100
}
```

`sporglset2linkset` queries the spanfilade for crums whose `SPANRANGE` intersects the query I-addresses and whose `ORGLRANGE` prefix matches the appropriate span type (`LINKFROMSPAN`, etc.). Since those crums were never deleted, they are found. Document A's permutation matrix state is irrelevant to this search.

---

### The home-document filter is structurally disabled in spanfilade queries

`crumqualifies2d` [retrie.c:270–280] has a filter for home document:

```c
if ((crumptr->height == 0) && infoptr &&
    !tumblereq (&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc))) {
    return (FALSE);
}
```

But `findcbcinarea2d` [retrie.c:229–251] treats a non-NULL `infoptr` as a fatal error:

```c
if(infoptr){
    fprintf(stderr,"not NULL infoptr ... shouldent happen...\n");
    gerror("findcbcinarea2d");
}
```

And all spanfilade calls pass `(typeisa*)NULL` as the `docisaptr` parameter — see for example `finddocscontainingsp` [spanf1.c:171]:

```c
context = retrieverestricted((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);
```

Which propagates through `retrieverestricted` [retrie.c:77–82]:

```c
if (docisaptr) {
    movetumbler(docisaptr, &info.homedoc);
    infoptr = &info;
} else {
    infoptr = NULL;  // always taken for spanfilade queries
}
```

So `infoptr` is always `NULL` in spanfilade traversals, the home-document guard in `crumqualifies2d` never fires, and **both the stale L1 and the new L2 DOCISPAN crums — and all link endpoint crums — are returned by any I-address range query regardless of which document they nominally belong to.**

---

### Summary

| Operation | Permutation matrix (`granf/docorgl`) | Spanfilade (`spanf`) |
|-----------|--------------------------------------|----------------------|
| Original COPY/INSERT of `[.0.1.1, .0.1.5]` into doc A | Written (V→I mapping) | DOCISPAN crum L1 written permanently |
| DELETE of that range from doc A | `deletend` removes V→I entries | **Untouched** |
| Re-COPY of same I-range from doc B into doc A | Written again (new V→I mapping) | DOCISPAN crum L2 written permanently |
| `find_links` query on `[.0.1.1, .0.1.5]` | Not consulted | Finds all `LINKFROMSPAN`/`LINKTOSPAN` crums (permanent); rediscovers all links |

**Both DOCISPAN entries (L1 stale, L2 new) coexist permanently** in the spanfilade enfilade tree with no mechanism to distinguish or evict the stale one. **`find_links` fully rediscovers any link** whose endpoint I-addresses overlap `[.0.1.1, .0.1.5]`, because link records are written once to the spanfilade and never deleted, and the spanfilade search ignores document permutation matrix state entirely.
