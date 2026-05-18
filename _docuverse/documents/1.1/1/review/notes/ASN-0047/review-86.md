# Review of ASN-0047

## REVISE

### Issue 1: Pervasive forward-reference accretion (anti-bloat classifier)
**ASN-0047, multiple sections**: Several flagged patterns appear throughout.

- *Use-site inventories at definition sites*: "Entity-allocator-tracked predicate (used by K.δ and downstream)" in *Notation* labels consumers. "Three paths close `e ∉ E`: **Path 1**... **Path 2**... **Path 3**..." at K.δ is a downstream-citation index. SubAllocatorAxiom's three labeled sub-clauses (Exists / Disjoint / Namespace) exist for downstream citation.
- *Axiom rationale prose*: The "Bootstrap node" paragraph after the initial state definition is four paragraphs of Nelson/Gregory citations rather than the definition. SubspaceConventionAxiom and LinkVPositionDepthAxiom both append source citations justifying specific values. The two-paragraph discussion of J0-axiomatic / J1-derived / P7a-orientation in *Temporal decomposition* is meta-prose about logical role.
- *Scope-of-amendment paragraphs*: D-CTG★/D-MIN★, L3, L0, L14a, L-fin each get prose explaining "this is a local strengthening" / "remains authoritative within original scope" / "not retroactively modified here" rather than stating content.
- *Defer-and-cite threading*: "see *Allocator hierarchy under documents* section above," "established by SubAllocatorAxiom, defined in the Allocator hierarchy section below," etc.

**Required**: Inline definitions at point of use; remove scope-of-amendment prose; eliminate use-site inventories.

### Issue 2: Two-parallel-theorems split with substantial framing
**ASN-0047, Extended reachable-state invariants**: Multiple paragraphs explain why the theorem partitions into ExtendedReachableStateInvariants (per-state) vs ExtendedTransitionInvariants (per-transition), including the P0 ⇔ S0 + S1 equivalence-trace paragraph and the retention of S9 "for cross-foundation traceability" despite being subsumed by P0.

**Required**: State the two theorems and their conjuncts; remove the prose about why the split is necessary; either drop S9 (subsumed) or state it without traceability rationale.

### Issue 3: Triplicated property tables at end
**ASN-0047, Properties Introduced**: Three tables — "New properties," "Local extensions," "Foundation restatements (recapitulated for self-contained reference)." The third is largely a citation log of foundation properties used elsewhere.

**Required**: Single index table, or rely on body's definitions. The "Foundation restatements" table re-states content available in foundation references.

### Issue 4: Six worked examples with overlapping verification
**ASN-0047, worked examples**: node baptism, account+document descent, fork+insertion, interior replacement, ghost-base versioning, link allocation+arrangement. The node baptism and account+document descent examples are essentially the same K.δ flow at different strata. Each example repeats the invariant-check pattern (S2 / S3★ / D-CTG★ / D-MIN★ / P5★ / P7a / frame). "Synthesis" paragraphs at the end of each example restate what the example demonstrated.

**Required**: Consolidate entity-layer examples; reduce per-example verification to non-trivial cases; remove "Synthesis" paragraphs.

### Issue 5: K.μ~ split across three sections
**ASN-0047, K.μ~**: The bijection-equation contract sits in *Elementary transitions* despite the prose "K.μ~ — *arrangement reordering* — is a named composite of K.μ⁻ + K.μ⁺ (analogous to J4), not a primitive transition." The decomposition is then re-treated in *Decomposition of K.μ~*, including the K.μ~-FIX derivation. Link-subspace fixity gets its own derivation, plus another in worked examples.

**Required**: K.μ~ should appear in one section, named composite or elementary but not both. The π = id / π ≠ id split inside Decomposition is conceptually one point: K.μ~ reduces to K.μ⁻ + K.μ⁺ only when content actually permutes; otherwise no-op.

### Issue 6: K.μ⁻ exhaustiveness lemma and counterfactual repetition
**ASN-0047, K.μ⁻ "Exhaustiveness lemma"**: The (a)/(b)/(c) partition over per-subspace contraction shapes is proved in detail. Worked examples' "Step 5 (counterfactual)" then re-derive case-(b) and case-(c) rejections.

**Required**: Lemma once; worked examples cite the lemma rather than re-derive rejection mechanics.

### Issue 7: NodeLineage, CL-OWN, CL-UNIQ derivations duplicated
**ASN-0047**: NodeLineage carries an inline discharge in its K.δ definition, plus another proof in ExtendedReachableStateInvariants. Same pattern for CL-OWN (own section + induction case) and CL-UNIQ (own section + induction case).

**Required**: Single proof per invariant.

### Issue 8: "Structural sufficiency" claim restated twice
**ASN-0047, Elementary transitions and Scoped coupling constraints**: "Five primitive kinds... are *structurally sufficient*..." then "Seven elementary transition kinds... plus the named composite K.μ~, are *structurally sufficient*..." The arguments are nearly identical.

**Required**: One sufficiency statement covering the extended seven-kind set; the four-component case is a specialisation, not a parallel claim.

### Issue 9: "Temporal decomposition" is editorial summary
**ASN-0047, Temporal decomposition**: The three-layer table and surrounding prose reflect on the rest of the ASN's content. The two paragraphs analysing the difference between J0-axiomatic and P7a-derived orientations are meta-prose about logical structure.

**Required**: One-paragraph index, or remove and rely on the elementary-transitions table.

### Issue 10: K.μ⁺_L invariant verification duplicated
**ASN-0047, "Per-subspace arrangement invariants under K.μ⁺_L"**: Substantial paragraphs verify S8a / S8-fin / S8-depth / D-CTG★ / D-MIN★ / D-SEQ★(s_L) / S8 at K.μ⁺_L post-state. Re-verified in the link-allocation worked example (Step 2) and again in ExtendedReachableStateInvariants's K.μ⁺_L case.

**Required**: Discharge once; cite elsewhere.

### Issue 11: Counterfactual "Step N" prose inside worked examples
**ASN-0047, worked examples**: "Step 2 (counterfactual — transition not in the set)," "Step 3 (counterfactual)," "Step 5 (counterfactual)" run whole paragraphs through cases the precondition already excludes. This matches the anti-bloat pattern "a paragraph imagines a case the claim's carrier or precondition already excludes."

**Required**: Brief observation that the precondition rejects the case, not a full rejection trace.

### Issue 12: K.α and K.λ first-emission discharge prose
**ASN-0047, K.α and K.λ**: Each transition's precondition lists a freshness clause, then *separately* states that the clause is discharged by SubAllocatorAxiom (first emission) or T10a GlobalUniqueness (subsequent). The prose treats the precondition and the discharge as two layers when one combined statement would suffice. The "structural chain" justification (`d → inc(d, 2) = b_C(d) → ...`) at K.λ's first-link case is then re-elaborated to explain why L1c is "weaker than SubAllocatorAxiom at the first-emission boundary."

**Required**: State the precondition and its discharge premise once at the transition definition; the L1c-vs-SubAllocatorAxiom comparison is not load-bearing for K.λ's contract and can be removed.

## OUT_OF_SCOPE

The ASN's *Open Questions* list captures genuinely deferred items appropriately: link withdrawal mechanism reconciling tombstoning with D-CTG★; concurrent operation discipline; version contract beyond ghost-base; account-level k=1 admissibility. These are correctly categorised.

VERDICT: REVISE
