# Review of ASN-0094

## REVISE

### Issue 1: Foundation citation violation — ASN-0036 and ASN-0093 cited by number
**ASN-0094, Definition — SubstrateConformingLayer**: "*(a) Invariant Catalog.* The full L/S/M/C invariant list of ASN-0036, ASN-0043, and ASN-0093: ... *ASN-0036 content/arrangement invariants:* S0, S1, S2, S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ. *ASN-0093 substrate invariants:* M0, M1, C0, C1, C1b, C1c, C-fin."
**Problem**: The foundation set is ASN-0034, ASN-0043, ASN-0086. ASN-0036 and ASN-0093 are not foundation. Restating their invariant lists by number is a cross-ASN reference violation.
**Required**: Either surface the needed invariants as scaffolding clauses (the ASN does this for some — finish the job), or defer entirely to ASN-0086's SubstrateConformingLayer Definition without restating its catalog (a). Catalog (b)'s chain-discipline names (SubAllocatorAxiom, ChainMembershipForOrigin, etc.) appear nowhere in foundation extracts and likewise need to be either scaffolded or omitted.

### Issue 2: Sh5's central claim collapses to hand-curation
**ASN-0094, Sh5 META and "Status of per-shape uniformity"**: "Per-shape uniformity is an aspiration, not a framework commitment." "Both Sh5(a) and Sh5(b) are design conventions enforced by catalog-author diligence, not by any framework-supplied tool."
**Problem**: The intro promises "a predicate template family is mechanically organized" from shapes. The body downgrades this to hand-curation with no mechanical gate. If two registrations at the same shape may register divergent bodies, what does the shape commit to beyond a 5-tuple of registry values? The framework's central premise is undermined.
**Required**: Either (a) prove mechanical body derivation (and remove the downgrade language), or (b) acknowledge the framework's actual content is Sh-conf + Sh0–Sh4 + discipline contracts, with the catalog being an organizational convenience, and shrink Sh5's claims accordingly.

### Issue 3: Massive reviser-drift accretion
**ASN-0094, throughout**: Sub-paragraphs labeled "Status," "Scope," "Stratification," "Ordering with Sh-conf," "Why this ordering," "Design rationale," "Per-layer choice is not offered at this draft," "Compatibility envelope," "Notational convention," etc. appear on nearly every formal statement.
**Problem**: The system reminder flags exactly these patterns: prose around an axiom explaining why it's needed rather than what it says; multiple paragraphs deferring to downstream locations; definitions enumerating downstream consumers; prose justifying document ordering. Examples:
- The Sh4 idempotency contract's "Ordering with Sh-conf" clause restates information from the Gate Ordering section.
- The "Audit-slice set-semantics commitment" appears in 3+ places with substantively identical content.
- The TypedRelationCatalog Definition's "Decidable membership" and "Lifetime constancy" paragraphs explain why the catalog has its properties, not what they are.
- The Open Questions section opens with meta-prose about its own organization ("Items in the third category are listed here, not in a separate Scope Limitations section, because...").
**Required**: Cut ~40-50% of prose. Specifically remove all "Status," "Scope," "Design rationale," "Why X matters" sub-paragraphs; consolidate the repeated audit-slice discussion; remove justifications for ordering, naming, and design alternatives.

### Issue 4: Properties Introduced table entries are essays, not statements
**ASN-0094, Properties Introduced table**: The "Statement" column for Sh4 (9 lines), NullifyActiveSubsetCompatibility (~25 lines), EffectiveWpSimplification (~15 lines), Sh-conf, SubstrateConsumerActiveSubsetCompatibility, etc. are multi-paragraph essays including rationale, alternatives considered, scope clarifications, and branch-structure commentary.
**Problem**: A properties-introduced table should summarize. These entries duplicate the body's discussion verbatim.
**Required**: One-line summaries per row. Push rationale and branch structure back to the body section (and trim there too).

