// ASN-0034: T6 — DecidableContainment
// Containment under an address is decidable from tumbler representations
// alone: each of the four cases (a)–(d) admits a terminating boolean
// decision procedure via field extraction (T4b), zero-count comparison
// (NAT-card/NAT-closure), and sequence equality (T3).
include "./CarrierSetDefinition.dfy"
include "./HierarchicalParsing.dfy"
include "./UniqueParse.dfy"

module DecidableContainment {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened HierarchicalParsing
  import opened UniqueParse

  // (a) Same node field.
  function DecideSameNode(a: Tumbler, b: Tumbler): bool
    requires InT(a) && HierarchicalParsing.HierarchicalParsing(a)
    requires InT(b) && HierarchicalParsing.HierarchicalParsing(b)
  {
    N(a) == N(b)
  }

  // (b) Matching user and node fields under shared presence.
  // Symmetric or asymmetric absence returns false via short-circuit on Zeros.
  function DecideMatchingUserNode(a: Tumbler, b: Tumbler): bool
    requires InT(a) && HierarchicalParsing.HierarchicalParsing(a)
    requires InT(b) && HierarchicalParsing.HierarchicalParsing(b)
  {
    Zeros(a) >= 1 && Zeros(b) >= 1 && N(a) == N(b) && U(a) == U(b)
  }

  // (c) Matching node, user, and document fields under shared presence.
  function DecideMatchingDocUserNode(a: Tumbler, b: Tumbler): bool
    requires InT(a) && HierarchicalParsing.HierarchicalParsing(a)
    requires InT(b) && HierarchicalParsing.HierarchicalParsing(b)
  {
    Zeros(a) >= 2 && Zeros(b) >= 2 &&
    N(a) == N(b) && U(a) == U(b) && D(a) == D(b)
  }

  // (d) Document-field prefix within shared document family.
  function DecideContainedUnder(a: Tumbler, b: Tumbler): bool
    requires InT(a) && HierarchicalParsing.HierarchicalParsing(a)
    requires InT(b) && HierarchicalParsing.HierarchicalParsing(b)
  {
    Zeros(a) >= 2 && Zeros(b) >= 2 &&
    N(a) == N(b) && U(a) == U(b) &&
    Length(D(b)) <= Length(D(a)) &&
    forall k :: 1 <= k <= Length(D(b)) ==>
      Component(D(a), k) == Component(D(b), k)
  }

  // T6: corollary of T4b (projections N, U, D) + T3 (sequence equality)
  // + NAT-card (zero-count) + decidable equality on ℕ. Each containment
  // relation is computed by a terminating boolean function over a and b
  // alone, with postconditions matching the four cases of the contract.
  lemma DecidableContainment(a: Tumbler, b: Tumbler)
    requires InT(a) && HierarchicalParsing.HierarchicalParsing(a)
    requires InT(b) && HierarchicalParsing.HierarchicalParsing(b)
    ensures DecideSameNode(a, b) <==> N(a) == N(b)
    ensures DecideMatchingUserNode(a, b) <==>
      (Zeros(a) >= 1 && Zeros(b) >= 1 && N(a) == N(b) && U(a) == U(b))
    ensures DecideMatchingDocUserNode(a, b) <==>
      (Zeros(a) >= 2 && Zeros(b) >= 2 &&
       N(a) == N(b) && U(a) == U(b) && D(a) == D(b))
    ensures DecideContainedUnder(a, b) <==>
      (Zeros(a) >= 2 && Zeros(b) >= 2 &&
       N(a) == N(b) && U(a) == U(b) &&
       Length(D(b)) <= Length(D(a)) &&
       forall k :: 1 <= k <= Length(D(b)) ==>
         Component(D(a), k) == Component(D(b), k))
  { }
}
