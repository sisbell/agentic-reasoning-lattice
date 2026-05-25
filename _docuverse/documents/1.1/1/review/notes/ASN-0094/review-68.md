# Review of ASN-0094

## REVISE

### Issue 1: Forward-reference accretion is severe

**ASN-0094, throughout**: The document exhibits the accretion patterns the framework's own classifier flags. Specific instances:
- *"Common rejection patterns (canonical references)"* — a preemptive essay explaining how later rejections cross-reference earlier ones (Pattern 1–6 enumeration before any rejection is exhibited).
- *"Per the *Convention for per-walkthrough registered-catalog declarations*"* deferrals in every walkthrough.
- *"Catalog row naming policy"* — essay paragraph on structural vs semantic naming.
- *"Naming conventions are layer constructs, not catalog rows"* — defensive disclaimer.
- *"Routing Failure Modes"* — enumerates consequences without a substantive check.
- *"Per-class constancy is then *automatic from the registration interface*"* + extensive justification of why constancy holds.
- *"Locally derived NAT primitives and framework-local Peano-style axioms"* preamble + *"Scope decision: framework-local vs upstream into ASN-0034"* + *"Practical alternative — restructure derivations to avoid supplements — rejected"* — three paragraphs justifying a design decision rather than advancing it.
- The Sh4 contract's *"Scope: single-process substrate"* paragraph and the structurally equivalent FDD contract's atomicity-scope reading restate the same point.
- *"Stratification"* clauses in Sh2, Sh3, Sh4, FDD, and SHCD preservation arguments each individually enumerate the consumption of Sh0–Sh3.
- The Sh-conf section's *"Failure modes under contract violation"*, *"Why a layer-level contract rather than a substrate-level axiom"*, and *"Why this is strictly stronger than Sh4"* paragraphs all explain motivation rather than content.

**Problem**: Reviser drift across cycles. Many paragraphs defer to other paragraphs, restate prior decisions, or justify scope boundaries rather than advance argument. The reader must skip past meta-prose to follow claims.

**Required**: Remove justifications that don't advance reasoning. Consolidate canonical references (a single "Common rejection patterns" entry per pattern, cited by name in walkthroughs). Eliminate "Status" / "Why" / "Failure modes" sub-paragraphs that restate META status or motivation already established.

### Issue 2: Sh5(b) status equivocation

**ASN-0094, Sh5 section**: "Sh5(b) is a hand-followed convention, not a framework-enforced gate. Both Sh5(a) (per-shape uniformity) and Sh5(b) (six-category citation rule) are design conventions enforced by catalog-author diligence, not by any framework-supplied tool."

