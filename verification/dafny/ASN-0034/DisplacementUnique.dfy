// ASN-0034: D2 — DisplacementUnique (corollary)
// Under D1's preconditions (a < b, divergence(a, b) ≤ #a, #a ≤ #b),
// for any w ∈ T with Pos(w) and actionPoint(w) ≤ #a such that a ⊕ w = b,
// we have w = b ⊖ a.
include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./TumblerAdd.dfy"
include "./TumblerSub.dfy"
include "./Divergence.dfy"
include "./ZeroPaddedDivergence.dfy"
include "./DisplacementRoundTrip.dfy"
include "./LeftCancellation.dfy"

module DisplacementUnique {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened TumblerSub
  import opened Divergence
  import opened ZeroPaddedDivergence
  import opened DisplacementRoundTrip
  import opened LeftCancellation

  lemma DisplacementUnique(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires Divergence.Divergence(a, b) <= Length(a)
    requires Length(a) <= Length(b)
    requires PositiveTumbler.PositiveTumbler(w)
    requires ActionPoint.ActionPoint(w) <= Length(a)
    requires TumblerAdd.TumblerAdd(a, w) == b
    ensures w == TumblerSub.TumblerSub(b, a)
  {
    // Establish a != b and identify k = Divergence(a, b) = ZPD(b, a).
    DisplacementRoundTrip.LexImpliesNotEqual(a, b);
    var k := Divergence.Divergence(a, b);
    Divergence.DivergenceSymmetric(a, b);
    ZeroPaddedDivergence.ZeroPaddedDivergenceCaseI(b, a);
    assert ZeroPaddedDivergence.ZeroPaddedDivergence(b, a) == k;
    // Second witness w' = b ⊖ a is positive with action point k ≤ #a.
    var wprime := TumblerSub.TumblerSub(b, a);
    assert PositiveTumbler.PositiveTumbler(wprime);
    assert ActionPoint.ActionPoint(wprime) == k;
    // D1 closes the loop: a ⊕ w' = b.
    DisplacementRoundTrip.DisplacementRoundTrip(a, b);
    assert TumblerAdd.TumblerAdd(a, wprime) == b;
    // Left cancellation: a ⊕ w = b = a ⊕ w' ⇒ w = w'.
    LeftCancellation.LeftCancellation(a, w, wprime);
  }
}
