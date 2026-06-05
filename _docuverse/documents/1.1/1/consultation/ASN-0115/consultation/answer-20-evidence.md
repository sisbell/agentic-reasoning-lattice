## Question 20 [evidence]

> Does RETRIEVECONTENTS always source bytes from the granfilade by I-address (FC-GRANFILADE-PERMANENT), meaning deleted-then-orphaned I-addresses are still deliverable if a SpecSet somehow references them?

## KB Synthesis

Yes — with one important qualification about how I-addresses can be referenced.

## Retrieval Chain

RETRIEVECONTENTS (`doretrievev`) always terminates in `ispanset2vstuffset(taskptr, granf, ispanset, ...)`, which dereferences I-addresses directly against the granfilade byte store. There is no alternative path. [SS-GRANF-OPERATIONS]

## Granfilade Is Permanent

DELETE never touches the granfilade. It frees only the POOM bottom crums that *reference* I-addresses; the I-addresses and their bytes persist unconditionally. [FC-GRANF-ON-DELETE], [INV-IADDR-IMMUTABILITY]

## Can a SpecSet Reference Orphaned I-Addresses?

**Yes, but only indirectly.** A SpecSet contains V-spans, not I-addresses. The path is:

```
SpecSet (VSpec) → specset2ispanset → POOM traversal → I-addresses → granfilade bytes
```

So the reachability question reduces to: *does any currently-open document's POOM still map some V-position to the orphaned I-address?*

- If Document D deleted content but Document T (which transcluded that content via COPY) has not deleted it, T's POOM still maps those V-positions to the same I-addresses. A SpecSet referencing T's V-positions will successfully deliver the bytes. [FC-DELETE-CROSS-DOC], [ST-DELETE]
- If ALL documents have removed those I-addresses from their POOMs, no SpecSet can be constructed that resolves to them — not because the granfilade lacks them, but because there is no live V→I path.

## The Precondition Gap

`doretrievev` also requires the referenced documents to be open (`findorgl` check). If the document holding the surviving POOM mapping is closed, retrieval fails before reaching the granfilade. [PRE-RETRIEVE-CONTENTS]

## Summary

RETRIEVECONTENTS is granfilade-sourced by I-address — the bytes for any I-address that was ever inserted are permanently present. Orphaned I-addresses remain deliverable as long as **at least one open document's POOM still maps a V-position to them**. This is exactly why COPY (not INSERT) is the identity-preserving restoration mechanism: it re-establishes a POOM mapping to existing I-addresses without allocating new ones. [ST-COPY], [INV-DELETE-NOT-INVERSE]

---

## Code Exploration

I have all the source I need. Here is the full answer.

---

## Does RETRIEVECONTENTS always source bytes from the granfilade by I-address, and are orphaned I-addresses still deliverable?

**Short answer: Yes to both.** The granfilade is permanently append-only, deletion is a no-op stub, and raw I-spans bypass BERT entirely.

---

### The Execution Path

**`fns.c:175-187` — FEBE entry point**

```c
void retrievev(typetask *taskptr)
{
    if (getretrievev (taskptr, &specset)
     && doretrievev (taskptr, specset, &vstuffset))
         putretrievev (taskptr, &vstuffset);
```

**`do1.c:338-346` — `doretrievev`**

```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr)
{
  typeispanset ispanset;
    return
       specset2ispanset (taskptr, specset, &ispanset, READBERT)
    && ispanset2vstuffset (taskptr, granf, ispanset, vstuffsetptr);
}
```

Two distinct phases: (1) convert the specset to I-spans, (2) fetch bytes from the global `granf` using those I-spans. The second phase is purely positional — it takes whatever I-spans come out of phase 1 and reads bytes at those addresses.

---

### Phase 1: SpecSet → ISpanSet (the fork)

**`do2.c:23-39` — `specset2ispanset`**

```c
for (; specset; ...) {
    if (... itemid == ISPANID) {
        *ispansetptr = (typeispanset)specset;   // ← pass-through, NO check
        ispansetptr = ...
    } else if (... itemid == VSPECID) {
        if (!(
          findorgl (taskptr, granf, &...docisa, &docorgl, type)  // BERT gated
        && (ispansetptr = vspanset2ispanset (...))))
               return (FALSE);
    }
}
```

This is the critical fork:

- **`VSPECID` path**: Calls `findorgl` [granf1.c:17], which calls `checkforopen` [bert.c:52] against the document's I-address. Only succeeds if the document is open (BERT registered).
- **`ISPANID` path**: The I-span is wired **directly into the output list** with no gate at all. No BERT check, no document-open check, no ownership check.

If a client somehow constructs or holds a `specset` containing raw `ISPANID` items, phase 1 emits them verbatim into the I-span set that feeds granfilade retrieval.

---

### Phase 1 (VSPEC path): The BERT gate

