# Review of ASN-0098

## REVISE

### Issue 1: LP20 claim incorrect in extended state
**ASN-0098, LP20 — RangeConfinement**: "For every endset e, document d, state Σ: `{Σ.M(d)(v) : v ∈ project(e, d, Σ)} ⊆ coverage(e) ∩ dom(Σ.C)`"
**Problem**: This is wrong in the extended state. S3★ (ASN-0047) permits V-positions in subspace s_L to map into `dom(Σ.L)`, not `dom(Σ.C)`. An endset whose coverage includes link addresses (admitted by L4(c) of ASN-0043) and a document arranging those addresses via s_L V-positions yields a projection whose image lies in `dom(Σ.L)`. The proof itself contradicts the claim by appealing to L14 for link-subspace V-positions but still states the conclusion as `∩ dom(Σ.C)`.
**Required**: Restate as `⊆ coverage(e) ∩ (dom(Σ.C) ∪ dom(Σ.L))`, or split by subspace into two cases.

### Issue 2: Worked trace uses K.μ⁻ inconsistently with its definition
**ASN-0098, "A Worked Trace"**: "Apply K.μ⁻ removing v₃ from d₁'s arrangement, producing state Σ_1: Σ_1.M(d₁) = {v₁ ↦ i₁, v₂ ↦ i₂, v₄ ↦ i₄}"
**Problem**: K.μ⁻ in ASN-0047 only supports per-subspace prefix retention: `M'(d) = M(d) ↾ R` where `R := ∪_S {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}`. Removing a single middle position v₃ while retaining v₄ is not an admissible K.μ⁻ effect — it leaves a non-contiguous arrangement violating D-CTG★ and D-SEQ★.
**Required**: Either reconstruct the trace using K.μ~ followed by K.μ⁻, or pick a removal scenario consistent with K.μ⁻'s prefix-retention semantics (e.g., remove v₄ as the last position).

### Issue 3: K.μ⁺_L not addressed in K.μ family analysis
**ASN-0098, LP5**: "Every operation in the K.μ family (K.μ⁺, K.μ⁻, K.μ~) has frame `(A d' : d' ≠ d : M'(d') = M(d'))`"
**Problem**: ASN-0047 introduces K.μ⁺_L (link-subspace arrangement extension) as a distinct operation; ASN-0047's K.μ⁺ is amended to a content-subspace restriction only. The ASN omits K.μ⁺_L entirely. Since link arrangement entries affect ran(M(d)) just as content arrangement entries do, every claim about projection displacement under arrangement extension (LP9, LP12, LP16, LP18) needs to cover K.μ⁺_L explicitly.
**Required**: Add K.μ⁺_L to the operation enumeration and show that LP4–LP12 hold for it analogously.

### Issue 4: Coverage definition restated with malformed notation
**ASN-0098, "The Coverage of an Endset"**: "`coverage(e) = ⋃ {(s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ}}`"
**Problem**: The notation is syntactically incorrect — it reads as a set-builder where `{t ∈ T : s ≤ t < s ⊕ ℓ}` sits in the constraint position rather than the expression position. ASN-0043 already defines `coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})` in the foundation's three-part quantifier form.
**Required**: Cite ASN-0043's definition rather than restate; foundation definitions should be used directly per review standards.

### Issue 5: LP19 is either trivial or unsupported
**ASN-0098, LP19 — BoundaryInsertionExclusion**: "v_new ∉ project(e, d, Σ') unless a_new ∈ coverage(e) by structural inclusion"
**Problem**: As formally stated, the claim reduces to "if a_new ∉ coverage(e), then v_new ∉ project(e, d, Σ')" — a direct restatement of project's definition, adding no content. The prose argues the "typical case" where freshly allocated addresses fall outside "tightly constructed" coverage, but tightness is not formalized and the formal claim doesn't capture it. The "by structural inclusion" qualifier acknowledges the gap without closing it.
**Required**: Either remove LP19 as redundant with LP9, or formalize a notion of "tight endset construction" and prove the stronger claim against it.

