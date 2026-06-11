# Review of ASN-0111

I checked every formal claim against the foundations. The core specification is sound: the definition, RL0's wp derivation, the necessity/insufficiency split at the structural screen, the RL4 branched-history witness (I verified the K.δ chain from `n₀`, the branch-agreement of K.λ's binding precondition, and the coupling discharge), the three permanence families (I verified all three example tumblers component-by-component, the P8/NodeLineage contradiction chains, and the account user-field induction over K.δ's cases), the residual-class allocatability construction (node baptism, account/document/element frontier arguments all check against K.δ/K.λ preconditions and ChildSpawnFreshness/FrontierEquivalence), and the worked read (LP-Fin gives exactly the three claimed F-members in `coverage(F)`; the J0/J1★/J1'★ discharge for the K.α composites and the K.μ⁻ contraction route are correct). Three issues remain — one precision gap, two anti-bloat findings.

## REVISE

### Issue 1: RL4's "function of (a, Σ.L(a)) alone" gloss outruns its formal statement, and the claims table drops the precondition

**ASN-0111, RL4 / RL5 / Claims table**: "`readlink` is a function of `(a, Σ.L(a))` alone, immediate from the definition `readlink(a, Σ) = Σ.L(a)` on the success branch." and RL5: "`readlink` is a pure function of `(a, Σ.L(a))` (RL4)."

**Problem**: RL4's formal statement quantifies only over `a ∈ dom(Σ₁.L) ∩ dom(Σ₂.L)` with `Σ₁.L(a) = Σ₂.L(a)`. The factorization claim "function of `(a, Σ.L(a))` alone" — which RL5 cites as full purity — additionally requires the both-absent congruence: `a ∉ dom(Σ₁.L) ∧ a ∉ dom(Σ₂.L) ⟹ readlink(a, Σ₁) = ⊥ = readlink(a, Σ₂)`. This is immediate from the definition's else-branch but is never stated; as written, RL5 cites RL4 for a claim strictly broader than what RL4 proves. Compounding this, the claims-table row for RL4 reads "reachable `Σ₁, Σ₂` with `Σ₁.L(a) = Σ₂.L(a)` give `readlink(a, Σ₁) = readlink(a, Σ₂)`" — dropping the body's domain-membership precondition, so the table statement and the body statement are not the same claim under partial-function semantics.

**Required**: Add the one-line failure-branch clause to RL4 (both-undefined case yields `⊥ = ⊥` by the definition), so RL5's "pure function of `(a, Σ.L(a))`" is fully discharged by citation; restore the precondition `a ∈ dom(Σ₁.L) ∩ dom(Σ₂.L)` in the claims-table row so table and body agree.

### Issue 2: Justificatory parenthetical inside the 𝒮 definition; reachability restriction stated three times

**ASN-0111, "Deriving the read"**: "Writing `𝒮` for the extended state space whose members are the states `Σ = (C, L, E, M, R)` (ASN-0047 — the substrate state of ASN-0093 as extended there; these are the states the standing precondition already ranges over, and the ones carrying the `Σ.L` component the definition consults), with the second argument restricted to reachable states per the standing precondition, ..."

**Problem**: The clause "these are the states the standing precondition already ranges over, and the ones carrying the `Σ.L` component the definition consults" explains why 𝒮 is the right choice rather than what 𝒮 is — defensive justification of the reviser-drift kind. It also restates the reachability restriction that the standing-precondition paragraph already established and that the same sentence restates a third time ("with the second argument restricted to reachable states per the standing precondition"). One definition has accreted three statements of one fact plus a rationale.

**Required**: Reduce to the definitional content: 𝒮 is the extended state space of ASN-0047, members `Σ = (C, L, E, M, R)`. Delete the justification clause; one pointer to the standing precondition suffices for the reachability restriction.

### Issue 3: Composite-validity discharge duplicated verbatim plus a forward use-site pointer

**ASN-0111, RL4 construction and RL5 residual-class paragraph**: RL4: "...compose into valid composites: none touches `dom(C)`, a content-subspace arrangement range, or `R`, so J0, J1★, and J1'★ hold vacuously at every boundary (the same discharge covers the worked read's three bare K.λ steps below)"; residual class: "The steps compose into valid composites: none touches `dom(C)`, a content-subspace arrangement range, or `R`, so J0, J1★, and J1'★ hold vacuously at every boundary."

**Problem**: The same one-sentence discharge appears verbatim in two sections, and the first occurrence carries a forward pointer enumerating a third consumer ("the worked read's three bare K.λ steps below") — a downstream-use inventory embedded in a proof. This is exactly the accretion pattern the anti-bloat classifier targets: three sites depend on one argument, and the document handles it by repetition plus deferral instead of by naming it.

**Required**: State the discharge once as a named micro-lemma (e.g., *store-only composite validity*: a composite whose steps touch neither `dom(C)`, a content-subspace arrangement range, nor `R` satisfies J0, J1★, J1'★ vacuously) and cite it at the RL4 construction, the residual-class construction, and the worked read's K.λ steps; remove the forward pointer.

## OUT_OF_SCOPE

### Topic 1: Read authorization and visibility
**Why out of scope**: `readlink` returns the full recorded value to any holder of the address; whether reads are mediated by ownership or account identity is an access-control question no foundation ASN yet models — new territory for a future ASN, not an error here.

### Topic 2: Distinguishability guarantees deferred to FOLLOWLINK and link-identity ASNs
**Why out of scope**: The three Open Questions (validity inference from a read alone, empty-versus-unwitnessed endsets under resolution, distinguishing value-identical links) are correctly framed as obligations on future operations, not gaps in the read's contract.

VERDICT: REVISE
