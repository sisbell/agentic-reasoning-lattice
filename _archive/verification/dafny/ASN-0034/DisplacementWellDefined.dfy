include "./Divergence.dfy"
include "./TumblerAdd.dfy"
include "./TumblerSub.dfy"

module DisplacementWellDefined {
  // D0 — DisplacementWellDefined
  // Under a < b and divergence(a, b) ≤ #a, the displacement w = b ⊖ a
  // is a well-defined positive tumbler whose action point equals
  // divergence(a, b), and a ⊕ w is well-defined.

  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened PositiveTumbler
  import Div = Divergence
  import TA = TumblerAdd
  import TS = TumblerSub

  lemma DisplacementWellDefined(a: Tumbler, b: Tumbler)
    requires ValidTumbler(a) && ValidTumbler(b)
    requires LessThan(a, b)
    requires Div.Divergence(a, b) <= |a.components|
    ensures ValidTumbler(TS.TumblerSub(b, a))
    ensures IsPositive(TS.TumblerSub(b, a))
    ensures TA.ActionPoint(TS.TumblerSub(b, a)) + 1 == Div.Divergence(a, b)
    ensures |TS.TumblerSub(b, a).components| == TS.Max(|a.components|, |b.components|)
    ensures ValidTumbler(TA.TumblerAdd(a, TS.TumblerSub(b, a)))
    ensures |a.components| > |b.components| ==> TA.TumblerAdd(a, TS.TumblerSub(b, a)) != b
  {
    FirstDivergenceProperties(a.components, b.components, 0);
    var div0 := FirstDivergence(a.components, b.components, 0);
    var w := TS.TumblerSub(b, a);
    assert div0 < |w.components| && w.components[div0] != 0;
  }
}
