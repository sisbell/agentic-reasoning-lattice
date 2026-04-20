include "./TumblerAdd.dfy"
include "./TumblerSub.dfy"

module ReverseInverse {
  // ReverseInverse — SubtractAddInverse

  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import TA = TumblerAdd
  import TS = TumblerSub

  lemma ReverseInverseLemma(a: Tumbler, w: Tumbler)
    requires ValidTumbler(a)
    requires ValidTumbler(w)
    requires TS.GreaterOrEqual(a, w)
    requires IsPositive(w)
    requires TA.ActionPoint(w) == |a.components| - 1
    requires |w.components| == |a.components|
    requires forall i :: 0 <= i < TA.ActionPoint(w) ==> a.components[i] == 0
    ensures TA.TumblerAdd(TS.TumblerSub(a, w), w) == a
  { }
}
