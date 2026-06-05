# Review of ASN-0103

I checked the load-bearing proofs — the length-restricted frontier `D_A`, the freshness argument, the cross-allocator version-dominance argument, and the invariant discharge — case by case. Each holds.

## What I verified

**The `D_A = E ∩ S(A,2)` identity.** Both inclusions are proven, and the load-bearing direction (`D_A ⊆ S(A,2)`) is genuinely derived via T4b's unique parse: `Document(e) ∧ parent(e) = A ∧ #e = #A+2 ⟹ e = [A,0,j]`. The length filter `#e = #A+2` is what excludes versions (length `≥ #A+3`), and the worked example demonstrates the concrete collision (`inc(v1,0)` re-baptising the next version) that an unrestricted frontier would cause. This is exactly the kind of boundary the review standard demands, and it is shown, not asserted.

**Freshness.** `d ∈ S(A,2) \ D_A = S(A,2) \ E ⟹ d ∉ E` holds without the contiguity assumption the ASN deliberately declines. The `D_A = ∅` (first-document) boundary and the subsequent case are both covered. The exclusion split (nodes/accounts by `zeros=2`, documents/versions by stream membership) is exhaustive.

**Version dominance.** The on-chain `v_{#A+1}=0` argument correctly avoids T9 (different allocator) and argues directly by T1 at position `#A+2`, establishing the root `d_i ∈ D_A` via P1 persistence so that `i ≤ p−1 < p`. The off-chain `v_{#A+1}≠0` case is correctly scoped to distinctness-by-divergence rather than dominance. The `#t ≥ #A` sub-argument (prefix `t ≼ A` would force `zeros(t) ≤ 1`, contradicting `zeros(t)=2`) is sound, and the "exactly one k=2 descent off A" derivation is airtight (a second k=2 violates `zeros(operand) ≤ 1`; a leading k=0 breaks `A ≼ t`).

**Deferrals are honest, not holes.** The O5 authority and the `ω`-valued ownership are correctly declined because the state `(C,L,E,M,R)` carries no registry `B`; the ASN asserts only the structurally-derivable `pfx(π) ≼ A ≼ d`. CND.A-act is a clearly-labeled standing assumption owed by out-of-scope account provisioning, with a coherent account-tier analogue to SubAllocatorBundle. The avoidance of GlobalUniqueness (undischarged T10a-conformance) and B8's same-namespace branch (undischarged single-authority) in favor of S0 + B7 is correct and necessary.

**Invariant discharge.** Every conjunct of ExtendedReachableStateInvariants and P3 is accounted for — directly verified, vacuous via `dom(M'(d)) = ∅`, or frame-inherited via `C'=C ∧ L'=L ∧ R'=R`. The frame batches are legitimate inheritance, not hand-waves. Atomicity follows from the single-K.δ decomposition. Coupling J0/J1★/J1'★ vacuous (no content, no provenance).

## OUT_OF_SCOPE

### Topic 1: Entity-set ↔ baptismal-registry coupling for the `ω`-valued ownership
**Why out of scope**: The effective-owner statement `ω_{Σ'}(d) = ω_Σ(A)` requires a state carrying the registry `B` and an `E`↔`B` coupling invariant no foundation supplies. The ASN correctly defers this (and flags it in Open Questions). Belongs to a registry-carrying ASN.

### Topic 2: Failure recovery, concurrent creation, write-readiness, never-populated-document removal
**Why out of scope**: These are the Open Questions; each concerns dynamics (crash recovery, concurrency serialization, session semantics, garbage collection) beyond the single atomic creation transition this ASN specifies.

VERDICT: CONVERGED
