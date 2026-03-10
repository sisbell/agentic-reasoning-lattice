include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module ISpaceFrameModule {
  import opened Foundation

  // ASN-0027 A1 — ISpaceFrame (INV, predicate(State, State))
  // transition invariant; all operations
  //
  // For each primitive operation, I-space is either preserved exactly
  // (DELETE, REARRANGE, COPY, CREATENEWVERSION) or extended with fresh
  // addresses (INSERT). The common frame: all existing bindings persist.
  ghost predicate ISpaceFrame(s: State, s': State) {
    forall a :: a in s.iota ==> a in s'.iota && s'.iota[a] == s.iota[a]
  }
}
