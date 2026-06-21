// ASN-0034: T8 AllocationPermanence — INV (theorem)
// Once allocated, an address remains allocated through every admissible transition.
include "./NoDeallocation.dfy"

module AllocationPermanence {
  import opened AllocatedSet
  import ND = NoDeallocation

  // T8 invariant: any admissible step is non-decreasing on Allocated.
  ghost predicate AllocationPermanence(s: State, s': State)
    requires ValidState(s) && ValidState(s')
  {
    Allocated(s) <= Allocated(s')
  }

  // T8 holds for every admissible single step.
  lemma AllocationPermanenceHolds(s: State, s': State)
    requires ValidState(s) && ValidState(s')
    requires (exists a :: T1Step(s, s', a)) || (exists a :: T2Step(s, s', a)) || T3Step(s, s')
    ensures AllocationPermanence(s, s')
  {
    ND.NoDeallocation(s, s');
  }
}
