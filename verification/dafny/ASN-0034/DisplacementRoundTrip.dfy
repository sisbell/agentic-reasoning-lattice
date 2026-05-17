// ASN-0034: D1 — DisplacementRoundTrip
// When a < b, divergence(a, b) ≤ #a, and #a ≤ #b, then a ⊕ (b ⊖ a) = b.
include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./TumblerAdd.dfy"
include "./TumblerSub.dfy"
include "./Divergence.dfy"
include "./ZeroPaddedDivergence.dfy"
include "./CanonicalRepresentation.dfy"
include "./NatStrictTotalOrder.dfy"
include "./WellDefinedAddition.dfy"

module DisplacementRoundTrip {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened TumblerSub
  import opened Divergence
  import opened ZeroPaddedDivergence
  import opened CanonicalRepresentation
  import opened NatStrictTotalOrder
  import opened NatCarrierSet
  import opened WellDefinedAddition

  // Helper: LexicographicOrder(a, b) implies a != b. (T1 witness rules out equality.)
  lemma LexImpliesNotEqual(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    ensures a != b
  {
    if a == b {
      var kw :| 1 <= kw
                && (forall i :: 1 <= i < kw ==>
                      i <= Length(a) && i <= Length(b) &&
                      Component(a, i) == Component(b, i))
                && ((kw <= Length(a) && kw <= Length(b) && Less(Component(a, kw), Component(b, kw)))
                    || (kw == Length(a) + 1 && kw <= Length(b)));
      if kw <= Length(a) && kw <= Length(b) && Less(Component(a, kw), Component(b, kw)) {
        Irreflexive(Component(a, kw));
      }
    }
  }

  // Helper: from a < b at divergence k ≤ #a ≤ #b, components agree below k
  // and a_k < b_k. Combines T1's witness with Divergence's identification.
  lemma DivergenceCaseIComponents(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires a != b
    requires Divergence.Divergence(a, b) <= Length(a)
    requires Length(a) <= Length(b)
    ensures var k := Divergence.Divergence(a, b);
            1 <= k <= Length(a) &&
            (forall i :: 1 <= i < k ==> Component(a, i) == Component(b, i)) &&
            Component(a, k) < Component(b, k)
  {
    var m := if Length(a) <= Length(b) then Length(a) else Length(b);
    assert m == Length(a);
    var k := Divergence.Divergence(a, b);
    assert k == Divergence.FirstMismatch(a, b, 1, m);
    assert k <= m;
    assert Component(a, k) != Component(b, k);
    var kp :| 1 <= kp
              && (forall i :: 1 <= i < kp ==>
                    i <= Length(a) && i <= Length(b) &&
                    Component(a, i) == Component(b, i))
              && ((kp <= Length(a) && kp <= Length(b) && Less(Component(a, kp), Component(b, kp)))
                  || (kp == Length(a) + 1 && kp <= Length(b)));
    if kp < k {
      assert Component(a, kp) == Component(b, kp);
      if kp <= Length(a) && kp <= Length(b) && Less(Component(a, kp), Component(b, kp)) {
        Irreflexive(Component(a, kp));
      }
    } else if kp > k {
      assert 1 <= k < kp;
      assert Component(a, k) == Component(b, k);
    }
    assert kp == k;
  }

  // Bridge: TumblerSub's componentwise formula via SubComponent.
  // Exposes BuildSubSeq's index-by-index ensures as a usable consequence.
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

  // D1: DisplacementRoundTrip.
  lemma DisplacementRoundTrip(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires Divergence.Divergence(a, b) <= Length(a)
    requires Length(a) <= Length(b)
    ensures
      var w := TumblerSub.TumblerSub(b, a);
      PositiveTumbler.PositiveTumbler(w) && ActionPoint.ActionPoint(w) <= Length(a)
      ==> TumblerAdd.TumblerAdd(a, w) == b
  {
    LexImpliesNotEqual(a, b);
    var k := Divergence.Divergence(a, b);
    Divergence.DivergenceSymmetric(a, b);
    assert Divergence.Divergence(b, a) == k;
    assert k <= Length(a) <= Length(b);
    ZeroPaddedDivergence.ZeroPaddedDivergenceCaseI(b, a);
    assert ZeroPaddedDivergence.ZeroPaddedDivergence(b, a) == k;
    var w := TumblerSub.TumblerSub(b, a);
    assert PositiveTumbler.PositiveTumbler(w);
    assert ActionPoint.ActionPoint(w) == k;
    assert ActionPoint.ActionPoint(w) <= Length(a);
    assert Length(w) == Length(b);
    var r := TumblerAdd.TumblerAdd(a, w);
    assert Length(r) == Length(w) == Length(b);
    TumblerSubComponents(b, a);
    DivergenceCaseIComponents(a, b);
    forall i | 1 <= i <= Length(b)
      ensures Component(r, i) == Component(b, i)
    {
      if i < k {
        assert Component(r, i) == Component(a, i);
        assert Component(a, i) == Component(b, i);
      } else if i == k {
        assert Component(r, k) == Component(a, k) + Component(w, k);
        assert Component(w, k) == SubComponent(b, a, k, k);
        assert PaddedComponent(b, k) == Component(b, k);
        assert PaddedComponent(a, k) == Component(a, k);
        assert Component(b, k) > Component(a, k);
        assert SubComponent(b, a, k, k) == Component(b, k) - Component(a, k);
        assert Component(w, k) == Component(b, k) - Component(a, k);
      } else {
        assert k < i <= Length(w);
        assert Component(r, i) == Component(w, i);
        assert Component(w, i) == SubComponent(b, a, k, i);
        assert SubComponent(b, a, k, i) == PaddedComponent(b, i);
        assert PaddedComponent(b, i) == Component(b, i);
      }
    }
    CanonicalRepresentation.CanonicalRepresentation(r, b);
    assert r == b;
  }
}
