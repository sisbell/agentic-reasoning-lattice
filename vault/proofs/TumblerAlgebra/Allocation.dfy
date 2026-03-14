// Allocation properties (ASN-0034): T8, T10a, T10b, T10c, T10d, T11
module Allocation {
  import opened TumblerAlgebra
  import Hierarchy

  // ---------------------------------------------------------------------------
  // T8 — AddressPermanence
  // ---------------------------------------------------------------------------

  ghost predicate AddressPermanence(before: set<Tumbler>, after: set<Tumbler>) {
    before <= after
  }

  lemma AddressPermanenceTransitive(s1: set<Tumbler>, s2: set<Tumbler>, s3: set<Tumbler>)
    requires AddressPermanence(s1, s2)
    requires AddressPermanence(s2, s3)
    ensures AddressPermanence(s1, s3)
  { }

  // ---------------------------------------------------------------------------
  // T10a — AllocatorDiscipline
  // ---------------------------------------------------------------------------

  ghost predicate AllocatorDiscipline(t: Address, k: nat)
    requires PositiveTumbler(t)
    requires |t.components| > 0
  {
    var r := AllocationInc(t, k);
    PositiveTumbler(r) && |r.components| > 0 &&
    (k == 0 ==> |r.components| == |t.components| && LastNonzero(r) == LastNonzero(t)) &&
    (k > 0 ==> |r.components| == |t.components| + k && LastNonzero(r) > LastNonzero(t))
  }

  lemma AllocatorDisciplineHolds(t: Address, k: nat)
    requires PositiveTumbler(t)
    requires |t.components| > 0
    ensures AllocatorDiscipline(t, k)
  {
    var r := AllocationInc(t, k);
    var s := LastNonzero(t);
    if k == 0 {
      assert r.components[s] == t.components[s] + 1;
      LastNonzeroAt(r, s);
    } else {
      var last := |r.components| - 1;
      assert r.components[last] == 1;
    }
  }

  // ---------------------------------------------------------------------------
  // T10b — PartitionIndependence
  // ---------------------------------------------------------------------------

  ghost predicate NonNesting(p1: Tumbler, p2: Tumbler) {
    !IsPrefix(p1, p2) && !IsPrefix(p2, p1)
  }

  lemma PartitionIndependence(p1: Tumbler, p2: Tumbler, a: Tumbler, b: Tumbler)
    requires NonNesting(p1, p2)
    requires IsPrefix(p1, a)
    requires IsPrefix(p2, b)
    ensures a != b
  { }

  // ---------------------------------------------------------------------------
  // T10c — PartitionMonotonicity
  // ---------------------------------------------------------------------------

  ghost predicate AllExtend(stream: seq<Tumbler>, p: Tumbler) {
    forall i :: 0 <= i < |stream| ==> IsPrefix(p, stream[i])
  }

  ghost predicate StrictlyIncreasing(stream: seq<Tumbler>) {
    forall i, j :: 0 <= i < j < |stream| ==> LessThan(stream[i], stream[j])
  }

  lemma IntraPartitionTotalOrder(stream: seq<Tumbler>, i: nat, j: nat)
    requires StrictlyIncreasing(stream)
    requires 0 <= i < |stream| && 0 <= j < |stream| && i != j
    ensures LessThan(stream[i], stream[j]) || LessThan(stream[j], stream[i])
  { }

  lemma AllocationOrderConsistency(stream: seq<Tumbler>, i: nat, j: nat)
    requires StrictlyIncreasing(stream)
    requires 0 <= i < j < |stream|
    ensures LessThan(stream[i], stream[j])
  { }

  lemma CrossPartitionMonotonicity(
    p1: Tumbler, p2: Tumbler,
    stream1: seq<Tumbler>, stream2: seq<Tumbler>
  )
    requires LessThan(p1, p2)
    requires NonNesting(p1, p2)
    requires AllExtend(stream1, p1) && AllExtend(stream2, p2)
    ensures forall i, j :: 0 <= i < |stream1| && 0 <= j < |stream2|
              ==> LessThan(stream1[i], stream2[j])
  {
    forall i, j | 0 <= i < |stream1| && 0 <= j < |stream2|
      ensures LessThan(stream1[i], stream2[j])
    {
      Hierarchy.PrefixOrderingExtension(p1, p2, stream1[i], stream2[j]);
    }
  }

  // ---------------------------------------------------------------------------
  // T10d — IncrementPreservesValidity (TA5 preserves T4)
  // ---------------------------------------------------------------------------

  lemma ZeroCountConcat(a: seq<nat>, b: seq<nat>)
    ensures Hierarchy.ZeroCount(a + b) == Hierarchy.ZeroCount(a) + Hierarchy.ZeroCount(b)
    decreases |a|
  {
    if |a| == 0 {
      assert a + b == b;
    } else {
      assert (a + b)[1..] == a[1..] + b;
      ZeroCountConcat(a[1..], b);
    }
  }

  lemma ZeroCountNonzeroLast(s: seq<nat>)
    requires |s| >= 1
    requires s[|s| - 1] != 0
    ensures Hierarchy.ZeroCount(s) == Hierarchy.ZeroCount(s[..|s| - 1])
  {
    assert s == s[..|s| - 1] + [s[|s| - 1]];
    ZeroCountConcat(s[..|s| - 1], [s[|s| - 1]]);
  }

  lemma IncrementPreservesValidity(t: Address, k: nat)
    requires Hierarchy.ValidAddress(t)
    requires k <= 2
    requires k >= 1 ==> Hierarchy.ZeroCount(t.components) + k <= 4
    ensures Hierarchy.ValidAddress(AllocationInc(t, k))
  {
    if k == 0 {
      var s := LastNonzero(t);
      var tc := t.components;
      var rc := AllocationInc(t, 0).components;
      ZeroCountNonzeroLast(tc);
      assert rc == tc[..s] + [tc[s] + 1] + tc[s+1..];
      ZeroCountConcat(tc[..s], [tc[s] + 1]);
      ZeroCountConcat(tc[..s] + [tc[s] + 1], tc[s+1..]);
    } else if k == 1 {
      assert Zeros(0) == [];
      assert AllocationInc(t, 1).components == t.components + [1];
      ZeroCountConcat(t.components, [1]);
    } else {
      assert Zeros(1) == [0];
      assert AllocationInc(t, 2).components == t.components + [0, 1];
      ZeroCountConcat(t.components, [0, 1]);
    }
  }

  // ---------------------------------------------------------------------------
  // T11 — GlobalUniqueness
  // ---------------------------------------------------------------------------

  // DIVERGENCE: The ASN states GlobalUniqueness as a system-level property
  // over all allocation events at all times. The Dafny model captures the
  // structural core: given that the allocation system provides one of three
  // discriminants (ordering, non-nesting prefixes, or length difference),
  // a ≠ b follows. The exhaustiveness argument depends on T9, T10, and T10a
  // as system invariants, which cannot be expressed as a Dafny precondition
  // without modeling the full allocation state machine.

  lemma GlobalUniqueness(
    a: Tumbler, b: Tumbler,
    pa: Tumbler, pb: Tumbler
  )
    requires IsPrefix(pa, a) && IsPrefix(pb, b)
    requires
      (LessThan(a, b) || LessThan(b, a))
      ||
      (!IsPrefix(pa, pb) && !IsPrefix(pb, pa))
      ||
      |a.components| != |b.components|
    ensures a != b
  { }
}
