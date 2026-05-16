include "./DisplacementWellDefined.dfy"
include "./LeftCancellation.dfy"

module DisplacementUnique {
  // D2 — DisplacementUnique
  // Under D1 preconditions, if a ⊕ w = b then w = b ⊖ a.
  // Corollary of D1 (round-trip) and TA-LC (left cancellation).

  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened PositiveTumbler
  import D0 = DisplacementWellDefined
  import Div = Divergence
  import TA = TumblerAdd
  import TS = TumblerSub
  import LC = LeftCancellation

  // D1 — Displacement round-trip: a ⊕ (b ⊖ a) = b
  lemma DisplacementRoundTrip(a: Tumbler, b: Tumbler)
    requires ValidTumbler(a) && ValidTumbler(b)
    requires LessThan(a, b)
    requires Div.Divergence(a, b) <= |a.components|
    requires |a.components| <= |b.components|
    requires IsPositive(TS.TumblerSub(b, a))
    requires TA.ActionPoint(TS.TumblerSub(b, a)) < |a.components|
    ensures TA.TumblerAdd(a, TS.TumblerSub(b, a)) == b
  {
    D0.DisplacementWellDefined(a, b);
    FirstDivergenceProperties(a.components, b.components, 0);

    var div0 := FirstDivergence(a.components, b.components, 0);
    var w := TS.TumblerSub(b, a);
    var k := TA.ActionPoint(w);
    var r := TA.TumblerAdd(a, w);

    // k equals the 0-indexed divergence point (from D0)
    assert k == div0;

    // Prefix: a and b agree before divergence
    assert a.components[..k] == b.components[..k];

    // At k: from LessThan, a[k] < b[k]; TumblerSub gives w[k] = b[k] - a[k]
    assert k < |a.components| && k < |b.components|;
    assert a.components[k] < b.components[k];
  }

  lemma DisplacementUnique(a: Tumbler, b: Tumbler, w: Tumbler)
    requires ValidTumbler(a) && ValidTumbler(b) && ValidTumbler(w)
    requires LessThan(a, b)
    requires Div.Divergence(a, b) <= |a.components|
    requires |a.components| <= |b.components|
    requires IsPositive(w) && TA.ActionPoint(w) < |a.components| && TA.TumblerAdd(a, w) == b
    ensures w == TS.TumblerSub(b, a)
  {
    D0.DisplacementWellDefined(a, b);
    DisplacementRoundTrip(a, b);
    LC.LeftCancellation(a, w, TS.TumblerSub(b, a));
  }
}
