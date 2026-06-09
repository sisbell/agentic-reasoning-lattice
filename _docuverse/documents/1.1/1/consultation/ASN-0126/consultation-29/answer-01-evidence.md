## Question 1 [evidence]

> Does udanax-green's delete/retraction path carry an attributing source span, or does it emit retractions with no from-set?

## KB Synthesis

The KB describes no "from-set" or attributing source span on the delete path. DELETEVSPAN carries exactly two parameters: the target document ISA and a vspan (start + width). Nothing more.

The relevant evidence:

**Operation signature** — [ST-REMOVE] (Finding 0006) says deletion uses FEBE command 12 "which takes a vspan (start address + width offset)" and "This is the correct and only mechanism for removing content from a document." No source attribution parameter is described anywhere.

**Implementation** — [ST-DELETE] (Finding 0057) traces the call path as `dodeletevspan` → `deletevspanpm` → `deletend`, with `logbertmodified` as the only side effect. There is no call to any spanf function and no record of what was deleted.

**Spanfilade is untouched** — [INV-SPANF-WRITE-ONLY] confirms DELETE makes no spanfilade entry whatsoever. If there were a from-set, you'd expect an index entry recording the retraction; none is created.

**No inverse exists** — [INV-DELETE-NOT-INVERSE] explicitly notes that DELETE+INSERT of identical text does not restore identity because no information about the retracted content is preserved in any index.

In short: udanax-green's delete path emits retractions with no from-set. It is a pure V-space positional operation — document plus vspan — with no attribution, no source recording, and no spanfilade side effect.

---

## Code Exploration

I now have the complete picture across all layers. Here is the full answer.

---

## Does `DELETEVSPAN` carry an attributing source span (from-set)?

**No. The delete/retraction path carries no from-set at any level — not in the protocol, not in the response, and not in the internal implementation.**

---

### Full call chain, with citations

#### 1. FEBE protocol input — `get1.c:162–171`

```c
bool getdeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    prompt(taskptr, "document=> ");
    if (!getisa(taskptr, docisaptr)) return (FALSE);
    prompt(taskptr, "delete this part\n");
    if (!getspan(taskptr, vspanptr, VSPANID)) return (FALSE);
    return (TRUE);
}
```

The parser reads exactly **two fields** off the wire:
- `docisaptr` — the document tumbler (which document to edit)
- `vspanptr` — the virtual span to delete (`stream` = V-origin, `width` = V-width)

There is no from-set field. There is no I-span parameter. The protocol message `DELETEVSPAN` (opcode 12, `requests.h:29`) structurally cannot carry attribution.

---

#### 2. FEBE protocol output — `putfe.c:316–319`

```c
int putdeletevspan(typetask *taskptr)
{
    putnumber(taskptr->outp, DELETEVSPAN);
}
```

The response is a bare opcode acknowledgment — **no payload whatsoever**. No from-set is returned to the client. Compare this with `putcreatelink` (which returns a `linkisa`) or `putcreatenewversion` (which returns a `newdocisa`): `putdeletevspan` has an entirely empty body.

---

#### 3. Top-level handler — `fns.c:333–347`

```c
void deletevspan(typetask *taskptr)
{
    typeisa docisa;
    typespan vspan;
    (void) getdeletevspan(taskptr, &docisa, &vspan);
    putdeletevspan(taskptr);                          /* ACK before the work */
    if (!dodeletevspan(taskptr, &docisa, &vspan))
        ...
}
```

Note: the acknowledgment is sent *before* `dodeletevspan` executes (fire-and-forget pattern used for non-critical ops). Only `docisa` and `vspan` are threaded through. No I-span is resolved at this layer.

---

#### 4. Domain logic — `do1.c:158–167`

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    typeorgl docorgl;
    return (
       findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

`findorgl` resolves the document ISA to its POOM root (`docorgl`). Only the POOM handle and the V-span are passed on. There is no call to convert the V-span to I-span here, and no I-span is produced.

---

#### 5. POOM edit — `orglinks.c:145–152`

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

This is the innermost delete function. It calls `deletend` with:
- `&vspanptr->stream` — V-origin tumbler
- `&vspanptr->width` — V-width tumbler
- `V` — the V-axis index

**No V→I permutation is performed before the delete.** The I-space identity of the content being removed is never resolved; the I-span is never computed, stored, logged, or emitted.

---

#### 6. Tree surgery — `edit.c:31–76`

```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    ...
    makecutsnd(fullcrumptr, &knives);           /* cut at origin and origin+width */
    newfindintersectionnd(fullcrumptr, &knives, &father, &foffset);
    for (ptr = findleftson(father); ptr; ptr = next) {
        next = findrightbro((typecorecrum*)ptr);
        switch (deletecutsectionnd(...)) {
          case 1:
            disown((typecorecrum*)ptr);         /* remove crum from tree */
            subtreefree((typecorecrum*)ptr);    /* free its storage */
            break;
          case 2:
            tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
            break;
        }
    }
    setwispupwards(father, 1);
    recombine(father);
}
```

`deletend` cuts the POOM tree at the V-origin and V-origin+width, then walks the children of the cut node:
- Crums fully inside the deleted range are `disown`ed and `subtreefree`d — **their I-space content (`cdsp.dsas[I]`) is silently discarded**
- Crums that straddle the boundary have their V-displacement adjusted

At no point is `cdsp.dsas[I]` (the I-axis address stored in each crum) read, returned, or recorded during the delete. The I-space half of the mapping simply disappears.

---

### What this means architecturally

The delete operation is a **pure V-space edit** of the POOM (permutation matrix enfilade). The POOM maps V-addresses → I-addresses (permascroll locations). Deleting a V-span removes POOM entries in that V-range, which hides the corresponding permascroll content from that document version. But:

1. The permascroll content itself is never touched — granfilade content is append-only and permanent.
2. The system makes no record of *which* I-spans were retracted. The V→I lookup that would reveal this (via `permute` / `vspanset2ispanset` in `orglinks.c`) is never invoked during delete.
3. The response is an empty opcode acknowledgment — no from-set is returned to the caller.

**The DELETEVSPAN operation emits retractions with no from-set.** The attributing source span of deleted content is unrecoverable from the delete operation itself. A client wishing to know "what was removed" would need to call `retrievev` *before* the delete and record the result independently.
