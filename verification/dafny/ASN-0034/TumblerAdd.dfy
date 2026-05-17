// ASN-0034: TumblerAdd — definition (DEF)
// Tumbler addition a ⊕ w, defined component-wise:
//   k = actionPoint(w); rᵢ = aᵢ if i < k; rₖ = aₖ + wₖ; rᵢ = wᵢ if i > k.
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"

module TumblerAdd {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened NatCarrierSet

  function TumblerAdd(a: Tumbler, w: Tumbler): (r: Tumbler)
    requires InT(a) && InT(w)
    requires PositiveTumbler.PositiveTumbler(w)
    requires ActionPoint.ActionPoint(w) <= Length(a)
    ensures InT(r)
    ensures Length(r) == Length(w)
    ensures forall i :: 1 <= i < ActionPoint.ActionPoint(w) ==>
              Component(r, i) == Component(a, i)
    ensures Component(r, ActionPoint.ActionPoint(w)) ==
              Component(a, ActionPoint.ActionPoint(w)) +
              Component(w, ActionPoint.ActionPoint(w))
    ensures forall i :: ActionPoint.ActionPoint(w) < i <= Length(w) ==>
              Component(r, i) == Component(w, i)
  {
    var k := ActionPoint.ActionPoint(w);
    Tumbler(a.components[..k-1]
            + [a.components[k-1] + w.components[k-1]]
            + w.components[k..])
  }
}
