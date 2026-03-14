include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// T1 — LexicographicOrder
module LexicographicOrder {
  import opened TumblerAlgebra

  // T1: Lexicographic ordering defines a strict total order on tumblers.
  // a < b iff there exists k such that all components before k agree and either:
  //   (i) k < |a| and k < |b| and a[k] < b[k], or
  //   (ii) k == |a| and k < |b| (a is a proper prefix of b).
  ghost predicate LexicographicOrder(a: Tumbler, b: Tumbler) {
    LessThan(a, b)
  }

  // Irreflexivity: no tumbler is less than itself
  lemma Irreflexive(a: Tumbler)
    ensures !LexicographicOrder(a, a)
  { }

  // Transitivity: a < b < c implies a < c
  lemma Transitive(a: Tumbler, b: Tumbler, c: Tumbler)
    requires LexicographicOrder(a, b)
    requires LexicographicOrder(b, c)
    ensures LexicographicOrder(a, c)
  {
    var k_ab: nat :| LessThanAt(a, b, k_ab);
    var k_bc: nat :| LessThanAt(b, c, k_bc);
    if k_ab <= k_bc {
      LessThanIntro(a, c, k_ab);
    } else {
      LessThanIntro(a, c, k_bc);
    }
  }

  // Asymmetry: a < b implies not b < a
  lemma Asymmetric(a: Tumbler, b: Tumbler)
    requires LexicographicOrder(a, b)
    ensures !LexicographicOrder(b, a)
  {
    if LexicographicOrder(b, a) {
      Transitive(a, b, a);
      Irreflexive(a);
    }
  }

  // Totality helper: scan from position i to find the divergence point
  lemma TotalScan(a: Tumbler, b: Tumbler, i: nat)
    requires a != b
    requires i <= |a.components| && i <= |b.components|
    requires forall j :: 0 <= j < i ==> a.components[j] == b.components[j]
    ensures LessThan(a, b) || LessThan(b, a)
    decreases (|a.components| - i) + (|b.components| - i)
  {
    if i == |a.components| && i < |b.components| {
      LessThanIntro(a, b, i);
    } else if i < |a.components| && i == |b.components| {
      LessThanIntro(b, a, i);
    } else if i < |a.components| && i < |b.components| {
      if a.components[i] < b.components[i] {
        LessThanIntro(a, b, i);
      } else if a.components[i] > b.components[i] {
        LessThanIntro(b, a, i);
      } else {
        TotalScan(a, b, i + 1);
      }
    }
    // Remaining case: i == |a| && i == |b|. All components agree and same
    // length, so a.components == b.components, contradicting a != b.
  }

  // Totality: distinct tumblers are comparable
  lemma Total(a: Tumbler, b: Tumbler)
    requires a != b
    ensures LexicographicOrder(a, b) || LexicographicOrder(b, a)
  {
    TotalScan(a, b, 0);
  }
}
