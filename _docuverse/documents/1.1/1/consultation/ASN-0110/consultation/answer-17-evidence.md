## Question 17 [evidence]

> Does the operation discover endsets anchored through transclusion — endsets whose I-addresses this document shares with another document — when the region is phrased in this document's V-space?

## KB Synthesis

Yes. The discovery mechanism is purely I-address-based, so transclusion-shared I-addresses are fully visible to it.

**The mechanism** [SS-RETRIEVE-ENDSETS, Finding 0035]:

1. The input V-region is converted to I-addresses via the querying document's POOM (`specset2sporglset` → V-to-I).
2. The spanfilade is searched with those I-addresses as the SPANRANGE restriction.
3. Results are converted back to V-positions using the querying document's docid.

Because transclusion copies I-addresses rather than allocating new ones [ST-VCOPY], step 1 produces the same I-addresses that were indexed in the spanfilade when the link was created. The spanfilade has no knowledge of which document is querying — it is keyed purely on I-address.

**Direct confirmation** [INT-LINK-TRANSCLUSION, Finding 0028]:

> `vcopy(content, src_doc, dst_doc) => (forall L :: I-addresses(L.source) ∩ I-addresses(content) ≠ ∅ => findable(L, dst_doc))`

This is explicitly validated for RETRIEVEENDSETS in [SS-RETRIEVE-ENDSETS]: "Key: endsets are resolved in terms of the querying document's V-space, not the link's home document."

**One caveat** [INV-ITOV-FILTERING]: The I-to-V conversion at step 3 silently drops I-addresses that have no current mapping in the querying document's POOM. If the transcluded content was subsequently deleted from this document, the endset resolution returns empty for this document's perspective — even though the link still exists and is discoverable from other documents that retain the I-addresses [EC-GHOST-LINK].

---

## Code Exploration

I now have everything I need to trace the complete execution path. Let me compile the full answer.

---

## Answer

**Yes — the operation discovers endsets anchored through transclusion.** When a region is phrased in a document's V-space, the system translates it to I-space through that document's permutation matrix, then searches the spanfilade by I-address with no document-identity filter. Any link whose endset touches that I-space region is returned, regardless of which document originally anchored the endset.

Here is the complete traced path with every claim cited to source.

---

## Execution Path: `findlinksfromtothree`

### Stage 1 — FEBE entry (`fns.c:189-202`)

```c
void findlinksfromtothree(typetask *taskptr)
{
    getfindlinksfromtothree(taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset);
    dofindlinksfromtothree(taskptr, fromvspecset, tovspecset, threevspecset,
                           (typeispan*)NULL/*homeset*/, &linkset);   // fns.c:198
    putfindlinksfromtothree(taskptr, linkset);
}
```

The `homeset` parameter — which could restrict results by document — is **explicitly nulled** with the comment `/*homeset*/` at `fns.c:198`. This is not an accident; it expresses a deliberate choice to remove the document filter from the call.

---

### Stage 2 — Dispatch through `do1.c`

`do1.c:348-353`:
```c
bool dofindlinksfromtothree(...) {
    return findlinksfromtothreesp(taskptr, spanf, fromvspecset, ...);
}
```

No transformation here; passes the V-specsets directly to the spanfilade layer.

---

### Stage 3 — V-space → I-space via the named document's PM

`spanf1.c:70-75`:
```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
```

`specset2sporglset` is in `sporgl.c:14-33`. For each item in the specset:

- If `ISPANID`: used directly as I-space.
- If `VSPECID`: delegates to `vspanset2sporglset`.

`sporgl.c:35-65` — `vspanset2sporglset`:
```c
findorgl(taskptr, granf, docisa, &orgl, type);           // line 44 — opens named document's orgl
for (; vspanset; vspanset = vspanset->next) {
    vspanset2ispanset(taskptr, orgl, vspanset, &ispanset); // line 48 — V→I through this doc's PM
    for (; ispanset; ispanset = ispanset->next) {
        sporglset = taskalloc(taskptr, sizeof(typesporgl));
        sporglset->itemid = SPORGLID;
        movetumbler(docisa, &sporglset->sporgladdress);     // line 53 — records querying doc ISA
        movetumbler(&ispanset->stream, &sporglset->sporglorigin); // line 54 — I-space origin
        movetumbler(&ispanset->width,  &sporglset->sporglwidth);  // line 55 — I-space width
    }
}
```

The V→I translation uses **the named document's permutation matrix** (`orglinks.c:397-401`):
```c
typeispanset *vspanset2ispanset(..., typeorgl orgl, typevspanset vspanptr, ...) {
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` at `orglinks.c:404-422` iterates over each V-span and calls `span2spanset`, which calls `retrieverestricted((typecuc*)orgl, ...)` — an enfilade search **within the named document's own permutation matrix** — to produce the corresponding I-spans.

