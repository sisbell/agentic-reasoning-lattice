## Question 3 [evidence]

> Does udanax-green's granfilade orgl tree under each document use a single shared depth-1 element-field allocator producing positions that land in either content subspace (s_C) or link subspace (s_L) by their first-element-field value, or does it maintain separate per-subspace allocator trees?

## KB Synthesis

## Single Shared Granfilade Tree with Atomtype-Partitioned Bounds

The granfilade uses a **single shared tree** for both subspaces, not separate per-subspace allocator trees. Both text content and link orgls are allocated through the same `findisatoinsertmolecule` path via `findisatoinsertgr`, differentiated only by the `atomtype` parameter.

### Allocation Mechanism

Both subspaces allocate via stateless query-and-increment [SS-ADDRESS-SPACE, Finding 0061]: `findpreviousisagr` finds the highest existing I-address below an `atomtype`-specific upper bound, then increments by 1.

The upper bound is computed as `tumblerincrement(docISA, 2, atomtype+1)` [SS-ADDRESS-ALLOC, Finding 0065]:

| Subspace | atomtype | atomtype+1 | Upper bound | Element field |
|----------|----------|-----------|-------------|---------------|
| Text (s_C) | TEXTATOM=1 | 2 | `docISA.x.2` | 3 (e.g., `docISA.3.0.1.x`) |
| Link orgls (s_L) | LINKATOM=2 | 3 | `docISA.x.3` | 2 (e.g., `docISA.0.2.x`) |

From Finding 0077's address layout:
```
docISA = 1.1.0.1.0.1
  └── 1.1.0.1.0.1.0.2.1   ← link orgl (s_L, element_field=2)
  └── 1.1.0.1.0.1.3.0.1.1 ← text content (s_C, element_field=3)
```

### It Is Not Separate Per-Subspace Trees

[SS-ADDRESS-SPACE, Finding 0077] states explicitly: *"Both query the same granfilade tree but search different subtrees."* The subtrees are different ranges of the single B-tree, not separate allocator structures.

The most direct evidence that the allocator is shared comes from [INT-LINK-INSERT, Finding 0063]:

> CREATELINK **breaks text I-address contiguity** for subsequent INSERTs. "The formal model must account for a **shared I-address allocator across all granfilade entities**."

This contrasts with CREATENEWVERSION, which uses `findisatoinsertnonmolecule` in a **separate** document-address subtree and does NOT break text contiguity [INV-MONOTONIC, Finding 0077].

### Why CREATELINK Interferes Despite Different Element Fields

The interaction `post(create_link) ⟹ next_text_iaddr > pre(create_link).next_text_iaddr + link_width` [INT-LINK-INSERT] means the link orgl allocation advances the effective high-water mark seen by the text allocator. Both use the same stateless `findpreviousisagr` against the same underlying granfilade tree; the subspace partitioning via different upper bounds provides separate storage positions (element_field 2 vs 3) but not a fully isolated counter [INT-LINK-INSERT, Finding 0063].

### Summary

This is the **single shared depth-1 element-field allocator** model: one granfilade tree, one dispatch function (`findisatoinsertmolecule`), with the subspace (s_C or s_L) determined by first-element-field value (3 for text, 2 for links) produced by the `atomtype` parameter setting different search bounds. Separate per-subspace trees do not exist.

---

## Code Exploration

I now have a complete picture. Let me synthesize the full answer from the source evidence.

---

## Answer

The granfilade uses a **single shared allocator** — not separate per-subspace trees. Here is the full chain of evidence from the C source.

---

### The Single Global Granfilade

`xanadu.h:14` declares:
```c
#define typegranf INT *
extern typegranf granf;
```

There is one global `granf` tree. Every document's text content, every document's own POOM orgl, and every link orgl all live in this one tree, distinguished solely by their tumbler I-addresses.

---

### The Allocation Entry Point

Both text insertion and link creation converge on the same allocator via `findisatoinsertgr` in `granf2.c:130-156`:

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        ...
        findisatoinsertmolecule(fullcrumptr, hintptr, isaptr);  // same function for both
    } else {
        findisatoinsertnonmolecule(fullcrumptr, hintptr, isaptr);
    }
    tumblerjustify(isaptr);
    return TRUE;
}
```

`doinsert` calls `inserttextingranf` → `inserttextgr` → `findisatoinsertgr` with `atomtype=TEXTATOM`.  
`docreatelink` calls `createorglingranf` → `createorglgr` → `findisatoinsertgr` with `atomtype=LINKATOM`.

Both paths converge on `findisatoinsertmolecule`.

---

### The Shared Allocator: `findisatoinsertmolecule`

`granf2.c:158-181`:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear(&lowerbound, sizeof(lowerbound));
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

    if (tumblerlength(&hintptr->hintisa) == tumblerlength(&lowerbound)) {
        tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement(isaptr, 1, 1, isaptr);
    } else if (hintptr->atomtype == TEXTATOM) {
        tumblerincrement(&lowerbound, 0, 1, isaptr);
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement(&hintptr->hintisa, 2, 2, isaptr);
        if (tumblercmp(&lowerbound, isaptr) == LESS)
            tumblerincrement(isaptr, 1, 1, isaptr);
        else
            tumblerincrement(&lowerbound, 0, 1, isaptr);
    }
}
```

