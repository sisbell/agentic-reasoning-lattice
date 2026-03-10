include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "ISpaceFrame.dfy"

module ReferencePermanenceModule {
  import opened Foundation
  import ISpaceFrameModule

  // ASN-0027 A8 — ReferencePermanence (LEMMA, lemma)
  // derived from A1 (ISpaceFrame)
  //
  // For any address in dom(Σ.I), after any finite sequence of operations:
  //   (i)  the address remains in dom(Σ_n.I)
  //   (ii) Σ_n.I(a) = Σ.I(a)

  // A trace: consecutive states each satisfy A1 (ISpaceFrame)
  ghost predicate ValidTrace(trace: seq<State>) {
    forall i :: 0 <= i < |trace| - 1 ==>
      ISpaceFrameModule.ISpaceFrame(trace[i], trace[i + 1])
  }

  // A8: induction over the trace length
  lemma ReferencePermanence(trace: seq<State>, a: IAddr)
    requires |trace| >= 1
    requires ValidTrace(trace)
    requires a in Allocated(trace[0])
    ensures a in Allocated(trace[|trace| - 1])
    ensures trace[|trace| - 1].iota[a] == trace[0].iota[a]
    decreases |trace|
  {
    if |trace| == 1 {
    } else {
      ReferencePermanence(trace[..|trace| - 1], a);
    }
  }
}
