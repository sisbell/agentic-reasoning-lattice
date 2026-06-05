## Question 15 [evidence]

> Does creating an empty document produce any DOCISPAN entries in the spanfilade, or does the spanfilade remain unchanged until content is inserted?

## KB Synthesis

Creating an empty document produces **no DOCISPAN entries**. The spanfilade remains completely unchanged.

The KB is explicit on the access pattern: [FC-CONTENT-SPANF-ISOLATION] (Finding 0012) lists document creation as a **granf-only** operation — it allocates a new address in the granfilade via `createorglingranf`/`findisatoinsertnonmolecule`, but makes no call to any spanf function.

DOCISPAN entries are created only by the `docopy` path: `doinsert` → `inserttextingranf` → `docopy` → `insertspanf(..., DOCISPAN)` [ST-INSERT, Finding 0036]. No content means no ispanset, which means `insertspanf` is never called.

[INV-SPANF-GROWTH] confirms this: spanfilade size is bounded by `Σ |ispanset(op)|` across INSERT/COPY operations — zero operations means zero entries.

Note the contrast with CREATENEWVERSION on a non-empty source: even though that also "creates" a document, it does call `docopyinternal` → `insertspanf` to register the copied I-addresses [ST-VERSION, Finding 0077]. But that's because it's copying content, not because it's creating a document.

Bottom line: an empty document is invisible to the spanfilade until first INSERT or COPY.

---

## Code Exploration

I have all the information needed. Here is the complete answer.

---

## Answer: Empty Document Creation and the Spanfilade

**Creating an empty document produces no DOCISPAN entries in the spanfilade. The spanfilade remains completely unchanged until content is inserted.**

---

### The `createnewdocument` Path

The FEBE handler is `createnewdocument` [fns.c:276–286]:

```c
void createnewdocument(typetask *taskptr)
{
  typeisa newdocisa;
  bool docreatenewdocument();
    getcreatenewdocument();
    if (docreatenewdocument (taskptr, &newdocisa))
        putcreatenewdocument (taskptr, &newdocisa);
      else
        putrequestfailed (taskptr);
}
```

It delegates immediately to `docreatenewdocument` [do1.c:234–241]:

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
  typehint hint;
  bool createorglingranf();
    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

This is the complete body. It calls exactly one function: `createorglingranf`. That function creates a new orgling entry in the **granfilade** (the document tree). There is no call to `insertspanf`, `insertendsetsinspanf`, or any spanfilade function at all.

---

### What Creates DOCISPAN Entries

`DOCISPAN` is defined at [xanadu.h:39]:

```c
#define DOCISPAN        4
```

It is passed to `insertspanf` in exactly two places:

1. **`docopy`** [do1.c:62]: `insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)` — called during content copy operations.
2. **`docopyinternal`** [do1.c:79]: `insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)` — called during `docreatenewversion`.

Both require a non-NULL `ispanset` to do any work.

---

### Why `insertspanf` Does Nothing With an Empty Set

`insertspanf` [spanf1.c:15–54] iterates over its `sporglset` argument (the ispanset):

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    ...
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
}
return (TRUE);
```

The only place `insertnd` is called — the actual node insertion into the spanfilade — is inside that `for` loop at [spanf1.c:51]. If `sporglset` is `NULL`, the loop body never executes. The function returns `TRUE` without writing anything.

---

### The `docreatenewversion` Case (From an Empty Document)

`docreatenewversion` [do1.c:260–299] is more complex: after calling `createorglingranf` to allocate the new document ISA, it calls `doretrievedocvspanfoo` to get the source document's vspan, then calls `docopyinternal` with it [do1.c:293]:

```c
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
```

When the source document is empty, `doretrievedocvspanfoo` [do1.c:301–309] retrieves a zero-width or null vspan from the granfilade. `docopyinternal` then calls `specset2ispanset` on that empty vspec, producing a `NULL` ispanset. When that NULL ispanset reaches `insertspanf` [spanf1.c:25], the `for` loop condition fails immediately — `sporglset` is `NULL` — and no DOCISPAN node is inserted.

The `doretrievedocvspanset` function [do1.c:330–332] explicitly documents this contract:

```c
if (isemptyorgl (docorgl)) {
    *vspansetptr = NULL;  /* Empty document returns empty vspanset */
    return TRUE;
}
```

---

### Summary

| Operation | Spanfilade effect |
|-----------|-------------------|
| `docreatenewdocument` | **None** — only `createorglingranf` is called |
| `docreatenewversion` from empty doc | **None** — `insertspanf` is called but `sporglset` is NULL; the loop at [spanf1.c:25] never executes |
| `doinsert` | Creates DOCISPAN entries — calls `docopy` → `insertspanf` with actual content |
| `docopy` / `docopyinternal` with content | Creates DOCISPAN entries — calls `insertspanf` at [do1.c:62] / [do1.c:79] |

The spanfilade is purely a content-address index. Until content spans exist and are passed through `insertspanf`, the spanfilade has no record of the document's existence.
