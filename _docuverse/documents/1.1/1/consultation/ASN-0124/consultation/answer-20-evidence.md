## Question 20 [evidence]

> Does CREATENEWVERSION's copying of SPAN metadata create DOCISPAN entries for the new version document, so that querying the original's text immediately returns every version sharing those I-addresses — and conversely, does FINDDOCSCONTAINING require the returned documents (or the queried document) to be open under a BERT, or does the spanfilade search bypass `findorgl` entirely?

## KB Synthesis

## CREATENEWVERSION and FINDDOCSCONTAINING: Two-Part Answer

### Part 1: Does CREATENEWVERSION create DOCISPAN entries for the new version?

Yes. The call chain documented in [ST-VERSION] is:

> `docreatenewversion` → `createorglingranf` (allocates doc address) → `doretrievedocvspanfoo` (gets source's text V-span) → `docopyinternal` → `specset2ispanset` → `insertpm` (updates POOM) → **`insertspanf`** (records SPAN entries)

`docopyinternal` (`do1.c:66-82`) calls `insertspanf` with the new version's ISA as `docisaptr` and the shared text I-addresses as the `ispanset`. This is the same `insertspanf(..., DOCISPAN)` call made by regular `docopy()` [ST-INSERT, Finding 0036]. The new version's address is thereby registered in the DOCISPAN sub-index against every text I-address it shares with the source.

Consequence: immediately after `CREATENEWVERSION(d)` produces `d'`, `FINDDOCSCONTAINING` for any text I-address in `d` returns `{d, d', …}`. [INV-IADDRESS-PERMANENT] then guarantees that entry persists regardless of subsequent edits to either document.

[ST-VERSION] also explicitly confirms no new content I-addresses are allocated — the `insertspanf` call only registers existing I-addresses under the new docISA, no `findisatoinsertgr` for content occurs.

---

### Part 2: Does FINDDOCSCONTAINING require open documents or a BERT?

Neither. The spanfilade search bypasses `findorgl` entirely.

The open-document/BERT gate lives in the **content retrieval** path: `doretrievev` → `specset2ispanset` → `findorgl` [PRE-RETRIEVE-CONTENTS, Finding 0027]. `findorgl` checks the BERT table and the open-document list before returning a document orgl for V→I resolution.

The DOCISPAN query path (`finddocscontainingsp`) is a pure spanfilade index lookup. As [SS-DOCUMENT-LIFECYCLE] states:

> "Operations that work through I-address lookup (e.g., `find_links` via span-f) do not require the referenced document to be open."

And [FC-CONTENT-SPANF-ISOLATION] / Finding 0012 confirms the structural separation: `spanf1.c` and `spanf2.c` contain no granf references, and the `dofindlinksfromtothree` path (`do1.c:386-391`) delegates "entirely to `findlinksfromtothreesp()`" with no `findorgl` call.

The practical consequence — documented in [INT-LINK-FOLLOW-LIFECYCLE] — is a three-phase pipeline:

| Phase | Operation | Open doc required? |
|-------|-----------|-------------------|
| Discovery | `FINDDOCSCONTAINING` / `find_links` (spanf) | No |
| Follow | `follow_link` (reads link orgl directly) | No |
| Resolve | `retrieve_contents` (V→I resolution via `findorgl`) | **Yes** |

So `FINDDOCSCONTAINING` returns document ISAs freely without consulting the BERT table or the open list. Only the downstream `RETRIEVEV` call — which resolves V-positions within a returned document — requires that document to be opened first.

---

## Code Exploration

I now have a complete picture. Here is the full analysis.

---

## Answer

### Question 1: Does CREATENEWVERSION create DOCISPAN entries for the new version?

**Yes — explicitly and unconditionally.**

#### Call chain

`fns.c:289-300`: `createnewversion` calls `docreatenewversion(taskptr, &originaldocisa, &originaldocisa, &newdocisa)` — `wheretoputit` is the same as the original ISA.

`do1.c:260-299`: `docreatenewversion` does the following in sequence:

1. **Line 277** — allocates a new orgl:
   ```c
   if (!createorglingranf(taskptr, granf, &hint, newisaptr)) return (FALSE);
   ```

2. **Lines 281-283** — retrieves the original document's full V-extent with **`NOBERTREQUIRED`**:
   ```c
   if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) return FALSE;
   ```
   `doretrievedocvspanfoo` [do1.c:301-309] calls `findorgl` with `NOBERTREQUIRED`, then `retrievedocumentpartofvspanpm` [orglinks.c:155-162], which reads the root crum directly:
   ```c
   movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
   movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
   ```
   Result: `vspan` = the root-crum V-extent of the original document (all content, from stream to stream+width).

3. **Lines 285-289** — builds a `vspec` pointing at the **original** document with its full V-span:
   ```c
   vspec.docisa = *isaptr;        /* original doc's ISA */
   vspec.vspanset = &vspan;       /* original's full V-span */
   ```

4. **Line 292** — directly adds the new document to the BERT table without going through `doopen`:
   ```c
   addtoopen(newisaptr, user, TRUE, WRITEBERT);
   ```
   (`created=TRUE`, `modified=FALSE` — so if the operation is later abandoned, `removefromopen` [bert.c:173-174] will delete the version via `deleteversion`.)

5. **Line 293** — calls `docopyinternal`:
   ```c
   docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
   ```

#### Inside `docopyinternal` [do1.c:66-82]

`docisaptr` = `newisaptr` throughout; `specset` = the original-doc vspec.

**Line 74** — V → I translation, `NOBERTREQUIRED`:
```c
if (!specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)) return FALSE;
```
`specset2ispanset` [do2.c:14-46] finds `vspec.itemid == VSPECID`, calls:
```c
findorgl (taskptr, granf, &vspec.docisa, &docorgl, NOBERTREQUIRED)
```
…then `vspanset2ispanset` [orglinks.c:397-402]:
```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```
`permute` [orglinks.c:404-422] → `span2spanset` → `retrieverestricted` on the **original** doc's POOM, translating V-addresses to I-addresses. Result: `ispanset` = every I-span (permascroll region) referenced by the original document.

**Line 79** — the critical insertion:
```c
if (!insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)) return FALSE;
```

`insertspanf` [spanf1.c:15-54] with `isaptr = newisaptr` and `spantype = DOCISPAN`:
```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
/* ... for each I-span: */
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);
movetumbler (isaptr, &linfo.homedoc);
insertnd(taskptr, (typecuc*)spanf, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

The ORGL-dimension key is `prefixtumbler(newisaptr, DOCISPAN, ...)`. The SPAN-dimension key is the I-span address. The `homedoc` stored in the crum is `newisaptr`.

**These are exactly the same I-spans that the original document had DOCISPAN entries for** — both documents now have entries in the spanfilade mapping to the same permascroll regions.

#### Consequence

After `CREATENEWVERSION`, the spanfilade contains two sets of DOCISPAN crums covering the same I-span addresses: one keyed by the original's ISA, one keyed by the new version's ISA. A `FINDDOCSCONTAINING` query against any of those I-spans will traverse the spanfilade and surface both documents from their respective DOCISPAN crum entries — without any further open/BERT check on either.

---

### Question 2: Does FINDDOCSCONTAINING require BERT for the queried or returned documents?

**No — neither the queried document nor the returned documents require a BERT. The spanfilade search completely bypasses `findorgl`.**

#### Entry point

`fns.c:20-32`: `finddocscontaining` → `dofinddocscontaining`.

`do1.c:15-23`:
```c
bool dofinddocscontaining(typetask *taskptr, typespecset specset, typelinkset *addresssetptr)
{
  typeispanset ispanset;
  bool specset2ispanset(), finddocscontainingsp();

	return (
	   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
	&& finddocscontainingsp (taskptr, ispanset, addresssetptr));
}
```

**`NOBERTREQUIRED` is passed for the input.** If the caller supplies a V-spec (V-address inside some document), `specset2ispanset` [do2.c:35] calls `findorgl` with `NOBERTREQUIRED`:
```c
findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
```
And `checkforopen` [bert.c:59-61] short-circuits immediately:
```c
if (type == NOBERTREQUIRED) {
    return 1;	/* Random > 0 */
}
```
No BERT open is required for the queried document.

#### The spanfilade search — no `findorgl` at all

`spanf1.c:151-188`: `finddocscontainingsp`:

```c
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
        context = retrieverestricted (
            (typecuc*)spanf, 
            &docspace,   /* ORGL key: the DOCISPAN slice */
            ORGLRANGE, 
            ispanset,    /* SPAN key: the queried I-span */
            SPANRANGE, 
            (typeisa*)NULL);  /* <— no homedoc restriction */
        for (c = context; c; c = c->nextcontext) {
                movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
                beheadtumbler (&docid, &document.address);
                /* deduplicate, append to addressset */
        }
        contextfree (context);
}
```

`retrieverestricted` [retrie.c:56-85] receives `docisaptr = NULL`:
```c
if (docisaptr) {
        movetumbler(docisaptr, &info.homedoc);
        infoptr = &info;
} else {
        infoptr = NULL;   /* <— this branch */
}
temp = retrieveinarea (fullcrumptr, ..., (typebottomcruminfo*)infoptr);
```

`retrieveinarea` [retrie.c:87-110] → `findcbcinarea2d` [retrie.c:229-268] with `infoptr = NULL`. In the DISTRIBUTION build, passing non-NULL `infoptr` to `findcbcinarea2d` is an immediate `gerror` — this path was intentionally never exercised:
```c
if (infoptr)
    gerror("!NULL");
