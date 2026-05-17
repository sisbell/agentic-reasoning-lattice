## Question 3 [evidence]

> In udanax-green, when a link is retracted or its analogous lifecycle operation invoked, where is the retracting structure homed — at the target link's home document, at a caller-specified document, or at a system-wide location?

## KB Synthesis

The KB is unambiguous: **udanax-green has no link retraction operation**.

[INV-LINK-PERMANENCE] states directly: "There is no DELETELINK operation in the FEBE protocol. Once created, a link exists forever." This is confirmed across Findings 0024, 0029, and 0040.

The only operation that resembles retraction is `DELETEVSPAN(2.x)`, which removes a link's POOM entry from a document's V-stream [SS-THREE-LAYER-MODEL]. That operation is homed at **the document whose POOM is being modified** — typically the link's home document — but it does not delete the link. The link object in I-space and the spanfilade entries remain intact and permanently discoverable [EC-REVERSE-ORPHAN].

Link "retraction" in the semantic sense is impossible by design. The KB contains no entry describing a retracting structure because none exists.

---

## Code Exploration

I now have all the information needed to answer. Here is my full analysis, grounded in the actual source code:

---

## Where the "Retracting Structure" Is Homed in Udanax-Green

### 1. There Is No Retraction Operation in the Codebase

A systematic search across all `.c` and `.h` files in `backend/` returns **zero matches** for `retract`, `endorse`, `Retract`, or `Endorse`. The concept of link retraction — a structure that asserts a prior link is withdrawn — is part of the Xanadu intellectual model but is **not implemented** in udanax-green as shipped.

### 2. The Analogous Lifecycle Operation: `docreatelink`

The closest lifecycle operation is link creation itself. The call chain is:

**`fns.c:100-112`** — FEBE handler `createlink`:
```c
void createlink(typetask *taskptr)
{
  typeisa docisa, linkisa;
  ...
  if (
     getcreatelink (taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
  && docreatelink (taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)){
      putcreatelink (taskptr, &linkisa);
  }
```
The client provides `docisa` — the **caller-specified document** — explicitly. This is the home anchor for everything that follows.

**`do1.c:195-221`** — `docreatelink` implementation:
```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr, typespecset fromspecset, ...)
{
  typehint hint;
  ...
  makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);      // line 207
  return (
       createorglingranf (taskptr, granf, &hint, linkisaptr)  // line 209 — link born under docisaptr
    && tumbler2spanset (taskptr, linkisaptr, &ispanset)        // line 210
    && findnextlinkvsa (taskptr, docisaptr, &linkvsa)          // line 211 — VSA slot in docisaptr
    && docopy (taskptr, docisaptr, &linkvsa, ispanset)         // line 212 — reference placed in docisaptr
    ...
    && insertendsetsinspanf (taskptr, spanf, linkisaptr, ...)  // line 219 — spanf entries keyed on linkisaptr
  );
}
```

### 3. Where the Link Atom Is Homed

**`do1.c:207`**: `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` — the hint encodes the **caller-specified document** (`docisaptr`) as the parent context. `LINKATOM` (value `2`, `xanadu.h:146`) is the atom type.

**`do1.c:209`**: `createorglingranf(taskptr, granf, &hint, linkisaptr)` — the granfilade allocates the link's ISA address (`linkisaptr`) **as a child of `docisaptr`** in the address hierarchy. The link atom is homed at the **caller-specified document**.

### 4. Where the Link Reference Is Placed in Virtual Address Space

**`do2.c:151-167`** — `findnextlinkvsa`:
```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler firstlink;
  tumblerclear (&firstlink);
  tumblerincrement (&firstlink, 0, 2, &firstlink);  // subspace 0.2
  tumblerincrement (&firstlink, 1, 1, &firstlink);  // → 2.1 in link subspace
  ...
  movetumbler (&vspanreach, vsaptr);
}
```
The link's virtual address is placed in the **link subspace** (V-addresses in the 0.x range, specifically beginning at tumbler components `[0:2, 1:1]`) of the **caller-specified document** (`docisaptr`).

**`do1.c:212`**: `docopy(taskptr, docisaptr, &linkvsa, ispanset)` — the link atom's ispan is copied into `docisaptr` at `linkvsa`. The link's existence as a document entity is recorded in the **caller-specified document's** virtual address space.

### 5. Where the Spanfilade Endpoint Index Is Homed

**`spanf1.c:15-54`** — `insertspanf` (called via `insertendsetsinspanf` at `do1.c:219` with `isaptr = linkisaptr`):
```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr, ...)
{
  type2dbottomcruminfo linfo;
  ...
  if (itemid == ISPANID) {
      movetumbler (isaptr, &linfo.homedoc);   // line 29 — homedoc = linkisaptr
  } else if (itemid == SPORGLID) {
      movetumbler (&sporgl->sporgladdress, &linfo.homedoc);  // line 33 — homedoc = sporgl's own address
  } else if (itemid == TEXTID) {
      movetumbler (isaptr, &linfo.homedoc);   // line 42 — homedoc = linkisaptr
  }
  insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
```
Each spanfilade crum (the index entry that maps content spans to the link) has its `homedoc` set to **the link's own ISA** (`linkisaptr`) — not `docisaptr` and not a system-wide location. For cross-document SPORGL items, `homedoc` is the sporgl's own address.

### Summary

| Structure | Homed At |
|-----------|----------|
| Link atom (granfilade node) | **Caller-specified document** (`docisaptr`), via `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` at `do1.c:207` |
| Link VSA reference (in document's virtual space) | **Caller-specified document**, link subspace (0.x), at next available slot computed by `findnextlinkvsa` at `do2.c:151` |
| Spanfilade endpoint index (`homedoc`) | **The link's own ISA** (`linkisaptr`), not the calling document, set at `spanf1.c:29,42` |
| **Retraction structure** | **Does not exist** — no retract/endorse code anywhere in `backend/*.c` or `backend/*.h` |

### Conclusion

The "retracting structure" has no implementation in udanax-green. The analogous lifecycle operation — `docreatelink` — homes the link atom and its virtual address reference at the **caller-specified document** (`docisaptr`). The spanfilade's `homedoc` for endpoint lookup is homed at the **link's own ISA**, not the calling document. There is no system-wide link registry. Link lifecycle is managed entirely through document versioning (`docreatenewversion`, `do1.c:260`) and the BERT open/close table (`bert.c`), not through any explicit retraction structure.
