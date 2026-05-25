## Question 16 [evidence]

> Could CREATENEWVERSION be invoked on a link orgl ISA (e.g., `docISA.0.2.N`) the way it is invoked on a document ISA, given that both are non-molecules allocated via `findisatoinsertnonmolecule`?

## KB Synthesis

The KB is silent on this specific experiment — no finding directly tests calling CREATENEWVERSION with a link orgl ISA. What can be synthesized from existing entries:

---

## 1. The premise needs a correction

The question states link orgls are "non-molecules allocated via `findisatoinsertnonmolecule`." The KB contradicts this.

From [SS-ADDRESS-ALLOC] / Finding 0065:
> "MAKELINK allocates link I-addresses using query-and-increment within a document-bounded region of the global granfilade. The allocation uses the same **`findisatoinsertmolecule`** mechanism as text allocation but with different bounds."

From [SS-ADDRESS-SPACE] / Finding 0077:
> document addresses use `findisatoinsertnonmolecule` (depth 1 or 2); content I-addresses use `findisatoinsertmolecule` (depth 3+)

And from do1.c:211 (cited in [SS-ADDRESS-SPACE] / Finding 0065): `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` — the `LINKATOM` hint routes through the molecule branch.

Link orgls are **molecules** (LINKATOM), not non-molecules. Document orgls and link orgls use different allocation branches despite both going through `createorglingranf`.

---

## 2. What CREATENEWVERSION would actually encounter

Three internal steps, and each has a problem:

**Step 1 — Address allocation** [ST-VERSION-CREATE / Finding 0032, ST-VERSION-OWNERSHIP / Finding 0068]:
The ownership check `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)` examines the ISA. A link orgl ISA like `1.1.0.1.0.1.0.2.1` is under the current user's account, so ownership would likely pass. A version address would be allocated as a child: `1.1.0.1.0.1.0.2.1.1`. This is structurally valid per the tumbler hierarchy — but it places a document-typed orgl under a link-typed orgl's namespace, violating the address layout convention from [SS-ADDRESS-ALLOC] / Finding 0065.

**Step 2 — Content retrieval** [ST-VERSION-CREATE / Finding 0043, SS-VSPAN-VS-VSPANSET / Finding 0035]:
`doretrievedocvspanfoo` delegates to `retrievedocumentpartofvspanpm`, which reads `cdsp.dsas[V]` and `cwid.dsas[V]` from the root crum of the supplied orgl.

A link orgl does NOT have a V-dimension POOM layout like a document. Its internal structure stores endsets at positions 0.1, 0.2, 0.3 accessed via `retrieverestricted` [SS-FOLLOWLINK / Finding 0048]. The V-dimension displacement would be zero or undefined — `retrievedocumentpartofvspanpm` would return an empty vspan (zero width at position 1).

**Step 3 — Copy** [ST-VERSION-CREATE / Finding 0046]:
With a zero-width vspan, `docopyinternal` would copy nothing into the new orgl. The resulting "version" is structurally empty.

---

## 3. Why this differs from a real document version

A document orgl's root crum has a populated V-dimension displacement (`cdsp.dsas[V]` pointing to the text subspace) because INSERT and COPY write into it via `insertpm` [ST-INSERT / Finding 0066]. A link orgl never has text inserted through that path — links are created via `docreatelink` which writes the link ISA into the *document's* POOM at V-position 2.x, not into the link orgl's V-dimension [SS-DUAL-ENFILADE / Finding 0009, ST-CREATE-LINK / Finding 0012].

The "content" of a link orgl — its FROM/TO/TYPE endsets — is stored at I-space positions 0.1, 0.2, 0.3 internal to the orgl, inaccessible to `retrievedocumentpartofvspanpm`, which only reads V-dimension fields [SS-FOLLOWLINK / Finding 0048].

---

## Summary

Not answerable with full confidence from the KB — no finding directly tests this path. Based on synthesis:

