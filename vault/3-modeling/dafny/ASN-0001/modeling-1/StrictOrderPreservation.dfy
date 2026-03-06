include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module StrictOrderPreservation {

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

  // TA1-strict — StrictOrderPreservation (POST, ensures)
  // (A a, b, w : a < b ∧ w > 0 ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)
  lemma StrictOrderPreservation(a: Tumbler, b: Tumbler, w: Tumbler)
    requires LessThan(a, b)
    requires PositiveTumbler(w)
    requires ActionPoint(w) < |a.components|
    requires ActionPoint(w) < |b.components|
    // k ≥ divergence(a, b)
    requires exists d: nat ::
      (d <= ActionPoint(w) &&
       d < |a.components| && d < |b.components| &&
       a.components[d] != b.components[d] &&
       forall j :: 0 <= j < d ==> a.components[j] == b.components[j])
    ensures LessThan(TumblerAdd(a, w), TumblerAdd(b, w))
  {
    var k := ActionPoint(w);
    var ra := TumblerAdd(a, w);
    var rb := TumblerAdd(b, w);

    var d: nat :| d <= k &&
      d < |a.components| && d < |b.components| &&
      a.components[d] != b.components[d] &&
      (forall j :: 0 <= j < d ==> a.components[j] == b.components[j]);

    LessThanImpliesLessAt(a, b, d);
    LessThanFromWitness(ra, rb, d);
  }

}
