// ASN-0034: NAT-cancel
// Addition on ℕ is cancellative: left and right cancellation as axioms,
// summand absorption (both forms) as proved consequences.
include "./NatCarrierSet.dfy"
include "./NatArithmeticClosureAndIdentity.dfy"

module NatAdditionCancellation {
  import opened NatCarrierSet
  import opened NatArithmeticClosureAndIdentity

  lemma {:axiom} NatAdditionLeftCancellation(m: Carrier, n: Carrier, p: Carrier)
    requires m + n == m + p
    ensures n == p

  lemma {:axiom} NatAdditionRightCancellation(n: Carrier, p: Carrier, m: Carrier)
    requires n + m == p + m
    ensures n == p

  lemma NatAdditionSummandAbsorption(m: Carrier, n: Carrier)
    requires m + n == m
    ensures n == 0
  {
    RightAdditiveIdentity(m);
    NatAdditionLeftCancellation(m, n, 0);
  }

  lemma NatAdditionSummandAbsorptionMirror(n: Carrier, m: Carrier)
    requires n + m == m
    ensures n == 0
  {
    LeftAdditiveIdentity(m);
    NatAdditionRightCancellation(n, 0, m);
  }
}
