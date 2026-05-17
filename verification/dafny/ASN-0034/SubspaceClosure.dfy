// ASN-0034: TA7a — SubspaceClosure
// Defines the subspace S of ordinals with all positive components:
//   S = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}.
// Two closure theorems for ⊕ and ⊖ keep results in S.
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./LexicographicOrder.dfy"
include "./TumblerAdd.dfy"
include "./TumblerSub.dfy"
include "./WellDefinedAddition.dfy"
include "./WellDefinedSubtraction.dfy"
include "./ZeroPaddedDivergence.dfy"
include "./NatStrictTotalOrder.dfy"

module SubspaceClosure {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened PositiveTumbler
  import opened ActionPoint
  import opened LexicographicOrder
  import opened TumblerAdd
  import opened TumblerSub
  import opened WellDefinedAddition
  import opened WellDefinedSubtraction
  import opened ZeroPaddedDivergence
  import opened NatStrictTotalOrder

  ghost predicate InSubspaceS(o: Tumbler)
    requires InT(o)
  {
    forall i :: 1 <= i <= Length(o) ==> Component(o, i) > 0
  }

  ghost function SubspaceS(): iset<Tumbler>
  {
    iset o | InT(o) && InSubspaceS(o)
  }

  // Bridge: TumblerSub's componentwise formula via SubComponent.
  lemma TumblerSubComponents(a: Tumbler, w: Tumbler)
    requires InT(a) && InT(w)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    ensures
      var k := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
      var L := if Length(a) >= Length(w) then Length(a) else Length(w);
      var r := TumblerSub.TumblerSub(a, w);
      Length(r) == L &&
      forall i :: 1 <= i <= L ==>
        Component(r, i) == SubComponent(a, w, k, i)
  { }

  // ⊕-closure conjunct of TA7a.
  // From o ∈ S, w ∈ T, Pos(w), actionPoint(w) ≤ #o, and tail-positivity
  // (w_i > 0 for k ≤ i ≤ #w), conclude o ⊕ w ∈ S with #(o ⊕ w) = #w.
  lemma SubspaceAddClosure(o: Tumbler, w: Tumbler)
    requires InT(o) && InT(w)
    requires InSubspaceS(o)
    requires PositiveTumbler.PositiveTumbler(w)
    requires ActionPoint.ActionPoint(w) <= Length(o)
    requires forall i :: ActionPoint.ActionPoint(w) <= i <= Length(w) ==>
               Component(w, i) > 0
    ensures InT(TumblerAdd.TumblerAdd(o, w))
    ensures Length(TumblerAdd.TumblerAdd(o, w)) == Length(w)
    ensures InSubspaceS(TumblerAdd.TumblerAdd(o, w))
  {
    var k := ActionPoint.ActionPoint(w);
    var r := TumblerAdd.TumblerAdd(o, w);
    assert Length(r) == Length(w);

    forall i | 1 <= i <= Length(r)
      ensures Component(r, i) > 0
    {
      if i < k {
        assert Component(r, i) == Component(o, i);
        assert i < k <= Length(o);
        assert Component(o, i) > 0;
      } else if i == k {
        assert Component(r, k) == Component(o, k) + Component(w, k);
        assert k <= Length(o);
        assert Component(o, k) > 0;
      } else {
        assert k < i <= Length(w);
        assert Component(r, i) == Component(w, i);
        assert Component(w, i) > 0;
      }
    }
  }

  // ⊖-closure conjunct of TA7a.
  // From o ∈ S, w ∈ T, Pos(w), o ≥ w, actionPoint(w) ≤ #o, #w ≤ #o,
  // and o_1 > w_1, conclude o ⊖ w ∈ S with #(o ⊖ w) = #o.
  lemma SubspaceSubClosure(o: Tumbler, w: Tumbler)
    requires InT(o) && InT(w)
    requires InSubspaceS(o)
    requires PositiveTumbler.PositiveTumbler(w)
    requires LexicographicOrder.LexicographicOrder(w, o) || w == o
    requires ActionPoint.ActionPoint(w) <= Length(o)
    requires Length(w) <= Length(o)
    requires Component(o, 1) > Component(w, 1)
    ensures InT(TumblerSub.TumblerSub(o, w))
    ensures Length(TumblerSub.TumblerSub(o, w)) == Length(o)
    ensures InSubspaceS(TumblerSub.TumblerSub(o, w))
  {
    var r := TumblerSub.TumblerSub(o, w);
    var L := if Length(o) >= Length(w) then Length(o) else Length(w);
    assert L == Length(o);
    assert Length(r) == L;

    // zpd(o, w) = 1 from o_1 > w_1 (so padded(o,1) != padded(w,1)).
    assert PaddedComponent(o, 1) == Component(o, 1);
    assert PaddedComponent(w, 1) == Component(w, 1);
    assert PaddedComponent(o, 1) != PaddedComponent(w, 1);
    var k := ZeroPaddedDivergence.ZeroPaddedDivergence(o, w);
    assert FirstPaddedMismatch(o, w, 1, L) == 1;
    assert k == 1;

    TumblerSubComponents(o, w);

    forall i | 1 <= i <= Length(r)
      ensures Component(r, i) > 0
    {
      assert Component(r, i) == SubComponent(o, w, k, i);
      if i == 1 {
        assert Component(r, 1) ==
          SatSub(PaddedComponent(o, 1), PaddedComponent(w, 1));
        assert PaddedComponent(o, 1) > PaddedComponent(w, 1);
        assert SatSub(PaddedComponent(o, 1), PaddedComponent(w, 1))
            == PaddedComponent(o, 1) - PaddedComponent(w, 1);
        assert Component(o, 1) > Component(w, 1);
      } else {
        assert i > 1;
        assert i > k;
        assert Component(r, i) == PaddedComponent(o, i);
        assert i <= Length(o);
        assert PaddedComponent(o, i) == Component(o, i);
        assert Component(o, i) > 0;
      }
    }
  }
}
