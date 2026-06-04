## Question 3 [evidence]

> Does the udanax-green link allocator guarantee that every A_L(d) emission satisfies the inc-chain (L1c / LinkAllocatorConformance) structurally, so the property transfers from K.λ without per-step reconstruction?

## KB Synthesis

## Link Allocator Inc-Chain: Structural Guarantee

**Short answer: Yes — L1c transfers structurally from K.λ without per-step reconstruction.** The granfilade itself *is* the inc-chain witness.

### Mechanism

The link allocator in `findisatoinsertmolecule` operates as a **stateless query-and-increment** over the granfilade [SS-ADDRESS-ALLOC, Finding 0065]:

1. Compute `upperbound = docISA.2.3` — confines search to document-local link namespace
2. `findpreviousisagr(granf, upperbound)` — returns current maximum link ISA in that range
3. If below `docISA.2.2`: allocate first link at `docISA.2.2.1`
4. Otherwise: `tumblerincrement(lowerbound, 0, 1)` → strictly next value

Each emission is defined purely as `max(K.λ ∩ [docISA.2.2, docISA.2.3)) + 1`. No session counter, no cached state [SS-ADDRESS-SPACE, Finding 0061].

### Why the Property Transfers Without Reconstruction

The structural guarantee rests on **granfilade append-only semantics** [FC-GRANF-ON-DELETE, INV-MONOTONIC Finding 0061]:

> DELETE and REARRANGE never touch the granfilade. All previously emitted link ISAs remain in the tree permanently as witnesses.

This means K.λ monotonically grows — `max(K.λ)` is non-decreasing across time. The allocator queries K.λ fresh each call, so it sees the correct global maximum *without* needing to walk the emission history.

The inc-chain is not a separately maintained structure; the append-only granfilade subtree `[docISA.2.2, docISA.2.3)` **is** the chain. `findpreviousisagr` efficiently extracts its supremum in a single tree traversal.

### Per-Document Independence

The upper bound `docISA.2.3` confines each emission to the document-local namespace [ST-ADDRESS-ALLOC, Finding 0065]:

> MAKELINK on docB → `docB.2.1`; MAKELINK on docA (already has `.2.1`) → `docA.2.2` — independent counters, unaffected by each other.

Cross-document CREATELINK operations do not contaminate a document's link ISA sequence. Interleaved operations on other documents are invisible to the bounded search.

### One Caveat

CREATELINK *does* consume address space in the content region of the granfilade, which breaks text I-address contiguity for subsequent INSERTs [INT-LINK-INSERT, Finding 0063]. This is a cross-chain interaction between the text emission sequence and the link orgl allocation, but it does **not** affect the link-to-link inc-chain within `docISA.2.x` — those remain in a strictly bounded, separately queried namespace.

### Summary

| Property | Mechanism |
|---|---|
| `∀ l₁ < l₂ : iaddr(l₂) > iaddr(l₁)` | `findpreviousisagr` + `tumblerincrement` on append-only tree |
| Transfers from K.λ | Granfilade never loses prior emissions; max is always correct |
| No per-step reconstruction | Tree query IS the chain; no separate witness needed |
| Document isolation | `upperbound = docISA.2.3` confines each search |

---

## Code Exploration

I now have everything needed. Let me compose the complete answer.

---

## A_L(d) and the Inc-Chain Guarantee (L1c / LinkAllocatorConformance)

**Short answer:** No. The granfilade (K.λ) is the authoritative ordered structure, and the inc-chain invariant is maintained within it — but A_L(d) does **not** transfer the property without per-step reconstruction. Each emission requires a tree traversal of K.λ to re-derive the current maximum ISA.

---

### Call Chain for Link Allocation

```
fns.c:createlink
  → do1.c:docreatelink [line 195]
    → granf1.c:createorglingranf [line 50]   ← thin wrapper
      → granf2.c:createorglgr [line 111]
        → granf2.c:findisatoinsertgr [line 117]
          → granf2.c:findisatoinsertmolecule [line 142]  ← where ISA is chosen
            → granf2.c:findpreviousisagr [line 164]      ← K.λ tree traversal
            → tumble.c:tumblerincrement                  ← arithmetic
        → genf.c:insertseq [line 125]                   ← writes new ISA into K.λ
```

---

### Step 1 — The Hint Construction

`docreatelink` [do1.c:207]:
```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
```
This marks the allocation as `subtype=ATOM`, `atomtype=LINKATOM`. That distinction routes execution through `findisatoinsertmolecule` rather than `findisatoinsertnonmolecule`.

---

### Step 2 — Route to the Molecule Path

`findisatoinsertgr` [granf2.c:130–156]:
```c
if (hintptr->subtype == ATOM) {                          // line 135
    if (!isaexistsgr(fullcrumptr, &hintptr->hintisa))    // line 136
        return(FALSE);
    findisatoinsertmolecule(fullcrumptr, hintptr, isaptr); // line 142
```

Links are `ATOM` subtype, so every emission goes through `findisatoinsertmolecule`. The document must already exist (line 136) — the allocation depends on the document's ISA as `hintisa`.

---

