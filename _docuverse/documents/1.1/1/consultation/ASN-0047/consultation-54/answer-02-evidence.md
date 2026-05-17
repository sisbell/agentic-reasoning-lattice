## Question 2 [evidence]

> In udanax-green, are the content sub-allocator and link sub-allocator under a document realized as a single allocator emitting siblings differing in subspace prefix, or as two structurally distinct allocators with disjoint domains and independent frontiers?

## KB Synthesis

## Single Allocator vs. Two Distinct Allocators

The evidence points unambiguously to **two structurally distinct allocators with disjoint domains and independent frontiers**, sharing only the underlying `findpreviousisagr` + increment mechanism operating on different subtrees of the same global granfilade.

---

### Address Domains Are Disjoint

The two allocators produce addresses in non-overlapping tumbler ranges [SS-ADDRESS-SPACE]:

| Entity type | Address pattern | Anchor |
|-------------|----------------|--------|
| Text atoms (permascroll) | `2.1.0.a.0.b.3.n` | Under permascroll node `2.x` |
| Link orgls | `1.1.0.a.0.b.0.2.n` | Under document ISA |

Text I-addresses live under the permascroll (node-2 space); link I-addresses live under the owning document in node-1 space. These subtrees are structurally disjoint [SS-ADDRESS-SPACE Finding 0077].

---

### Independent Upper Bounds Confirm Distinct Frontiers

`findisatoinsertgr` dispatches to separate functions [SS-ADDRESS-SPACE Finding 0077]:

- **Text**: `findisatoinsertmolecule` — searches permascroll subtree, upper bound derived from the molecule context
- **Links**: Same `findisatoinsertmolecule` path but with a *document-scoped* upper bound computed as `tumblerincrement(docISA, 2, atomtype+1)` = `docISA.0.2.3`, bounding the search to the document's link element subspace [SS-ADDRESS-SPACE Finding 0065]

Each allocator searches its own subtree. Finding 0077 makes this explicit: "Both query the same granfilade tree but search **different subtrees**."

---

### Independence Is Directly Confirmed by VERSION Experiment

Finding 0077 provides the decisive test: CREATENEWVERSION allocates a document address via `findisatoinsertnonmolecule` (document subtree), then immediately performs text INSERTs. The resulting text I-addresses are **contiguous** with pre-VERSION inserts — no gap. This proves that crossing the document-address frontier leaves the text-atom frontier untouched [SS-ADDRESS-SPACE Finding 0077].

```
INSERT "ABC"        → I.1, I.2, I.3  (text subtree)
CREATENEWVERSION    → doc address allocated (document subtree) — independent
INSERT "XYZ"        → I.4, I.5, I.6  (text subtree, contiguous)
compare_versions    → 1 shared span pair, width 0.6
```

