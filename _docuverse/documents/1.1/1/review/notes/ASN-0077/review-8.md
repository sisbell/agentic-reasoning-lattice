# Review of ASN-0077

## REVISE

### Issue 1: O8 section title mismatched with claim content
**ASN-0077, "Span union monotonicity" section**: Section title says "Span union monotonicity" but Claim O8 states "For I-spans σ₁, σ₂ with ⟦σ₁⟧ ⊆ ⟦σ₂⟧: origins_I(Σ, σ₁) ⊆ origins_I(Σ, σ₂)."
**Problem**: The title suggests the property concerns unions of multiple spans, but the claim is about denotational *containment* of two spans. The mismatch is misleading. The prose immediately above the claim uses "set-inclusion" and "enlarging the span", confirming containment is the actual topic.
**Required**: Retitle the section "Span containment monotonicity" or "Span inclusion monotonicity" to match the claim's content.

### Issue 2: O1(c) wording conflates "document" with "allocator"
**ASN-0077, O1 (Origin partitions allocated content), conclusion (c)**: "each equivalence class consists exactly of those I-addresses in ⟦σ⟧ ∩ dom(C) allocated by one document — by S7d (DocumentAllocationDiscipline, ASN-0036), one allocator."
**Problem**: S7d establishes uniqueness of document-level tumblers per allocation event; it does not by itself identify "one allocator". The promotion from "one document" to "one allocator" requires SubAllocatorAxiom (each document has a unique A_C). The citation chain is incomplete.
**Required**: Either tighten the conclusion to "one document" (matching S7d's actual content), or augment the citation with SubAllocatorAxiom (a) to support the identification with the unique content sub-allocator A_C(d).

### Issue 3: V-span counterparts of O6 and O8 not derived
**ASN-0077, "Permanence" and "Span union monotonicity" sections**: The ASN derives I-span monotonic growth under state (O6) and I-span containment monotonicity (O8), but does not state the V-span counterparts as consequences.
**Problem**: V-span behaviour under K.μ⁺ extensions (monotonic growth of origins_V when new positions enter the span's range) and V-span containment monotonicity follow by reasoning parallel to O6/O8 — but the ASN leaves these as exercises. The worked example demonstrates K.μ⁻ inadmissibility but does not formally derive the K.μ⁺ growth case for origins_V. The standards require explicit consequences, not "by similar reasoning."
**Required**: State as additional numbered claims: (i) origins_V(Σ, d, σ) ⊆ origins_V(Σ', d, σ) under K.μ⁺ when σ remains admissible at Σ'; (ii) for well-formed V-spans σ_1, σ_2 with σ_1 ⊆ σ_2, origins_V(Σ, d, σ_1) ⊆ origins_V(Σ, d, σ_2). Brief derivations from O5 + S3★ + (F1) suffice.

## OUT_OF_SCOPE

### Topic 1: Cross-subspace I-span reporting of link origins
**Why out of scope**: Open Question 1 — the ASN deliberately restricts origins_I to dom(C). Extending to dom(C) ∪ dom(L) in the I-span case is a design choice for a future ASN.

### Topic 2: Surfacing intermediate transclusion chain
**Why out of scope**: Open Question 2 — chain-traversal operations are distinct from direct origin reporting.

### Topic 3: Distinguishing native from transcluded content
**Why out of scope**: Open Question 3 — a separate predicate or operation, not part of SHOWORIGIN's set-based result.

### Topic 4: Behaviour when home document is unreachable
**Why out of scope**: Open Question 4 — networking and reachability concerns are orthogonal to the abstract origin mechanism.

### Topic 5: Historical containment via Σ.R
**Why out of scope**: Open Question 5 — provenance reporting is distinct from current arrangement origins and belongs in a separate operation.

### Topic 6: Per-position attribution under intra-document sharing
**Why out of scope**: Open Question 6 — SHOWORIGIN's set-based result handles intra-document sharing naturally; per-position attribution is a different operation.

VERDICT: REVISE
