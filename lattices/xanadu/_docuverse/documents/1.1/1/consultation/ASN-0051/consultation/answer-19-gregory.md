## Question 19 [gregory]

> Does the spanfilade entry for a link's endset record the document ID where the link was created, and if the link's home document is itself deleted from the POOM (all content removed), do the spanfilade endset entries for that link remain fully intact — meaning the link is discoverable from any other document sharing those I-addresses regardless of the creating document's state?

## KB Synthesis

## Spanfilade Endset Entries and Home Document Deletion

**What the spanfilade endset entries record:**

The spanfilade endset entries record the `sporgladdress` field from each sporgl — this is the ISA of the document *containing the endpoint content* at link creation time, not necessarily the home document [SS-SPORGL]. As [INT-SPORGL-LINK-INDEX] confirms, the provenance field is stored so link retrieval can reconstruct which document each endpoint references. The home document determines where the link orgl's *address is allocated* [SS-LINK-HOME-DOCUMENT], which is a separate concern from where the endpoint content lives.

**On spanfilade survival when the home document loses all content:**

Yes — the spanfilade endset entries remain fully intact. Three independent lines of evidence:

1. **The spanfilade is write-only.** No delete function exists anywhere in `spanf1.c` or `spanf2.c` [INV-SPANF-WRITE-ONLY]. No operation can remove a spanfilade entry once created.

2. **DELETE operates only on the POOM layer.** `deletevspanpm` calls only `deletend` (granf/POOM) and `logbertmodified` — there is no call to any spanf removal function [FC-LINK-DELETE-ISOLATION], [ST-DELETE]. The spanfilade frame condition for DELETE is explicit: `delete(D, vspan) ⟹ spanf_entries_after = spanf_entries_before` [ST-DELETE Finding 0057].

3. **This specific scenario is directly confirmed.** [FC-LINK-PERSISTENCE] Finding 0024 explicitly tests and verifies: "Deleting all text from the home document has zero effect on link functionality — the link's source, target, and type endsets remain fully operational." The three-layer model [SS-THREE-LAYER-MODEL] formalizes this: `DELETEVSPAN` only removes POOM entries; I-space and spanfilade are structurally independent.

**Discoverability from other documents:**

Link discovery is purely content-identity-based — `find_links` converts V-spans to I-addresses then searches the spanfilade [SS-FIND-LINKS]. Since the spanfilade entries are intact, any document sharing the endpoint I-addresses (via transclusion or versioning) will discover the link regardless of the home document's POOM state [INV-LINK-GLOBAL-VISIBILITY], [INT-LINK-TRANSCLUSION].

**One caveat:** If the endpoint content itself was also removed from *all* documents (not just the home document), FOLLOWLINK would return empty results at the I-to-V conversion step [INV-ITOV-FILTERING], [EC-GHOST-LINK] — but the link remains discoverable from documents still holding those I-addresses. The home document's state is orthogonal to this.

---

## Code Exploration

I now have everything I need. Let me compile the full answer.

---

## Full Answer

### 1. What Does the Spanfilade Entry for a Link's Endset Actually Record?

**The entry records the link's own ISA — not the creating document's ISA.**

Trace from `docreatelink` [`do1.c:195`]:

```c
// do1.c:207-219
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)   // allocate link's ISA
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)         // plant link in creating doc's POOM
  && ...
  && specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
  && specset2sporglset (taskptr, tospecset, &tosporglset, NOBERTREQUIRED)
  && specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
  && setlinkvsas (&fromvsa, &tovsa, &threevsa)
  && insertendsetsinorgl (...)
  && insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
);
```

`insertendsetsinspanf` [`do2.c:116`] calls `insertspanf` with `linkisaptr` three times:

```c
// do2.c:116-128
bool insertendsetsinspanf(..., typeisa *linkisaptr, ...)
{
  insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // LINKFROMSPAN = 1
  insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)     // LINKTOSPAN   = 2
  insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN) // LINKTHREESPAN= 3
}
```

Inside `insertspanf` [`spanf1.c:15`], the `isaptr` argument is `linkisaptr`:

