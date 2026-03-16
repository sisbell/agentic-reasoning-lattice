include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "PrefixDetermination.dfy"

// O3 — OwnershipRefinement
// (A a ∈ Σ.alloc, Σ, Σ' : Σ → Σ' ∧ ω_{Σ'}(a) ≠ ω_Σ(a) ⟹
//   (E π' ∈ Π_{Σ'} ∖ Π_Σ : pfx(π') ≼ a ∧ #pfx(π') > #pfx(ω_Σ(a))))
// Derived from O12 (PrincipalPersistence), O13 (PrefixImmutable), T8 (AddressPermanence)
module OwnershipRefinement {
  import opened TumblerAlgebra
  import PrefixDetermination

  type Principal = PrefixDetermination.Principal

  datatype State = State(principals: set<Principal>, alloc: set<Tumbler>)

  ghost predicate Covers(pi: Principal, a: Tumbler, principals: set<Principal>) {
    pi in principals && IsPrefix(pi.prefix, a)
  }

  ghost predicate IsEffectiveOwner(pi: Principal, a: Tumbler, principals: set<Principal>) {
    Covers(pi, a, principals) &&
    forall pi' :: Covers(pi', a, principals) && pi' != pi ==>
      |pi.prefix.components| > |pi'.prefix.components|
  }

  // O12 — PrincipalPersistence
  ghost predicate PrincipalPersistence(s: State, s': State) {
    s.principals <= s'.principals
  }

  // O13 — PrefixImmutable
  // DIVERGENCE: Prefix immutability is structural in this model. Since Principal
  // embeds its prefix as a datatype field, the same principal value in both states
  // carries the same prefix by construction. No separate O13 predicate is needed.

  // T8 — AddressPermanence
  ghost predicate AddressPermanence(s: State, s': State) {
    s.alloc <= s'.alloc
  }

  // O3 — OwnershipRefinement
  // If the effective owner of an allocated address changes across a transition,
  // a new principal was introduced with a longer covering prefix.
  lemma OwnershipRefinement(
    s: State, s': State, a: Tumbler,
    oldOwner: Principal, newOwner: Principal
  )
    requires a in s.alloc
    requires PrincipalPersistence(s, s')
    requires AddressPermanence(s, s')
    requires IsEffectiveOwner(oldOwner, a, s.principals)
    requires IsEffectiveOwner(newOwner, a, s'.principals)
    requires newOwner != oldOwner
    ensures newOwner in s'.principals && newOwner !in s.principals
    ensures IsPrefix(newOwner.prefix, a)
    ensures |newOwner.prefix.components| > |oldOwner.prefix.components|
  {
  }
}
