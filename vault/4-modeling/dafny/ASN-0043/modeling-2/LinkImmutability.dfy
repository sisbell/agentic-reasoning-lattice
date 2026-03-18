include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerAddition.dfy"
include "LinkStore.dfy"

// L12 — LinkImmutability (ASN-0043)
module LinkImmutability {
  import opened TumblerAlgebra
  import opened LinkStore

  // L12: Once created, a link's value never changes.
  // (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))
  ghost predicate LinkImmutability(before: Store, after: Store) {
    forall a :: a in before ==> a in after && after[a] == before[a]
  }

  // Reflexivity: identity transition preserves all links
  lemma LinkImmutabilityReflexive(s: Store)
    ensures LinkImmutability(s, s)
  { }

  // Transitivity: composition of immutability-preserving transitions
  lemma LinkImmutabilityTransitive(s1: Store, s2: Store, s3: Store)
    requires LinkImmutability(s1, s2)
    requires LinkImmutability(s2, s3)
    ensures LinkImmutability(s1, s3)
  { }
}
