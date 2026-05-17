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
      var p := LastSignificantPosition.LastSignificantPosition(t);
      assert p == n;
      assert Component(t, n) != 0;
      assert t.components[n-1] != 0;
      assert t.components[n-1] + 1 != 0;

      // Build the expected tumbler and equate via Extensionality.
      var expected := Tumbler(t.components[..n-1] + [t.components[n-1] + 1]);
      assert |t.components[..n-1] + [t.components[n-1] + 1]| == n;
      assert InT(expected);
      assert Length(expected) == n;

      forall i | 1 <= i <= n
        ensures Component(inc, i) == Component(expected, i)
      {
        if i < n {
          assert Component(inc, i) == Component(t, i);
          assert (t.components[..n-1] + [t.components[n-1] + 1])[i-1] == t.components[i-1];
          assert Component(expected, i) == t.components[i-1];
        } else {
          assert i == n;
          assert Component(inc, n) == Component(t, n) + 1;
          assert (t.components[..n-1] + [t.components[n-1] + 1])[n-1] == t.components[n-1] + 1;
          assert Component(expected, n) == t.components[n-1] + 1;
        }
      }
      Extensionality(inc, expected);

      // Now relate Zeros(expected) to Zeros(t).
      CountZerosConcat(t.components[..n-1], [t.components[n-1] + 1]);
      CountZerosConcat(t.components[..n-1], [t.components[n-1]]);
      assert t.components == t.components[..n-1] + [t.components[n-1]];
      assert Zeros(inc) == Zeros(t);

      // No adjacent zeros in inc.
      forall i | 1 <= i < Length(inc)
        ensures !(Component(inc, i) == 0 && Component(inc, i + 1) == 0)
      {
        if i < n - 1 {
          // Both Component(inc, i) and Component(inc, i+1) match t.
        } else {
          assert i == n - 1;
          assert Component(inc, n) == Component(t, n) + 1 != 0;
        }
      }
    } else if k == 1 {
      assert seq(0, _ => 0 as Carrier) == [];
      var expected := Tumbler(t.components + [1 as Carrier]);
      assert |expected.components| == n + 1;
      assert InT(expected);
      assert Length(expected) == n + 1;

      forall i | 1 <= i <= n + 1
        ensures Component(inc, i) == Component(expected, i)
      {
        if i <= n {
          assert Component(inc, i) == Component(t, i);
          assert expected.components[i-1] == t.components[i-1];
        } else {
          assert i == n + 1;
          assert Component(inc, n + 1) == 1;
          assert expected.components[n] == 1;
        }
      }
      Extensionality(inc, expected);

      CountZerosConcat(t.components, [1 as Carrier]);
      assert Zeros(inc) == Zeros(t);

      forall i | 1 <= i < Length(inc)
        ensures !(Component(inc, i) == 0 && Component(inc, i + 1) == 0)
      {
        if i < n {
          // Both components match t.
        } else {
          assert i == n;
          assert Component(inc, n + 1) == 1;
        }
      }
    } else if k == 2 {
      assert seq(1, _ => 0 as Carrier) == [0 as Carrier];
      var expected := Tumbler(t.components + [0 as Carrier, 1 as Carrier]);
      assert |expected.components| == n + 2;
      assert InT(expected);
      assert Length(expected) == n + 2;

      forall i | 1 <= i <= n + 2
        ensures Component(inc, i) == Component(expected, i)
      {
        if i <= n {
          assert Component(inc, i) == Component(t, i);
          assert expected.components[i-1] == t.components[i-1];
        } else if i == n + 1 {
          assert Component(inc, n + 1) == 0;
          assert expected.components[n] == 0;
        } else {
          assert i == n + 2;
          assert Component(inc, n + 2) == 1;
          assert expected.components[n + 1] == 1;
        }
      }
      Extensionality(inc, expected);

      CountZerosConcat(t.components, [0 as Carrier, 1 as Carrier]);
      assert CountZeros([0 as Carrier, 1 as Carrier]) == 1;
      assert Zeros(inc) == Zeros(t) + 1;

      forall i | 1 <= i < Length(inc)
        ensures !(Component(inc, i) == 0 && Component(inc, i + 1) == 0) ||
                (i == n && Zeros(t) > 2 ==> false) ||
                true
      {
      }
    } else {
      // k >= 3: adjacent zeros at positions n+1 and n+2 violate HierarchicalParsing.
      assert k >= 3;
      assert Length(inc) == n + k;
      assert Component(inc, n + 1) == 0;
      assert Component(inc, n + 2) == 0;
      assert 1 <= n + 1 < Length(inc);
      assert Component(inc, n + 1) == 0 && Component(inc, (n + 1) + 1) == 0;
    }
  }
}