- The premise that link orgls use `findisatoinsertnonmolecule` is **incorrect per the KB** [SS-ADDRESS-ALLOC / Finding 0065].
- If CREATENEWVERSION were called on a link orgl ISA, it would likely **succeed without crashing** (ownership check passes, address allocation proceeds), but would produce an **empty document** at a semantically anomalous address (a document-typed orgl child of a link-typed orgl), because `retrievedocumentpartofvspanpm` finds no V-dimension content in a link orgl's root crum [ST-VERSION-CREATE / Findings 0043, 0046].
- The link's actual endsets (FROM/TO/TYPE) would **not be copied** into the version, since they are inaccessible to the V-span retrieval path used by CREATENEWVERSION.

---

## Code Exploration

I now have everything needed. Let me compile the full answer.

---

## Can CREATENEWVERSION Be Invoked on a Link Orgl ISA?

**Short answer: No — and the premise of the question contains a factual error.**

The question assumes link orgls and document orgls are both non-molecules allocated via `findisatoinsertnonmolecule`. This is incorrect. They live in different subspaces and are allocated by different code paths.

---

### 1. The Premise Is Wrong: Link Orgls Are Molecules

The routing in `findisatoinsertgr` [granf2.c:130–156] decides allocation path based on `hint.subtype`:

```c
if (hintptr->subtype == ATOM) {
    findisatoinsertmolecule(fullcrumptr, hintptr, isaptr);  // links, text
} else {
    findisatoinsertnonmolecule(fullcrumptr, hintptr, isaptr); // documents
}
```

**Document orgls** — `docreatenewdocument` [do1.c:187]:
```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
```
`subtype == DOCUMENT ≠ ATOM` → routes to `findisatoinsertnonmolecule`.

**Link orgls** — `docreatelink` [do1.c:168]:
```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
```
`subtype == ATOM` → routes to `findisatoinsertmolecule` [granf2.c:142].

`findisatoinsertmolecule` [granf2.c:170–175] places link orgls at:
```c
tumblerincrement(&hintptr->hintisa, 2, 2, isaptr);   // docISA.0.2
tumblerincrement(isaptr, 1, 1, isaptr);               // docISA.0.2.1
```
yielding `docISA.0.2.N` — inside the molecule/atom subspace, three components deeper than the document ISA, **not** in the non-molecule hierarchy.

---

### 2. What Actually Happens If You Try

Tracing `docreatenewversion(taskptr, linkISA, linkISA, newISA)` — as called from `fns.c:296`:

```c
docreatenewversion(taskptr, &originaldocisa, &originaldocisa, &newdocisa)
```

#### Gate 1 — Ownership check [do1.c:270]

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);
```

- `tumbleraccounteq(linkISA, linkISA)` → trivially TRUE  
- `isthisusersdocument(linkISA)` [be.c:171–175] calls `tumbleraccounteq(linkISA, &account)` — TRUE because a link ISA shares the account prefix with all user documents [tumble.c:38–54]

**Both conditions pass.** The hint becomes `(DOCUMENT, DOCUMENT, 0, linkISA)`.

#### Gate 2 — New ISA allocation [do1.c:217]

```c
createorglingranf(taskptr, granf, &hint, newisaptr)
```

→ `createorglgr` → `findisatoinsertgr` → `findisatoinsertnonmolecule` (since `hint.subtype == DOCUMENT ≠ ATOM`).

In `findisatoinsertnonmolecule` [granf2.c:203–242] with `hintisa = linkISA`:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
// DOCUMENT == DOCUMENT → depth = 1

tumblerincrement(&hintptr->hintisa, depth - 1, 1, &upperbound);
// upperbound = linkISA incremented at position 0

findpreviousisagr(fullcrumptr, &upperbound, &lowerbound);
// finds highest granfilade entry below upperbound — likely linkISA itself
```

Since `linkISA` exists in the granfilade, `lowerbound = linkISA`, `lowerbound_under_hint = TRUE`, and the computed new ISA is `linkISA` truncated to `hintlength + 1` components then incremented — **placing a new GRANORGL node inside the molecule subspace**, at an address that conflicts with the contiguous text/link atom layout. This is structural corruption of the granfilade.

#### Gate 3 — Retrieve source vspan [do1.c:221–222]

```c
if (!doretrievedocvspanfoo(taskptr, isaptr, &vspan)) {
    return FALSE;
}
```

