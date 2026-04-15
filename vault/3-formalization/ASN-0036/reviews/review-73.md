# Cone Review — ASN-0036/D-CTG-depth (cycle 4)

*2026-04-14 21:32*

### All three invariant proofs assume an implicit closed-world transition relation that no property defines
**Foundation**: Σ.M(d) (Arrangement) — defines the state component but not how it evolves
**ASN**: D-CTG proof: "Let Σ → Σ' be any state transition produced by an operation (INSERT, DELETE, COPY, MOVE, REARRANGE, or APPEND)." S8-depth proof: identical enumeration. S8-fin proof: identical enumeration.
**Issue**: Each inductive proof's soundness depends on the enumerated operations being the *complete* set of state transitions — every possible Σ → Σ' is produced by one of these six. But this completeness claim has no formal anchor. The six operations are independently replicated in three separate proof texts without citing a shared definition. If the transition relation is incomplete — e.g., if document creation, document deletion, or link operations can also modify dom(M(d)) — every inductive argument is unsound, because the inductive step would fail to cover all transitions. For TLA+ formalization, this is the `Next` predicate: a single disjunction that all invariant proofs reference. The ASN has no analogue — each property independently asserts its own version of what transitions exist, with no guarantee that the three lists agree or are exhaustive.
**What needs resolving**: A definition (either in this ASN or a shared system-model property) that formally specifies the complete set of state-modifying operations, so that the inductive proofs cite a defined term rather than independently maintained enumerations.
