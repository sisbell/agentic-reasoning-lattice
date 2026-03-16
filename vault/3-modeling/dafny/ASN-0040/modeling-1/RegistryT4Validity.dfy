include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerAllocation.dfy"

// B10 — RegistryT4Validity
module RegistryT4Validity {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import TumblerAllocation

  // B10 — RegistryT4Validity
  // (A t ∈ Σ.B : t satisfies T4)
  // Derived from B₀ conf. (seeds satisfy T4) and B6 (valid depth).

  ghost predicate AllValid(B: set<Tumbler>) {
    forall t :: t in B ==> TumblerHierarchy.ValidAddress(t)
  }

  // ValidAddress implies AllocationInc preconditions
  lemma ValidImpliesPositive(t: Tumbler)
    requires TumblerHierarchy.ValidAddress(t)
    ensures PositiveTumbler(t)
    ensures |t.components| > 0
  { }

  // Inductive step, first-child case: inc(p, d) valid under B6
  lemma FirstChildValid(p: Tumbler, d: nat)
    requires TumblerHierarchy.ValidAddress(p)
    requires d == 1 || d == 2
    requires TumblerHierarchy.ZeroCount(p.components) + (d - 1) <= 3
    ensures TumblerHierarchy.ValidAddress(AllocationInc(p, d))
  {
    TumblerAllocation.IncrementPreservesValidity(p, d);
  }

  // Inductive step, sibling case: inc(t, 0) valid when t valid
  lemma NextSiblingValid(t: Tumbler)
    requires TumblerHierarchy.ValidAddress(t)
    ensures TumblerHierarchy.ValidAddress(AllocationInc(t, 0))
  {
    TumblerAllocation.IncrementPreservesValidity(t, 0);
  }

  // B10 — AllValid is an inductive invariant of the baptismal registry.
  // Base: B₀ conf. asserts AllValid(B₀).
  // Step: baptize(p, d) adds next(B, p, d) to B.
  //   children empty  → fresh = inc(p, d)      → valid by FirstChildValid
  //   children exist  → fresh = inc(maxChild, 0) → valid by NextSiblingValid
  //
  // DIVERGENCE: The ASN states B10 as a universal over all reachable registry
  // states. The Dafny proof captures single-step preservation: given AllValid(B)
  // and a B6-compliant baptism, B ∪ {fresh} remains AllValid. Full induction
  // over the allocation state machine is outside scope.
  lemma RegistryT4Validity(
    B: set<Tumbler>, p: Tumbler, d: nat,
    maxChild: Tumbler, childrenEmpty: bool
  )
    requires AllValid(B)
    requires TumblerHierarchy.ValidAddress(p)
    requires d == 1 || d == 2
    requires TumblerHierarchy.ZeroCount(p.components) + (d - 1) <= 3
    requires !childrenEmpty ==> maxChild in B
    ensures childrenEmpty ==>
              TumblerHierarchy.ValidAddress(AllocationInc(p, d)) &&
              AllValid(B + {AllocationInc(p, d)})
    ensures !childrenEmpty ==>
              TumblerHierarchy.ValidAddress(AllocationInc(maxChild, 0)) &&
              AllValid(B + {AllocationInc(maxChild, 0)})
  {
    if childrenEmpty {
      FirstChildValid(p, d);
    } else {
      NextSiblingValid(maxChild);
    }
  }
}
