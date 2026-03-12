include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/IVSpaceProperties/CrossDocVIndependent.dfy"

module InclusionNonDestruction {
  import opened Foundation
  import CrossDocVIndependent

  // D8 — InclusionNonDestruction (LEMMA, lemma)
  // Derived from P7 (CrossDocVIndependent, ASN-0026).
  //
  //   [target(COPY) = d₂ ∧ d₁ ≠ d₂ ⟹ Σ'.V(d₁) = Σ.V(d₁)]

  lemma InclusionNonDestruction(s: State, s': State, d1: DocId, d2: DocId)
    requires d1 in s.docs && d1 in s.vmap
    requires d1 != d2
    requires CrossDocVIndependent.CrossDocVIndependent(s, s', d2)
    ensures d1 in s'.vmap && s'.vmap[d1] == s.vmap[d1]
  { }
}
