// ASN-0034: T10a.4 — T4PreservationUnderDiscipline (LEMMA, corollary)
// Allocators conforming to T10a produce only T4-compliant addresses.
include "./AllocatorDiscipline.dfy"
include "./IncrementPreservesT4.dfy"
include "./HierarchicalParsing.dfy"

module T4PreservationUnderDiscipline {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened HierarchicalParsing
  import opened HierarchicalIncrement
  import opened AllocatorDiscipline
  import IncrementPreservesT4

  // Strengthened hypothesis: every sibling in dom(a) is T4-valid.
  // Induction on (a, n) lexicographically.
  lemma SiblingT4(a: Allocator, n: nat)
    requires AllocatorDiscipline(a)
    ensures InT(SiblingAt(a, n))
    ensures HierarchicalParsing.HierarchicalParsing(SiblingAt(a, n))
    decreases a, n
  {
    if n == 0 {
      match a {
        case RootAllocator(b) =>
        case ChildAllocator(p, sp, k) =>
          var nW :| SiblingAt(p, nW) == sp;
          SiblingT4(p, nW);
          IncrementPreservesT4.IncrementPreservesT4(sp, k);
      }
    } else {
      SiblingT4(a, n - 1);
      var prev := SiblingAt(a, n - 1);
      IncrementPreservesT4.IncrementPreservesT4(prev, 0);
    }
  }

  // T10a.4: every t ∈ dom(a) is T4-valid.
  lemma T4PreservationUnderDiscipline(a: Allocator, t: Tumbler)
    requires AllocatorDiscipline(a)
    requires InDomain(t, a)
    ensures InT(t)
    ensures HierarchicalParsing.HierarchicalParsing(t)
  {
    var n :| SiblingAt(a, n) == t;
    SiblingT4(a, n);
  }
}
