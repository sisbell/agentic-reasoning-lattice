// ASN-0034: NAT-card
// |S| is the cardinality operator on finite subsets of ℕ: the unique
// k ∈ ℕ such that S is enumerated by a strictly increasing function
// f : {1, …, k} → ℕ. For S ⊆ {1, …, n}, |S| ≤ n.
include "./NatCarrierSet.dfy"

module NatFiniteSetCardinality {
  import opened NatCarrierSet

  lemma {:axiom} NatFiniteSetCardinality(S: set<Carrier>, n: nat)
    requires forall x :: x in S ==> 1 <= x <= n
    ensures |S| <= n
}
