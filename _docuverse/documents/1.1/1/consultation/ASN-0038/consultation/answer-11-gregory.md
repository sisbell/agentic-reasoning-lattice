## Question 11 [gregory]

> Are there different baptism invariants for different hierarchy levels — for instance, do element-level positions follow different rules than the levels above them in the tumbler tree?

## KB Synthesis

Yes. The allocation invariants differ meaningfully between hierarchy levels, driven by different code paths (`findisatoinsertnonmolecule` vs `findisatoinsertmolecule`) and different increment strategies.

## Document-level and above (non-molecules)

Handled by `findisatoinsertnonmolecule` [SS-ADDRESS-ALLOC]. The core invariant is:

**Allocated address = max child under parent + 1, with containment check.**

The depth parameter encodes crossing `.0.` field boundaries [SS-ADDRESS-SPACE Finding 0021]:

| Supertype → Subtype | Depth | Pattern |
|---------------------|-------|---------|
| NODE → NODE | 1 | `1.1.0.1.1`, `1.1.0.1.2` |
| ACCOUNT → DOCUMENT | 2 | `1.1.0.2.0.1`, `1.1.0.2.0.2` |
| DOCUMENT → DOCUMENT (version, owned) | 1 | `1.1.0.1.0.1.1`, `1.1.0.1.0.1.2` |

The containment check is **mandatory** at these levels — Bug 0013 showed that without it, `findpreviousisagr` crosses account boundaries and allocates under the wrong parent [PRE-ADDRESS-ALLOC]. The increment is a truncate-at-depth then increment, producing the next sibling.

## Element level (molecules)

Handled by `findisatoinsertmolecule` [SS-ADDRESS-SPACE Finding 0065, 0061, 0033]. The core invariant is:

**Allocated address = max address in document's element subspace + 0.1.**

The critical difference: instead of a containment check, molecule allocation uses an **explicit upperbound** to pre-scope the search:

```
upperbound = tumblerincrement(docISA, 2, atomtype + 1)
```

For TEXTATOM (=1): upperbound = `docISA.2.2`  
For LINKATOM (=2): upperbound = `docISA.2.3`

This creates independent, non-overlapping sub-namespaces under each document. Text atoms accumulate in `docISA.3.x` (approximately `docISA.2.1+` range before link space), link orgls in `docISA.2.2–2.3`. Because the search is bounded by construction, no containment check is needed — it cannot stray outside the target document's element namespace [SS-ADDRESS-SPACE Finding 0077].

The increment at element level is always `tumblerincrement(&lowerbound, 0, 1, ...)` — increment at position 0 (rightshift=0), producing `+0.1` steps, not sibling-level steps [ST-INSERT Finding 0031].

## Key invariant distinctions

| Level | Allocation function | Boundary enforcement | Increment |
|-------|--------------------|--------------------|-----------|
| Node/account/doc | `findisatoinsertnonmolecule` | Post-search containment check | Truncate-at-depth, +1 |
| Element (text, link) | `findisatoinsertmolecule` | Pre-search upperbound | Position-0 increment (+0.1) |

The formal model therefore cannot use a single `Σ.next` counter or a single allocation rule. It requires two families of functions partitioned by entity kind [SS-ADDRESS-SPACE Finding 0077]:

```
next_doc_addr(granf, parent)     = max_child(granf, parent) + 1
next_content_addr(granf, doc)    = max_iaddr_in_namespace(granf, doc, type) + 0.1
```

The owned-vs-unowned distinction for VERSION adds a third variant: when the creating user doesn't own the source document, the allocation falls back to `ACCOUNT→DOCUMENT` depth=2 behavior rather than `DOCUMENT→DOCUMENT` depth=1, placing the version under the user's account instead of the source document [SS-VERSION-ADDRESS Finding 0068].

---

## Code Exploration

Now I have everything I need to give a complete, fully-cited answer.

---

## Baptism Invariants by Hierarchy Level in udanax-green

