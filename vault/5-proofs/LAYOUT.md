# vault/proofs/ Layout

## Directory structure

```
proofs/
├── TumblerAlgebra/
│   ├── TumblerAlgebra.dfy          Shared definitions: Tumbler, ordering, arithmetic, allocation ops
│   ├── TumblerOrder.dfy            T0, T1, T2, T3, TA6
│   ├── TumblerHierarchy.dfy        T4, T5, T6, T7, PrefixOrderingExtension, level predicates
│   ├── TumblerAddition.dfy         TA0, TA1, TA-strict, TA1-strict/weak, T12, TA7a
│   ├── TumblerSubtraction.dfy      TA2, TA3-strict/weak, TA4, ReverseInverse
│   └── TumblerAllocation.dfy       T8, T10a-d, T11
├── TwoSpace/
│   ├── TwoSpace.dfy                Shared definitions: Val, TwoSpaceState, ContentImmutability, ReferentialIntegrity, Origin
│   ├── TwoSpaceContent.dfy         S0, S1, S4, S6, S7a, S7b, S7
│   ├── TwoSpaceArrangement.dfy     S2, S3, S5, S8-fin, S8a, S8-depth, S8
│   └── TwoSpaceSeparation.dfy      S9
├── TumblerBaptism/
│   ├── TumblerBaptism.dfy          Shared definitions: StreamElement, InStream, Children, ValidBaptism, BaptismState
│   ├── BaptismBranching.dfy        S0, S1, B5, B5a, B7
│   ├── BaptismRegistry.dfy         B0, B0a, B₀, B1, B2, B4, B6, B8, B9, B10, Bop
│   └── BaptismGhost.dfy            B3 (cross-cutting — bridges baptism and content model)
├── TumblerOwnership/
│   ├── TumblerOwnership.dfy        Shared definitions: Principal, State, Covers, IsEffectiveOwner, Acct, O1, O9, O11, O12
│   ├── OwnershipProvenance.dfy     O0, O1a, O1b, O6, AccountPrefix
│   ├── OwnershipExclusivity.dfy    O2
│   ├── OwnershipPermanence.dfy     O3, O8, O13, AccountPermanence
│   ├── OwnershipDelegation.dfy     O4, O5, O7, O14, O15, O16, O17
│   └── OwnershipFork.dfy           O10 (DenialAsFork — ForkAddressExists is {:axiom})
├── CHANGELOG.md                    History of module changes and rationale
└── dfyconfig.toml                  Picks up **/*.dfy — no include directives needed
```

## TumblerAlgebra

`TumblerAlgebra.dfy` contains shared definitions used by all property proof modules: Tumbler datatype, Address/Displacement type aliases, LessThan/LessEq ordering, ActionPoint, LastNonzero, FindZero, TumblerAdd, AllocationInc, TumblerSubtract, SubtractResultAt, IsPrefix, and utility helpers.

Five consolidated proof modules live alongside it. Each groups related ASN-0034 properties by theme:

- **TumblerOrder** — unbounded structure, lexicographic ordering, intrinsic comparison, canonical representation, zero tumbler sentinel
- **TumblerHierarchy** — valid address structure, contiguous subtrees, decidable containment, subspace disjointness, prefix ordering extension, hierarchy level predicates (NodeAddress, AccountAddress, DocumentAddress, ElementAddress, Root)
- **TumblerAddition** — well-definedness, associativity, strict increase, order preservation, span well-definedness, subspace closure
- **TumblerSubtraction** — well-definedness, order preservation (strict and weak), partial inverse, reverse inverse
- **TumblerAllocation** — address permanence, allocator discipline, partition independence/monotonicity, increment preserves validity, global uniqueness

## TwoSpace

`TwoSpace.dfy` contains shared definitions for two-space architecture: Val type, TwoSpaceState datatype, ContentImmutability and ReferentialIntegrity predicates, AllPositive, Origin function.

Three consolidated proof modules:

- **TwoSpaceContent** — content immutability, store monotonicity, origin-based identity, persistence independence, document-scoped allocation, element-level addresses, structural attribution
- **TwoSpaceArrangement** — arrangement functionality, referential integrity, unrestricted sharing, finite arrangement, V-position well-formedness, fixed-depth positions, span decomposition
- **TwoSpaceSeparation** — the capstone theorem: arrangement changes cannot alter stored content

## TumblerOwnership

`TumblerOwnership.dfy` contains shared definitions for tumbler ownership: Principal datatype (with embedded prefix), State (principals + allocated addresses), Covers/IsEffectiveOwner predicates, StrictPrefix, DelegationPrecondition, Acct (account-field truncation), PrincipalPersistence (O12), AddressPermanence (T8), CoveringPrefixesOrdered utility lemma, O1 (Owns), O9 (NodeLocalOwnership), O11 (ValidSession).

Six consolidated proof modules:

- **OwnershipProvenance** — structural ownership (O0), account boundary (O1a), prefix injectivity (O1b), structural provenance (O6), account prefix corollary. Non-trivial proofs: ZeroAtIndex, TwoZerosCount (recursive), CoveringToAccount (case analysis with FindZero), CoveringBiconditional (dual implication), StructuralProvenance (composition).
- **OwnershipExclusivity** — the central theorem O2: unique effective owner exists. Non-trivial proofs: MostSpecificExists (recursive set induction, `decreases |candidates|`), OwnershipExclusivity (witness construction + forall).
- **OwnershipPermanence** — ownership refinement (O3), irrevocable delegation (O8), prefix immutability (O13, structural), account permanence corollary. O13 is structural with the embedded-prefix Principal model (documented in comments).
- **OwnershipDelegation** — domain coverage (O4), subdivision authority (O5), delegation state transition (O7), bootstrap invariants (O14), principal closure (O15), allocation closure (O16), allocated address validity (O17). Non-trivial proof: DomainCoveragePreserved (forall with witness extraction).
- **OwnershipFork** — denial as fork (O10). ForkAddressExists declared `{:axiom}` — witness construction requires finite-set reasoning not yet mechanized.

## Dependency graph

```
TumblerAlgebra
    ↑
    +--- TumblerOrder, TumblerHierarchy, TumblerAddition, TumblerSubtraction
    |                       ↑
    |                       |
    +--- TumblerAllocation (imports TumblerHierarchy)
    |
    +--- TwoSpace (imports TumblerAlgebra, TumblerHierarchy)
    |        ↑
    |        +--- TwoSpaceContent (imports TwoSpace, TumblerHierarchy, TumblerAllocation)
    |        +--- TwoSpaceArrangement (imports TwoSpace)
    |        +--- TwoSpaceSeparation (imports TwoSpace)
    |
    +--- TumblerOwnership (imports TumblerAlgebra, TumblerHierarchy)
             ↑
             +--- OwnershipProvenance (imports TumblerOwnership, TumblerHierarchy)
             +--- OwnershipExclusivity (imports TumblerOwnership)
             +--- OwnershipPermanence (imports TumblerOwnership, TumblerHierarchy)
             +--- OwnershipDelegation (imports TumblerOwnership, TumblerHierarchy)
             +--- OwnershipFork (imports TumblerOwnership, TumblerHierarchy)
```

## dfyconfig.toml

`includes = ["**/*.dfy"]` — all .dfy files under proofs/ are resolved automatically. No `include` directives in individual files. Module imports (`import TumblerAlgebra`, `import TwoSpace`, etc.) are the only coupling mechanism.

`warn-redundant-assumptions = false` — disabled because Dafny's checker incorrectly flags requires clauses that are needed for well-formedness of subsequent requires.
