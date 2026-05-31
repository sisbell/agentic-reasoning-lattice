## Question 1 [evidence]

> Does `docreatelink`/`findisatoinsertmolecule` allocate every link homed in a given document through a single shared allocator (one I-stream/enfilade), so all such links descend from one `inc(home, 2)` child-spawn and diverge only at sibling-ordinal advances?

## KB Synthesis

Yes — all links homed in a given document are allocated through a single, stateless query-and-increment allocator bounded to one subtree of the global granfilade.

## Mechanism

From `[SS-ADDRESS-ALLOC]` Finding 0065:

1. `findisatoinsertmolecule` computes `upperbound = tumblerincrement(docISA, 2, LINKATOM+1)`, which bounds the search to `docISA.2.3` — the exclusive upper limit of the document's link element field.
2. `findpreviousisagr` scans the granfilade tree for the highest existing I-address strictly below that bound.
3. If nothing exists yet (`lowerbound < docISA.2.2`), the first link is placed at `docISA.0.2.1`.
4. Otherwise, the result is `max_existing + 0.1` — a monotone increment by one sibling ordinal.

The concrete address structure (`[SS-ADDRESS-SPACE]` Finding 0065):
```
Document A = 1.1.0.1.0.1
Link 1:      1.1.0.1.0.1.0.2.1
Link 2:      1.1.0.1.0.1.0.2.2
Link 3:      1.1.0.1.0.1.0.2.3
```

All siblings under `docISA.0.2`, differing only in the final ordinal.

## Single Allocator, Document-Scoped

There is no per-document counter object — the allocator is a pure function of the granfilade's current state (`[SS-ADDRESS-ALLOC]` Finding 0061): `next_link_addr(D) = max_child(granf, D.0.2.*) + 0.1`. Every `findisatoinsertmolecule` call for document D queries the same subtree, so all link allocations for D compete through and advance the same cursor.

## Cross-Document Independence

From `[SS-ADDRESS-SPACE]` Finding 0065 and `[INV-MONOTONIC]`: allocations for document B (`B.0.2.N`) and document A (`A.0.2.N`) use different subtree bounds and never interfere. Each document has its own `N`-sequence restarting at 1.

## One Caveat

The global granfilade is shared (`[SS-ADDRESS-SPACE]` Finding 0077): while link allocations for different documents are scoped independently, they all live in the same tree. Creating a link in document A (`[ST-INSERT]` / `[INT-LINK-INSERT]` Finding 0063) advances the granfilade maximum within `A.0.2.*`, which has no effect on `B.0.2.*`'s maximum — the subtree bounds isolate them.

**Summary:** Yes — one shared allocator per home document, implemented as stateless query-and-increment over the `docISA.0.2.*` subtree of the global granfilade, producing strictly monotone sibling ordinals `docISA.0.2.1, 0.2.2, 0.2.3, ...` with no cross-document interference.

---

## Code Exploration

Now I have everything I need for a complete, verified answer.

---

## Answer: Link Allocation per Home Document in udanax-green

**Short answer: Yes — with one important precision about the child ordinal.**

All links homed in a given document are allocated through the single process-wide granfilade (`granf`), all descend from a first allocation at `inc(home, 2, LINKATOM)` = `inc(home, 2, 2)`, and successive allocations diverge via sibling-ordinal advances at that same depth. Here is the full code trace.

---

### 1. One Global Granfilade for Everything

`backend/corediskout.c:21`:
```c
typegranf granf;
```
`backend/xanadu.h:14`:
```c
extern typegranf granf;
```

There is **no per-document granfilade**. The single `granf` holds addresses for all documents, text atoms, and link atoms across the entire system. Document identity is imposed by the hint mechanism, not by separate allocators.

---

### 2. `docreatelink` Embeds Home Before Calling the Allocator

`do1.c:207–209`:
```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)
  ...
```

`makehint` fills `hint.hintisa = *docisaptr`, `hint.subtype = ATOM`, `hint.atomtype = LINKATOM`. The home document address is thus baked into the hint before the allocator is called; `granf` is the global singleton.

---

### 3. Dispatch: `findisatoinsertgr` Routes All ATOMs to `findisatoinsertmolecule`

`granf2.c:130–156`:
```c
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
```

Both TEXTATOM and LINKATOM go through `findisatoinsertmolecule`. The guard at line 136 first confirms the home document exists in the granf; if not, allocation is refused.