```c
// spanf1.c:22-51
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // ORGLRANGE key = prefix(linkISA, FROM|TO|THREE)
tumblerclear (&crumwidth.dsas[ORGLRANGE]);
...
for (; sporglset; ...) {
    if (itemid == SPORGLID) {
        movetumbler (&sporgl->sporglorigin,  &lstream);        // SPANRANGE = I-address of endset
        movetumbler (&sporgl->sporglwidth,   &lwidth);
        movetumbler (&sporgl->sporgladdress, &linfo.homedoc);  // homedoc = doc that holds that V-span
    }
    ...
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
```

Each spanfilade crum for a link's endset stores:

| Field | Value | Source |
|-------|-------|--------|
| `ORGLRANGE` | `prefixtumbler(linkISA, 1|2|3)` | link's own ISA, prefixed by endset slot |
| `SPANRANGE` | I-address + width of endset content | from `sporglorigin`/`sporglwidth` |
| `linfo.homedoc` | ISA of the doc whose V-span maps to that I-address | from `sporgladdress` set by `vspanset2sporglset` [`sporgl.c:53`] |

`prefixtumbler` [`tumble.c:641`] prepends `bint` (1/2/3) as the leading digit of the link's ISA tumbler; this makes the ORGLRANGE key `<FROM|TO|THREE>.<link-account>.<link-doc>.<link-atom>`.

**The creating document's ISA does not appear in ORGLRANGE.** The `homedoc` crum field stores the ISA of whichever document's POOM maps the referenced V-address — which may or may not be the creating document, depending on where the link's endsets point.

---

### 2. What Happens When the Creating Document's Content Is Deleted?

`dodeletevspan` [`do1.c:158`]:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

`deletevspanpm` [`orglinks.c:145`]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);  // operates on docorgl only
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` [`edit.c:31`] receives `(typecuc*)docorgl` as its first argument — the POOM node for that document. It performs all operations (cuts, disown, subtreefree, tumblersub) on that tree only. **`spanf` (the spanfilade) is never passed to `deletend` and is never modified by any code in the deletion chain.**

There is no call to `insertspanf`, no call to any spanfilade-writing function, anywhere in the path from `deletevspan` → `dodeletevspan` → `deletevspanpm` → `deletend`.

---

### 3. Link Discovery Is Blind to the Creating Document's State

When another document queries for links touching its I-addresses, `findlinksfromtothreesp` [`spanf1.c:56`] → `sporglset2linkset` [`sporgl.c:222`] → `sporglset2linksetinrange` [`sporgl.c:239`]:

```c
// sporgl.c:250-265
for (; sporglset; ...) {
    if (FALSE /*trying to kluge links followable thru versions*/
        && itemid == SPORGLID) {
        infoptr = &linfo;
        movetumbler(&sporgl->sporgladdress, &linfo.homedoc);
    } else
        infoptr = NULL;  // ← always reached due to `FALSE ||`

    context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE,
                                 (typeisa*)infoptr);   // infoptr == NULL → no homedoc filter
    for (c = context; c; c = c->nextcontext) {
        beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);  // strip prefix → extract link ISA
        onlinklist(taskptr, linksetptr, &linksa);
    }
}
```

The `if (FALSE || ...)` guard forces `infoptr = NULL` unconditionally — the `homedoc` field stored in each spanfilade crum is **never used as a filter** during link retrieval. Discovery is keyed purely on:
1. **SPANRANGE**: the I-address of the queried content
2. **ORGLRANGE**: the endset-type prefix range (`LINKFROMSPAN`=1, `LINKTOSPAN`=2, `LINKTHREESPAN`=3)

The link's ISA is then recovered by stripping the prefix off the ORGLRANGE value with `beheadtumbler`.

---

### Summary

**Part 1:** The spanfilade endset entry records the **link's own ISA** in ORGLRANGE (prefixed by endset slot number). The `homedoc` field records the ISA of the document whose V-space maps the referenced I-address — not the creating document's ISA per se (though they coincide when the endset points into the creating document). The creating document is **not** the keying identity in the spanfilade record.

**Part 2:** Yes — the spanfilade endset entries remain **fully intact** if the creating document's POOM content is deleted. `deletevspan` → `deletend` operates exclusively on `docorgl` (the document's enfilade subtree); `spanf` is never touched. Link discovery via `sporglset2linksetinrange` searches by I-address alone, with `homedoc` filtering disabled (`FALSE ||` at `sporgl.c:251`). Any document sharing those I-addresses will continue to find the link through the spanfilade, with no dependency on the creating document's POOM state.
