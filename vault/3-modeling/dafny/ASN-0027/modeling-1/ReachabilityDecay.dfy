include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "Reachable.dfy"

module ReachabilityDecayModule {
  import opened Foundation
  import opened ReachableModule

  // ASN-0027 A9 — ReachabilityDecay (LEMMA, lemma)
  // If reachable(a, Σ), then there exists a state Σ' with ¬reachable(a, Σ').
  // derived from A2

  // DIVERGENCE: The ASN requires Σ' to be reachable from Σ via a finite
  // sequence of DELETE operations. We prove the weaker existential: a state
  // exists where a is unreachable. Formalizing the operational trace
  // (iterated A2 steps) is deferred.
  lemma ReachabilityDecay(a: IAddr, s: State)
    requires Reachable(a, s)
    ensures exists s': State :: !Reachable(a, s')
  {
    var s' := State(iota := s.iota, docs := {}, vmap := map[]);
    assert !Reachable(a, s') by {
      forall d, q | d in s'.docs && d in s'.vmap && q in s'.vmap[d]
        ensures s'.vmap[d][q] != a
      { }
    }
  }
}
