include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module IntrinsicComparison {

  import opened TumblerAlgebra

  // T2 — IntrinsicComparison
  // The order relation T1 is computable from the two tumblers alone,
  // without consulting any external data structure. The comparison
  // examines at most min(#a, #b) component pairs.

  // Computable comparison function — no ghost, no external state
  function CompareRec(a: seq<nat>, b: seq<nat>, i: nat): bool
    requires i <= |a| && i <= |b|
    decreases |a| - i
  {
    if i == |a| then i < |b|
    else if i == |b| then false
    else if a[i] < b[i] then true
    else if a[i] > b[i] then false
    else CompareRec(a, b, i + 1)
  }

  function Compare(a: Tumbler, b: Tumbler): bool {
    CompareRec(a.components, b.components, 0)
  }

  // Direction 1: Compare true implies LessThan
  lemma CompareImpliesLessThan(a: seq<nat>, b: seq<nat>, i: nat)
    requires i <= |a| && i <= |b|
    requires CompareRec(a, b, i)
    requires forall j :: 0 <= j < i ==> a[j] == b[j]
    ensures LessThan(Tumbler(a), Tumbler(b))
    decreases |a| - i
  { }

  // Direction 2: LessThan implies Compare true
  lemma LessThanImpliesCompare(a: seq<nat>, b: seq<nat>, i: nat)
    requires i <= |a| && i <= |b|
    requires LessThan(Tumbler(a), Tumbler(b))
    requires forall j :: 0 <= j < i ==> a[j] == b[j]
    ensures CompareRec(a, b, i)
    decreases |a| - i
  { }

  // Compare is equivalent to the ghost predicate LessThan
  lemma IntrinsicComparison(a: Tumbler, b: Tumbler)
    ensures Compare(a, b) <==> LessThan(a, b)
  {
    if Compare(a, b) {
      CompareImpliesLessThan(a.components, b.components, 0);
    }
    if LessThan(a, b) {
      LessThanImpliesCompare(a.components, b.components, 0);
    }
  }
}
