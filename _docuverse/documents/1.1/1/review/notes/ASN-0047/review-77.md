# Review of ASN-0047

## REVISE

### Issue 1: J1★ formulation has incorrect operand in negated existential
**ASN-0047, Scoped coupling constraints**: `(A Σ → Σ', d ∈ E'_doc, a : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) : (a, d) ∈ R')`
**Problem**: The negated existential ranges over `v ∈ dom(M(d))` (pre-state) but reads `M'(d)(v)`. M'(d) need not be defined on v ∈ dom(M(d)) \ dom(M'(d)). The explanatory prose ("`a₃` is genuinely new to the content-subspace range and requires provenance recording") makes clear the intent is `a ∈ ran(M'(d)|_{s_C}) ∧ a ∉ ran(M(d)|_{s_C})`. J1'★ correctly uses `M(d)(v) = a` in the analogous slot.
**Required**: Change `M'(d)(v) = a` to `M(d)(v) = a` in J1★'s negated existential.

### Issue 2: Defensive axiom commentary dwarfs axiom content
**ASN-0047, NodeUniqueAllocation (and SubAllocatorAxiom, NodeLineage)**: The NodeUniqueAllocation axiom is one sentence. It is followed by sub-paragraphs labeled *Scope*, *Object-level axiom content (what is load-bearing)*, *Why the axiom is needed (negative argument, not protocol-dependent)*, *Protocol rationale (meta-level, not part of the axiom)*. SubAllocatorAxiom adds *Relationship to T10a's allocator tree*, *Mapping onto T10a's `Act(s)`/spawning machinery — virtual spawning events*, *Reconciliation with ASN-0043's L1c*. NodeLineage adds *Scope* and *Structural mechanism and load-bearing premise*.
**Problem**: Exactly the pattern flagged in the anti-bloat note — sub-paragraphs labeled "Scope," "Object-level content," "Protocol rationale," "Why the axiom is needed." Justification dwarfs the load-bearing statement; future readers must work past meta-commentary to find the actual axiom.
**Required**: State each axiom, name its consumers in one line, delete the *Why*/*How*/*Protocol rationale*/*Mapping*/*Reconciliation* sub-paragraphs. Let downstream proofs do their own discharging.

### Issue 3: Document-ordering justification at D-SEQ★
**ASN-0047, Elementary transitions (Per-state arrangement shape preamble)**: The *Inductive structure (no circularity)* paragraph is ~600 words walking through three-level induction with an "acyclicity certificate" to justify that a forward pointer to the derivation in *Amendments to existing transitions* is non-circular.
**Problem**: "Prose justifies document ordering" — explicit pattern in the anti-bloat note. The staging argument is generic to any forward reference to a single-state derivation chain.
**Required**: Reorder so D-SEQ★ is stated before its first consumer (K.μ⁻ admissibility) and remove the *Inductive structure* paragraph entirely.

### Issue 4: K.δ table followed by prose restating identical content
**ASN-0047, Elementary transitions (K.δ)**: The K.δ table partitions admissible events across 8 rows × 5 columns. The opening prose acknowledges "the prose below restates the same content with full derivation."
**Problem**: Self-acknowledged duplication producing ~3000 words of redundant case-walk-through. The table or the prose suffices, not both. The accompanying "Three discharge paths," "Exemplars are not exhaustive," "Mutual exclusivity and joint exhaustiveness," and "Exemplar (a)/(b)/(c)/(d) routing through `A_v(t_root)`" sub-paragraphs compound the duplication — multiple paragraphs restating that premises determine routing.
**Required**: Pick one. If the table is the load-bearing artifact, drop the per-case prose; if the prose carries derivations the table cannot, lift the table to a one-screen summary. Remove the exemplar-routing prose — premise-based dispatch suffices.

