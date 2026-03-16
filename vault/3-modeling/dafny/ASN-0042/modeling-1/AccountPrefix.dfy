include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module AccountPrefix {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // acct(a): account-field truncation
  // zeros(a) = 0 → acct(a) = a
  // zeros(a) ≥ 1 → acct(a) = a truncated through user field
  function Acct(a: Tumbler): Tumbler {
    var z0 := FindZero(a.components, 0);
    if z0 >= |a.components| then
      a
    else
      var z1 := FindZero(a.components, z0 + 1);
      Tumbler(a.components[..z1])
  }

  // AccountPrefix — (A a ∈ T : T4(a) ⟹ acct(a) ≼ a)
  lemma AccountPrefix(a: Tumbler)
    requires TumblerHierarchy.ValidAddress(a)
    ensures IsPrefix(Acct(a), a)
  { }
}
