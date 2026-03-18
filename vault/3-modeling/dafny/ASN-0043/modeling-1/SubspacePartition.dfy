include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// L0 — SubspacePartition
module SubspacePartition {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // Subspace identifiers — concrete distinct values
  const S_C: nat := 1  // content subspace
  const S_L: nat := 2  // link subspace

  // State — domains of the link store and content store
  datatype State = State(
    linkDomain: set<Tumbler>,
    contentDomain: set<Tumbler>
  )

  // L0 — SubspacePartition
  // Every link address has subspace identifier S_L, every content address
  // has subspace identifier S_C.
  ghost predicate SubspacePartition(sigma: State) {
    (forall a :: a in sigma.linkDomain ==>
      TumblerHierarchy.HasElementField(a) && TumblerHierarchy.E1(a) == S_L) &&
    (forall a :: a in sigma.contentDomain ==>
      TumblerHierarchy.HasElementField(a) && TumblerHierarchy.E1(a) == S_C)
  }

  // Disjointness follows from distinct subspace identifiers
  lemma SubspacePartitionImpliesDisjoint(sigma: State)
    requires SubspacePartition(sigma)
    ensures sigma.linkDomain !! sigma.contentDomain
  { }
}
