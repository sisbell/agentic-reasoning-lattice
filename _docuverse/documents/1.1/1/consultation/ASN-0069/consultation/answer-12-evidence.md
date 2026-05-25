## Question 12 [evidence]

> Does CREATENEWVERSION emit DOCISPAN entries in the spanfilade for the new version, given that no new I-spans are introduced — and if so, is there one DOCISPAN per shared I-span in the source's text subspace?

## KB Synthesis

**Yes — CREATENEWVERSION emits DOCISPAN entries for the new version, one per contiguous I-span in the source's text subspace.**

## Evidence

**Call chain confirms `insertspanf` is invoked:**

`[ST-VERSION]` (Finding 0077) gives the full chain:
`docreatenewversion` → `createorglingranf` (doc address) → `doretrievedocvspanfoo` → `docopyinternal` → `specset2ispanset` → `insertpm` (POOM) → **`insertspanf` (SPAN entries)**

The code reference is `docopyinternal` at `do1.c:66-82`. While Finding 0077 says "SPAN entries" rather than explicitly "DOCISPAN entries," the empirical proof follows immediately.

**Versions appear in `find_documents`, which requires DOCISPAN entries:**

`[INT-LINK-VERSION]` / `[ST-VERSION-CREATE]` (Finding 0018) documents:
> `find_documents("Original text") → [original, version]`

`[INV-IADDRESS-PERMANENT]` establishes that `FINDDOCSCONTAINING` only returns documents indexed in the spanfilade DOCISPAN sub-index. For a version to appear there, `insertspanf(..., DOCISPAN)` must have been called with the version's ISA.

**No new content I-addresses are created:**

`[FC-GRANF-ON-VERSION]` (Finding 0077) establishes CREATENEWVERSION makes no calls to `findisatoinsertgr` for content — the version's DOCISPAN entries reference the **source's existing I-addresses**, now mapped to the new version document ISA. This is consistent with `[INV-SPANF-GROWTH]`: DOCISPAN count grows by the number of I-spans placed, regardless of byte count.

## Entry count

`[SS-DOCISPAN]` (Finding 0047) is the controlling rule: `insertspanf` makes one `insertnd` call per `typeispan` in the linked list. Therefore:

| Source content structure | DOCISPAN entries created |
|--------------------------|-------------------------|
| Single contiguous block (1 I-span) | **1** |
| k contiguous I-spans (e.g., due to interleaved CREATELINK operations breaking contiguity per `[INT-LINK-INSERT]`) | **k** |

Only the **text subspace** (1.x) is copied (`[ST-VERSION-CREATE]`, Finding 0043 / 0046) — the link subspace (2.x) is excluded, so no DOCISPAN entries are emitted for link orgls.

## Summary

CREATENEWVERSION emits exactly `|ispanset(source_text_subspace)|` DOCISPAN entries into the spanfilade, each mapping a contiguous I-address range from the source → new version document ISA. No new content I-addresses are allocated; the entries share the source's existing I-space.

---

## Code Exploration

All line numbers verified. Here is the complete answer.

---

## Does CREATENEWVERSION emit DOCISPAN entries in the spanfilade?

**Yes — exactly one DOCISPAN entry per I-span in the source document's text subspace.**

---

### Call chain

**`fns.c:289`** — `createnewversion` entry point:
```c
void createnewversion(typetask *taskptr) {
    ...
    if (   getcreatenewversion (taskptr, &originaldocisa)
        && docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa))
        putcreatenewversion (taskptr, &newdocisa);
```
The source ISA is passed as both `isaptr` and `wheretoputit`. Since they are equal and the user owns the document, `makehint(DOCUMENT, DOCUMENT, ...)` applies [`do1.c:270–271`].

---

**`do1.c:260`** — `docreatenewversion`:

```c
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) return FALSE;   // line 281

vspec.next = NULL;
vspec.itemid = VSPECID;
movetumbler(isaptr, &vspec.docisa);      // vspec.docisa = SOURCE doc ISA
vspec.vspanset = &vspan;                 // vspan from the source doc

addtoopen(newisaptr, user, TRUE, WRITEBERT);
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);   // line 293
```

`doretrievedocvspanfoo` [`do1.c:301`] retrieves the source document's full V-span. That vspan is then wrapped in a `vspec` (with `docisa` = source ISA) and passed to `docopyinternal` with `newisaptr` as the target.

---

**`do1.c:66`** — `docopyinternal`:

```c
if (!specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)) return FALSE; // line 74
if (!findorgl      (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)) return FALSE;
if (!acceptablevsa (vsaptr, docorgl)) return FALSE;
if (!asserttreeisok(docorgl)) return FALSE;
if (!insertpm      (taskptr, docisaptr, docorgl, vsaptr, ispanset)) return FALSE;
if (!insertspanf   (taskptr, spanf, docisaptr, ispanset, DOCISPAN)) return FALSE;  // line 79
```

`specset2ispanset` converts the vspec (source doc's V-spans) into an ispanset — a linked list of I-span records. Every V-span segment in the source is resolved to the I-span(s) that back it. Then `insertspanf` is called with `docisaptr = newisaptr` and spantype `DOCISPAN`.

---

**`spanf1.c:15`** — `insertspanf`:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // line 22
tumblerclear  (&crumwidth.dsas[ORGLRANGE]);
clear (&linfo, sizeof(linfo));
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    if (((typeitemheader *)sporglset)->itemid == ISPANID) {
        movetumbler (&((typeispan *)sporglset)->stream, &lstream);   // line 27
        movetumbler (&((typeispan *)sporglset)->width,  &lwidth);    // line 28
        movetumbler (isaptr, &linfo.homedoc);                        // line 29
    }
    ...
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);             // line 49
    movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);              // line 50
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE); // line 51
}
```

The loop walks the entire ispanset. **For each I-span, one `insertnd` call is made** — one spanfilade node inserted.

The node's ORGLRANGE dimension is keyed by `prefixtumbler(newisaptr, DOCISPAN, ...)` — that is, the new document's ISA, tagged with span-type 4 (DOCISPAN). The SPANRANGE dimension carries the I-span's `stream` (origin) and `width`. The `linfo.homedoc` is also set to `newisaptr`.

---

### Conclusion

CREATENEWVERSION **does** emit DOCISPAN entries into the spanfilade for the new version. The granularity is **one entry per I-span** in the source document's text subspace. No new I-spans are allocated — the source document's existing I-spans are re-used — but each one gets its own DOCISPAN crumb in the spanfilade keyed under the new version's ISA. If the source document's text subspace is backed by N distinct I-spans, the new version receives exactly N DOCISPAN entries.
