include "./WellDefinedAddition.dfy"

module PartialInverse {
  // TA4 — PartialInverse
  // (a ⊕ w) ⊖ w = a when action point k = #a, #w = #a, aᵢ = 0 for i < k

  import opened PrefixRelation
  import opened WellDefinedAddition

  function Max(a: nat, b: nat): (r: nat)
    ensures r >= a && r >= b
  {
    if a >= b then a else b
  }

  function ZeroPad(s: seq<nat>, n: nat): (r: seq<nat>)
    requires n >= |s|
    ensures |r| == n
    ensures forall i :: 0 <= i < |s| ==> r[i] == s[i]
    ensures forall i :: |s| <= i < n ==> r[i] == 0
  {
    s + seq(n - |s|, _ => 0)
  }

  function FindDivergence(a: seq<nat>, b: seq<nat>, pos: nat): (k: nat)
    requires |a| == |b|
    requires pos <= |a|
    ensures pos <= k <= |a|
    ensures forall i :: pos <= i < k ==> a[i] == b[i]
    ensures k < |a| ==> a[k] != b[k]
    decreases |a| - pos
  {
    if pos == |a| then pos
    else if a[pos] != b[pos] then pos
    else FindDivergence(a, b, pos + 1)
  }

  predicate Subtractable(a: Tumbler, w: Tumbler) {
    var n := Max(|a.components|, |w.components|);
    var pa := ZeroPad(a.components, n);
    var pw := ZeroPad(w.components, n);
    var k := FindDivergence(pa, pw, 0);
    k == n || pa[k] >= pw[k]
  }

  function TumblerSub(a: Tumbler, w: Tumbler): (r: Tumbler)
    requires ValidTumbler(a) && ValidTumbler(w)
    requires Subtractable(a, w)
    ensures ValidTumbler(r)
    ensures |r.components| == Max(|a.components|, |w.components|)
  {
    var n := Max(|a.components|, |w.components|);
    var pa := ZeroPad(a.components, n);
    var pw := ZeroPad(w.components, n);
    var k := FindDivergence(pa, pw, 0);
    if k == n then
      Tumbler(seq(n, _ => 0))
    else
      Tumbler(seq(k, _ => 0) + [pa[k] - pw[k]] + pa[k+1..])
  }

  lemma PartialInverseLemma(a: Tumbler, w: Tumbler)
    requires ValidTumbler(a) && ValidTumbler(w)
    requires IsPositive(w)
    requires ActionPoint(w) == |a.components| - 1
    requires |w.components| == |a.components|
    requires forall i :: 0 <= i < ActionPoint(w) ==> a.components[i] == 0
    ensures Subtractable(TumblerAdd(a, w), w)
    ensures TumblerSub(TumblerAdd(a, w), w) == a
  { }
}
