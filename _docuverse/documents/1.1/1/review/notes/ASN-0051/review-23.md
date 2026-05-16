# Review of ASN-0051

The ASN delivers a coherent survivability theory: it cleanly separates discovery from resolution, handles boundary cases (empty endsets, asymmetric absence) explicitly, provides a worked example with concrete tumblers that verifies the main claims, and structures partial survival through the m·p decomposition. The proofs of SV2-SV10 are short but correct. The SV6 cross-origin proof works through the sandwich argument carefully, and the worked example's tumbler values check out. I found two correctness issues, both fixable.

## REVISE

### Issue 1: SV11 — incorrect foundation citation for ordinal monotonicity
**ASN-0051, SV11 proof**: "For ordinal indices j₁ < j₂ < j₃ with a_k + j₁ and a_k + j₃ both in ⟦(sⱼ, ℓⱼ)⟧, we have a_k + j₁ < a_k + j₂ < a_k + j₃ (by TA-strict), so by the convexity of the span (S0), a_k + j₂ ∈ ⟦(sⱼ, ℓⱼ)⟧."

**Problem**: TA-strict (StrictIncrease, ASN-0034) establishes `a ⊕ w > a` under specific preconditions — it does not directly establish strict monotonicity of ordinal shifts in the shift amount. The property the proof actually needs — that shift(a_k, j₁) < shift(a_k, j₂) when j₁ < j₂ — is M1 (OrderPreservation, ASN-0058), which states "for 0 ≤ j < k < n: v + j < v + k ∧ a + j < a + k" within a mapping block. TS5 (ShiftAmountMonotonicity, ASN-0034) covers the j₁, j₂ ≥ 1 case. The current citation requires the reader to construct an intermediate bridge (a_k + j₁ ⊕ δ(j₂ − j₁, m) = a_k + j₂ via TS3, then TA-strict) that the proof does not provide.

**Required**: Replace "by TA-strict" with "by M1 (OrderPreservation, ASN-0058)" — M1 is the direct source, and the mapping-block context matches.

### Issue 2: SV0 — set notation error
**ASN-0051, SV0 statement**: "For every state Σ, endset e, and document d ∈ dom(Σ.E_doc):"

**Problem**: Σ.E_doc is defined in ASN-0047 as a set (the subset of E containing documents), not a function. `dom()` applied to a set is undefined notation.

**Required**: Replace `d ∈ dom(Σ.E_doc)` with `d ∈ Σ.E_doc`.

## OUT_OF_SCOPE

### Topic 1: Detailed link-subspace projection
**Why out of scope**: SV11 explicitly decomposes π_text only; link-referencing endsets, reflexive addressing (L13), and the link-subspace contribution to projection are deferred to the Link Subspace ASN.

### Topic 2: Same-origin coverage growth formalization
**Why out of scope**: The "Content Allocation and Coverage Stability" section correctly identifies that the architectural resolution depends on allocation regimes — byte-level sequential allocation vs. broader-level hierarchical openness. Conversion to formal claims is appropriately deferred since these are implementation-regime properties, not foundation-level invariants.

### Topic 3: Fork-specific survivability analysis
**Why out of scope**: Mentioned in SV7 discussion; detailed analysis listed as open question.

### Topic 4: Within-document-sharing resolution semantics
**Why out of scope**: SV5's witness illustrates non-injective M(d), and SV11 notes the cover-not-partition consequence. Specific resolution behavior for multiply-occurring I-addresses is listed as open question.

### Topic 5: Discovery latency, fragment ordering bounds, dormant link revival, link-home/vitality relationship
**Why out of scope**: All listed as open questions appropriate for future ASNs.

VERDICT: REVISE
