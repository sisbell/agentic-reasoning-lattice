# Review of ASN-0094

## REVISE

### Issue 1: Lemma-placement meta-prose
**ASN-0094, "Lemma — LinkAddressNotPrefixOfEmit" opening**: "This lemma bridges Sh-conf's structural gates to wp_086 simplification at Retraction-typed emissions. Independent of Sh0–Sh4."
**ASN-0094, "Lemma — RetractionSelfFreshness" opening**: "Independent of Sh4's preservation argument (cited downstream by Sh4 Case C and Case D), and structurally parallel to LinkAddressNotPrefixOfEmit's placement before Sh0."
**Problem**: Both openings justify *where* the lemma sits rather than state what it says. The "structurally parallel to LinkAddressNotPrefixOfEmit's placement" line is naked meta-prose about author choice.
**Required**: Open each lemma with its statement. Drop the placement narration.

### Issue 2: Repetitive forward references to per-K contracts
**ASN-0094, Sh4 definition**: "conditional on the *Sh4 idempotency contract* (defined below; the contract's clauses (i)–(iii) gate every Emit_K call site for such K)."
**ASN-0094, FDD definition**: "conditional on the *FDD functional-dependency contract* (defined below; the contract's clauses (i)–(iii) gate every Emit_K call site for FDD-registered K)."
**ASN-0094, SHCD definition**: "conditional on the *single-home commitment* (defined below; the contract's clauses (i)–(ii) gate every Emit_K call site for SHCD-registered K)."
**Problem**: The same defer-to-below pattern repeats three times, each pointing at a contract sitting in the same subsection. The contracts also appear in the named-commitments table in Sh-conf, the consolidated gate ordering, and the substrate-conforming-layer Definition.
**Required**: Define each discipline and its contract in one block. Drop the parenthetical forward pointers.

### Issue 3: Catalog Curation Discipline as organizational essay
**ASN-0094, "Catalog Curation Discipline" section**.
**Problem**: This entire section meta-explains the catalog's status ("hand-curated under three rules enforced by catalog-author diligence") with citation-category lists (six categories under rule 3). It is governance prose about the catalog tables, not framework content. The ASN itself concludes elsewhere: "The framework's actual content is therefore Sh-conf + Sh0–Sh4 + the layer-discipline contracts; the catalog and template families are an organizational layer on top."
**Required**: Fold the discipline rules into the catalog table introduction (one paragraph), or move to an appendix. Either way, the section as a separate structural slot should go.

### Issue 4: Catalog table "Template family" column carries use-site inventories
**ASN-0094, "Canonical Shape Catalog" table**.
- Retraction row: "*primary consumption:* by ASN-0086's `nullified(·)` definition, which reads each `L_R`-tuple's G-coverage directly over the audit slice…"
- Resolution row: "*dominant downstream pattern:* parametric consumption by NonIdempotentDirectedPair's `_via` templates…"
- BundledDirectedPair row: full paragraph on "Coverage class disjointness from R by shape-tuple inequality…" inside a table cell.
- NonIdempotentDirectedPair row: opt-in and parametric extensions enumerated inline.
**Problem**: The column does triple duty (templates, downstream consumers, design rationale). A definition's column should not enumerate its consumers — that is use-site inventory in a structural slot.
**Required**: List templates only in the column. Move consumption notes into per-shape prose if load-bearing.

### Issue 5: "Gate Ordering (consolidated)" duplicates per-K ordering clauses
**ASN-0094, Sh-conf section, "Gate Ordering (consolidated)" subsection** enumerates five gates with per-K dispatch.
**ASN-0094, FDD section, SHCD section**: each carries its own "Ordering with Sh-conf" clause, also referenced from the Sh-conf named-commitments table.
**Problem**: Two paragraphs in different sections say the same thing in different words. The reader has to reconcile the consolidated view against the distributed view.
**Required**: One canonical location. Either consolidate at Sh-conf (drop per-K ordering clauses) or distribute (drop the consolidated section).

### Issue 6: BundledDirectedPair migration essay
**ASN-0094, BundledDirectedPair section, "Backward compatibility with legacy single-target emissions" paragraph**: walks through how a layer migrates from `c_G = 1` to `c_G = *`, invoking per-class constancy and lifetime constancy of `shape(·)`, concluding with the recipe "must declare the relation at `c_G = *` from `Σ_init` to recover both regimes under one row."
**Problem**: This is migration recipe content inside a shape catalog row. The migration is a layer concern, not a framework property. The shape's definition does not need this exposition.
**Required**: Drop. The shape stands on its own; layers manage their own migrations.

### Issue 7: Defensive prose around scaffolding clause limitations
**ASN-0094, "Substrate-conforming-layer scaffolding", Link subspace partition clause**: "Local commitment consistent with L0: identifies `subspace_I(·) = E(·).1` on link-side element-level addresses. Not derivable from L0 alone — L0 treats `subspace_I(·)` as uninterpreted. The two partition clauses adopt this identification framework-wide; substrates surfacing `subspace_I` via a different projection lie outside the framework's scope."
**Problem**: The clause itself is one line; the paragraph pre-empts an objection ("Not derivable from L0…") and bounds the framework's scope per-clause.
**Required**: State the clause. Put scope statements once at framework level.

