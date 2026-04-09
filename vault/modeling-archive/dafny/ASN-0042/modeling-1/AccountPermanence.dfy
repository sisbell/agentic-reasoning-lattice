include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "PrefixDetermination.dfy"

// Corollary — AccountPermanence
// derived from O5, O14, O15
module AccountPermanence {
  import opened TumblerAlgebra
  import TumblerHierarchy
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

  // Delegation validity — conditions (i), (ii), (iv), (v), (vi) from Delegated definition
  ghost predicate DelegationValid(
    s: State, delegator: Principal, delegate: Principal
  ) {
    delegator in s.principals &&
    delegate !in s.principals &&
    StrictPrefix(delegator.prefix, delegate.prefix) &&
    (forall pi :: pi in s.principals && IsPrefix(pi.prefix, delegate.prefix)
      ==> |pi.prefix.components| <= |delegator.prefix.components|) &&
    TumblerHierarchy.ZeroCount(delegate.prefix.components) <= 1 &&
    TumblerHierarchy.ValidAddress(delegate.prefix) &&
    (forall pi :: pi in s.principals ==> !StrictPrefix(delegate.prefix, pi.prefix))
  }

  // Two covering prefixes of the same address nest by length
  lemma CoveringPrefixesNest(p1: Tumbler, p2: Tumbler, a: Tumbler)
    requires IsPrefix(p1, a)
    requires IsPrefix(p2, a)
    requires |p1.components| <= |p2.components|
    ensures IsPrefix(p1, p2)
  { }

  // Base case (O14): non-nesting prefixes cannot both cover the same address
  lemma BootstrapDomainsDisjoint(
    pi1: Principal, pi2: Principal, a: Tumbler
  )
    requires !IsPrefix(pi1.prefix, pi2.prefix) && !IsPrefix(pi2.prefix, pi1.prefix)
    requires IsPrefix(pi1.prefix, a)
    requires IsPrefix(pi2.prefix, a)
    ensures false
  { }

  // If π covers a but isn't the effective owner, ω(a) strictly extends π's prefix
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
  // pfx(π) ≼ pfx(delegate), the delegator is within dom(π)
  lemma DelegatorWithinDomain(
    s: State, pi: Principal, delegator: Principal, delegate: Principal
  )
    requires pi in s.principals
    requires DelegationValid(s, delegator, delegate)
    requires IsPrefix(pi.prefix, delegate.prefix)
    ensures IsPrefix(pi.prefix, delegator.prefix)
  { }

  // DIVERGENCE: The ASN states AccountPermanence as a trace-level inductive
  // property: in any reachable state, every principal within dom(π) was
  // introduced through a delegation chain rooted at π. The full induction
  // over state traces is not mechanized. What IS verified:
  // (1) BootstrapDomainsDisjoint: base case — O14 non-nesting gives disjoint domains
  // (2) EffectiveOwnerExtends: structural consequence pfx(π) ≺ pfx(ω(a))
  // (3) DelegatorWithinDomain: inductive kernel — each delegation within dom(π)
  //     is performed by a delegator also within dom(π)
  // (4) AccountPermanence: single-transition composition of (2) and (3)
  // Together these establish that the delegation chain cannot escape dom(π).

  // Corollary — AccountPermanence (single-transition form)
  // If ω changes at a ∈ dom(π), the newly introduced principal and its
  // delegator are both within dom(π).
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
    requires DelegationValid(s, delegator, newOwner)
    ensures StrictPrefix(pi.prefix, newOwner.prefix)
    ensures IsPrefix(pi.prefix, delegator.prefix)
  { }
}