```

With `infoptr = NULL`, `crumqualifies2d` [retrie.c:270-305] skips the `homedoc` equality check at line 274 entirely:
```c
if ((crumptr->height == 0) && infoptr && !tumblereq(...)) return (FALSE);
```

The enfilade is traversed purely structurally against the two dimension ranges (ORGLRANGE in the DOCISPAN slice, SPANRANGE matching the I-span). Every qualifying crum bottom is returned.

The returned document ISA is then recovered from the crum's accumulated ORGL offset:
```c
movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
beheadtumbler (&docid, &document.address);  /* strips DOCISPAN prefix */
```

**`findorgl` is never called for any returned document.** The document ISA comes directly out of the spanfilade crum key — the same key that `insertspanf` wrote as `prefixtumbler(isaptr, DOCISPAN, ...)` during the original insert or version copy. No BERT check, no open check, no granfilade lookup. The returned addresses are raw tumbler values decoded from the crum structure.

---

### Combined answer

**Q1:** Yes. `docreatenewversion` [do1.c:260] calls `docopyinternal` [do1.c:293], which calls `insertspanf(taskptr, spanf, newisaptr, ispanset, DOCISPAN)` [do1.c:79]. The I-spans come from translating the original document's full V-extent through `specset2ispanset` → `vspanset2ispanset` → `permute`. After this call, the spanfilade has DOCISPAN entries for both the original and the new version, keyed by their respective ISAs but mapped to identical I-span (permascroll) addresses. A `FINDDOCSCONTAINING` query over any of those I-spans therefore returns both documents.

**Q2:** No BERT is required for either the queried document or the returned documents. The queried document uses `NOBERTREQUIRED` [do1.c:21], which `checkforopen` [bert.c:59] passes unconditionally. The returned documents are never subjected to `findorgl` at all — `finddocscontainingsp` [spanf1.c:171] calls `retrieverestricted` with `(typeisa*)NULL`, which feeds `infoptr = NULL` into `findcbcinarea2d` [retrie.c:249], bypassing all access-control filtering. The document ISAs in the result set are decoded directly from spanfilade crum keys via `beheadtumbler` [spanf1.c:174], with no open check of any kind.
