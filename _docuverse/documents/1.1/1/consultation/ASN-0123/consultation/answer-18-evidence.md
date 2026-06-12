## Question 18 [evidence]

> Is there any structure written into the source document's orgl or POOM when a version is created from it — a forward pointer to the child version — or is the ancestry chain navigable only downward-to-upward by parsing the version's tumbler address?

## KB Synthesis

No forward pointer is written anywhere in the source document's orgl or POOM. The ancestry chain is navigable only by parsing the version's tumbler address.

**What CREATENEWVERSION actually does to the source**

`docreatenewversion` performs exactly three effects, none of which touch the source document's orgl or POOM [ST-VERSION, Finding 0077]:

1. Allocates a new document address `d'` via `createorglingranf` (adds one entry to the document-address region of the granfilade)
2. Reads the source's text vspan via `doretrievedocvspanfoo` (a read — no mutation)
3. Copies text content into the new version via `docopyinternal` → `insertspanf` (writes to the version's POOM and the spanfilade, not to the source)

[FC-VERSION-ISOLATION] is explicit: "once a version is created, it is a fully independent document with its own POOM tree. Edits to the original document do not affect the version and vice versa." [FC-GRANF-ON-VERSION] confirms that VERSION "does NOT modify the content portion of the granfilade" for the source — only a new document address entry appears.

**How lineage is encoded**

For owned-document versions, the allocation rule is `version_address ∈ children(source_address)` — the version's tumbler is a structural child of the source's tumbler [SS-VERSION-ADDRESS, Finding 0032]. For example, source `1.1.0.1.0.1` produces versions `1.1.0.1.0.1.1`, `1.1.0.1.0.1.2`, etc. This encoding is the *only* record of the relationship.

To discover what versions exist of a document, a reader must search the granfilade for addresses whose prefix matches the source document's address — exactly what `findpreviousisagr` does during allocation [ST-ADDRESS-ALLOC, Finding 0068]. There is no index, no pointer list, and no back-reference stored in the source.

**The cross-user break**

For versions created by a user who does not own the source document, even this address-based lineage disappears. VERSION uses `makehint(ACCOUNT, DOCUMENT, ...)` in the unowned case, placing the version under the creating user's account rather than under the source document [SS-VERSION-ADDRESS, Finding 0068]. Those versions are structurally indistinguishable from ordinary new documents — the ancestry chain has been fully severed at the address level.

---

## Code Exploration

I now have everything needed for a definitive answer. Here is the full analysis with code citations.

---

## Answer

**No forward pointer is written into the source document's POOM or orgl when a version is created.** The ancestry chain is navigable in only one direction — upward (child→parent) — and only by decoding the version's tumbler address. There is no way to enumerate a document's children by reading the document's own data structures.

---

### The complete execution trace for `createnewversion`

The FEBE handler dispatches at `fns.c:289-300`:

```c
void createnewversion(typetask *taskptr)
{
    typeisa originaldocisa, newdocisa;
    if (getcreatenewversion(taskptr, &originaldocisa)
    && docreatenewversion(taskptr, &originaldocisa, &originaldocisa, &newdocisa))
        putcreatenewversion(taskptr, &newdocisa);
```

Note: `wheretoputit = &originaldocisa` — the same address as the source. The work is in `docreatenewversion` at `do1.c:260-298`.

#### Step 1 — Compute and allocate the new version's address [`do1.c:270-279`]

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
if (!createorglingranf(taskptr, granf, &hint, newisaptr)) {
    return (FALSE);
}
```

`makehint` simply fills in `hintptr->supertype`, `hintptr->subtype`, `hintptr->atomtype`, `hintptr->hintisa` [`do2.c:78-84`]. For the standard case (own document), `hint.hintisa = *isaptr` (the source address) and `hint.supertype = hint.subtype = DOCUMENT`.

`createorglingranf` → `createorglgr` [`granf2.c:111-128`] calls `findisatoinsertgr` to compute a **new** ISA, then calls `insertseq` to write a `GRANORGL` node into the granfilade at that new address — **the source document is not touched**.

#### Step 2 — How the new address is computed [`granf2.c:203-242`]

In `findisatoinsertnonmolecule`, with `hint.supertype == hint.subtype == DOCUMENT`:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;   // depth = 1
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);  // upperbound = hintisa + 1
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

`findpreviousisagr` finds the rightmost existing granfilade address strictly less than `upperbound = hintisa + 1`. The source document itself (`hintisa`) is the rightmost address satisfying that bound. The `lowerbound_under_hint` check confirms it's a prefix match. Then:

```c
tumblertruncate (&lowerbound, hintlength + depth, isaptr);
tumblerincrement(isaptr, tumblerlength(isaptr) == hintlength ? depth : 0, 1, isaptr);
```

For the first version child, `lowerbound = hintisa` (length = `hintlength`), so the increment fires at `depth = 1`:

```c
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);  // hintisa.0.1
```

The resulting address is `source_isa.0.1` — the first "story" appended below the source's address. Subsequent versions get `.0.2`, `.0.3`, etc.

**This is purely address arithmetic computed from the existing granfilade contents. No write to the source document occurs.**

#### Step 3 — Read the source document's V-span [`do1.c:281-283`]

```c
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {
    return FALSE;
}
```

`doretrievedocvspanfoo` → `findorgl(…, NOBERTREQUIRED)` + `retrievedocumentpartofvspanpm`:

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```
[`orglinks.c:155-162`]

