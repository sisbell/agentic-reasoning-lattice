// ASN-0034: TA-MTO — ManyToOne
// For displacement w and tumblers a, b with #a ≥ k and #b ≥ k (k = actionPoint(w)):
//   a ⊕ w = b ⊕ w ⟺ (∀ i : 1 ≤ i ≤ k : aᵢ = bᵢ).
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./TumblerAdd.dfy"
include "./WellDefinedAddition.dfy"
include "./CanonicalRepresentation.dfy"
include "./NatAdditionCancellation.dfy"

module ManyToOne {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened WellDefinedAddition
  import opened CanonicalRepresentation
  import opened NatAdditionCancellation
  import opened NatCarrierSet

  lemma ManyToOne(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires PositiveTumbler.PositiveTumbler(w)
    requires ActionPoint.ActionPoint(w) <= Length(a)
    requires ActionPoint.ActionPoint(w) <= Length(b)
    ensures TumblerAdd.TumblerAdd(a, w) == TumblerAdd.TumblerAdd(b, w) <==>
      (forall i :: 1 <= i <= ActionPoint.ActionPoint(w) ==>
        Component(a, i) == Component(b, i))
  {
    var k := ActionPoint.ActionPoint(w);
    var ra := TumblerAdd.TumblerAdd(a, w);
    var rb := TumblerAdd.TumblerAdd(b, w);

    // Forward: prefix agreement up to k implies equal results.
    if forall i :: 1 <= i <= k ==> Component(a, i) == Component(b, i) {
      assert Length(ra) == Length(w) == Length(rb);
      forall i | 1 <= i <= Length(ra)
        ensures Component(ra, i) == Component(rb, i)
      {
        if i < k {
          // prefix-copy: ra_i = a_i = b_i = rb_i
        } else if i == k {
          // advance: ra_k = a_k + w_k = b_k + w_k = rb_k
        } else {
          // tail-copy: ra_i = w_i = rb_i
        }
      }
      CanonicalRepresentation.CanonicalRepresentation(ra, rb);
    }

    // Converse: equal results implies prefix agreement up to k.
    if ra == rb {
      forall i | 1 <= i <= k
        ensures Component(a, i) == Component(b, i)
      {
        if i < k {
          // prefix-copy gives ra_i = a_i and rb_i = b_i; equal results yield a_i = b_i
        } else {
          // i == k: advance yields a_k + w_k = b_k + w_k; cancel on the right
          NatAdditionCancellation.NatAdditionRightCancellation(
            Component(a, k), Component(b, k), Component(w, k));
        }
      }
    }
  }
}
