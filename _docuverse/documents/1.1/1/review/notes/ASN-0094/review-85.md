# Review of ASN-0094

The ASN carries the `review-mode.anti-bloat` classifier, and the patterns it warns about are present at scale. The mathematical content is largely sound — Sh0–Sh4, FDD, SHCD preservation arguments check out — but the prose around forward references, axioms, and case enumerations has accumulated. I focus on the highest-impact patterns plus one technical gap.

## REVISE

### Issue 1: Sh-conf admission's "biconditional" wording explains why the axiom is structured rather than stating what it says
**ASN-0094, Conformance Axiom section**: "If `Emit_K(Σ, d, F, G)` is Sh-conf-admissible, then `d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G)`. The biconditional defining Sh-conf-admissibility (admission iff the three conjuncts hold) is the substrate's own characterization of the Sh-conf gate's decision procedure; the framework consumes only the forward direction..."
**Problem**: A biconditional is named but never stated, and a paragraph explains why only the forward direction is needed. This is reviser drift — meta-prose justifying the axiom's structure rather than asserting it. The exact pattern called out at the head of the review (new prose around an axiom explains why it is needed rather than what it says).
**Required**: State the axiom as a definition: "Emit_K(Σ, d, F, G) is Sh-conf-admissible iff d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G); on inadmissibility, Emit_K returns ⊥." Drop the "the framework consumes only the forward direction" reasoning.

### Issue 2: RetractionSelfFreshness Precondition 3 mixes precondition with consequence
**ASN-0094, Lemma — RetractionSelfFreshness**: "Gates 0–4 all admit the `Emit_R(Σ, d, F, G)` call, so the call proceeds to K.λ at home `d` (gate 5) and deposits a fresh tuple τ_new... Consequently: under R's registration `shape(R) = (*, 1, A, A_rel, ⊤)` (Precondition 2), R is Sh4-registered via the framework's *Sh4 idempotency contract*..., so gate-3 admission entails Sh4's clause (i) check `C(F_{τ_new}, G_{τ_new}, Σ) = ∅` already passed at gate 3 — not as an additional condition imposed by this precondition but as a consequence of gate-3 admission's evaluation procedure."
**Problem**: The "Consequently:" half is defensive justification for why properties cited in the proof are already discharged by gate-3 admission. The lemma's actual precondition is simply "gates 0–4 admit"; the rest belongs in the proof body where the facts are used.
**Required**: Reduce Precondition 3 to "Gates 0–4 admit the `Emit_R(Σ, d, F, G)` call, producing fresh tuple τ_new at state Σ'." Move the Sh4-contract clause discharge into the proof's part (i) where it's invoked.

### Issue 3: "Gate 5" mislabels the K.λ emission step
**ASN-0094, Conformance Axiom section, Gate Ordering**: "5. **Substrate primitive K.λ** (ASN-0086): the call invokes K.λ at home `d` with value `(F, G, K)`. K.λ's first/subsequent-emission protocol fires..."
**Problem**: Gates 0–4 are pass/reject gates. Gate 5 is not a gate — it's the emission. The framework returns once gate 5 fires; nothing rejects. The "six-gate sequence" framing (also in the recent commit message) is misleading — there are five gates plus an emission. Subsequent prose ("if gate 5 fires...") then has no meaning since gate 5 cannot fail.
**Required**: Restructure as "Gates 0–4 followed by K.λ emission." Drop "gate 5" wording; reword references to "after gate 4 admits, the call invokes K.λ."

### Issue 4: Sh-conf Rejection Patterns omits d ∉ dom(Σ.M)
**ASN-0094, Sh-conf Rejection Patterns**: Catalog has four patterns: non-canonical slot endset, unallocated slot target, cardinality mismatch, unregistered type.
**Problem**: Gate 0 is described as testing two conjuncts (`K ∈ T_cat` and `d ∈ dom(Σ.M)`), and the gate-0 prose says "On failure of either conjunct (`K ∉ T_cat` or `d ∉ dom(Σ.M)`)". But only the `K ∉ T_cat` case is catalogued (Pattern 4). The `d ∉ dom(Σ.M)` rejection has no pattern entry. The walkthroughs cite "by reference" but the reference is incomplete.
**Required**: Add a fifth pattern for d ∉ dom(Σ.M), or note in Pattern 4's body that gate-0 failures of either conjunct fall under it. The current asymmetry is a documentation gap.

### Issue 5: Case A enumeration duplicated across Sh4, FDD, and SHCD preservation proofs
**ASN-0094, Sh4 / FDD / SHCD preservation proofs**: Each "Case A" enumerates the same four ↦-step classes (K.σ/K.α, K.λ at K' ≁ K and K' ≁ R, K.λ at K' ≁ K and K' ~ R, arrangement-modifying) with case-equation discharge for each. The FDD and SHCD proofs explicitly say "paralleling Sh4's Case A enumeration" but reproduce the enumeration verbatim with minor variation.
**Problem**: Three near-identical 4-class enumerations. CaseAClosureForLK already handles L_K-level closure for Sh0–Sh3; the A_K-level / L_K-side-stable closure used by Sh4, FDD, SHCD has no shared lemma and is re-derived three times.
**Required**: Lift the A_K-closure / L_K-side-stable case enumeration into a shared lemma (or extend CaseAClosureForLK to cover both regimes), and have Sh4/FDD/SHCD cite it rather than re-deriving. The current structure is a maintenance hazard and an instance of relocation-rather-than-removal.

