include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module NonInjective {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0026 P5 — NonInjective (LEMMA)
  // V-space map is not required to be injective.
  // Self-transclusion and cross-document transclusion are both permitted.

  // Self-transclusion: same document, two positions share an address
  lemma SelfTransclusionPermitted()
    ensures exists s: State, d: DocId, q1: VPos, q2: VPos ::
      WellFormed(s) && d in s.docs && d in s.vmap &&
      q1 in s.vmap[d] && q2 in s.vmap[d] &&
      q1 != q2 && s.vmap[d][q1] == s.vmap[d][q2]
  {
    var d := Tumbler([1]);
    var a := Tumbler([2]);
    var vm: map<VPos, IAddr> := map[TextPos(1) := a, TextPos(2) := a];
    var s := State(
      iota := map[d := Value(0), a := Value(1)],
      docs := {d},
      vmap := map[d := vm]
    );
    assert vm.Keys == {TextPos(1), TextPos(2)};
    assert forall q :: q in vm ==> q == TextPos(1) || q == TextPos(2);
    assert 1 in TextOrdinals(s, d);
    assert 2 in TextOrdinals(s, d);
    assert forall n :: n in TextOrdinals(s, d) ==> n == 1 || n == 2;
    assert TextOrdinals(s, d) == {1, 2};
    assert LinkOrdinals(s, d) == {};
    assert WellFormed(s);
  }

  // Cross-document transclusion: distinct documents share an address
  lemma CrossTransclusionPermitted()
    ensures exists s: State, d1: DocId, d2: DocId, q1: VPos, q2: VPos ::
      WellFormed(s) && d1 in s.docs && d2 in s.docs &&
      d1 != d2 && d1 in s.vmap && d2 in s.vmap &&
      q1 in s.vmap[d1] && q2 in s.vmap[d2] &&
      s.vmap[d1][q1] == s.vmap[d2][q2]
  {
    var d1 := Tumbler([1]);
    var d2 := Tumbler([2]);
    var a := Tumbler([3]);
    var vm1: map<VPos, IAddr> := map[TextPos(1) := a];
    var vm2: map<VPos, IAddr> := map[TextPos(1) := a];
    var s := State(
      iota := map[d1 := Value(0), d2 := Value(1), a := Value(2)],
      docs := {d1, d2},
      vmap := map[d1 := vm1, d2 := vm2]
    );
    assert s.vmap[d1] == vm1;
    assert s.vmap[d2] == vm2;
    assert forall q :: q in vm1 ==> q == TextPos(1);
    assert forall q :: q in vm2 ==> q == TextPos(1);
    assert 1 in TextOrdinals(s, d1);
    assert forall n :: n in TextOrdinals(s, d1) ==> n == 1;
    assert TextOrdinals(s, d1) == {1};
    assert 1 in TextOrdinals(s, d2);
    assert forall n :: n in TextOrdinals(s, d2) ==> n == 1;
    assert TextOrdinals(s, d2) == {1};
    assert LinkOrdinals(s, d1) == {};
    assert LinkOrdinals(s, d2) == {};
    assert WellFormed(s);
  }
}
