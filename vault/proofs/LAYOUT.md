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
├── CHANGELOG.md                    History of module changes and rationale
├── imports.md                      Maps ASN → proof module dependencies for Dafny generation
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

## Dependency graph

```
TumblerAlgebra
    ↑
    |
    +--- TumblerOrder, TumblerHierarchy, TumblerAddition, TumblerSubtraction
    |                       ↑
    |                       |
    +--- TumblerAllocation (imports TumblerHierarchy for ValidAddress, PrefixOrderingExtension)
```

## dfyconfig.toml

`includes = ["**/*.dfy"]` — all .dfy files under proofs/ are resolved automatically. No `include` directives in individual files. Module imports (`import TumblerAlgebra`, `import TumblerHierarchy`, etc.) are the only coupling mechanism.

`warn-redundant-assumptions = false` — disabled because Dafny's checker incorrectly flags requires clauses that are needed for well-formedness of subsequent requires.
