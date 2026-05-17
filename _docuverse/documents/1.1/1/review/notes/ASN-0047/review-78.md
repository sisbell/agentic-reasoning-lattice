# Review of ASN-0047

## REVISE

### Issue 1: P3★ and P5★ are the same predicate
**ASN-0047, Extended monotonicity invariants**: "P3★ and P5★ are logically equivalent at the predicate level: each is the conjunction of the same six clauses on `Σ → Σ'`... Both names are nonetheless retained because they serve distinct citation roles..."
**Problem**: The ASN admits the two are identical and defends retaining both. Citation continuity is paid once; both names persist forever. The accompanying equivalence paragraph and the trace `P5★'s clauses (a)–(d) and P3★'s six-conjunct body group these same clauses differently` is exactly the "two paragraphs say the same thing in different words" pattern.
**Required**: Pick one. Discharging either discharges the other; downstream proofs can cite whichever, but the ASN should not state both as conjuncts of `ExtendedTransitionInvariants`.

### Issue 2: K.δ routing stated three times
**ASN-0047, Elementary transitions / K.δ**: The 8-row precondition table is followed by "Three discharge paths (named for downstream citation)" prose, which is followed by inline derivation in each subcase explaining the same routing.
**Problem**: Same content (operand requirement, path-discriminating premise, discharge path, operational allocator) appears in tabular, named-rule, and per-subcase forms. The split of "k = 0 sibling tracked" vs "k = 0 sibling ghost-chain" into separate rows triples row count without precondition-signature variation.
**Required**: One presentation. The table suffices; remove the named-rule prose and the per-subcase inline derivations.

### Issue 3: Axiom-site consumer inventories
**ASN-0047, throughout**: NodeUniqueAllocation, NodeLineage, SubAllocatorAxiom, SubspaceConventionAxiom, LinkVPositionDepthAxiom each carry "Consumers: ..." and "Load-bearing alongside SC-NEQ, NodeUniqueAllocation, SubAllocatorAxiom, NoDeallocation (ASN-0034), and S0 (ASN-0036)" paragraphs.
**Problem**: Definition-site inventories of downstream use sites. The same list is repeated across multiple axioms; each axiom's introduction explains why it is needed rather than what it says.
**Required**: Remove. Use-site citations belong at use sites.

### Issue 4: K.μ~ defined four times
**ASN-0047, Elementary transitions / Amendments / Decomposition of K.μ~ / Worked examples**: "K.μ~ (Arrangement reordering, named composite — pointer only)" defers entirely to "Decomposition of K.μ~"; the frame-extension catalogue lists K.μ~ separately; the decomposition section restates the contract; worked examples reference the contract.
**Problem**: Multiple paragraphs in different sections defer to the same downstream location. The "pointer only" definition exists solely to forward-reference; the decomposition section opens with "This section states the K.μ~ contract, verifies invariant preservation, derives link-subspace fixity as a corollary, and exhibits an admissible K.μ⁻ + K.μ⁺ realisation" — a section-table-of-contents paragraph.
**Required**: One definition. References from other sections are pointers; the pointer should not itself be a separate definition.

### Issue 5: Defensive non-circularity prose
**ASN-0047, Link-subspace fixity and elsewhere**: "(This argument uses only subspace-preservation + bijectivity of π + CL-UNIQ at the pre-state; it does not invoke the link-subspace identity property `π(v) = v` — which is itself a derived consequence proved separately in *Link-subspace fixity under K.μ~* — so the CL-UNIQ induction is non-circular with respect to that derivation.)" Similarly "*Staging within the outer induction.* The K.μ~-FIX derivation below consumes D-SEQ★ at both the pre-state and the post-state..."
**Problem**: Document-ordering justifications. The proof either is or isn't circular; explaining how it avoids circularity is meta-prose around the proof.
**Required**: Trust the proof structure. If a proof is suspected of being circular, fix it; otherwise omit the defense.

### Issue 6: Frame extension catalogue duplicates definition-site frames
**ASN-0047, Amendments to existing transitions**: "To consolidate the seven elementary transitions plus the K.μ~ named composite in one place — so that the catalogue stands as a single authoritative reference rather than being split between this amendment site and the K.λ and K.μ⁺_L definition sites — both link-side transitions are reproduced here alongside the six pre-existing ones."
**Problem**: Frames already stated at definition sites. The justification for duplication ("authoritative reference") is itself meta-prose. K.λ's frame appears at its definition site *and* in the catalogue, prefaced by "frame, reproduced from K.λ's definition site for catalogue completeness."
**Required**: Frames stated once. Either at definitions or in a catalogue, not both.

### Issue 7: "Structural sufficiency and known gaps" consolidates content already consolidated
**ASN-0047, Structural sufficiency and known gaps**: "The two structural-sufficiency claims above — the five-primitive claim at the end of *Elementary transitions*... and the extended seven-elementary-plus-K.μ~ claim at the end of *Scoped coupling constraints*... appear at the natural locations in the document, each accompanied by its own bounded-sufficiency caveat and known gap. This subsection consolidates what *is* and what *is not* covered..."
**Problem**: Third statement of the same claim with explicit acknowledgment that the first two also state it. The consolidation paragraph explains why a consolidation paragraph exists.
**Required**: Either state once with the full enumeration, or distribute, but not both.

