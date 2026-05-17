// ASN-0034: NAT-order
// The natural numbers carry a strict total order under <.
include "./NatCarrierSet.dfy"

module NatStrictTotalOrder {
  import opened NatCarrierSet

  lemma {:axiom} Irreflexive(a: Carrier)
    ensures !(a < a)

  lemma {:axiom} Asymmetric(a: Carrier, b: Carrier)
    requires a < b
    ensures !(b < a)

  lemma {:axiom} Transitive(a: Carrier, b: Carrier, c: Carrier)
    requires a < b
    requires b < c
    ensures a < c

  lemma {:axiom} Trichotomy(a: Carrier, b: Carrier)
    ensures a < b || a == b || b < a

  lemma {:axiom} NatStrictTotalOrder()
    ensures forall a: Carrier :: !(a < a)
    ensures forall a: Carrier, b: Carrier :: a < b ==> !(b < a)
    ensures forall a: Carrier, b: Carrier, c: Carrier ::
              a < b && b < c ==> a < c
    ensures forall a: Carrier, b: Carrier ::
              a < b || a == b || b < a
}
