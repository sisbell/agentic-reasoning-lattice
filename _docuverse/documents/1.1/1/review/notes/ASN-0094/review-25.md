# Review of ASN-0094

## REVISE

### Issue 1: Sh4 Case D — "τ_new joins A_R^{Σ'}" is asserted but never justified explicitly

**ASN-0094, Sh4 preservation Step (Case D):** "an `Emit_R`-step that adds τ_new to A_R while potentially nullifying prior R-tuple addresses"... "The resulting active subset is `A_R^{Σ'} = (A_R^Σ ∪ {τ_new}) \ leaving`."

**Problem:** The case description presupposes τ_new ∈ A_R^{Σ'}, but the proof never justifies this. Three things must hold for τ_new to join A_R^{Σ'}: (a) τ_new is not self-nullified; (b) τ_new is not nullified by any prior R-tuple; (c) addr(τ_new) ∉ nullified(Σ) at pre-step (trivially true since addr is fresh).

The proof only mentions (a) parenthetically in Case C's text ("The complementary `K ~ R` sub-case... is empty by Lemma — RetractionTargetNotOnChain"). It never addresses (b) — that no *prior* R-tuple's G-coverage contains addr(τ_new). Step 1 of EffectiveWpSimplification handles (b) but is not cited within Case D's body.

**Required:** Add an explicit step at the head of Case D applying the Lemma at *both* (i) τ_new's own G-slot witness (for self-nullification) and (ii) every prior R-tuple's G-slot witness (for cross-nullification), concluding addr(τ_new) ∉ nullified(Σ'), hence τ_new ∈ A_R^{Σ'}. This is the justification that makes "the resulting active subset is `(A_R^Σ ∪ {τ_new}) \ leaving`" a theorem rather than a definition.

### Issue 2: Origin vs home terminology in RetractionTargetNotOnChain

**ASN-0094, RetractionTargetNotOnChain proof, Case I:** "the first-emission branch's gating predicate `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = ∅` is *false* in Case I — it contains at least `b`"

**Problem:** The case hypothesis is `home(b) = d`. ASN-0086's FreshEmissionAddress uses `origin(ℓ')`. ASN-0086's R0a-Cor1 uses `home(a) = d`. The Lemma uses `home(b) = d` and concludes about a predicate using `origin(·)`. The two terms are nowhere identified.

**Required:** Either explicitly identify `origin(·) = home(·)` (citing wherever ASN-0086 establishes this) or use one term throughout. Without identification, the conclusion "the homed set... contains at least b" doesn't directly follow from `home(b) = d`.

### Issue 3: Worked example baseline is stronger than framework's empty-baseline

**ASN-0094, Worked Example: K = comment, opening paragraph:** "We also assume `dom(Σ_0.L) = ∅`... this is what makes K.λ's first-emission branch fire at the first emission below — the predicate `{ℓ' ∈ dom(Σ_0.L) : origin(ℓ') = home_K}` ranges over *all* of `dom(Σ_0.L)`, not just K-typed links, so the empty-`L_K` reading is insufficient."

**Problem:** The framework's *Initial-state baseline for preservation proofs* requires only `L_K^{Σ_init} = ∅` for each `K ∈ T_cat`. The walkthrough asserts the strictly stronger `dom(Σ_0.L) = ∅`. The walkthrough notes this gap but then uses Σ_0 inconsistently — Σ_0 here has documents already registered (so Σ_0 ≠ Σ_init in the proof's notation), yet uses the same symbol.

**Required:** Either (a) clarify that the walkthrough's Σ_0 is a *post-Σ_init* state reached via K.σ-steps with `dom(Σ_0.L) = ∅` preserved, or (b) use a different symbol (e.g., Σ_w) to distinguish the walkthrough's starting state from the framework's Σ_init. The current notational collision invites confusion about what the framework's preservation theorems are actually claiming.

### Issue 4: The "L1c via T10a.4" derivation in RetractionTargetNotOnChain Case II is unexplained

**ASN-0094, RetractionTargetNotOnChain Case II:** "(TA5(c) with `k = 0`, ASN-0034: the step modifies only position `sig(ℓ_prev)`, and on T4-valid `ℓ_prev` — T4-validity supplied by L1c via T10a.4 on the link side — that position carries a non-zero value..."

**Problem:** "L1c via T10a.4" is a multi-step inference: L1c posits T10a-conformant allocation; T10a.4 then proves every T10a-conformant output is T4-valid. The reader has to reconstruct this two-step chain. Earlier in the same proof, the analogous derivation for L1's `zeros(b) = 3` is stated directly without intermediate citation.

**Required:** Either expand to "L1c (ASN-0043) places ℓ_prev in a T10a-conforming allocator chain; T10a.4 (ASN-0034) then gives T4-validity at every chain output, hence at ℓ_prev" or replace with a single citation that directly delivers T4-validity for link-side addresses.

### Issue 5: Resolution catalog row's "primary consumption" framing obscures base templates

**ASN-0094, Canonical Shape Catalog table, Resolution row:** "*base (inherited from `(1, 1, A_doc, A_rel, ⊤)` per Sh5(b)):* `pair_K(a, b)`, `from_K(a)`, `to_K(b)`, `from_addrs_K(b)`, `to_addrs_K(a)`; *primary consumption:* parametrically by NonIdempotentDirectedPair's `_via` templates"

**Problem:** The "primary consumption" column suggests Resolution's base templates are auxiliary. But by Sh5(b), every K registered with shape `(1, 1, A_doc, A_rel, ⊤)` mechanically generates these five templates. The catalog should make clear that a layer can register K at this shape *without* a downstream NonIdempotentDirectedPair consumer and still use the base templates directly.

**Required:** Reword the row to clarify that base templates are first-class and available for any K registered at the shape; the "primary consumption" column is documenting the dominant pattern, not constraining the row's usage.

### Issue 6: Sh4 universal-scope clarification is repeated verbatim in Sh4 Case D and FDD preservation

**ASN-0094, Sh4 *Universal scope* paragraph and FDD preservation paragraph beginning "The FDD property... has the same off-diagonal/diagonal structure as Sh4":** Both passages re-explain the diagonal-trivial / off-diagonal-substantive reading.

**Problem:** Two near-identical paragraphs covering the same logical structure (universal over A_K with reflexive diagonal). The second occurrence in FDD's proof could simply cite Sh4's clarification.

**Required:** Replace the second occurrence with "By the same off-diagonal/diagonal split as in Sh4 (see *Universal scope* above), the substantive content is..."

### Issue 7: Sh5(b) catalog audit table's "failed-check illustration" placement

**ASN-0094, Sh5 *Catalog-wide citation audit*:** The table presents ten catalog-row checks, all passing. The failed-check illustration (`K_is_fresh` with `mtime`) is in a callout *after* the table.

**Problem:** A reader scanning the table sees only passing rows and may not register that the discipline can reject. The framework's META falsifiability claim depends on the rejection path being prominent.

**Required:** Either add a "rejected" row to the table (with `K_is_fresh` and the failure annotation), or restructure the callout to come *before* the table, framing the audit as "here is what the discipline accepts, here is what it rejects."

### Issue 8: Pre-emission candidate-set computation as a workaround is mentioned but not specified

**ASN-0094, Sh-conf section:** "a caller that needs to distinguish rejection-by-Sh-conf from rejection-by-discipline-suppression may consult the discipline's pre-emission candidate-set computation before issuing the `Emit_K` call."

**Problem:** "the discipline's pre-emission candidate-set computation" is not a named operation. The framework defines `C(F, G, Σ)` and `C_fd(F, Σ)` inside the contract clauses, but doesn't surface them as standalone queries. A layer wanting to distinguish rejection sources has no documented interface.

**Required:** Either define `C_K(F, G, Σ)` as a layer-callable computation (with the same Observe-then-postfilter semantics as clause (i) of the contracts), or remove the sentence and state plainly that rejection sources are not distinguishable through the framework's interface.

### Issue 9: AllocatedAddressAntichain Step 3.1 contradiction argument is verbose

**ASN-0094, AllocatedAddressAntichain Step 3.1:** The contradiction-argument paragraph (starting "Suppose, toward contradiction, that `a` has a fourth zero at some position `m`...") splits on `m ≤ #x` and `m > #x`.

