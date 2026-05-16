include "./LexicographicOrder.dfy"

module PrefixOrderingExtension {
  // PrefixOrderingExtension — NonNestingSubtreeOrdering

  import opened CarrierSetDefinition
  import opened LexicographicOrder

  ghost predicate IsPrefix(p: Tumbler, q: Tumbler) {
    |p.components| <= |q.components| &&
    forall i :: 0 <= i < |p.components| ==> p.components[i] == q.components[i]
  }

  // For p₁ < p₂ with neither a prefix of the other,
  // every extension of p₁ precedes every extension of p₂.
  lemma PrefixOrderingExtension(p1: Tumbler, p2: Tumbler, a: Tumbler, b: Tumbler)
    requires LessThan(p1, p2)
    requires !IsPrefix(p1, p2) && !IsPrefix(p2, p1)
    requires IsPrefix(p1, a) && IsPrefix(p2, b)
    ensures LessThan(a, b)
  { }
}
