include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "PrefixDetermination.dfy"

// O6 — StructuralProvenance
// (A a, b ∈ Σ.alloc : acct(a) = acct(b) ⟹ ω(a) = ω(b))
// Derived from O1a, T4, AccountPrefix
module StructuralProvenance {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import PrefixDetermination

  type Principal = PrefixDetermination.Principal

  // Definition — AccountField
  // zeros(a) = 0: acct(a) = a
  // zeros(a) ≥ 1: acct(a) = truncation through user field (N.0.U)
  function AccountField(t: Tumbler): Tumbler
    requires TumblerHierarchy.ValidAddress(t)
  {
    var z0 := FindZero(t.components, 0);
    if z0 >= |t.components| then
      t
    else
      var z1 := FindZero(t.components, z0 + 1);
      Tumbler(t.components[..z1])
  }

  // AccountPrefix — acct(a) ≼ a
  lemma AccountPrefix(a: Tumbler)
    requires TumblerHierarchy.ValidAddress(a)
    ensures IsPrefix(AccountField(a), a)
  { }

  // Helper: a zero at position i implies ZeroCount ≥ 1
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

  // Helper: zeros at positions i and j imply ZeroCount ≥ 2
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

  // Forward: p ≼ a ∧ zeros(p) ≤ 1 ⟹ p ≼ acct(a)
  lemma CoveringToAccount(p: Tumbler, a: Tumbler)
    requires TumblerHierarchy.ValidAddress(a)
    requires TumblerHierarchy.ZeroCount(p.components) <= 1
    requires IsPrefix(p, a)
    ensures IsPrefix(p, AccountField(a))
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

  // Reverse: p ≼ acct(a) ⟹ p ≼ a
  lemma AccountToCovering(p: Tumbler, a: Tumbler)
    requires TumblerHierarchy.ValidAddress(a)
    requires IsPrefix(p, AccountField(a))
    ensures IsPrefix(p, a)
  {
    AccountPrefix(a);
  }

  // Effective owner: most-specific covering principal
  ghost predicate IsEffectiveOwner(pi: Principal, a: Tumbler, principals: set<Principal>) {
    pi in principals && IsPrefix(pi.prefix, a) &&
    forall pi' :: pi' in principals && IsPrefix(pi'.prefix, a) && pi' != pi ==>
      |pi.prefix.components| > |pi'.prefix.components|
  }

  // DIVERGENCE: The ASN states O6 over ω (effective owner) and Σ.alloc. The Dafny
  // model captures the structural core: same account field implies identical covering
  // sets for all O1a-compliant prefixes (zeros ≤ 1). Since ω is defined as the
  // most-specific covering prefix, identical covering sets give identical ω.
  // Modeling ω directly would require the full principal set as a parameter.

  // O6 — StructuralProvenance (biconditional core)
  // Same account field ⟹ same covering set for all O1a-compliant prefixes
  lemma CoveringBiconditional(a: Tumbler, b: Tumbler, p: Tumbler)
    requires TumblerHierarchy.ValidAddress(a)
    requires TumblerHierarchy.ValidAddress(b)
    requires AccountField(a) == AccountField(b)
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
  // acct(a) = acct(b) ⟹ ω(a) = ω(b)
  lemma StructuralProvenance(
    a: Tumbler, b: Tumbler,
    principals: set<Principal>,
    pi_a: Principal, pi_b: Principal
  )
    requires TumblerHierarchy.ValidAddress(a)
    requires TumblerHierarchy.ValidAddress(b)
    requires AccountField(a) == AccountField(b)
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