This contrasts sharply with what CREATELINK does (if Finding 0063's contiguity break is taken at face value), which would imply a shared frontier — but Finding 0065 (Essential) establishes link allocation as also molecule-branch with a document-scoped ceiling, and Finding 0077 categorically states "separate tumbler ranges... allocated independently."

---

### The Finding 0063 Apparent Conflict

Finding 0063 claims CREATELINK breaks text I-address contiguity, implying a shared sequence. This conflicts with:

- [SS-ADDRESS-SPACE Finding 0077]: "Document addresses and content I-addresses occupy **separate tumbler ranges** and are allocated independently."
- [SS-ADDRESS-SPACE Finding 0065]: Link allocation is bounded to `docISA.2.3` — an address under document-space, not permascroll-space.
- The VERSION experiment above.

Finding 0063's simplified notation (`1.1 → 1.2 → 1.3 → ~2 → 2.1`) appears to use abstract shorthand rather than actual tumbler addresses, and the stated interpretation that "link orgls and text characters share the same allocation sequence" is contradicted by the more specific and Essential-rated findings. Finding 0077 explicitly resolves this: "No single global Σ.next counter exists."

---

### Summary

The content and link sub-allocators under a document are **two structurally distinct allocators**:

- **Disjoint domains**: text atoms in the permascroll subtree (`2.x...`), link orgls in the document subtree (`1.x...0.2.n`)
- **Independent frontiers**: each uses `findpreviousisagr` bounded to its own tumbler range; one allocator's activity does not advance the other's frontier
- **Same mechanism, different subtrees**: `findisatoinsertmolecule` is called for both, but with bounds that constrain each search to a non-overlapping region of the global granfilade [SS-ADDRESS-SPACE Findings 0065, 0077]

They are not siblings differing only in a subspace prefix digit; they are anchored to structurally distinct parent nodes in the global granfilade tree.

---

## Code Exploration

I now have all the evidence needed. Here is the complete answer.

---

## Answer: Single Allocator with Sibling Subspace Prefixes

The content sub-allocator and link sub-allocator under a document are **a single granfilade** (`granf`) that emits siblings distinguished by a subspace prefix encoded in the `atomtype` field. There are **no two structurally distinct allocators** — there is one tree with one shared physical structure.

---

### 1. One Granfilade for Everything

There is a single global `granf`:

```c
// xanadu.h:14
extern typegranf granf;
```

Both operations — text insertion and link creation — call into this same tree:

```c
// do1.c:118 — text path
inserttextingranf(taskptr, granf, &hint, textset, &ispanset)

// do1.c:182 — link path
createorglingranf(taskptr, granf, &hint, linkisaptr)
```

The tree is shared. There is no second granfilade for links.

---

### 2. The `typehint` Struct Carries the Discriminant

```c
// xanadu.h:148-153
typedef struct {
    INT supertype;   // container level: NODE(1), ACCOUNT(2), DOCUMENT(3)
    INT subtype;     // content level: ATOM(4)
    INT atomtype;    // subspace discriminant: TEXTATOM(1) or LINKATOM(2)
    typeisa hintisa; // ISA of the containing document
} typehint;
```

The constants are numerically load-bearing — the comment in the source says so explicitly:

```c
// xanadu.h:144-146
                  /* atom types - don't change these */
#define TEXTATOM  1
#define LINKATOM  2
```

The hint is built by `makehint` (`do2.c:78-84`):

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

For text: `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)` [`do1.c:117`] → `atomtype = 1`  
For link: `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` [`do1.c:180, 207`] → `atomtype = 2`

---

### 3. How `atomtype` Becomes the Subspace Prefix

The partitioning happens inside `findisatoinsertmolecule` (`granf2.c:158-181`). This is called by both `inserttextgr` and `createorglgr` via `findisatoinsertgr` (`granf2.c:130-155`).

**Upper-bound computation:**

```c
// granf2.c:162
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
```

`tumblerincrement(T, rightshift=2, value, result)` appends `value` two places below `T`'s last significant digit (`tumble.c:599-621`). So:

- Text (`atomtype=1`): `upperbound = docISA...(+1)=2` at depth+2
- Link (`atomtype=2`): `upperbound = docISA...(+1)=3` at depth+2

These two ranges — `[docISA..1, docISA..2)` and `[docISA..2, docISA..3)` — are **disjoint intervals** within the same granfilade ISA space.

**Address assignment for the first link** (`granf2.c:170-171`):

```c
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
```

The first link atom is placed at `docISA` extended by `2` at depth+2 — i.e., the address literally encodes `LINKATOM=2` as the subspace prefix. The first text atom is placed at `docISA..1` by the `TEXTATOM=1` path (lines 168-169).

Each subsequent allocation in a subspace finds its frontier with:

```c
// granf2.c:164
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

This scans the granfilade for the highest ISA strictly below `upperbound` — independently for each subspace. So each subspace has its own frontier, but they share the same underlying tree and the same `findpreviousisagr` machinery.

---

### 4. Validity Constraint Confirms the Invariant

The `validhint` function (`do2.c:86-108`) enforces the legal range: `atomtype ∈ {0, 1, 2}` where 0 is forbidden when `subtype == ATOM`. This means exactly two atom subspaces are possible under any document, numbered 1 and 2.

---

### Conclusion

The content sub-allocator (text) and link sub-allocator under a document are **one granfilade (`granf`)** with a **single shared tree structure**, emitting ISAs that are siblings at the same depth, differentiated by a single subspace prefix digit: `TEXTATOM=1` → addresses in `[docISA..1, docISA..2)`, `LINKATOM=2` → addresses in `[docISA..2, docISA..3)`.

The domains are disjoint by construction (the search bounds in `findisatoinsertmolecule` guarantee no overlap), and each subspace has an independent high-water frontier tracked by `findpreviousisagr` within its own range. But the allocators share all physical structure: the same granfilade tree, the same crum layout, the same retrieval engine. The discriminant is not a structural division — it is a two-digit numeric prefix embedded into the ISA tumbler by the `atomtype` value, which is why the comment at `xanadu.h:144` says explicitly *"don't change these"*: the integer values are the subspace indices.