---

### 4. `findisatoinsertmolecule`: The Address Derivation Logic

`granf2.c:158–181` (full function):

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // line 162
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);      // line 164
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {        // line 165
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);              // line 166
        tumblerincrement (isaptr, 1, 1, isaptr);                                   // line 167
    } else if (hintptr->atomtype == TEXTATOM) {
            tumblerincrement (&lowerbound, 0, 1, isaptr);
    } else if (hintptr->atomtype == LINKATOM) {                                    // line 170
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);                        // line 171
        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);                               // line 173
        else
            tumblerincrement (&lowerbound , 0, 1, isaptr);                         // line 175
    }
}
```

**Working through the two cases for `LINKATOM = 2` (`xanadu.h:146`):**

**Upper-bound calculation (line 162):**
`upperbound = inc(home, 2, atomtype+1) = inc(home, 2, 3)`
This bounds the `findpreviousisagr` search to addresses strictly below the 3-child of home at depth 2 — i.e., within the home document's LINKATOM address family.

**Case A — first link ever in this document** (`else if LINKATOM` branch, lines 170–175):

`tumblerlength(hintisa) != tumblerlength(lowerbound)` — the search found nothing at the same nesting depth.

```
isa = inc(home, 2, 2)         // line 171: the 2-child of home at depth 2
```
If `lowerbound < isa` (nothing collides):
```
isa = inc(isa, 1, 1)          // line 173: bump generation sub-digit
```

**This is the single child-spawn:** every first LINKATOM for a home document is rooted at `inc(home, 2, 2)`.

**Case B — subsequent links** (`if tumblerlength` branch, lines 165–167):

`tumblerlength(hintisa) == tumblerlength(lowerbound)` — we found a prior link at the same nesting level (meaning `lowerbound` is a previously allocated link address for this home).

```
isa = inc(lowerbound, 2, atomtype)   // line 166: advance sibling ordinal by 2 from previous
isa = inc(isa, 1, 1)                  // line 167: bump generation digit
```

Successive links diverge from the immediately prior one at **depth 2, step LINKATOM (=2)** — strictly sibling-ordinal advances within the depth-2 address space of the home document.

---

### 5. Address Space Containment: `findpreviousisagr`

`granf2.c:255–278` — The tree walk that finds the immediately preceding ISA:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{ RECURSIVE
    ...
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);   // line 264: leaf: take last ISA
        return(0);
    }
    for (ptr = findleftson(...); ptr; ptr = findrightbro(ptr)) {
        if (... THRUME ... || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);   // line 272: descend into child
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  // line 275: acc += sibling.width
        }
    }
}
```

Divergence between siblings is created by **`tumbleradd` accumulating each right sibling's width** (line 275). Each link address is the cumulative sum of all prior sibling widths below the upper-bound, guaranteeing uniqueness via ordinal accumulation — exactly sibling-ordinal advances.

---

### 6. Cross-Document Guard: `isanextensionnd`

`insertnd.c:301–306`:
```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
  ...
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);   // line 305–306: refuse if home documents don't match
```

Every bottom crum in the enfilade carries a `homedoc` field (`wisp.h`: `type2dbottomcruminfo`). An append into an existing run is rejected if the home documents differ. This enforces the containment property: link allocations for document A can never bleed into document B's address range, even though both share the global `granf`.

---

### Summary

| Claim | Code Evidence |
|---|---|
| Single shared allocator | `typegranf granf` is a global at `corediskout.c:21`; all calls pass it by name |
| Document home embedded in hint | `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` at `do1.c:207` |
| First link at `inc(home, 2, 2)` | `tumblerincrement(&hintptr->hintisa, 2, 2, isaptr)` at `granf2.c:171` |
| Subsequent links by sibling-ordinal advance | `tumblerincrement(&lowerbound, 2, atomtype, isaptr)` at `granf2.c:166` |
| Address ordering by cumulative sibling width | `tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset)` at `granf2.c:275` |
| Cross-document barrier | `tumblereq` guard at `insertnd.c:305` |

**All links homed in a document descend from a single `inc(home, 2, 2)` child-spawn and diverge at depth-2 sibling-ordinal advances.** The "single allocator" is the process-wide `granf`; scoping per home document is enforced by the hint's upper-bound `inc(home, 2, 3)` passed to `findpreviousisagr`, and by the `homedoc` equality guard in `isanextensionnd`.