**Yes — definitively different rules apply at different hierarchy levels.** The code encodes three distinct baptism regimes, controlled by the `hint` struct and the `depth` variable.

---

### The Hierarchy Type Constants

`backend/xanadu.h:140-146` defines the four levels:

```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4

#define TEXTATOM  1
#define LINKATOM  2
```

This ordered numeric sequence is not cosmetic — the ordering is enforced by `validhint` [do2.c:95-96], which rejects any hint where `subtype < supertype` (you can't go up the hierarchy) or `subtype - supertype > 1` (you can't skip a level). Every address creation call must stay on adjacent rungs of the ladder.

---

### The `makehint` Entry Point

All baptism flows through `makehint` [do2.c:78-84]:

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

The `(supertype, subtype)` pair is the primary dispatch mechanism. Callers in `do1.c` use it to encode what level they are creating at:

| Call site | `(supertype, subtype)` | What is being baptized |
|---|---|---|
| `docreatenewdocument` [do1.c:239] | `(ACCOUNT, DOCUMENT)` | new document under account |
| `docreatenode_or_account` [do1.c:251] | `(NODE, NODE)` | node or account peer |
| `docreatenewversion` [do1.c:271] | `(DOCUMENT, DOCUMENT)` | version sibling within same document |
| `docreatenewversion` [do1.c:275] | `(ACCOUNT, DOCUMENT)` | version in a different account |
| text insert [do1.c:117] | `(DOCUMENT, ATOM, TEXTATOM)` | text content within a document |
| link create [do1.c:180,207] | `(DOCUMENT, ATOM, LINKATOM)` | link object within a document |

---

### Regime 1: NODE / ACCOUNT / DOCUMENT Level — `findisatoinsertnonmolecule`

`granf2.c:203-242` handles all non-ATOM baptisms. The critical variable is `depth`:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```
[granf2.c:209]

- **depth = 1** when `supertype == subtype` (e.g., `NODE→NODE` or `DOCUMENT→DOCUMENT`): the new sibling is placed one tumbler digit to the right of the hint address.
- **depth = 2** when crossing a boundary (e.g., `ACCOUNT→DOCUMENT`): two digits of separation are interposed.

The **first child** case:
```c
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
```
[granf2.c:237]

This uses `tumblerincrement`'s `rightshift` parameter [tumble.c:599-622] to place the new digit exactly `depth` positions to the right of the last significant digit of the parent address:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    // ...
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify (cptr);
}
```

So `ACCOUNT → first DOCUMENT` yields `accountaddr.0.0.1` (depth=2 zeros inserted), while `DOCUMENT → first VERSION` yields `docaddr.0.1` (depth=1).

The **subsequent sibling** case:
```c
tumblertruncate (&lowerbound, hintlength + depth, isaptr);
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
```
[granf2.c:239-240]

This truncates the previous sibling's address to `hintlength + depth` digits, then increments either at position `depth` (if truncation landed exactly at the parent boundary) or at position 0 (last digit). The depth value is thus baked into the truncation length — siblings one level apart are always exactly `depth` digits deeper than their parent.

---

### Regime 2: ATOM Level — `findisatoinsertmolecule`

`granf2.c:158-181` handles ATOM baptism. It does **not** use `depth` at all. Instead, `atomtype` (TEXTATOM=1, LINKATOM=2) drives different increment strategies.

**Boundary condition** first — the parent document must already exist:
```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {
        return (FALSE);  // no parent document, no atom address
    }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
```
[granf2.c:135-142]

This guard has no analogue at the non-atom levels. Only ATOM baptism requires an existing parent to be validated before address generation proceeds.

