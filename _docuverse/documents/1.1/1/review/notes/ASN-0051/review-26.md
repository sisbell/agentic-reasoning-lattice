# Review of ASN-0051

## REVISE

### Issue 1: SV0 is a definitional restatement, not a substantive claim
**ASN-0051, "Endset Projection" section, SV0**: "For every state Σ, endset e, and document d ∈ Σ.E_doc: `locate_Σ(e, d) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)}`"
**Problem**: This is literally the definition of locate from two paragraphs earlier, with state subscripts added. As stated, SV0 is a tautology. The substantive architectural claim ("no state component external to (coverage(e), M(d)) participates in resolution") lives entirely in the surrounding prose.
**Required**: Either reformulate SV0 as a substantive theorem about the algebra — e.g., "no operation in {K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ} writes or reads any state component that contributes to locate beyond Σ.L (via coverage) and Σ.M(d)" — with proof by inspection of each transition's effect/frame, or demote SV0 from a numbered property to a definitional remark.

### Issue 2: SV6 precondition omits required T4-validity of s
**ASN-0051, SV6 statement**: "For a span (s, ℓ) in an existing endset where s is element-level (zeros(s) = 3), and a newly allocated address b with zeros(b) = 3 and origin(b) ≠ origin(s)"
**Problem**: The precondition `zeros(s) = 3` is necessary but not sufficient for `origin(s)` to be defined — T4b's projections N, U, D require T4-validity (no adjacent zeros, t₁ ≠ 0, t_{#t} ≠ 0). L4 (EndsetGenerality) permits span starts that are not T4-valid. The proof's "field separator positions p₁, p₂, p₃ of s" reasoning silently presumes T4-validity, and the condition "origin(b) ≠ origin(s)" only type-checks when origin(s) is defined.
**Required**: Add T4-validity of s to the precondition explicitly. The current implicit assumption — that origin(s) is well-defined — should be stated as a precondition, not derived in the proof.

### Issue 3: SV10 existential lacks a concrete witness
**ASN-0051, SV10**: "(E Σ, a, d, s, V ⊆ dom(M(d)) :: a ∈ discover_s({M(d)(v) : v ∈ V}) ∧ π(Σ.L(a).s, d) ⊊ coverage(Σ.L(a).s))"
**Problem**: The existential is supported only by intuitive narration ("Suppose a link's from-endset covers I-addresses {i₁, i₂, i₃}..."). An existential claim is established by exhibiting a witness, not by sketching one. The worked example later constructs concrete tumblers for SV6 but no comparable witness is given for SV10.
**Required**: Exhibit a concrete witness with specific tumbler values — analogous to the SV6 worked example — demonstrating coverage(F) ⊋ π(F, d) under a state satisfying all S- and L-invariants.

### Issue 4: wp analysis mixes pre-state and post-state predicates
**ASN-0051, "Weakest Precondition Analysis" section**: "wp(K.μ⁻, π(e, d) ≠ ∅) = `coverage(e) ∩ ran(M'(d)) ≠ ∅`"
**Problem**: A weakest precondition is by definition a predicate on the *pre-state*. The right-hand side here references ran(M'(d)) — the post-state arrangement — which is just the postcondition restated. The same issue occurs in wp(K.μ⁺, ...) where the second disjunct quantifies over M' \ M. The "vitality loss condition" further down ("(A i : i ∈ coverage(e) ∩ ran(M(d)) :: i ∉ ran(M'(d)))") still mixes M and M'. The section claims to "read off wp by direct rearrangement" but doesn't actually compute pre-state predicates.
**Required**: For each elementary transition K parameterised by its effect inputs (e.g., V_remove for K.μ⁻, new mappings for K.μ⁺), express wp as a predicate on (Σ, effect-inputs) referencing only the pre-state M. Alternatively, rename the section to "post-condition characterisation" or "vitality-loss characterisation" and drop the wp framing.

### Issue 5: Worked example covers only m = 1 and injective M(d) for SV11
**ASN-0051, "Worked Example" section**: The example endset is F = {(a₂, ℓ)} — a single span.
**Problem**: SV11's central claim concerns the m · p decomposition and the *cover-not-partition* behaviour under non-injective M(d). The example exercises neither: m = 1 collapses the m · p bound, and the arrangement is injective. Neither term-overlap within a block nor fragment-overlap across blocks is illustrated. The standard for "concrete example" — verify the key postconditions against a specific scenario — is met for SV2–SV6 but not for SV11.
**Required**: Add (or extend) an example with m ≥ 2 spans and a non-injective M(d) (within-document sharing via S5) so the cover-not-partition behaviour is visible, and the m · p bound is exercised non-trivially.

### Issue 6: "Same-origin coverage growth" section has no formal status
**ASN-0051, "Content Allocation and Coverage Stability" section**: The "Counterexample to a universal exclusion claim" paragraph and the "architectural resolution" discussion.
**Problem**: The section presents informal counterexamples to an unnamed claim and concludes with a design observation ("endset coverage stability is architectural, not definitional"). No SV property is introduced; no explicit deferral is recorded. A Dijkstra reviewer reading the ASN top-to-bottom cannot tell whether the section asserts a guarantee, denies one, or defers the question.
**Required**: Either state a formal property (positive or negative) capturing the same-origin growth modes, or add an explicit scoping note: "We make no formal claim about same-origin coverage growth in this ASN; the matter is deferred to [target ASN]." The "Remark" in SV13(f) is a step in this direction but is buried in the synthesis.

### Issue 7: SV6 proof step combining cases would benefit from explicit structure
**ASN-0051, SV6 proof**: The arguments for "#t ≥ k" and "t agrees with s on positions 1 through k−1" use the same T1(i)-divergence machinery twice in a row, with only the bound on j changing.
**Problem**: The reader has to verify essentially the same argument twice and check that the second invocation's bound (j < k) is compatible with the first's conclusion (#t ≥ k). The proof would be cleaner — and more reliably correct — as a single lemma: "any t with s ≤ t ≤ s ⊕ ℓ' (where ℓ' has action point k) agrees with s on positions 1..k−1 and has #t ≥ k." Read as written, the redundancy invites the suspicion of a hidden gap.
**Required**: Restructure the SV6 proof to extract the shared T1(i)-contradiction argument once, then apply it to both conclusions.

## OUT_OF_SCOPE

### Topic 1: Higher-arity links (N > 3)
**Why out of scope**: The scoping note explicitly restricts to standard triples (arity 3); generalisation follows the same machinery slot-wise and is deferred.

### Topic 2: Link-subspace projection and reflexive endsets
**Why out of scope**: Explicitly deferred to a future Link Subspace ASN; the π_text / π distinction is introduced to mark the boundary cleanly.

### Topic 3: Bilateral vitality across forks
**Why out of scope**: Forking is a composite transition (J4 in ASN-0047); elementary-transition analysis here suffices and the fork-specific question is recorded in Open Questions.

### Topic 4: Discovery latency and indexing performance
**Why out of scope**: An implementation concern, not a survivability invariant; recorded in Open Questions.

VERDICT: REVISE
