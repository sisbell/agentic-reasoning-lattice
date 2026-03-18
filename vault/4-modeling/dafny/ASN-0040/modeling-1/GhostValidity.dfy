include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module GhostValidity {
  import opened TumblerAlgebra

  // B3 — GhostValidity
  // For any t, if t is occupied then t must be baptized.
  // The four ASN cases are exhaustive; only (¬baptized ∧ occupied) is forbidden.

  // DIVERGENCE: The ASN's baptismal state Σ contains only Σ.B. "Occupied" is
  // a downstream concept defined by content operations. This module models
  // occupancy as an explicit set to state the constraint; content-layer
  // modules will instantiate what "occupied" means concretely.
  datatype ContentState = ContentState(baptized: set<Tumbler>, occupied: set<Tumbler>)

  ghost predicate GhostValidity(s: ContentState) {
    s.occupied <= s.baptized
  }
}
