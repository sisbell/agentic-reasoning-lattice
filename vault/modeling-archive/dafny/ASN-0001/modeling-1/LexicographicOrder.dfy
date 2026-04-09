include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module LexicographicOrder {

  import opened TumblerAlgebra

  // T1 — LexicographicOrder (INV, predicate(Tumbler, Tumbler))
  ghost predicate LexicographicOrder(a: Tumbler, b: Tumbler) {
    LessThan(a, b)
  }

  // Computable comparison for solver reasoning
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

  // Bridge: CompareSeq → LessThan
  lemma CompareSound(a: seq<nat>, b: seq<nat>, i: nat)
    requires i <= |a| && i <= |b|
    requires CompareSeq(a, b, i)
    requires forall j :: 0 <= j < i ==> a[j] == b[j]
    ensures LessThan(Tumbler(a), Tumbler(b))
    decreases |a| - i
  { }

  // Bridge: LessThan → CompareSeq
  lemma CompareComplete(a: seq<nat>, b: seq<nat>, i: nat)
    requires i <= |a| && i <= |b|
    requires LessThan(Tumbler(a), Tumbler(b))
    requires forall j :: 0 <= j < i ==> a[j] == b[j]
    ensures CompareSeq(a, b, i)
    decreases |a| - i
  { }

  // Bridge: neither direction → equal
  lemma CompareEqual(a: seq<nat>, b: seq<nat>, i: nat)
    requires i <= |a| && i <= |b|
    requires !CompareSeq(a, b, i) && !CompareSeq(b, a, i)
    requires forall j :: 0 <= j < i ==> a[j] == b[j]
    ensures a == b
    decreases |a| + |b| - 2 * i
  { }

  // Transitivity for computable comparison
  lemma CompareTransitive(a: seq<nat>, b: seq<nat>, c: seq<nat>, i: nat)
    requires i <= |a| && i <= |b| && i <= |c|
    requires CompareSeq(a, b, i)
    requires CompareSeq(b, c, i)
    ensures CompareSeq(a, c, i)
    decreases |a| - i
  { }

  lemma Irreflexive(a: Tumbler)
    ensures !LexicographicOrder(a, a)
  { }

  lemma Transitive(a: Tumbler, b: Tumbler, c: Tumbler)
    requires LexicographicOrder(a, b)
    requires LexicographicOrder(b, c)
    ensures LexicographicOrder(a, c)
  {
    CompareComplete(a.components, b.components, 0);
    CompareComplete(b.components, c.components, 0);
    CompareTransitive(a.components, b.components, c.components, 0);
    CompareSound(a.components, c.components, 0);
  }

  lemma Asymmetric(a: Tumbler, b: Tumbler)
    requires LexicographicOrder(a, b)
    ensures !LexicographicOrder(b, a)
  {
    if LexicographicOrder(b, a) {
      Transitive(a, b, a);
      Irreflexive(a);
    }
  }

  lemma Trichotomy(a: Tumbler, b: Tumbler)
    ensures LexicographicOrder(a, b) || a == b || LexicographicOrder(b, a)
  {
    if CompareSeq(a.components, b.components, 0) {
      CompareSound(a.components, b.components, 0);
    } else if CompareSeq(b.components, a.components, 0) {
      CompareSound(b.components, a.components, 0);
    } else {
      CompareEqual(a.components, b.components, 0);
    }
  }
}
