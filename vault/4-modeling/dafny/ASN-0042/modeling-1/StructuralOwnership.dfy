include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module StructuralOwnership {
  import opened TumblerAlgebra

  // O0 — StructuralOwnership
  // Ownership is decidable from pfx(π) and a alone, without mutable state.
  // The predicate takes only the prefix and address — no State parameter —
  // which structurally guarantees state-independence.
  ghost predicate Owns(prefix: Tumbler, a: Tumbler) {
    IsPrefix(prefix, a)
  }
}