After this stage, the query is expressed purely in I-space: `sporglorigin`/`sporglwidth` are permascroll addresses.

---

### Stage 4 — Spanfilade lookup: no document filter applied

`spanf1.c:76-82`:
```c
sporglset2linkset(taskptr, spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
```

`orglrange` is `NULL` (passed from `fns.c:198` as `(typeispan*)NULL`), so no link-document restriction is applied.

`sporgl.c:239-269` — `sporglset2linksetinrange`:
```c
for (; sporglset; ...) {
    if (FALSE/*trying to kluge links followable thru versions */
        && ((typeitemheader*)sporglset)->itemid == SPORGLID) {
        infoptr = &linfo;
        movetumbler(&sporglset->sporgladdress, &linfo.homedoc);
    } else
        infoptr = NULL;                              // line 255 — always NULL; filter disabled

    context = retrieverestricted(spanfptr,
                                 (typespan*)sporglset,  // I-space address as restriction
                                 SPANRANGE,
                                 (typespan*)NULL,       // no ORGLRANGE restriction (orglrange==NULL path)
                                 ORGLRANGE,
                                 (typeisa*)infoptr);    // NULL — no homedoc filter
    for (c = context; c; c = c->nextcontext) {
        beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa); // extract link ISA
        onlinklist(taskptr, linksetptr, &linksa);
    }
}
```

The condition `FALSE && ...` is hardcoded false at `sporgl.c:251` — the comment *"trying to kluge links followable thru versions"* shows this was an experiment that was disabled. As a result:

- `infoptr` is always `NULL` (`sporgl.c:255`)
- `retrieverestricted` is called with no document filter
- The spanfilade lookup is **purely by I-space address** (SPANRANGE dimension)

The spanfilade (`spanf`) was populated at link-creation time by `insertspanf` (`spanf1.c:15-54`), which indexed each endset by its I-space position (SPANRANGE) and the link's ISA (ORGLRANGE). Because the index key is I-address alone, **every link whose endset touches the queried I-space range is returned**, regardless of which document originally anchored the endset.

---

## The Transclusion Case

When document **A** and document **B** both transclude the same permascroll content at I-space address **[i₁, i₂]**:

- A link created with an endset in document A's V-space (which maps to [i₁, i₂]) was stored in the spanfilade at SPANRANGE = [i₁, i₂].
- Querying "find links whose from-endset overlaps V-region R in document B", where R maps through B's PM to [i₁, i₂]:
  1. `vspanset2sporglset` opens B's orgl → translates R → [i₁, i₂]. `sporgl.c:44,48`
  2. `sporglset2linksetinrange` queries the spanfilade at SPANRANGE = [i₁, i₂] with no document filter. `sporgl.c:255,259`
  3. The spanfilade returns the link anchored in A — **found via transclusion**.

---

## What Is Not Cross-Document: Endset Back-Projection

When the found link's endsets are subsequently retrieved (e.g., via `followlink` or `retrieveendsets`), the I-space endsets are projected back to V-space. This uses the **home document stored with the endset**, not the querying document.

`sporgl.c:205-220` — `contextintosporgl`:
```c
movetumbler(&context->context2dinfo.homedoc, &sporglptr->sporgladdress);
```

The `homedoc` in the returned sporgl is the document that originally anchored the endset (document A in the transclusion example). `linksporglset2vspec` (`sporgl.c:134`) then back-projects to V-space using A's orgl:
```c
movetumbler(homedoc, &specptr->docisa);   // endset returned in A's coordinate system
sporglset2vspanset(taskptr, homedoc, ...); // I→V through A's PM
```

So the **link is found** through transclusion, but its **endsets are returned in the original document's V-space**, not the querying document's. The caller receives a VSPECID whose `docisa` names the document through which the endset was originally anchored.

---

## Summary

| Step | Mechanism | Document scope |
|------|-----------|----------------|
| V→I translation | Named doc's PM (`orglinks.c:397`) | Document-specific |
| Spanfilade lookup | By I-address (SPANRANGE), `infoptr=NULL` (`sporgl.c:255`) | **Document-agnostic** |
| Link discovery | All links whose endsets touch that I-space | Cross-document (incl. transclusion) |
| Endset back-projection | Through original home-doc's PM (`sporgl.c:134,152`) | Returns coords in original doc |

The answer is yes. The spanfilade lookup at `sporgl.c:259` has no document filter — `infoptr` is always `NULL` because the version-filtering branch at `sporgl.c:251` is hardcoded to `FALSE`. This is the mechanism by which transclusion-shared endsets surface: the I-space is the universal address space shared across all documents, and the spanfilade is indexed on I-space alone.
