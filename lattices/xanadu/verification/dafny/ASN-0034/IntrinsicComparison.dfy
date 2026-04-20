include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"

module IntrinsicComparison {
  // T2 — IntrinsicComparison

  import opened CarrierSetDefinition
  import opened LexicographicOrder

  datatype Cmp = LT | EQ | GT

  // Computable comparison — scans left-to-right, at most min(|a|,|b|) pairs
  function CompareAt(a: seq<nat>, b: seq<nat>, i: nat): Cmp
    requires i <= |a| && i <= |b|
    decreases |a| - i
  {
    if i == |a| && i == |b| then EQ
    else if i == |a| then LT
    else if i == |b| then GT
    else if a[i] < b[i] then LT
    else if a[i] > b[i] then GT
    else CompareAt(a, b, i + 1)
  }

  function Compare(a: Tumbler, b: Tumbler): Cmp {
    CompareAt(a.components, b.components, 0)
  }

  // Number of component pairs examined by CompareAt
  function PairsExamined(a: seq<nat>, b: seq<nat>, i: nat): nat
    requires i <= |a| && i <= |b|
    decreases |a| - i
  {
    if i == |a| || i == |b| then 0
    else if a[i] != b[i] then 1
    else 1 + PairsExamined(a, b, i + 1)
  }

  lemma PairsExaminedBound(a: seq<nat>, b: seq<nat>, i: nat)
    requires i <= |a| && i <= |b|
    decreases |a| - i
    ensures PairsExamined(a, b, i) <= (if |a| <= |b| then |a| else |b|) - i
  {
  }

  // Inductive core: if first i components agree, CompareAt decides T1
  lemma CompareAtCorrect(a: seq<nat>, b: seq<nat>, i: nat)
    requires i <= |a| && i <= |b|
    requires forall j :: 0 <= j < i ==> j < |a| && j < |b| && a[j] == b[j]
    decreases |a| - i
    ensures CompareAt(a, b, i) == LT <==> LessThan(Tumbler(a), Tumbler(b))
    ensures CompareAt(a, b, i) == EQ <==> Tumbler(a) == Tumbler(b)
    ensures CompareAt(a, b, i) == GT <==> LessThan(Tumbler(b), Tumbler(a))
  { }

  // T2: The computable comparison is equivalent to the T1 ordering
  lemma IntrinsicComparison(a: Tumbler, b: Tumbler)
    ensures Compare(a, b) == LT <==> LessThan(a, b)
    ensures Compare(a, b) == EQ <==> a == b
    ensures Compare(a, b) == GT <==> LessThan(b, a)
    ensures PairsExamined(a.components, b.components, 0) <=
      (if |a.components| <= |b.components| then |a.components| else |b.components|)
  {
    CompareAtCorrect(a.components, b.components, 0);
    PairsExaminedBound(a.components, b.components, 0);
  }
}
