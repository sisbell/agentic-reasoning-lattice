// ASN-0034: T0(a) — UnboundedComponentValues
// For every tumbler t ∈ T, every component position i with 1 ≤ i ≤ #t,
// and every bound M ∈ ℕ, there exists t' ∈ T with #t' = #t that agrees
// with t at all positions except i, where t'.dᵢ > M.
include "./CarrierSetDefinition.dfy"

module UnboundedComponentValues {
  import opened CarrierSetDefinition
  import opened NatCarrierSet

  lemma UnboundedComponentValues(t: Tumbler, i: nat, M: nat)
    requires InT(t)
    requires 1 <= i <= Length(t)
    ensures exists tp: Tumbler ::
      InT(tp) &&
      Length(tp) == Length(t) &&
      Component(tp, i) > M &&
      (forall j :: 1 <= j <= Length(t) && j != i ==>
         Component(tp, j) == Component(t, j))
  {
    var r: nat -> Carrier := (j: nat) =>
      if 1 <= j <= |t.components| then
        (if j == i then M + 1 else t.components[j - 1])
      else 0;
    Comprehension(Length(t), r);
  }
}
