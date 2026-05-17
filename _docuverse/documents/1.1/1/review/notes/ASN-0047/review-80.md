# Review of ASN-0047

## REVISE

### Issue 1: Coordinating coverage table is pure navigational meta-prose
**ASN-0047, "Worked examples — coordinating coverage table"**: The table maps five worked examples to invariants exercised and "frame-only coverage". It contains no formal content — it is a use-site inventory whose only function is to point the reader at downstream worked examples.
**Problem**: Per anti-bloat guidance, use-site inventories and tables that catalog downstream consumers do not advance reasoning.
**Required**: Remove the table. If readers need cross-references, each worked example's own opening sentence already names what it exercises.

### Issue 2: Design provenance section is "Why the axiom is needed" essay content
**ASN-0047, "Design provenance"**: A consolidated section explaining consultation evidence for bootstrap node form, SubspaceConventionAxiom, LinkVPositionDepthAxiom, SubAllocatorAxiom, NodeUniqueAllocation, K.δ ghost-base, L1b, versioning, K.μ⁺_L origin, and link-subspace correspondence-run scope.
**Problem**: This is the canonical "Why the axiom is needed" anti-pattern — explaining why axioms exist rather than what they say. The axiom statements themselves carry the formal content; the rationale is archeology.
**Required**: Delete the section. Where a single sentence of inline justification at the axiom site genuinely clarifies the formal content, keep it there. Move consultation citations to a separate provenance log outside the ASN.

### Issue 3: Cross-references to deferred questions duplicates the Open Questions section
**ASN-0047, "Structural sufficiency and known gaps"**: The "Cross-references to deferred questions" subsection lists four items, each pointing to the Open Questions section below.
**Problem**: This is the forward-reference-accretion pattern flagged in the anti-bloat guidance: multiple paragraphs in different sections defer to the same downstream location.
**Required**: Delete the cross-reference list. Readers can find Open Questions on their own.

### Issue 4: K.μ⁻ Precondition signpost paragraph is defensive justification
**ASN-0047, K.μ⁻ definition, "Precondition — admissibility structure (signpost)"**: A paragraph explaining that "the load-bearing admissibility content comprises two jointly necessary clauses, signposted here at the head of the precondition list so the division of labour is visible before the per-clause detail".
**Problem**: Meta-prose explaining what is about to be said. The precondition that follows is clear without the signpost.
**Required**: Delete the signpost paragraph. State the precondition clauses directly.

### Issue 5: ValidComposite★ "identity composite (n = 0 case)" paragraph
**ASN-0047, ValidComposite★**: The paragraph beginning "*Identity composite (n = 0 case).* The sequence length `n ≥ 0` is permitted, so the *empty* sequence..." defends admitting n = 0.
**Problem**: Defensive justification. If n ≥ 0 is in the quantifier, the empty sequence is admitted; if n ≥ 1 was intended, change the quantifier. The half-page of explanation belongs in neither case.
**Required**: Either remove this paragraph and let the quantifier carry the meaning, or amend the quantifier to exclude the degenerate case if that was the intent.

### Issue 6: K.μ~ "Other admissible decompositions" subsection is a use-site inventory
**ASN-0047, "Decomposition of K.μ~"**: A subsection listing three alternative decompositions ("Swap of the two maximum content-subspace positions", "Permutation acting on the top-k content-subspace positions only", "Permutation acting on the link-subspace minimum").
**Problem**: Once the existence claim is established, illustrative variants belong in implementation documentation, not the abstract spec. The contract is the bijection equation; the worked decomposition discharges the existence obligation.
**Required**: Delete the subsection. The full-clearance witness already establishes existence.

### Issue 7: "Reconciliation with ASN-0043's L1c" is defensive justification
**ASN-0047, "Allocator hierarchy under documents"**: Multi-paragraph explanation of why SubAllocatorAxiom does not conflict with L1c, including a worked chain witness.
**Problem**: The non-conflict is stated three times in slightly different words ("L1c is a structural-producibility existential", "SubAllocatorAxiom packages the operational claim", "both are satisfied by the witnessing chain").
**Required**: One sentence: "SubAllocatorAxiom is operational; L1c is structural-producibility; the chain `d → inc(d, 2) → inc(b_C(d), 0) → inc(b_L(d), 1)` witnesses both."

### Issue 8: Ghost-base K.δ admissibility presumes an unmodeled allocator
**ASN-0047, K.δ ghost-base case + worked example 4**: K.δ k=1 ghost-base admits inc operand `t` with `t ∈ allocated(s) ∧ t ∉ E_doc`. The worked example stipulates: "We take `allocated(Σ₆)` ... to include `t`."
**Problem**: The mechanism by which `t` enters `allocated(s)` without K.δ firing is not modeled. ASN-0034's AllocatedSet derives `allocated(s)` from emissions of active T10a allocators; ghost emission has no corresponding K-event in this ASN's elementary set.
**Required**: Either drop `t ∈ allocated(s)` from the K.δ ghost case (admit any T4-valid IsDocument tumbler as operand), or specify the ghost-emission mechanism as an elementary transition or named axiom.

