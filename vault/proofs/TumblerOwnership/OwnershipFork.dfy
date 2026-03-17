include "../TumblerAlgebra/TumblerAlgebra.dfy"
include "../TumblerAlgebra/TumblerHierarchy.dfy"
include "TumblerOwnership.dfy"

// O10 — DenialAsFork
module OwnershipFork {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import opened TumblerOwnership

  // O1a — account boundary constraint on principals
  ghost predicate AccountBoundary(principals: set<Principal>) {
    forall pi :: pi in principals ==>
      TumblerHierarchy.ZeroCount(pi.prefix.components) <= 1 &&
      TumblerHierarchy.ValidAddress(pi.prefix)
  }

  // Fork: add the alternative address to the allocation set
  function Fork(s: State, alt: Tumbler): State {
    State(s.principals, s.alloc + {alt})
  }

  // (b) Ownership depends on principals, not alloc.
  // Fork preserves all existing effective ownership.
  lemma OwnershipPreserved(pi: Principal, a: Tumbler, s: State, alt: Tumbler)
    requires IsEffectiveOwner(pi, a, s.principals)
    ensures IsEffectiveOwner(pi, a, Fork(s, alt).principals)
  { }

  // (a) When alt in dom(pi) and pi is most-specific, pi owns alt after fork.
  lemma ForkOwnership(pi: Principal, alt: Tumbler, s: State)
    requires pi in s.principals
    requires IsPrefix(pi.prefix, alt)
    requires forall pi' :: Covers(pi', alt, s.principals) && pi' != pi ==>
      |pi.prefix.components| > |pi'.prefix.components|
    ensures IsEffectiveOwner(pi, alt, Fork(s, alt).principals)
  { }

  // Existence: for any pi, there exists alt in dom(pi) where pi is effective owner.
  // ASN-0042 constructive argument:
  //   zeros=1: sub-delegates cannot reach document-level (would need >= 2 zeros)
  //   zeros=0: choose user-field exceeding all sub-delegate prefixes (T0a)
  // AXIOM: witness construction requires finite-set reasoning over principals
  // not yet mechanized.
  lemma {:axiom} ForkAddressExists(pi: Principal, s: State)
    requires pi in s.principals
    requires AccountBoundary(s.principals)
    ensures exists alt ::
      (IsPrefix(pi.prefix, alt) &&
       (forall pi' :: Covers(pi', alt, s.principals) && pi' != pi ==>
         |pi.prefix.components| > |pi'.prefix.components|))
}