### Issue 5: NullifyActiveSubsetCompatibility Corollary is over-elaborated
**ASN-0094, Nullify Compatibility section**: The corollary statement plus surrounding prose ("Branch structure," "Audit-slice multiplicity is not preserved," "Migration discipline for bare-Nullify multiset consumers," "Per-consumer compatibility commitments" table, "Lemma — SubstrateConsumerActiveSubsetCompatibility," "Compatibility envelope") spans several pages.
**Problem**: The corollary's actual content is: "Under the contract, Nullify's active-subset postcondition holds whether the call issues or suppresses; audit-slice multiplicity is not preserved." The proof is a 4-line case split. Everything else is meta-discussion.
**Required**: Reduce to the bare corollary + 5-line case-split proof. Move the per-consumer table to an appendix or remove. The SubstrateConsumerActiveSubsetCompatibility Lemma is redundant — it states the same compatibility relation in more generality without adding teeth.

### Issue 6: Walkthrough redundancy
**ASN-0094, Per-Shape Template Walkthroughs + Additional Worked Examples**: Comment, Coverage, Resolution-standalone, Tuple-Classifier, Provenance, Attributed Retraction, Sh4 emission suppression — 7+ walkthroughs.
**Problem**: Each walkthrough exhibits the same Sh-conf gate firings (canonical-form, cardinality, target-domain), the same Sh4/FDD suppression behavior, the same rejection patterns. The Common rejection patterns section already enumerates the 6 patterns; each walkthrough then re-instantiates them on different K's. The walkthroughs add bulk without adding structural insight.
**Required**: Consolidate to one canonical walkthrough per distinct cardinality skeleton (one (1,1), one (0,1), one (*,1), one (1,0|1)). Cite the Common rejection patterns rather than re-deriving them at each walkthrough.

### Issue 7: Three Peano-style axioms added in the appendix
**ASN-0094, Appendix**: "*Foundation extensions — three framework-local Peano-style axioms.* This framework introduces three Peano-style axioms not in ASN-0034's NAT axiom list... *(Peano-rec)*, *(Peano-zero-least)*, *(Peano-pred)*."
**Problem**: Adding three new axioms to derive `ℕ-commutativity` for a length-subtraction step in a lemma proof signals that the proof strategy is off. The Lemma — LinkAddressNotPrefixOfEmit Step II.0 needs `#a − #b ∈ ℕ` well-defined under `#b ≤ #a`; this is a one-line consequence of T0's ℕ properties in most reasonable formulations. The need for three new axioms plus a multi-page appendix is a workaround.
**Required**: Either (a) restructure the lemma's proof to avoid needing partial subtraction at the ℕ level (e.g., reason about positions directly without subtracting lengths), or (b) request foundation extension to ASN-0034 rather than introducing framework-local axioms.

### Issue 8: The "Reach of the framework's target-domain symbols" is a scope-boundary essay
**ASN-0094, Canonical Shape Catalog**: "Throughout this catalog, `A_doc` denotes *content addresses* (per ASN-0086, `A_doc^Σ = dom(Σ.C)` — content-store entries with `zeros(·) = 3`), *not* document-level container addresses... This is a scope boundary the framework adopts, following udanax-green's implementation practice (Gregory)..."
**Problem**: The scope boundary can be stated in one sentence. The current paragraph explains the boundary, justifies it via Nelson + Gregory, and previews future extension work.
**Required**: Reduce to one sentence stating the boundary. Move the udanax/Nelson commentary to a separate design-notes file if it must be preserved.

### Issue 9: The Sh-conf "Gate Ordering (consolidated)" duplicates per-contract ordering clauses
**ASN-0094, Sh-conf section + per-contract subsections**: The Gate Ordering clause lists 5 gates with execution order; each per-contract section then has its own "Ordering with Sh-conf" sub-paragraph re-stating its position in the sequence.
**Problem**: Same information stated in 4-5 places (Sh-conf gate ordering, Sh4 contract ordering, FDD contract ordering, SHCD contract ordering, plus the consolidated commitment reference table).
**Required**: State once. Have per-contract sections cite the consolidated table by gate number rather than repeating the ordering.

### Issue 10: AllocatedAddressAntichain's Case 3 has a worked-example admission that the example doesn't satisfy the lemma
**ASN-0094, AllocatedAddressAntichain proof**: "*Case II.B example: no concrete satisfying configuration exists.* The Lemma's conclusion is that *no* substrate-reachable `(b, a)` configuration... exists. A worked example would therefore necessarily exhibit a configuration that does not satisfy the proof's hypothesis. Rather than walking through a hypothetical trace on a non-satisfying configuration... we omit the Case II.B worked example..."
**Problem**: This is a non-example explaining why no example can be given. It's meta-prose substituting for either a real example or a clean omission.
**Required**: Either provide a concrete contradiction-extraction trace at an almost-satisfying configuration (the paragraph almost does this for Case II.A and then drops it), or just omit the example without explanation.

