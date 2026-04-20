# Review of ASN-0074

## REVISE

### Issue 1: C0a proof has an unacknowledged sequential dependency

**ASN-0074, C0a — PrefixConfinement**: "Fix any j with 1 ≤ j < m and any t ∈ ⟦σ⟧ ... If tⱼ < uⱼ, then t < u by T1(i) at divergence point j ... If tⱼ > uⱼ = reach(σ)ⱼ, then t > reach(σ) by T1(i) at divergence point j ... The argument is uniform in j, applying identically at each component from 1 through m − 1."

**Problem**: Invoking "T1(i) at divergence point j" requires j to *be* the divergence point, which requires all components before j to agree: tᵢ = uᵢ for 1 ≤ i < j. This holds for j = 1 vacuously, but for j > 1 it depends on the lemma's own conclusion for smaller indices. The "fix any j" phrasing and "uniform in j" claim present the argument as independent per j, when it is actually sequential.

Concrete counterexample to the "independent" reading: if j = 3 and t₂ > u₂ (not yet ruled out), then the divergence of t and u is at position 2, not 3. The claim "t < u at divergence point 3" when t₃ < u₃ would be wrong — the divergence point is 2 and t > u.

**Required**: Either (a) restructure as an induction on j, noting the base case j = 1 and the inductive step using tᵢ = uᵢ for i < j, or (b) use a smallest-counterexample argument:

> Suppose J = {j : 1 ≤ j < m ∧ tⱼ ≠ uⱼ} is non-empty. Let j₀ = min(J). Then tᵢ = uᵢ for i < j₀, so the divergence of t and u is at j₀. Since u ≤ t, T1(i) gives t\_{j₀} > u\_{j₀}. Since reach(σ)\_{j₀} = u\_{j₀}, and tᵢ = uᵢ = reach(σ)ᵢ for i < j₀, the divergence of t and reach(σ) is also at j₀ with t\_{j₀} > reach(σ)\_{j₀}. By T1(i), t > reach(σ), contradicting t < reach(σ).

### Issue 2: w(resolve(d\_s, σ)) is a type mismatch in C2

**ASN-0074, Resolution section**: "The total width is: w(R) = (+ j : 1 ≤ j ≤ k : nⱼ) where ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ = resolve(R)."

**ASN-0074, C2**: "w(resolve(d\_s, σ)) = (+ j : 1 ≤ j ≤ k : nⱼ) = ℓₘ"

**Problem**: w is defined on content reference sequences (R is a ContentReferenceSequence). But resolve(d\_s, σ) is an I-address sequence ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩, not a reference sequence. The C2 statement applies w to the wrong type.

**Required**: Either (a) define w directly on I-address sequences — w(⟨(a₁, n₁), ..., (aₖ, nₖ)⟩) = Σnⱼ — with the reference-sequence form as a derived convenience, or (b) state C2 without w: "For a well-formed content reference (d\_s, σ) with σ = (u, δ(ℓₘ, m)), let ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ = resolve(d\_s, σ). Then (+ j : 1 ≤ j ≤ k : nⱼ) = ℓₘ."

## OUT_OF_SCOPE

### Topic 1: Resolution interaction with edit operations
**Why out of scope**: How resolved I-address sequences feed into INSERT, COPY, or other arrangement-modifying operations is the subject of future operation ASNs. This ASN correctly defines the read-side mechanism (content reference + resolution) without prescribing write-side semantics.

### Topic 2: I-address overlap in composite resolution
**Why out of scope**: A ContentReferenceSequence may yield duplicate I-addresses (same content transcluded via different source documents, or via overlapping spans of the same document). Whether duplicates are intentional (faithful to transclusion multiplicity) or require deduplication depends on the consuming operation. This ASN correctly preserves the raw resolution without making that decision.

VERDICT: REVISE
