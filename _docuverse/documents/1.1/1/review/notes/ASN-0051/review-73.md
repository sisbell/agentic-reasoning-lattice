# Review of ASN-0051

## REVISE

### Issue 1: SV5 proof reads to "composite endpoints" but worked example treats K.μ~ steps atomically without traceable intermediate verification

**ASN-0051, SV5 + Worked Example Step 1**: The SV5 proof relies on "K.μ~'s ran-preservation corollary" read "at the composite endpoints Σ and Σ' bracketing the full K.μ~ composite." The Worked Example then exhibits Step 1 as "K.μ~" producing M_reord(d), with the K.μ⁻+K.μ⁺ expansion's intermediate state never named, and the K.μ⁻ stage's D-SEQ admissibility checked against the upward-tail-of-V_{s_C}(d) condition "rooted at v₂" without showing why v₂ (not some other cut) is the admissible cut.

**Problem**: Two related issues. (i) The Worked Example's K.μ~ Step 1 implicitly chooses a cut position (v₂) for its K.μ⁻ stage but the rationale is implicit — the reader cannot verify D-SEQ admissibility without deriving the cut from the bijection ψ themselves. (ii) The "Reordering that changes locate" subsection's K.μ~ uses cut n'=0 (full V_{s_C}(d) removal), which is explicitly noted; the parallel admissibility check in the original Step 1 is more compressed.

