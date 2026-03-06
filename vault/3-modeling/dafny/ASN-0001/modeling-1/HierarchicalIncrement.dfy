include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module HierarchicalIncrement {

  import opened TumblerAlgebra

  // ASN-0001 TA5 — HierarchicalIncrement

  // ---------------------------------------------------------------------------
  // LastSignificantPosition — last nonzero component index (0-indexed).
  // For zero tumblers, returns the last index.
  // ---------------------------------------------------------------------------

  function FindLastNonzero(s: seq<nat>, i: nat): (r: int)
    requires i < |s|
    ensures -1 <= r <= i
    ensures r >= 0 ==> s[r] != 0
    ensures r < 0 ==> forall j :: 0 <= j <= i ==> s[j] == 0
    decreases i
  {
    if s[i] != 0 then i
    else if i == 0 then -1
    else FindLastNonzero(s, i - 1)
  }

  function LastSig(t: Tumbler): (s: nat)
    requires |t.components| > 0
    ensures s < |t.components|
  {
    var r := FindLastNonzero(t.components, |t.components| - 1);
    if r >= 0 then r else |t.components| - 1
  }

  // ---------------------------------------------------------------------------
  // Inc — hierarchical increment at level k
  //
  // k = 0: sibling increment (advance at last significant position)
  // k > 0: child spawn (append k-1 separators and first child)
  // ---------------------------------------------------------------------------

  function Inc(t: Tumbler, k: nat): Tumbler
    requires |t.components| > 0
  {
    if k == 0 then
      var s := LastSig(t);
      Tumbler(t.components[..s] + [t.components[s] + 1] + t.components[s+1..])
    else
      Tumbler(t.components + Zeros(k - 1) + [1])
  }

  // Bridge: proper prefix implies LessThan
  lemma LessThanByPrefix(a: Tumbler, b: Tumbler)
    requires |a.components| < |b.components|
    requires forall i :: 0 <= i < |a.components| ==> a.components[i] == b.components[i]
    ensures LessThan(a, b)
  {
    LessThanIntro(a, b, |a.components|);
  }

  // (a) Strict increase: inc(t, k) > t under LessThan
  lemma IncStrictIncrease(t: Tumbler, k: nat)
    requires |t.components| > 0
    ensures LessThan(t, Inc(t, k))
  {
    var t' := Inc(t, k);
    if k == 0 {
      var s := LastSig(t);
      assert t.components[s] < t'.components[s];
    } else {
      LessThanByPrefix(t, t');
    }
  }

  // (b,c) Sibling properties (k = 0): same length, differs only at sig(t)
  lemma IncSiblingProperties(t: Tumbler)
    requires |t.components| > 0
    ensures |Inc(t, 0).components| == |t.components|
    ensures Inc(t, 0).components[LastSig(t)] == t.components[LastSig(t)] + 1
    ensures forall i :: 0 <= i < |t.components| && i != LastSig(t) ==>
      Inc(t, 0).components[i] == t.components[i]
  { }

  // (b,d) Child properties (k > 0): extended, separators, first child
  lemma IncChildProperties(t: Tumbler, k: nat)
    requires |t.components| > 0
    requires k > 0
    ensures |Inc(t, k).components| == |t.components| + k
    ensures forall i :: 0 <= i < |t.components| ==>
      Inc(t, k).components[i] == t.components[i]
    ensures forall i :: |t.components| <= i < |t.components| + k - 1 ==>
      Inc(t, k).components[i] == 0
    ensures Inc(t, k).components[|t.components| + k - 1] == 1
  { }
}
