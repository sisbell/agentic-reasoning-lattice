## Question 17 [evidence]

> After DELETEVSPAN removes a link's V→I entry from its home document's link subspace (reverse-orphaned link), does that link still contribute to a count whose home-set bounds that document, since its endsets persist in the spanfilade?

## KB Synthesis

Yes, the reverse-orphaned link still contributes and remains discoverable. Here is why, synthesized across the relevant layers.

## What DELETEVSPAN actually touches

DELETEVSPAN targets only the POOM layer [SS-THREE-LAYER-MODEL]. It calls `deletevspanpm` → `deletend` on the document's orgl enfilade, removing the V-position 2.x → link ISA mapping. It makes no call to any spanfilade function [ST-DELETE, Finding 0057]. The other two layers are untouched:

- **I-space**: the link orgl at its allocated ISA (e.g., `1.1.0.1.0.1.0.2.1`) is permanent [INV-LINK-PERMANENCE].
- **Spanfilade**: both the link endpoint entries (endpoint I-addresses → link ISA) and the DOCISPAN entries remain, because the spanfilade is strictly append-only with no delete mechanism [INV-SPANF-WRITE-ONLY].

This is the "reverse orphan" state documented in [EC-REVERSE-ORPHAN]: the link exists in I-space and the spanfilade, but has no POOM entry.

## The home-set (orgl-dimension) filter

The orgl-dimension of the spanfilade search was designed to restrict results to links whose ISAs fall within a specified orgl range. Whether intended semantics or actual behavior is considered, the reverse-orphaned link still satisfies this filter:

**Intended semantics**: The link's ISA was allocated under the home document's address via `createorglingranf` and `findisatoinsertnonmolecule` [SS-ADDRESS-ALLOC, SS-LINK-HOME-DOCUMENT]. The ISA (e.g., `1.1.0.1.0.1.0.2.1`) is permanently a child of the home document address (`1.1.0.1.0.1`) in the address hierarchy [SS-TUMBLER-CONTAINMENT]. DELETEVSPAN does not reallocate or move this address — the granfilade is append-only [FC-GRANF-ON-DELETE, INV-MONOTONIC]. A home-set filter bounded to that document would still encompass the link's ISA.

**Actual implementation**: The orgl-dimension filter is non-functional. `sporglset2linkset()` contains a `TRUE||!homeset` guard that always fires, replacing the caller-supplied orgl range with a hardcoded unbounded range [EC-FIND-LINKS-GLOBAL, PRE-FIND-LINKS Finding 0069]. All `find_links` calls are effectively global in the orgl dimension, so the reverse-orphaned link is returned as long as the span-dimension (content I-address) match succeeds.

## The span-dimension condition

For `find_links` to return the link, the query specset's I-addresses must intersect the link's endpoint I-addresses [SS-FIND-LINKS]. The link's endpoints reference the content the link was created on — those I-addresses live in the spanfilade permanently [INV-SPANF-WRITE-ONLY] and are unaffected by removing the link's own POOM entry. The link remains discoverable from any document sharing content identity with its endpoints [EC-REVERSE-ORPHAN]:

> `find_links(source_specs) → still finds the link (spanfilade intact)`

## Summary

After DELETEVSPAN reverse-orphans a link:

1. Its ISA is still under the home document's address (permanent, immutable) [INV-MONOTONIC, INV-NO-IADDR-REUSE].
2. Its spanfilade entries are still present (append-only, no delete) [INV-SPANF-WRITE-ONLY].
3. Under intended semantics, an orgl filter bounded to the home document still includes the link's ISA.
4. In the actual implementation, the orgl filter is disabled [EC-FIND-LINKS-GLOBAL], making the question of home-set bounds moot — the link is globally discoverable regardless.

The link contributes to any count or result set from that document's home-set, both in the design and the implementation.

---

## Code Exploration

I now have the complete picture. Here is my full answer.

---

## Does a reverse-orphaned link still contribute to a count bounded by its home document?

**Answer: Yes — unconditionally and permanently.** There are three independent reasons, each sufficient on its own. I trace each through the source.

---

### 1. DELETEVSPAN only removes the POOM entry; the spanfilade is never touched

`dodeletevspan` (`do1.c:158–167`) does exactly two things:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  ...
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    /*&& TRUE*/ /* ht stuff */ );
}
```

It finds the document's POOM root in the granfilade, then calls `deletevspanpm`. That function (`orglinks.c:145–152`) calls `deletend` on `docorgl`:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` (`edit.c:31–76`) cuts nodes out of the crum tree for the V dimension of the document's POOM. **There is no corresponding operation on `spanf` (the spanfilade).** The comment `/*&& TRUE*/ /* ht stuff */` confirms the ht (hypertextual) layer was never wired up.

Contrast with `docreatelink` (`do1.c:195–220`), which writes to **both** structures:

```c
&& docopy (taskptr, docisaptr, &linkvsa, ispanset)           // → POOM (granfilade)
&& insertendsetsinorgl (...)                                 // → link's own POOM
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, ...)    // → spanfilade
```

