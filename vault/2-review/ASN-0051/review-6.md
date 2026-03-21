# Review of ASN-0051

## REVISE

### Issue 1: SV6 precondition "within the element field" is informal
**ASN-0051, SV6 (CrossOriginExclusion)**: "when the action point of ℓ falls within the element field (i.e., beyond the three field separators)"
**Problem**: The proof's correctness hinges on the sandwich argument covering all three separator positions, which requires the action point k to satisfy k ≥ p₃ + 1 where p₃ is the position of s's third field separator. "Within the element field" is an informal gloss. A different reader might interpret "beyond the three field separators" as k > p₃ (same thing) or k ≥ p₃ (off by one, would miss the third separator). The T4 field decomposition gives the formal apparatus — the precondition should use it.
**Required**: State the precondition formally. One clean formulation: for s with zeros(s) = 3, let p₃ denote the position of the third zero component in s; the precondition is k > p₃. Equivalently: the leading k − 1 components of s contain all three field separators, i.e., |{i : 1 ≤ i ≤ k−1 ∧ sᵢ = 0}| = 3.

### Issue 2: Resolution change under reordering — claimed without proof, contradicted by worked example
**ASN-0051, SV5 section**: "resolve_{Σ'}(e, d) ≠ resolve_Σ(e, d) in general, because the V-positions have been remapped."
**ASN-0051, SV13(e)**: "Reordering of M(d) preserves π(e, d) but may change resolve(e, d). [SV5]"
**ASN-0051, Worked Example**: "resolve(F, d) = {v₂, v₄} — same V-positions, but v₂ now shows a₄ and v₄ shows a₂"
**Problem**: Three issues compound. (1) The claim "resolve ≠ resolve in general" is asserted without proof or witness; SV5 proves only projection invariance. (2) The worked example shows the resolve *set* is {v₂, v₄} both before and after the swap — it does not demonstrate resolution change. A reader following the example would conclude resolution is preserved. (3) The underlying formal relationship — resolve_{Σ'} = π(resolve_Σ) where π is the reordering bijection — is never stated, though it follows directly from K.μ~'s definition.
**Required**: (a) State the formal relationship: resolve_{Σ'}(e, d) = π(resolve_Σ(e, d)). (b) Prove or exhibit a witness that the resolve *set* can change: e.g., if π swaps a V-position in the resolve set with one outside it, the set changes (take dom(M(d)) = {v₁, v₂}, M(d) = {v₁ ↦ a₁, v₂ ↦ a₂}, coverage = {a₁}, π swaps v₁ and v₂ — resolve changes from {v₁} to {v₂}). (c) Annotate the worked example to note it shows a special case where the resolve set happens to be preserved (the swap permutes within the resolve set), and that the general case differs.

### Issue 3: SV7 formal content is subsumed by SV8
**ASN-0051, SV7 (TransclusionDiscovery)**: "discover_s({a}) in Σ ⊆ discover_s({a}) in Σ'"
**ASN-0051, SV8 (DiscoveryPermanence)**: "a ∈ discover_s(A) in Σ :: a ∈ discover_s(A) in Σ'"
**Problem**: SV8 establishes: for any fixed A and any transition Σ → Σ', every link discoverable through A in Σ remains discoverable through A in Σ'. Setting A = {a} and collecting over all links gives discover_s({a}) in Σ ⊆ discover_s({a}) in Σ' — which is SV7's formal statement exactly, for all transitions (not just K.μ⁺). SV7 adds no formal content beyond what SV8 provides. The architectural insight — that transclusion inherits link discoverability without a coupling step — is valuable, but it is a narrative observation about the *precondition context* (a entering ran(M(d₂)) via K.μ⁺), not a new formal property. As written, a future ASN referencing "SV7" should instead reference "SV8" since the latter is strictly stronger.
**Required**: Either (a) reframe SV7 as a corollary of SV8 and make the architectural observation explicit prose rather than a separate property, or (b) reformulate SV7 to capture something SV8 does not — e.g., the specific claim that no K.ρ or link-store operation is needed when V→I mappings are shared, which is a claim about the *absence of coupling constraints* rather than about discovery monotonicity.

### Issue 4: Bilateral vitality — vacuous case unaddressed
**ASN-0051, Bilateral Vitality definition**: "F = ∅ ∨ π(F, d) ≠ ∅ and G = ∅ ∨ π(G, d) ≠ ∅"
**Problem**: When both F = ∅ and G = ∅, both disjunctions are satisfied by the left branch, making the link bilaterally vital in every document — vacuously. L3 permits empty endsets, so such links exist. Nelson's "if anything is left at each end" presupposes something at each end to begin with. A link (∅, ∅, Θ) is a pure type annotation with no content endpoints; calling it "bilaterally vital" everywhere is formally correct but semantically odd and should be acknowledged. The vitality condition is used in the survivability narrative ("the link is useful when something remains at each content endset") — for a link with no content endsets, this narrative breaks down.
**Required**: Add a sentence stating that when both F = ∅ and G = ∅, bilateral vitality holds vacuously. Either (a) state this is intentional (the link has no content associations to lose), or (b) add a precondition `F ≠ ∅ ∨ G ≠ ∅` to make bilateral vitality non-trivial.

### Issue 5: SV13(e) omits non-arrangement transitions
**ASN-0051, SV13**: "for any state transition Σ → Σ'" ... clause (e) lists Extension, Contraction, Reordering, and cross-document isolation.
**Problem**: The preamble quantifies over *all* state transitions, but clause (e) discusses only arrangement operations (K.μ⁺, K.μ⁻, K.μ~). The remaining elementary transitions — K.α (content allocation), K.δ (entity creation), K.ρ (provenance recording) — all hold M in their frame, so resolve(e, d) is trivially preserved. This is immediate but unstated. A reader checking whether SV13 covers the full transition repertoire of ASN-0047 finds the gap.
**Required**: Add to SV13(e): "All other elementary transitions (K.α, K.δ, K.ρ) preserve M in their frame, so resolve(e, d) is unchanged."

## OUT_OF_SCOPE

### Topic 1: Same-origin byte-level coverage closure
**Why out of scope**: The ASN correctly identifies that same-origin byte-level coverage closure depends on "allocation discipline assumptions not formalised in this ASN." Formalizing the sibling-allocation-only discipline for text content and proving that tight spans over previously allocated content are closed to future allocations is a self-contained problem that belongs in a dedicated allocation-discipline ASN or as an extension to ASN-0034's T10a.

### Topic 2: Link creation as a state transition
**Why out of scope**: ASN-0047 defines transitions K.α through K.ρ but does not include a link creation transition. This ASN analyses existing links. Defining the link creation operation (and its coupling constraints — e.g., must endset I-addresses be in dom(C) at creation time?) is new territory for a future state-transitions extension.

### Topic 3: Resolution under composite transitions
**Why out of scope**: The ASN analyses each elementary transition kind independently. A composite that interleaves K.μ⁺ and K.μ⁻ on the same document can both enlarge and shrink the resolve set. Characterising the net effect requires compositional reasoning about transition sequences, which is a general framework question, not an error in this ASN's per-transition analysis.

VERDICT: REVISE
