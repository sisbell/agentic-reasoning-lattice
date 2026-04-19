include "./AllocatorDiscipline.dfy"

module LengthSeparation {
  // T10a.3 — LengthSeparation (LEMMA)
  // Corollary of T10a.1, T3, TA5: child-spawning inc extends by exactly k positions.

  import opened AllocatorDiscipline

  // Single-step: child length strictly exceeds parent sibling length,
  // and no parent-length tumbler equals the child output (T3).
  lemma LengthSeparation(t: Tumbler, k: nat)
    requires ValidTumbler(t)
    requires k == 1 || k == 2
    requires k == 1 ==> Zeros(t) <= 3
    requires k == 2 ==> Zeros(t) <= 2
    ensures |IncChild(t, k).components| == |t.components| + k
    ensures |IncChild(t, k).components| > |t.components|
    ensures forall s: Tumbler :: |s.components| == |t.components| ==> s != IncChild(t, k)
  { }

  // Helper: SumNats of valid chain elements >= chain length (each k'_i >= 1)
  lemma SumNatsBound(base: Tumbler, ks: seq<nat>)
    requires ValidChildChain(base, ks)
    ensures SumNats(ks) >= |ks|
    decreases |ks|
  {
    if |ks| > 0 {
      SumNatsBound(IncChild(base, ks[0]), ks[1..]);
    }
  }

  // Multi-level: depth-d descendant has length γ + Σk'_i ≥ γ + d > γ;
  // no base-length tumbler equals the descendant (T3).
  lemma DepthSeparation(base: Tumbler, ks: seq<nat>)
    requires ValidChildChain(base, ks)
    requires |ks| > 0
    ensures |ChildChain(base, ks).components| == |base.components| + SumNats(ks)
    ensures SumNats(ks) >= |ks|
    ensures |ChildChain(base, ks).components| > |base.components|
    ensures forall s: Tumbler :: |s.components| == |base.components| ==> s != ChildChain(base, ks)
  {
    MultiLevelSeparation(base, ks);
    SumNatsBound(base, ks);
  }

  // A valid child chain can be split: prefix is valid, suffix is valid
  // from the chain endpoint. Ordered ensures: first establishes the
  // precondition that ChildChain needs in the second.
  lemma ValidChildChainSplit(base: Tumbler, ks: seq<nat>, n: nat)
    requires ValidChildChain(base, ks)
    requires n <= |ks|
    ensures ValidChildChain(base, ks[..n])
    ensures ValidChildChain(ChildChain(base, ks[..n]), ks[n..])
    decreases n
  {
    if n > 0 {
      ValidChildChainSplit(IncChild(base, ks[0]), ks[1..], n - 1);
      assert ks[..n][0] == ks[0];
      assert (ks[..n])[1..] == ks[1..n];
      assert (ks[1..])[..n-1] == ks[1..n];
      assert (ks[1..])[n-1..] == ks[n..];
    }
  }

  // SumNats distributes over concatenation
  lemma SumNatsSplit(xs: seq<nat>, ys: seq<nat>)
    ensures SumNats(xs + ys) == SumNats(xs) + SumNats(ys)
    decreases |xs|
  {
    if |xs| == 0 {
      assert xs + ys == ys;
    } else {
      assert (xs + ys)[0] == xs[0];
      assert (xs + ys)[1..] == xs[1..] + ys;
      SumNatsSplit(xs[1..], ys);
    }
  }

  // Distinct depths along a lineage produce distinct outputs:
  // cumulative length is strictly increasing, so outputs never collide (T3).
  lemma DepthsNeverCollide(base: Tumbler, ks: seq<nat>, i: nat, j: nat)
    requires ValidChildChain(base, ks)
    requires 0 <= i < j <= |ks|
    ensures ValidChildChain(base, ks[..i])
    ensures ValidChildChain(base, ks[..j])
    ensures |ChildChain(base, ks[..i]).components| < |ChildChain(base, ks[..j]).components|
    ensures ChildChain(base, ks[..i]) != ChildChain(base, ks[..j])
  {
    ValidChildChainSplit(base, ks, i);
    ValidChildChainSplit(base, ks, j);
    MultiLevelSeparation(base, ks[..i]);
    MultiLevelSeparation(base, ks[..j]);
    assert ks[..j] == ks[..i] + ks[i..j];
    SumNatsSplit(ks[..i], ks[i..j]);
    ValidChildChainSplit(ChildChain(base, ks[..i]), ks[i..], j - i);
    assert ks[i..][..j-i] == ks[i..j];
    SumNatsBound(ChildChain(base, ks[..i]), ks[i..j]);
  }
}
