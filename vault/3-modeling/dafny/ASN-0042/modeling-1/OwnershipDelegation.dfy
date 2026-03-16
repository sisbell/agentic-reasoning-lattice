include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "PrefixDetermination.dfy"

// O7 — OwnershipDelegation
module OwnershipDelegation {
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

  // Delegation preconditions from ASN-0042 Delegated definition
  ghost predicate DelegationPrecondition(
    s: State, delegator: Principal, delegate: Principal
  ) {
    delegator in s.principals &&
    delegate !in s.principals &&
    // (i) pfx(delegator) ≺ pfx(delegate)
    StrictPrefix(delegator.prefix, delegate.prefix) &&
    // (ii) delegator is most-specific covering principal for pfx(delegate)
    (forall pi :: pi in s.principals && IsPrefix(pi.prefix, delegate.prefix)
      ==> |pi.prefix.components| <= |delegator.prefix.components|) &&
    // (iv) zeros(pfx(delegate)) <= 1
    TumblerHierarchy.ZeroCount(delegate.prefix.components) <= 1 &&
    // (v) T4(pfx(delegate))
    TumblerHierarchy.ValidAddress(delegate.prefix) &&
    // (vi) no existing principal has delegate's prefix as strict prefix of theirs
    (forall pi :: pi in s.principals ==>
      !StrictPrefix(delegate.prefix, pi.prefix))
  }

  function Delegate(s: State, delegator: Principal, delegate: Principal): State
    requires DelegationPrecondition(s, delegator, delegate)
  {
    State(s.principals + {delegate}, s.alloc)
  }

  // Two prefixes of the same address are nested by length
  lemma CoveringPrefixesNest(p1: Tumbler, p2: Tumbler, a: Tumbler)
    requires IsPrefix(p1, a)
    requires IsPrefix(p2, a)
    requires |p1.components| <= |p2.components|
    ensures IsPrefix(p1, p2)
  { }

  // Postcondition (a): omega(a) = delegate for all a in dom(delegate) ^ alloc
  lemma DelegationEffectiveOwnership(
    s: State, delegator: Principal, delegate: Principal, a: Tumbler
  )
    requires DelegationPrecondition(s, delegator, delegate)
    requires a in s.alloc
    requires IsPrefix(delegate.prefix, a)
    ensures IsEffectiveOwner(delegate, a, Delegate(s, delegator, delegate).principals)
  { }

  // Postcondition (b): delegate can allocate within dom(delegate) — O5 applies
  lemma DelegationEnablesAllocation(
    s: State, delegator: Principal, delegate: Principal
  )
    requires DelegationPrecondition(s, delegator, delegate)
    ensures delegate in Delegate(s, delegator, delegate).principals
    ensures TumblerHierarchy.ValidAddress(delegate.prefix)
  { }

  // Postcondition (c): delegate can delegate sub-prefixes — recursive O7
  lemma DelegationEnablesFurtherDelegation(
    s: State, delegator: Principal, delegate: Principal
  )
    requires DelegationPrecondition(s, delegator, delegate)
    ensures delegate in Delegate(s, delegator, delegate).principals
    ensures TumblerHierarchy.ValidAddress(delegate.prefix)
    ensures TumblerHierarchy.ZeroCount(delegate.prefix.components) <= 1
  { }
}