**Required**: For each K.μ~ instance in the Worked Example, state the K.μ⁻ cut position n' explicitly and derive it from the bijection's altered V↦I assignments (the minimal upward-tail covering ψ's altered positions).

### Issue 2: SV11 m·p attainment biconditional - "no two non-empty terms within a block ordinally adjacent or overlap" needs sharper statement

**ASN-0051, SV11 biconditional**: "the bound m · p is attained iff every (j, k) pair yields a non-empty decomposition term *and* these terms are pairwise non-adjacent and non-overlapping within each block."

**Problem**: The condition "pairwise non-adjacent and non-overlapping within each block" is correct but slightly imprecise about pairwise-vs-collection. Specifically, in the disjoint-pair non-attainment case (b) m=2 disjoint singletons subcase, the proof argues that span 1's β_{k₁}-contribution at offsets [..., i] and span 2's at offsets [i+1, ...] coalesce by mechanism (b) — but this requires understanding that "ordinally adjacent" means "the max offset of one equals min offset of other minus one" (gap = 0), not the strict "share a boundary point" reading. The biconditional's "pairwise non-adjacent" requires gap ≥ 1 between every pair within each block.

**Required**: Add to the biconditional statement: "non-adjacent means the offset ranges of the two terms within a single block are separated by at least one offset, i.e., gap ≥ 1; non-overlapping means the offset ranges are disjoint."

### Issue 3: SV6's case-(ii) of T4-validity check for t at boundary (k-1, k)

**ASN-0051, SV6 proof, T4-validity case (ii)**: "Case (ii) — k > p₃ + 1. Position k − 1 lies strictly between p₃ and k, i.e., k − 1 > p₃. The three field-separator positions p₁, p₂, p₃ of t are all ≤ p₃ < k − 1, so position k − 1 is not one of them; by the element-level zero-confinement, t_{k−1} ≠ 0."

**Problem**: The argument is correct but the "element-level zero-confinement" — established earlier as "the three zeros of element-level t sit exactly at p₁, p₂, p₃ ≤ k − 1" — only confines zeros within positions 1..k-1. For position k-1 specifically (which is in 1..k-1), the confinement says t_{k-1} could be one of p₁, p₂, p₃ (and hence zero) only if k-1 ∈ {p₁, p₂, p₃}. Since k-1 > p₃ in case (ii), this is impossible. The argument is right but could be clearer.

**Required**: Reword to: "Since p₁ < p₂ < p₃ < k−1 in case (ii), position k−1 is not among the three zero positions, hence t_{k-1} ≠ 0."

### Issue 4: SV11 (m = 1, p ≥ 4) recipe size-≥3 invariant bound

**ASN-0051, SV11 (m = 1, p ≥ 4) construction**: "The size-≥3 invariant required before step i — i.e., that the main block be at least size 3 before being excised — holds iff 2p + 1 − 2(i − 1) ≥ 3, i.e., i ≤ p; the invariant therefore holds through step p − 1 inclusive."

**Problem**: The algebraic conclusion is correct (i ≤ p) but the phrasing "holds through step p − 1 inclusive" is potentially misleading. The invariant holds for i = 1, ..., p (per i ≤ p), but we only need it for i = 1, ..., p−1 (since we do p−1 excisions). Stating "holds through step p − 1 inclusive" obscures that the invariant has one more degree of slack than required.

**Required**: Replace with: "The bound i ≤ p ensures the invariant holds for every excision step i = 1, ..., p−1; the construction therefore terminates after p−1 excisions yielding p blocks."

### Issue 5: SV13(e) bullet on K.μ~ - "composite-level" π-invariance vs locate-set non-preservation needs clearer separation

**ASN-0051, SV13(e)**: The bullet on K.μ~ states "Reordering of M(d) — via the *distinguished composite* K.μ~... — preserves π(e, d) exactly *at the composite endpoints* (pre-state Σ and post-state Σ' bracketing the full K.μ~ composite), but not pointwise across the composite's elementary stages..."

**Problem**: The parenthetical "but not pointwise across the composite's elementary stages" is correct but is conflated in the bullet with the locate transformation discussion that follows. A reader could miss that per-step π is genuinely not invariant (it shrinks at K.μ⁻ stage and recovers at K.μ⁺ stage) and the only claim is at composite endpoints.

**Required**: Either: (a) split the bullet into two sub-bullets (one for π at endpoints; one for locate transformation via ψ); or (b) explicitly say that the SV5 composite-level scope discussion's account of the intermediate state applies here.

### Issue 6: ASN length and SV11 witness proof exhaustiveness

**ASN-0051, SV11 attainment section**: The witness verification spans many pages, with five attainment regions, four lift schemata ((α), (β), (α_2), (β_2)), and detailed parameter-change recipes.

**Problem**: While rigor is appropriate, the inductive lift framing's "the inductive step is the lift body" is asserted without consolidating the structural verifications into a single lemma form. The (α_2) and (β_2) boundary lifts are described as "the (α)/(β) recipe instantiated at p = 2/m = 2 with the appropriate base-shape relabelling" — but the relabeling is implicit, requiring careful re-reading of the W(m, p) shape description.

**Required**: Add a single explicit lemma form for the lifts: "Lift L: For W(m, p) satisfying the SV11 attainment biconditional with block sizes (n_1, ..., n_p) and m single-element spans, L produces W(m', p') with parameters (m + 1, p) [under (α)/(α_2)] or (m, p + 1) [under (β)/(β_2)] by [explicit parameter delta]. Preservation of the biconditional follows because [single sentence]."

### Issue 7: Worked Example V-positions unspecified

**ASN-0051, Worked Example, Setup**: "v₁ < v₂ < v₃ < v₄ < v₅" with no explicit tumbler form.

**Problem**: Per S8a (ASN-0036), V-positions in dom(M(d)) must satisfy zeros(v) = 0, #v ≥ 2, and componentwise positivity. The Worked Example uses v₁, ..., v₅ as abstract symbols without specifying they are e.g. [s_C, 1], [s_C, 2], etc. of depth m_C = 2. The downstream K.μ⁻ admissibility (D-SEQ upward-tail removal) and D-MIN checks need to be verifiable against the actual V-position values.

**Required**: State the V-positions explicitly as [s_C, 1], [s_C, 2], [s_C, 3], [s_C, 4], [s_C, 5] (depth 2 in content subspace s_C), or note explicitly that the values are determined by the standard D-MIN form for V_{s_C}(d).

### Issue 8: Withdrawn-labels (SV0, SV1, SV12) provenance

**ASN-0051, Properties Introduced**: "SV0, SV1, and SV12 were used in earlier drafts and have been withdrawn during revision..."

**Problem**: The withdrawal note is appropriate for revision history but makes the SV-label sequence non-contiguous. Readers consulting downstream cross-references may wonder why SV0/SV1/SV12 are missing. The framing "the labels are not reused; the surviving SV labels retain their historical numbering" is correct but obscures whether the *withdrawn content* was incorrect or merely re-organized.

**Required**: Add one sentence clarifying that the withdrawn SV0/SV1 content is now in the NoStaleResolutionState architectural remark, and SV12's content is now in SV7. The current text says this but distributed across multiple sentences; consolidation would help.

### Issue 9: SV11's "term cardinality inflation" identity is witness-specific but the scope of that witness-specificity could be sharper

**ASN-0051, SV11 worked example attribution**: "*Scope of the witness-specific separation.* The clean independence here — mechanism (b) acting per-block on within-block fragment count, non-injective sharing acting on term-cardinality inflation — is a feature of *this* (B, e), not a general separation theorem."

**Problem**: The structural identity `Σ_{j,k} |term_{j,k}| − |π_text(e, d)| = Σ_{a ∈ π_text(e, d)} (s_a · m_a − 1)` is stated as a general fact, but the witness-specific reduction (s_a = 1 for every a) makes it look like a witness fact rather than a general identity. A reader could miss that the structural identity is general but only the *clean separation* is witness-specific.

**Required**: Add a sentence: "The structural identity itself holds for every (B, e) by the same counting argument (each a ∈ π_text appears in exactly s_a · m_a decomposition terms by definition of term)."

## OUT_OF_SCOPE

### Topic 1: Broader-level span survivability (action point k ≤ p₃)

**Why out of scope**: SV6 explicitly scopes itself to element-level spans with k > p₃. Broader-level spans (server, account, document) are admitted by L4 but require allocator-discipline analysis at the prefix-region level, deferred to ASN-0034.

### Topic 2: Link-subspace projection contributions

**Why out of scope**: SV11's π_text restricts to content-subspace projection. The full π may include link-subspace contributions via K.μ⁺_L; treatment is deferred to the Link Subspace ASN. The parenthetical after SV11 makes this explicit.

### Topic 3: Higher-arity links (|Σ.L(a)| > 3)

**Why out of scope**: The ASN's scoping note in the Endset Projection section restricts to the standard triple (F, G, Θ). L3 admits higher arity; generalization is deferred to ASN-0043.

### Topic 4: Bilateral vitality preservation across forking (J4 ForkComposite)

**Why out of scope**: The Open Questions section explicitly identifies this; SV13(h) treats bilateral vitality under elementary transitions and K.μ~, not composites like J4.

### Topic 5: Discovery latency and eventual consistency

**Why out of scope**: Identified in Open Questions; out of scope for a state-survivability specification.

VERDICT: REVISE
