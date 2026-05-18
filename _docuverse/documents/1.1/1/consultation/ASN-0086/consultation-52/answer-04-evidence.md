## Question 4 [evidence]

> Does udanax-green's retraction path enforce the sibling-frontier discipline on the emitter address and rely on it for single-tuple-scope behavior, or does it admit retractions whose fresh emitters could land at prefix-extensions of the target?

## KB Synthesis

The KB does not use the vocabulary of "retraction," "emitter address," or "sibling-frontier discipline," so I cannot confirm whether the implementation *relies on* these as explicit design primitives. However, the relevant KB evidence points clearly in one direction.

**DELETE emits nothing.** The retraction path (DELETE / `dodeletevspan`) modifies only the POOM and leaves the granfilade entirely untouched [FC-GRANF-ON-DELETE]. There are no fresh I-addresses allocated during deletion. If "retraction path" means the DELETE operation, there are no emitters at all — the premise of the question doesn't apply.

**If "retraction" involves re-insertion**, the allocation mechanism enforces exactly what the question calls sibling-frontier behavior. `findisatoinsertmolecule` / `findpreviousisagr` find the current granfilade maximum and increment by 1 at `rightshift=0` [SS-ADDRESS-ALLOC, Finding 0061]. This guarantees the new address is a *sibling-successor* of the maximum, never a prefix-extension (child) of any existing address. The upper-bound containment check [PRE-ADDRESS-ALLOC] further blocks the allocation from crossing into a sibling subtree. Deleted I-addresses are never reused [INV-NO-IADDR-REUSE], so gaps are never backfilled with children.

**The implementation does not admit fresh emitters as prefix-extensions of the target.** The monotonic, gap-preserving, sibling-only allocation is a structural consequence of the `query-and-increment` design, but it is not documented as a deliberate invariant protecting "single-tuple-scope behavior" — that framing is not in the KB.

If these terms come from a formal spec layer above the implementation (ASN definitions, span algebra), the KB cannot speak to that.

---

## Code Exploration

Now I have all the evidence needed for a complete answer. Let me synthesize the full trace.

---

## Does the Retraction Path Enforce Sibling-Frontier Discipline?

**Short answer: No — and for two independent reasons. The retraction path allocates no fresh emitter at all, and when a new version address is created upstream (via `doopen()`), the allocation deliberately lands at a prefix-extension (child) of the source ISA, not a sibling. Single-document scope is enforced by an exact-equality lookup, not by address topology.**

---

### 1. The Complete Retraction Call Chain

```
fns.c:333-347   deletevspan()
  do1.c:158-167   dodeletevspan()
    granf1.c:17-41  findorgl()        [WRITEBERT check]
    orglinks.c:145-152  deletevspanpm()
      edit.c:31-76  deletend()        [knife-cut tree deletion]
      bert.c:97-109  logbertmodified()
```

**No step in this chain computes or validates an emitter address.**

#### `fns.c:333-347` — FEBE entry point

```c
void deletevspan(typetask *taskptr)
{
  typeisa docisa;
  typespan vspan;
  bool getdeletevspan(), dodeletevspan();
 
    (void) getdeletevspan(taskptr, &docisa, &vspan);   // read docisa from wire
    putdeletevspan(taskptr);
    if (!dodeletevspan(taskptr, &docisa, &vspan))      // operate on it directly
        fprintf(stderr,"deletevspan failed \n");
}
```

The document ISA arrives from the frontend unchanged. No address computation precedes its use. No frontier check. `putdeletevspan` is issued before `dodeletevspan` even executes — the reply is sent before the operation runs.