### Issue 8: "Per-state arrangement shape (D-SEQ★)" signpost
**ASN-0047, Elementary transitions**: A boxed pseudo-derivation states D-SEQ★ as `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` and notes "Downstream sections (K.μ⁻ admissibility, the K.μ~-FIX domain-fixity argument, the link-subspace fixity proof, and the ExtendedReachableStateInvariants induction) appeal to D-SEQ★ by name at each state where its premises hold."
**Problem**: Signpost block whose content is restated below in the Amendments section's full D-SEQ★ derivation. The signpost is a downstream-consumer enumeration relocated to a position where D-SEQ★ has not yet been derived.
**Required**: Remove the signpost. The derivation in Amendments suffices; downstream appeals find it there.

### Issue 9: S5 absence-defense
**ASN-0047, ExtendedReachableStateInvariants**: "S5 (UnrestrictedSharing) of ASN-0036 — the absence of an injectivity constraint on M(d), permitting multiple V-positions to map to the same I-address — is preserved as a derived consequence of the conjunction above rather than as a separately named conjunct: no listed per-state invariant imposes injectivity..."
**Problem**: A paragraph imagining a case the conjunction already handles. S5 is an existential claim ("there exists a state with multiplicity > N"); whether it's a named conjunct is a presentational choice, but the defense reads as if S5's status required explanation.
**Required**: Either list S5 as a conjunct or omit it silently. The defense is not load-bearing.

### Issue 10: SC-NEQ promotion explained in three places
**ASN-0047, throughout**: SC-NEQ is stated at "SC-NEQ (Axiom, SubspaceDistinctness)," re-explained in the L14 derivation chain, restated in the Foundation restatements table with prose about promotion provenance ("ASN-0043 also states `s_C ≠ s_L` inline as a definitional stipulation but does not name it as an axiom; this ASN *promotes* that inline inequality to a load-bearing named axiom"), and discussed in Design provenance.
**Problem**: Each restatement explains why SC-NEQ exists as a separate axiom. The promotion rationale belongs at exactly one place.
**Required**: Single statement of SC-NEQ with its rationale; remove repeats.

### Issue 11: K.δ case-(ii) precondition table row split is over-specified
**ASN-0047, Elementary transitions / K.δ**: Rows "(ii) k = 1 (live, tracked)" / "(ii) k = 1 (ghost-base)" / "(ii) k = 1 (ghost-chain)" have identical operand-requirement columns. The split is on the path-discriminating premise, which is itself a derived consequence of state.
**Problem**: The precondition list does not distinguish these three sub-cases. The table conflates "preconditions required to fire K.δ" with "operational state determining which discharge path applies." A reader checking K.δ's contract sees three rows for what is one precondition signature.
**Required**: Collapse to one row per precondition signature. State separately, in derivation prose, that the discharge path varies by InEntityAllocatorDomain(t).

### Issue 12: Worked-examples coordinating table preamble
**ASN-0047, Worked examples — coordinating coverage table**: "Five worked examples follow, coordinated by the transition kinds, invariants, and design-point obligations they exercise. Each row identifies the example's primary load — what it is engineered to verify on a concrete state — and its frame-only coverage..."
**Problem**: Section describing what the section does. The table is the coordination; the preamble explains why a coordination exists.
**Required**: Remove the preamble. The table heading and column names suffice.

### Issue 13: "Cross-example coverage" closing paragraph
**ASN-0047, Worked examples — coordinating coverage table**: A paragraph after the table enumerates which example exercises which transition: "K.α and K.δ on accounts and documents are exercised in Examples 2, 3, and 4..."
**Problem**: Use-site inventory in tabular form is already in the table; the prose paragraph re-enumerates the same coverage.
**Required**: Remove.

### Issue 14: Per-example "exercised invariants" recapitulation
**ASN-0047, end of each worked example**: Closing paragraphs list every invariant the example exercised. Example 5 closes with "Invariants exercised *directly*... Invariants exercised *only as frame-preserved*..."
**Problem**: Each example ends with a coverage summary that the coordinating table also captures. A reader scanning for invariant coverage now has three locations: per-example summary, coordinating table, ExtendedReachableStateInvariants theorem.
**Required**: One coverage trace per example, in the table. Closing paragraphs should state what the example *concluded*, not what it touched.

## OUT_OF_SCOPE

### Topic 1: Withdrawal mechanism
The open question on link withdrawal (tombstone vs status flag vs retraction link) is correctly deferred. The K.μ⁻ D-CTG★/D-MIN★ amendment forecloses Nelson's tombstoning at LM 4/9; the open question records this gap. Not an error in this ASN.

### Topic 2: Version lineage acyclicity
Version DAG constraints, content-allocator linkage across versions, and version-management semantics are correctly deferred (open question).

### Topic 3: Concurrent operation semantics
Atomicity, serialization, and concurrency model are correctly deferred (open question).

VERDICT: REVISE
