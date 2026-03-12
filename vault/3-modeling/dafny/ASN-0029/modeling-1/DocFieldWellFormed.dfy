include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"

module DocFieldWellFormedModule {
  import opened TumblerAlgebra
  import opened Foundation
  import SubspaceDisjointness

  // D14a — DocFieldWellFormed (INV, predicate(DocId))
  // (A d ∈ Σ.D : let (N, U, D) = fields(d) : #D ≥ 1 ∧ (A i : 1 ≤ i ≤ #D : Dᵢ > 0))

  // Document address: exactly 2 zero separators (N.0.U.0.D₁...Dₖ)
  predicate IsDocAddress(d: DocId) {
    SubspaceDisjointness.HasKZeros(d.components, 2, 0) &&
    !SubspaceDisjointness.HasKZeros(d.components, 3, 0)
  }

  // Position of the second zero separator
  function SecondZeroPos(d: DocId): nat
    requires IsDocAddress(d)
    ensures SecondZeroPos(d) < |d.components|
  {
    SubspaceDisjointness.KthZero(d.components, 2, 0)
  }

  // Document field: components after the second zero
  function DocFieldComponents(d: DocId): seq<nat>
    requires IsDocAddress(d)
  {
    d.components[SecondZeroPos(d) + 1..]
  }

  // D14a: document field has ≥ 1 component, each strictly positive
  predicate DocFieldWellFormed(d: DocId)
    requires IsDocAddress(d)
  {
    |DocFieldComponents(d)| >= 1 &&
    forall i :: 0 <= i < |DocFieldComponents(d)| ==> DocFieldComponents(d)[i] > 0
  }
}
