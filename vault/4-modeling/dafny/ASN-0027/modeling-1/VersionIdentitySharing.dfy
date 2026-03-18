include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module VersionIdentitySharing {
  import opened Foundation

  // ASN-0027 A5.identity — VersionIdentitySharing (POST, ensures)
  // |Σ'.V(d')| = n_d ∧ (A j : 1 ≤ j ≤ n_d : Σ'.V(d')(j) = Σ.V(d)(j))
  // After CREATENEWVERSION: the new document d' has an identical V-space
  // mapping to source document d. Map equality captures both same-length
  // (same key set) and same-content (same value at each key).
  ghost predicate VersionIdentitySharing(s: State, s': State, d: DocId, dNew: DocId) {
    d in s.vmap && dNew in s'.vmap &&
    s'.vmap[dNew] == s.vmap[d]
  }
}
