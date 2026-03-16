include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "PrefixDetermination.dfy"

// O8 — IrrevocableDelegation
// (A π, π', a, Σ, Σ' : delegated_Σ(π, π') ∧ a ∈ dom(π') ∩ Σ'.alloc ∧ Σ →⁺ Σ' : ω_{Σ'}(a) ≠ π)
// Derived from O3 (OwnershipRefinement), O12 (PrincipalPersistence), O13 (PrefixImmutable).
module IrrevocableDelegation {
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

  ghost predicate StrictPrefix(p: Tumbler, a: Tumbler) {
    IsPrefix(p, a) && |p.components| < |a.components|
  }

  // O12 — PrincipalPersistence
  ghost predicate PrincipalPersistence(s: State, s': State) {
    s.principals <= s'.principals
  }

  // O13 — PrefixImmutable: structural in this model (prefix embedded in Principal datatype)

  // O8 — IrrevocableDelegation
  // Once π delegates to π', π can never be the effective owner of addresses
  // in dom(π'). The delegate π' persists (O12) with unchanged prefix (O13,
  // structural) and has a strictly longer prefix than π, so π cannot be the
  // most-specific covering principal for any address that π' also covers.
  lemma IrrevocableDelegation(
    s: State, s': State,
    pi: Principal, pi': Principal, a: Tumbler
  )
    requires pi in s.principals && pi' in s.principals
    // Delegation: pfx(π) ≺ pfx(π')
    requires StrictPrefix(pi.prefix, pi'.prefix)
    // a ∈ dom(π') ∩ Σ'.alloc
    requires a in s'.alloc
    requires IsPrefix(pi'.prefix, a)
    // O12
    requires PrincipalPersistence(s, s')
    ensures !IsEffectiveOwner(pi, a, s'.principals)
  { }
}
