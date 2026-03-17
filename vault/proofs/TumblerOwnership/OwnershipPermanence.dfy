include "../TumblerAlgebra/TumblerAlgebra.dfy"
include "../TumblerAlgebra/TumblerHierarchy.dfy"
include "TumblerOwnership.dfy"

// OwnershipPermanence — O3, O8, O12, O13, AccountPermanence
// O12 (PrincipalPersistence) and T8 (AddressPermanence) defined in TumblerOwnership
module OwnershipPermanence {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import opened TumblerOwnership

  // O13 — PrefixImmutable
  // In the abstract ASN model, O13 states:
  //   (A pi in Pi_S ^ Pi_S' : pfx_{S'}(pi) = pfx_S(pi))
  // With Principal modeled as datatype Principal(prefix: Tumbler), prefix
  // immutability is structural — the same principal value in both states
  // carries the same prefix by construction. No separate predicate needed.

  // O3 — OwnershipRefinement
  // If the effective owner of an allocated address changes across a transition,
  // a new principal was introduced with a longer covering prefix.
  // Derived from O12 (PrincipalPersistence), O13 (PrefixImmutable), T8 (AddressPermanence)
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

  // O8 — IrrevocableDelegation
  // Once pi delegates to pi', pi can never be the effective owner of addresses
  // in dom(pi'). The delegate pi' persists (O12) with unchanged prefix (O13,
  // structural) and has a strictly longer prefix than pi, so pi cannot be the
  // most-specific covering principal for any address that pi' also covers.
  // Derived from O3 (OwnershipRefinement), O12 (PrincipalPersistence), O13 (PrefixImmutable).
  lemma IrrevocableDelegation(
    s: State, s': State,
    pi: Principal, pi': Principal, a: Tumbler
  )
    requires pi in s.principals && pi' in s.principals
    // Delegation: pfx(pi) < pfx(pi')
    requires StrictPrefix(pi.prefix, pi'.prefix)
    // a in dom(pi') ^ S'.alloc
    requires a in s'.alloc
    requires IsPrefix(pi'.prefix, a)
    // O12
    requires PrincipalPersistence(s, s')
    ensures !IsEffectiveOwner(pi, a, s'.principals)
  { }

  // Base case (O14): two prefixes of the same address must nest
  // (contrapositive: non-nesting prefixes cannot both cover the same address)
  lemma BootstrapDomainsDisjoint(
    pi1: Principal, pi2: Principal, a: Tumbler
  )
    requires IsPrefix(pi1.prefix, a)
    requires IsPrefix(pi2.prefix, a)
    ensures IsPrefix(pi1.prefix, pi2.prefix) || IsPrefix(pi2.prefix, pi1.prefix)
  { }

  // If pi covers a but isn't the effective owner, omega(a) strictly extends pi's prefix
  lemma EffectiveOwnerExtends(
    pi: Principal, omega: Principal, a: Tumbler,
    principals: set<Principal>
  )
    requires Covers(pi, a, principals)
    requires IsEffectiveOwner(omega, a, principals)
    requires omega != pi
    ensures StrictPrefix(pi.prefix, omega.prefix)
    ensures IsPrefix(omega.prefix, a)
  { }

  // Inductive step: when delegate is introduced by delegation and
  // pfx(pi) <= pfx(delegate), the delegator is within dom(pi)
  lemma DelegatorWithinDomain(
    s: State, pi: Principal, delegator: Principal, delegate: Principal
  )
    requires pi in s.principals
    requires DelegationPrecondition(s, delegator, delegate)
    requires IsPrefix(pi.prefix, delegate.prefix)
    ensures IsPrefix(pi.prefix, delegator.prefix)
  { }

  // Corollary — AccountPermanence (single-transition form)
  // If omega changes at a in dom(pi), the newly introduced principal and its
  // delegator are both within dom(pi).
  lemma AccountPermanence(
    s: State, s': State,
    pi: Principal, a: Tumbler,
    oldOwner: Principal, newOwner: Principal,
    delegator: Principal
  )
    requires pi in s.principals && IsPrefix(pi.prefix, a)
    requires IsEffectiveOwner(oldOwner, a, s.principals)
    requires IsEffectiveOwner(newOwner, a, s'.principals)
    requires newOwner != oldOwner
    requires PrincipalPersistence(s, s')
    requires newOwner in s'.principals && newOwner !in s.principals
    requires IsPrefix(newOwner.prefix, a)
    requires |newOwner.prefix.components| > |oldOwner.prefix.components|
    requires DelegationPrecondition(s, delegator, newOwner)
    ensures StrictPrefix(pi.prefix, newOwner.prefix)
    ensures IsPrefix(pi.prefix, delegator.prefix)
  { }
}
