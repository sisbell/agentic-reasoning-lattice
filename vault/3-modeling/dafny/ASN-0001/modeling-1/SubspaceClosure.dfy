include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module SubspaceClosure {

  import opened TumblerAlgebra

  // TA7a — SubspaceClosure
  // Algebraic closure of single-component tumblers under Add and Subtract.
  // In the ordinal-only formulation, [x] ⊕ [n] = [x + n] and [x] ⊖ [n] = [x - n].

  lemma AddClosure(x: nat, n: nat)
    requires n > 0
    ensures PositiveTumbler(Tumbler([n]))
    ensures ActionPoint(Tumbler([n])) == 0
    ensures ActionPoint(Tumbler([n])) < |Tumbler([x]).components|
    ensures TumblerAdd(Tumbler([x]), Tumbler([n])) == Tumbler([x + n])
  { }

  lemma SubClosure(x: nat, n: nat)
    requires n > 0
    requires x >= n
    ensures Subtractable(Tumbler([x]), Tumbler([n]))
    ensures TumblerSubtract(Tumbler([x]), Tumbler([n])) == Tumbler([x - n])
  {
    if x == n {
      assert Pad([x], 1) == Pad([n], 1);
    }
  }
}