**Problem**: Sh5(b) is variously called a "discipline" (multiple sites), "convention" (the downgrade paragraph), "META observation" (the Sh5 status preamble), and "aspiration" (Sh5(a)'s downgrade). The downgrade undermines downstream consequence claims like *"Adding a new relation generates predicates for free"* (Consequences section) — that consequence depends on per-shape uniformity, which is now aspirational. Subsequent prose still treats the audit table as authoritative ("Catalog-wide citation audit").

**Required**: Either (a) commit to Sh5(b) as a framework-enforced gate (with tooling), or (b) explicitly weaken downstream consequences to "the present catalog supplies these templates by hand-curation" rather than "the shape generates them." Pick one reading and propagate.

### Issue 3: Audit-slice set-semantics commitment is a substantive semantic change tucked into the Nullify section

**ASN-0094, Nullify Compatibility section**: "Under this framework, two consecutive bare-form `Nullify(Σ, d_retr, a)` calls at the same target `a` produce *only one* tuple in `L_R^Σ` — not two."

**Problem**: ASN-0086's Nullify was specified as if it always produces a fresh `(Σ', _)` pair. The framework's choice `shape(R).idem = ⊤` changes this. NullifyActiveSubsetCompatibility documents that active-subset content is preserved across the issue/suppress branches, but audit-slice multiplicity is *not* preserved — a deliberate semantic departure. This is buried in a sub-section of Nullify Compatibility despite being one of the framework's most consequential commitments.

**Required**: Hoist the commitment to the framework's main introduction. State at the document's top that the framework changes ASN-0086's apparent multiset semantics at R to set semantics, with attributed retraction as the multiset-preserving migration path.

### Issue 4: Three Peano-style axioms introduced framework-locally but tucked into the appendix

**ASN-0094, Properties Introduced table**: Lists (Peano-rec), (Peano-zero-least), (Peano-pred) as *introduced* alongside Sh-conf, Sh0–Sh5.

**Problem**: The framework extends ℕ's axiom base with three new commitments. The non-derivability arguments are sound, but the introduction is buried in the appendix. A reader scanning the body wouldn't notice that the framework adds three axioms.

**Required**: Surface the three axioms at the document's main level (e.g., a brief "Foundation extensions" subsection in Scope and Substrate Scaffolding), with the detailed derivations remaining in the appendix.

### Issue 5: LinkAddressNotPrefixOfEmit doesn't cite TA5a explicitly

**ASN-0094, LinkAddressNotPrefixOfEmit, Case II preamble**: "subsequent-emission `a = inc(ℓ_prev, 0)` preserves zeros (TA5(c), ASN-0034, modifies only position `sig(ℓ_prev)`, and on T4-valid `ℓ_prev` ... the sig position carries a non-zero value whose incremented value remains non-zero)"

**Problem**: T4-validity of `a = inc(ℓ_prev, 0)` is what the proof actually needs (for T4b's positional projections, T4a's E-field segment formula). TA5(c) gives length and positional change but doesn't give T4-validity. The correct foundation citation is TA5a (IncrementPreservesT4), which establishes preservation of T4 under `inc(·, 0)`. The proof argues equivalent content inline but fails to cite the named theorem.

**Required**: Cite TA5a explicitly where T4-validity of `inc(ℓ_prev, 0)` is asserted (both in the Case II preamble and in Step II.2's "both `b` and `a` are T4-valid" identification).

### Issue 6: "Reach of the framework's target-domain symbols" restriction is substantive but relegated to a note

**ASN-0094, Canonical Shape Catalog section, Reach note**: "Throughout this catalog, `A_doc` denotes content addresses (per ASN-0086, `A_doc^Σ = dom(Σ.C)`), *not* document-level container addresses (which live in `dom(Σ.M)` ...). The framework provides no target-domain symbol for `dom(Σ.M)` addresses."

**Problem**: This is a significant expressiveness limitation — relations cannot directly target document containers. Layers must record relations against a "document head" content address as a workaround. The note appears once, mid-document, and isn't traced through the walkthroughs (e.g., the Comment walkthrough's `d_1, d_2` are described as "documents" but are really content addresses).

**Required**: Either (a) extend the target-domain vocabulary to admit `dom(Σ.M)` (e.g., add an `A_M` symbol), or (b) make the workaround explicit throughout the walkthroughs ("`d_2` is a content address within document container `D_2`").

### Issue 7: Caller-side rejection classification protocol is tucked into a callout box

**ASN-0094, Sh-conf section, Caller-side rejection classification**: A caller-side six-step protocol for disambiguating Sh-conf rejection from per-K-discipline suppression.

**Problem**: This is the operational interface for callers wanting to verify pre-call that `wp_eff` will hold. It's described as a side-effect-free protocol but presented as a sub-paragraph within Sh-conf rather than as a first-class definition.

**Required**: Promote the protocol to a named Definition or Lemma (e.g., "Definition — CallerSideClassification") so callers can reference it directly. Alternatively, fold its content into the framework's effective-wp formulation.

### Issue 8: Repeated stratification clauses

**ASN-0094, Sh2/Sh3/Sh4/FDD/SHCD preservation arguments**: Each lemma's *"Stratification"* clause enumerates Sh0–Sh3 consumption with slight variations.

**Problem**: Reviser drift. The stratification structure (Sh0/Sh1 independent → Sh2/Sh3 consume them → Sh4 consumes Sh0–Sh3 + RetractionSelfFreshness → FDD/SHCD consume Sh0–Sh3) is the same across consumers but stated five times.

**Required**: State the stratification once at framework level (e.g., a "Stratification" subsection after Sh-conf) and reference from each lemma.

### Issue 9: Mutual exclusion of FDD and SHCD stated in multiple places

**ASN-0094, Gate Ordering section + FDD section + SHCD section + Per-K opt-in registry paragraph + consolidated commitment reference table**: The fact that FDD requires `idem = ⊤` and SHCD requires `idem = ⊥` is repeated five times across the document.

**Required**: State once (e.g., in the Per-K opt-in registry paragraph) and reference.

### Issue 10: BundledDirectedPair's empty-G admissibility paragraph is essay-like

**ASN-0094, BundledDirectedPair section, Empty-G admissibility paragraph**: A long paragraph justifying that `c_G = *` admits `n = 0`, with extensive design rationale ("symmetric counterpart to Retraction") rather than substantive content.

**Required**: Condense to the operational fact ("`c_G = *` admits `n = 0` per `match(0, *)`") plus a one-sentence note on the asymmetry with Retraction.

## OUT_OF_SCOPE

### Topic 1: Higher-arity links

**Why out of scope**: The framework explicitly restricts to standard-triple slice `L^Σ` (arity-3 links). Extending to higher arities requires per-extra-slot shape components — new ASN territory.

### Topic 2: Ghost-targeting slot semantics

**Why out of scope**: L9 admits ghost spans in endsets generally; the framework restricts slot positions to allocated addresses. A future shape family admitting ghost-targeting under a state-dependent conformance rule would extend the framework's expressiveness.

### Topic 3: Composite shapes (shapes whose F or G is constrained by another relation's content)

**Why out of scope**: The current shape vocabulary is five components; composite shapes would require new restriction axes.

### Topic 4: Cross-process consistency

**Why out of scope**: The framework commits to single-process substrates. Multi-process Sh4-emitter coordination would require a distributed lock protocol outside the framework.

### Topic 5: Generalization of FDD to other `c_F = 1` shapes

**Why out of scope**: The current draft attaches FDD only to DirectedPair. Generalization to other shapes (e.g., FDD at Resolution's `(1, 1, A_doc, A_rel, ⊤)`) is admissible but not exercised.

### Topic 6: Catalog completion across the cardinality lattice

**Why out of scope**: The catalog enumerates the rows demanded by present-day predicates. The full cardinality lattice `(c_F, c_G) ∈ {0, 1, *, 0|1}²` has 16 combinations; only 7 are catalogued. Future demands can drive catalog extensions.

META: ASN-0094's substantive content is the shape discipline atop ASN-0086 — it remains within specification territory (state restrictions, conformance axiom, preservation theorems, accessor totality) and does not drift into implementation mechanics; the framework's work is well-aimed.

VERDICT: REVISE