### Issue 6: LP18 proof miscites LP9
**ASN-0098, LP18 — Resurrection proof**: "By LP9, v ∈ project(a, i, d, Σ') since Σ'.M(d)(v) = a* ∈ coverage(eᵢ)."
**Problem**: LP9 establishes monotonicity for a single K.μ⁺ transition, but LP18's hypothesis is a sequence `Σ →* Σ'` which may include K.σ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~ in any combination. The conclusion `v ∈ project(a, i, d, Σ')` follows directly from project's definition once `Σ'.M(d)(v) ∈ coverage(eᵢ)` is given — LP9 is not the right citation.
**Required**: Replace the LP9 citation with direct invocation of project's definition, or strengthen LP9 to cover transition sequences via induction.

### Issue 7: LP18 cites wrong invariant for coverage permanence
**ASN-0098, LP18 — Resurrection proof**: "Because LP1 keeps the link's coverage fixed across the entire sequence..."
**Problem**: LP1 establishes `Σ'.L(a) = Σ.L(a)` (value persistence). Coverage invariance is LP3. The proof should cite LP3.
**Required**: Replace LP1 with LP3 in the citation.

### Issue 8: LP13 introduces informal vocabulary
**ASN-0098, LP13 — PartialSurvival**: "The link is *bidirectionally usable* from d when both `coverage(F) ∩ ran(Σ.M(d)) ≠ ∅` and `coverage(G) ∩ ran(Σ.M(d)) ≠ ∅`... *unidirectionally usable*... *type-only*..."
**Problem**: These terms are presented as definitions but are conditional on the link being a standard triple (a convention from L6's StandardTriple, not an invariant). They also have no follow-on use in any subsequent claim. Definitions that aren't used or aren't invariant should not be in a formal specification.
**Required**: Either remove the informal terms and let LP12 stand alone, or promote them to formal definitions conditioned on the standard-triple convention and exercise them in subsequent claims.

### Issue 9: LP1 restates L12 verbatim
**ASN-0098, LP1 — LinkValuePersistence**: The claim is identical (modulo state-component notation) to L12 of ASN-0043 (also restated as L12 in ASN-0093). The accompanying prose says "This is L12 of ASN-0043, restated."
**Problem**: Per review standards, ASNs should use foundation claims rather than reinvent or rename them. LP1 adds no content beyond L12 and creates citation ambiguity (does LP2's proof depend on L12 or LP1?).
**Required**: Remove LP1; have LP2's proof cite L12 directly. The "what stays fixed" narrative can be framed by reminding the reader of L12 in prose without elevating it to a new label.

### Issue 10: LP4 proof does not connect to coverage invariance
**ASN-0098, LP4 proof**: "The proof is immediate from the definition. If both inputs to the comparison agree pointwise (same domain, same mapping), then the set comprehension produces identical results."
**Problem**: project takes three inputs: e, d, Σ. The proof addresses M(d) being unchanged but doesn't note that coverage(e) is also unchanged (because e is the same on both sides of the equation — but this is a property of e, not of the transition). The argument is sound but the proof should be explicit about both inputs.
**Required**: Note that `coverage(e)` is a pure function of e, and e does not vary across the comparison; the projection depends on (coverage(e), M(d)) and both are pointwise equal.

### Issue 11: Empty-endset and empty-arrangement edge cases unaddressed
**ASN-0098, "The Projection Operation"** and surrounding claims
**Problem**: The ASN does not address: (i) `e = ∅` (the empty endset has `coverage(∅) = ∅`, so project is uniformly ∅); (ii) `dom(Σ.M(d)) = ∅` (empty arrangement, project is ∅); (iii) a link with only the mandatory type endset non-empty and from/to slots empty (allowed by L3, which only requires e₃ ≠ ∅). The behavior in each case is consistent with the definition but worth stating to confirm the projection framework handles degenerate cases.
**Required**: Add explicit edge-case claims, or at minimum a remark confirming uniform behavior in degenerate cases.

### Issue 12: LP14, LP15 are observations, not lemmas
**ASN-0098, LP14, LP15**: Each says discoverability is independent of home/origin because LP12 doesn't reference them.
**Problem**: These are tautologies — observations about the form of LP12's right-hand side. They state nothing that isn't visible by inspection of LP12. Promoting observations to lemma status weakens the spec by inflating its claim count.
**Required**: Either fold these observations into LP12's prose, or strengthen them to actual independence claims (e.g., construct two states differing only in `home(a)` and show projections are identical).

## OUT_OF_SCOPE

### Topic 1: Link-to-link discovery chains
**Why out of scope**: ASN's Open Questions section appropriately flags this; endsets-referencing-links is admissible per L4(c) of ASN-0043 but transitive discovery is a separate question.

### Topic 2: V-order of projected positions within a single projection
**Why out of scope**: The relationship between I-order in coverage and V-order in the projection depends on per-document arrangement properties that this ASN's framework does not need to commit to.

### Topic 3: Reverse-discovery primitive (V-position to set of containing links)
**Why out of scope**: This requires an additional indexing structure beyond the link store; a forward-projection ASN need not specify the reverse direction.

VERDICT: REVISE
