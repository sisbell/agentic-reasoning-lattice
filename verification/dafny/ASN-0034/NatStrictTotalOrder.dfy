// ASN-0034: NAT-order
// The natural numbers carry a strict total order under <.
include "./NatCarrierSet.dfy"

module NatStrictTotalOrder {
  import opened NatCarrierSet

  predicate Less(a: Carrier, b: Carrier) { a < b }
  predicate LessOrEqual(a: Carrier, b: Carrier) { Less(a, b) || a == b }
  predicate GreaterOrEqual(a: Carrier, b: Carrier) { LessOrEqual(b, a) }
  predicate Greater(a: Carrier, b: Carrier) { Less(b, a) }

  lemma {:axiom} Irreflexive(a: Carrier)
    ensures !Less(a, a)

  lemma {:axiom} Transitive(a: Carrier, b: Carrier, c: Carrier)
    requires Less(a, b)
    requires Less(b, c)
    ensures Less(a, c)

  lemma {:axiom} Trichotomy(a: Carrier, b: Carrier)
    ensures Less(a, b) || a == b || Less(b, a)

  // Consequence: asymmetry follows from transitivity chaining a<b and b<a to a<a
  // against irreflexivity.
  lemma Asymmetric(a: Carrier, b: Carrier)
    requires Less(a, b)
    ensures !Less(b, a)
  {
    if Less(b, a) {
      Transitive(a, b, a);
      Irreflexive(a);
    }
  }

  // Consequence: exactly-one trichotomy. The disjunction is the at-least-one axiom;
  // the three mutual-exclusion clauses follow from transitivity and irreflexivity
  // (and indiscernibility of = for the mixed cases).
  lemma ExactlyOneTrichotomy(a: Carrier, b: Carrier)
    ensures Less(a, b) || a == b || Less(b, a)
    ensures !(Less(a, b) && Less(b, a))
    ensures !(Less(a, b) && a == b)
    ensures !(a == b && Less(b, a))
  {
    Trichotomy(a, b);
    if Less(a, b) && Less(b, a) {
      Transitive(a, b, a);
      Irreflexive(a);
    }
    if Less(a, b) && a == b {
      Irreflexive(a);
    }
    if a == b && Less(b, a) {
      Irreflexive(a);
    }
  }

  // Consequence: ≤-transitivity. Unfolding each hypothesis against the definition
  // x ≤ y ⟺ x < y ∨ x = y yields four cases; each discharges to m ≤ p via
  // <-transitivity or substitution of equalities.
  lemma LessOrEqualTransitive(a: Carrier, b: Carrier, c: Carrier)
    requires LessOrEqual(a, b)
    requires LessOrEqual(b, c)
    ensures LessOrEqual(a, c)
  {
    if Less(a, b) && Less(b, c) {
      Transitive(a, b, c);
    }
  }
}
