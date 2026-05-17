// ASN-0034: TA5a — IncrementPreservesT4 (LEMMA)
// inc(t, k) preserves T4 iff k = 0, or k = 1 ∧ zeros(t) ≤ 3,
// or k = 2 ∧ zeros(t) ≤ 2. For k ≥ 3, T4 is violated (adjacent zeros).
include "./HierarchicalIncrement.dfy"
include "./HierarchicalParsing.dfy"
include "./SigOnValidAddresses.dfy"
include "./LastSignificantPosition.dfy"
include "./CarrierSetDefinition.dfy"

module IncrementPreservesT4 {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened LastSignificantPosition
  import opened HierarchicalIncrement
  import opened HierarchicalParsing
  import opened SigOnValidAddresses

  // Helper: zero-count distributes over concatenation.
  lemma CountZerosConcat(s1: seq<Carrier>, s2: seq<Carrier>)
    ensures CountZeros(s1 + s2) == CountZeros(s1) + CountZeros(s2)
    decreases |s1|
  {
    if |s1| == 0 {
      assert s1 + s2 == s2;
    } else {
      assert (s1 + s2)[0] == s1[0];
      assert (s1 + s2)[1..] == s1[1..] + s2;
      CountZerosConcat(s1[1..], s2);
    }
  }

  // Helper: zero count of a run of zeros equals its length.
  lemma CountZerosOfZeroRun(n: nat)
    ensures CountZeros(seq(n, _ => 0 as Carrier)) == n
    decreases n
  {
    if n == 0 {
    } else {
      var s := seq(n, _ => 0 as Carrier);
      assert s[0] == 0;
      assert s[1..] == seq(n - 1, _ => 0 as Carrier);
      CountZerosOfZeroRun(n - 1);
    }
  }

  lemma IncrementPreservesT4(t: Tumbler, k: nat)
    requires InT(t)
    requires HierarchicalParsing.HierarchicalParsing(t)
    ensures HierarchicalParsing.HierarchicalParsing(
              HierarchicalIncrement.HierarchicalIncrement(t, k)) <==>
            (k == 0 || (k == 1 && Zeros(t) <= 3) || (k == 2 && Zeros(t) <= 2))
  {
    SigOnValidAddresses.SigOnValidAddresses(t);
    var n := Length(t);
    var inc := HierarchicalIncrement.HierarchicalIncrement(t, k);

    if k == 0 {
      // sig(t) = n, so inc.components = t.components[..n-1] + [t.components[n-1] + 1].
      // The replaced component was nonzero (T4), stays nonzero. Zeros unchanged.
      var p := LastSignificantPosition.LastSignificantPosition(t);
      assert p == n;
      // Zero count is preserved at position p.
      assert Component(t, n) != 0;
      assert t.components[n-1] != 0;
      assert t.components[n-1] + 1 != 0;
      CountZerosConcat(t.components[..n-1], [t.components[n-1] + 1]);
      CountZerosConcat(t.components[..n-1], [t.components[n-1]]);
      assert t.components == t.components[..n-1] + [t.components[n-1]];
      assert Zeros(inc) == Zeros(t);
    } else if k == 1 {
      // inc.components = t.components + [] + [1] = t.components + [1]. Length = n+1.
      // Zeros(inc) = Zeros(t). T4 iff Zeros(t) <= 3.
      assert seq(0, _ => 0 as Carrier) == [];
      assert inc.components == t.components + [] + [1 as Carrier];
      assert inc.components == t.components + [1 as Carrier];
      CountZerosConcat(t.components, [1 as Carrier]);
      assert Zeros(inc) == Zeros(t);
    } else if k == 2 {
      // inc.components = t.components + [0] + [1]. Length = n+2.
      // Zeros(inc) = Zeros(t) + 1. T4 iff Zeros(t) <= 2.
      assert seq(1, _ => 0 as Carrier) == [0 as Carrier];
      assert inc.components == t.components + [0 as Carrier] + [1 as Carrier];
      CountZerosConcat(t.components, [0 as Carrier]);
      CountZerosConcat(t.components + [0 as Carrier], [1 as Carrier]);
      assert Zeros(inc) == Zeros(t) + 1;
      // Adjacency at (n, n+1): Component(t, n) != 0, so OK.
      assert Component(inc, n) == Component(t, n);
      assert Component(t, n) != 0;
    } else {
      // k >= 3: adjacent zeros at positions n+1 and n+2 in the appended block.
      assert k >= 3;
      assert Length(inc) == n + k;
      // Both positions n+1 and n+2 are within [n+1, n+k-1] (the zero block).
      assert Component(inc, n + 1) == 0;
      assert Component(inc, n + 2) == 0;
      // So adjacent-zero check at index n+1 fails.
      assert 1 <= n + 1 < Length(inc);
      assert Component(inc, n + 1) == 0 && Component(inc, n + 1 + 1) == 0;
      assert !HierarchicalParsing.HierarchicalParsing(inc);
    }
  }
}
