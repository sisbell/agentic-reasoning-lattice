include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// S7a — DocumentScopedAllocation
module DocumentScopedAllocation {
  import opened TumblerAlgebra
  import TumblerHierarchy

  type Val(==)

  // Two-space state: content store + known document prefixes
  datatype State = State(C: map<Tumbler, Val>, documents: set<Tumbler>)

  // Origin — document-level prefix N.0.U.0.D
  // E1Pos(a) is the position of the first element component;
  // truncating at E1Pos(a) - 1 removes the element field and its
  // leading zero separator, yielding the document prefix.
  function Origin(a: Tumbler): Tumbler
    requires TumblerHierarchy.HasElementField(a)
    ensures IsPrefix(Origin(a), a)
  {
    Tumbler(a.components[..TumblerHierarchy.E1Pos(a) - 1])
  }

  // S7a — DocumentScopedAllocation
  // DIVERGENCE: The ASN states the origin identifies "the document whose
  // owner performed the allocation." This provenance guarantee depends on
  // the allocation protocol (T9, T10 from ASN-0034). The predicate
  // captures the structural invariant: every stored address has an element
  // field and its document-level prefix belongs to the known document set.
  ghost predicate DocumentScopedAllocation(s: State) {
    forall a :: a in s.C ==>
      TumblerHierarchy.HasElementField(a) &&
      Origin(a) in s.documents
  }
}
