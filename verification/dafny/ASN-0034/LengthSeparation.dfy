// ASN-0034: T10a.3 — LengthSeparation (LEMMA, corollary)
// Child allocator outputs are strictly longer than any parent sibling output,
// with additive separation across nesting levels.
//   Single-step: BaseAddress(child) = inc(spawnPt, k) with k ∈ {1,2}; TA5(d)
//   gives length = #spawnPt + k. T10a.1 makes spawnPt's length match the
//   parent's uniform sibling length γ, and again on the child gives all child
//   outputs length γ + k > γ.
//   Lineage-depth: depth-d output has length γ + k'₁+…+k'_d ≥ γ + d.
//   Local monotonicity: ancestor A at depth d_A and descendant B at depth
//   d_B > d_A on the same lineage satisfy
//     #output(B) − #output(A) = k'_{d_A+1}+…+k'_{d_B} ≥ d_B − d_A ≥ 1.
// T3 lifts distinct lengths to distinct tumblers.
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

  // Root of the allocator's lineage chain.
  function Root(a: Allocator): Allocator
    decreases a
  {
    if a.RootAllocator? then a else Root(a.parent)
  }

  // Cumulative spawn parameters along the lineage from root to a.
  function SumSpawnParams(a: Allocator): nat
    decreases a
  {
    if a.RootAllocator? then 0
    else SumSpawnParams(a.parent) + a.spawnParam
  }

  // Lineage relation: a appears on b's chain (a is an ancestor of b, or a = b).
  predicate OnLineage(a: Allocator, b: Allocator)
    decreases b
  {
    a == b || (b.ChildAllocator? && OnLineage(a, b.parent))
  }

  // Distinct lengths force distinct tumblers (T3 corollary).
  lemma DistinctLengthsDistinctTumblers(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires Length(a) != Length(b)
    ensures a != b
  {
    CR.CanonicalRepresentation(a, b);
  }

  // On a lineage, both allocators share the same root.
  lemma OnLineageRoot(a: Allocator, b: Allocator)
    requires OnLineage(a, b)
    ensures Root(a) == Root(b)
    decreases b
  {
    if a != b {
      OnLineageRoot(a, b.parent);
    }
  }

  // On a lineage, the ancestor's depth is ≤ the descendant's.
  lemma OnLineageDepth(a: Allocator, b: Allocator)
    requires OnLineage(a, b)
    ensures Depth(a) <= Depth(b)
    decreases b
  {
    if a != b {
      OnLineageDepth(a, b.parent);
    }
  }

  // On a lineage, the ancestor's cumulative spawn-param sum is ≤ the descendant's.
  lemma OnLineageSumSpawnParams(a: Allocator, b: Allocator)
    requires OnLineage(a, b)
    ensures SumSpawnParams(a) <= SumSpawnParams(b)
    decreases b
  {
    if a != b {
      OnLineageSumSpawnParams(a, b.parent);
    }
  }

  // Discipline propagates up the lineage.
  lemma OnLineageDiscipline(a: Allocator, b: Allocator)
    requires AllocatorDiscipline.AllocatorDiscipline(b)
    requires OnLineage(a, b)
    ensures AllocatorDiscipline.AllocatorDiscipline(a)
    decreases b
  {
    if a != b {
      OnLineageDiscipline(a, b.parent);
    }
  }

  // BaseAddress length is the root base length plus the cumulative spawn params.
  // Identifies γ + k'₁+…+k'_d for a depth-d descendant on a lineage.
  lemma BaseAddressLineageLength(a: Allocator)
    requires AllocatorDiscipline.AllocatorDiscipline(a)
    ensures Length(BaseAddress(a)) ==
            Length(BaseAddress(Root(a))) + SumSpawnParams(a)
    decreases a
  {
    if a.ChildAllocator? {
      BaseAddressLineageLength(a.parent);
      ghost var m: nat :| SiblingAt(a.parent, m) == a.spawnPt;
      USL.UniformSiblingLength(a.parent, m);
    }
  }

  // Cumulative spawn parameters dominate depth: SumSpawnParams ≥ Depth.
  // Each k'_i ∈ {1, 2} contributes at least 1 (NAT-zero + NAT-discrete).
  lemma SumSpawnParamsBound(a: Allocator)
    requires AllocatorDiscipline.AllocatorDiscipline(a)
    ensures SumSpawnParams(a) >= Depth(a)
    decreases a
  {
    if a.ChildAllocator? {
      SumSpawnParamsBound(a.parent);
    }
  }

  // Lineage spawn-param difference dominates depth difference.
  // For ancestor a and descendant b on the same lineage, the sum of the
  // intervening k'_i values is at least the number of intervening steps.
  lemma SumSpawnParamsLineageBound(a: Allocator, b: Allocator)
    requires AllocatorDiscipline.AllocatorDiscipline(b)
    requires OnLineage(a, b)
    ensures SumSpawnParams(b) - SumSpawnParams(a) >= Depth(b) - Depth(a)
    decreases b
  {
    if a != b {
      SumSpawnParamsLineageBound(a, b.parent);
      OnLineageDepth(a, b.parent);
      OnLineageSumSpawnParams(a, b.parent);
    }
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

  // T10a.3 lineage-depth length: every output at depth d on a lineage with
  // parameters k'₁,…,k'_d has length γ + k'₁+…+k'_d ≥ γ + d. Cumulative
  // length is strictly increasing with depth (Depth(a) ≤ SumSpawnParams(a)
  // and each k'_i ≥ 1).
  lemma LineageDepthLength(a: Allocator, n: nat)
    requires AllocatorDiscipline.AllocatorDiscipline(a)
    ensures Length(SiblingAt(a, n)) ==
            Length(BaseAddress(Root(a))) + SumSpawnParams(a)
    ensures SumSpawnParams(a) >= Depth(a)
    ensures Length(SiblingAt(a, n)) >=
            Length(BaseAddress(Root(a))) + Depth(a)
  {
    USL.UniformSiblingLength(a, n);
    BaseAddressLineageLength(a);
    SumSpawnParamsBound(a);
  }

  // T10a.3 local monotonicity: for ancestor A at depth d_A and descendant B
  // at depth d_B > d_A on the same lineage,
  //   #output(B) − #output(A) = k'_{d_A+1}+…+k'_{d_B} ≥ d_B − d_A ≥ 1.
  // Outputs at different depths along a lineage never collide (cross-depth
  // distinctness via T3).
  lemma LocalMonotonicity(A: Allocator, B: Allocator, nA: nat, nB: nat)
    requires AllocatorDiscipline.AllocatorDiscipline(B)
    requires OnLineage(A, B)
    requires Depth(B) > Depth(A)
    ensures AllocatorDiscipline.AllocatorDiscipline(A)
    ensures Root(A) == Root(B)
    ensures Length(SiblingAt(B, nB)) - Length(SiblingAt(A, nA)) ==
            SumSpawnParams(B) - SumSpawnParams(A)
    ensures SumSpawnParams(B) - SumSpawnParams(A) >= Depth(B) - Depth(A) >= 1
    ensures Length(SiblingAt(B, nB)) > Length(SiblingAt(A, nA))
    ensures SiblingAt(A, nA) != SiblingAt(B, nB)
  {
    OnLineageDiscipline(A, B);
    OnLineageRoot(A, B);
    LineageDepthLength(A, nA);
    LineageDepthLength(B, nB);
    OnLineageSumSpawnParams(A, B);
    OnLineageDepth(A, B);
    SumSpawnParamsLineageBound(A, B);
    USL.SiblingInT(A, nA);
    USL.SiblingInT(B, nB);
    DistinctLengthsDistinctTumblers(SiblingAt(B, nB), SiblingAt(A, nA));
  }
}
