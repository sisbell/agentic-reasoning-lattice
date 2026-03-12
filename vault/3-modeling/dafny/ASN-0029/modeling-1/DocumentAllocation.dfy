include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"

module DocumentAllocationModule {
  import opened TumblerAlgebra
  import opened Foundation
  import HierarchicalParsing

  // ASN-0029 D1 — DocumentAllocation (INV, predicate(DocId, DocId))
  // per-allocator: within each allocator stream, allocation order ⊆ address order

  // Document-level address: at least 5 components, exactly 2 zero separators
  predicate IsDocAddr(d: Tumbler) {
    |d.components| >= 5 &&
    HierarchicalParsing.CountZeros(d.components) == 2
  }

  // SameAllocator: both doc-level, same length, identical prefix except last component.
  // Captures both allocator kinds:
  //   Root allocator: same account+zero prefix, differing D₁
  //   Child allocator: same parent prefix, differing last doc component
  ghost predicate SameAllocator(d1: Tumbler, d2: Tumbler) {
    IsDocAddr(d1) && IsDocAddr(d2) &&
    |d1.components| == |d2.components| &&
    d1.components[..|d1.components| - 1] == d2.components[..|d2.components| - 1]
  }

  // D1 — DocumentAllocation
  // DIVERGENCE: allocated_before(d1, d2) is encoded by parameter ordering
  // convention, not as an explicit temporal relation. The full D1 invariant —
  // that temporal allocation order agrees with tumbler address order — is
  // enforced by the inc mechanism (T10a) being monotone. This predicate
  // captures the structural consequence for a given pair where d1 is known
  // to have been allocated before d2.
  ghost predicate DocumentAllocation(d1: DocId, d2: DocId) {
    SameAllocator(d1, d2) ==> LessThan(d1, d2)
  }
}
