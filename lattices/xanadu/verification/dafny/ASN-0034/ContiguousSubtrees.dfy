include "./LexicographicOrder.dfy"
include "./CanonicalRepresentation.dfy"

module ContiguousSubtrees {
  // T5 — ContiguousSubtrees
  // p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b

  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import CanonicalRepresentation

  ghost predicate IsPrefix(p: Tumbler, t: Tumbler) {
    |p.components| <= |t.components| &&
    forall i :: 0 <= i < |p.components| ==> p.components[i] == t.components[i]
  }

  lemma ContiguousSubtrees(p: Tumbler, a: Tumbler, b: Tumbler, c: Tumbler)
    requires |p.components| >= 1
    requires IsPrefix(p, a)
    requires IsPrefix(p, c)
    requires LessThan(a, b) || a == b
    requires LessThan(b, c) || b == c
    ensures IsPrefix(p, b)
  {
  }
}
