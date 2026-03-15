# vault/proofs/ Layout

## Directory structure

```
proofs/
├── TumblerAlgebra/
│   ├── TumblerAlgebra.dfy          Shared definitions: Tumbler, ordering, arithmetic, allocation ops
│   ├── TumblerOrder.dfy            T0, T1, T2, T3, TA6
│   ├── TumblerHierarchy.dfy        T4, T5, T6, T7, PrefixOrderingExtension
│   ├── TumblerAddition.dfy         TA0, TA1, TA-strict, TA1-strict/weak, T12, TA7a
│   ├── TumblerSubtraction.dfy      TA2, TA3-strict/weak, TA4, ReverseInverse
│   └── TumblerAllocation.dfy       T8, T10a-d, T11
├── NodeOntology/
│   ├── NodeOntology.dfy            Shared definitions: NodeAddress, Parent, Children, NodeState, Actor
│   ├── NodeIdentity.dfy            Σ.nodes, N0, N1, N2, N3, N5, N6, N7, N9, N10, N13, N14, N16
│   └── NodeAllocation.dfy          N4, N8, N11, N12
├── CHANGELOG.md                    History of module changes and rationale
└── dfyconfig.toml                  Picks up **/*.dfy — no include directives needed
```

## TumblerAlgebra

`TumblerAlgebra.dfy` contains shared definitions used by all property proof modules: Tumbler datatype, Address/Displacement type aliases, LessThan/LessEq ordering, ActionPoint, LastNonzero, FindZero, TumblerAdd, AllocationInc, TumblerSubtract, SubtractResultAt, IsPrefix, and utility helpers.

Five consolidated proof modules live alongside it. Each groups related ASN-0034 properties by theme:

- **TumblerOrder** — unbounded structure, lexicographic ordering, intrinsic comparison, canonical representation, zero tumbler sentinel
- **TumblerHierarchy** — valid address structure, contiguous subtrees, decidable containment, subspace disjointness, prefix ordering extension
- **TumblerAddition** — well-definedness, associativity, strict increase, order preservation, span well-definedness, subspace closure
- **TumblerSubtraction** — well-definedness, order preservation (strict and weak), partial inverse, reverse inverse
- **TumblerAllocation** — address permanence, allocator discipline, partition independence/monotonicity, increment preserves validity, global uniqueness

## NodeOntology

`NodeOntology.dfy` contains shared definitions for node ontology: NodeAddress predicate, Root constant, Parent/IsChildOf/Children functions, NodeState datatype, Actor type, AuthGrant datatype, authorized predicate, and ZeroCount helper lemmas.

Two consolidated proof modules:

- **NodeIdentity** — what nodes ARE: baptized nodes, ghost element, identity by assignment, single root, node tree, sequential children, structural ordering, forward reference admissibility, subtree contiguity/disjointness, uniform node type, no mutable state, prefix propagation
- **NodeAllocation** — how nodes are CREATED: baptism monotonicity, allocation authority, authority permanence, coordination-free disjointness, local serialization sufficiency, always-valid states (BAPTIZE preserves all invariants)

## Dependency graph

```
TumblerAlgebra
    ↑
    +--- TumblerOrder, TumblerHierarchy, TumblerAddition, TumblerSubtraction
    |                       ↑
    |                       |
    +--- TumblerAllocation (imports TumblerHierarchy)
    |
    +--- NodeOntology (imports TumblerAlgebra, TumblerHierarchy)
             ↑
             |
             +--- NodeIdentity (imports NodeOntology, TumblerHierarchy, TumblerOrder, TumblerAddition)
             |
             +--- NodeAllocation (imports NodeOntology, NodeIdentity, TumblerHierarchy, TumblerAllocation)
```

## dfyconfig.toml

`includes = ["**/*.dfy"]` — all .dfy files under proofs/ are resolved automatically. No `include` directives in individual files. Module imports (`import TumblerAlgebra`, `import NodeOntology`, etc.) are the only coupling mechanism.

`warn-redundant-assumptions = false` — disabled because Dafny's checker incorrectly flags requires clauses that are needed for well-formedness of subsequent requires.
