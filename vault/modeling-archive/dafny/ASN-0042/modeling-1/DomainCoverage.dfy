include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "PrefixDetermination.dfy"

// O4 — DomainCoverage
// (A a ∈ Σ.alloc : (E π ∈ Π : pfx(π) ≼ a))
// Derived from O5 (SubdivisionAuthority), O14 (BootstrapPrincipal), O16 (AllocationClosure)
module DomainCoverage {
  import opened TumblerAlgebra
  import PrefixDetermination

  type Principal = PrefixDetermination.Principal

  datatype State = State(principals: set<Principal>, alloc: set<Tumbler>)

  ghost predicate Covers(pi: Principal, a: Tumbler, principals: set<Principal>) {
    pi in principals && IsPrefix(pi.prefix, a)
  }

  // O4 — DomainCoverage
  ghost predicate DomainCoverage(s: State) {
    forall a :: a in s.alloc ==> exists pi :: Covers(pi, a, s.principals)
  }

  // O12 — PrincipalPersistence
  ghost predicate PrincipalPersistence(s: State, s': State) {
    s.principals <= s'.principals
  }

  // O5 + O16 — every new allocation is covered by some principal
  ghost predicate NewAllocationsCovered(s: State, s': State) {
    forall a :: a in s'.alloc && a !in s.alloc ==>
      exists pi :: Covers(pi, a, s'.principals)
  }

  // Inductive step: DomainCoverage is preserved across transitions.
  // Base case: O14 (BootstrapPrincipal) establishes DomainCoverage(Σ₀).
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
}
