// ASN-0034: PrefixOrderingExtension
// If p1 < p2 (T1) and neither is a prefix of the other, then every tumbler
// extending p1 precedes every tumbler extending p2 under T1. The divergence
// position witnessing p1 < p2 carries through to all extensions.
include "./CarrierSetDefinition.dfy"
include "./PrefixRelation.dfy"
include "./LexicographicOrder.dfy"

module PrefixOrderingExtension {
  import opened CarrierSetDefinition
  import opened PrefixRelation
  import opened LexicographicOrder
  import opened NatStrictTotalOrder
  import opened NatCarrierSet

  lemma PrefixOrderingExtension(p1: Tumbler, p2: Tumbler, a: Tumbler, b: Tumbler)
    requires InT(p1) && InT(p2) && InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(p1, p2)
    requires !PrefixOf(p1, p2) && !PrefixOf(p2, p1)
    requires PrefixOf(p1, a) && PrefixOf(p2, b)
    ensures LexicographicOrder.LexicographicOrder(a, b)
  {
    var k :| 1 <= k
          && (forall i :: 1 <= i < k ==>
                i <= Length(p1) && i <= Length(p2) &&
                Component(p1, i) == Component(p2, i))
          && ((k <= Length(p1) && k <= Length(p2) &&
               Less(Component(p1, k), Component(p2, k)))
              || (k == Length(p1) + 1 && k <= Length(p2)));

    // Case (ii): k = #p1+1 ≤ #p2 would force p1 ≼ p2, contradicting non-nesting.
    if k == Length(p1) + 1 && k <= Length(p2) {
      assert PrefixOf(p1, p2);
      assert false;
    }

    // Case (i): k ≤ min(#p1,#p2) and p1_k < p2_k. Same k witnesses a < b.
    assert k <= Length(a) && k <= Length(b);
    assert Component(a, k) == Component(p1, k);
    assert Component(b, k) == Component(p2, k);
  }
}
