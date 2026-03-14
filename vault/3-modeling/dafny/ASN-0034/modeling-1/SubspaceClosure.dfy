include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// TA7a — SubspaceClosure
module SubspaceClosure {
  import opened TumblerAlgebra

  // Addition closure: [x] ⊕ [n] = [x + n] ∈ S₁
  lemma AdditionClosure(x: nat, n: nat)
    requires x > 0
    requires n > 0
    ensures PositiveTumbler(Tumbler([n]))
    ensures TumblerAdd(Tumbler([x]), Tumbler([n])) == Tumbler([x + n])
    ensures PositiveTumbler(Tumbler([x + n]))
  {
    assert Tumbler([n]).components[0] != 0;
    assert Tumbler([x + n]).components[0] != 0;
  }

  // Subtraction closure: [x] ⊖ [n] = [x - n] ∈ S₁ ∪ {[0]}
  lemma SubtractionClosure(x: nat, n: nat)
    requires x > 0
    requires n > 0
    requires x >= n
    ensures Subtractable(Tumbler([x]), Tumbler([n]))
    ensures TumblerSubtract(Tumbler([x]), Tumbler([n])) == Tumbler([x - n])
    ensures x > n ==> PositiveTumbler(Tumbler([x - n]))
  {
    if x > n {
      assert Tumbler([x - n]).components[0] != 0;
    }
  }
}