The `atomtype` constants from `xanadu.h:145-146`:
```c
#define TEXTATOM  1
#define LINKATOM  2
```

---

### Address-Range Partitioning by the First Element-Field Value

`tumblerincrement(aptr, rightshift, bint, cptr)` [tumble.c:599-623] places `bint` at mantissa position `last_nonzero_idx + rightshift`. With `rightshift=2`, it appends a zero separator and then the value — producing `D.0.bint` in tumbler dot-notation.

**For document D at address D:**

| Operation | atomtype | upperbound computation | upperbound | Allocation target |
|-----------|----------|------------------------|------------|-------------------|
| Text insert | TEXTATOM=1 | `tumblerincrement(D, 2, 1+1=2, …)` | D.0.2 | **D.0.1.x** |
| Link create | LINKATOM=2 | `tumblerincrement(D, 2, 2+1=3, …)` | D.0.3 | **D.0.2.x** |

**Concrete address structure confirmed by `granf2.c` allocation logic:**

- When `lowerbound == D` (document's own GRANORGL found, same tumbler length as D):
  - TEXTATOM: `tumblerincrement(D, 2, atomtype=1, …)` → D.0.1, then `tumblerincrement(D.0.1, 1, 1, …)` → **D.0.1.1** [`granf2.c:166-167`]
  - LINKATOM: `tumblerincrement(D, 2, 2, …)` → D.0.2, then `tumblerincrement(D.0.2, 1, 1, …)` → **D.0.2.1** [`granf2.c:171-173`]

- When `lowerbound == D.0.1.n` (nth text atom already exists):
  - TEXTATOM: `tumblerincrement(D.0.1.n, 0, 1, …)` → **D.0.1.(n+1)** [`granf2.c:169`]

- When `lowerbound == D.0.2.n` (nth link already exists):
  - LINKATOM: `tumblerincrement(D.0.2.n, 0, 1, …)` → **D.0.2.(n+1)** [`granf2.c:175`]

The single `findpreviousisagr` call [granf2.c:255-278] searches the **same single granfilade tree** in both cases; only the upperbound differs.

---

### Granfilade Bottom-Crum Types

`wisp.h:69-71`:
```c
#define GRANTEXT   1
#define GRANORGL   2
```

Content (s_C) crums are `GRANTEXT` type, inserted at D.0.1.x.  
Link orgl (s_L) crums are `GRANORGL` type (same type as the document's own orgl), inserted at D.0.2.x.

---

### The Full Granfilade Address Space Under Document D

```
D           → GRANORGL  (document's own POOM orgl, created by createorglgr)
D.0.1.1     → GRANTEXT  (first text content atom)
D.0.1.2     → GRANTEXT  (second text content atom)
D.0.2.1     → GRANORGL  (first link's orgl)
D.0.2.2     → GRANORGL  (second link's orgl)
...
```

The `.0.` separator (the zero slot) marks the boundary between D's own address and its sub-allocations. The first element field after the separator — value **1** for s_C, value **2** for s_L — is what discriminates the subspace. This value is derived directly from `atomtype` in both the upperbound construction and the initial allocation target computation.

---

### Confirmed by Golden Tests (Finding 0065)

Finding 0065 golden output shows link I-addresses like `1.1.0.1.0.1.0.2.1` for document `1.1.0.1.0.1`, confirming the `.0.2.x` pattern (element field 2 = s_L). Text addresses follow the `.0.1.x` pattern (element field 1 = s_C).

**Note:** Finding 0065 contains a minor error in the prose — it states "element field 3 for text," but the code at `granf2.c:166` uses `atomtype=TEXTATOM=1`, placing text at element field 1 (D.0.1.x), not 3.

---

### Direct Answer

The granfilade orgl tree under each document uses a **single shared allocator** (`findisatoinsertmolecule`, `granf2.c:158-181`) operating on the **single global granfilade tree**. There are no separate per-subspace allocator trees. The first element-field value after the document's `.0.` separator encodes the subspace:

- **Element field 1** (s_C, content): GRANTEXT crums at D.0.**1**.x — allocated when `atomtype == TEXTATOM`
- **Element field 2** (s_L, links): GRANORGL crums at D.0.**2**.x — allocated when `atomtype == LINKATOM`

The subspace routing is achieved by varying the `upperbound` passed to `findpreviousisagr` (D.0.2 vs D.0.3) and the initial target position (D.0.1 vs D.0.2) — purely an address-range partition within the one global tree, not two separate allocator trees.
