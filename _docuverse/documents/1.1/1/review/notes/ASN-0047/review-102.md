# Review of ASN-0047

## REVISE

### Issue 1: Design-rationale subsections in K.δ k=2 discharge
**ASN-0047, K.δ case (ii) k=2 discharge in *Freshness-discharge summary***: The subsections "*Connection to ownership semantics.*" and "*This contrasts with content/link sub-allocators*" explain *why* a separate axiom isn't needed by appealing to Nelson (LM 4/17) and Gregory (`findisatoinsertnonmolecule`) design intent.
**Problem**: New prose around an axiom explaining why the axiom is needed (or not needed) rather than what it says — matches the reviser-drift pattern explicitly called out in the prompt. The "Connection to ownership semantics" subsection adds 6+ lines of citation-driven justification; "This contrasts with" adds another 5+ lines comparing to SubAllocatorAxiom. Neither paragraph advances the formal discharge — the T10a T2 spawn analysis already closes the obligation.
**Required**: Delete both subsections. The K.δ k=2 paragraph above them already states the T10a T2 spawn structure rigorously.

### Issue 2: NotationDisambiguation block accretion
**ASN-0047, *Scoped coupling constraints*, ValidComposite★ block**: Clauses (a)–(d) explaining `Σ → Σ'` semantics, plus the trailing paragraph "A notational distinction (`Σ → Σ'` atomic vs. `Σ ⇒ Σ'` composite) was considered but not adopted, to preserve compatibility with ASN-0036 and ASN-0043's existing usage."
**Problem**: Essay content in a structural slot — the block justifies notation choices, defers to "the operations layer's obligation, not the elementary transition model's" (clause d), and documents a rejected design alternative inline. Matches "prose justifies document ordering" pattern. Clauses (c) and (d) restate what ValidComposite★ already says about composite-boundary evaluation.
**Required**: Either (i) adopt distinct symbols (`→` atomic, `⇒` composite) and delete the block, or (ii) collapse clauses (a)–(d) into a single sentence: "`Σ → Σ'` denotes the boundary of a finite sequence of elementary transitions when used in coupling/composite contexts, and a single atomic step elsewhere." Delete the "considered but not adopted" sentence.

### Issue 3: Replacement-by-position elaboration overlap
**ASN-0047, *Elementary transitions***: The paragraphs "Replacement at the maximum position of a subspace" and "Replacement at an interior position of a subspace" enumerate the K.α + K.μ⁻ + K.μ⁺ + K.ρ decomposition at length.
**Problem**: The same content appears three times: (i) here in Elementary transitions, (ii) in *Decomposition of K.μ~* under "Decomposition", and (iii) in *Worked example: interior content replacement*. Two paragraphs in different sections say the same thing in different words.
**Required**: Delete the two paragraphs in Elementary transitions. Reference the worked example for the concrete trace; let *Decomposition of K.μ~* hold the formal claim.

### Issue 4: Fork composite J4 discussed in two places
**ASN-0047**: "Amendments to existing transitions" → "Consequence for J4 (Fork)" treats J4's invariant discharge; "Coupling and isolation" → "Definition (Fork)" then re-defines J4 formally.
**Problem**: Two sections defer to each other for the same claim. The Amendments-section discussion verifies J1★/J1'★/D-CTG/D-MIN on J4 using definitions not yet stated; the Coupling-section discussion repeats the structure formally.
**Required**: Move the Amendments-section J4 verification into "Coupling and isolation" alongside the J4 definition.

### Issue 5: Link-withdrawal gap section is scope-deferral prose
**ASN-0047, after D-CTG★ / D-MIN★ definitions**: "Link-withdrawal gap under D-CTG★ / D-MIN★" — section dedicated to explaining what's NOT expressible, citing Nelson's tombstoning design (LM 4/9) as "not specified in the present ASN."
**Problem**: A paragraph imagines a case the claim's preconditions already exclude (interior link withdrawal) and defers resolution to a future ASN. The Open Questions section already records this. Matches the reviser-drift pattern of paragraphs that read like prior findings relocated rather than removed.
**Required**: Delete the section. The Open Questions entry suffices.

