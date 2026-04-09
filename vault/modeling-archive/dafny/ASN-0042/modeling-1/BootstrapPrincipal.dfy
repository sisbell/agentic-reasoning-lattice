include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "PrefixDetermination.dfy"

// O14 — BootstrapPrincipal
// Π₀ ≠ ∅ ∧ (A a ∈ Σ₀.alloc : (E π ∈ Π₀ : pfx(π) ≼ a))
// (A π ∈ Π₀ : zeros(pfx(π)) ≤ 1)
// (A π₁, π₂ ∈ Π₀ : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)
// (A π ∈ Π₀ : T4(pfx(π)))
// (A π₁, π₂ ∈ Π₀ : π₁ ≠ π₂ ⟹ pfx(π₁) ⋠ pfx(π₂) ∧ pfx(π₂) ⋠ pfx(π₁))
module BootstrapPrincipal {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import PrefixDetermination

  type Principal = PrefixDetermination.Principal

  datatype State = State(principals: set<Principal>, alloc: set<Tumbler>)

  // O14 — BootstrapPrincipal
  // Initial state invariant: bootstrap principals are non-empty, cover all
  // allocated addresses, have injective valid prefixes with zeros ≤ 1,
  // and no two prefixes nest.
  ghost predicate BootstrapPrincipal(s: State) {
    // Π₀ ≠ ∅
    s.principals != {} &&

    // (A a ∈ Σ₀.alloc : (E π ∈ Π₀ : pfx(π) ≼ a))
    (forall a :: a in s.alloc ==>
      exists pi :: pi in s.principals && IsPrefix(pi.prefix, a)) &&

    // (A π ∈ Π₀ : zeros(pfx(π)) ≤ 1)
    (forall pi :: pi in s.principals ==>
      TumblerHierarchy.ZeroCount(pi.prefix.components) <= 1) &&

    // (A π₁, π₂ ∈ Π₀ : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)
    (forall p1, p2 ::
      (p1 in s.principals && p2 in s.principals && p1.prefix == p2.prefix)
        ==> p1 == p2) &&

    // (A π ∈ Π₀ : T4(pfx(π)))
    (forall pi :: pi in s.principals ==>
      TumblerHierarchy.ValidAddress(pi.prefix)) &&

    // (A π₁, π₂ ∈ Π₀ : π₁ ≠ π₂ ⟹ pfx(π₁) ⋠ pfx(π₂) ∧ pfx(π₂) ⋠ pfx(π₁))
    (forall p1, p2 ::
      (p1 in s.principals && p2 in s.principals && p1 != p2)
        ==> !IsPrefix(p1.prefix, p2.prefix) && !IsPrefix(p2.prefix, p1.prefix))
  }
}
