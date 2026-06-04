## Question 3 [evidence]

> What does the composite-boundary invariant P7a require of a post-state Σ', and is it discharged solely by frame-fixity of Σ.C and Σ.R?

## KB Synthesis

The KB does not contain an entry for "P7a," "composite-boundary invariant," or the notation Σ.C / Σ.R. These terms appear nowhere in the findings.

The KB defines related but distinct named artifacts:
- Permanence axioms **P0** / **P0'** [SS-THREE-LAYER-MODEL]
- Placement guard predicate **ENF0** [PRE-ENF0-PLACEMENT-GAP]
- Bijectivity invariant **I₁** [INV-POOM-BIJECTIVITY]
- Content discipline **CD0** [EC-REARRANGE-CROSS-SUBSPACE]
- B-tree occupancy invariant **EN-4** [INV-ENFILADE-MINIMALITY]
- The `Σ.next` counter (explicitly rejected as a model) [SS-ADDRESS-SPACE Finding 0077]

None of these is P7a, and Σ.C / Σ.R are not defined anywhere in the KB.

This question is not answerable from the knowledge base as provided.

---

## Code Exploration

I now have everything I need to answer.

---

## P7a Does Not Exist in This Codebase

The label **P7a**, the notation "composite-boundary invariant," and the Greek-letter state model (Σ, Σ', Σ.C, Σ.R) are **not present anywhere** in this repository. I searched exhaustively: `knowledge-base/kb-formal.md` (601KB), all 80+ findings, all C source files. Zero matches. The formal system used here is a different labeling scheme entirely: `SS-*` (state structure), `ST-*` (state transition), `FC-*` (frame condition), `INV-*` (invariant), `PRE-*`, `EC-*`, `INT-*`.

I will not fabricate a specification for a label that does not appear in any source. What I can do is trace the closest equivalent concepts from the actual code and knowledge base.

---

## The Actual Formal System and Its State Model

The canonical state decomposition is given at `knowledge-base/kb-formal.md:5073–5079` (**FC-POOM-MUTABILITY**, sourced from Finding 0072):

```
State = {
  granfilade: I-addr → byte          -- immutable, append-only
  spanfilade: I-addr → {doc-ISA}     -- immutable, write-only (no delete)
  pooms: doc-ISA → (V-addr → I-addr) -- MUTABLE, modified in-place
}
```

Notice the model has **three** components, not two. If the question's Σ.C maps to `granfilade` and Σ.R maps to `spanfilade`, then the POOM (`pooms`) is a third component Σ.P that is omitted from the frame-fixity hypothesis. This omission is the central issue.

---

## What "Frame-Fixity of Σ.C and Σ.R" Covers

**FC-GRANF-ON-DELETE** (`kb-formal.md:5182`): DELETE and REARRANGE are frame-condition-preserving on the granfilade — `granf_after(op) = granf_before(op)`. These two operations also leave the spanfilade unchanged because they never call any spanfilade-writing function.

**FC-INSERT-IADDR** (`kb-formal.md:5163`): INSERT preserves all pre-existing I-addresses and does not modify the spanfilade link-index entries (though it does write DOCISPAN entries to `spanf`, a correction noted at `kb-formal.md:5008`).

**FC-SUBSPACE** (`kb-formal.md:4799`): The subspace boundary frame condition — operations on subspace `s` do not affect subspace `s' ≠ s` — is enforced structurally by `insertcutsectionnd` at `edit.c:207–233`. When `nblades == 2`, the function checks each POOM crum against `blade[1]` (the subspace boundary at the next `.0.` digit boundary) first. For a crum at or beyond that boundary, `whereoncrum` returns `ONMYLEFTBORDER`, triggering `return(2)` (no shift) before the crum's position is ever touched:

```c
// edit.c:212-220
if (knives->nblades == 2) {
    i = 1;
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    ...
    } else if (cmp <= ONMYLEFTBORDER) {
        return (2);   // case 2: beyond second blade, no shift
    }
}
```

This is a code-level enforcement of subspace isolation in the POOM — not in the granfilade or spanfilade.

---

## Why Frame-Fixity of Σ.C and Σ.R Is Not Sufficient

**1. CREATELINK modifies both granfilade and spanfilade non-atomically.**

`docreatelink` at `do1.c:195–221` executes this chain:

```c
// do1.c:208-220
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)   // writes granfilade [line 209]
  && tumbler2spanset (...)
  && findnextlinkvsa (...)
  && docopy (...)
  && findorgl (...)
  && ...
  && insertendsetsinspanf (taskptr, spanf, linkisaptr, ...)  // writes spanfilade [line 219]
);
```

Neither Σ.C nor Σ.R is frame-fixed by CREATELINK — both are mutated. The cross-structure invariant **INV-DUAL-ENFILADE-CONSISTENCY** (`kb-formal.md:5683`) requires `∀ link_isa ∈ granf.link_orgls : endpoints(link_isa) ⊆ spanf.indexed_endpoints(link_isa)`. This invariant is not dischargeable by frame-fixity of either component; it requires that both be *consistently updated*. Because the two writes at `do1.c:209` and `do1.c:219` are not transactional (no rollback on failure between them), partial failure can violate it despite neither component being "fixed."

**2. INSERT, DELETE, REARRANGE mutate only the POOM (Σ.P).**

For these operations, Σ.C and Σ.R are indeed frame-fixed in the sense that the granfilade and spanfilade-link-index are unchanged. But the invariant that clients care about — the V-to-I mapping — lives in Σ.P, which changes. Subspace isolation (FC-SUBSPACE) is preserved by the two-blade knife at `edit.c:212–220`, not by anything about Σ.C or Σ.R.

**3. The POOM is the sole locus of destructive mutation.**

`kb-formal.md:5081`: "The POOM is the sole locus of destructive mutation. All state transitions (ST-INSERT, ST-DELETE, ST-REARRANGE) operate on POOMs. Invariants about content permanence (INV-IADDR-IMMUTABILITY) hold because they apply to the granfilade, not the POOM." Any invariant that concerns V-address mutation, subspace isolation, or address-shift behavior is a statement about Σ.P, not Σ.C or Σ.R.

---

## Summary

The label P7a does not appear in this codebase or its knowledge base. No answer can be sourced to it.

For the underlying structural question: frame-fixity of the content layer (granfilade) and the reference/registry layer (spanfilade) is **not sufficient** to discharge what would naturally be called a "composite-boundary invariant" in this system, for two independent reasons:

- `CREATELINK` (`do1.c:208–219`) necessarily modifies **both** layers non-atomically; neither is frame-fixed, and consistency between them depends on uninterrupted sequential execution.
- The subspace-boundary isolation property is enforced in the POOM layer via the two-blade knife mechanism (`edit.c:212–220`), which is a third state component (`Σ.P`) absent from the Σ.C + Σ.R framing. Frame-fixity of Σ.C and Σ.R says nothing about POOM mutation, and POOM mutation is what all document-modifying operations actually perform.
