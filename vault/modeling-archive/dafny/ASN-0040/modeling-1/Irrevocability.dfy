include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module Irrevocability {
  import opened TumblerAlgebra

  // B0 — Irrevocability
  // (A Σ, Σ' : Σ → Σ' : Σ.B ⊆ Σ'.B)

  datatype BaptismalState = BaptismalState(B: set<Tumbler>)

  ghost predicate Irrevocable(s: BaptismalState, s': BaptismalState) {
    s.B <= s'.B
  }

  // Transitivity: if irrevocability holds across two transitions,
  // it holds across their composition.
  lemma IrrevocabilityTransitive(s1: BaptismalState, s2: BaptismalState, s3: BaptismalState)
    requires Irrevocable(s1, s2)
    requires Irrevocable(s2, s3)
    ensures Irrevocable(s1, s3)
  { }

  // Reflexivity: the identity transition preserves irrevocability.
  lemma IrrevocabilityReflexive(s: BaptismalState)
    ensures Irrevocable(s, s)
  { }
}
