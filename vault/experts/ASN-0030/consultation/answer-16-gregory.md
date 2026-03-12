## Question 16 [gregory]

> Does CREATENEWVERSION produce a version whose POOM entries point to the exact same I-address values as the source, or does `docopyinternal` allocate any fresh I-addresses during the copy — even for metadata or structural bookkeeping?

## KB Synthesis

The version's POOM entries point to the **exact same I-address values** as the source. `docopyinternal` allocates no fresh I-addresses.

The call chain is: `docreatenewversion` → `doretrievedocvspanfoo` → `docopyinternal` → `specset2ispanset` → `insertpm` + `insertspanf`. The `specset2ispanset` step converts the source's V-spans to their existing I-spans by looking them up in the source's POOM. These I-spans are then passed directly to `insertpm` (to build the version's POOM mappings) and `insertspanf` (to register DOCISPAN entries). Neither call allocates; they record pre-existing I-addresses. [ST-VERSION]

The only allocation in the entire operation is the new document address itself — `createorglingranf` calls `findisatoinsertnonmolecule`, which assigns a child address under the source document. This is a document address, not a content I-address, and it lives in a separate tumbler range that does not affect the content allocation counter. [ST-VERSION-CREATE, SS-ADDRESS-ALLOC]

The KB directly confirms the consequence: inserting text after VERSION produces contiguous I-addresses with any text previously in the source, because the content allocation counter was untouched. Contrast this with CREATELINK, which does call `createorglingranf` for the link orgl (a content-type allocation), breaking subsequent text I-address contiguity. [INV-MONOTONIC]

So: `ispans(version) = ispans(source)` at creation time — a strict equality, not a copy. [ST-VERSION-CREATE]

---

## Code Exploration

I now have a complete picture of the entire call chain. Here is the full analysis.

---

## Does `docopyinternal` allocate fresh I-addresses?

**No. Zero new I-addresses are allocated.** The new version's POOM crums point to the exact same permascroll I-address values as the source document's POOM crums. Here is the code proof, step by step.

---

### Step 1 — `docreatenewversion` sets up the copy [do1.c:260-299]

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
  typevspan vspan;
  typevspec vspec;

  createorglingranf(taskptr, granf, &hint, newisaptr);        // [do1.c:277]
  doretrievedocvspanfoo(taskptr, isaptr, &vspan);             // [do1.c:281]

  vspec.docisa = *isaptr;     // source document ISA          // [do1.c:287]
  vspec.vspanset = &vspan;    // source V-span                // [do1.c:288]

  docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // [do1.c:293]
```

`createorglingranf` allocates a new document-ISA tumbler (a document address, not a permascroll content address). `vspan.stream` is the source document's V-space start position, read from the POOM root [do1.c:281].

---

### Step 2 — `doretrievedocvspanfoo` reads the source V-span [orglinks.c:155-162]

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->stream = ((typecuc *)orgl)->cdsp.dsas[V];   // POOM root displacement
    vspanptr->width  = ((typecuc *)orgl)->cwid.dsas[V];   // POOM root width
    return TRUE;
}
```

Pure read. No allocation. `vspan.stream` is the V-space start of the source document (e.g., `1.1`).

---

### Step 3 — `docopyinternal` [do1.c:66-82]

```c
bool docopyinternal(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED);   // V→I lookup
    insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset);          // POOM write
    insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN);       // spanf index
```

Three calls. None of them allocate I-addresses.

---

### Step 4 — `specset2ispanset` performs a pure read [do2.c:14-46]

```c
bool specset2ispanset(typetask *taskptr, typespec *specset, typeispanset *ispansetptr, int type)
{
    for (; specset; ...) {
        if (itemid == VSPECID) {
            findorgl(taskptr, granf, &vspec->docisa, &docorgl, type);       // open source POOM
            vspanset2ispanset(taskptr, docorgl, vspec->vspanset, ispansetptr);  // V→I
        }
    }
}
```

For the `vspec` built in `docreatenewversion`, `docisa = *isaptr` (source document) and `vspanset = &vspan` (source V-span). This looks up the source document's POOM.

---

### Step 5 — `vspanset2ispanset` → `permute` reads source POOM crums [orglinks.c:397-422]

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl,
    typevspanset vspanptr, typeispanset *ispansetptr)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` calls `span2spanset` → `retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` [retrie.c:87-110]. This traverses the source document's existing POOM tree, collecting bottom crums whose V-dimension intersects the query. Then `context2span` extracts the I-dimension values from those crums.

**This is a pure read.** No new content is written to the granfilade. The returned `typeispanset` contains `typeispan` items (itemid = `ISPANID`) holding the exact I-addresses already stored in the source POOM crums.

---

### Step 6 — `insertpm` writes those exact I-addresses into the new POOM [orglinks.c:75-134]

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl,
              tumbler *vsaptr, typesporglset sporglset)
{
    for (; sporglset; sporglset = sporglset->next) {
        unpacksporgl(sporglset, &lstream, &lwidth, &linfo);       // extract I-address

        movetumbler(&lstream, &crumorigin.dsas[I]);               // I = verbatim
        movetumbler(vsaptr,   &crumorigin.dsas[V]);               // V = source V-start

        insertnd(taskptr, orgl, &crumorigin, &crumwidth, &linfo, V);

        tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);           // advance V-pointer
    }
}
```

And `unpacksporgl` for `ISPANID` items [sporgl.c:178-203]:

```c
if (itemid == ISPANID) {
    movetumbler(&ispanptr->stream, streamptr);   // lstream = source I-address, verbatim
    movetumbler(&ispanptr->width,  widthptr);    // lwidth  = source I-width, verbatim
    tumblerclear(&infoptr->homedoc);             // homedoc = 0 (not carried over)
}
```

The I-address (`lstream`) placed into `crumorigin.dsas[I]` is the **verbatim permascroll address** read from the source POOM. No arithmetic transforms it. No allocation creates a fresh one.

---

### What IS allocated during `docreatenewversion`

| Allocation | Type | Function | Notes |
|---|---|---|---|
| New document ISA (tumbler) | Document address | `createorglingranf` [do1.c:277] | Not an I-address; document identity only |
| New POOM crums | Tree nodes | `insertnd` → `insertcbcnd` → `createcrum` [insertnd.c:260] | POOM structure, not content |
| New spanfilade entries | Index records | `insertspanf` | Link index, same I-addresses |
| Task-local `ispanset` etc. | Transient | `taskalloc` | Freed with task |

---

### Summary

`docreatenewversion` produces a version whose POOM entries carry **the exact same I-address values** as the source. The mechanism is:

1. `doretrievedocvspanfoo` reads the source V-span from the POOM root [orglinks.c:157-160]
2. `specset2ispanset` → `permute` → `retrieverestricted` reads the source POOM crums, extracting their I-dimension values [do2.c:36, orglinks.c:397-422]
3. `insertpm` places those values verbatim into `crumorigin.dsas[I]` of the new POOM crums [orglinks.c:105,130]

`docopyinternal` never calls `inserttextingranf` (the only function that allocates permascroll I-addresses). No I-space allocation occurs, not even for metadata or structural bookkeeping. The permascroll content is shared by reference across both document versions — this is the fundamental transclusional identity mechanism of udanax-green.
