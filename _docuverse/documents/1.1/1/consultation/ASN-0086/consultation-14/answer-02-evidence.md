## Question 2 [evidence]

> In udanax-green's link-emission path (`docreatelink`, `findisatoinsertmolecule`), how is the home document for a new link determined — explicit parameter, derived from current context, or allocator-chosen — and is this choice exposed at the operation's call interface?

## KB Synthesis

## Home Document Determination in `docreatelink`

The home document is an **explicit caller-supplied parameter**, fully exposed at every layer of the call interface.

**Call interface:** `create_link(home_doc, source_specs, target_specs, type_specs)` takes the home document as its first argument. `docreatelink` at `do1.c:199-225` receives it as `docisaptr`. [SS-LINK-HOME-DOCUMENT]

**Hint construction:** At `do1.c:211`, `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` encodes the home document ISA into the allocator hint. The hint sets both the allocation depth and the parent address. [SS-ADDRESS-SPACE, Finding 0065]

**Allocator use:** `findisatoinsertmolecule` (called via `createorglingranf`) uses the hint ISA to compute `upperbound = tumblerincrement(docISA, 2, LINKATOM+1)`, bounding the granfilade search to `docISA.2.x`. The new link I-address is allocated as `max_existing_link_in_doc + 0.1`, or `docISA.2.2.1` if no links exist yet. [SS-ADDRESS-ALLOC, Finding 0065]

**Result:** The link's I-address is scoped per-document — Document A's links live at `docA.0.2.1`, `docA.0.2.2`, ..., independent of Document B's counter. [SS-LINK-HOME-DOCUMENT]

The allocator makes no autonomous choice: it derives the allocation namespace entirely from the `docisaptr` parameter passed down from the top-level `create_link` call.

---

## Code Exploration

I have all I need to give a complete, cited answer.

---

## How the Home Document for a New Link Is Determined

### The Call Chain

```
createlink()       [fns.c:100]
  → docreatelink() [do1.c:195]
      → makehint() [do2.c:78]
      → createorglingranf() → findisatoinsertgr() [granf2.c:130]
                               → findisatoinsertmolecule() [granf2.c:158]
      → findnextlinkvsa()   [do2.c:151]
      → docopy()            [do1.c:212]
```

---

### 1. The FEBE Handler: `createlink()` — `fns.c:100-112`

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

`getcreatelink` reads `docisa` **off the wire** — it is an explicit, caller-supplied parameter. No context is inferred; no default is chosen. The home document is chosen by the client at protocol level before any backend logic runs.

---

### 2. `docreatelink()` — `do1.c:195-221`

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr, typespecset fromspecset,
                  typespecset tospecset, typespecset threespecset, typeisa *linkisaptr)
{
  typehint hint;
  tumbler linkvsa, fromvsa, tovsa, threevsa;
  ...
    makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);   // line 207
    return (
         createorglingranf (taskptr, granf, &hint, linkisaptr)  // line 209
      && tumbler2spanset (taskptr, linkisaptr, &ispanset)
      && findnextlinkvsa (taskptr, docisaptr, &linkvsa)          // line 211
      && docopy (taskptr, docisaptr, &linkvsa, ispanset)         // line 212
      ...
    );
}
```

`docisaptr` is used in **two distinct roles** here:

- **As the address-space owner:** `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` packages it as `hint.hintisa`, pointing the granfilade allocator at this document's subtree.
- **As the POOM insertion target:** `findnextlinkvsa(taskptr, docisaptr, &linkvsa)` and `docopy(taskptr, docisaptr, &linkvsa, ispanset)` insert the link's ISA reference into this document's version-address space.

---

### 3. `makehint()` — `do2.c:78-84`

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);   // line 83
}
```

`docisa` is copied verbatim into `hint.hintisa`. The allocator receives the home document's tumbler address as its only placement guidance.

---

### 4. `findisatoinsertgr()` — `granf2.c:130-156`

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {
            ...
            return (FALSE);
        }
        findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);  // line 142
    } else {
        findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
    }
    tumblerjustify(isaptr);
    return (TRUE);
}
```

Because `subtype == ATOM` (links are ATOM-level objects), the allocator dispatches to `findisatoinsertmolecule`. Critically, it **first checks that `hintisa` (= `docisa`) already exists** in the granfilade — the home document must pre-exist.

---

### 5. `findisatoinsertmolecule()` — `granf2.c:158-181`

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // line 162
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);     // line 164
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement (isaptr, 1, 1, isaptr);
    } else if (hintptr->atomtype == TEXTATOM) {
        ...
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);                       // line 171
        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);                              // line 173
        else
            tumblerincrement (&lowerbound , 0, 1, isaptr);                        // line 175
    }
}
```

For a link (`LINKATOM == 2`):
- `upperbound = hintisa.0.3` (depth-2 increment by `atomtype+1 = 3`)
- The allocator searches for the highest existing ISA below that bound
- The new link gets `hintisa.0.2` if the space is empty, or `previous + 1` sequentially

The allocator **determines only the specific address within the home document's subspace**. The home document itself (`hintptr->hintisa`) was fixed by the caller. The allocator has no freedom to choose a different document.

---

### 6. `findnextlinkvsa()` — `do2.c:151-167`

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);   // firstlink = 2
    tumblerincrement (&firstlink, 1, 1, &firstlink);   // firstlink = 2.1

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);
    else
        movetumbler (&vspanreach, vsaptr);
    return (TRUE);
}
```

This computes the next available V-address in `docisaptr`'s version space. The minimum is `2.1` (the link subspace begins at V=2, text at V=1). Again, `docisaptr` is the only input that controls which document's V-space is used.

---

## Summary

| Question | Answer |
|---|---|
| **How is the home document determined?** | It is an **explicit parameter** supplied by the client over FEBE, read by `getcreatelink` and passed as `docisaptr` down the entire call chain |
| **Is context used?** | No. There is no implicit "current document." The only guard is that `findisatoinsertgr` (granf2.c:136) checks the document **exists** before allocating under it |
| **Is the allocator free to choose?** | No. `findisatoinsertmolecule` allocates the link's ISA **within** the home document's address subspace (`docisa.0.2`, `.0.3`, etc.), but which document that is has already been fixed |
| **Is this exposed at the call interface?** | Yes, fully. `docisa` is a required argument at the FEBE protocol level (`fns.c:107`), at the `docreatelink` function signature (`do1.c:195`), and at every internal call that uses it — nothing is hidden or defaulted |

The architecture is unambiguous: the client chooses the home document; the allocator (`findisatoinsertmolecule`) only decides the sequential position within that document's link subspace.
