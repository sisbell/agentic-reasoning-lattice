include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module AdditionAssociative {
  import opened TumblerAlgebra

  // (Associativity) — ASN-0034
  // Addition is associative where both compositions are defined.
  lemma AdditionAssociative(a: Tumbler, b: Tumbler, c: Tumbler)
    requires PositiveTumbler(b)
    requires PositiveTumbler(c)
    requires ActionPoint(b) < |a.components|
    requires ActionPoint(c) < |b.components|
    ensures PositiveTumbler(TumblerAdd(b, c))
    ensures ActionPoint(TumblerAdd(b, c)) < |a.components|
    ensures TumblerAdd(TumblerAdd(a, b), c) == TumblerAdd(a, TumblerAdd(b, c))
  {
    var kb := ActionPoint(b);
    var kc := ActionPoint(c);
    var bc := TumblerAdd(b, c);

    // Establish PositiveTumbler(bc): component at kc is nonzero
    assert bc.components[kc] != 0;

    // Establish ActionPoint(bc) <= kb < |a.components|
    if kb <= kc {
      assert bc.components[kb] != 0;
    }
  }
}
