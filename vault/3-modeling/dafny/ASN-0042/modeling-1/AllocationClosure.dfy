include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// O16 — AllocationClosure
// (A Σ, Σ', a : Σ → Σ' ∧ a ∈ Σ'.alloc ∖ Σ.alloc
//   ⟹ (E π ∈ Π_Σ : allocated_by_{Σ'}(π, a)))
module AllocationClosure {
  import opened TumblerAlgebra

  datatype Principal = Principal(id: nat)

  datatype State = State(
    alloc: set<Tumbler>,
    principals: set<Principal>
  )

  // O16 — AllocationClosure
  // DIVERGENCE: allocated_by is modeled as an allocator map (Tumbler → Principal)
  // consistent with O5's SubdivisionAuthority. The map makes the existential
  // witness explicit: every newly allocated address must have an entry mapping
  // to a principal in the pre-state.
  ghost predicate AllocationClosure(
    s: State,
    s': State,
    allocator: map<Tumbler, Principal>
  ) {
    forall a :: a in s'.alloc && a !in s.alloc ==>
      a in allocator && allocator[a] in s.principals
  }
}
