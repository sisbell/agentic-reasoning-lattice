include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/TwoSpace/ISpaceMonotone.dfy"

module AccessibilityTransitions {
  import opened TumblerAlgebra
  import opened Foundation
  import ISpaceMonotone

  // ASN-0030 A3 — AccessibilityTransitions (LEMMA, lemma)
  // derived from P1 (ISpaceMonotone), operation definitions
  //
  // Transitions between accessibility states (from A2):
  //   (a) iii → i:   permitted
  //   (b) i   → ii:  permitted
  //   (c) ii  → i:   permitted by invariants
  //   (d) i   → iii: forbidden — violates P1
  //   (e) ii  → iii: forbidden — violates P1
  //   (f) iii → ii:  composite via (a) then (b)

  // Accessibility categories (from A2)
  ghost predicate Active(a: IAddr, s: State) {
    a in Allocated(s) && VisibleInSystem(a, s)
  }

  ghost predicate Unreferenced(a: IAddr, s: State) {
    a in Allocated(s) && !VisibleInSystem(a, s)
  }

  ghost predicate Unallocated(a: IAddr, s: State) {
    a !in Allocated(s)
  }

  // (d) active → unallocated: forbidden — violates P1
  lemma ForbiddenActiveToUnallocated(s: State, s': State, a: IAddr)
    requires Active(a, s)
    requires ISpaceMonotone.ISpaceMonotone(s, s')
    ensures !Unallocated(a, s')
  { }

  // (e) unreferenced → unallocated: forbidden — violates P1
  lemma ForbiddenUnreferencedToUnallocated(s: State, s': State, a: IAddr)
    requires Unreferenced(a, s)
    requires ISpaceMonotone.ISpaceMonotone(s, s')
    ensures !Unallocated(a, s')
  { }

  // (f) P1 composes transitively, enabling composite paths
  // such as iii → i (step a) then i → ii (step b) to achieve iii → ii.
  lemma MonotoneTransitive(s: State, sMid: State, s': State)
    requires ISpaceMonotone.ISpaceMonotone(s, sMid)
    requires ISpaceMonotone.ISpaceMonotone(sMid, s')
    ensures ISpaceMonotone.ISpaceMonotone(s, s')
  { }
}
