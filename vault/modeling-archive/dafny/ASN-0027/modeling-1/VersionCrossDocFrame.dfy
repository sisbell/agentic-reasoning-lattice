include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module VersionCrossDocFrame {
  import opened Foundation

  // ASN-0027 A5.frame-doc — VersionCrossDocFrame (FRAME, ensures)
  // (A d'' : d'' ∈ Σ.D : Σ'.V(d'') = Σ.V(d''))
  // All existing documents are unchanged by CREATENEWVERSION.
  // No target exclusion: the new document d' is fresh (d' ∉ Σ.D),
  // so every d'' in Σ.D is preserved.
  ghost predicate VersionCrossDocFrame(s: State, s': State) {
    forall d :: d in s.docs && d in s.vmap ==>
      d in s'.vmap && s'.vmap[d] == s.vmap[d]
  }
}
