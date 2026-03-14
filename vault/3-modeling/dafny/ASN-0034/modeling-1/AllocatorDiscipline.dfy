include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module AllocatorDiscipline {

  import opened TumblerAlgebra

  // ---------------------------------------------------------------------------
  // LastSig — 0-indexed position of last nonzero component
  // ---------------------------------------------------------------------------

  function LastSigRec(s: seq<nat>, i: nat): nat
    requires 0 < i <= |s|
    requires exists j :: 0 <= j < i && s[j] != 0
    ensures LastSigRec(s, i) < i
    ensures s[LastSigRec(s, i)] != 0
    ensures forall j :: LastSigRec(s, i) < j < i ==> s[j] == 0
    decreases i
  {
    if s[i-1] != 0 then i - 1
    else LastSigRec(s, i - 1)
  }

  function LastSig(t: Tumbler): nat
    requires PositiveTumbler(t)
    requires |t.components| > 0
    ensures LastSig(t) < |t.components|
    ensures t.components[LastSig(t)] != 0
    ensures forall j :: LastSig(t) < j < |t.components| ==> t.components[j] == 0
  {
    LastSigRec(t.components, |t.components|)
  }

  // If position s is the last nonzero, LastSig returns s
  lemma LastSigIs(t: Tumbler, s: nat)
    requires |t.components| > 0
    requires s < |t.components|
    requires t.components[s] != 0
    requires forall j :: s < j < |t.components| ==> t.components[j] == 0
    ensures PositiveTumbler(t)
    ensures LastSig(t) == s
  { }

  // ---------------------------------------------------------------------------
  // Inc — hierarchical increment (TA5)
  // k=0: sibling — increment at LastSig, same length
  // k>0: child — extend with k-1 zero separators and child value 1
  // ---------------------------------------------------------------------------

  function Inc(t: Tumbler, k: nat): Tumbler
    requires PositiveTumbler(t)
    requires |t.components| > 0
    ensures |Inc(t, k).components| == (if k == 0 then |t.components| else |t.components| + k)
  {
    if k == 0 then
      var s := LastSig(t);
      Tumbler(t.components[..s] + [t.components[s] + 1] + t.components[s+1..])
    else
      Tumbler(t.components + Zeros(k - 1) + [1])
  }

  // T10a — AllocatorDiscipline
  // Protocol constraint on inc usage: sibling inc preserves length and
  // operating level; spawn inc extends length and deepens level.
  ghost predicate AllocatorDiscipline(t: Tumbler, k: nat)
    requires PositiveTumbler(t)
    requires |t.components| > 0
  {
    var r := Inc(t, k);
    PositiveTumbler(r) && |r.components| > 0 &&
    (k == 0 ==> |r.components| == |t.components| && LastSig(r) == LastSig(t)) &&
    (k > 0 ==> |r.components| == |t.components| + k && LastSig(r) > LastSig(t))
  }

  lemma AllocatorDisciplineHolds(t: Tumbler, k: nat)
    requires PositiveTumbler(t)
    requires |t.components| > 0
    ensures AllocatorDiscipline(t, k)
  {
    var r := Inc(t, k);
    var s := LastSig(t);
    if k == 0 {
      assert r.components[s] == t.components[s] + 1;
      LastSigIs(r, s);
    } else {
      var last := |r.components| - 1;
      assert r.components[last] == 1;
    }
  }
}
