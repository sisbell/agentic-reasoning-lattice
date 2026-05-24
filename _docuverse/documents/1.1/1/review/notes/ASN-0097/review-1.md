# Review of ASN-0097

## REVISE

### Issue 1: Transition claims lack explicit proofs
**ASN-0097, Π8, Π9, Π10**: Stated as multi-part inclusions/equalities with one-sentence justifications.
**Problem**: Π8(a) (set inclusion), Π8(b) (set equality), Π9(a) (set equality), and Π10(a)+(b) each require multi-step derivations from the K.μ contracts. The ASN cites the contract preamble but never derives the projection consequence. "Extension can only grow the projection" is a claim, not a proof — neither direction of the difference-set equality in Π8(b) is exhibited.
**Required**: Show one full derivation per Π8, Π9, Π10 from definition. The set equalities (Π8(b), Π9(a), Π10(a), Π10(b)) need both ⊆ and ⊇ shown explicitly.

### Issue 2: Π10(b) set equality without showing both directions
**ASN-0097, Π10(b)**: "The V-projection is permuted: proj(d, e, Σ') = {π(v) : v ∈ proj(d, e, Σ)}"
**Problem**: This is an equality of sets but the justification ("Rearrangement preserves the set of (V, I) pairs up to permutation") does not show ⊆ and ⊇. The ⊇ direction uses `Σ'.M(d)(π(v)) = Σ.M(d)(v)`; the ⊆ direction additionally uses bijectivity of π. Neither is exhibited.
**Required**: Exhibit both inclusions using the K.μ~ contract and the bijection property.

### Issue 3: Π11 prose-vs-formal mismatch
**ASN-0097, Π11**: "Synthesizing Π8–Π10: if a state transition leaves some I-address a ∈ cov(e) mapped to a V-position in M(d) — possibly at a different V-position than before — then the projection in Σ' contains a's new V-position."
**Problem**: The prose frames this as a transition-level synthesis of Π8–Π10. The symbolic claim, however, is a single-state property of any Σ', requiring no transition reasoning at all — it is one rewrite from the definition of proj. As stated, Π11 either is redundant with the definition (state-level reading) or lacks the transition reasoning the prose claims (transition reading).
**Required**: Either (a) reformulate symbolically as a transition property `Σ → Σ'` and derive from Π8/Π9/Π10, or (b) acknowledge it as a definitional rearrangement and remove the "synthesis" framing.

### Issue 4: R13 (boundary insertion) depends on an unstated link-creation constraint
**ASN-0097, R13 and Π13 commentary**: "newly allocated addresses (via K.α) are not in any existing endset's coverage (they did not exist when the link was made)"
**Problem**: The argument requires that cov(e) at link creation contained only addresses already in dom(Σ.C) at that time. The ASN does not establish this. The shared vocabulary defines spans as "contiguous ranges in address space" and endsets as references to I-addresses, but does not restrict either to allocated addresses. Without an explicit link-creation constraint, K.α could allocate an address `a_new ∈ cov(e)` for some pre-existing link, and a subsequent K.μ⁺ would silently extend that link's projection — the exact behavior R13 promises is excluded.
**Required**: Cite or state the link-allocation rule that constrains endset coverage at creation to dom(Σ.C), or weaken R13 to a conditional ("provided the link-allocation rule restricts endsets to then-allocated addresses").

### Issue 5: Π15 collapses to Π0
**ASN-0097, Π15**: "(A ℓ ∈ dom(Σ.L), Σ → Σ' :: ℓ ∈ dom(Σ'.L) ∧ Σ'.L(ℓ) = Σ.L(ℓ))"
**Problem**: The formal statement of Π15 is literally Π0. The substantive content — that a link can exist in L without being arranged in any M(d), and can be removed from an M(d) arrangement without leaving L — appears only in the prose ("regardless of whether (E d, v :: ...)"). The reverse-orphaning property is real but the formalization given does not capture it.
**Required**: Formalize the bidirectional independence properly: (a) a link in L need not be in the range of any M(d), and (b) for any link ever in range of some M(d), a subsequent K.μ⁻ may remove it from that range without changing Σ.L. Derive each from L12 and the relevant frame condition.

### Issue 6: No concrete example
**ASN-0097**: Eighteen Π claims, twelve R-reliances, and three modes of displacement, all entirely abstract.
**Problem**: The review standards require verification of key postconditions against at least one specific scenario. Without one, the reader cannot confirm that the claims survive a non-trivial state.
**Required**: Walk through one scenario — e.g., a link with cov = {a₅, a₆, a₇}, document d with M = {0→a₅, 1→a₆, 2→a₇, 3→a₈}, then apply K.μ⁻ removing position 1, then K.μ~ swapping positions 0 and 2 — and verify Π8/Π9/Π10/Π11 and iproj-invariance against the resulting state.

### Issue 7: Weakest-precondition analysis absent
**ASN-0097**: No wp computation appears anywhere.
**Problem**: The review standards treat wp analysis as mandatory and call out trivial-only wp as insufficient. The ASN provides forward-direction analysis throughout (what holds after a transition) but no backward analysis.
**Required**: Compute one non-trivial wp — e.g., `wp(K.μ⁻, iproj(d, e) ≠ ∅)` (which positions must be retained so that the projection remains non-empty) or `wp(K.μ⁺, reaches(ℓ, d, V_q))` (which extensions establish discoverability in V_q).

## OUT_OF_SCOPE

### Topic 1: Path-independence of composite μ-transitions
**Why out of scope**: Raised correctly in Open Questions as a follow-on ASN topic.

### Topic 2: Lifted projections over endset unions/intersections
**Why out of scope**: Structural generalization; belongs in a follow-on ASN.

### Topic 3: Multi-origin endset projection across document boundaries
**Why out of scope**: A genuinely new topic about how per-document projections compose when cov(e) spans multiple originating documents.

VERDICT: REVISE
