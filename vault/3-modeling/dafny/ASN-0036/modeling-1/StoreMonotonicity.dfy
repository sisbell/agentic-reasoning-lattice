include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "ContentImmutability.dfy"

module StoreMonotonicity {
  import opened TumblerAlgebra
  import CI = ContentImmutability

  // S1 — StoreMonotonicity
  // dom(Σ.C) ⊆ dom(Σ'.C)
  // Corollary of S0 (ContentImmutability), for every state transition Σ → Σ'.
  lemma StoreMonotonicity(s: CI.State, s': CI.State)
    requires CI.ContentImmutability(s, s')
    ensures s.C.Keys <= s'.C.Keys
  { }
}
