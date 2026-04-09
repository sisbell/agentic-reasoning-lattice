include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "Reachable.dfy"

module ReachabilityNonMonotone {
  import opened TumblerAlgebra
  import opened Foundation
  import Reachable

  // ASN-0030 A1 — ReachabilityNonMonotone (LEMMA, lemma)
  // ¬[reachable(a, d) in Σ ⟹ reachable(a, d) in Σ']
  // Witness: DELETE on document d can remove the V-space mappings
  // that made a reachable through d.

  lemma ReachabilityNonMonotone()
    ensures exists s: State, s': State, a: IAddr, d: DocId ::
      d in s.vmap && Reachable.Reachable(a, d, s) &&
      d in s'.vmap && !Reachable.Reachable(a, d, s')
  {
    var a := Tumbler([1]);
    var d := Tumbler([2]);
    var q := TextPos(1);

    var s := State(
      iota := map[a := Value(0), d := Value(1)],
      docs := {d},
      vmap := map[d := map[q := a]]
    );

    var s' := State(
      iota := map[a := Value(0), d := Value(1)],
      docs := {d},
      vmap := map[d := map[]]
    );

    assert q in s.vmap[d] && s.vmap[d][q] == a;
    assert Reachable.Reachable(a, d, s);
    assert !Reachable.Reachable(a, d, s');
  }
}