Only the first of these is undone by DELETEVSPAN. The spanfilade insertion is permanent.

---

### 2. Link counting reads from the spanfilade, not the POOM

`findnumoflinksfromtothreesp` (`spanf1.c:105–115`) counts by calling `findlinksfromtothreesp` and counting the returned list:

```c
bool findnumoflinksfromtothreesp(..., INT *numptr)
{
  typelinkset linkset;
  INT n;

    if (!findlinksfromtothreesp (taskptr, spanfptr, fromvspecset, tovspecset,
                                  threevspecset, orglrange, &linkset))
        return(FALSE);
    for (n = 0; linkset; linkset = linkset->next, ++n);
    *numptr = n;
    return (TRUE);
}
```

`findlinksfromtothreesp` (`spanf1.c:56–103`) converts the query's V-specs to sporgls (I-spans) via `specset2sporglset`, then calls `sporglset2linkset`. That in turn calls `sporglset2linksetinrange` (`sporgl.c:239–269`), which searches the spanfilade:

```c
context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE,
                               &range, ORGLRANGE, (typeisa*)infoptr);
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE],&linksa);
    onlinklist (taskptr, linksetptr, &linksa);
}
```

The spanfilade node for each link endset was inserted by `insertendsetsinspanf` → `insertspanf` (`spanf1.c:15–54`) at creation time:

```c
// spantype = LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);   // key: spantype.link-isa
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);              // key: endset I-span
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

Since DELETEVSPAN never touches the spanfilade, these nodes remain. The counter finds them.

---

### 3. The home-set bound is hard-wired to be ignored

`sporglset2linkset` (`sporgl.c:222–237`) receives the home-set and immediately discards it:

```c
int sporglset2linkset(typetask *taskptr, typecuc *spanfptr, typesporglset sporglset,
                      typelinkset *linksetptr, typeispan *homeset, INT spantype)
{
  typeispan nullhomeset;

    *linksetptr = NULL;
    if (TRUE||!homeset) {          // <— always true; homeset is never used
        tumblerclear (&nullhomeset.stream);
        tumblerclear (&nullhomeset.width);
        nullhomeset.width.mantissa[0] = 100;
        nullhomeset.next = NULL;
        homeset = &nullhomeset;
    }
    for (; homeset; homeset = homeset->next) {
        sporglset2linksetinrange (taskptr, spanfptr, sporglset, linksetptr, homeset, spantype);
    }
}
```

`if (TRUE||!homeset)` short-circuits unconditionally. The `homeset` parameter — whatever I-span the caller passes — is replaced with `{stream=0, width=100}`. Every call to `sporglset2linksetinrange` thus uses an ORGLRANGE of `[spantype.0, +100]`, covering the entire link ISA number space. No home-document bound is ever applied.

This affects both public interfaces: `fns.c:198` explicitly passes `(typeispan*)NULL/*homeset*/` for `FINDLINKSFROMTOTHREE`, and `fns.c:213` passes the received homeset for `FINDNUMOFLINKSFROMTOTHREE` — but `if (TRUE||!homeset)` discards it either way.

---

### 4. Even if the guard were removed, the ISA is still inside the document's I-span

Suppose the `TRUE||` guard were patched out. Would the reverse-orphaned link then be excluded?

Still no. The ORGLRANGE key stored for each endset is:

```
prefixtumbler(linkisaptr, spantype, &crumorigin.dsas[ORGLRANGE])
```

which yields `spantype.link-isa` (e.g., `1.account.doc.link-N`). `prefixtumbler` (`tumble.c:641–651`) prepends `spantype` as a leading tumbler digit.

The home-set search range is built in `sporglset2linksetinrange` (`sporgl.c:256–259`):

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);
prefixtumbler(&orglrange->width,  0,        &range.width);
context = retrieverestricted (spanfptr, ..., &range, ORGLRANGE, ...);
```

This restricts the ORGLRANGE search to `[spantype.doc-ispan-start, + doc-ispan-width]`.

The link ISA is allocated by `createorglingranf` (`do1.c:209`) using:

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
createorglingranf (taskptr, granf, &hint, linkisaptr);
```

The hint parents the link under the home document, so the link's permascroll address is permanently allocated within the document's I-span range. Therefore `spantype.link-isa` lies within `[spantype.doc-ispan-start, spantype.doc-ispan-start + doc-ispan-width]`. Deleting the POOM entry does nothing to this geometric fact — the ISA is immutable once allocated.

---

### Summary

| What DELETEVSPAN removes | What it does NOT touch |
|---|---|
| V→I mapping in home document's POOM (`deletend` on `docorgl`, V-dim) | Spanfilade endset entries (`LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN`) |
| | Link's own POOM (its FROM/TO/THREE V→I maps) |

After the V→I entry is deleted, every link-finding and link-counting call goes through `findlinksfromtothreesp` → `sporglset2linksetinrange` → `retrieverestricted` on the spanfilade. The link's endset nodes are still there. The home-set parameter is ignored by `if (TRUE||!homeset)` at `sporgl.c:227`. Even if that guard were fixed, the link ISA falls within the home document's I-span by construction. The link is counted.