**Problem:** The two sub-cases reduce to the same elementary observation: zeros(x) = 3 = zeros(a) and a inherits x's zero positions on indices ≤ #x, so any "extra" zero in a either duplicates one of x's (impossible since x has exactly 3) or sits at index > #x (forcing zeros(a) ≥ 4). The current presentation buries this in a four-sentence argument.

**Required:** Tighten to: "If a has a zero at any m ∉ {n_1, n_2, n_3}: at m ≤ #x, componentwise agreement forces x_m = 0, contradicting zeros(x) = 3; at m > #x, a carries the three zeros at n_1, n_2, n_3 plus m, giving zeros(a) ≥ 4, contradicting zeros(a) = 3."

## OUT_OF_SCOPE

### Topic 1: Closure of composite predicates over the catalog's atomic templates

**Why out of scope:** The framework explicitly acknowledges this open question — "The framework does not establish a closure theorem about these primitives" — and notes the design observation is weaker. Establishing or refuting closure requires choosing a composition language and is a separate ASN.

### Topic 2: Higher-arity links and shape extension

**Why out of scope:** The framework restricts to arity-3 (standard-triple) links per its *Arity scope* commitment. Extending shape constraints to higher-arity links (additional cardinality and target-domain components per extra slot) is a future direction the framework explicitly defers.

### Topic 3: Multi-process Sh4 atomicity protocols

**Why out of scope:** The framework's *Scope: single-process substrate* paragraph identifies multi-process coordination as outside the current draft. Specifying the minimum protocol that preserves Sh4 in a distributed setting is a separate problem.

### Topic 4: Ghost-targeting slot semantics

**Why out of scope:** Currently in Open Questions. Whether future shape families should admit ghost-targeting slot semantics, and under what state-dependent conformance rule, is a design question not resolvable within this ASN's scope.

### Topic 5: Sixth shape-tuple component for per-K disciplines

**Why out of scope:** Currently in Open Questions. Promoting FDD and SHCD to a structural shape-tuple component (versus opt-in extensions) is a catalog redesign decision.

VERDICT: REVISE
