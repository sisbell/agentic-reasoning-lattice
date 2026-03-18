include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module ISpaceUnchanged {
  import opened Foundation

  // ASN-0030 A4(a) — ISpaceUnchanged/DELETE (FRAME, ensures)
  // ASN-0030 A4a(a) — ISpaceUnchanged/REARRANGE (FRAME, ensures)
  // Σ'.I = Σ.I
  // Instance of +_ext (ISpaceExtension, ASN-0026) with fresh = ∅.
  // Shared frame condition: neither DELETE nor REARRANGE modifies I-space.
  predicate ISpaceUnchanged(s: State, s': State) {
    s'.iota == s.iota
  }
}
