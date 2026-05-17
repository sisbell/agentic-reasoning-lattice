// ASN-0034: T10a.8 — UniformSiblingZeroCount (LEMMA, corollary)
// All siblings produced by a single allocator have the same zero count as
// its base address. Sibling production uses only inc(·, 0); on a T4-valid
// address inc(·, 0) modifies only position sig(t) = #t whose value is
// nonzero and remains nonzero after +1, so the zero-index set is preserved.
include "./AllocatorDiscipline.dfy"
include "./HierarchicalIncrement.dfy"
include "./HierarchicalParsing.dfy"
include "./T4PreservationUnderDiscipline.dfy"
include "./CarrierSetDefinition.dfy"
include "./SigOnValidAddresses.dfy"
include "./LastSignificantPosition.dfy"

module UniformSiblingZeroCount {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened HierarchicalParsing
  import opened HierarchicalIncrement
  import opened AllocatorDiscipline
  import opened SigOnValidAddresses
  import opened LastSignificantPosition
  import T4PreservationUnderDiscipline

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

  // Helper: inc(t, 0) preserves the zero count on T4-valid t.
  lemma IncZeroPreservesZeros(t: Tumbler)
    requires InT(t)
    requires HierarchicalParsing.HierarchicalParsing(t)
    ensures Zeros(HierarchicalIncrement.HierarchicalIncrement(t, 0)) == Zeros(t)
  {
    SigOnValidAddresses.SigOnValidAddresses(t);
    var n := Length(t);
    var inc := HierarchicalIncrement.HierarchicalIncrement(t, 0);
    var p := LastSignificantPosition.LastSignificantPosition(t);
    assert p == n;
    assert Component(t, n) != 0;
    assert t.components[n-1] != 0;
    assert t.components[n-1] + 1 != 0;

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

    CountZerosConcat(t.components[..n-1], [t.components[n-1] + 1]);
    CountZerosConcat(t.components[..n-1], [t.components[n-1]]);
    assert t.components == t.components[..n-1] + [t.components[n-1]];
  }

  lemma UniformSiblingZeroCount(a: Allocator, n: nat)
    requires AllocatorDiscipline.AllocatorDiscipline(a)
    ensures Zeros(SiblingAt(a, n)) == Zeros(BaseAddress(a))
    decreases n
  {
    if n == 0 {
    } else {
      UniformSiblingZeroCount(a, n - 1);
      T4PreservationUnderDiscipline.SiblingT4(a, n - 1);
      var prev := SiblingAt(a, n - 1);
      IncZeroPreservesZeros(prev);
    }
  }
}
