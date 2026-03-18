include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "Reachable.dfy"

module ReachabilityNonPermanentModule {
  import opened TumblerAlgebra
  import opened Foundation
  import opened ReachableModule

  // ASN-0027 A0 — ReachabilityNonPermanent (LEMMA, lemma)
  // There exist transitions Σ → Σ' such that reachable(a, Σ) ∧ ¬reachable(a, Σ').
  // derived from A2

  lemma ReachabilityNonPermanent()
    ensures exists a: IAddr, s: State, s': State ::
              Reachable(a, s) && !Reachable(a, s')
  {
    var a := Tumbler([1]);
    var d := Tumbler([2]);

    var s := State(
      iota := map[a := Value(1), d := Value(2)],
      docs := {d},
      vmap := map[d := map[TextPos(1) := a]]
    );

    var s' := State(
      iota := map[a := Value(1), d := Value(2)],
      docs := {d},
      vmap := map[d := map[]]
    );

    assert Reachable(a, s) by {
      assert d in s.docs && d in s.vmap && TextPos(1) in s.vmap[d] && s.vmap[d][TextPos(1)] == a;
    }

    assert !Reachable(a, s') by {
      forall d', q | d' in s'.docs && d' in s'.vmap && q in s'.vmap[d']
        ensures s'.vmap[d'][q] != a
      { }
    }
  }
}
