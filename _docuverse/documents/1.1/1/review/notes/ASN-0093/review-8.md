# Review of ASN-0093

## REVISE

### Issue 1: L1c restatement weakens ASN-0043's L1c without acknowledgment

**ASN-0093, Link store invariants section, L1c**: "Every link address ℓ ∈ dom(L) has a structural inc-chain from its home document to ℓ: a finite sequence (t₀, t₁, …, tₙ) with t₀ = origin(ℓ) and tₙ = ℓ, where each step tᵢ = inc(tᵢ₋₁, kᵢ) with kᵢ ∈ {0, 1, 2} satisfies T10a's per-step admissibility constraints (T4-validity preservation, zero-count side conditions)."

**Problem**: ASN-0043's foundation L1c (per the extract supplied above) includes two clauses the substrate's restatement omits: `k₁ = 2` (first step is a depth-2 increment) and `(A i : 1 ≤ i ≤ n : #tᵢ > #s)` (every intermediate length strictly exceeds the seed's). The substrate's preamble describes L1c as inherited from ASN-0043 ("ASN-0043 introduced the link store and its structural invariants (L0/L1/L1a/L1b/L1c/L3/L12/L14)"), while the Properties Introduced table identifies L1c as a "Substrate commitment: per-step inc-rule conformance." These framings are inconsistent: the preamble suggests inheritance, but the substrate's L1c statement is strictly weaker than the foundation. The L1c chain exhibition (chain `d → b_C(d) → b_L(d) → ℓ` with k₁=2, k₂=0, k₃=1 and monotonically increasing length) actually does establish the stronger foundation form during discharge, so the substrate's invariant is sound but understated. The contrast paragraph below the L1c statement compares only to a different stronger form ("every intermediate tᵢ inhabits a T10a-tracked allocator's domain at the state of emission") and does not address the missing k₁=2 / length-increasing clauses. Downstream ASNs citing "L1c from the substrate" inherit the weaker form, even though the discharge proves more.

**Required**: Either (a) restate L1c using ASN-0043's formal clauses (including k₁ = 2 and `(A i : 1 ≤ i ≤ n : #tᵢ > #s)`), so that the invariant statement aligns with what the discharge proves; or (b) explicitly note that the substrate's L1c is a deliberately abstract restatement weaker than the foundation, with the contrast paragraph extended to mention the omitted k₁=2 / length-increasing clauses. Either way, reconcile the preamble's "inherited from ASN-0043" framing with the Properties Introduced table's "Substrate commitment" framing.

### Issue 2: ChainPrefixExtension's quantifier scope ambiguous; freshness derivations route through a redundant step-argument detour

**ASN-0093, ChainPrefixExtension lemma**: "At every reachable state Σ, every element of an active sub-allocator chain extends its anchor under the prefix relation: `(A d ∈ dom(M), t ∈ A_C(d) :: b_C(d) ≼ t)`."

**Problem**: A_C(d) per SubAllocatorAxiom.ChainDiscipline is the conceptual chain (all t_n for n ≥ 1, not only realized elements at Σ). The lemma quantifies over `t ∈ A_C(d)` without disambiguating whether this means the conceptual chain or only realized chain elements. The proof inducts over chain indices and establishes the conclusion for all n ≥ 1 (conceptual interpretation), but the statement leaves a reader free to read it either way. The K.α/K.λ subsequent-emit cross-document freshness derivations consume the conceptual interpretation — they need b_C(d) ≼ a for a freshly emitted address a not yet in dom(C) at Σ — yet they route through "ChainPrefixExtension's step argument (TA5(b)/(c) at k = 0 preserving positions 1..#a_prev − 1 under TA5-SigValid pinning sig(a_prev) = #a_prev)" applied to a_prev to "carry the prefix relation forward". Since a ∈ A_C(d) by ChainDiscipline's closure under inc(·, 0), ChainPrefixExtension(Σ) covers a directly under the conceptual interpretation; the step-argument detour is redundant.

**Required**: (a) Make the quantifier scope explicit, e.g., "for every t = t_n ∈ A_C(d) at any chain index n ≥ 1, b_C(d) ≼ t — including unrealized chain elements." (b) Simplify the K.α/K.λ subsequent-emit cross-document freshness derivations to cite ChainPrefixExtension(Σ) directly at a (since a ∈ A_C(d) by ChainDiscipline's closure), eliminating the step-argument detour.

### Issue 3: K.α and K.λ effect clauses do not state dom(M') = dom(M) explicitly

**ASN-0093, K.α Frame**: "L' = L; (A d' :: M'(d') = M(d'))." Similarly K.λ.

**Problem**: The frame `(A d' :: M'(d') = M(d'))` is pointwise function equality. Under standard partial-function semantics — undefined = undefined — this implies `dom(M') = dom(M)`, but the equality only fixes the *function values*, not the domain explicitly. ChainMembershipForOrigin's K.σ branch leans on the fact that K.α/K.λ are frame-preserving on M (so prior d' ∈ dom(M) remain there); the freshness arguments for K.α/K.λ similarly assume C2 and L1a are preserved across the transition (origin(a') ∈ dom(M(Σ)) implies origin(a') ∈ dom(M(Σ'))). Making `dom(M') = dom(M)` explicit in the frame removes any ambiguity about partial-function-equality semantics.

**Required**: State `dom(M') = dom(M)` directly in K.α's and K.λ's Frame clauses, alongside the pointwise function equality.

## OUT_OF_SCOPE

(All deferred items — arrangement mutation, entity stratification, provenance recording, coupling constraints, link withdrawal — are explicitly enumerated in the Scope section and Open Questions; nothing additional belongs in this category.)

VERDICT: REVISE
