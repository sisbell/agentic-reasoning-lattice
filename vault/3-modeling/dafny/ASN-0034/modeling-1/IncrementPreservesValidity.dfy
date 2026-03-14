include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "ValidAddress.dfy"
include "HierarchicalIncrement.dfy"

// (TA5 preserves T4) — IncrementPreservesValidity
module IncrementPreservesValidity {
  import opened TumblerAlgebra
  import VA = ValidAddress
  import opened HierarchicalIncrement

  lemma ZeroCountConcat(a: seq<nat>, b: seq<nat>)
    ensures VA.ZeroCount(a + b) == VA.ZeroCount(a) + VA.ZeroCount(b)
    decreases |a|
  {
    if |a| == 0 {
      assert a + b == b;
    } else {
      assert (a + b)[1..] == a[1..] + b;
      ZeroCountConcat(a[1..], b);
    }
  }

  // When the last element is nonzero, ZeroCount of the whole equals ZeroCount of the prefix
  lemma ZeroCountNonzeroLast(s: seq<nat>)
    requires |s| >= 1
    requires s[|s| - 1] != 0
    ensures VA.ZeroCount(s) == VA.ZeroCount(s[..|s| - 1])
  {
    assert s == s[..|s| - 1] + [s[|s| - 1]];
    ZeroCountConcat(s[..|s| - 1], [s[|s| - 1]]);
  }

  lemma IncrementPreservesValidity(t: Tumbler, k: nat)
    requires VA.ValidAddress(t)
    requires k <= 2
    requires k >= 1 ==> VA.ZeroCount(t.components) + k <= 4
    ensures VA.ValidAddress(Inc(t, k))
  {
    if k == 0 {
      var s := LastSig(t);
      var tc := t.components;
      var rc := Inc(t, 0).components;
      // T4 implies last component nonzero, so LastSig = last index
      ZeroCountNonzeroLast(tc);
      assert rc == tc[..s] + [tc[s] + 1] + tc[s+1..];
      ZeroCountConcat(tc[..s], [tc[s] + 1]);
      ZeroCountConcat(tc[..s] + [tc[s] + 1], tc[s+1..]);
    } else if k == 1 {
      assert Zeros(0) == [];
      assert Inc(t, 1).components == t.components + [1];
      ZeroCountConcat(t.components, [1]);
    } else {
      assert Zeros(1) == [0];
      assert Inc(t, 2).components == t.components + [0, 1];
      ZeroCountConcat(t.components, [0, 1]);
    }
  }
}