### Issue 5: Consultation evidence in spec body
**ASN-0047, multiple sites**: *Structural form of n₀* cites LM 4/28, LM 4/38 with multi-paragraph readings of "two interlocking Nelsonian readings of the digit `1`". SubspaceConventionAxiom cites LM 4/30–4/31, xanadu.h:144–146, granf2.c:162, do2.c:94. LinkVPositionDepthAxiom cites LM 4/31, do2.c:151–167, xanadu.h:144–146, do2.c:169–183. Similar prose recurs around SubAllocatorAxiom, NodeUniqueAllocation, the "Reconciliation with ASN-0043's L1c" paragraph, and the K.δ ghost-base discussion.
**Problem**: The spec is a structural specification; consultation evidence belongs in reasoning docs. Sprinkling evidence prose throughout produces a hybrid spec/commentary document and significantly inflates the body relative to load-bearing content.
**Required**: Move consultation-evidence prose to a single *Design provenance* section (or to a separate reasoning document) with one-line citations remaining in the body where strictly needed.

### Issue 6: Worked example "Rejection model" paragraph
**ASN-0047, *Worked example: node baptism under the bootstrap root***: The example opens with a "Rejection model (formal status of counterfactuals)" paragraph explaining what *rejected* means in the transition-set definition.
**Problem**: Essay content in a worked-example slot. The example illustrates transition validity by exhibiting valid and invalid attempts; the meta-paragraph about what rejection means at the spec layer doesn't advance the example.
**Required**: State the convention once at the *Elementary transitions* heading (if needed) and remove from the worked example.

### Issue 7: K.μ⁻ "Worked sub-case" inside precondition
**ASN-0047, Elementary transitions (K.μ⁻)**: After the (A)/(B) precondition signpost, a *Worked sub-case: case (a) with `n'_S = n_S` on every subspace* paragraph illustrates that (A) alone is insufficient.
**Problem**: The case analysis already proves (B)'s necessity (the effect clause has no witness when n'_C = n_C ∧ n'_L = n_L). The worked sub-case is illustrative duplication.
**Required**: Remove the *Worked sub-case* paragraph.

### Issue 8: Repeated S8 discharge across K.μ⁺/K.μ⁻/K.μ~ cases
**ASN-0047, ExtendedReachableStateInvariants (Class (a))**: The S8 verification — naming preconditions S2, S3, S7b, S7c, S8a, S8-depth, S8-fin and the foundation-layer dependencies — is restated near-verbatim in K.μ⁺, K.μ⁻, and K.μ~ cases. The *S8-scope in the extended state* note and *Link-subspace correspondence-run structure — out of scope* note together repeat much of the same content again.
**Problem**: Three identical discharge blocks; a single S8 detail change would require multiple edits. The *correspondence-run structure — out of scope* note is ~1000 words explaining that S8 applies via content-subspace projection.
**Required**: Factor S8 discharge into a single lemma ("S8 over the content-subspace projection holds when S2/S3★/S7b/S7c/S8a/S8-depth/S8-fin all hold at Σ'") cited from each transition case in one line; collapse the *S8-scope* and *correspondence-run* notes into the same lemma's statement.

### Issue 9: K.μ~ corollary placement justifications
**ASN-0047, Decomposition of K.μ~ (Link-subspace fixity under K.μ~)**: The corollary opens with a paragraph justifying its placement before the decomposition cases. The same content recurs in *K.μ~ — contract* ("Listing S3★(Σ') in admissibility makes subspace preservation a derived consequence...") and in *Invariant preservation under K.μ~* ("Link-subspace fixity is *not* invoked..."). Across the K.μ~ section, ~1500 words of placement/dependency commentary surround ~1000 words of derivation.
**Problem**: Document-ordering and forward-reference prose compounds across cross-references — the pattern flagged in the anti-bloat note. Multiple paragraphs defer to the same downstream location.
**Required**: Reorder the K.μ~ section so structural dependencies are in linear order and remove the dependency-commentary prose.

### Issue 10: Properties Introduced table commentary
**ASN-0047, Properties Introduced**: Three paragraphs explain the partition into "New properties", "Local extensions and strengthenings", "Foundation restatements" — including what each subsection contains and which foundation properties are or aren't restated.
**Problem**: The partition is self-evident from headings and contents. The commentary is meta-content explaining the table.
**Required**: Remove the commentary paragraphs; attach any per-subsection rationale as one-line notes to the relevant headings.

## OUT_OF_SCOPE

None. The ASN respects its declared scope exclusions; deferred topics (tombstoning, version semantics, withdrawal invariants, account-level k = 1, non-T10a allocators) are properly named in *Open Questions*.

VERDICT: REVISE
