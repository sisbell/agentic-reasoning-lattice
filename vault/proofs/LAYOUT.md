# vault/proofs/ Layout

## Directory structure

```
proofs/
├── TumblerAlgebra/      Tumbler datatype, LessThan, Add/Subtract, IsPrefix
├── Foundation/          State model: IAddr, VPos, State, J0–J2
├── AddressAllocation/   ASN-0001 address properties: T4, T7, T9, T10, T10a, GlobalUniqueness
├── imports.md           Maps ASN → proof module dependencies for Dafny generation
└── dfyconfig.toml       Picks up **/*.dfy — no include directives needed
```

## Why three peer directories (not nested)

AddressAllocation is a top-level peer of TumblerAlgebra, not a subdirectory of it.

**Import direction, not containment.** AddressAllocation imports TumblerAlgebra (it uses Tumbler, LessThan, IsPrefix), but it is not part of the tumbler algebra. It is a collection of ASN-0001 domain properties — hierarchical parsing, subspace disjointness, forward allocation, allocator discipline, partition independence, global uniqueness. These are specification-level properties about how the Xanadu address space behaves, not algebraic operations on tumblers.

**Separate concerns for downstream consumers.** ASN-25 proofs (and future ASN proofs) import Foundation for types and AddressAllocation for lemmas. These are independent concerns: a proof file might need the State model without any address properties, or vice versa. Nesting would conflate them.

**Promotion origin.** These files were promoted from `vault/3-modeling/dafny/ASN-0001/modeling-1/` into `vault/proofs/` so that downstream ASN proofs can import them as verified building blocks. They were not refactored or restructured — only `include` directives were removed (dfyconfig.toml handles resolution).

## Dependency graph

```
TumblerAlgebra          Foundation
    ↑       ↑               ↑
    |       |               |
    |   AddressAllocation   |
    |   (T4,T7,T9,T10,GU)  |
    |                       |
    +--- ASN-NN proofs -----+
```

AddressAllocation depends on TumblerAlgebra only. Foundation depends on TumblerAlgebra only. Future ASN proof files import both Foundation and AddressAllocation.

## dfyconfig.toml

`includes = ["**/*.dfy"]` — all .dfy files under proofs/ are resolved automatically. No `include` directives in individual files. Module imports (`import TumblerAlgebra`, `import ForwardAllocation`, etc.) are the only coupling mechanism.

`warn-redundant-assumptions = false` — disabled because Dafny's checker incorrectly flags requires clauses that are needed for well-formedness of subsequent requires (e.g., `ElementAddress(a)` is needed for `SubspaceId(a)` to be well-formed, but Dafny considers it redundant for the proof body). The other warning flags (shadowing, contradictory assumptions) remain enabled.

## imports.md

Maps each ASN to the proof modules the Dafny generator injects as context. The generator reads all `.dfy` files from each listed module directory and includes their source in the generation prompt. Generated files (which live in `vault/3-modeling/dafny/`) use `include` directives with relative paths back to `vault/proofs/` to access these modules, then `import` to use them. dfyconfig.toml only covers files within `vault/proofs/`.
