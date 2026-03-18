include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// (Prefix ordering extension) — ASN-0034
module PrefixOrderingExtension {
  import opened TumblerAlgebra

  lemma PrefixOrderingExtension(p1: Tumbler, p2: Tumbler, a: Tumbler, b: Tumbler)
    requires LessThan(p1, p2)
    requires !IsPrefix(p1, p2)
    requires !IsPrefix(p2, p1)
    requires IsPrefix(p1, a)
    requires IsPrefix(p2, b)
    ensures LessThan(a, b)
  {
    var k :| LessThanAt(p1, p2, k);
    LessThanIntro(a, b, k);
  }
}
