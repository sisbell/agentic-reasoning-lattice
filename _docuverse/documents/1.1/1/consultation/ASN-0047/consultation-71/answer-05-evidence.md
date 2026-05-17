## Question 5 [evidence]

> In udanax-green's document-copy operation (docopy/docreatenewdocument when copying content from a source), are the destination V-positions structurally identical to the source's V-positions, or are they freshly allocated under the new document's VSA frontier?

## KB Synthesis

## V-Position Allocation in docopy and CREATENEWVERSION

The answer differs depending on which copy path is used.

---

### CREATENEWVERSION (docopyinternal)

V-positions are **structurally preserved** from the source. The call chain [ST-VERSION] is:

```
docreatenewversion → doretrievedocvspanfoo → docopyinternal
  → specset2ispanset (V-spans → I-spans from source)
  → insertpm (destination POOM, at source V-positions)
```

`doretrievedocvspanfoo` retrieves the source's V-span starting at `cdsp.dsas[V]` (i.e., 1.something for the text subspace) [ST-VERSION-CREATE, Finding 0043]. That same VSpec — including its start address — is passed into `docopyinternal`, which calls `insertpm` to place content at those V-positions in the new document.

The concrete result confirms this: a source with text at `{start: "1.1", width: "0.34"}` produces a version with `{start: "1.1", width: "0.34"}` [ST-VERSION-CREATE, Finding 0043]. The I-addresses are **shared** (not reallocated) — no call to `findisatoinsertgr` for content occurs [ST-VERSION, Finding 0077].

---

### User-invoked docopy (vcopy/transclusion)

V-positions are **freshly specified by the caller**, not copied from the source. [PRE-VCOPY, Finding 0010] describes this directly:

> "The `docopy` operation copies I-spans from a source specset into a destination document at V-position `vsaptr`."

The `vsaptr` is caller-provided. The source specset is converted to I-spans (discarding source V-positions), and those I-spans are placed at the caller-specified destination address. The concrete evidence from [ST-VCOPY, Finding 0039] shows a user specifying `vcopy(doc, V=1.19, specset=V 1.10..1.13)` — source at 1.10, destination at 1.19, entirely independent.

I-addresses are still **shared** in both cases: `docopy` uses `insertpm` (sharing existing I-addresses), never `inserttextingranf` (which would allocate fresh ones) [ST-COPY, Finding 0064].

---

### Summary

| Operation | Destination V-positions | I-addresses |
|-----------|------------------------|-------------|
| `CREATENEWVERSION` | Preserved from source (same V-address range) | Shared |
| User `vcopy`/`docopy` | Caller-specified (fresh frontier) | Shared |

---

## Code Exploration

Now I have everything I need. Let me compile the full answer.

---

## Answer: V-Position Assignment in `docreatenewversion`

### Short answer

The destination V-positions are **structurally identical to the source's V-positions** — specifically, the source document's starting V-address is copied verbatim and used as the destination VSA. They are **not** freshly allocated from the new document's frontier.

---

### Execution trace

#### 1. Entry point: `docreatenewversion` [do1.c:260–298]

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    ...
    if (!createorglingranf(taskptr, granf, &hint, newisaptr)) return FALSE;  // fresh ISA allocated
    if (!doretrievedocvspanfoo(taskptr, isaptr, &vspan)) return FALSE;       // read SOURCE vspan
    ...
    movetumbler(isaptr, &vspec.docisa);  // vspec points at SOURCE document
    vspec.vspanset = &vspan;             // vspec covers SOURCE's full V-range
    ...
    docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // <-- vsaptr = SOURCE's start
```

`vspan.stream` is the starting V-address of the **source** document. That same address is passed directly as `vsaptr` to `docopyinternal` — the destination for the copy.

#### 2. V-span extraction: `retrievedocumentpartofvspanpm` [orglinks.c:155–162]

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge */
    ...
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);  // root node's V-displacement
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);   // root node's V-width
```

This reads the POOM root node's `cdsp.dsas[V]` (V-displacement of the whole tree) directly into `vspanptr->stream`. For a document whose text begins at V=`1.1`, this yields `stream = 1.1`. **No arithmetic, no frontier lookup, no allocation.**

#### 3. `docopyinternal` → `insertpm`: V-address passed through unchanged [orglinks.c:75–134]

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, tumbler *vsaptr, typesporglset sporglset)
{
    ...
    for (; sporglset; ...) {
        unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
        movetumbler(&lstream, &crumorigin.dsas[I]);        // I-dim: permascroll address
        movetumbler(vsaptr, &crumorigin.dsas[V]);          // V-dim: = source's start addr [line 113]
        ...
        insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // insert crum
        tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);   // advance by width [line 131]
    }
```

For each I-span chunk in the source, `insertpm` creates a POOM crum whose V-dimension **starts at `vsaptr`** — which is `vspan.stream` from the source — and advances `vsaptr` by the width of each chunk. The result: successive V-addresses in the new document's POOM tree that are identical to those in the source's POOM tree.

#### 4. The `acceptablevsa` guard is a stub [do2.c:110–113]

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

No frontier check. Any VSA is accepted. There is no enforcement that the destination VSA lies at or beyond the new document's frontier.

---

### What about regular `docopy` (for inserts and links)?

For comparison, `doinsert` → `appendpm` computes the destination VSA with `findvsatoappend` [orglinks.c:29–49], which does find the end of existing content and appends beyond it — a genuine frontier-based allocation.

For `domakelink` → `findnextlinkvsa` [do2.c:151–167]:
```c
tumbleradd(&vspan.stream, &vspan.width, &vspanreach);   // compute end of doc's V-span
if (tumblercmp(&vspanreach, &firstlink) == LESS)
    movetumbler(&firstlink, vsaptr);
else
    movetumbler(&vspanreach, vsaptr);                   // use frontier
```
Link creation uses the frontier. Document-content copy (`docreatenewversion`) does not.

---

### Conclusion

In `docreatenewversion`, the sequence is:

| Step | What happens |
|------|-------------|
| `doretrievedocvspanfoo` [do1.c:281] | Reads source's root POOM node `cdsp.dsas[V]` → `vspan.stream` |
| `docopyinternal(..., &vspan.stream, ...)` [do1.c:293] | Passes source's start address as destination VSA |
| `insertpm` [orglinks.c:113] | Stamps each new POOM crum's V-dimension with that address, advancing by width |

The destination V-positions in the new document are **the same tumblers as the source document's V-positions**. The new document's ISA is freshly allocated by `createorglingranf`, but the POOM tree it receives maps the identical V-addresses → identical I-addresses (permascroll spans). There is no "new document VSA frontier" consulted; the source's `cdsp.dsas[V]` is used verbatim as the insertion point.

This is semantically intentional: a new version should preserve V-addresses so that content identity across versions (tracked by V-address) is maintained, enabling `doshowrelationof2versions` to find common content by intersecting I-spans.