Inside `findisatoinsertmolecule`:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
```
[granf2.c:162]

The upper bound search is set 2 positions to the right, with value `atomtype + 1` (TEXTATOM=2, LINKATOM=3). This is a different offset than either `depth=1` or `depth=2`.

When the lower bound matches the parent's length exactly (same-level sibling found):
```c
tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);  // position 2 right, value=atomtype
tumblerincrement (isaptr, 1, 1, isaptr);                        // then one more right
```
[granf2.c:166-167]

When no same-level atom exists yet, **TEXTATOM** and **LINKATOM** diverge further:

- **TEXTATOM**: `tumblerincrement (&lowerbound, 0, 1, isaptr)` [line 169] — simple increment of the last digit
- **LINKATOM**: `tumblerincrement (&hintptr->hintisa, 2, 2, isaptr)` [line 171] — jump 2 positions right with value 2, then conditionally add one more

These are structurally different from each other and from either non-atom regime. **Text content and link objects receive addresses via different algorithms even though both are ATOM-level entities.**

---

### Regime 3: Character / Byte Position — Sequential Increment

Within a text atom, individual characters are positioned purely sequentially — no search, no hint lookup:

```c
insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
tumblerincrement (&lsa, 0, textset->length, &lsa);
```
[granf2.c:99-100]

`rightshift=0` means increment the last (rightmost) significant digit by `textset->length`. This is flat sequential addressing with no structural depth computation whatsoever — the character stream is a raw linear span within the atom's location.

---

### The Account Boundary Invariant

`tumbleraccounteq` [tumble.c:38-70] enforces a cross-cutting structural invariant that applies regardless of which regime minted an address:

```c
for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
        if (++j_b == 2) {
            return(TRUE);  // second zero: account boundary exhausted, document is contained
        }
        // first zero: document may continue with any digit
    } else {
        if (aptr->mantissa[i] != bptr->mantissa[i]) {
            return(FALSE);  // non-zero mismatch: definitely a different account
        }
    }
}
```

Account addresses terminate with a **double-zero suffix**. Any document or atom address that was correctly baptized under that account must be a numeric extension of the account's prefix. This invariant spans all hierarchy levels — it is the containment constraint that makes the tumbler tree coherent across levels, not a per-level rule, but a universal prefix-containment rule enforced at query time.

---

### The `levelpush` Non-Invariant

`levelpush` [genf.c:263-294] reorganizes the enfilade tree when a level fills up, but crucially **preserves all existing addresses unchanged**:

```c
new = createcrum(fullcrumptr->height, fullcrumptr->cenftype);
transferloaf(fullcrumptr, new);  // move children
fullcrumptr->height++;
adopt((typecorecrum*)new, SON, (typecorecrum*)fullcrumptr);
```

The old children and their addresses are simply moved to a new intermediate node. No re-baptism occurs. `levelpull` [genf.c:318-342] is entirely stubbed out (`return(0)`).

---

### Summary

| Hierarchy level | Entry function | Key variable | Increment position | Requiresparent check? |
|---|---|---|---|---|
| NODE → NODE, DOCUMENT → DOCUMENT | `findisatoinsertnonmolecule` | `depth = 1` | rightshift = 1 | No |
| ACCOUNT → DOCUMENT, DOCUMENT → DOCUMENT (cross-account) | `findisatoinsertnonmolecule` | `depth = 2` | rightshift = 2 | No |
| DOCUMENT → TEXTATOM | `findisatoinsertmolecule` | `atomtype = 1` | rightshift = 0 or 2 | Yes — `isaexistsgr` |
| DOCUMENT → LINKATOM | `findisatoinsertmolecule` | `atomtype = 2` | rightshift = 1 or 2 | Yes — `isaexistsgr` |
| Characters within text | `inserttextgr` direct | `textset->length` | rightshift = 0 always | No (sequential) |

The `depth` variable is the clearest expression of level-specific baptism logic: it encodes how many tumbler digits must separate a parent address from its children at that level of the hierarchy. `depth=1` for same-level creation, `depth=2` for cross-level creation. Atom-level creation abandons `depth` entirely and switches to `atomtype`-driven logic with a mandatory parent-existence guard that no other level carries.
