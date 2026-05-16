# Review of ASN-0051

I read this ASN as Dijkstra would: looking for hand-waves, missing cases, and unproven claims. The ASN is unusually rigorous.

## What I checked

**SV6 proof structure.** Verified the sub-lemma's two pillars (prefix exclusion via T1(ii); divergence-is-upward via T1(i)), the conclusion (a)/(b) split on `t = s` vs `t ≠ s`, the field-separator alignment argument (p₁ ≥ 2, p₂ ≥ 4, p₃ ≥ 6 from T4-validity), and the T4-validity check for `t` covering all three conjuncts including the (k−1, k) boundary case. Position-by-position arithmetic at the worked tumbler example (s = 1.0.1.0.1.0.1.2.3, reach = 1.0.1.0.1.0.1.2.8) checks out.

**SV10 / CrossDocumentDecoupling witnesses.** Walked through the multi-step composite chain (InitialState n₀ = 1 → K.δ account → K.δ document → K.α i₂ → K.λ a → K.μ⁺ + K.ρ), verified S8a/D-MIN/S7c/K.α-amendment preconditions discharged at each step. Sibling-document allocation under shared account in the corollary witness correctly invokes SV6 since origin(j) = 1.0.1.0.2 ≠ origin(s_span) = 1.0.1.0.1, action point k = 8 > p₃ = 6.

**Worked Example arithmetic.** The K.μ~ + K.μ⁻ composite for removing a₃: ψ rotation places a₃ at v₅ (D-SEQ-admissible after the swap), K.μ⁻ then removes v₅. Block decomposition into β₁ = (v₁, a₁, 2), β₂ = (v₃, a₄, 2) — M7's I-adjacency fails (a₂ + 2 = a₄ would need a₄ = shift(a₁, 2) = a₃ ≠ a₄). Two-span non-injective scenario decomposes to 4 non-empty terms collapsing to 2 fragments via mechanism (b); three-span extension exhibits mechanism (a) without altering Σ.C.

**SV11 biconditional.** Both directions are rigorous. (⇒) chains the bounds fragment-count ≤ non-empty-term-count ≤ m·p and forces both to be tight; the overlap-coalescence argument (union of overlapping contiguous sets in I(β_k)'s ordinal sequence is contiguous) is explicit. (⇐) constructs m fragments per block from m pairwise non-adjacent non-overlapping terms.

**Frame and L-frame analysis.** Verified every K.* transition in ASN-0047: K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ are L-frame; K.λ is the unique L-extending transition; K.μ~ is L-frame as composite of L-frame elementaries. SV7's invariance and SV9's monotonicity follow.

**NewLinkEvaluationDefinedness.** Four-step proof (link value defined, slot projection defined via L3, coverage defined via L4/T12, M(d) defined via K.λ frame) is complete and each step has a single citation.

**SV14(d) witness.** K.λ allocates a' with F' = {(a₃, a₄ ⊖ a₃)} (D0 discharged via sibling structure, reach = a₄ by D1, coverage = [a₃, a₄)). At Σ_int post-K.μ~, a₃ ∈ ran(M_int(d)) so a' is discovered through d. Post-K.μ⁻, the remaining {a₁, a₂, a₄, a₅} are all outside [a₃, a₄), so a' exits — strict shrinkage realised.

**Architectural remark on NoStaleResolutionState.** Per-transition check that no K.* writes a V-address into Σ.L holds by direct inspection of each transition's effect.

## REVISE

(none)

## OUT_OF_SCOPE

(none — the ASN's deferrals are explicit and correct: broader-level spans (k ≤ p₃) deferred to ASN-0034; link-subspace projection contribution and reflexive-addressing analysis deferred to the Link Subspace ASN; same-origin coverage growth properly identified as architectural rather than a formal SV claim; type semantics and BEBE explicitly out of scope per the front matter)

VERDICT: CONVERGED
