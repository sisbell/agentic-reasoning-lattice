# Review of ASN-0094

## REVISE

### Issue 1: NAT-sub uniqueness derivation lacks the strict-monotonicity-of-addition step

**ASN-0094, "Locally derived NAT primitives" / NAT-sub derivation, *Uniqueness*:** "If `n + p₁ = n + p₂ = m`, NAT-order's trichotomy on `p₁, p₂` rules out the strict cases: were `p₁ < p₂`, NAT-addcompat would give `n + p₁ < n + p₂`, contradicting `n + p₁ = n + p₂`."

**Problem:** NAT-addcompat as listed in the foundation gives non-strict inequality (`n ≥ p → m + n ≥ m + p`). The strict step `p₁ < p₂ → n + p₁ < n + p₂` is not directly axiomatized. Deriving it requires (i) NAT-discrete (`p₁ < p₂ → p₁ + 1 ≤ p₂`), (ii) NAT-addcompat applied to `q ≥ p + 1`, (iii) ℕ-associativity (`n + (p + 1) = (n + p) + 1` — not in the listed NAT axioms), and (iv) NAT-strict-successor inequality. The "symmetric" argument `m + 0 = 0 + m = m` in NAT-sub's existence Case A similarly relies on commutativity-with-zero not directly in the foundation. The local NAT-sub derivation is load-bearing for the framework's well-definedness of `m − n` and is cited in Step II.0 of Lemma — RetractionTargetNotOnChain and in Step II.1's zero-count rearrangement.

**Required:** Either add explicit ℕ-associativity and the strict-monotonicity-of-addition step to the local derivation (and account for what additional axioms they require), or acknowledge that the local NAT-sub derivation relies on "standard ℕ arithmetic" beyond the explicit foundation axioms. Apply the same to the `m + 0 = m` step.

### Issue 2: Walkthrough initial-state assumption stronger than framework's stated baseline

**ASN-0094, "Worked Example: K = comment" notational distinction paragraph:** "The framework's empty-baseline assumption is `L_K^{Σ_init} = ∅` *per K ∈ T_cat*; the walkthrough's `dom(Σ_0.L) = ∅` is strictly stronger (it holds across every K simultaneously, not just per-K), but the strengthening is automatic at any state reachable from `Σ_init` by K.σ/K.α-only paths, so no extra assumption beyond the framework's baseline is needed."

**Problem:** The strengthening is NOT automatic. The framework's baseline constrains `L_K^{Σ_init}` only for `K ∈ T_cat`. Substrate-level K.λ emissions at unregistered types `K' ∈ T_admissible \ T_cat` are not forbidden at `Σ_init`, so `dom(Σ_init.L)` could contain tuples from unregistered K's even when `L_K^{Σ_init} = ∅` for every registered K. Then `dom(Σ_0.L) ≠ ∅`, and K.λ's first-emission branch predicate `{ℓ' ∈ dom(Σ_0.L) : origin(ℓ') = home_K}` is not automatically empty. The walkthrough's claim hides an unstated assumption that `Σ_init` is the substrate's literal initial state with `dom(Σ_init.L) = ∅` globally.

**Required:** Either strengthen the framework's baseline at Initial-State Baseline to `dom(Σ_init.L) = ∅` globally (justified as Σ_init being the substrate's initial state), or weaken the walkthroughs to claim only per-home freshness ("no prior emissions at `home_K`"), which suffices for K.λ's first-emission branch without requiring global emptiness.

### Issue 3: Lemma — RetractionTargetNotOnChain Step II.0 strict-positivity derivation gap

**ASN-0094, Lemma — RetractionTargetNotOnChain, Step II.0:** "Define the suffix `w` of `a` after `b` with `#w := #a − #b ≥ 1` (conditional closure under NAT-sub, locally derived in Scope and Substrate Scaffolding above, applied at `#b ≤ #a`, with strict positivity from the sub-case hypothesis `#b < #a`)."

**Problem:** The "strict positivity from the sub-case hypothesis `#b < #a`" step requires deriving `#a − #b ≥ 1` from `#b < #a`. The proof has been spelled out elsewhere (NAT-discrete contrapositive yields `#b + 1 ≤ #a`, then NAT-sub yields `#a − #b ≥ 1` by uniqueness combined with `#b + 0 = #b ≠ #a`), but this chain is asserted parenthetically without being written out. Given the framework's per-step citation convention elsewhere (NAT-card derivation, AllocatedAddressAntichain Step 3.1), this gap stands out.

**Required:** Spell out the NAT-discrete + NAT-sub chain inline at Step II.0, matching the per-step convention applied at Step II.1 and at AllocatedAddressAntichain.

### Issue 4: Layer-commitment qualifier on AllocatedAddressAntichain consumed implicitly by element-level-character clause

**ASN-0094, AllocatedAddressAntichain, *Element-level character of `A^Σ`*:** "the same `subspace_I(·) = E(·).1` layer-commitment surfaced at the lemma's qualifier paragraph above, so the 'every address in `A^Σ` is element-level' claim is conditional on the same layer-commitment."