### Step 3 — The Actual ISA Computation (LINKATOM branch)

`findisatoinsertmolecule` [granf2.c:158–181]:
```c
tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // line 162
clear(&lowerbound, sizeof(lowerbound));                                        // line 163
findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);      // line 164

// ...

} else if (hintptr->atomtype == LINKATOM) {                                   // line 170
    tumblerincrement(&hintptr->hintisa, 2, 2, isaptr);                        // line 171
    if (tumblercmp(&lowerbound, isaptr) == LESS)                              // line 172
        tumblerincrement(isaptr, 1, 1, isaptr);                               // line 173
    else
        tumblerincrement(&lowerbound, 0, 1, isaptr);                          // line 175
}
```

For `LINKATOM` (`atomtype = 2`):
- **Line 162**: `upperbound = hintisa.0.0.3` — the upper fence for the search
- **Line 163–164**: `lowerbound` is zeroed, then `findpreviousisagr` fills it with the **highest existing link ISA below `upperbound`** in the current K.λ tree
- **Line 171**: `isaptr = hintisa.0.0.2` — the "floor" address for the first possible link slot
- **Lines 172–175**: Branch decision:
  - If `lowerbound < isaptr` (no link exists yet, or lowerbound hasn't reached the floor): increment `isaptr` → first link lands at `hintisa.0.0.2.1`
  - Otherwise: `isaptr = lowerbound + 1` → each subsequent link strictly exceeds the last

The result is always `> lowerbound` by construction, and `lowerbound` is the current maximum — so every emitted ISA is strictly greater than all prior ISAs for this document's link slot.

---

### Step 4 — The K.λ Traversal That Makes This Work

`findpreviousisagr` [granf2.c:255–278]:
```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{                                                                // line 255
    if (crumptr->height == 0) {
        findlastisaincbcgr((typecbc*)crumptr, offset);          // line 264 — leaf: read max ISA
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {  // line 267
        if ((tmp = whereoncrum(ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
            || tmp == ONMYRIGHTBORDER
            || !ptr->rightbro) {
            findpreviousisagr(ptr, upperbound, offset);         // line 272 — descend right
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset); // line 275 — accumulate width
        }
    }
}
```

This is a recursive traversal of the granfilade tree, walking **left-to-right through siblings** and descending into the rightmost child that contains the upper bound. It terminates at a leaf and reads the last ISA there. There is **no stored cursor** or **no "last allocated" field** — the maximum must be reconstructed from the tree structure at every call.

---

### Why the Property Does NOT Transfer Without Per-Step Reconstruction

Three structural facts combine:

**1. No stored maximum.** Nowhere in `typecuc`, `typecbc`, or any enfilade node structure is there a field tracking "last link ISA emitted." The `cwid.dsas[WIDTH]` field at line 275 holds the cumulative width of each subtree, used for navigation — not the rightmost ISA.

**2. `findpreviousisagr` is always executed.** Line 164 is unconditional for the LINKATOM branch. Every single `createorglingranf` call for a link triggers a full O(depth) tree walk. This is per-step, not amortized.

**3. The conditional at lines 172–175 re-derives the comparison fresh each time.** The allocator does not assume it knows where it left off. It re-reads K.λ, computes `lowerbound`, and branches. If two concurrent sessions (if any existed) or a crash recovery scenario placed a different ISA in the tree, this code would correctly find it — because it always searches.

---

### What IS Structural in K.λ

The granfilade **does** maintain the inc-chain as a structural invariant:
- `insertseq` [granf2.c:125] inserts at the computed ISA position
- Sibling ordering in the tree reflects tumbler ordering (left-to-right = increasing ISA)
- `findpreviousisagr`'s left-to-right traversal [line 267] is correct precisely because the tree encodes the order

So K.λ **embodies** the inc-chain, but the allocator must **query** K.λ to extract the current maximum before each emission. The invariant lives in the data structure, not in a cached invariant that can be transferred without reading.

---

### Concrete ISA Sequence (LINKATOM)

For document `d` with ISA `hintisa`:

| Emission | `lowerbound` (from search) | Branch taken | Emitted ISA |
|---|---|---|---|
| 1st | 0 (zero) | line 173: `isaptr+1` | `hintisa.0.0.2.1` |
| 2nd | `hintisa.0.0.2.1` | line 175: `lowerbound+1` | `hintisa.0.0.2.2` |
| 3rd | `hintisa.0.0.2.2` | line 175 | `hintisa.0.0.2.3` |
| … | … | line 175 | `hintisa.0.0.2.n` |

Strictly increasing at position `hintisa.0.0.2.*`, with each step requiring a traversal to find `n`.

---

### Summary

A_L(d) **does** guarantee that every emitted ISA satisfies the inc-chain (L1c): each new link ISA is strictly greater than all prior ones for document `d`. The guarantee is sound.

However, the property does **not** transfer from K.λ without per-step reconstruction. `findpreviousisagr` [granf2.c:255–278] traverses the granfilade tree on every emission — there is no stored invariant that could be propagated across steps. The inc-chain is an **emergent property** of the per-step tree-query-and-increment cycle, not a structural fact that can be read off K.λ without that cycle.
