include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module PrefixOrderingExtension {

  import opened TumblerAlgebra

  // Prefix ordering extension — PrefixOrderingExtension
  // If p1 < p2 and neither is a prefix of the other, then every
  // extension of p1 is less than every extension of p2.
  lemma PrefixOrderingExtension(p1: Tumbler, p2: Tumbler, a: Tumbler, b: Tumbler)
    requires LessThan(p1, p2)
    requires !IsPrefix(p1, p2)
    requires !IsPrefix(p2, p1)
    requires IsPrefix(p1, a)
    requires IsPrefix(p2, b)
    ensures LessThan(a, b)
  { }
}
