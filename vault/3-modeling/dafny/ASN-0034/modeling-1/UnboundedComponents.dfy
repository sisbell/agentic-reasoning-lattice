include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module UnboundedComponents {
  import opened TumblerAlgebra

  // T0(a) — UnboundedComponents
  // (A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: t' agrees with t except t'.dᵢ > M)))

  // Constructive witness: replace component i with value v
  function WithComponent(t: Tumbler, i: nat, v: nat): Tumbler
    requires 0 <= i < |t.components|
    ensures |WithComponent(t, i, v).components| == |t.components|
    ensures WithComponent(t, i, v).components[i] == v
    ensures forall j :: 0 <= j < |t.components| && j != i ==>
              WithComponent(t, i, v).components[j] == t.components[j]
  {
    Tumbler(t.components[..i] + [v] + t.components[i+1..])
  }

  // Components are unbounded: for any tumbler t, position i, and bound M,
  // there exists a tumbler agreeing with t everywhere except at i, where it exceeds M.
  lemma UnboundedComponents(t: Tumbler, i: nat, M: nat)
    requires 0 <= i < |t.components|
    ensures exists t': Tumbler ::
      |t'.components| == |t.components| &&
      t'.components[i] > M &&
      (forall j :: 0 <= j < |t.components| && j != i ==>
         t'.components[j] == t.components[j])
  {
    var t' := WithComponent(t, i, M + 1);
  }
}
