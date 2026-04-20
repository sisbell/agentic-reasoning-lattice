include "./LexicographicOrder.dfy"
include "./LastSignificantPosition.dfy"

module HierarchicalIncrement {
  // TA5 — HierarchicalIncrement (DEF)
  // inc(t, k): when k = 0, increment at sig(t); when k > 0, extend by k positions

  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import LSP = LastSignificantPosition

  // Bridge: sig position using CarrierSetDefinition.Tumbler
  function SigPos(t: Tumbler): (p: nat)
    requires ValidTumbler(t)
    ensures p < |t.components|
  {
    LSP.Sig(LSP.Tumbler(t.components))
  }

  method Inc(t: Tumbler, k: nat) returns (t': Tumbler)
    requires ValidTumbler(t)
    ensures ValidTumbler(t')
    // (a) strict increase under T1
    ensures LessThan(t, t')
    // (b,c) k = 0: length preserved, differs only at sig(t), incremented by 1
    ensures k == 0 ==> |t'.components| == |t.components|
    ensures k == 0 ==> t'.components[SigPos(t)] == t.components[SigPos(t)] + 1
    ensures k == 0 ==> forall i :: 0 <= i < |t.components| && i != SigPos(t) ==> t'.components[i] == t.components[i]
    // (b,d) k > 0: length = #t + k, original preserved, k-1 zeros, final 1
    ensures k > 0 ==> |t'.components| == |t.components| + k
    ensures k > 0 ==> forall i :: 0 <= i < |t.components| ==> t'.components[i] == t.components[i]
    ensures k > 0 ==> forall i :: |t.components| <= i < |t.components| + k - 1 ==> t'.components[i] == 0
    ensures k > 0 ==> t'.components[|t.components| + k - 1] == 1
  {
    var s := t.components;
    if k == 0 {
      var p := SigPos(t);
      t' := Tumbler(s[..p] + [s[p] + 1] + s[p+1..]);
      LessThanTrichotomy(t, t');
      assert t'.components[p] > t.components[p];
    } else {
      t' := Tumbler(s + seq(k - 1, _ => 0) + [1]);
      LessThanTrichotomy(t, t');
      assert |t.components| < |t'.components|;
      assert forall i :: 0 <= i < |t.components| ==> t.components[i] == t'.components[i];
    }
  }
}
