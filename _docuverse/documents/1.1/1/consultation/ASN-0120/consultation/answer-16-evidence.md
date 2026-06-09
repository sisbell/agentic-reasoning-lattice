## Question 16 [evidence]

> Must the home document of a new link have any I-address overlap with the content its endsets reference, or can a link be created whose home document shares no content identity with either its source or target endset?

## KB Synthesis

No overlap is required. The KB is explicit on this.

**Home document's actual role** [SS-LINK-HOME-DOCUMENT]: the home document serves two purposes only — (1) it determines the link's allocated address (the link gets an I-address under `home_doc.0.2.N`), and (2) it receives the link orgl ISA reference in its own 2.x POOM subspace via `docopy`. The KB explicitly states: "The home document is distinct from the source document — a link's home document need not be the document containing the link's source endpoint" and "the home document is the owner/container of the link for allocation purposes, independent of where the link's endpoints point."

**Precondition for `create_link`** [PRE-LINK-CREATE]: "source content exists AND target content exists AND both endpoint widths >= 1 AND home_doc is valid." No constraint requiring the home document to overlap in I-space with either endpoint.

**Mechanically** [ST-LINK-CREATE] (Finding 0012): `docreatelink` runs three steps — allocate link orgl in granf, copy link ISA into home doc's 2.x subspace, then index endpoints in spanf via `insertendsetsinspanf`. The endpoint indexing step reads the source/target specsets and converts them to I-spans for spanf insertion. Home doc content is never consulted during this step.

**Consequence**: a link can be created where `home_doc`, `source_doc`, and `target_doc` are three completely distinct documents with no shared I-addresses. The link is stored in `home_doc`'s POOM, but discovered via I-address intersection with `source_doc` or `target_doc` content [INT-LINK-TRANSCLUSION]. The home doc's content is irrelevant to link discovery — `find_links` operates purely through the spanf I-address index [SS-SPANF-OPERATIONS].

---

## Code Exploration

The code is unambiguous. Here is the full answer.

---

## Answer: No Overlap Required

A link can be created whose home document shares **no I-address content identity** with either its source or target endset. The code enforces no such constraint anywhere in the call chain.

---

### Call Chain

**`fns.c:100-112` — `createlink` (FEBE entry point)**

```c
void createlink(typetask *taskptr)
{
  typeisa docisa, linkisa;
  typespecset fromspecset, tospecset, threespecset;
  bool getcreatelink(), docreatelink();

    if (
       getcreatelink (taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
    && docreatelink (taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)){
        putcreatelink (taskptr, &linkisa);
    }else
        putrequestfailed (taskptr);
}
```

`docisa` (home document) and the three endsets are parsed as independent values. No cross-check.

---

**`get1.c:46-61` — `getcreatelink` (parser)**

```c
bool getcreatelink(typetask *taskptr, typeisa *docisaptr, typespecset *fromspecsetptr,
                   typespecset *tospecsetptr, typespecset *threespecsetptr)
{
    prompt (taskptr, "home document=> ");
    if (!getisa (taskptr, docisaptr))      return (FALSE);
    prompt (taskptr, "fromset\n");
    if (!getspecset (taskptr, fromspecsetptr)) return (FALSE);
    prompt (taskptr, "toset\n");
    if (!getspecset (taskptr, tospecsetptr))   return (FALSE);
    prompt (taskptr, "threeset\n");
    if (!getspecset (taskptr, threespecsetptr)) return (FALSE);
    return (TRUE);
}
```

Each parameter is parsed and validated in isolation. No comparison between `docisaptr` and any endset.

---

**`do1.c:195-221` — `docreatelink` (core logic)**

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr, typespecset fromspecset,
                  typespecset tospecset, typespecset threespecset, typeisa *linkisaptr)
{
    ...
    makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);          // line 207
    return (
         createorglingranf (taskptr, granf, &hint, linkisaptr)      // allocate link ISA
      && tumbler2spanset (taskptr, linkisaptr, &ispanset)
      && findnextlinkvsa (taskptr, docisaptr, &linkvsa)             // find next V-addr in home doc
      && docopy (taskptr, docisaptr, &linkvsa, ispanset)            // copy link into home doc
      && findorgl (taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
      && specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)  // line 214
      && specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)  // line 215
      && specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)// line 216
      && setlinkvsas (&fromvsa, &tovsa, &threevsa)
      && insertendsetsinorgl (...)
      && insertendsetsinspanf (...)
    );
}
```

`docisaptr` is used for exactly three purposes:
1. Build the `hint` that places the link inside the home document's address space (`makehint`, line 207)
2. Find where to append the link V-address within the home doc (`findnextlinkvsa`, line 211)
3. Copy the link atom into the home doc (`docopy`, line 212)

The endsets are resolved completely independently via `specset2sporglset` (lines 214–216), which reads the `docisa` embedded in each `vspec`—the documents the endsets *point to*—not the home document.

---

**`sporgl.c:14-33` — `specset2sporglset` (endset resolution)**

```c
bool specset2sporglset(typetask *taskptr, typespecset specset,
                       typesporglset *sporglsetptr, int type)
{
    for (; specset; ...) {
        if (itemid == ISPANID) { ... }
        else if (itemid == VSPECID) {
            vspanset2sporglset(taskptr, &((typevspec *)specset)->docisa,  // endset's own docisa
                               ((typevspec *)specset)->vspanset, ...)
        }
    }
}
```

The `docisa` field used here belongs to the spec itself — the document the endset refers to. The home document is **never consulted**.

---

**`insertnd.c:301-309` — `isanextensionnd` (the only `homedoc` check)**

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    ...
}
```

This is the **sole place** in the insertion path where `homedoc` is compared. It checks whether two crums in the enfilade share the same home document—a **data structure consistency** check internal to the home document's enfilade, not a constraint relating the home document to endset content.

---

### What the Home Document Actually Is

`wisp.h:108` shows `homedoc` is simply a `tumbler` field in `type2dbottomcruminfo`. It records *where the link is stored*, not what it points at. The link atom lives in the home document's virtual address space; the endsets live in their own documents, located by independent V→I address mappings resolved through the spanfilade (`spanf`) and granfilade (`granf`).

---

### Conclusion

**A link's home document can share zero content identity with either endset.** The home document is purely a storage address — it determines which document's enfilade will hold the link atom. The endsets are independently specified V-spans in arbitrary other documents. Nothing in `getcreatelink` [`get1.c:46`], `docreatelink` [`do1.c:207-220`], `specset2sporglset` [`sporgl.c:14-33`], or any called function checks for, requires, or enforces any I-address overlap between the home document and the content the endsets identify.
