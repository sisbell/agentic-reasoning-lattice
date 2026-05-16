# Review of ASN-0051

## REVISE

### Issue 1: Schema Lemma's status as "schema observation, not derivation" is structurally anomalous

**ASN-0051, "Endset Projection" section, Schema Lemma (NoStaleResolutionState)**: The lemma is explicitly framed as "not given an SV label because the content is structural inspection of the schema rather than a transition-induced survivability claim... it is not a derivation; it is an inspection of what (i)–(iii) make available."

**Problem**: The lemma's substantive architectural content — that V-position caching is structurally precluded by the state schema — is load-bearing for the survivability story but unaddressable by downstream consumers who cannot cite "SV-x". It sits in an inspection/lemma limbo. If the content is a structural property, it can be stated as a numbered invariant (e.g., the conditional `Σ₁.M(d) = Σ₂.M(d) ⟹ locate_{Σ₁}(e, d) = locate_{Σ₂}(e, d)` plus a one-line schema closure clause). If it is merely commentary, it should not be styled as a Lemma.

**Required**: Either promote to an SV-labelled invariant (with the conditional as the formal content) or demote to an in-prose architectural remark without the "Schema Lemma" framing.

### Issue 2: Bilateral vitality rationale is underspecified

**ASN-0051, "Endset Projection" section, Bilateral Vitality definition**: "We exclude the type endset from the vitality condition because type endsets may reference addresses outside dom(Σ.C), per L9, TypeGhostPermission."

**Problem**: L4 (EndsetGenerality) permits *any* endset — including F and G — to reference ghost addresses, so "may reference addresses outside dom(C)" is not what distinguishes Θ from F/G. The actual distinction is semantic (Θ is a type annotation, not an endpoint to which the link "connects" content), but the rationale as written invokes a structural property that doesn't separate the cases.

**Required**: Sharpen to "type endsets are *designed* to reference type definitions which may be ghosts (L9), whereas content endsets are *endpoints* whose visibility constitutes the link's utility" — or equivalent. The current wording leaves a reader wondering whether a content endset with ghost-only coverage should also be excluded.

### Issue 3: SV13 (e) for K.μ~ overstates locate-set behavior

**ASN-0051, SV13 (e)**: "Reordering of M(d) preserves π(e, d); locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)} where ψ is the reordering bijection from K.μ~. The locate *set* may change."

**Problem**: The synthesis line drops the K.μ~-FIX consequence that ψ is a permutation of a *fixed* domain (dom(M'(d)) = dom(M(d)) per ASN-0047). Without this, a reader may infer that locate can move "outside" the original domain. The image {ψ(v) : v ∈ locate_Σ(e, d)} is always a subset of dom(M(d)) — the set changes via permutation, not via domain shift.

**Required**: One additional clause in SV13 (e) noting ψ acts on a fixed domain (K.μ~-FIX), so the locate set permutes within dom(M(d)) rather than relocating.

### Issue 4: Discovery-resolution worked example for SV10 has implicit coverage assumption

**ASN-0051, SV10 witness**: "Set Σ.M(d) = {v₁ ↦ i₂}, and let a ∈ dom(Σ.L) carry F = {(i₁, ℓ_span)} so coverage(F) ⊇ {i₁, i₂, i₃} ∋ i₂."

**Problem**: The witness sets `Σ.M(d) = {v₁ ↦ i₂}` but does not state whether v₁ satisfies S8a (which requires #v ≥ 2 and componentwise positivity). The single-V-position arrangement also requires D-MIN — v₁ = [1, 1, ..., 1] — to be a valid arrangement of a content subspace. As written, v₁ is just a symbol; an attentive reader cannot tell whether the witness state is actually reachable from Σ₀ via valid composite transitions.

**Required**: Either specify v₁ concretely (e.g., v₁ = [1, 1] at depth 2) and verify S8a/D-MIN, or assert state-reachability under the standing preconditions.

### Issue 5: SV11 fragment-count derivation under K.μ⁻ + K.μ~ composite is hand-waved

**ASN-0051, "Partial Survival" section, paragraph after SV11 derivation**: "The number of maximal fragments can grow through repeated edits: a composite operation (K.μ~ followed by K.μ⁻) that rearranges interior content to the maximum V-position and then removes it has the net effect of excising I-addresses from the interior of a contiguous endset region."

**Problem**: This describes how fragment count can grow but does not bound it. SV11 gives "at most m·p" for a single state. After repeated K.μ⁻ + K.μ~ edits, p grows (each excision adds a block boundary). The claim "the upper bound m · p (spans times blocks) still applies after the operation, with both the block count p and the maximal-fragment count potentially increased" is correct but the bound m·p is then trivially satisfied because p grows alongside the fragment count. The reader is not told the substantive constraint.

**Required**: Either (a) state explicitly that fragment count is bounded by current block count p, which itself is bounded by |dom(M(d))|, or (b) drop the growth-via-edits remark since SV11's bound is per-state and the composite-edit analysis doesn't refine it.

### Issue 6: The K.μ⁻ wp for vitality loss does not address content endsets with link-address coverage

**ASN-0051, "Weakest Precondition Analysis" section**: The wp values for K.μ⁻ are stated for π(e, d), where coverage(e) is implicitly content-subspace.

**Problem**: For endsets with coverage in dom(Σ.L) (per L13 reflexive addressing, or per L4 generality), K.μ⁻ on link-subspace V-positions can shrink ran(M(d)) ∩ dom(Σ.L), affecting π. The wp expression `(E v : v ∈ dom(Σ.M(d)) \ V_rm : Σ.M(d)(v) ∈ coverage(e))` is correct in form for any coverage, but the prose treatment is content-endset-centric and the link-subspace contraction case is not exercised in any example.

**Required**: One additional sentence noting that the wp form applies uniformly to content and link coverage, with link-subspace contractions affecting endsets whose coverage contains link addresses. Alternatively, defer explicitly as is done for SV2's strict-inclusion analysis.

## OUT_OF_SCOPE

### Topic 1: Same-origin coverage growth
**Why out of scope**: The ASN explicitly defers formal claims about which same-origin allocations enter which spans to ASN-0034's allocator-discipline treatment. The descriptive analysis (sequential overshoot, child-depth entry, byte-level closure under sibling discipline) and Gregory's implementation evidence are provided as motivation; a formal SV claim requires allocator-discipline conditions developed in the foundation.

### Topic 2: Broader-level spans (k ≤ p₃)
**Why out of scope**: SV6 restricts to k > p₃. Broader-level spans require prefix-region allocator discipline of a specific implementation, and udanax-green does not implement them. Formal treatment is deferred to ASN-0034.

### Topic 3: Link-subspace endsets and reflexive addressing
**Why out of scope**: Detailed analysis of link-referencing endsets via L13 is deferred to a future "Link Subspace ASN". SV2 correctly covers both K.μ⁺ and K.μ⁺_L; the strict-versus-reflexive inclusion analysis is the future ASN's territory.

### Topic 4: Bilateral vitality preservation across forks (J4)
**Why out of scope**: Listed in Open Questions. Requires composite-transition analysis specific to forking, beyond the elementary-transition scope of SV2–SV11.

VERDICT: REVISE
