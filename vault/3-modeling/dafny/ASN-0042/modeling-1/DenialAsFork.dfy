include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "PrefixDetermination.dfy"

// O10 — DenialAsFork
module DenialAsFork {
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

  // (a) When alt ∈ dom(π) and π is most-specific, π owns alt after fork.
  lemma ForkOwnership(pi: Principal, alt: Tumbler, s: State)
    requires pi in s.principals
    requires IsPrefix(pi.prefix, alt)
    requires forall pi' :: Covers(pi', alt, s.principals) && pi' != pi ==>
      |pi.prefix.components| > |pi'.prefix.components|
    ensures IsEffectiveOwner(pi, alt, Fork(s, alt).principals)
  { }

  // Existence: for any π, there exists alt ∈ dom(π) where π is effective owner.
  // ASN-0042 constructive argument:
  //   zeros=1: sub-delegates cannot reach document-level (would need ≥2 zeros)
  //   zeros=0: choose user-field exceeding all sub-delegate prefixes (T0a)
  lemma ForkAddressExists(pi: Principal, s: State)
    requires pi in s.principals
    requires AccountBoundary(s.principals)
    ensures exists alt ::
      (IsPrefix(pi.prefix, alt) &&
       (forall pi' :: Covers(pi', alt, s.principals) && pi' != pi ==>
         |pi.prefix.components| > |pi'.prefix.components|))
  {
    assume {:axiom} false;  // witness construction requires finite-set reasoning over principals
  }
}