This is a **read-only** operation. It copies the root crum's `cdsp` and `cwid` fields into a local `vspan` struct. No modification.

#### Step 4 — Copy the content into the new version [`do1.c:292-296`]

```c
addtoopen(newisaptr, user, TRUE, WRITEBERT);          // BERT table only (in-memory)
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // writes to NEW POOM only
logbertmodified(newisaptr, user);                     // BERT table only (in-memory)
doclose(taskptr, newisaptr, user);                    // closes NEW doc
```

`docopyinternal` calls `insertpm` [`orglinks.c:75-134`] which calls `insertnd` [`insertnd.c:15`] which calls `makegappm` and `doinsertnd` — all acting on `newisaptr`'s POOM (the new version's orgl), not the source's.

The `logbertmodified` and `addtoopen` calls operate on the BERT table, which is an in-memory session hash table [`bert.c:13-30`]. The BERT table tracks open-state for the current connection only; it is not part of the persistent data structures and contains no ancestry information.

---

### What "forward-navigable ancestry" would require (and why it's absent)

A forward pointer (parent→child) would require that `docreatenewversion` call `findorgl(…, WRITEBERT)` on the source document and then `insertpm` or `insertnd` on its POOM. There is no such call anywhere in the function. The only `findorgl` call on the source is in `doretrievedocvspanfoo` with `NOBERTREQUIRED` — an explicit read-only access mode [`do1.c:307`].

---

### How upward navigation (child→parent) works

The tumbler address structure is the only ancestry record. Given a version at address `A.0.N`:

- **Parent document address** = `A` = `tumblertruncate(child_address, tumblerlength(child_address) - 2)`
- **Sibling versions** = addresses matching prefix `A.0.*`

Neither operation requires reading the POOM or orgl of any document. The granfilade itself serves as the address-space index, and `findpreviousisagr`/`retrievecrums` can traverse it to enumerate all children of a given prefix — but that is a **granfilade scan**, not a pointer dereference from the parent document's internal structure.

---

### Summary

| Direction | Mechanism | Where encoded |
|---|---|---|
| Child → Parent | Truncate child's tumbler address by 2 digits | In the address itself |
| Parent → Children | Granfilade scan over prefix `parent_addr.0.*` | In the global granfilade |
| Parent document POOM/orgl | Nothing written | **No record exists** |

The source document's POOM and orgl are completely unmodified by version creation. There is no forward pointer. The ancestry graph is encoded purely in the address space, and downward navigation requires querying the granfilade by prefix — not reading the parent's data.
