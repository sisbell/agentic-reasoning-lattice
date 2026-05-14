## Question 5 [evidence]

> In udanax-green, are element-level I-address allocators created by `inc(·, k')` operations applied to document-level allocators (i.e., descendants in the same allocator tree), such that any T10a-discipline placed on document-level allocators propagates to element-level allocators?

## KB Synthesis

The KB does not support the claim that element-level I-address allocators are derived from document-level allocators via `inc(·, k')` or any equivalent operation. The implementation uses a flat, shared allocation mechanism — not a hierarchical allocator tree — and T10a discipline cannot propagate through a derivation chain that does not exist.

## What the KB shows

**Two allocation functions, same granfilade, independent bounds**

[SS-ADDRESS-SPACE Finding 0077] states explicitly:

> Document addresses are allocated under the parent account/document via `findisatoinsertnonmolecule` (depth 1 or 2), while content I-addresses are allocated under the document's content subspace via `findisatoinsertmolecule` (depth 3+). There is no single global "next" counter (no Σ.next). Allocation is stateless query-and-increment on different tumbler ranges via `findpreviousisagr`.

These are two separate functions dispatched from `findisatoinsertgr` depending on whether the target is a molecule (text/link atom) or non-molecule (document orgl). Neither calls the other. Neither is derived from the other.

**Element bounds are computed from the document ISA, not from a document-level allocator**

[SS-ADDRESS-ALLOC Finding 0065] shows the element allocation bound:

> `backend/granf2.c:162` — `tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound)` sets document-scoped bound

The upper bound is computed directly from the document ISA via `tumblerincrement` at call time — not read from any allocator object or derived counter. The element allocator is a stateless range-bounded tree query, bounded by a fresh arithmetic operation on the document address. There is no allocator object to inherit from.

**The relationship is address containment, not allocator derivation**

Element I-addresses are structurally subordinate to the document ISA in tumbler space: link element addresses are in `[docISA.0.2.1, docISA.0.2.3)` per [SS-ADDRESS-ALLOC Finding 0065], and text element addresses are in the document's content subspace. This is a prefix/containment relationship between address ranges, not a derived-allocator relationship. The check uses tumbler truncation and comparison [SS-TUMBLER-CONTAINMENT].

**Monotonicity is global, not inherited**

[INV-MONOTONIC] holds at the element level because all allocations query the same granfilade tree via `findpreviousisagr`, which returns the current global maximum. It is not a consequence of deriving element allocators from document allocators. Any T10a-type monotonicity constraint at element level must be established independently for that allocation subspace.

## Conclusion

The element-level allocator is not produced by any `inc(·, k')` applied to the document-level allocator. The KB shows no allocator inheritance chain: the two allocation functions are independent, operating on the same flat granfilade with different search bounds computed fresh at each call. A T10a discipline placed on document-level allocators (e.g., on `findisatoinsertnonmolecule`'s output) has no formal propagation path to `findisatoinsertmolecule`'s outputs. The only shared constraint is global granfilade monotonicity, which both satisfy independently via `findpreviousisagr + tumblerincrement(+1)` [SS-ADDRESS-SPACE Finding 0061].

---

## Code Exploration

I now have all the verified source evidence to answer fully.

---

## Answer: I-Address Allocator Hierarchy in udanax-green

### Short Answer

**Yes on structure, qualified on discipline propagation.** Element-level I-addresses are created by `tumblerincrement()` — the code's `inc(·, k')` — applied to document-level addresses as the hint base. They are structurally descendants in the same allocator tree via tumbler prefix. However, the codebase has no explicit T10a constraint mechanism; what propagates is the structural prefix relationship, not an enforced discipline layer.

---

### 1. The Three-Level Allocator Tree

The hierarchy is **account → document → element (ATOM)**, established entirely through the `makehint` + `findisatoinsertgr` pathway.

**`makehint` [do2.c:78-84]** packages the parent ISA as `hintptr->hintisa` and encodes the type relationship as `(supertype, subtype)`:

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

The three call sites that build the hierarchy:

| Level | Call site | Hint |
|-------|-----------|------|
| Account → Document | `do1.c:239` | `makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)` |
| Document → Document (version) | `do1.c:271` | `makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint)` |
| Document → Text element | `do1.c:117` | `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)` |
| Document → Link element | `do1.c:180,207` | `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` |

---

### 2. Allocator Dispatch: `findisatoinsertgr` [granf2.c:130-156]

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {
            fprintf (stderr,"nothing at hintisa for atom\n");
            return (FALSE);
        }
        findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
    } else {
        findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
    }
    tumblerjustify(isaptr);
    return (TRUE);
}
```

