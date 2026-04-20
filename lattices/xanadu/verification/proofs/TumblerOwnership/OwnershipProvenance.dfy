include "../TumblerAlgebra/TumblerAlgebra.dfy"
include "../TumblerAlgebra/TumblerHierarchy.dfy"
include "TumblerOwnership.dfy"

// OwnershipProvenance — O0, O1, O1a, O1b, O6, AccountPrefix
module OwnershipProvenance {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import opened TumblerOwnership

  // O0 — StructuralOwnership
  // Ownership is decidable from pfx(pi) and a alone, without mutable state.
  // Structurally guaranteed: Owns takes only prefix and address, no State.
  // (Defined in TumblerOwnership.Owns)

  // O1a — AccountBoundary
  // (A pi in Pi : zeros(pfx(pi)) <= 1)
  ghost predicate AccountBoundary(s: State) {
    forall pi :: pi in s.principals ==>
      TumblerHierarchy.ZeroCount(pi.prefix.components) <= 1
  }

  // O1b — PrefixInjective
  // (A p1, p2 in Pi : pfx(p1) = pfx(p2) ==> p1 = p2)
  // DIVERGENCE: With Principal modeled as a datatype whose sole field is
  // the prefix tumbler, injectivity holds by construction (structural
  // equality). Sound: any model satisfying the abstract version also
  // satisfies this one, and vice versa.
  ghost predicate PrefixInjective(s: State) {
    forall p1, p2 ::
      (p1 in s.principals && p2 in s.principals && p1.prefix == p2.prefix)
        ==> p1 == p2
  }

  // AccountPrefix — acct(a) <= a
  lemma AccountPrefixLemma(a: Tumbler)
    requires TumblerHierarchy.ValidAddress(a)
    ensures IsPrefix(Acct(a), a)
  { }

  // Helper: a zero at position i implies ZeroCount >= 1
  lemma ZeroAtIndex(s: seq<nat>, i: nat)
    requires i < |s|
    requires s[i] == 0
    ensures TumblerHierarchy.ZeroCount(s) >= 1
    decreases |s|
  {
    if i > 0 {
      ZeroAtIndex(s[1..], i - 1);
    }
  }

  // Helper: zeros at positions i and j imply ZeroCount >= 2
  lemma TwoZerosCount(s: seq<nat>, i: nat, j: nat)
    requires i < j < |s|
    requires s[i] == 0
    requires s[j] == 0
    ensures TumblerHierarchy.ZeroCount(s) >= 2
    decreases |s|
  {
    if i == 0 {
      ZeroAtIndex(s[1..], j - 1);
    } else {
      TwoZerosCount(s[1..], i - 1, j - 1);
    }
  }

  // Forward: p <= a && zeros(p) <= 1 ==> p <= acct(a)
  lemma CoveringToAccount(p: Tumbler, a: Tumbler)
    requires TumblerHierarchy.ValidAddress(a)
    requires TumblerHierarchy.ZeroCount(p.components) <= 1
    requires IsPrefix(p, a)
    ensures IsPrefix(p, Acct(a))
  {
    var z0 := FindZero(a.components, 0);
    if z0 >= |a.components| {
    } else {
      var z1 := FindZero(a.components, z0 + 1);
      if z1 >= |a.components| {
      } else if |p.components| > z1 {
        TwoZerosCount(p.components, z0, z1);
      }
    }
  }

  // Reverse: p <= acct(a) ==> p <= a
  lemma AccountToCovering(p: Tumbler, a: Tumbler)
    requires TumblerHierarchy.ValidAddress(a)
    requires IsPrefix(p, Acct(a))
    ensures IsPrefix(p, a)
  {
    AccountPrefixLemma(a);
  }

  // O6 — StructuralProvenance (biconditional core)
  // Same account field ==> same covering set for all O1a-compliant prefixes
  lemma CoveringBiconditional(a: Tumbler, b: Tumbler, p: Tumbler)
    requires TumblerHierarchy.ValidAddress(a)
    requires TumblerHierarchy.ValidAddress(b)
    requires Acct(a) == Acct(b)
    requires TumblerHierarchy.ZeroCount(p.components) <= 1
    ensures IsPrefix(p, a) <==> IsPrefix(p, b)
  {
    if IsPrefix(p, a) {
      CoveringToAccount(p, a);
      AccountToCovering(p, b);
    }
    if IsPrefix(p, b) {
      CoveringToAccount(p, b);
      AccountToCovering(p, a);
    }
  }

  // O6 — StructuralProvenance
  // acct(a) = acct(b) ==> omega(a) = omega(b)
  lemma StructuralProvenance(
    a: Tumbler, b: Tumbler,
    principals: set<Principal>,
    pi_a: Principal, pi_b: Principal
  )
    requires TumblerHierarchy.ValidAddress(a)
    requires TumblerHierarchy.ValidAddress(b)
    requires Acct(a) == Acct(b)
    requires IsEffectiveOwner(pi_a, a, principals)
    requires IsEffectiveOwner(pi_b, b, principals)
    requires forall pi :: pi in principals ==>
      TumblerHierarchy.ZeroCount(pi.prefix.components) <= 1
    ensures pi_a == pi_b
  {
    CoveringBiconditional(a, b, pi_a.prefix);
    CoveringBiconditional(a, b, pi_b.prefix);
  }
}
