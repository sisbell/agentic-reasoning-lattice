include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module AccessibilityPartition {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0030 A2 — AccessibilityPartition (LEMMA, lemma)
  // derived from P2 (ReferentiallyComplete, ASN-0026)

  // (i) active: allocated and reachable
  ghost predicate Active(a: IAddr, s: State) {
    a in Allocated(s) && VisibleInSystem(a, s)
  }

  // (ii) unreferenced: allocated but not reachable
  ghost predicate Unreferenced(a: IAddr, s: State) {
    a in Allocated(s) && !VisibleInSystem(a, s)
  }

  // (iii) unallocated
  ghost predicate Unallocated(a: IAddr, s: State) {
    a !in Allocated(s)
  }

  // Key sub-property: J0/P2 rules out the fourth combination
  // (reachable but unallocated)
  lemma ReachableImpliesAllocated(a: IAddr, s: State)
    requires WellFormed(s)
    requires VisibleInSystem(a, s)
    ensures a in Allocated(s)
  { }

  // A2: the three categories are exhaustive and mutually exclusive
  lemma AccessibilityPartition(a: IAddr, s: State)
    requires WellFormed(s)
    ensures Active(a, s) || Unreferenced(a, s) || Unallocated(a, s)
    ensures !(Active(a, s) && Unreferenced(a, s))
    ensures !(Active(a, s) && Unallocated(a, s))
    ensures !(Unreferenced(a, s) && Unallocated(a, s))
  { }
}