**Critical point [granf2.c:136]:** Before allocating any element address, `isaexistsgr` verifies the document ISA already exists in the granfilade. Element allocation is *gated* on the existence of the parent document allocator — you cannot create elements without a live document node in the tree.

---

### 3. Element ISA Allocation: `findisatoinsertmolecule` [granf2.c:158-181]

Every branch derives the element ISA by `tumblerincrement` from `hintptr->hintisa` (the document ISA) or from `lowerbound` (the previously allocated peer, which is itself a descendant of the document ISA):

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound); // line 162
    ...
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);  // line 166
        tumblerincrement (isaptr, 1, 1, isaptr);                        // line 167
    } else if (hintptr->atomtype == TEXTATOM) {
        tumblerincrement (&lowerbound, 0, 1, isaptr);                   // line 169
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);             // line 171
        ...
    }
}
```

All paths are exclusively `tumblerincrement` operations on the document ISA or on prior element ISAs that are themselves children of the document ISA. This is the `inc(·, k')` operation of the formalism.

---

### 4. `tumblerincrement` — The `inc(·, k')` Implementation [tumble.c:599-623]

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    if (iszerotumbler (aptr)) {
        cptr->exp = -rightshift;
        cptr->mantissa[0] = bint;
        return(0);
    }
    if (aptr != cptr) movetumbler(aptr,cptr);
    for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
    cptr->mantissa[idx + rightshift] += bint;   // line 621
    tumblerjustify (cptr);
}
```

`rightshift` is the `k'` depth parameter. When called from `findisatoinsertmolecule` with `rightshift=2`, it appends two new decimal places to the document ISA, creating a child address at the next hierarchical level. The resulting element ISA **shares the document ISA as a prefix** — the defining property of being a descendant in the allocator tree.

---

### 5. Prefix Ownership Verification: `tumbleraccounteq` [tumble.c:38-70]

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    ...
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2)
                return(TRUE);  // document's prefix matches account — it is a descendant
        } else {
            if (aptr->mantissa[i] != bptr->mantissa[i])
                return(FALSE);
        }
    }
    return (TRUE);
}
```

Used at `do1.c:270` (`docreatenewversion`) to verify: "does this document ISA belong to this account?" The test is purely a **prefix match** — if the first N non-zero mantissa places of the document ISA match the account ISA, the document is in the account's allocator subtree. There is no separate ownership record; the ISA structure *is* the ownership record.

---

### 6. On T10a-Discipline Propagation

The term "T10a" does not appear anywhere in the codebase (confirmed by grep across all `.c` and `.h` files). What the code *does* implement is a **structural enforcement** that, in effect, enacts the spirit of T10a:

1. **Element allocation requires parent existence** [granf2.c:136]: `isaexistsgr` blocks element ISA allocation if the document does not yet exist — the document allocator must be live.
2. **ISA prefix is inherent** [tumble.c:621]: Because element ISAs are always formed by appending to the document ISA, the prefix relationship is mathematically inevitable. Any predicate that tests the document ISA prefix (like `tumbleraccounteq`) will return true for all its elements.
3. **No explicit constraint propagation layer exists**: There is no code that takes a rule attached to a document allocator and enforces it at element-allocation time. The only "propagation" is the implicit one: because element ISAs carry the document ISA as a prefix, any check that scans by prefix (e.g., account membership, retrieval range) will naturally include all elements belonging to that document.

---

### Conclusion

Element-level I-addresses in udanax-green are created exactly by `tumblerincrement(document_isa, k', 1)` — the `inc(·, k')` operation — and are structurally descendants of the document-level allocator [granf2.c:158-181, tumble.c:599-623]. The allocator tree is account → document → element, instantiated via the `makehint` / `findisatoinsertgr` chain [do1.c:117,239; granf2.c:130-156]. Ownership propagates through the ISA prefix itself, verified by `tumbleraccounteq` [tumble.c:38-70].

However, T10a-discipline as a named mechanism with explicit propagation semantics does not exist in this implementation. What propagates is the **prefix relationship**: any property that is tested by prefix scan (retrieval, account membership, range queries) automatically subsumes elements under their parent document. Whether that constitutes T10a-discipline propagation depends on whether the T10a rules in your formal model reduce to prefix-range tests — if they do, the codebase implicitly satisfies them through its tumbler arithmetic; if they require a separate constraint-enforcement layer, that layer is absent.