### Issue 6: "Link-subspace replacement asymmetry" is meta-content
**ASN-0047, *Elementary transitions***: Paragraph explaining why K.μ⁻ + K.μ⁺_L doesn't compose like K.μ⁻ + K.μ⁺ for content, with two structural-barrier explanations.
**Problem**: Meta-prose explaining a non-feature. The asymmetry is a derived consequence of K.μ⁺_L's preconditions (`ℓ ∉ ran(M(d))` first-arrangement + min/max position rule) — those preconditions are already stated at K.μ⁺_L's definition.
**Required**: Delete the paragraph. Readers can derive the asymmetry from K.μ⁺_L's preconditions.

### Issue 7: Freshness-discharge summary is a use-site inventory
**ASN-0047, *Freshness-discharge summary***: Table catalogues discharge routes for K.α, K.δ, K.λ across multiple sub-cases.
**Problem**: Use-site inventory enumerating downstream consumers of axioms. Each row restates content that's already in the transition's definition or in the *Cross-document disjointness chain lemma*. The post-table commentary "Nodes are baptised by an external authority… Document and account allocation operates within T10a…" reiterates design framing without advancing the formal claim.
**Required**: Delete the table and commentary, or move to a separate reference appendix if it serves consultation needs.

### Issue 8: Forward reference for P6, P7, P7a
**ASN-0047, *Extended reachable-state invariants***: The Class (a) conjunction lists `... P6 ∧ P7 ∧ P8 ∧ NodeLineage ∧ ...` but P6 and P7 (and P7a) are introduced in the *Temporal decomposition* section, which appears after the theorem.
**Problem**: Forward reference within the document; the theorem cites invariants that haven't been defined yet.
**Required**: Move the P6, P7, P7a, GlobalLineage definitions out of *Temporal decomposition* and into a section before *Extended reachable-state invariants*. The temporal decomposition table can summarise; the formal invariant definitions should precede their use.

### Issue 9: L1c weakening from foundation
**ASN-0047, *Foundation invariants* (in main proof)**: The L1c discharge appeals to a "structural inc-chain" defined as "per-step inc-rule conformance — each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfying TA5's structural preconditions ... *not* T10a's full discipline including allocator-frontier domain tracking."
**Problem**: ASN-0043's L1c (LinkAllocatorConformance) reads "operates within a system conforming to T10a (AllocatorDiscipline, ASN-0034)". This ASN's discharge weakens that to a per-step inc-rule property. The Properties Introduced table doesn't list L1c as a local strengthening or weakening of the foundation invariant. This is a substantive divergence that should be flagged.
**Required**: Either (i) state L1c as a *local weakening* of foundation L1c in the Properties Introduced table, with the new "structural inc-chain" formalism named explicitly, or (ii) strengthen the discharge to capture full T10a conformance (which requires axiomatising the activation cross-step for anchors).

### Issue 10: shift(·, 0) = identity convention
**ASN-0047, *Extended reachable-state invariants* (S8★ link-subspace proof)**: "the singleton `(v, M(d')(v), 1)` is a correspondence run satisfying conditions (a) and (b) trivially at the unique singleton index k = 0 ... under the `shift(·, 0) = identity` convention".
**Problem**: ASN-0034's OrdinalShift requires `n ≥ 1`, so `shift(v, 0)` is undefined in the foundation. The convention is asserted ad hoc without a foundation citation. (This may be an issue inherited from ASN-0036's S8 statement, but it surfaces here.)
**Required**: Either cite the convention to its source ASN, or restate S8★(s_L) without invoking shift at k = 0 (e.g., by using a depth-2-specific formulation that bypasses the trivial decomposition).

### Issue 11: K.δ case (ii) k=1 variable inconsistency
**ASN-0047, *Freshness-discharge summary*, K.δ case (ii) k=1 sub-case**: "The step `e = inc(t, 1)` is a T10a T1 sibling-increment (after the first version) or T2 spawn step (for the first version) on `A_v(d)`."
**Problem**: Variable `d` is used where `t` is the operand. The definition of `A_v(d)` (in *Allocator hierarchy under documents*) takes `d ∈ E_doc`; in the k=1 sub-case the operand variable is `t`, and `A_v(t)` would be the correctly-named sub-allocator. Minor but readability-impacting.
**Required**: Rename `A_v(d)` to `A_v(t)` in this paragraph (and any other k=1 discharge text using the same naming).

