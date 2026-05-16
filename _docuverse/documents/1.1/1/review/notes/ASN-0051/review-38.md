# Review of ASN-0051

## REVISE

### Issue 1: SV6 informal statement says "newly allocated" but formal precondition is purely structural

**ASN-0051, Section "Content Allocation and Coverage Stability"**: "**SV6 (CrossOriginExclusion).** For a span (s, ℓ) in an existing endset where s is element-level (zeros(s) = 3), and a newly allocated address b with zeros(b) = 3 and origin(b) ≠ origin(s)..."

**Problem**: The informal statement says "newly allocated address b," but the formal precondition list immediately below contains no allocation requirement — only `s, b ∈ T`, T4-validity, `zeros(s) = zeros(b) = 3`, `origin(b) ≠ origin(s)`, and `k > p₃`. The proof works for any T4-valid element-level b regardless of allocation status; SV6 is used downstream (in the cross-document decoupling corollary) on an allocated `j` precisely because allocation produces T4-valid element-level addresses, not because allocation is part of SV6 itself. A reader reasoning from the informal statement may believe SV6 is restricted to fresh allocations.

**Required**: Either remove "newly allocated" from the informal statement so it matches the structural precondition, or add an explanatory note that the structural form is the formal claim and "newly allocated" names the typical application context.

### Issue 2: SV6 proof asserts "p₃ ≥ 6" without derivation

**ASN-0051, Section "Content Allocation and Coverage Stability"** (SV6 proof): "since k > p₃ ≥ 6, so k ≥ 7 ≥ 2"

**Problem**: The bound `p₃ ≥ 6` is invoked but not derived. The derivation chains three T4 constraints — `t₁ ≠ 0 ⟹ p₁ ≥ 2`; no adjacent zeros ⟹ `p₂ ≥ p₁ + 2 ≥ 4`; no adjacent zeros ⟹ `p₃ ≥ p₂ + 2 ≥ 6` — and the chain is the load-bearing reason the field-separator positions are confined strictly before `k`, so the proof should make it explicit rather than treat it as common knowledge.

**Required**: Insert a one-line derivation: "(`p₃ ≥ 6` follows from T4-validity: `t₁ ≠ 0` gives `p₁ ≥ 2`, no adjacent zeros gives `p₂ ≥ 4` and `p₃ ≥ 6`.)"

### Issue 3: Properties table omits corollaries stated in the body

**ASN-0051, "Properties Introduced" table**: The table lists `ArrangementLinkFrame` and `ContentFidelity` as cited corollaries, but omits three corollaries that the body introduces and proves: `TransclusionCcouplingAbsence` (under SV7), `CrossDocumentDecoupling` (under SV10), and `NewLinkEvaluationDefinedness` (under SV13(e)).

**Problem**: The omitted corollaries carry substantive content — `CrossDocumentDecoupling` in particular has its own multi-step witness construction occupying several paragraphs. A reader scanning the table for the ASN's claim surface would miss them.

**Required**: Add rows for `TransclusionCouplingAbsence`, `CrossDocumentDecoupling`, and `NewLinkEvaluationDefinedness` with the same "Corollary of [parent]" status format used for `ArrangementLinkFrame` and `ContentFidelity`.

### Issue 4: Cross-document decoupling witness — V-position naming collision left implicit

**ASN-0051, Section "Discovery-Resolution Distinction"** (CrossDocumentDecoupling witness, Step 3): "Σ⁺.M(d₂) = {v₁ ↦ j}"

**Problem**: The symbol `v₁` was bound in the SV10 witness to `[s_C, 1]` as a V-position in `M(d₁)`. Step 3 reuses `v₁` as a V-position in `M(d₂)`. These are distinct V-positions in different document namespaces (V-positions are document-local), but the prose does not pause to note this — and immediately after the witness, the corollary's conclusion references `Σ⁺.M(d₁)` and `Σ⁺.M(d₂)` side-by-side. A careful reader has to reconstruct that `v₁` is namespace-shadowed by document.

**Required**: At the point of reuse, add one clause noting V-positions are document-local (e.g., "the `v₁ = [s_C, 1]` here is the D-MIN position of d₂'s content subspace, distinct from but co-named with d₁'s D-MIN").

## OUT_OF_SCOPE

The ASN's explicit scope decisions (broader-level spans, link-subspace contributions to π, higher-arity links, same-origin coverage growth, forking-bilateral-vitality, discovery latency) are all appropriately deferred to future ASNs or open questions. No additional out-of-scope items to flag.

VERDICT: REVISE
