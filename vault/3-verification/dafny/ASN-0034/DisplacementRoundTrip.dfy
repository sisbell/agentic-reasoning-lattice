include "./DisplacementWellDefined.dfy"

module DisplacementRoundTrip {
  // D1 — DisplacementRoundTrip

  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened PositiveTumbler
  import D0 = DisplacementWellDefined
  import Div = Divergence
  import TA = TumblerAdd
  import TS = TumblerSub

  lemma DisplacementRoundTrip(a: Tumbler, b: Tumbler)
    requires ValidTumbler(a) && ValidTumbler(b)
    requires LessThan(a, b)
    requires Div.Divergence(a, b) <= |a.components|
    requires |a.components| <= |b.components|
    ensures var d := TS.TumblerSub(b, a);
            IsPositive(d) && TA.ActionPoint(d) < |a.components| && TA.TumblerAdd(a, d) == b
  {
    D0.DisplacementWellDefined(a, b);
    FirstDivergenceProperties(a.components, b.components, 0);
  }
}
