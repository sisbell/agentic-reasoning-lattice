## Question 18 [gregory]

> Is there a CREATEDOCUMENT operation distinct from the first INSERT into a new address, or does the document implicitly come into existence when content is first inserted — i.e., does the POOM get created lazily on first write?

## KB Synthesis

There is a distinct CREATEDOCUMENT operation — documents do not come into existence lazily.

**Evidence for explicit creation:**

[ST-VERSION-CREATE] Finding 0032 directly contrasts the two mechanisms: "This atomicity distinguishes it from the two-step CREATEDOCUMENT + COPY sequence, which has an observable intermediate state (empty document exists)." This confirms CREATEDOCUMENT is a distinct protocol operation that produces an empty-but-existent document before any content is inserted.

[SS-GRANF-OPERATIONS] Finding 0012 lists `createorglingranf()` as the operation that "creates a new orgl (used for documents and links)." This is called at creation time, not deferred.

[EC-EMPTY-DOC] Finding 0058 identifies two structurally distinct empty states:
- **Never-filled** (`createenf` output): height-1 tree with one zero-width bottom node
- **After delete-everything**: taller tree with empty intermediates, no bottom nodes

The never-filled state is the initial state established at document creation. The POOM is created eagerly via `createenf(POOM)` at that point. This distinction matters operationally: Finding 0064/Bug 0019 shows that inserting into a delete-everything document crashes, because `firstinsertionnd` assumes a bottom crum exists (true for never-filled, false for delete-everything).

[ST-ADDRESS-ALLOC] Finding 0021 establishes that address allocation via `findisatoinsertnonmolecule` happens at creation time, producing a new document address under the parent account. There is no mechanism for lazy address assignment.

[PRE-OPEN-DOC] Finding 0014 requires documents to be opened (BERT token acquired) before mutations. Opening requires the document to already exist in the BERT table and the open list — another precondition that requires prior creation.

**Summary:** CREATEDOCUMENT is a distinct operation that (1) allocates a document address via `findisatoinsertnonmolecule`, (2) creates a document orgl via `createorglingranf`, and (3) initializes a minimal POOM via `createenf(POOM)`. The resulting document has an empty but structurally valid POOM. Subsequent INSERT operations use `firstinsertionnd` to add the first content into this pre-existing structure.

---

## Code Exploration

I now have everything I need. Here is my full answer.

---

## Answer: CREATENEWDOCUMENT is a Real, Distinct, Mandatory Operation

Documents are **not** created lazily on first INSERT. There is an explicit `CREATENEWDOCUMENT` operation (opcode 11), and inserting into a document address that was never created will **immediately fail** — not create anything implicitly.

---

### 1. CREATENEWDOCUMENT is a registered protocol operation

`requests.h:28`:
```c
#define CREATENEWDOCUMENT 11
```

`init.c:52`:
```c
requestfns[CREATENEWDOCUMENT] = createnewdocument;
```

Its get/do/put pipeline:

- **`fns.c:276-286`** — `createnewdocument()`, the top-level handler
- **`get1fe.c:131-136`** — `getcreatenewdocument()` takes no arguments — there is nothing to receive from the client; just logging and emitting the opcode
- **`do1.c:234-241`** — `docreatenewdocument()` — does the actual work
- **`putfe.c:305-314`** — `putcreatenewdocument()` — sends the newly allocated address back

---

### 2. What CREATENEWDOCUMENT actually creates — the POOM

`do1.c:239-240`:
```c
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf (taskptr, granf, &hint, isaptr));
```

The hint type is `ACCOUNT → DOCUMENT`: "find the next available DOCUMENT slot beneath the user's ACCOUNT address."

`createorglingranf()` → `createorglgr()` at `granf2.c:111-128`:
```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
    return (FALSE);
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);   // ← allocates the POOM
reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
locinfo.granstuff.orglstuff.orglincore = TRUE;
locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);       // ← registers in granfilade
```

`createenf(POOM)` allocates a fresh, empty enfilade tree (the POOM — **Permutation Of Ordered Material** — the tree structure that holds a document's content in V-space). This tree is inserted into the granfilade at the newly computed address, which is returned to the caller as the document's permanent ISA (e.g., `1.1.0.1.0.2`).

---

### 3. Why INSERT fails if CREATENEWDOCUMENT was never called

`doinsert()` at `do1.c:117-119`:
```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset));
```

The hint subtype is `ATOM`. This flows to `inserttextingranf()` → `inserttextgr()` → `findisatoinsertgr()`.

**The decisive guard** at `granf2.c:134-141`:
```c
/* For ATOM types (text/link content), we need a document to exist first */
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {
#ifndef DISTRIBUTION
        fprintf (stderr,"nothing at hintisa for atom\n");
#endif
        return (FALSE);
    }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
```

`isaexistsgr()` (at `granf2.c:244-253`) does a live lookup in the granfilade tree for the document's tumbler address. If no `GRANORGL` node exists at that address — because `CREATENEWDOCUMENT` was never called — it returns `FALSE`, which propagates up through `inserttextgr` → `inserttextingranf` → `doinsert` as a hard failure. There is **no fallback, no auto-create path**.

---

### 4. A second guard: the OPEN check

Even if the document's granfilade node *does* exist, `docopy()` (also called from `doinsert`) calls `findorgl()`, which enforces the bert open table:

`granf1.c:22-38`:
```c
if ((temp = checkforopen(isaptr, type, user)) <= 0) {
    ...
    *orglptr = NULL;
    return FALSE;
}
*orglptr = fetchorglgr(taskptr, granfptr, isaptr);
return (*orglptr ? TRUE : FALSE);
```

`checkforopen()` in `bert.c:52-87` returns 0 for "sufficiently open" owned documents that are not yet in the bert table, or -1 when write access is needed but blocked. A document must be opened with `OPEN` (opcode 35, `doopen()`) before its POOM can be fetched. `findorgl` with `WRITEBERT` will fail unless the connection holds a write-open entry in the bert hash table.

The complete mandatory sequence to insert into a document is therefore:
1. **`CREATENEWDOCUMENT`** → allocates POOM, registers in granfilade, returns address
2. **`OPEN`** → adds bert entry (with `WRITEBERT` type) for this connection
3. **`INSERT`** → both guards pass; text is placed in the POOM and V-span recorded

---

### 5. Internal code confirms the same pattern

`xumain.c:127-144` — the `sourceunixcommand` handler, which bulk-loads text, calls `docreatenewdocument()` explicitly before entering the insert loop:
```c
docreatenewdocument (taskptr, &docisa);
putcreatenewdocument (taskptr, &docisa);
...
while (...) {
    doappend (taskptr, &docisa, textsetptr);
```

Even in this internal path, document creation must precede content insertion.

---

### Conclusion

The POOM — the enfilade tree that stores a document's content — is **eagerly allocated** by `CREATENEWDOCUMENT` via `createenf(POOM)` and registered in the granfilade at a new permanent address. There is no lazy creation. The `findisatoinsertgr` guard at `granf2.c:135-141` explicitly checks `isaexistsgr` before allowing any atom (text or link) insertion, and returns `FALSE` with the message `"nothing at hintisa for atom"` if the document node is absent. No INSERT operation has any code path that would create a document node as a side effect.
