include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"

module TumblerSub {
  // TumblerSub — StartPositionRecovery

  import opened CarrierSetDefinition
  import opened LexicographicOrder

  function Max(a: nat, b: nat): nat {
    if a >= b then a else b
  }

  function Pad(s: seq<nat>, n: nat): seq<nat>
    requires n >= |s|
    ensures |Pad(s, n)| == n
    ensures forall i :: 0 <= i < |s| ==> Pad(s, n)[i] == s[i]
    ensures forall i :: |s| <= i < n ==> Pad(s, n)[i] == 0
  {
    s + seq(n - |s|, _ => 0)
  }

  ghost predicate GreaterOrEqual(a: Tumbler, b: Tumbler) {
    a == b || LessThan(b, a)
  }

  function FindDivergence(s1: seq<nat>, s2: seq<nat>, pos: nat): (k: nat)
    requires |s1| == |s2|
    requires pos <= |s1|
    ensures pos <= k <= |s1|
    ensures forall i :: pos <= i < k ==> s1[i] == s2[i]
    ensures k < |s1| ==> s1[k] != s2[k]
    decreases |s1| - pos
  {
    if pos == |s1| then pos
    else if s1[pos] != s2[pos] then pos
    else FindDivergence(s1, s2, pos + 1)
  }

  function TumblerSub(a: Tumbler, w: Tumbler): (r: Tumbler)
    requires ValidTumbler(a) && ValidTumbler(w)
    requires GreaterOrEqual(a, w)
    ensures |r.components| == Max(|a.components|, |w.components|)
    ensures ValidTumbler(r)
  {
    var len := Max(|a.components|, |w.components|);
    var pa := Pad(a.components, len);
    var pw := Pad(w.components, len);
    var k := FindDivergence(pa, pw, 0);
    if k == len then
      Tumbler(seq(len, _ => 0))
    else
      // Guard: under GreaterOrEqual, pa[k] >= pw[k] at divergence.
      // The guard makes the body unconditionally well-typed;
      // the else branch is unreachable under the precondition.
      Tumbler(seq(len, i requires 0 <= i < len =>
        if i < k then 0
        else if i == k then (if pa[k] >= pw[k] then pa[k] - pw[k] else 0)
        else pa[i]))
  }
}
