// ASN-0034: T2 — IntrinsicComparison
// The order relation T1 is computable from the two tumblers alone, without
// consulting any external data structure. The scan examines at most #a and
// at most #b component pairs.
include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"
include "./CanonicalRepresentation.dfy"
include "./NatStrictTotalOrder.dfy"
include "./NatWellOrdering.dfy"
include "./NatDiscreteness.dfy"
include "./NatAdditionOrderAndSuccessor.dfy"

module IntrinsicComparison {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened CanonicalRepresentation
  import opened NatStrictTotalOrder
  import opened NatWellOrdering
  import opened NatDiscreteness
  import opened NatAdditionOrderAndSuccessor
  import opened NatCarrierSet

  datatype Comparison = LT | EQ | GT

  // Constructive scan starting at index i (0-indexed; the next pair examined
  // is position i+1 of both tumblers). Pure function of a and b's components
  // and lengths — no external state participates.
  function CompareFrom(a: Tumbler, b: Tumbler, i: nat): Comparison
    requires InT(a) && InT(b)
    requires 0 <= i <= Length(a) && 0 <= i <= Length(b)
    decreases (if Length(a) <= Length(b) then Length(a) else Length(b)) - i
  {
    if i == Length(a) && i == Length(b) then EQ
    else if i == Length(a) then LT
    else if i == Length(b) then GT
    else
      var ai := Component(a, i + 1);
      var bi := Component(b, i + 1);
      if Less(ai, bi) then LT
      else if Less(bi, ai) then GT
      else CompareFrom(a, b, i + 1)
  }

  function Compare(a: Tumbler, b: Tumbler): Comparison
    requires InT(a) && InT(b)
  {
    CompareFrom(a, b, 0)
  }

  // T2: the constructive scan decides T1's order relation.
  lemma IntrinsicComparison(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    ensures Compare(a, b) == LT <==> LexicographicOrder.LexicographicOrder(a, b)
    ensures Compare(a, b) == GT <==> LexicographicOrder.LexicographicOrder(b, a)
    ensures Compare(a, b) == EQ <==> a == b
  {
    CompareFromCorrect(a, b, 0);
  }

  // Inductive correctness of the scan: given pointwise agreement up to position
  // i, the scan starting at i decides the order on the full tumblers.
  lemma CompareFromCorrect(a: Tumbler, b: Tumbler, i: nat)
    requires InT(a) && InT(b)
    requires 0 <= i <= Length(a) && 0 <= i <= Length(b)
    requires forall j :: 1 <= j <= i ==> Component(a, j) == Component(b, j)
    ensures CompareFrom(a, b, i) == LT <==> LexicographicOrder.LexicographicOrder(a, b)
    ensures CompareFrom(a, b, i) == GT <==> LexicographicOrder.LexicographicOrder(b, a)
    ensures CompareFrom(a, b, i) == EQ <==> a == b
    decreases (if Length(a) <= Length(b) then Length(a) else Length(b)) - i
  {
    if i == Length(a) && i == Length(b) {
      Extensionality(a, b);
    } else if i == Length(a) {
      if LexicographicOrder.LexicographicOrder(b, a) {
        var k :| 1 <= k
              && (forall i' :: 1 <= i' < k ==>
                    i' <= Length(b) && i' <= Length(a) &&
                    Component(b, i') == Component(a, i'))
              && ((k <= Length(b) && k <= Length(a) &&
                   Less(Component(b, k), Component(a, k)))
                  || (k == Length(b) + 1 && k <= Length(a)));
        if k <= Length(b) && k <= Length(a) && Less(Component(b, k), Component(a, k)) {
          Irreflexive(Component(a, k));
        }
      }
    } else if i == Length(b) {
    } else {
      var ai := Component(a, i + 1);
      var bi := Component(b, i + 1);
      if Less(ai, bi) {
      } else if Less(bi, ai) {
      } else {
        CompareFromCorrect(a, b, i + 1);
      }
    }
  }
}
