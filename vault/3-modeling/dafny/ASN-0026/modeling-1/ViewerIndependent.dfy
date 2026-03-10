include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module ViewerIndependent {
  import opened Foundation

  // ASN-0026 P11 — ViewerIndependent (INV, predicate(State))
  // RETRIEVE is a pure function of (DocId, Pos); no viewer, session,
  // or context parameter appears in the protocol signature.

  // Hypothetical extra parameter (viewer, session, or context)
  datatype Viewer = Viewer(id: nat)

  // Xanadu RETRIEVE: pure lookup through I-space / V-space
  function Retrieve(s: State, d: DocId, q: VPos): Value
    requires d in s.vmap
    requires q in s.vmap[d]
    requires s.vmap[d][q] in s.iota
  {
    s.iota[s.vmap[d][q]]
  }

  // Hypothetical delivery accepting an extra viewer parameter.
  // Body resolves through Retrieve — viewer is structurally unused.
  function Delivery(s: State, d: DocId, q: VPos, v: Viewer): Value
    requires d in s.vmap
    requires q in s.vmap[d]
    requires s.vmap[d][q] in s.iota
  {
    Retrieve(s, d, q)
  }

  // P11: delivery is viewer-independent
  ghost predicate ViewerIndependent(s: State) {
    forall d, q, v1, v2 ::
      d in s.docs && d in s.vmap && q in s.vmap[d] && s.vmap[d][q] in s.iota ==>
      Delivery(s, d, q, v1) == Delivery(s, d, q, v2)
  }
}
