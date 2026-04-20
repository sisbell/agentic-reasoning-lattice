module PrefixRelation {
  // Prefix — PrefixRelation
  // p ≼ q iff #p ≤ #q ∧ ∀i ∈ [1, #p]: qᵢ = pᵢ

  datatype Tumbler = Tumbler(components: seq<nat>)

  ghost predicate IsPrefix(p: Tumbler, q: Tumbler) {
    |p.components| <= |q.components| &&
    forall i :: 0 <= i < |p.components| ==> p.components[i] == q.components[i]
  }

  ghost predicate IsProperPrefix(p: Tumbler, q: Tumbler) {
    IsPrefix(p, q) && p != q
  }
}
