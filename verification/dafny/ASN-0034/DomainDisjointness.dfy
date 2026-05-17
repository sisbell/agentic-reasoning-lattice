// ASN-0034: T10a.6 — DomainDisjointness (LEMMA, corollary)
// Distinct allocators have disjoint output domains.
//   Case split on the lineage relation between X and Y:
//   (i)  Ancestor–descendant — OnLineage(X, Y) (or its symmetric) with
//        X != Y forces strictly different depths (T10a OnLineageEqualDepth-
//        IsEqual). T10a.3 LocalMonotonicity then makes the descendant's
//        output strictly longer than the ancestor's, so the two sibling
//        sequences cannot share any value.
//   (ii) Non-lineage — T10a.5 CrossAllocatorIncomparability gives mutual
//        prefix-incomparability. Instantiating at x = y = t contradicts
//        reflexivity of ≼ from PrefixRelation.
include "./AllocatorDiscipline.dfy"
include "./UniformSiblingLength.dfy"
include "./LengthSeparation.dfy"
include "./CrossAllocatorIncomparability.dfy"
include "./PrefixRelation.dfy"

module DomainDisjointness {
  import opened AllocatorDiscipline
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened LengthSeparation
  import opened PrefixRelation
  import USL = UniformSiblingLength
  import CAI = CrossAllocatorIncomparability

  // Per-element form: t cannot lie in dom(X) and dom(Y) simultaneously.
  lemma DomainDisjointnessPair(X: Allocator, Y: Allocator, t: Tumbler)
    requires AllocatorDiscipline.AllocatorDiscipline(X)
    requires AllocatorDiscipline.AllocatorDiscipline(Y)
    requires X != Y
    requires InDomain(t, X)
    requires InDomain(t, Y)
    ensures false
  {
    var nx :| SiblingAt(X, nx) == t;
    var ny :| SiblingAt(Y, ny) == t;

    if OnLineage(X, Y) {
      OnLineageDepth(X, Y);
      if Depth(X) == Depth(Y) {
        CAI.OnLineageEqualDepthIsEqual(X, Y);
        assert false;
      }
      LocalMonotonicity(X, Y, nx, ny);
    } else if OnLineage(Y, X) {
      OnLineageDepth(Y, X);
      if Depth(Y) == Depth(X) {
        CAI.OnLineageEqualDepthIsEqual(Y, X);
        assert false;
      }
      LocalMonotonicity(Y, X, ny, nx);
    } else {
      USL.SiblingInT(X, nx);
      CAI.CrossAllocatorIncomparability(X, Y, t, t);
    }
  }

  // T10a.6: dom(X) ∩ dom(Y) = ∅ whenever X and Y are distinct allocators.
  lemma DomainDisjointness(X: Allocator, Y: Allocator)
    requires AllocatorDiscipline.AllocatorDiscipline(X)
    requires AllocatorDiscipline.AllocatorDiscipline(Y)
    requires X != Y
    ensures forall t: Tumbler :: !(InDomain(t, X) && InDomain(t, Y))
  {
    forall t: Tumbler
      ensures !(InDomain(t, X) && InDomain(t, Y))
    {
      if InDomain(t, X) && InDomain(t, Y) {
        DomainDisjointnessPair(X, Y, t);
      }
    }
  }
}
