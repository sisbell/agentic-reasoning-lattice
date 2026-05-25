# Review of ASN-0094

## REVISE

### Issue 1: Defensive justification of walkthrough curation depth
**ASN-0094, Per-Shape Template Walkthroughs / "Coverage of the walkthroughs"**: The paragraph beginning "The per-shape walkthroughs do not exhibit uniform depth across the catalog..." explains why Resolution, Retraction, and Provenance lack standalone walkthroughs ("structurally identical to Classifier modulo a t_G substitution", "exercised end-to-end as K_res in the Comment walkthrough", "structurally simpler than DirectedPair").

**Problem**: This is the "defensive justifications" anti-bloat pattern — meta-prose explaining catalog curation choices that does not advance the framework's argument. A reader who needs the framework's claims learns nothing from being told why some walkthroughs are shallow.

**Required**: Either remove the paragraph, or relocate its content as brief inline notes at each shape's section ("exercised in the Comment walkthrough" at Resolution, etc.).

### Issue 2: Defensive scope-justification at Sh4 Case A enumeration
**ASN-0094, Sh4 — IdempotencyDiscipline / Step (Case A)**: After enumerating the four classes, a concluding paragraph reads "The enumeration is exhaustive for *Case A coverage* within the framework's ↦-vocabulary... Transition classes the full Xanadu substrate may admit at scopes outside this framework's commitment (e.g., publication-state transitions, BEBE topology migrations) lie outside ↦'s vocabulary and so outside Sh4's preservation scope by construction."

**Problem**: The second sentence imagines transitions outside the framework's vocabulary to deflect anticipated objections — "a paragraph imagines a case the claim's carrier or precondition already excludes" (anti-bloat pattern). The framework's ↦-vocabulary is defined; transitions outside it are not in scope, and the parenthetical examples drag in concrete substrates (BEBE) the framework does not name elsewhere.

**Required**: Remove the second sentence.

### Issue 3: Meta-prose about word "literal" in Decidable membership
**ASN-0094, Definition — TypedRelationCatalog / Decidable membership**: The closing paragraph reads "The membership predicate is therefore *not* a literal-equality test on the endset value K itself... the word 'literal' applies to the registry's representative list (literally enumerated) and to the well-definedness of the check (no state-indexed quantification), not to the comparison operation on endsets..."

**Problem**: Two paragraphs in the same passage say the same thing in different words (anti-bloat pattern). The first paragraph already establishes that membership is a coverage-equivalence check; the second exists to explain the word "literal" used in subsequent prose.

**Required**: Trim the second paragraph to a parenthetical, or fold the clarification into the first description directly (e.g., "decidable as the coverage-equivalence check `coverage(K) = coverage(K_rep)` against each registered representative").

### Issue 4: NullifyActiveSubsetCompatibility Case B witness selection is under-justified
**ASN-0094, Corollary — NullifyActiveSubsetCompatibility / Case B**: The proof in suppress-case reads "Pick τ_prior ∈ C; slot_addrs(G_{τ_prior}) = {a} forces a ∈ coverage(G_{τ_prior})..."

**Problem**: `C(F, G, Σ)` is the bare-Nullify candidate set (matches `slot_addrs(F_τ) = ∅ ∧ slot_addrs(G_τ) = {a}`). The argument silently relies on the Sh4-suppression hypothesis to populate `C`. But the stated postcondition `a ∈ nullified(Σ)` is more general — it would hold even if some attributed retraction of `a` exists with `C = ∅`. The proof only handles the path where the suppression witness is a prior bare Nullify; this is correct (because suppression requires C ≠ ∅, which requires a bare-form witness), but the reasoning chain "Sh4 suppresses ⟹ bare witness exists in C ⟹ a ∈ nullified" should be stated explicitly so the reader does not have to reconstruct it.

**Required**: One additional sentence between the suppression hypothesis and the witness selection: "By the Sh4 contract clause (ii) precondition `C ≠ ∅`, at least one τ_prior ∈ A_R^Σ exists with slot_addrs(F_{τ_prior}) = ∅ and slot_addrs(G_{τ_prior}) = {a}."

### Issue 5: AllocatedAddressAntichain Case 3b dispatched as "symmetric"
**ASN-0094, Lemma — AllocatedAddressAntichain, Case 3**: "Sub-case 3b is symmetric (swap link/content side labels; the disjointness predicate s_L ≠ s_C is symmetric)."

**Problem**: The reviewer's standard "No proof by 'similarly'" applies here. While the symmetry is genuine, the proof's Step 3.2 invokes T4a + T4b + T4c "uniformly to element-level addresses without reference to subspace identifier" — but Step 3.3 then breaks the symmetry by citing different scaffolding clauses for x's and a's subspace identifier. In 3b, the citation roles swap: link-side scaffolding gives E(a).1 = s_L and content-side gives E(x).1 = s_C. The swap is mechanical, but stating it makes the dispatch verifiable.

**Required**: Replace the parenthetical with one explicit line: "Sub-case 3b: by symmetry, the link subspace partition gives E(a).1 = s_L and the content subspace partition gives E(x).1 = s_C; Step 3.2's componentwise agreement still yields E(x).1 = E(a).1, contradicting s_L ≠ s_C."

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate consistency
**Why out of scope**: Explicitly flagged in Open Questions as a `[scope boundary]`. The framework's Sh4 and FDD contracts commit to single-process substrates by design; multi-process consistency requires a coordination protocol outside the current framework.

### Topic 2: Container-level link targeting (`A_M`)
**Why out of scope**: Explicitly flagged in Open Questions as a `[scope boundary]`. Adding a target-domain symbol for `dom(Σ.M)` would extend the catalog vocabulary; the framework follows the implementation's element-level-only restriction.

### Topic 3: Composite shapes
**Why out of scope**: Explicitly flagged in Open Questions. The framework's atomic vocabulary is the canonical-shape catalog; structurally new patterns are handled by extending the catalog, not by composition.

### Topic 4: Non-empty initial link store baselines
**Why out of scope**: Explicitly flagged in Open Questions as a `[scope boundary]`. Sh0–Sh3 hold under per-tuple-conformance at Σ_init; Sh4/FDD/SHCD's preservation theorems require empty initial state and would need per-K baseline-verification at registration time to extend.

### Topic 5: Ghost-targeting slot semantics
**Why out of scope**: Explicitly flagged in Open Questions as a `[design choice]`. The framework restricts slot addresses to allocated targets; ghost-targeting slots would require a state-dependent conformance rule extending the framework.

### Topic 6: Body uniformity enforcement for catalog templates
**Why out of scope**: Acknowledged in Consequences (a) — what the framework does *not* derive is per-shape template body shape. The Catalog Curation Discipline is hand-curated by author convention, not mechanically enforced. Enforcing body uniformity would require a meta-language over template bodies, outside the current framework.

VERDICT: REVISE
