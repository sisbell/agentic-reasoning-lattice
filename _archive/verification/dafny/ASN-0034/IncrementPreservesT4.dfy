include "./HierarchicalParsing.dfy"

module IncrementPreservesT4 {
  // TA5a — IncrementPreservesT4 (LEMMA)
  // inc(t, k) preserves T4 (ValidAddress) iff k = 0, or k = 1 ∧ zeros(t) ≤ 3,
  // or k = 2 ∧ zeros(t) ≤ 2. For k ≥ 3, T4 is violated (adjacent zeros).

  import HP = HierarchicalParsing
  import SE = SyntacticEquivalence
  import LD = LevelDetermination

  // inc(t, k): sibling (k=0) increments last component;
  // child (k>0) appends k-1 zeros and trailing 1
  function Inc(t: SE.Tumbler, k: nat): SE.Tumbler
    requires HP.ValidAddress(t)
    ensures SE.ValidTumbler(Inc(t, k))
  {
    if k == 0 then
      var n := |t.components|;
      SE.Tumbler(t.components[..n-1] + [t.components[n-1] + 1])
    else
      SE.Tumbler(t.components + seq(k - 1, _ => 0) + [1])
  }

  lemma ZeroCountConcat(s1: seq<nat>, s2: seq<nat>)
    ensures LD.ZeroCount(s1 + s2) == LD.ZeroCount(s1) + LD.ZeroCount(s2)
    decreases |s1|
  {
    if |s1| == 0 {
      assert s1 + s2 == s2;
    } else {
      assert (s1 + s2)[1..] == s1[1..] + s2;
      ZeroCountConcat(s1[1..], s2);
    }
  }

  // TA5a: increment preserves ValidAddress (biconditional)
  lemma IncrementPreservesT4(t: SE.Tumbler, k: nat)
    requires HP.ValidAddress(t)
    ensures HP.ValidAddress(Inc(t, k)) <==>
      (k == 0 || (k == 1 && LD.ZeroCount(t.components) <= 3) || (k == 2 && LD.ZeroCount(t.components) <= 2))
  {
    var s := t.components;
    var n := |s|;
    if k == 0 {
      ZeroCountConcat(s[..n-1], [s[n-1] + 1]);
      ZeroCountConcat(s[..n-1], [s[n-1]]);
      assert s == s[..n-1] + [s[n-1]];
    } else if k <= 2 {
      var mid := seq(k - 1, _ => 0);
      ZeroCountConcat(s, mid);
      ZeroCountConcat(s + mid, [1]);
    } else {
      // k >= 3: adjacent zeros at positions n and n+1 violate SyntacticWF
      var s' := Inc(t, k).components;
      assert s' == s + seq(k - 1, _ => 0) + [1];
      assert s'[n] == 0;
      assert s'[n + 1] == 0;
    }
  }
}
