# Review of ASN-0051

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Link creation operation (K.λ)
**Why out of scope**: ASN-0047 defines elementary transitions for (C, E, M, R) but has no transition for creating entries in Σ.L. ASN-0051 correctly depends only on L12/L12a (immutability and monotonicity of the link store), so the absence of K.λ doesn't affect any proof here. But a future foundation ASN should define link creation formally.

### Topic 2: Monotonicity of discover_s in its argument
**Why out of scope**: The property `A₁ ⊆ A₂ ⟹ discover_s(A₁) ⊆ discover_s(A₂)` is a useful lemma that would connect SV8/SV9 (permanence/monotonicity for fixed A) to the practical scenario where A = ran(M(d)) changes with the arrangement. The ASN notes the document-specific case in SV8's caveat and SV10's discussion, and the proof is immediate from the definition. A future ASN could state this as an explicit lemma.

### Topic 3: Link-subspace V-positions
**Why out of scope**: SV11 decomposes only π_text(e, d). The ASN correctly notes that no defined operation creates non-text V-positions, so π_text = π for all reachable states. The link-subspace contribution is deferred to a future ASN, as stated.

---

**Verification notes on the key proofs:**

**SV2/SV3 (Extension/Contraction monotonicity):** Both proofs are correct. K.μ⁺ preserves existing mappings (dom and values), giving ran(M'(d)) ⊇ ran(M(d)); K.μ⁻ restricts the domain while preserving values, giving ran(M'(d)) ⊆ ran(M(d)). The non-injectivity of M(d) (S5) means contraction removing a V-position v does not necessarily remove M(d)(v) from ran — another V-position may also map there. The proofs use only ⊆/⊇ on ranges, so this subtlety is correctly handled without explicit mention.

**SV5 (Reordering):** The proof correctly identifies ψ as the K.μ~ bijection, derives ran(M'(d)) = ran(M(d)) from the bijective structure, and establishes the resolve set transformation. The witness for resolve-set change is valid.

**SV6 (CrossOriginExclusion):** The sandwich argument is the critical step. I verified it for all tumbler-length cases: shorter tumblers cannot be in [s, s⊕ℓ) (they would fall below s); same-length and longer tumblers agree with s on positions 1..k−1 (divergence before k forces t > s⊕ℓ by T1, contradicting t < s⊕ℓ). Since k > p₃ places all three field separators within the agreement zone, every element-level t in the span shares origin(s). The precondition is correctly stated and the proof is sound.

**SV11 (Partial Survival):** The convexity argument is correct: S0 on ⟦(sⱼ, ℓⱼ)⟧ combined with TA-strict on ordinal increments ensures each intersection ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k) is a contiguous ordinal subsequence. The fragment bound m·p is valid. The distinction between fragments (finite sets from ordinal increment) and span denotations (half-open intervals including child-depth tumblers) is correctly drawn.

**SV13 (Synthesis):** All seven components cite the correct supporting properties. Elementary transitions are exhaustively covered: K.μ⁺ (SV2), K.μ⁻ (SV3), K.μ~ (SV5), cross-document isolation (SV4), and K.α/K.δ/K.ρ preserve M in their frames. The claim about byte-level coverage closure is correctly hedged as architectural, not formal.

**Worked example:** Verified all computed values. The post-contraction block structure, SV11 fragment decomposition, and SV5 bijection application are all correct.

VERDICT: CONVERGED
