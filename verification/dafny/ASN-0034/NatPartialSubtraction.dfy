// ASN-0034: NAT-sub
// Partial binary subtraction on ℕ. When m ≥ n, m − n is the unique
// natural number characterised by (m − n) + n = m.
include "./NatCarrierSet.dfy"
include "./NatStrictTotalOrder.dfy"

module NatPartialSubtraction {
  import opened NatCarrierSet
  import opened NatStrictTotalOrder

  function Sub(m: Carrier, n: Carrier): Carrier
    requires GreaterOrEqual(m, n)
  {
    m - n
  }

  lemma {:axiom} ConditionalClosure(m: Carrier, n: Carrier)
    requires GreaterOrEqual(m, n)
    ensures InCarrier(Sub(m, n))

  lemma {:axiom} RightInverse(m: Carrier, n: Carrier)
    requires GreaterOrEqual(m, n)
    ensures Sub(m, n) + n == m

  lemma {:axiom} LeftInverse(m: Carrier, n: Carrier)
    requires GreaterOrEqual(m, n)
    ensures n + Sub(m, n) == m

  lemma {:axiom} RightTelescoping(m: Carrier, n: Carrier)
    requires GreaterOrEqual(m + n, n)
    ensures Sub(m + n, n) == m

  lemma {:axiom} LeftTelescoping(m: Carrier, n: Carrier)
    requires GreaterOrEqual(n + m, n)
    ensures Sub(n + m, n) == m
}