### Issue 12: Cross-document disjointness chain framing at K.δ document level
**ASN-0047, *Freshness-discharge summary***, in S4 discharge: "for two K.δ events allocating documents d₁, d₂ under distinct accounts A₁ ≠ A₂ ... the *Cross-document disjointness chain* lemma applies at the account level — with A₁ and A₂ playing the role of `d₁, d₂` in the lemma, and the document sub-allocators under each account playing the role of `b_C, b_L`."
**Problem**: The lemma is stated for anchors `b_C(d), b_L(d)` under documents. "Document sub-allocators under each account playing the role of `b_C, b_L`" is conceptually different from the lemma's structure — documents under an account are minted directly by `inc(account, 2)`, not via intermediate element-field anchors. The framing conflates two different allocator-hierarchy levels.
**Required**: Either re-state the lemma generically (e.g., for any pair of non-nesting prefixes), or re-derive the document-level argument directly without analogising to b_C/b_L.

### Issue 13: K.μ⁻ admissibility split between sections
**ASN-0047**: The base K.μ⁻ definition (*Elementary transitions*) includes per-subspace patterns referencing D-SEQ★ enumeration `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}`; the *Amendments to existing transitions* section then formalizes the per-subspace forms D-CTG★/D-MIN★ that D-SEQ★ derives from.
**Problem**: Forward dependency: K.μ⁻'s base definition references D-SEQ★ (which depends on D-CTG★/D-MIN★) before those are introduced. The K.μ⁻ amendment paragraph in *Amendments* then "re-states" the per-subspace scope. The base definition partially anticipates the amendment.
**Required**: Either (i) state K.μ⁻ purely in the original (per-document, no per-subspace) form, with the amendment in *Amendments* doing all the per-subspace work, or (ii) introduce D-CTG★/D-MIN★/D-SEQ★ before K.μ⁻'s definition and state K.μ⁻ in its final per-subspace form once.

### Issue 14: "Arrangement invariants" lemma overlaps with main proof
**ASN-0047, end of *Elementary transitions***: "Lemma (Arrangement invariants from elementary preservation)" — one paragraph claiming "Every valid composite transition preserves S2, S3, S8a, S8-depth, S8-fin, D-CTG, and D-MIN."
**Problem**: The lemma's proof is a one-paragraph restatement of K.μ⁺/K.μ⁻ postconditions. Class (a) of ExtendedReachableStateInvariants covers the same ground in much more detail, including the link-subspace transitions K.λ/K.μ⁺_L and the strengthened D-CTG★/D-MIN★. The lemma is subsumed.
**Required**: Delete the lemma. The main theorem covers the claim with the correct (extended-state) invariants.

### Issue 15: K.μ⁻ precondition clause (3) is a derived consequence
**ASN-0047, *Elementary transitions*, K.μ⁻ precondition**: Clause "(3) *Whole-arrangement effect clause.*" is presented as part of the *Admissible removal pattern*, but its content reads "Together clauses (1) and (2) deliver the whole-arrangement effect clause `dom(M'(d)) ⊂ dom(M(d))`".
**Problem**: Clause (3) is explicitly derived from (1) + (2). Listing it as a third precondition clause obscures that the precondition is just (1) + (2). Mild but a redundant-elaboration pattern.
**Required**: Either fold (3) into (2) as a "Consequence:" remark, or delete (3) and add a derived-effect note to (2).

## OUT_OF_SCOPE

### Topic 1: Account-level k=1 versioning
**Why out of scope**: The ASN's Open Question 11 records that admitting account-level k=1 extension is a design decision deferred to a future use-case. The exclusion at the K.δ case (ii) k=1 precondition (`t ∈ E_doc`) is consistent with current Nelson and Gregory design.

### Topic 2: Node-allocation registry mechanism
**Why out of scope**: NodeUniqueAllocation is posited axiomatically. The protocol-level details (issuing, persistence, concurrency) are appropriately deferred to a future registry-discipline ASN, as noted in Open Question 9.

### Topic 3: Link withdrawal / tombstoning
**Why out of scope**: Nelson's tombstoning design (LM 4/9) requires a separate withdrawal mechanism, explicitly deferred to a future ASN per Open Question 10. The present transition vocabulary's inability to express interior link withdrawal under D-CTG★ is a consequence, not a defect of the ASN's scope.

### Topic 4: Concurrent operations and link address availability
**Why out of scope**: Open Questions 7 and 8 record concurrency and address-availability questions appropriate for an operations ASN, not this transition-classification ASN.

### Topic 5: Transitive transclusion provenance
**Why out of scope**: Open Question 2 records this as a question for a future ASN that addresses link-content interaction.

VERDICT: REVISE
