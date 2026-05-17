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

  // Witness for LexOrder(a, b) via T1 case (ii) at k = Length(a) + 1.
  // The trigger registration via Component(b, Length(a)+1) forces Z3 to
  // consider k = Length(a) + 1 as an existential witness candidate.
  lemma LexOrderShorterWitness(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires Length(a) < Length(b)
    requires forall j :: 1 <= j <= Length(a) ==> Component(a, j) == Component(b, j)
    ensures LexicographicOrder.LexicographicOrder(a, b)
  {
    var w: nat := Length(a) + 1;
    assert 1 <= w;
    assert w <= Length(b);
    // Register trigger Component(b, w) so Dafny considers k = w for the existential.
    ghost var bw := Component(b, w);
    assert forall i :: 1 <= i < w ==>
            i <= Length(a) && i <= Length(b) &&
            Component(a, i) == Component(b, i);
  }

  // Witness for LexOrder(a, b) via T1 case (i) at k = i + 1 with Less divergence.
  lemma LexOrderDivergenceWitness(a: Tumbler, b: Tumbler, i: nat)
    requires InT(a) && InT(b)
    requires 0 <= i < Length(a) && 0 <= i < Length(b)
    requires forall j :: 1 <= j <= i ==> Component(a, j) == Component(b, j)
    requires Less(Component(a, i + 1), Component(b, i + 1))
    ensures LexicographicOrder.LexicographicOrder(a, b)
  {
    ghost var k: nat :| k == i + 1;
    assert 1 <= k;
    assert k <= Length(a) && k <= Length(b);
    assert Less(Component(a, k), Component(b, k));
    assert forall i' :: 1 <= i' < k ==>
            i' <= Length(a) && i' <= Length(b) &&
            Component(a, i') == Component(b, i');
  }

  // Helper: when a is a strict componentwise prefix of b, LexOrder(a, b) holds
  // (via T1 case (ii)) but LexOrder(b, a) cannot — its witness would have to
  // be either a position where they agree (contradicting Less) or a length
  // beyond Length(b), which exceeds Length(a).
  lemma ShorterPrefix(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires Length(a) < Length(b)
    requires forall j :: 1 <= j <= Length(a) ==> Component(a, j) == Component(b, j)
    ensures LexicographicOrder.LexicographicOrder(a, b)
    ensures !LexicographicOrder.LexicographicOrder(b, a)
    ensures a != b
  {
    LexOrderShorterWitness(a, b);

    if LexicographicOrder.LexicographicOrder(b, a) {
      var k :| 1 <= k
            && (forall i' :: 1 <= i' < k ==>
                  i' <= Length(b) && i' <= Length(a) &&
                  Component(b, i') == Component(a, i'))
            && ((k <= Length(b) && k <= Length(a) &&
                 Less(Component(b, k), Component(a, k)))
                || (k == Length(b) + 1 && k <= Length(a)));
      if k <= Length(b) && k <= Length(a) && Less(Component(b, k), Component(a, k)) {
        assert Component(a, k) == Component(b, k);
        Irreflexive(Component(a, k));
      }
    }
  }

  // Helper: at a divergence position with Less(a_{i+1}, b_{i+1}) and prior
  // agreement, LexOrder(a, b) holds via T1 case (i) and LexOrder(b, a) cannot
  // — any witness k' would either agree at k' ≤ i (impossible to Less) or
  // diverge at i+1 with the inequality reversed (contradicting trichotomy).
  lemma Divergence(a: Tumbler, b: Tumbler, i: nat)
    requires InT(a) && InT(b)
    requires 0 <= i < Length(a) && 0 <= i < Length(b)
    requires forall j :: 1 <= j <= i ==> Component(a, j) == Component(b, j)
    requires Less(Component(a, i + 1), Component(b, i + 1))
    ensures LexicographicOrder.LexicographicOrder(a, b)
    ensures !LexicographicOrder.LexicographicOrder(b, a)
    ensures a != b
  {
    LexOrderDivergenceWitness(a, b, i);

    if LexicographicOrder.LexicographicOrder(b, a) {
      var k :| 1 <= k
            && (forall i' :: 1 <= i' < k ==>
                  i' <= Length(b) && i' <= Length(a) &&
                  Component(b, i') == Component(a, i'))
            && ((k <= Length(b) && k <= Length(a) &&
                 Less(Component(b, k), Component(a, k)))
                || (k == Length(b) + 1 && k <= Length(a)));
      if k <= Length(b) && k <= Length(a) && Less(Component(b, k), Component(a, k)) {
        if k <= i {
          assert Component(a, k) == Component(b, k);
          Irreflexive(Component(a, k));
        } else {
          assert k == i + 1;
          Asymmetric(Component(a, i + 1), Component(b, i + 1));
        }
      }
    }
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
      ShorterPrefix(a, b);
    } else if i == Length(b) {
      ShorterPrefix(b, a);
    } else {
      var ai := Component(a, i + 1);
      var bi := Component(b, i + 1);
      if Less(ai, bi) {
        Divergence(a, b, i);
      } else if Less(bi, ai) {
        Divergence(b, a, i);
      } else {
        CompareFromCorrect(a, b, i + 1);
      }
    }
  }
}
