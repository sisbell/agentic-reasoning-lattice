// ASN-0034: T10a.3 — LengthSeparation (LEMMA, corollary)
// Child allocator outputs are strictly longer than any parent sibling output.
// One-step: BaseAddress(child) = inc(spawnPt, k) with k ∈ {1,2}; TA5(d) gives
// length = #spawnPt + k. T10a.1 makes spawnPt's length match the parent's
// uniform sibling length γ, and again on the child gives all child outputs
// length γ + k > γ. T3 lifts distinct lengths to distinct tumblers.
include "./AllocatorDiscipline.dfy"
include "./UniformSiblingLength.dfy"
include "./HierarchicalIncrement.dfy"
include "./CarrierSetDefinition.dfy"
include "./CanonicalRepresentation.dfy"

module LengthSeparation {
  import opened AllocatorDiscipline
  import USL = UniformSiblingLength
  import opened HierarchicalIncrement
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import CR = CanonicalRepresentation

  // Distinct lengths force distinct tumblers (T3 corollary).
  lemma DistinctLengthsDistinctTumblers(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires Length(a) != Length(b)
    ensures a != b
  {
    CR.CanonicalRepresentation(a, b);
  }

  // T10a.3 single-step length separation: every output of a child allocator
  // is strictly longer than every output of its parent, and (by T3) no
  // child output equals any parent sibling.
  lemma LengthSeparation(c: Allocator, np: nat, nc: nat)
    requires c.ChildAllocator?
    requires AllocatorDiscipline.AllocatorDiscipline(c)
    ensures Length(SiblingAt(c, nc)) > Length(SiblingAt(c.parent, np))
    ensures SiblingAt(c, nc) != SiblingAt(c.parent, np)
  {
    var p := c.parent;
    var sp := c.spawnPt;
    var k := c.spawnParam;

    // Witness for sp ∈ dom(p) — unfolds InDomain's existential.
    ghost var m: nat :| SiblingAt(p, m) == sp;
    USL.UniformSiblingLength(p, m);

    // T10a.1 on both allocators places all siblings at the base length.
    USL.UniformSiblingLength(c, nc);
    USL.UniformSiblingLength(p, np);

    // T3 lifts the strict length inequality to distinctness.
    USL.SiblingInT(c, nc);
    USL.SiblingInT(p, np);
    DistinctLengthsDistinctTumblers(SiblingAt(c, nc), SiblingAt(p, np));
  }
}
