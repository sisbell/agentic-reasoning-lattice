include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module ContentImmutability {
  import opened TumblerAlgebra

  // Opaque content value type
  type Val(==)

  // Two-space state (content store only; arrangements modeled per-property)
  datatype State = State(C: map<Tumbler, Val>)

  // S0 — ContentImmutability
  // For every state transition Σ → Σ':
  //   a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)
  ghost predicate ContentImmutability(s: State, s': State) {
    forall a :: a in s.C ==> a in s'.C && s'.C[a] == s.C[a]
  }
}