### Issue 9: J4 admits k=0, k=1, k=2 without distinguishing forking from sibling allocation
**ASN-0047, J4 definition + worked example 2**: J4 is described as Nelson's "forking", but the K.δ step is unrestricted. Worked example 2 instantiates J4 with k=0 sibling allocation (`1.0.1.0.2` = inc(1.0.1.0.1, 0)) producing a new document under the same account, not a version of the source.
**Problem**: Nelson's "fork" is specifically version-creation (k=1 in this ASN's terms); the example exhibits a different operation. J4's definition admits both without distinguishing them, conflating two design-distinct creation patterns.
**Required**: Either restrict J4 to a specific K.δ sub-case (the k=1 version case if "fork" is meant in Nelson's sense), or rename and distinguish ("new-document-with-transclusion" vs "version-fork").

### Issue 10: Three-discharge-paths paragraph is essay content surrounding the dispatch table
**ASN-0047, K.δ**: The "Three discharge paths for `e ∉ E` — named rules" paragraph names Path 1, Path 2, Path 3 in prose after the table already presents them.
**Problem**: The discharge table already routes events through the three paths; the named-rules paragraph re-states the table's content as essay text.
**Required**: Delete the paragraph. Add Path 1/2/3 labels directly in the table's "discharge path" column if cross-references downstream need them.

### Issue 11: Per-state vs per-transition theorem split is restated for four-component and extended states
**ASN-0047, "Coupling and isolation" + "Extended reachable-state invariants"**: Two pairs of theorems (Reachable-state per-state, Reachable-state per-transition; ExtendedReachableStateInvariants, ExtendedTransitionInvariants), with parallel structure and proof shape.
**Problem**: The four-component theorems are scaffolding superseded by the extended versions. Both being stated forces the reader to track which model applies at each section.
**Required**: State only the extended theorems. If the four-component case needs explicit treatment, note that the extended forms specialize to it when L = ∅.

### Issue 12: SubspaceConventionAxiom subsumes SC-NEQ but both are stated as axioms
**ASN-0047, axiom layering**: SubspaceConventionAxiom (`s_C = 1 ∧ s_L = 2`) trivially implies SC-NEQ (`s_C ≠ s_L`). The ASN justifies keeping both: "SC-NEQ remains as the *parametric* axiom for arguments that need only distinctness."
**Problem**: Defensive justification of redundancy. Every argument cited as "needing only SC-NEQ" continues to work under SubspaceConventionAxiom; the parametric/concrete distinction adds nothing operational.
**Required**: Choose one axiom. Either commit to SubspaceConventionAxiom and let arguments cite it; or commit to SC-NEQ and treat the (1, 2) values as a model-instantiation note outside the axiom set.

### Issue 13: K.μ⁻ exhaustiveness lemma duplicates content with subsequent case analysis
**ASN-0047, K.μ⁻**: The exhaustiveness lemma proves three cases (a)/(b)/(c) partition all per-subspace contractions. The case analysis that follows then re-presents the same three cases as "verification" that the precondition matches the postcondition.
**Problem**: The lemma and case analysis cover overlapping ground; the "verification" framing in the case analysis is meta-prose about what the lemma already established.
**Required**: Either delete the case analysis (the lemma plus admissibility precondition suffice) or delete the lemma (the case analysis already partitions cases). Pick one presentation.

### Issue 14: Multiple "load-bearing" / "operative" tagging throughout
**ASN-0047, passim**: The words "load-bearing", "operative", "the operative", "operative axiom" appear dozens of times to flag which premise is doing work in a derivation.
**Problem**: This is essay-style emphasis substituting for clear logical structure. Where the proof's structure is clear, the tag is redundant; where the structure is unclear, the tag does not fix it.
**Required**: Delete the tagging language. If a particular premise is the one bearing weight in a derivation, the derivation's structure should show this without verbal flagging.

### Issue 15: Notation section's "T" vs "allocated(s)" clarification
**ASN-0047, "Two scopes of 'T10a's domain' — named predicates"**: Includes a "Note on naming. This ASN reserves the symbol `T` for ASN-0034's foundation T0 (CarrierSetDefinition) ... earlier informal usage of `T` to mean 'the universe of allocated tumblers' conflated the two and is replaced throughout by `allocated(s)`."
**Problem**: This is meta-prose about the ASN's own terminology history — a prior finding's content relocated rather than removed.
**Required**: Delete the note. Use `allocated(s)` throughout consistently without explaining what the older form was.

## OUT_OF_SCOPE

None — the ASN stays within its declared scope (state, elementary transitions, invariants, coupling) and explicitly defers named operations, authorization, atomicity, etc. to other ASNs.

VERDICT: REVISE
