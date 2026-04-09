include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module AllocationPermanence {

  import opened TumblerAlgebra

  // T8 — AllocationPermanence
  // The set of allocated addresses is monotonically non-decreasing.
  // No operation removes an allocated address from the address space.
  ghost predicate AllocationPermanence(before: set<Tumbler>, after: set<Tumbler>) {
    before <= after
  }

  // Transitivity: if permanence holds at each step, it holds across
  // any chain of states — establishing "for all subsequent states."
  lemma Transitive(s1: set<Tumbler>, s2: set<Tumbler>, s3: set<Tumbler>)
    requires AllocationPermanence(s1, s2)
    requires AllocationPermanence(s2, s3)
    ensures AllocationPermanence(s1, s3)
  { }

}