`doretrievedocvspanfoo` [do1.c:241–249]:
```c
findorgl(taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)
&& retrievedocumentpartofvspanpm(taskptr, docorgl, vspanptr)
```

- `checkforopen(linkISA, NOBERTREQUIRED, user)` [bert.c:59–61] → early return `1` — **NOBERTREQUIRED bypasses all bert checks**
- `fetchorglgr` finds the link orgl in the granfilade — **succeeds**

Then `retrievedocumentpartofvspanpm` [orglinks.c:155–162]:
```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler(&((typecuc *)orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler(&((typecuc *)orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);  // always succeeds
}
```

This **always returns TRUE** — it blindly reads the link orgl root's V-span `cdsp.dsas[V]` and `cwid.dsas[V]`. For a link orgl, these reflect the cumulative V-extent of the endpoint sets stored via `insertpm` at VSAs `1.1`, `2.1`, `3.1` (from/to/three). These are endpoint addresses, not document content positions. The vspan is meaningless as a copy source.

#### Gate 4 — Copy content [do1.c:232–235]

```c
addtoopen(newisaptr, user, TRUE, WRITEBERT);
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
logbertmodified(newisaptr, user);
doclose(taskptr, newisaptr, user);
```

`docopyinternal` constructs `vspec.docisa = linkISA`, then calls `specset2ispanset(taskptr, &vspec, &ispanset, NOBERTREQUIRED)` [do2.c:14–45], which calls `findorgl(granf, &linkISA, NOBERTREQUIRED)` (succeeds) then `vspanset2ispanset` — trying to interpret the link's endpoint V-span as document content. The result is either garbage ispans or an empty set, and the "new version" ends up with incoherent or empty content.

---

### 3. The Structural Reason It Cannot Work

The granfilade address space is partitioned into two non-overlapping subspaces:

| Subspace | Addresses | Allocated by |
|---|---|---|
| Non-molecule (accounts, docs) | sparse, depth 2, 4, 6… | `findisatoinsertnonmolecule` |
| Molecule (text, link orgls) | dense, depth = docDepth+3 | `findisatoinsertmolecule` |

A link ISA like `docISA.0.2.N` sits in the molecule subspace. Passing it as `hintisa` to `makehint(DOCUMENT, DOCUMENT, 0, ...)` instructs `findisatoinsertnonmolecule` to find the "next non-molecule sibling" of a molecule-space address — a category error. The allocated new ISA lands inside the molecule subspace, corrupting the granfilade's structural invariant that orgls live only at non-molecule addresses.

Additionally, `retrievedocumentpartofvspanpm` [orglinks.c:155–162] does not fail on a link orgl — it unconditionally returns TRUE — but it reads the wrong data: the V-extent of link endpoint sets, not a document content span. This silently produces a bad vspan that propagates through `docopyinternal` as garbage.

**Key observation:** `docreatelink` itself deliberately avoids the bert system when accessing the link orgl it just created [do1.c:171]:
```c
&& findorgl(taskptr, granf, linkisaptr, &link, /*WRITEBERT ECH 7-1*/NOBERTREQUIRED)
```
The comment marks this as a specific design decision. Link orgls are never registered with bert; they are write-accessed without BERT tracking. `CREATENEWVERSION` presupposes bert-tracked document ownership semantics that link orgls entirely lack.

---

### Summary

`CREATENEWVERSION` on a link orgl ISA:

1. **Passes gates 1 and 3 without crashing** — the bert bypass (`NOBERTREQUIRED`) and the always-TRUE `retrievedocumentpartofvspanpm` allow execution to continue.
2. **Silently corrupts the granfilade at gate 2** — `findisatoinsertnonmolecule` allocates a new GRANORGL node inside the molecule subspace, where document-level orgls must not exist.
3. **Produces incoherent content at gate 4** — the vspan from the link orgl's root contains endpoint VSAs, not content positions; what gets copied is the link's endpoint structure misread as document content.
4. **The premise is factually wrong** — link orgls are molecules allocated by `findisatoinsertmolecule` [granf2.c:142], not `findisatoinsertnonmolecule`. The two live in categorically distinct address subspaces.
