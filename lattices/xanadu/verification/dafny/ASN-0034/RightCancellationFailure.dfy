include "./TumblerAdd.dfy"
include "./CanonicalRepresentation.dfy"

module RightCancellationFailure {
  // TA-RC — RightCancellationFailure
  // ∃ a, b, w ∈ T : w > 0 ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b ∧ a ≠ b ∧ a ⊕ w = b ⊕ w

  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import TA = TumblerAdd
  import CanonicalRepresentation

  lemma RightCancellationFailure()
    ensures exists a: Tumbler, b: Tumbler, w: Tumbler ::
      ValidTumbler(a) && ValidTumbler(b) && ValidTumbler(w) &&
      IsPositive(w) &&
      TA.ActionPoint(w) < |a.components| &&
      TA.ActionPoint(w) < |b.components| &&
      a != b &&
      TA.TumblerAdd(a, w) == TA.TumblerAdd(b, w)
  {
    var a := Tumbler([1, 3, 5]);
    var b := Tumbler([1, 3, 7]);
    var w := Tumbler([0, 2, 4]);
    assert IsPositive(w) by { assert w.components[1] != 0; }
    assert TA.TumblerAdd(a, w) == TA.TumblerAdd(b, w);
  }
}