### Issue 8: Per-walkthrough convention restated in every walkthrough
**ASN-0094, "Initial-State Baseline"**: defines `Per-walkthrough convention` (T_cat, R registered, `L_K^{Σ_init} = ∅`, `dom(Σ_init.L) = ∅`).
**ASN-0094, Classifier walkthrough**: "with `dom(Σ_0.L) = ∅` so K.λ's first-emission branch fires".
**ASN-0094, BundledDirectedPair walkthrough**: "with `dom(Σ_0.L) = ∅`".
**ASN-0094, Comment walkthrough**: "The walkthrough's `Σ_0` is reached from `Σ_init` by a finite sequence of K.σ/K.α steps (no K.λ-steps), so `dom(Σ_0.L) = ∅`."
**Problem**: Convention is established once. Every walkthrough then restates pieces of it inline.
**Required**: Cite the convention by reference. Walkthroughs name only their own additions.

### Issue 9: Sh-conf section is structurally fragmented
**ASN-0094, "The Conformance Axiom" section**: Sh-conf axiom statement (~one paragraph), followed by Definition — LayerCallableCandidateSets, a `*Scope.*` paragraph, then `*Gate Ordering (consolidated).*` with five numbered gates and a closing dispatch table.
**Problem**: The axiom is short; the surrounding machinery (candidate-set queries, scope clarification, gate ordering, commitments table) sprawls. The candidate-set Definition is used only by the per-K contracts that follow; it could live with them.
**Required**: Tighten. The Sh-conf section should be the axiom plus what its preconditions denote. Move the candidate-set queries to the per-K discipline subsections that consume them.

### Issue 10: Comment walkthrough's four rejection cases as canonical references
**ASN-0094, "Worked Example: K = comment", Rejection cases 1–4**: each a full walkthrough of one Sh-conf failure mode (non-canonical slot, unallocated target, cardinality mismatch, unregistered type). The section opener explicitly says these are "canonical references" for the four bare-Sh-conf patterns.
**Problem**: Sh-conf's failure modes deserve their own canonical demonstration at the Sh-conf section, not buried in a per-K shape walkthrough. The Comment walkthrough should exercise what is distinctive about NonIdempotentDirectedPair (non-idempotency, the `_via` parametric extension); it instead absorbs the framework's failure-mode catalog.
**Required**: Lift the Sh-conf failure-mode cases to a single canonical block at Sh-conf. Keep the Comment walkthrough on shape-distinctive content.

### Issue 11: Scaffolding terminology ambiguity on "chain"
**ASN-0094, "Per-document link sub-allocator chains" clause**: "the layer supplies a link sub-allocator whose output chain enumerates `{ℓ : home(ℓ) = d}`."
**ASN-0094, "Link sub-allocator chain-index function" clause**: "for each chain element `ℓ`, the layer supplies a total `chain_index(ℓ, d)`."
**ASN-0094, Lemma — LinkAddressNotPrefixOfEmit, Case I**: "Both `b` and `a_emit(Σ, d)` are chain elements of `A_L(d)`."
**Problem**: "Chain" is used for both the current finite homed-prefix (per R0a-Cor1) and the abstract infinite enumeration (per T10a). The lemma proof references `inc^{J_d^Σ + 1}` — an address in the abstract chain but not in the current homed set. The scaffolding clauses do not distinguish, and `chain_index`'s domain is unclear.
**Required**: Fix the terminology — distinguish abstract chain (`dom(A_L(d))`) from current realized prefix. Pin `chain_index`'s domain explicitly.

### Issue 12: ASN scope — framework / disciplines / catalog still bundled
**ASN-0094 overall**: ~43K words covering framework axioms + Sh0-Sh4 + four supporting lemmas + three per-K contracts + canonical catalog + per-shape walkthroughs + Comment worked example + Consequences + Open Questions. Previously flagged for 3-way split (framework / disciplines / catalog).
**Problem**: The framework content (Sh-conf, preservation theorems, lemmas, contracts) is spec-level and is what downstream consumers cite. The catalog and per-shape walkthroughs are organizational layered content. Bundled, they make the spec hard to extract and the catalog hard to evolve. Memory carries the prior split recommendation; the post-discovery split gap has not been closed.
**Required**: Execute the 3-way split. Land the framework as the load-bearing ASN; carry the catalog and walkthroughs as separate organizational ASNs.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate consistency
The framework is explicitly committed to single-process substrates (Sh4/FDD/SHCD atomicity reduces to within-call sequencing). A multi-process extension (with cross-process coordination at the `~`-class scope) is genuinely new content for a future ASN.

### Topic 2: Non-empty initial link-store baseline
Sh4/FDD/SHCD preservation theorems presuppose `L_K^{Σ_init} = ∅`. Relaxing this requires per-K baseline verification at registration time — a genuine framework extension, not a revision.

VERDICT: REVISE
