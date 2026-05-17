// ASN-0034: NAT-order
// The natural numbers carry a strict total order under <.
include "./NatCarrierSet.dfy"

module NatStrictTotalOrder {
  import opened NatCarrierSet

  predicate Less(a: Carrier, b: Carrier) { a < b }

  lemma {:axiom} Irreflexive(a: Carrier)
    ensures !Less(a, a)

  lemma {:axiom} Asymmetric(a: Carrier, b: Carrier)
    requires Less(a, b)
    ensures !Less(b, a)

  lemma {:axiom} Transitive(a: Carrier, b: Carrier, c: Carrier)
    requires Less(a, b)
    requires Less(b, c)
    ensures Less(a, c)

  lemma {:axiom} Trichotomy(a: Carrier, b: Carrier)
    ensures Less(a, b) || a == b || Less(b, a)

  lemma {:axiom} NatStrictTotalOrder()
    ensures forall a: Carrier :: !Less(a, a)
    ensures forall a: Carrier, b: Carrier :: Less(a, b) ==> !Less(b, a)
    ensures forall a: Carrier, b: Carrier, c: Carrier ::
              Less(a, b) && Less(b, c) ==> Less(a, c)
    ensures forall a: Carrier, b: Carrier ::
              Less(a, b) || a == b || Less(b, a)
}
