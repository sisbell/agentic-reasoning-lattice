# Review of ASN-0099

## REVISE

### Issue 1: F9 restates the transition-shape distinction A1a already establishes

**ASN-0099, F9 (LinkStoreInertPreservation)**: "For every transition produced by an operation in V ∖ {K.λ} — written Σ → Σ' for an atomic operation of V_atomic ∖ {K.λ}, and Σ →* Σ' for the composite K.μ~ ... A1a gives Σ.L = Σ'.L across every V ∖ {K.λ} operation (single-step for the atomic operations, the K.μ⁻ + K.μ⁺ composite for K.μ~)."

**Problem**: The single-step-vs-composite shape distinction is now stated three times in close succession: in the definition of `V` ("a transition produced by a `V_atomic` operation is single-step ... whereas a transition produced by K.μ~ is the two-step composite"), again in A1a ("single-step Σ → Σ' for the atomic operations, the two-step composite Σ →* Σ' for K.μ~"), and a third time in F9. F9 already cites A1a for the link-store equality; re-deriving the transition shapes there adds no reasoning the reader does not already have from A1a two lines above. This is the meta-prose accretion the anti-bloat classifier targets — clarification repeated rather than carried by reference.

**Required**: In F9, state the equality via A1a by reference and drop the re-explanation of the single-step/composite shapes. The shapes are fixed once in `V`'s definition and once where the lemma is proved (A1a); the consuming claim should not restate them.

### Issue 2: F4's claim statement omits Weakening 1's design category

**ASN-0099, F4 (MatchIndividuation)**: "each exhibits an (a, I) pair on which an alternative match design — coverage-containment in either direction, a cardinality threshold, or an I-independent slot test — disagrees with F1."

**Problem**: F4 lists four alternative-design categories (containment each way, cardinality threshold, I-independent slot test) but presents five witnesses. Weakening 2 (`P_∃-slot ≡ (E i : coverage(eᵢ) ≠ ∅)`) is the "I-independent slot test." Weakening 1 (`P_⊤ ≡ a ∈ dom(Σ.L)`) is a match-everything design that is neither a slot test nor covered by any listed category — it ignores both `I` and the slots entirely. The claim statement therefore under-describes what F4 actually proves: a reader checking the claim against the witnesses finds one witness whose design is unnamed.

**Required**: Either add the trivial/"match-all" design to F4's enumerated categories, or fold `P_⊤` and `P_∃-slot` into a single accurately-named category ("I-independent designs"). The claim should name every design the witnesses refute.

VERDICT: REVISE
