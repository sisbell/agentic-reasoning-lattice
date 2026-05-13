## Question 2 [evidence]

> Does `docreatelink` (and the chain through `findisatoinsertmolecule`) require the document parameter to refer to a document that has been previously created in the granfilade, or will it allocate a link address under any structurally valid document-level tumbler prefix?

## KB Synthesis

## Answer

The allocation in `findisatoinsertmolecule` is purely arithmetic — it does **not** require the document to have been previously created in the granfilade.

### How the allocation works

From [SS-ADDRESS-ALLOC] (Finding 0065), MAKELINK allocates link I-addresses by:
1. Setting `upperbound = docISA.2.3` (bounding the search to the document's link subspace)
2. Calling `findpreviousisagr` to find the highest existing link address below that bound
3. If nothing found (`lowerbound < docISA.2.2`): allocate at `docISA.2.2.1`
4. Otherwise: increment from the highest found address

Step 2–4 are pure granfilade tree arithmetic. If no document orgl exists at `docISA`, the search in `[docISA.2.2, docISA.2.3)` simply returns nothing, and the allocator falls through to the first-link case, producing `docISA.2.2.1`. There is no document-existence guard in `findisatoinsertmolecule`.

### Where existence IS checked

The document existence check lives in `docopy`, downstream of the allocation. From [PRE-INSERT] (Finding 0036), `docopy`'s precondition chain includes `findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)`. If the document doesn't exist or isn't open, `findorgl` returns FALSE and the link reference placement into the V-stream is silently dropped.

However, per [EC-RESPONSE-BEFORE-CHECK] (Finding 0050), the success response is sent to the frontend *before* `docreatelink` executes — so a non-existent home document causes a silent no-op from the frontend's perspective, not an error.

### Summary

| Layer | Checks document exists? |
|-------|------------------------|
| `findisatoinsertmolecule` | **No** — pure tree arithmetic |
| `createorglingranf` | **No** — allocates the link orgl unconditionally |
| `docopy` → `findorgl` | **Yes** — but failure is silent (response already sent) |

`findisatoinsertmolecule` will allocate under any structurally valid tumbler prefix. Document existence is enforced only at the V-stream insertion step, and that enforcement is advisory rather than blocking due to the response-before-check pattern in the FEBE protocol.

---

## Code Exploration

---

## Answer

**Yes — `docreatelink` requires the document to have been previously created in the granfilade.** It will not allocate a link address under a structurally valid but unregistered document tumbler prefix. The enforcement is unconditional.

---

### Execution trace

#### 1. `docreatelink` [do1.c:195–221]

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);   /* do1.c:207 */
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)  /* do1.c:209 */
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)         /* do1.c:211 */
  ...
```

`makehint` [do2.c:78–84] populates the hint struct:

```
supertype = DOCUMENT (3)
subtype   = ATOM     (4)
atomtype  = LINKATOM (2)
hintisa   = *docisaptr
```

`ATOM=4`, `LINKATOM=2` are defined at [xanadu.h:143–146].

The entire `docreatelink` is one short-circuit `&&` chain, so if `createorglingranf` returns `FALSE`, nothing else runs.

---

#### 2. `createorglingranf` → `createorglgr` → `findisatoinsertgr` — the enforcement gate

`createorglingranf` [granf1.c:50–55] is a thin wrapper calling `createorglgr` [granf2.c:111–128], which calls `findisatoinsertgr` at line 117:

```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
    return (FALSE);                              /* granf2.c:117-118 */
```

`findisatoinsertgr` [granf2.c:130–156]:

```c
if (hintptr->subtype == ATOM) {                /* granf2.c:135 */
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {
        fprintf (stderr,"nothing at hintisa for atom\n");
        return (FALSE);                         /* granf2.c:137-140 */
    }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr); /* granf2.c:142 */
```

Because the hint has `subtype=ATOM`, this path is always taken for `docreatelink`. The function calls `isaexistsgr` with `hintptr->hintisa = *docisaptr` — the document address passed to `docreatelink`. If the document is absent, `findisatoinsertgr` returns `FALSE` immediately. No alternate path exists.

---

#### 3. `isaexistsgr` — exact-match lookup [granf2.c:244–253]

```c
bool isaexistsgr(typecuc *crumptr, typeisa *isaptr)
{
  typecontext *context, *retrieve();
  bool ret;
    context = retrieve (crumptr, isaptr, WIDTH);    /* granf2.c:249 */
    ret = tumblereq ((tumbler*)&context->totaloffset, isaptr); /* granf2.c:250 */
    contextfree (context);
    return (ret);
}
```

`retrieve` walks the granfilade B-tree to the position of `isaptr`. `tumblereq` then tests **strict equality** between the tree's recorded offset and the requested address. This is not a prefix/range test — it requires the exact tumbler value to be present as a registered `GRANORGL` node. A structurally well-formed tumbler that has never been registered returns `FALSE`.

---

#### 4. `findisatoinsertmolecule` — address allocation only after gate passes [granf2.c:158–181]

Only reached if `isaexistsgr` returned `TRUE`. For `LINKATOM` (`atomtype=2`):

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  /* line 162 */
/* upperbound = docisa.0.0.3 — ceiling of link subspace */

findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);      /* line 164 */
/* lowerbound = last allocated ISA below upperbound */

} else if (hintptr->atomtype == LINKATOM) {                                   /* line 170 */
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
    /* isaptr = docisa.0.0.2 — base of link subspace */
    if (tumblercmp (&lowerbound, isaptr) == LESS)
        tumblerincrement (isaptr, 1, 1, isaptr);    /* first link: docisa.0.0.2.0.1 */
    else
        tumblerincrement (&lowerbound , 0, 1, isaptr); /* next: lowerbound+0.1 */
}
```

For the first link under a document, the allocated address is `docisa.0.0.2.0.1`. For subsequent links, it is the next sequential ISA above the previous link. Neither path bypasses the existence check — allocation is always relative to a confirmed document address.

---

#### 5. `findnextlinkvsa` — secondary document requirement [do2.c:151–167]

After the link ISA is created, `findnextlinkvsa` computes where in the document's V-space the link content will be placed:

```c
(void) doretrievedocvspan (taskptr, docisaptr, &vspan);   /* do2.c:160 */
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);
else
    movetumbler (&vspanreach, vsaptr);
```

`doretrievedocvspan` [do1.c:312–320] calls `findorgl(taskptr, granf, docisaptr, &docorgl, READBERT)` [do1.c:318], which checks `checkforopen` [granf1.c:22]. The return value of `doretrievedocvspan` is cast to `(void)`, so a failure here leaves `vspan` uninitialised. The document must be open in the bert table for this step to behave correctly, though `findnextlinkvsa` always returns `TRUE` regardless.

---

### Conclusion

**`docreatelink` will unconditionally fail if the document ISA has not been previously registered in the granfilade.**

The enforcement point is `findisatoinsertgr` [granf2.c:135–140], which calls `isaexistsgr` [granf2.c:249–250] to verify the document's exact tumbler address exists in the B-tree before proceeding. The hint system's two-path design (`subtype==ATOM` vs. non-ATOM) deliberately encodes this constraint: non-ATOM allocations (`DOCUMENT`, `ACCOUNT`) use `findisatoinsertnonmolecule` and need no parent; ATOM allocations (text, links) use `findisatoinsertmolecule` and require the parent document to be present.

Documents are registered by `docreatenewdocument` [do1.c:234–241] or `docreatenewversion` [do1.c:260–298], both of which call `createorglingranf` with `subtype=DOCUMENT` — a non-ATOM hint that does not require a prior existence check.
