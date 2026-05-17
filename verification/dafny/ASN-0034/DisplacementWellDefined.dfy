// ASN-0034: D0 — DisplacementWellDefined
// Corollary packaging the well-formedness consequences of a < b ∧ divergence ≤ #a:
//   b ⊖ a ∈ T, Pos(b ⊖ a), actionPoint(b ⊖ a) = divergence(a, b),
//   #(b ⊖ a) = max(#a, #b), a ⊕ (b ⊖ a) ∈ T, and #a > #b ⇒ a ⊕ (b ⊖ a) ≠ b.
include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./TumblerAdd.dfy"
include "./TumblerSub.dfy"
include "./Divergence.dfy"
include "./ZeroPaddedDivergence.dfy"
include "./CanonicalRepresentation.dfy"
include "./WellDefinedAddition.dfy"
include "./NatStrictTotalOrder.dfy"

module DisplacementWellDefined {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened TumblerSub
  import opened Divergence
  import opened ZeroPaddedDivergence
  import opened CanonicalRepresentation
  import opened WellDefinedAddition
  import opened NatStrictTotalOrder
  import opened NatCarrierSet

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

  // Helper: from a < b and divergence(a, b) ≤ #a, divergence ≤ #b also.
  // When #b < #a, the only way divergence > #b is FirstMismatch returning #b + 1
  // (components agree on [1, #b]). But T1's witness must either disagree somewhere
  // in [1, min(#a, #b)] = [1, #b] (Case (i) — contradicts agreement) or fall in
  // Case (ii) requiring #a + 1 ≤ #b (contradicts #b < #a).
  lemma DivergenceBoundedByB(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires a != b
    requires Divergence.Divergence(a, b) <= Length(a)
    ensures Divergence.Divergence(a, b) <= Length(b)
  {
    var k := Divergence.Divergence(a, b);
    if Length(b) < Length(a) {
      var m := Length(b);
      assert k == Divergence.FirstMismatch(a, b, 1, m);
      assert k <= m + 1;
      if k > Length(b) {
        assert k == m + 1;
        assert forall i :: 1 <= i < k ==> Component(a, i) == Component(b, i);
        var kw :| 1 <= kw
                  && (forall i :: 1 <= i < kw ==>
                        i <= Length(a) && i <= Length(b) &&
                        Component(a, i) == Component(b, i))
                  && ((kw <= Length(a) && kw <= Length(b) && Less(Component(a, kw), Component(b, kw)))
                      || (kw == Length(a) + 1 && kw <= Length(b)));
        if kw <= Length(a) && kw <= Length(b) && Less(Component(a, kw), Component(b, kw)) {
          assert kw <= Length(b) < k;
          assert Component(a, kw) == Component(b, kw);
          Irreflexive(Component(a, kw));
        }
      }
    }
  }

  lemma DisplacementWellDefined(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires Divergence.Divergence(a, b) <= Length(a)
    ensures
      var w := TumblerSub.TumblerSub(b, a);
      var k := Divergence.Divergence(a, b);
      InT(w) &&
      Length(w) == (if Length(a) >= Length(b) then Length(a) else Length(b)) &&
      PositiveTumbler.PositiveTumbler(w) &&
      ActionPoint.ActionPoint(w) == k &&
      ActionPoint.ActionPoint(w) <= Length(a) &&
      InT(TumblerAdd.TumblerAdd(a, w)) &&
      (Length(a) > Length(b) ==> TumblerAdd.TumblerAdd(a, w) != b)
  {
    LexImpliesNotEqual(a, b);
    DivergenceBoundedByB(a, b);
    var k := Divergence.Divergence(a, b);
    Divergence.DivergenceSymmetric(a, b);
    assert Divergence.Divergence(b, a) == k;
    ZeroPaddedDivergence.ZeroPaddedDivergenceCaseI(b, a);
    assert ZeroPaddedDivergence.ZeroPaddedDivergence(b, a) == k;
    var w := TumblerSub.TumblerSub(b, a);
    assert PositiveTumbler.PositiveTumbler(w);
    assert ActionPoint.ActionPoint(w) == k;
    WellDefinedAddition.WellDefinedAddition(a, w);
    var r := TumblerAdd.TumblerAdd(a, w);
    if Length(a) > Length(b) {
      assert Length(w) == Length(a);
      assert Length(r) == Length(w) == Length(a);
      assert Length(r) != Length(b);
      CanonicalRepresentation.CanonicalRepresentation(r, b);
    }
  }
}
