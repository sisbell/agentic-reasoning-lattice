# Review of ASN-0063

## REVISE

### Issue 1: Text-subspace precondition for V-spans does not prevent subspace crossing

**ASN-0063, CL1/CL2/CREATELINK precondition**: "every V-span lies in the text subspace: `subspace(start(σ)) = s_C`"

**Problem**: The formal precondition constrains only the start of the span, not its extent. A V-span with width action point at position 1 produces a reach whose first component differs from the start's. Concretely: σ = ([s_C, k], [1, 5]) satisfies T12 (action point 1 ≤ 2 = #start), and reach = [s_C + 1, 5] = [s_L, 5]. The denotation ⟦σ⟧ includes depth-2 tumblers [s_L, j] for j < 5 — link-subspace V-positions. If any are in dom(M(d)), their images M(d)(v) ∈ dom(L) (by S3★) fall in no text-subspace block. CL1's proof routes every element of `image(d, Ψ)` through exactly one text-subspace block (via B1/B2, ASN-0058), so these link-subspace images are uncovered. CL2 (`image ⊆ coverage(resolve)`) fails for such inputs.

The ASN itself identifies this dependency in prose: "a V-span crossing into the link subspace would contribute positions falling in no text-subspace block, leaving their images uncovered." The formal precondition does not enforce what the prose requires.

**Required**: Add a width constraint to the precondition in CL1, CL2, and CREATELINK. The cleanest formulation: require `(w_v)₁ = 0` for each V-span width `w_v` (equivalently, the action point satisfies k ≥ 2). By TumblerAdd, when the action point exceeds position 1, the result's first component equals the start's first component — so `subspace(reach(σ)) = subspace(start(σ)) = s_C`, confining the span to the text subspace. This aligns with TA7a's element-local displacement convention where the subspace identifier is structural context, not an arithmetic operand. No practical use case is excluded: content selections use ordinal displacements (action point at depth m ≥ 2), which already satisfy this constraint.

## OUT_OF_SCOPE

### Topic 1: Fork semantics for the link subspace

With K.μ⁺ amended to content-subspace only, the fork composite (J4, ASN-0047) — which populates M'(d\_new) via K.μ⁺ — cannot copy link-subspace V-positions. A forked document inherits content arrangements but starts with an empty link subspace. Whether this is intended, and whether a fork-specific mechanism should replicate or reference the source document's link arrangement, is a version-semantics question.

**Why out of scope**: CREATELINK defines link creation; fork behavior follows from J4's existing definition and the K.μ⁺ amendment as a consequence, not an error in this ASN.

### Topic 2: Two-subspace completeness of S3★

S3★ handles exactly two subspaces (s\_C → dom(C), s\_L → dom(L)) and is silent on V-positions with subspace(v) ∉ {s\_C, s\_L}. No defined transition creates such positions, so the gap is currently harmless but would need resolution if a third subspace is introduced.

**Why out of scope**: The current framework has exactly two subspaces; extending S3★ is preemptive until a concrete third subspace is defined.

VERDICT: REVISE
