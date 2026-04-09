include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// O9 — NodeLocalOwnership
// (A π ∈ Π, a ∈ T : owns(π, a) ⟹ nodeField(pfx(π)) ≼ nodeField(a))
module NodeLocalOwnership {
  import opened TumblerAlgebra
  import TumblerHierarchy

  lemma NodeLocalOwnership(p: Tumbler, a: Tumbler)
    requires IsPrefix(p, a)
    requires TumblerHierarchy.ZeroCount(p.components) <= 1
    ensures TumblerHierarchy.SeqIsPrefix(TumblerHierarchy.NodeField(p), TumblerHierarchy.NodeField(a))
  { }
}
