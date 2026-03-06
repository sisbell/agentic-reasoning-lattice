include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module WeakOrderPreservation {

  import opened TumblerAlgebra

  // Bridge: provide a LessThan witness directly
  lemma LessThanFromWitness(a: Tumbler, b: Tumbler, j: nat)
    requires j < |a.components| && j < |b.components|
    requires a.components[j] < b.components[j]
    requires forall i :: 0 <= i < j ==> a.components[i] == b.components[i]
    ensures LessThan(a, b)
  { }

  // Bridge: at the first divergence point, LessThan implies strictly less
  lemma LessThanImpliesLessAt(a: Tumbler, b: Tumbler, j: nat)
    requires LessThan(a, b)
    requires j < |a.components| && j < |b.components|
    requires forall i :: 0 <= i < j ==> a.components[i] == b.components[i]
    requires a.components[j] != b.components[j]
    ensures a.components[j] < b.components[j]
  { }

  // TA1 — WeakOrderPreservation (POST, ensures)
  // a < b ∧ w > 0 ∧ k ≤ min(#a, #b) ⟹ a ⊕ w ≤ b ⊕ w
  lemma WeakOrderPreservation(a: Tumbler, b: Tumbler, w: Tumbler)
    requires LessThan(a, b)
    requires PositiveTumbler(w)
    requires ActionPoint(w) < |a.components|
    requires ActionPoint(w) < |b.components|
    ensures LessThan(TumblerAdd(a, w), TumblerAdd(b, w)) || TumblerAdd(a, w) == TumblerAdd(b, w)
  {
    var k := ActionPoint(w);
    var ra := TumblerAdd(a, w);
    var rb := TumblerAdd(b, w);

    if a.components[..k+1] == b.components[..k+1] {
      // a and b agree on positions 0..k, so results are equal
    } else {
      // Divergence at or before k
      var j := FirstDiff(a.components[..k+1], b.components[..k+1]);
      LessThanImpliesLessAt(a, b, j);
      LessThanFromWitness(ra, rb, j);
    }
  }

}
