// ASN-0034: GlobalUniqueness — INV (theorem)
// No two distinct allocation events in a conforming single-root system
// produce the same address.
// Same-allocator case: T10a.7 (EnumerationInjectivity).
// Cross-allocator case: T10a.6 (DomainDisjointnessPair).
include "./DomainDisjointness.dfy"
include "./EnumerationInjectivity.dfy"

module GlobalUniqueness {
  import opened AllocatorDiscipline
  import opened LengthSeparation
  import opened DomainDisjointness
  import EI = EnumerationInjectivity

  // Invariant: distinct allocation events — (Allocator, index) pairs where
  // A1 != A2 or i != j — produce distinct addresses.
  // The single-root precondition (Root(A1) == Root(A2)) reflects ASN-0034's
  // single-root model: every conforming allocator descends from one n0.
  ghost predicate GlobalUniqueness(A1: Allocator, i: nat, A2: Allocator, j: nat) {
    (AllocatorDiscipline.AllocatorDiscipline(A1) &&
     AllocatorDiscipline.AllocatorDiscipline(A2) &&
     Root(A1) == Root(A2) &&
     (A1 != A2 || i != j))
    ==>
    SiblingAt(A1, i) != SiblingAt(A2, j)
  }

  // Theorem: GlobalUniqueness holds in every conforming single-root system.
  lemma GlobalUniquenessTheorem(A1: Allocator, i: nat, A2: Allocator, j: nat)
    requires AllocatorDiscipline.AllocatorDiscipline(A1)
    requires AllocatorDiscipline.AllocatorDiscipline(A2)
    requires Root(A1) == Root(A2)
    requires A1 != A2 || i != j
    ensures SiblingAt(A1, i) != SiblingAt(A2, j)
    ensures GlobalUniqueness(A1, i, A2, j)
  {
    if A1 == A2 {
      EI.EnumerationInjectivity(A1, i, j);
    } else {
      if SiblingAt(A1, i) == SiblingAt(A2, j) {
        DomainDisjointnessPair(A1, A2, SiblingAt(A1, i));
      }
    }
  }
}
