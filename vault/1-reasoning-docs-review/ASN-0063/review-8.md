# Review of ASN-0063

## REVISE

### Issue 1: CL1 and CL2 are stated for arbitrary V-span-sets but proven only for text-subspace V-spans

**ASN-0063, Endset Resolution**: "**Lemma CL1 — ResolutionExistence.** For any document d with M(d) satisfying the arrangement invariants (S2, S8-fin, ASN-0036) and **any V-span-set Ψ**, there exists an endset E ∈ Endset with image(d, Ψ) ⊆ coverage(E)."

**Problem**: CL0 has an implicit text-subspace precondition ("σ_v a V-span in the same subspace" as the mapping block β, which comes from the text-subspace block decomposition of ASN-0058). CL1's proof applies CL0 over these text-subspace blocks. If Ψ contains a V-span whose denotation extends into the link subspace — possible when the width has action point less than depth, e.g. σ = ([1, 1], [1, 3]) with reach [2, 3] crossing from s_C = 1 to s_L = 2 — then link-subspace V-positions in dom(M(d)) contribute to `image(d, Ψ)` but fall in no text-subspace block. No CL0 I-span covers them. CL2 (`image(d, Ψ) ⊆ coverage(resolve(d, Ψ))`) fails for these contributions.

The VSpanImage definition (`{M(d)(v) : v ∈ ⟦σ_v⟧ ∩ dom(M(d))}`) is unrestricted across subspaces. The resolve function collects CL0 I-spans from the text-subspace canonical decomposition only. The gap between the general definition and the restricted proof invalidates CL1 and CL2 as stated.

**Required**: Either (a) add a precondition to CL1/CL2 and CREATELINK restricting V-spans to the text subspace (`subspace(start(σ)) = s_C` for each σ ∈ Ψ), or (b) scope VSpanImage to text-subspace V-positions: `image(d, σ_v) = {M(d)(v) : v ∈ ⟦σ_v⟧ ∩ dom(M(d)) ∧ subspace(v) = s_C}`. Option (a) is cleaner — users needing to reference link addresses can use the direct I-span-set form, which the ASN already supports. The CREATELINK precondition "Every V-span in each endset specification satisfies T12" should gain the subspace clause.

### Issue 2: K.μ~ preservation of S3★ relies on a circular argument

**ASN-0063, Extending the Transition Framework**: "First, S3★ forces π to map link-subspace positions to link-subspace positions: if v ∈ dom_L(M(d)) then M(d)(v) ∈ dom(L), and M'(d)(π(v)) = M(d)(v) ∈ dom(L), so subspace(π(v)) = s_L **by S3★** (a content-subspace position mapping to dom(L) would violate the content clause)."

**Problem**: The argument uses S3★ in the final state M'(d) to establish that π preserves subspaces, then uses subspace preservation to run the cardinality argument, then concludes S3★ holds. The logical structure is: assume S3★ for M'(d) → derive subspace preservation of π → derive link-subspace fixity → conclude S3★ for M'(d). This is circular — the conclusion is used as a premise.

The conclusion is correct: S3★ is preserved by K.μ~ and can be proven independently by decomposition. After K.μ⁻, S3★ holds because dom(M_int(d)) ⊆ dom(M(d)) with values unchanged — content-subspace mappings still target dom(C), link-subspace mappings still target dom(L). After K.μ⁺ (amended), new positions have subspace s_C and target dom(C) (precondition); existing mappings are preserved (frame). S3★ holds at M'(d) without consulting π.

**Required**: Restructure the argument into two steps: (1) prove S3★ preservation for K.μ~ by direct decomposition (K.μ⁻ preserves by restriction of a valid arrangement, K.μ⁺ preserves by amendment and precondition — two sentences, no bijection needed); (2) then use S3★ as established to derive the stronger claim that π preserves subspaces, run the cardinality argument, and conclude link-subspace fixity. The current text interleaves these steps, producing a logically circular proof of S3★.

## OUT_OF_SCOPE

### Topic 1: Fork interaction with the K.μ⁺ amendment
**Why out of scope**: The K.μ⁺ content-subspace restriction introduced here means fork (K.δ + K.μ⁺ + K.ρ, ASN-0047) can only copy text-subspace positions — forked documents do not inherit link-subspace mappings. This is a consequence of the amendment that warrants documentation in a versioning or fork ASN, not a defect in CREATELINK.

### Topic 2: K.μ⁺_L applied to non-home documents
**Why out of scope**: K.μ⁺_L's precondition requires d ∈ E_doc and ℓ ∈ dom(L) but does not require origin(ℓ) = d. A document could arrange another document's link in its link subspace (analogous to content transclusion). Whether this is architecturally intended, and what invariants it should satisfy, is a question for a link-subspace management ASN.

VERDICT: REVISE
