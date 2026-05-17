// ASN-0034: TA-RC — RightCancellationFailure
// ∃ a, b, w ∈ T : Pos(w) ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b
//   ∧ a ≠ b ∧ a ⊕ w = b ⊕ w.
// Witnesses: a = [1,3,5], b = [1,3,7], w = [0,2,4].
// ActionPoint(w) = 2; both a ⊕ w and b ⊕ w equal [1,5,4].
include "./TumblerAdd.dfy"
include "./WellDefinedAddition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"

module RightCancellationFailure {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened NatCarrierSet

  lemma RightCancellationFailure()
    ensures exists a: Tumbler, b: Tumbler, w: Tumbler ::
      InT(a) && InT(b) && InT(w) &&
      PositiveTumbler.PositiveTumbler(w) &&
      ActionPoint.ActionPoint(w) <= Length(a) &&
      ActionPoint.ActionPoint(w) <= Length(b) &&
      a != b &&
      TumblerAdd.TumblerAdd(a, w) == TumblerAdd.TumblerAdd(b, w)
  {
    var a := Tumbler([1, 3, 5]);
    var b := Tumbler([1, 3, 7]);
    var w := Tumbler([0, 2, 4]);

    assert InT(a) && InT(b) && InT(w);

    // Pos(w): witness i = 2, Component(w, 2) = 2 != 0.
    assert Component(w, 2) == 2;
    assert PositiveTumbler.PositiveTumbler(w);

    // ActionPoint(w) = 2: Component(w, 1) = 0 and Component(w, 2) != 0.
    assert Component(w, 1) == 0;
    assert ActionPoint.ActionPoint(w) == 2;

    assert Length(a) == 3 && Length(b) == 3;
    assert a != b;

    // a ⊕ w and b ⊕ w both equal Tumbler([1, 5, 4]).
    var ra := TumblerAdd.TumblerAdd(a, w);
    var rb := TumblerAdd.TumblerAdd(b, w);
    assert ra == rb;
  }
}
