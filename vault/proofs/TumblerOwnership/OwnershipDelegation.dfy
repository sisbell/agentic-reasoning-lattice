include "../TumblerAlgebra/TumblerAlgebra.dfy"
include "../TumblerAlgebra/TumblerHierarchy.dfy"
include "TumblerOwnership.dfy"

// OwnershipDelegation — O4, O5, O7, O14, O15, O16, O17
module OwnershipDelegation {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import opened TumblerOwnership

  // --- O7 — OwnershipDelegation ---

  function Delegate(s: State, delegator: Principal, delegate: Principal): State
    requires DelegationPrecondition(s, delegator, delegate)
  {
    State(s.principals + {delegate}, s.alloc)
  }

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

  // --- O4 — DomainCoverage ---
  // (A a in Sigma.alloc : (E pi in Pi : pfx(pi) <= a))
  // Derived from O5 (SubdivisionAuthority), O14 (BootstrapPrincipal), O16 (AllocationClosure)

  ghost predicate DomainCoverage(s: State) {
    forall a :: a in s.alloc ==> exists pi :: Covers(pi, a, s.principals)
  }

  // O5 + O16 — every new allocation is covered by some principal
  ghost predicate NewAllocationsCovered(s: State, s': State) {
    forall a :: a in s'.alloc && a !in s.alloc ==>
      exists pi :: Covers(pi, a, s'.principals)
  }

  // Inductive step: DomainCoverage is preserved across transitions.
  // Base case: O14 (BootstrapPrincipal) establishes DomainCoverage(S0).
  // Inductive step: existing allocations stay covered via O12 (persistence);
  // new allocations are covered by O5/O16.
  lemma DomainCoveragePreserved(s: State, s': State)
    requires DomainCoverage(s)
    requires PrincipalPersistence(s, s')
    requires NewAllocationsCovered(s, s')
    ensures DomainCoverage(s')
  {
    forall a | a in s'.alloc
      ensures exists pi :: Covers(pi, a, s'.principals)
    {
      if a in s.alloc {
        var pi :| Covers(pi, a, s.principals);
        assert Covers(pi, a, s'.principals);
      }
    }
  }

  // --- O5 — SubdivisionAuthority ---
  // DIVERGENCE: allocated_by is modeled as an explicit allocator map
  // (Tumbler -> Principal). Principal type rewritten from abstract
  // Principal(id: nat) to embedded Principal(prefix: Tumbler), removing
  // the pfx map indirection.

  ghost predicate SubdivisionAuthority(
    s: State,
    s': State,
    allocator: map<Tumbler, Principal>
  ) {
    forall a :: a in s'.alloc && a !in s.alloc && a in allocator ==>
      var pi := allocator[a];
      pi in s.principals &&
      IsPrefix(pi.prefix, a) &&
      (forall pi' :: pi' in s.principals && IsPrefix(pi'.prefix, a)
        ==> |pi'.prefix.components| <= |pi.prefix.components|)
  }

  // --- O14 — BootstrapPrincipal ---
  // Pi0 != {} and (A a in S0.alloc : (E pi in Pi0 : pfx(pi) <= a))
  // (A pi in Pi0 : zeros(pfx(pi)) <= 1)
  // (A p1, p2 in Pi0 : pfx(p1) = pfx(p2) ==> p1 = p2)
  // (A pi in Pi0 : T4(pfx(pi)))
  // (A p1, p2 in Pi0 : p1 != p2 ==> pfx(p1) not<= pfx(p2) and pfx(p2) not<= pfx(p1))

  ghost predicate BootstrapPrincipal(s: State) {
    // Pi0 != {}
    s.principals != {} &&

    // (A a in S0.alloc : (E pi in Pi0 : pfx(pi) <= a))
    (forall a :: a in s.alloc ==>
      exists pi :: pi in s.principals && IsPrefix(pi.prefix, a)) &&

    // (A pi in Pi0 : zeros(pfx(pi)) <= 1)
    (forall pi :: pi in s.principals ==>
      TumblerHierarchy.ZeroCount(pi.prefix.components) <= 1) &&

    // (A p1, p2 in Pi0 : pfx(p1) = pfx(p2) ==> p1 = p2)
    (forall p1, p2 ::
      (p1 in s.principals && p2 in s.principals && p1.prefix == p2.prefix)
        ==> p1 == p2) &&

    // (A pi in Pi0 : T4(pfx(pi)))
    (forall pi :: pi in s.principals ==>
      TumblerHierarchy.ValidAddress(pi.prefix)) &&

    // (A p1, p2 in Pi0 : p1 != p2 ==> pfx(p1) not<= pfx(p2) and pfx(p2) not<= pfx(p1))
    (forall p1, p2 ::
      (p1 in s.principals && p2 in s.principals && p1 != p2)
        ==> !IsPrefix(p1.prefix, p2.prefix) && !IsPrefix(p2.prefix, p1.prefix))
  }

  // --- O15 — PrincipalClosure ---
  // (A Sigma, Sigma' : Sigma -> Sigma' ==> |Pi_{Sigma'} \ Pi_Sigma| <= 1)
  // (A pi' in Pi_{Sigma'} \ Pi_Sigma : (E pi in Pi_Sigma : delegated_Sigma(pi, pi')))

  ghost predicate PrincipalClosure(s: State, s': State) {
    |s'.principals - s.principals| <= 1 &&
    (forall pi' :: pi' in s'.principals - s.principals ==>
      exists pi :: pi in s.principals &&
        DelegationPrecondition(s, pi, pi'))
  }

  // --- O16 — AllocationClosure ---
  // (A S, S', a : S -> S' and a in S'.alloc \ S.alloc
  //   ==> (E pi in Pi_S : allocated_by_{S'}(pi, a)))
  // DIVERGENCE: allocated_by is modeled as an allocator map (Tumbler -> Principal)
  // consistent with O5. Principal type rewritten from abstract Principal(id: nat)
  // to embedded Principal(prefix: Tumbler).

  ghost predicate AllocationClosure(
    s: State,
    s': State,
    allocator: map<Tumbler, Principal>
  ) {
    forall a :: a in s'.alloc && a !in s.alloc ==>
      a in allocator && allocator[a] in s.principals
  }

  // --- O17 — AllocatedAddressValid ---
  // (A S, a : a in S.alloc ==> T4(a))

  ghost predicate AllocatedAddressValid(s: State) {
    forall a :: a in s.alloc ==> TumblerHierarchy.ValidAddress(a)
  }
}
