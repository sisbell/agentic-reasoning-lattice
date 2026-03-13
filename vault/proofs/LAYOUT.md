# vault/proofs/ Layout

## Directory structure

```
proofs/
├── TumblerAlgebra/      Shared definitions + generated property proofs (ASN-0034)
├── CHANGELOG.md         History of module changes and rationale
├── imports.md           Maps ASN → proof module dependencies for Dafny generation
└── dfyconfig.toml       Picks up **/*.dfy — no include directives needed
```

## TumblerAlgebra

`TumblerAlgebra.dfy` contains the shared definitions: Tumbler datatype, LessThan, ActionPoint, TumblerAdd, TumblerSubtract, IsPrefix, and utility helpers. Generated property proofs live alongside it in the same directory — each imports `TumblerAlgebra` and proves a specific ASN-0034 claim.

New shared definitions are extracted into `TumblerAlgebra.dfy` when multiple generated proofs independently define the same function. The definitions module evolves iteratively through generation cycles.

## dfyconfig.toml

`includes = ["**/*.dfy"]` — all .dfy files under proofs/ are resolved automatically. No `include` directives in individual files. Module imports (`import TumblerAlgebra`) are the only coupling mechanism.

`warn-redundant-assumptions = false` — disabled because Dafny's checker incorrectly flags requires clauses that are needed for well-formedness of subsequent requires.
