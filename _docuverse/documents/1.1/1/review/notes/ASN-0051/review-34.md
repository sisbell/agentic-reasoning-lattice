# Review of ASN-0051

## REVISE

### Issue 1: SV9 proof under-cites its dependencies
**ASN-0051, SV9 (DiscoveryMonotonicity)**: "New links may be created (L12a, LinkStoreMonotonicity: dom(Σ'.L) ⊇ dom(Σ.L)), so the discoverable set can only grow."
**Problem**: The argument cites only L12a, but the inclusion `discover_s(A) in Σ ⊆ discover_s(A) in Σ'` requires both (i) value preservation for existing entries (so that `a ∈ discover_s(A) in Σ ⟹ coverage(Σ'.L(a).s) = coverage(Σ.L(a).s)` and the intersection with A persists — L12) and (ii) domain monotonicity for new entries (L12a). The proof glosses the L12 piece. SV8's proof above already does this work, but SV9 doesn't cite SV8.
**Required**: Cite SV8 (or L12 directly) in addition to L12a, and state the two-part argument explicitly: existing discoverers persist by value preservation, new discoverers may join via dom-growth.

### Issue 2: CrossDocumentDecoupling witness has unstated precondition
**ASN-0051, CrossDocumentDecoupling corollary, Step 1**: "K.δ allocates d_2 under a node/account prefix yielding origin(d_2) ≠ O. The SV10 origin used was O = 1.0.1.0.1. Pick any node/account/document prefix `d₂ = 1.0.1.0.2` — agreeing with O on the node and account fields..."
**Problem**: K.δ's precondition (ASN-0047) requires `parent(d_2) ∈ E` for non-root entities. Here parent(d_2) = 1.0.1 (the account). The witness assumes 1.0.1 ∈ E_account is inherited from the SV10 base state, but the SV10 setup never explicitly populated E with the account or node entities — the witness only mentions content addresses i_1, i_2, i_3, a V-position v_1, link a, and document d. A reviewer cannot mechanically verify K.δ's precondition discharges without this acknowledgment.
**Required**: Add to the corollary witness an explicit precondition note that the SV10 base state Σ has the relevant node and account entities in E (or extend the SV10 witness to include their K.δ allocations as a setup chain).

### Issue 3: SV6 proof's structural conclusion (b) needs the t = s case treated
**ASN-0051, SV6 proof, structural conclusion (b)**: "(b) *t agrees with s on positions 1 through k−1.* If t did not agree with s on some position in [1, k−1], the first such position would be a divergence at some j < k — excluded by the sub-lemma."
**Problem**: The sub-lemma rules out *first divergence* at j < k. When t = s (which is admissible since the span is `[s, s ⊕ ℓ)`), there is no divergence at all — the sub-lemma is vacuous. The "If t did not agree" reasoning then needs to acknowledge that vacuous-divergence is itself agreement, not a separate case requiring proof. Adding one sentence resolves it; as written, the proof leaves a reader to verify the t = s case independently.
**Required**: State explicitly that t = s trivially agrees with s on every position (in particular 1..k−1), and the sub-lemma handles t ≠ s.

### Issue 4: Bilateral vitality predicate is named misleadingly for empty-endset cases
**ASN-0051, BilateralVitality definition and discussion**: The predicate `F = ∅ ∨ π(F, d) ≠ ∅` evaluates true vacuously when F = ∅. The text then concedes: "The word 'bilateral' overstates these cases: the formal condition holds but asserts no visibility claim on the empty side."
**Problem**: The text identifies the labelling concern but does nothing about it. The predicate either should be renamed (e.g., "non-empty-side vitality" or "content-side vitality") to match its actual content, or the substantive predicate the analysis below relies on should be stated separately. As it stands, downstream readers — and downstream ASNs — see "bilateral vitality" without the qualification and may misread.
**Required**: Either rename the predicate to remove the "bilateral" overstatement, or split into two predicates: one with the literal disjunction and one with the strict "both content endsets have non-empty projection" form actually invoked in the substantive analysis.

### Issue 5: OrdinalShiftBase convention used implicitly in this ASN without re-declaration
**ASN-0051, Worked Example, M-aux usage, "Same-origin coverage growth" descriptive section**: Notation `a + k` (meaning shift(a, k)) appears throughout — e.g., "If the allocator later spawns a child via inc(aₙ, 1) = c, then c is element-level... and satisfies aₙ < c < aₙ + 1". The Worked Example uses `shift(min(V_1(d)), 1)` style elsewhere but also relies on `a_k + j` reading.
**Problem**: The OrdinalShiftBase convention is established in ASN-0058 (M0-aux) but ASN-0051 does not re-declare or cite it at first use. A reader who treats `aₙ + 1` as numeric addition rather than ordinal shift will get the wrong tumbler in some derivations (e.g., child-depth comparison `aₙ < c < aₙ + 1`, where aₙ + 1 here means shift(aₙ, 1), i.e., next sibling, not "tumbler whose last component is one greater than aₙ's last component" in some other reading).
**Required**: Either re-state OrdinalShiftBase explicitly at first `+ k` use, or add a notation reminder at the top of the body alongside the scoping note for the standard triple.