### Issue 6: Forward-reference accretion around EffectiveWpSimplification
**ASN-0094, multiple sections**: Sh-conf section: "The framework's full success condition... is the `wp_eff` of Corollary — EffectiveWpSimplification below." Retraction shape section: "ASN-0086's wp simplification under regime (i) applies to every Sh-conf-admitted Retraction emission..." Lemma — LinkAddressNotPrefixOfEmit is hoisted with a preamble explaining its two downstream consumers. NoCraftedSpanReachesD discharge is mentioned in three different places.
**Problem**: Multiple sections defer to the same downstream location with overlapping defensive prose. Each deferral re-establishes context the corollary will discharge. The pattern is exactly the one flagged in the review prompt: "multiple paragraphs in different sections defer to the same downstream location."
**Required**: Concentrate the wp-simplification machinery in one location (the corollary). Other sections cite by label without re-justifying. Drop the preamble paragraphs that explain why LinkAddressNotPrefixOfEmit is hoisted to a top-level section.

### Issue 7: Per-walkthrough convention reiterated in every walkthrough
**ASN-0094, every walkthrough subsection**: "Per the Per-walkthrough convention. Pre-allocate..." or similar phrasing appears in Classifier, Tuple-Classifier, FDD worked example, Resolution, BundledDirectedPair, NonIdempotentDirectedPair under SHCD, Provenance, and the K=comment worked example.
**Problem**: The convention is defined once in Initial-State Baseline ("Every walkthrough below assumes: ..."). Each walkthrough then re-cites it before pre-allocating. The repetition is mechanical filler.
**Required**: State the convention once at the head of "Per-Shape Template Walkthroughs"; drop the per-walkthrough citation. Walkthroughs can directly say "pre-allocate ..." without the throat-clearing.

### Issue 8: AllocatedAddressAntichain Step 3.2 contains apologetic meta-prose
**ASN-0094, AllocatedAddressAntichain lemma proof, Step 3.2**: "The E-field of `x` is non-empty (we need only `#E(x) ≥ 1`, not the stronger `≥ 2` from L1b or its content-side analog, since Step 3.2's conclusion uses only the first position of `E(x)`)..."
**Problem**: The parenthetical explains why the proof doesn't need the stronger bound L1b supplies. This is defensive justification — the reader has the proof in hand and doesn't need to be told what isn't being used. The pattern is "imagining a case the claim's carrier already excludes."
**Required**: Strip the parenthetical. The proof works at `#E(x) ≥ 1`; the reader will see this. The "stronger ≥ 2" comparison adds no content.

### Issue 9: Tuple-Classifier's "single-letter substitution" misdescribes the change from Classifier
**ASN-0094, Tuple-Classifier section**: "The single-letter substitution `d ↝ τ` from Classifier's template body is the only difference; signature changes from `A_doc → Bool` to `A_rel → Bool`."
**Problem**: Classifier's body is `is_K(d) ≡ (E τ ∈ A_K^Σ :: to₁(τ) = d)`; Tuple-Classifier's is `is_K(τ) ≡ (E σ ∈ A_K^Σ :: to₁(σ) = τ)`. The actual change is (a) parameter renamed `d → τ`, (b) bound variable renamed `τ → σ` to avoid capture, (c) signature change. The "single-letter substitution `d ↝ τ`" phrasing obscures the bound-variable renaming and would mislead a reader writing other shape-mate templates.
**Required**: Either describe the substitution accurately (rename parameter and rename bound variable to avoid capture) or drop the framing and let the formal body speak.

### Issue 10: Properties Introduced table duplicates body content
**ASN-0094, Properties Introduced section**: Two tables (load-bearing claims, supporting definitions) re-state every named lemma/axiom/definition from the body with one-line summaries.
**Problem**: The table adds no content beyond the body's section headers and Statement entries. Each entry is essentially a section pointer with a restatement. The classification (load-bearing vs supporting) is the only new content — and most claims are obviously load-bearing where they're proved.
**Required**: Reduce to a navigation aid: a single list of named claims with section anchors, no restated statements. Or drop entirely and rely on the body's named-section organization.

## OUT_OF_SCOPE

### Topic 1: Three-way split (framework / disciplines / catalog)
**Why out of scope**: The MEMORY index records that review-30 recommended a 3-way split and the reviser punted to operator. Split decisions are operator-level architectural calls, not single-cycle revisions; this review does not re-litigate.

### Topic 2: Multi-process substrate semantics for Sh4/FDD/SHCD contracts
**Why out of scope**: The framework explicitly restricts itself to single-process substrates and lists this as an open question. Extending to multi-process would require a distributed coordination protocol — a new ASN's worth of work.

### Topic 3: `A_M` target-domain symbol for `dom(Σ.M)` (container addresses)
**Why out of scope**: Acknowledged in Open Questions. Adding `A_M` would enable Nelson-style metalink targeting; this is a substrate-extension decision, not a revision to the current framework.

### Topic 4: Cardinality vocabulary expansion (1..*, etc.)
**Why out of scope**: The vocabulary `{0, 1, *, 0|1}` is acknowledged as not expressing `1..*`. Whether to extend the vocabulary is a design choice for future shape additions, not a current-cycle revision.

VERDICT: REVISE
