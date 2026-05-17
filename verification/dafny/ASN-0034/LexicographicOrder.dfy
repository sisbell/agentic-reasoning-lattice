// ASN-0034: T1 — LexicographicOrder
// a < b iff ∃ k ∈ ℕ with 1 ≤ k and (∀ i : 1 ≤ i < k : aᵢ = bᵢ) and either
//   (i) k ≤ #a ∧ k ≤ #b ∧ aₖ < bₖ, or
//   (ii) k = #a + 1 ≤ #b.
include "./CarrierSetDefinition.dfy"
include "./NatStrictTotalOrder.dfy"

module LexicographicOrder {
  import opened CarrierSetDefinition
  import opened NatStrictTotalOrder
  import opened NatCarrierSet

  ghost predicate LexicographicOrder(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
  {
    exists k: nat ::
      && 1 <= k
      && (forall i :: 1 <= i < k ==>
            i <= Length(a) && i <= Length(b) &&
            Component(a, i) == Component(b, i))
      && ((k <= Length(a) && k <= Length(b) && Less(Component(a, k), Component(b, k)))
          || (k == Length(a) + 1 && k <= Length(b)))
  }
}
