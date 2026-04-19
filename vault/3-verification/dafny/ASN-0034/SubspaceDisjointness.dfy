include "./HierarchicalParsing.dfy"

module SubspaceDisjointness {
  // T7 — SubspaceDisjointness
  // (A a, b ∈ T : a.E₁ ≠ b.E₁ ⟹ a ≠ b)
  // Corollary of T3, T4

  import HP = HierarchicalParsing
  import SE = SyntacticEquivalence
  import LD = LevelDetermination

  // Position of the (n+1)th zero (0-indexed) in s, searching from pos.
  // Returns |s| if fewer than n+1 zeros exist from pos onward.
  ghost function NthZeroPos(s: seq<nat>, n: nat, pos: nat): nat
    requires pos <= |s|
    decreases |s| - pos
  {
    if pos == |s| then |s|
    else if s[pos] == 0 then
      if n == 0 then pos else NthZeroPos(s, n - 1, pos + 1)
    else NthZeroPos(s, n, pos + 1)
  }

  // Count of zeros from position pos onward
  ghost function ZeroCountFrom(s: seq<nat>, pos: nat): nat
    requires pos <= |s|
    decreases |s| - pos
  {
    if pos == |s| then 0
    else (if s[pos] == 0 then 1 else 0) + ZeroCountFrom(s, pos + 1)
  }

  // Relate position-based zero count to LD.ZeroCount (slice-based)
  lemma ZeroCountFromSlice(s: seq<nat>, pos: nat)
    requires pos <= |s|
    ensures ZeroCountFrom(s, pos) == LD.ZeroCount(s[pos..])
    decreases |s| - pos
  {
    if pos == |s| {
      assert s[pos..] == [];
    } else {
      assert s[pos..][0] == s[pos];
      assert s[pos..][1..] == s[pos + 1..];
      ZeroCountFromSlice(s, pos + 1);
    }
  }

  // NthZeroPos returns a valid zero position when enough zeros exist
  lemma NthZeroPosValid(s: seq<nat>, n: nat, pos: nat)
    requires pos <= |s|
    requires ZeroCountFrom(s, pos) >= n + 1
    ensures NthZeroPos(s, n, pos) < |s|
    ensures s[NthZeroPos(s, n, pos)] == 0
    decreases |s| - pos
  {
    if s[pos] == 0 {
      if n > 0 {
        NthZeroPosValid(s, n - 1, pos + 1);
      }
    } else {
      NthZeroPosValid(s, n, pos + 1);
    }
  }

  // E₁: first component of the element field (after the 3rd field separator)
  ghost function ElementSubspaceId(t: SE.Tumbler): nat
    requires SE.ValidTumbler(t) && SE.SyntacticWF(t.components)
    requires LD.ZeroCount(t.components) == 3
    requires NthZeroPos(t.components, 2, 0) + 1 < |t.components|
  {
    t.components[NthZeroPos(t.components, 2, 0) + 1]
  }

  // Helper: in a SyntacticWF sequence with ZeroCount == 3, the 3rd zero
  // is followed by at least one component (since last component is non-zero)
  lemma ThirdZeroInBounds(s: seq<nat>)
    requires |s| >= 1
    requires SE.SyntacticWF(s)
    requires LD.ZeroCount(s) == 3
    ensures NthZeroPos(s, 2, 0) + 1 < |s|
  {
    ZeroCountFromSlice(s, 0);
    NthZeroPosValid(s, 2, 0);
    // s[NthZeroPos(s, 2, 0)] == 0 but s[|s|-1] != 0 (SyntacticWF)
    assert s[|s| - 1] != 0;
  }

  // T7: different subspace identifiers imply distinct tumblers
  lemma SubspaceDisjointness(a: SE.Tumbler, b: SE.Tumbler)
    requires HP.ValidAddress(a) && HP.ValidAddress(b)
    requires LD.ZeroCount(a.components) == 3
    requires LD.ZeroCount(b.components) == 3
    ensures NthZeroPos(a.components, 2, 0) + 1 < |a.components|
    ensures NthZeroPos(b.components, 2, 0) + 1 < |b.components|
    ensures ElementSubspaceId(a) != ElementSubspaceId(b) ==> a != b
  {
    ThirdZeroInBounds(a.components);
    ThirdZeroInBounds(b.components);
  }
}
