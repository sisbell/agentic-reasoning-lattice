// ASN-0034: NAT-cancel
// Addition on ℕ is cancellative: m + k == n + k implies m == n.
include "./NatCarrierSet.dfy"

module NatAdditionCancellation {
  import opened NatCarrierSet

  lemma {:axiom} NatAdditionCancellation(m: Carrier, n: Carrier, k: Carrier)
    requires m + k == n + k
    ensures m == n
}
