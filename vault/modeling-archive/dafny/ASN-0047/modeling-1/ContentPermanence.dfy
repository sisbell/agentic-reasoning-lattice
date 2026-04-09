include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module ContentPermanence {
  import opened TumblerAlgebra

  // Minimal state projection: only the content map is needed for P0
  datatype State = State(C: map<Tumbler, nat>)

  // ---------------------------------------------------------------------------
  // P0 — ContentPermanence
  //
  // (A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a)))
  // ---------------------------------------------------------------------------

  ghost predicate ContentPermanence(s: State, s': State) {
    forall a :: a in s.C ==> a in s'.C && s'.C[a] == s.C[a]
  }
}
