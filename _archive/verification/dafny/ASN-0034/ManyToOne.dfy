include "./TumblerAdd.dfy"
include "./CanonicalRepresentation.dfy"

module ManyToOne {
  // TA-MTO — ManyToOneEquivalence
  // a ⊕ w = b ⊕ w ⟺ (∀ i : 0 ≤ i ≤ actionPoint(w) : aᵢ = bᵢ)

  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import TA = TumblerAdd
  import CanonicalRepresentation

  // Characterize the components of TumblerAdd's result
  lemma TumblerAddComponents(a: Tumbler, w: Tumbler)
    requires ValidTumbler(a)
    requires ValidTumbler(w)
    requires IsPositive(w)
    requires TA.ActionPoint(w) < |a.components|
    ensures var k := TA.ActionPoint(w);
            var r := TA.TumblerAdd(a, w);
            (forall i :: 0 <= i < k ==> r.components[i] == a.components[i]) &&
            r.components[k] == a.components[k] + w.components[k] &&
            (forall i :: k < i < |r.components| ==> r.components[i] == w.components[i])
  {
    var k := TA.ActionPoint(w);
    var r := TA.TumblerAdd(a, w);
    assert r.components == a.components[..k] + [a.components[k] + w.components[k]] + w.components[k+1..];
  }

  lemma ManyToOne(a: Tumbler, b: Tumbler, w: Tumbler)
    requires ValidTumbler(a)
    requires ValidTumbler(b)
    requires ValidTumbler(w)
    requires IsPositive(w)
    requires TA.ActionPoint(w) < |a.components|
    requires TA.ActionPoint(w) < |b.components|
    ensures TA.TumblerAdd(a, w) == TA.TumblerAdd(b, w) <==>
            (forall i :: 0 <= i <= TA.ActionPoint(w) ==> a.components[i] == b.components[i])
  {
    TumblerAddComponents(a, w);
    TumblerAddComponents(b, w);
  }
}
