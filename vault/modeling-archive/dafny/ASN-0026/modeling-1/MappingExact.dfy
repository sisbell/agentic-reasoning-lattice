include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module MappingExact {
  import opened Foundation

  // ASN-0026 P3 — MappingExact (INV, predicate(State))
  // RETRIEVE(d, p) = Sigma.I(Sigma.V(d)(p)) for all valid (d, p)

  // RETRIEVE: operational delivery — two-level composition V then I
  function Retrieve(s: State, d: DocId, q: VPos): Value
    requires d in s.vmap
    requires q in s.vmap[d]
    requires s.vmap[d][q] in s.iota
  {
    s.iota[s.vmap[d][q]]
  }

  ghost predicate MappingExact(s: State) {
    forall d :: d in s.docs && d in s.vmap ==>
      forall q :: q in s.vmap[d] ==>
        s.vmap[d][q] in Allocated(s) &&
        Retrieve(s, d, q) == s.iota[s.vmap[d][q]]
  }
}
