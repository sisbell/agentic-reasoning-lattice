# Channel Assignment — ASN-0040 review-19

**Date:** 2026-05-11 08:55

## Issue 1: State space and transition system never formally defined
Reason: Fix is internal — the AllocatedSet foundation already defines 𝒮, Σ, and s → s'. The author needs to apply this framework explicitly at the ASN's start, define reachability from B₀ as reflexive-transitive closure, and recast preservation proofs within it.

## Issue 2: B4 uses undefined temporal vocabulary
Reason: Fix is internal — once Issue 1's transition framework is in place, B4 recasts cleanly as "Bop is an atomic state transition; two same-namespace Bop transitions are linearly ordered in any execution." The ASN already notes Gregory's single-threaded dispatch achieves this; no new evidence needed.

## Issue 3: B0a "produced by baptism" predicate informally defined
Reason: Fix is internal — reformulate as a constraint on the operation vocabulary: "The only state transition that increases Σ.B is Bop, whose preconditions require B6(p, d)." This converts a provenance predicate into an operation-set axiom verifiable by future ASNs.

## Issue 4: B3 "occupied" predicate undefined; forbidden case is a forward requirement, not current invariant
Reason: Fix is internal — reframe B3 as a forward requirement on future content operations ("any operation populating t must precondition t ∈ Σ.B") and drop the trivalent table, or parameterize over a future `Occupied(t, σ_content)` predicate. The narrative already concedes this framing.

## Issue 5: T5 cited under non-canonical name
Reason: Fix is internal — substitute canonical `T5 (ContiguousSubtrees)` per the foundation registry. Pure naming alignment.

## Issue 6: Relationship between Σ.B and ASN-0034's `allocated(s)` not specified
Reason: Fix is internal — the ASN's own narrative ("B0 is the state-level reading of T8") already implies Σ.B ≡ allocated(s) under the identification of namespaces (p, d) with allocators. The author must state this equality explicitly and derive B0 as a corollary of T8 rather than stipulate it.
