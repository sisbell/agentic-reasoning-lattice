// ASN-0034: T10a.7 — EnumerationInjectivity (LEMMA, corollary)
// Within a single allocator, the indexing map n ↦ tₙ is injective:
// m ≠ n ⇒ tₘ ≠ tₙ. TA5(a) gives per-step strict increase; T1 (c)
// transitivity lifts it to arbitrary gaps; T1 (a) irreflexivity
// converts strict inequality into distinctness.
include "./AllocatorDiscipline.dfy"
include "./HierarchicalIncrement.dfy"
include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"
include "./NatStrictTotalOrder.dfy"
include "./UniformSiblingLength.dfy"
include "./SpanWellDefinedness.dfy"

module EnumerationInjectivity {
  import opened AllocatorDiscipline
  import opened HierarchicalIncrement
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened NatStrictTotalOrder
  import opened NatCarrierSet
  import opened UniformSiblingLength
  import SpanWellDefinedness

  // T1 irreflexivity: LO(a, b) implies a != b. Equality would force the
  // T1 witness k to satisfy Less(a_k, a_k), contradicting NAT irreflexivity.
  lemma LexImpliesNotEqual(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    ensures a != b
  { }

  // Strict monotonicity over the enumeration: m < n ⇒ tₘ < tₙ.
  // Induction on the gap via TA5(a) (per-step) + T1 (c) transitivity.
  lemma StrictMonotonicity(a: Allocator, m: nat, n: nat)
    requires AllocatorDiscipline.AllocatorDiscipline(a)
    requires m < n
    ensures LexicographicOrder.LexicographicOrder(
              SiblingAt(a, m), SiblingAt(a, n))
    decreases n - m
  { }

  // T10a.7: distinct indices produce distinct addresses.
  lemma EnumerationInjectivity(a: Allocator, m: nat, n: nat)
    requires AllocatorDiscipline.AllocatorDiscipline(a)
    requires m != n
    ensures SiblingAt(a, m) != SiblingAt(a, n)
  { }
}