### Issue 6: SV11 statement (b)'s "at most m · p" bound holds at the state-at-evaluation, but the relationship to evolving state is not stated
**ASN-0051, SV11(b), "Maximal-fragment count — at most m · p fragments"**: "The same set π_text(e, d) is also the disjoint union (within each block) of its maximal ordinal-contiguous fragments, totalling *at most* m · p of them across all blocks."
**Problem**: m is fixed by the endset (immutable by L12, so it doesn't move), but p — the block count of the maximally merged decomposition of M(d)|_{V_{s_C}(d)} — is a function of the current state and may grow under composite transitions that excise interior content (the bound paragraph briefly mentions this: "a composite edit that splits an existing block (e.g., K.μ~ + K.μ⁻ excising interior content) raises p"). The implication — that a single link can develop unbounded fragmentation in a single document under sufficient editing — is buried. This is the substantive *bound-moves-with-state* claim and deserves a more visible statement.
**Required**: Either elevate the "p moves with state" remark to a named consequence (e.g., FragmentCountUpperBoundIsStateDependent) or sharpen SV13(g) to note that m·p is not a fixed system-level invariant on fragment count, only a per-state bound.

### Issue 7: SV13(e) bullet 5 lists K.λ as M-frame for the locate-of-existing-endsets claim, but the same bullet's qualification needs to clarify newly-allocated link's discoverability scope
**ASN-0051, SV13(e), bullet 5**: "K.α, K.δ, K.ρ, and K.λ all preserve M in their frame, so locate(e, d) is unchanged for every endset e that existed prior to the transition. ... K.λ additionally creates a new link, and the locate and discover_s sets for its *new* endsets are evaluated against the unchanged M for the first time — see SV9 for the resulting monotonic growth of discover_s and SV7 for invariance under every transition *except* K.λ."
**Problem**: The qualification "for every endset e that existed prior to the transition" is correct, but it leaves the reader to derive on their own that newly-allocated link endsets *also* have well-defined `locate` and `discover_s` immediately after K.λ — the new endsets reach into the existing M(d) but were created in the same transition. This single-step "create-and-evaluate" semantics is implicit; the synthesis would benefit from a short claim that for any newly-allocated link a' in Σ', `locate(Σ'.L(a').s, d) = {v ∈ dom(Σ'.M(d)) : Σ'.M(d)(v) ∈ coverage(Σ'.L(a').s)}` is well-defined because Σ'.L(a') is defined (K.λ effect) and Σ'.M(d) = Σ.M(d) (K.λ frame).
**Required**: Add a one-sentence corollary on new-link evaluation, or expand SV13(e) bullet 5 to make this explicit.

## OUT_OF_SCOPE

### Topic 1: Link-subspace contribution to projection in SV11
**Why out of scope**: The ASN explicitly defers this to "the Link Subspace ASN" with a clear scope statement noting that π_text(e, d) ⊆ π(e, d) and that link-subspace V-positions can introduce additional projection terms (especially under L13 reflexive addressing). This is appropriate deferred work, not a defect in the present ASN.

### Topic 2: Broader-level spans (k ≤ p₃)
**Why out of scope**: The ASN's "Note on scope — what k ≤ p₃ permits" is explicit that SV6's cross-origin exclusion does not extend to spans with action points in the document prefix, and that broader-level spans (which Nelson describes) are deferred to ASN-0034's address-hierarchy treatment. The udanax-green implementation note further confirms that broader-level spans are not currently implementation-realized, so deferring is appropriate.

### Topic 3: Same-origin coverage growth under TA5 and T10a allocator regimes
**Why out of scope**: The ASN explicitly states no formal SV claim is being made about same-origin growth, deferring it to ASN-0034. The descriptive content (sequential overshoot, child-depth entry, the udanax steady-state vs. first-insertion bootstrap distinction) is appropriate context-setting rather than asserted survivability claims for this ASN.

### Topic 4: Fork (J4) preservation of bilateral vitality
**Why out of scope**: Listed as Open Question. Since J4 is a composite of K.δ + K.μ⁺ + K.ρ — all of which are covered by SV2/SV4/SV7 individually — composite-level forking is a synthesis exercise, not a missing primitive. The aggregate question of *when* bilateral vitality survives a fork (which depends on which I-addresses the K.μ⁺ step copies) is a reasonable future ASN topic.

### Topic 5: Aggregate vitality across documents
**Why out of scope**: The ASN's vitality predicates are per-document by design. A link might be unilaterally vital in one document and the reverse in another; the ASN focuses on per-document survivability. Cross-document aggregate notions are not present and not required for the ASN's stated scope.

### Topic 6: Sub-claims under L4 EndsetGenerality beyond the element-level case
**Why out of scope**: SV6 covers element-level cross-origin allocations. The text correctly notes that for content endsets (coverage in dom(Σ.C), which is restricted to element level by S7b/K.α amendment), this is the operative case. Endsets referencing non-element-level addresses (admitted by L4) are not formally treated; the proof's "t has at least three zeros at p_1, p_2, p_3" structurally excludes non-element-level descendants from element-level spans, but stating this as a corollary is deferred work.

VERDICT: REVISE