**Problem:** The clause makes the element-level character of `A^Σ` conditional on the layer-commitment, but downstream consumers (Sh4 idempotency contract clause (i.a), single-home contract preservation theorems, the *Codomain convention for partial templates*) cite "every address in `A^Σ` is element-level" or its consequences (e.g., `#a ≥ 1` for canonical-slot span construction at `b ∈ A_rel^Σ` in R5/L13) without explicit qualifier propagation. A consumer reasoning at L0's abstract `subspace_I(·)` level — without committing to `subspace_I(·) = E(·).1` — would find these clauses asserting conclusions not derivable at their abstraction layer. The framework currently surfaces the qualifier at one site (AllocatedAddressAntichain) but consumes the conclusion broadly.

**Required:** Either propagate the qualifier to every consumer site of "every address in `A^Σ` is element-level" or its consequences, or promote the layer-commitment to a framework-wide invariant declared once in *Scope and Substrate Scaffolding* (rather than left as a per-lemma qualifier). The latter is cleaner; the former requires a per-citation review.

### Issue 5: Sh5 META observation (a) "by analogy and hand-design" admits unbounded design freedom for new shapes

**ASN-0094, Sh5 *Status* (a):** "There is no procedure mapping an arbitrary shape to its template family; new shapes acquire templates by analogy with existing entries and by hand-design."

**Problem:** Combined with Sh5(b)'s mechanical falsifiability claim, this leaves a gap: the discipline can rule out template citations that fall outside categories (i)–(iv), but it cannot constrain the *body shape* of a hand-designed template at a new canonical shape. Two future drafts could register the same shape and produce incompatible base-template families both passing the audit; Sh5's per-shape uniformity claim ("rows with identical `(c_F, c_G, t_F, t_G, idem)` tuples agree on base templates by Sh5") would then be violated. The framework's catalog-extension process needs an additional constraint — e.g., "new shape's base templates must follow the structural pattern of the closest existing shape under a documented difference table" — to make the per-shape uniformity claim falsifiable rather than merely auditable.

**Required:** Either tighten the catalog-extension process to constrain new base-template body shapes, or weaken the per-shape uniformity claim to "rows with identical shape tuples agree on the data symbols their templates may cite, but not necessarily on template body shape." The current formulation oscillates between the two.

### Issue 6: Sh-conf return-type extension to `(Σ' × A_rel^{Σ'}) ∪ {⊥}` not surfaced as a framework-wide compatibility lemma

**ASN-0094, Sh-conf "Per-consumer compatibility commitments" table:** The table enumerates four affected ASN-0086 surfaces (Nullify alias, direct Emit_K calls, ASN-0086 composites, Observe_K, K.λ) and provides per-row commitments.

**Problem:** The compatibility analysis is per-row prose; the framework does not establish a single named lemma stating "for every ASN-0086 consumer that destructures `Emit_K`'s return, the framework's `⊥`-extension preserves the consumer's load-bearing semantics under the layer-discipline contracts." NullifyActiveSubsetCompatibility is named and proved for the Nullify alias only. Future ASN-0086 composites would each need a per-composite compatibility commitment; the framework provides no general principle for what counts as "compatible." The "Direct relational-layer Emit_K calls" row delegates to caller-side dispatch without offering a compatibility theorem, but downstream callers may need to reason about the framework's preservation guarantees at their call sites — without a general lemma, they have no anchor.

**Required:** Either establish a general framework-level lemma "Sh-conf's `⊥`-extension preserves the active-subset content of every Emit_K-consuming ASN-0086 surface satisfying [stated conditions]", or explicitly enumerate the *complete* set of affected surfaces and provide a per-surface compatibility lemma each (replacing the prose table with named theorems analogous to NullifyActiveSubsetCompatibility).

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate Sh4 contract atomicity
**Why out of scope:** The framework's *Sh4 idempotency contract* and *FDD functional-dependency contract* are explicitly committed to single-process substrates, with cross-process consistency flagged at Open Questions as a scope-boundary item. Extending the framework to multi-process substrates would require a new coordination protocol; this is correctly out of scope for ASN-0094.

### Topic 2: Ghost-targeting slot semantics
**Why out of scope:** Sh-conf clause (d) forbids ghost addresses in slot positions; the Open Questions section flags this as a design-choice scope boundary. Admitting ghost-targeting slot semantics would require a new shape-conformance discipline (e.g., state-dependent vs state-independent shape gates); this is correctly out of scope.

### Topic 3: Sixth shape-tuple component for per-K disciplines
**Why out of scope:** The Open Questions section already flags this as a design-choice question — whether FunctionalDependencyDiscipline and SingleHomeCoverageDiscipline should be promoted from opt-in registrations to a sixth shape component. The current opt-in encoding works; the promotion is a refinement, not a missing piece.

VERDICT: REVISE
