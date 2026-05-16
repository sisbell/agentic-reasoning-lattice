include "../TumblerAlgebra/TumblerAlgebra.dfy"
include "TumblerOwnership.dfy"

// O2 — OwnershipExclusivity
// (A a in Sigma.alloc : (E! pi in Pi : omega(a) = pi))
// Derived from O4 (DomainCoverage) and O1b (PrefixInjective)
module OwnershipExclusivity {
  import opened TumblerAlgebra
  import opened TumblerOwnership

  // O4 — Domain coverage (assumed as precondition)
  ghost predicate DomainCoverage(s: State) {
    forall a :: a in s.alloc ==> exists pi :: Covers(pi, a, s.principals)
  }

  // Equal-length covering prefixes are identical (T3)
  lemma EqualLengthCoveringEqual(p1: Tumbler, p2: Tumbler, a: Tumbler)
    requires IsPrefix(p1, a)
    requires IsPrefix(p2, a)
    requires |p1.components| == |p2.components|
    ensures p1 == p2
  { }

  // Uniqueness: at most one effective owner
  lemma EffectiveOwnerUnique(
    p1: Principal, p2: Principal, a: Tumbler,
    principals: set<Principal>
  )
    requires IsEffectiveOwner(p1, a, principals)
    requires IsEffectiveOwner(p2, a, principals)
    ensures p1 == p2
  { }

  // Among covering principals, one has strictly longer prefix than all others.
  // Induction on the candidate set; equal-length case collapses via
  // EqualLengthCoveringEqual + structural equality of Principal.
  lemma MostSpecificExists(
    candidates: set<Principal>,
    principals: set<Principal>,
    a: Tumbler
  )
    requires candidates <= principals
    requires candidates != {}
    requires forall pi :: pi in candidates ==> IsPrefix(pi.prefix, a)
    ensures exists pi ::
      (pi in candidates &&
       forall pi' :: pi' in candidates && pi' != pi ==>
         |pi.prefix.components| > |pi'.prefix.components|)
    decreases |candidates|
  {
    var x :| x in candidates;
    var rest := candidates - {x};
    if rest == {} {
      assert forall pi' :: pi' in candidates && pi' != x ==> pi' in rest;
    } else {
      MostSpecificExists(rest, principals, a);
      var best :| best in rest &&
        (forall pi' :: pi' in rest && pi' != best ==>
          |best.prefix.components| > |pi'.prefix.components|);
      if |x.prefix.components| > |best.prefix.components| {
      } else if |x.prefix.components| == |best.prefix.components| {
        EqualLengthCoveringEqual(x.prefix, best.prefix, a);
      } else {
      }
    }
  }

  // O2 — OwnershipExclusivity
  lemma OwnershipExclusivity(s: State, a: Tumbler)
    requires a in s.alloc
    requires DomainCoverage(s)
    ensures exists pi :: IsEffectiveOwner(pi, a, s.principals)
    ensures forall p1, p2 ::
      (IsEffectiveOwner(p1, a, s.principals) &&
       IsEffectiveOwner(p2, a, s.principals)) ==> p1 == p2
  {
    var candidates := set pi | pi in s.principals && IsPrefix(pi.prefix, a);
    var w :| w in s.principals && IsPrefix(w.prefix, a);
    assert w in candidates;
    MostSpecificExists(candidates, s.principals, a);
    var best :| best in candidates &&
      (forall pi' :: pi' in candidates && pi' != best ==>
        |best.prefix.components| > |pi'.prefix.components|);
    assert IsEffectiveOwner(best, a, s.principals);
    forall p1, p2 |
      IsEffectiveOwner(p1, a, s.principals) &&
      IsEffectiveOwner(p2, a, s.principals)
      ensures p1 == p2
    {
      EffectiveOwnerUnique(p1, p2, a, s.principals);
    }
  }
}
