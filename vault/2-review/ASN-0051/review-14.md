# Review of ASN-0051

## REVISE

### Issue 1: SV11 ran_text guard includes link-subspace V-positions
**ASN-0051, SV11**: "ran_text(M(d)) = {M(d)(v) : v ∈ dom(M(d)) ∧ v₁ ≥ 1} = ⋃_k I(β_k)"
**Problem**: In the extended state (ASN-0047), link-subspace V-positions have `v₁ = s_L ≥ 1`, so the guard `v₁ ≥ 1` includes them. The set `{M(d)(v) : v₁ ≥ 1}` is `ran(M(d))` — the full range, not the text-subspace range. But `⋃_k I(β_k)` covers only text-subspace positions (ASN-0058's block decomposition is defined for "the text-subspace arrangement"). The two sides of the equation are not equal when the link subspace is non-empty. The parenthetical "(B1 guards v₁ ≥ 1)" inherits this ambiguity from ASN-0058, where `v₁ ≥ 1` was synonymous with "text subspace" before the link subspace existed.
**Required**: Define `ran_text(M(d)) = {M(d)(v) : v ∈ dom(M(d)) ∧ subspace(v) = s_C}`. This matches the block decomposition's scope and excludes link-subspace contributions as intended.

### Issue 2: SV13(g) does not specify text-subspace restriction
**ASN-0051, SV13(g)**: "Partial survival is well-structured: the surviving projection in any document decomposes into finitely many ordinal-contiguous fragments within mapping blocks. [SV11]"
**Problem**: SV11 explicitly restricts to `π_text(e, d)` and notes that the link-subspace contribution is deferred. SV13(g) says "the surviving projection" without qualification, which reads as the full `π(e, d)`. A reader of SV13 alone would conclude the fragment decomposition covers all of `π(e, d)`, which it does not.
**Required**: State "the text-subspace projection" in SV13(g) to match SV11's scope.

### Issue 3: SV6 proof omits short-tumbler elimination
**ASN-0051, SV6 proof**: "We claim t agrees with s on all positions 1 through k−1. For suppose t diverges from s at position j < k..."
**Problem**: The proof establishes that no divergence before position k exists, then concludes agreement on positions 1 through k−1. This conclusion requires `#t ≥ k − 1`, which is never shown. The argument works — if `#t < #s` and t agrees with s on all shared positions, t is a proper prefix of s, giving `t < s` by T1(ii), contradicting `s ≤ t`; if t disagrees at some `j ≤ #t < k`, then `tⱼ > sⱼ = (s ⊕ ℓ)ⱼ` gives `t > s ⊕ ℓ`, contradiction — but neither case is stated.
**Required**: Add one sentence establishing `#t ≥ #s ≥ k` for all `t ∈ ⟦(s, ℓ)⟧`: if `#t < #s`, agreement on shared positions makes t a prefix of s (T1(ii) gives `t < s`, contradicting `s ≤ t`), and disagreement at `j < k` gives `t > s ⊕ ℓ`.

### Issue 4: Endset Fragment definition depends on choice of block decomposition
**ASN-0051, Endset Fragment definition**: "For an endset e and document d with block decomposition B = {β₁, ..., β_p} of M(d), a *fragment* of e in d is a maximal contiguous subsequence of I-addresses within a single mapping block's ordinal sequence."
**Problem**: The fragment definition uses an unspecified block decomposition B. If two V-adjacent, I-adjacent blocks β₁ and β₂ in a non-maximally-merged decomposition share a contiguous run of endset I-addresses across their boundary, the definition counts two fragments; in the maximally merged decomposition, the merged block yields one. The fragment count and identity are not canonical. The m·p bound is valid for any decomposition but loose for non-canonical ones.
**Required**: Specify "the canonical (maximally merged) block decomposition" (M11, M12, ASN-0058) in the definition. This makes fragments canonical and gives the tightest bound.

## OUT_OF_SCOPE

### Topic 1: Same-origin coverage closure at the byte level
**Why out of scope**: The ASN correctly identifies that byte-level spans are architecturally closed to future allocations under sequential sibling increment, but notes "the byte-level closure follows from allocation discipline assumptions not formalised in this ASN." Formalizing allocation discipline (e.g., that text I-address allocation uses sibling increment exclusively within a document) is a separate specification concern — it constrains the allocator, not the survivability properties.

### Topic 2: Link-subspace contribution to projection
**Why out of scope**: The ASN explicitly defers this: "The link-subspace contribution to projection — including links whose endsets reference other link addresses — is deferred to the Link Subspace ASN." This is a genuine deferred topic, not a gap in the current analysis.

VERDICT: REVISE
