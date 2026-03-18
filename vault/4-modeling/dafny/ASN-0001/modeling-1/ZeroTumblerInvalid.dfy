include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module ZeroTumblerInvalid {

  import opened TumblerAlgebra

  // TA6 — ZeroTumblerInvalid
  // A zero tumbler (all components zero) is not a valid address.
  // Every zero tumbler is less than every positive tumbler under T1.

  ghost predicate ZeroTumbler(t: Tumbler) {
    forall i :: 0 <= i < |t.components| ==> t.components[i] == 0
  }

  // Computable comparison (same pattern as LexicographicOrder.CompareSeq)
  function CompareSeq(a: seq<nat>, b: seq<nat>, i: nat): bool
    requires i <= |a| && i <= |b|
    decreases |a| - i
  {
    if i == |a| && i < |b| then true
    else if i >= |a| || i >= |b| then false
    else if a[i] < b[i] then true
    else if a[i] > b[i] then false
    else CompareSeq(a, b, i + 1)
  }

  lemma CompareSound(a: seq<nat>, b: seq<nat>, i: nat)
    requires i <= |a| && i <= |b|
    requires CompareSeq(a, b, i)
    requires forall j :: 0 <= j < i ==> a[j] == b[j]
    ensures LessThan(Tumbler(a), Tumbler(b))
    decreases |a| - i
  { }

  lemma ZeroLessThanPositive(z: Tumbler, p: Tumbler)
    requires ZeroTumbler(z)
    requires PositiveTumbler(p)
    ensures LessThan(z, p)
  {
    ZeroCompares(z.components, p.components, 0);
    CompareSound(z.components, p.components, 0);
  }

  // Zero seq compares less than any seq with a nonzero element
  lemma ZeroCompares(a: seq<nat>, b: seq<nat>, i: nat)
    requires i <= |a| && i <= |b|
    requires forall j :: 0 <= j < |a| ==> a[j] == 0
    requires exists j :: i <= j < |b| && b[j] != 0
    ensures CompareSeq(a, b, i)
    decreases |a| - i
  { }
}