### Issue 11: The single-home/Sh4/FDD contracts each state mutual-exclusion and routing
**ASN-0094, "Mutual exclusion of FDD and SHCD" paragraph + the contracts themselves**: The exclusion is stated in the Canonical Shape Catalog section, restated in the Gate Ordering section, restated again in the FDD section, restated in the consolidated commitment table.
**Problem**: Same fact restated 4+ times.
**Required**: One statement, in the Canonical Shape Catalog where the shapes' idem values establish the structural impossibility.

### Issue 12: The "Catalog-wide citation audit" table is itself bloat
**ASN-0094, Sh5(b) section**: The audit table walks through each row's data-symbol classifications.
**Problem**: Each row's audit reads "`from₁` (i: shape-component-derived), `K` (ii: K's name)" — the rule is identical at every row and the audit adds no information beyond saying "this row satisfies the rule." Combined with the "rejected candidate (`K_is_fresh`)" note, the audit table is illustrative bookkeeping rather than load-bearing content.
**Required**: Drop the table. If a worked check is useful, exhibit one (the existing "Worked check at `latest_K_for_addr`" suffices) and rely on it.

### Issue 13: The proof of Sh0 Case A enumerates step classes when the case-equation closure is trivial
**ASN-0094, Sh0 inductive step**: "Once the case-equation holds, Sh4 is inherited directly..." (this clarification appears in Sh4 Case A but the underlying issue applies to Sh0–Sh3 too). The Sh0/Sh1/Sh2/Sh3 proofs each enumerate K.σ, K.α, K.λ-at-other-types, and arrangement-modifying classes for Case A.
**Problem**: Once you've established `L_K^{Σ'} = L_K^Σ`, the inductive property follows immediately by set extensionality. The enumeration of how each transition class achieves the case-equation is expository, not load-bearing — and the same enumeration appears in all four proofs.
**Required**: State Case A once with the case-equation closure argument, then in each preservation theorem note "Case A by case-equation; Case B is the substantive direction." Cut redundant enumerations.

### Issue 14: Multiple "deferred to downstream" forward references
**ASN-0094, throughout**: "See the *Codomain convention*"; "see the *Asymmetry of `to_K`* note"; "(formalized as the NullifyActiveSubsetCompatibility Corollary below)"; "(established just above)"; "(per the *Decidable membership* paragraph in the TypedRelationCatalog Definition above)"; "(per the *Stratified proof order* clause in the Sh-conf section)"; etc.
**Problem**: The system reminder flags exactly this — multiple paragraphs deferring to the same downstream location, prose justifying document ordering. The pattern compounds across cycles.
**Required**: Resolve forward references by inlining the needed content or restructuring so cited material comes first. Remove "stratified proof order" clauses (they're scaffolding for the reader, not load-bearing).

### Issue 15: ShapeWellFormedness implications are stated with literal-vs-set arithmetic justifications
**ASN-0094, ShapeWellFormedness**: "The cardinality side of each implication tests the *literal* registry value `0`, not the broader set `{0, 0|1}`: the values `0` and `0|1` are distinct entries in `{0, 1, *, 0|1}`, so the antecedent `c_F = 0` is false when `c_F = 0|1`."
**Problem**: This is the formal antecedent of `=` between two registry values. The clarification of "literal" vs "set" is unnecessary; literal equality is the default reading.
**Required**: Cut the "Behavior at `c_F = 0|1`" and "Why the constraint matters" paragraphs.

## OUT_OF_SCOPE

### Topic 1: Multi-process consistency of registry and contracts
**Why out of scope**: The framework explicitly commits to single-process substrates (recorded in Open Questions). Generalizing to multi-process atomicity belongs in a separate ASN that introduces coordination protocols.

### Topic 2: A_M target-domain symbol for document-container addresses
**Why out of scope**: Currently the framework can only target content addresses, not document containers. Extending the target-domain vocabulary belongs in a future ASN; the current framework's coherence does not depend on it.

### Topic 3: Cross-process catalog consistency
**Why out of scope**: The shape registry's lifetime constancy is asserted within a process; cross-process drift is a distributed-system concern outside this ASN.

VERDICT: REVISE