#### `do1.c:158-167` — Core operation

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), deletevspanpm();

    return (
       findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

Compare this with `docopy` [do1.c:45-65], which takes an explicit `vsaptr` and calls `acceptablevsa()`, or `domakelink` / `docreatelink` [do1.c:169-221], which call `findnextlinkvsa()` to compute a fresh V-space address. `dodeletevspan` has neither: no `vsaptr` parameter, no `acceptablevsa()` call, no `findnextlinkvsa()` call.

#### `granf1.c:17-41` — `findorgl()` access check

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr,
              typeorgl *orglptr, int type)
{
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        if (!isxumain) {
            return FALSE;   // daemon mode: fail if not open
        }
        // isxumain mode: bypass — no check at all
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

The WRITEBERT check verifies the document is open for writing. In `isxumain` mode (running as a foreground process, not daemon), even this check is bypassed. There is no frontier-topology check here — only an access-control check.

#### `orglinks.c:145-152` — `deletevspanpm()`

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl,
                   typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

The only guard is a zero-width early-exit. The orgl passed in is the one fetched for the exact ISA. `deletend` operates within it. No new address is produced.

#### `edit.c:31-76` — `deletend()` — pure tree surgery

```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    movetumbler(origin, &knives.blades[0]);
    tumbleradd(origin, width, &knives.blades[1]);  // right knife = origin + width
    knives.nblades = 2;
    knives.dimension = index;
    makecutsnd(fullcrumptr, &knives);
    newfindintersectionnd(fullcrumptr, &knives, &father, &foffset);
    prologuend((typecorecrum*)father, &foffset, &fgrasp, (typedsp*)NULL);
    for (ptr = (typecuc*) findleftson(father); ptr; ptr = next) {
        next = (typecuc*) findrightbro((typecorecrum*)ptr);
        switch (deletecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives)) {
          case 1:  disown((typecorecrum*)ptr);        // fully inside → remove
                   subtreefree((typecorecrum*)ptr);   break;
          case 2:  tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
                   break;                             // overlaps right → adjust displacement
        }
    }
    setwispupwards(father, 1);
    recombine(father);
}
```

Knife blades are V-space positions within the document's own coordinate system. The loop walks only the children of the `father` node inside this orgl. No ISA allocation, no frontier check.

---

### 2. `acceptablevsa()` Is a Stub — and Isn't Called Here

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);   // do2.c:110-113
}
```

Even if it were a real check, it is only called in `docopy` [do1.c:56] and `docopyinternal` [do1.c:76]. It is entirely absent from the retraction path.

---

### 3. When `doopen()` Creates a Version Before Retraction

If the client calls `open(docISA, WRITE, COPYIF)`, `bert.c:264-322` may invoke `docreatenewversion()`. The ISA for that new version is allocated by `createorglgr()` → `findisatoinsertgr()` → `findisatoinsertnonmolecule()`.

#### `granf2.c:203-242` — `findisatoinsertnonmolecule()`

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;   // DOCUMENT→DOCUMENT: depth=1
    hintlength = tumblerlength(&hintptr->hintisa);
    tumblerincrement(&hintptr->hintisa, depth - 1, 1, &upperbound);
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);   // first version: hintISA.0.1
    } else {
        tumblertruncate(&lowerbound, hintlength + depth, isaptr);
        tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
    }
}
```

With `hint.supertype == hint.subtype == DOCUMENT` (from `do1.c:271: makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint)`), `depth = 1`.

`tumblerincrement(hintisa, depth=1, 1, isaptr)` [tumble.c:599-623] finds the last non-zero digit at position `idx` and increments `mantissa[idx + 1]` — one place to the right. In Xanadu tumbler notation, that is one level deeper: a child address.

**Example**: if the source document ISA is `1.1.0.1` (encoded `[1,1,0,1,0,0,...]`), the first new version is `1.1.0.1.0.1` (encoded `[1,1,0,1,0,1,0,...]`). Subsequent versions are `1.1.0.1.0.2`, `1.1.0.1.0.3`, etc.

**These new version addresses are prefix-extensions of the source ISA, not siblings.** The retraction path admits — and in fact relies on — emitters that are children of their source document.

---

### 4. How Single-Document Scope Is Actually Enforced

It is not the ISA address topology that scopes the deletion to one document. It is the exact-equality match in `fetchorglgr()`:

#### `granf2.c:22-81` — `fetchorglgr()`

```c
typeorgl fetchorglgr(typetask *taskptr, typegranf fullcrumptr, typeisa *address)
{
    if (tumblercmp(&((typecuc*)fullcrumptr)->cwid.dsas[WIDTH], address) == LESS)
        return (NULL);
    if ((context = retrievecrums((typecuc*)fullcrumptr, address, WIDTH)) == NULL)
        return NULL;
    if (!tumblereq((tumbler*)&context->totaloffset, address)) {   // EXACT MATCH
        crumcontextfree(context);
        return (NULL);
    }
    ...
    ret = context->corecrum->cinfo.granstuff.orglstuff.orglptr;
    return ((typeorgl)ret);
}
```

`tumblereq()` [tumble.c:24-36] is a field-by-field equality check — it returns false unless every mantissa digit, exp, and sign matches. So `fetchorglgr` returns non-NULL only when the ISA resolves to an exact crum in the granfilade. `deletend` then operates only within that crum's associated orgl subtree.

A version `1.1.0.1.0.2` and its source `1.1.0.1` are distinct crums in the granfilade (each has its own insertseq call [granf2.c:125]). `tumblereq` on one will not match the other. No amount of address prefix-extension confusion can cause `deletend` to operate on the wrong document's tree.

The isolation is structural (separate tree nodes) and identity-based (exact tumbler equality), not topological.

---

### Summary

| Claim | Evidence |
|---|---|
| Retraction path computes no fresh emitter | `dodeletevspan` has no `vsaptr` output, no `findnextlinkvsa` call [do1.c:158-167] |
| `acceptablevsa()` is a no-op and not called in retraction | `do2.c:110-113`, `do1.c:56,76` |
| New version ISAs are prefix-extensions (children) of source, not siblings | `granf2.c:237: tumblerincrement(hintisa, depth=1, 1, isaptr)` |
| Single-document scope enforced by exact ISA equality, not frontier discipline | `granf2.c:37: tumblereq(&context->totaloffset, address)` |
| No sibling-frontier check anywhere in retraction path | Absence of any such check in `fns.c:333-347`, `do1.c:158-167`, `orglinks.c:145-152`, `edit.c:31-76` |

The retraction path does not enforce sibling-frontier discipline, does not rely on it, and would not benefit from it for scope correctness. The system's invariant is: each document ISA is a distinct node in the granfilade, and `fetchorglgr`'s exact-equality gate ensures `deletend` never crosses document boundaries regardless of how emitter addresses are structured.
