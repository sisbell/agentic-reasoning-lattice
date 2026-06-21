// ASN-0034: NoDeallocation — AXIOM
// Design constraint (Nelson permanence): no operation in transition vocabulary
// Σ = {T1,T2,T3} may shrink the allocated address set.
include "./AllocatedSet.dfy"

module NoDeallocation {
  import opened AllocatedSet

  lemma {:axiom} NoDeallocation(s: State, s': State)
    requires ValidState(s) && ValidState(s')
    requires (exists a :: T1Step(s, s', a)) || (exists a :: T2Step(s, s', a)) || T3Step(s, s')
    ensures Allocated(s) <= Allocated(s')
}
