include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module HierarchicalIncrement {
  import opened TumblerAlgebra

  // TA5 — HierarchicalIncrement

  // Last significant position (0-indexed): index of last nonzero component,
  // or last index when all components are zero.
  function LastSigRec(s: seq<nat>, i: nat, top: nat): nat
    requires i < |s|
    requires top < |s|
    requires i <= top
    ensures LastSigRec(s, i, top) <= top
    decreases i
  {
    if s[i] != 0 then i
    else if i == 0 then top
    else LastSigRec(s, i - 1, top)
  }

  function LastSig(t: Tumbler): nat
    requires |t.components| >= 1
    ensures LastSig(t) < |t.components|
  {
    LastSigRec(t.components, |t.components| - 1, |t.components| - 1)
  }

  // inc(t, k): hierarchical increment at level k
  function Inc(t: Tumbler, k: nat): (t': Tumbler)
    requires |t.components| >= 1
    // (c) sibling (k = 0): same length, increment at LastSig(t)
    ensures k == 0 ==> |t'.components| == |t.components|
    ensures k == 0 ==> t'.components[LastSig(t)] == t.components[LastSig(t)] + 1
    ensures k == 0 ==> forall i :: 0 <= i < |t.components| && i != LastSig(t) ==>
              t'.components[i] == t.components[i]
    // (d) child (k > 0): extend by k, prefix preserved, separators, final 1
    ensures k > 0 ==> |t'.components| == |t.components| + k
    ensures k > 0 ==> forall i :: 0 <= i < |t.components| ==>
              t'.components[i] == t.components[i]
    ensures k > 0 ==> forall i :: |t.components| <= i < |t.components| + k - 1 ==>
              t'.components[i] == 0
    ensures k > 0 ==> t'.components[|t.components| + k - 1] == 1
  {
    if k == 0 then
      var s := LastSig(t);
      Tumbler(t.components[..s] + [t.components[s] + 1] + t.components[s+1..])
    else
      Tumbler(t.components + Zeros(k - 1) + [1])
  }

  // (a) inc(t, k) is strictly greater than t under T1
  lemma IncStrictlyGreater(t: Tumbler, k: nat)
    requires |t.components| >= 1
    ensures LessThan(t, Inc(t, k))
  {
    if k == 0 {
      LessThanIntro(t, Inc(t, 0), LastSig(t));
    } else {
      LessThanIntro(t, Inc(t, k), |t.components|);
    }
  }
}
