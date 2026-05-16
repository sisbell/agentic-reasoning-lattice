include "./TumblerSub.dfy"

module WellDefinedSubtraction {
  // TA2 — WellDefinedSubtraction

  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import TS = TumblerSub

  lemma WellDefinedSubtraction(a: Tumbler, w: Tumbler)
    requires ValidTumbler(a) && ValidTumbler(w)
    requires TS.GreaterOrEqual(a, w)
    ensures ValidTumbler(TS.TumblerSub(a, w))
  { }
}
