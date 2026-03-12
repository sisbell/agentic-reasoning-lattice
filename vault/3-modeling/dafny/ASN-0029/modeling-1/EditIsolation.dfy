include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/IVSpaceProperties/CrossDocVIndependent.dfy"

module EditIsolation {
  import opened Foundation
  import CrossDocVIndependent

  // D9 — EditIsolation (LEMMA, lemma)
  // Derived from P7 (CrossDocVIndependent, ASN-0026).
  //
  //   [op modifies Σ.V(d₁) ∧ d₁ ≠ d₂ ⟹ Σ'.V(d₂) = Σ.V(d₂)]

  lemma EditIsolation(s: State, s': State, d1: DocId, d2: DocId)
    requires d2 in s.docs && d2 in s.vmap
    requires d1 != d2
    requires CrossDocVIndependent.CrossDocVIndependent(s, s', d1)
    ensures d2 in s'.vmap && s'.vmap[d2] == s.vmap[d2]
  { }
}