**`granf1.c:17-41` — `findorgl`**

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
  int temp;
    if (/*backenddaemon &&*/(temp = checkforopen(isaptr, type, user)) <= 0) {
        if (!isxumain) {
            return FALSE;
        }
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

Two observations:

1. The `backenddaemon &&` guard is **commented out** — BERT is always checked.
2. `isxumain` is an escape hatch: if true, the function falls through to `fetchorglgr` **even if `checkforopen` returned ≤ 0**. This is for the interactive (non-daemon) `xumain` path.

The BERT gate [bert.c:52-87] only knows about *document-level* open state. It does not know whether the document's content at specific I-addresses was "deleted" from the ORGL — that distinction is invisible to the BERT hash table.

---

### Phase 1 (VSPEC path): ORGL fetch and V→I conversion

**`granf2.c:31-40` — `fetchorglgr`**

```c
if (tumblercmp (&((typecuc*)fullcrumptr)->cwid.dsas[WIDTH], address) == LESS)
    return (NULL);                          // only guard: address beyond granf bounds
if ((context = retrievecrums (..., address, WIDTH)) == NULL)
    return NULL;
if (!tumblereq((tumbler*)&context->totaloffset, address)) {
    ...
    return (NULL);                          // address not present as a granfilade node
}
```

The only guards are structural: is the I-address inside the granfilade's extent, and does an exact node exist at that address? There is no "this document was deleted" check.

**`orglinks.c:397-454` — `vspanset2ispanset` → `permute` → `span2spanset`**

Converts V-spans to I-spans by querying the document's ORGL (permutation matrix) via `retrieverestricted`. This is purely a coordinate-space translation — it returns whatever I-addresses the ORGL says correspond to the requested V-spans. No deletion check.

---

### Phase 2: ISpanSet → bytes (always by I-address)

**`granf1.c:58-74` — `ispanset2vstuffset`**

```c
bool ispanset2vstuffset(typetask *taskptr, typegranf granfptr, typeispanset ispanset, typevstuffset *vstuffsetptr)
{
    *vstuffsetptr = NULL;
    for (; ispanset; ispanset = ispanset->next) {
        vstuffsetptr = ispan2vstuffset (taskptr, granfptr, ispanset, vstuffsetptr);
    }
    return (TRUE);
}
```

No gate. Iterates all I-spans and retrieves bytes unconditionally.

**`granf2.c:286-318` — `ispan2vstuffset`**

```c
movetumbler (&ispanptr->stream, &lowerbound);
tumbleradd(&lowerbound, &ispanptr->width, &upperbound);
context = retrieveinspan ((typecuc*)fullcrumptr, &lowerbound, &upperbound, WIDTH);
for (temp = context; temp; temp = temp->nextcontext) {
    context2vstuff (taskptr, temp, ispanptr, &vstuffset);
    ...
}
```

Pure positional lookup on `granf` by I-address range. No ownership, no deletion, no access check.

**`retrie.c:112-136` — `retrieveinspan`**

```c
case GRAN:
    findcbcinspanseq ((typecorecrum*)fullcrumptr, ..., spanstart, spanend, &context);
    if (tumblercmp (spanend, &fullcrumptr->cwid.dsas[WIDTH]) == GREATER) {
        c = findlastcbcseq (...);
        oncontextlistseq (&context, c);
    }
    return (context);
```

Structural tree traversal returning all granfilade leaf nodes within the I-address interval. No concept of "orphaned."

---

### The Crucial Finding: `deleteversion` Is a Stub

**`bert.c:348-353`**

```c
int deleteversion(tumbler *tp)
{
#ifndef DISTRIBUTION
fprintf(stderr,"deleteversion: tp = ");dumptumbler(tp);fprintf(stderr,"\n");
#endif
}
```

The function body is **empty**. It prints a debug line and returns. Nothing is removed from the granfilade. `deleteversion` is called from `removefromopen` [bert.c:173-176] when a document that was `created && !modified` is closed — the intended semantics being "throw away an unmodified newly-created version." That too is a no-op.

---

### Direct Answer

**Yes, RETRIEVECONTENTS always sources bytes from the granfilade by I-address.** Phase 2 (`ispanset2vstuffset` → `ispan2vstuffset` → `retrieveinspan`) operates purely on I-span coordinates against the global `granf`. There is no higher-level deletion check at the byte-retrieval layer.

**Yes, orphaned I-addresses are deliverable**, for three independent reasons:

1. **`deleteversion` is a stub** [bert.c:348-353] — no bytes are ever removed from the granfilade. Content written at any I-address remains there for the lifetime of the process image.

2. **Raw `ISPANID` specsets bypass BERT entirely** [do2.c:24-26] — if a client holds or crafts an I-span directly, it is wired into the retrieval pipeline with zero access control.

3. **The BERT gate is document-level, not byte-level** [granf1.c:22-37, bert.c:52-87] — `checkforopen` tracks whether a document's ORGL I-address is registered as open. It does not know that specific I-spans within that document's content have been "deleted" from the ORGL's V→I mapping. Even with BERT engaged, a client that already knows the raw I-addresses of deleted content could retrieve them via the `ISPANID` path.

The term "FC-GRANFILADE-PERMANENT" does not appear in the source, but the implementation exactly matches that semantic: once bytes land in the granfilade at an I-address, they are structurally permanent. The granfilade has no delete operation — only `insertseq` [called from `inserttextgr`, granf2.c:99]. Deletion in udanax-green means removing V→I mappings from the ORGL, not removing bytes from the permascroll. Those bytes remain accessible at their I-addresses to anyone who knows them.
