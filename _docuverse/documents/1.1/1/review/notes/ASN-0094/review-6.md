# Review of ASN-0094

## REVISE

### Issue 1: Sh4 contract invokes Observe_K with infinite arguments

**ASN-0094, Sh4 Sub-claim "Layer-discipline contract"**: "Compute `C(F, G, Σ) := {τ ∈ A_K^Σ : ...}` via `Observe_K(coverage(F), coverage(G), oper)` filtered to canonical-form matches."

The same construction appears in FunctionalDependencyDiscipline's contract: "Compute `C_fd(F, Σ) := ...` via `Observe_K(coverage(F), ∅, oper)`."

**Problem**: ASN-0086's Observe_K signature is `℘_fin(T) × ℘_fin(T) × View → ℘_fin(L_K^Σ)` — pattern arguments are finite. By PrefixSpanCoverage and T0(a)/T0(b), `coverage(F)` for any non-empty canonical-slot F is infinite (`{t : x ≼ t}` for the unit-depth span at x is unbounded by sibling generation and nesting depth). Passing `coverage(F)` to Observe_K is type-incorrect, and the entire layer-discipline contract — on which Sh4 and FDD's preservation theorems depend — is ill-defined.

**Required**: Specify the Observe_K invocation with finite arguments. Either pass `slot_addrs(F)` (a finite subset of T, well-typed under `℘_fin(T)`) and accept that this matches *prefix-containing* tuples, then post-filter to exact slot equality; or define a different finite pattern derivation. Then re-verify that Cases B and D of Sh4's induction discharge against the corrected candidate set.

### Issue 2: No worked example for FunctionalDependencyDiscipline

**ASN-0094, "FunctionalDependencyDiscipline" sub-section**: FDD is introduced as strictly stronger than Sh4, with an explicit counterexample showing Sh4 alone is insufficient for singleton-returning accessors, and FDD anchors the `K_target_of` template the catalog opts in to.

**Problem**: The framework introduces FDD as a critical per-K commitment, exhibits its contract (clauses i–iii), and notes templates that depend on it. But no worked example exercises FDD. We see no demonstration of:
- A DirectedPair K with FDD registered, first emission accepted, second emission with same from-slot but different to-slot rejected via `C_fd` non-empty.
- `K_target_of(d)` returning a unique value under FDD where without FDD it would be set-valued or undefined.

The Comment, Coverage, Tuple-Classifier, and Provenance walkthroughs together exercise NonIdempotentDirectedPair (idem = ⊥), Tuple-Classifier, and Provenance — but DirectedPair itself (idem = ⊤) and its opt-in FDD discipline are unverified.

**Required**: Add a worked example registering a DirectedPair K with FDD, exhibiting an admitted first emission, a rejected second emission (with the rejection traced through clauses (i)–(iii) of the FDD contract), and the singleton-returning `K_target_of(d)` evaluation. Show the contrast with the same K without FDD where the set-valued accessor returns multiple elements.

### Issue 3: No worked example for Sh4 emission suppression

**ASN-0094, Sh4 contract**: "(ii) If `C(F, G, Σ) ≠ ∅`, the emission is *suppressed*: no `→`-step occurs."

**Problem**: The worked example for `K = comment` selects a non-idempotent K (idem = ⊥) where Sh4 doesn't apply. No example exhibits Sh4 suppression in action — an idempotent K where a duplicate emission attempt is suppressed by the layer-discipline contract. The Tuple-Classifier (idem = ⊤) and Provenance (idem = ⊤) examples emit only once each, so no suppression event occurs there either.

**Required**: Add an example with an idempotent K (Tuple-Classifier or DirectedPair) where a first emission is admitted, a second emission with identical slot-pair is attempted, the contract's clause (i) computes a non-empty `C(F, G, Σ)`, clause (ii) suppresses the emission, and the state remains unchanged. Verify `A_K^Σ` contains exactly one tuple, not two, after the suppression event.

### Issue 4: No worked example for K ∉ T_cat rejection

**ASN-0094, Sh-conf**: "`Emit_K(Σ, d, F, G)` succeeds iff `K ∈ T_cat ∧ conf_K^Σ(F, G)`."

**Problem**: Sh-conf has two top-level conjuncts. The worked rejection cases exercise the second conjunct (clauses (a), (c), (d) of conformance) but never the first (`K ∈ T_cat`). The framework's gate on unregistered types is structurally distinct from conformance failures and warrants its own example.

**Required**: Exhibit a rejection where `K ∈ T_admissible \ T_cat` — a valid type endset that doesn't appear in the registered catalog — and show Sh-conf rejecting the emission at the `K ∈ T_cat` gate before any conformance check occurs.

### Issue 5: AllocatedAddressAntichain Case 3 — "swap" wording obscures the symmetry

**ASN-0094, AllocatedAddressAntichain proof, Case 3**: "WLOG `x ∈ dom(Σ.L), a ∈ dom(Σ.C)`; the symmetric sub-case `x ∈ dom(Σ.C), a ∈ dom(Σ.L)` follows by swapping the roles of `x` and `a` (the argument below uses only that one side carries `s_L` and the other `s_C`, with `s_L ≠ s_C` symmetric)."

**Problem**: "Swapping the roles of x and a" is a misleading description: x is the prefix in the lemma's hypothesis `x ≼ a`, so swapping x and a would reverse the prefix relation and change the lemma's hypothesis. The actual symmetry is in which side carries `s_L` and which carries `s_C` — the subspace labels swap, not the prefix relation. The parenthetical hints at this but it is buried.

**Required**: Rephrase: "the sub-case `x ∈ dom(Σ.C), a ∈ dom(Σ.L)` proceeds identically with the subspace identifiers `s_L` and `s_C` exchanged in Step 3.3 (the prefix relation `x ≼ a` is unchanged; what symmetrizes is the subspace assignment at position `E(·).1`)."

### Issue 6: Initial state Σ_0 not formally pinned for induction

**ASN-0094, Sh0/Sh1/Sh2/Sh3 proofs**: "By induction on the broad transition relation `↦*` from the initial state `Σ_0`. ... Base case. At `Σ_0`, every `L_K^{Σ_0} = ∅`; the universal quantifier is vacuous."

**Problem**: The induction base case asserts `L_K^{Σ_0} = ∅` but the ASN never defines Σ_0 — neither in its own text nor by reference to a foundation ASN that pins it. ASN-0086's reachability quantifies over states reachable from "Σ_init" without formally pinning Σ_init either. If a substrate has any reachable starting state where Sh0-conformance was not enforced (e.g., pre-framework states with arbitrary L_K), the induction has no base to stand on.

**Required**: State explicitly that the framework's preservation theorems hold along `↦*`-chains starting from any state Σ_init satisfying `L_K^{Σ_init} = ∅` for every `K ∈ T_cat`, and that any state reached before the layer commitment was honored is outside the framework's scope. This makes the conditional nature of the induction precise.

### Issue 7: Sh-conf failure semantics underspecified

**ASN-0094, Sh-conf**: "Emissions failing either conjunct are rejected before any state transition occurs."

**Problem**: ASN-0086's Emit_K is specified with preconditions and postconditions but no explicit failure mode in its signature. Sh-conf adds preconditions; what does the operation produce when the preconditions fail? An error return? An exception? A no-op with the same return type? The Sh4 contract clauses (i)–(iii) rely on emission suppression being detectable by the layer (so the layer doesn't proceed to emit). The framework leaves this interface unspecified.

**Required**: Either extend Emit_K's signature with a failure return (e.g., `Σ' × A_rel^{Σ'} ∪ {⊥}` or a sum type), or cite a substrate-level failure-handling convention. Without this, the layer-discipline contract's "suppress" step has no formal handle on the caller side.

### Issue 8: Sh5 "base template" criterion not formally defined

**ASN-0094, Sh5 status note**: "*Base* templates are forced by the shape tuple alone — every K registered at the shape generates them. *Opt-in (per-K)* templates require a per-K discipline registration ... *Parametric* templates take an additional type-index argument."

**Problem**: The three-way split — base / opt-in / parametric — is presented as the discipline that makes Sh5 falsifiable ("rows with identical `(c_F, c_G, t_F, t_G, idem)` tuples agree on base templates by Sh5"). But what determines whether a template is "base" vs "opt-in" vs "parametric" is not formally specified — the criterion is the catalog's own classification. Two ASN drafts could reasonably disagree on whether a given template is base or opt-in (e.g., is `to_addrs_K` truly forced by the shape, or does it require a finiteness-of-A^Σ commitment that's a layer property?). Without a precise criterion, the falsifiability claim is circular.

**Required**: Specify the criterion: a template is "base" iff its definition is well-formed under exactly the shape tuple's components plus K's name plus Sh0–Sh4 (under Sh4's standard layer commitment when applicable); it is "opt-in" if its well-formedness additionally requires a per-K discipline registration listed in the catalog; it is "parametric" if it takes a type-index argument at evaluation time. Then verify each table entry against this criterion.

### Issue 9: Compatibility constraint between FDD and SHCD not stated

**ASN-0094, "FunctionalDependencyDiscipline" and "SingleHomeCoverageDiscipline" sub-sections**

**Problem**: FDD applies to DirectedPair (idem = ⊤). SHCD applies to NonIdempotentDirectedPair Coverage instantiation (idem = ⊥). These are structurally exclusive — no K can carry both because the underlying shape's idem flag is fixed. But the framework presents them as independent per-K registrations without stating their mutual exclusivity. A reader could mistakenly attempt to register both on the same K.

**Required**: State explicitly that FDD and SHCD attach to disjoint shapes (FDD ⊆ DirectedPair shape, SHCD ⊆ NonIdempotentDirectedPair Coverage shape), so no K is eligible for both. Generalize: the per-K opt-in registry is partitioned by base shape, and the available disciplines depend on which base shape K carries.

### Issue 10: Sh1 inductive step omits Case D, but Sh0 omits Case C and D

**ASN-0094, Sh0 proof inductive step**: Two cases — Case A (`L_K^{Σ'} = L_K^Σ`) and Case B (`L_K^{Σ'} = L_K^Σ ∪ {τ_new}`).

**Problem**: The induction for Sh0/Sh1/Sh2/Sh3 only considers `L_K` *growth* — Case B adds a tuple. Sh4's induction, by contrast, considers four cases including A_K contraction (Case C, via retraction) and simultaneous expansion-contraction (Case D, K ~ R). Sh0–Sh3 are stated over `L_K^Σ` which is monotone (only grows by R3), so no contraction case is needed. But the proofs don't say this; they enumerate Case A and Case B and stop, without explaining why no further cases arise.

**Required**: Add a one-line justification that `L_K` is monotone non-decreasing (cite R3), so the only `↦`-effects on `L_K` are unchanged (Case A) or extended by one (Case B); contraction cases that appear in Sh4 (over `A_K`, which can shrink) do not arise here. This makes the case analysis visibly complete.

### Issue 11: Sh5 catalog's `(0|1, A)` shapes — Provenance well-formedness ambiguity

**ASN-0094, Provenance worked example, Form 2**: `Emit_K(Σ, home_K, {(s, δ(1, #s))}, ∅)` with G = ∅. "clause (d) for G is vacuous since `slot_addrs(∅) = ∅` is a subset of any target domain."

**Problem**: ShapeWellFormedness says `t_G = - ⟺ c_G = 0`. Provenance has `c_G = 0|1`, which is *not* `c_G = 0`, so `t_G ≠ -`. Provenance registers `t_G = A`. When G = ∅ (`|X_G| = 0`), clause (d) requires `∅ ⊆ A^Σ`, vacuously true. But ShapeWellFormedness was derived for the "either both - or neither" alignment; the `c_G = 0|1` case sits awkwardly: when n=0 the target check is vacuous, when n=1 it's enforced. Is this admissible, or should `(0|1, A)` shapes carry an additional well-formedness clause?

**Required**: Either confirm that `c_X = 0|1, t_X ≠ -` is well-formed and re-derive ShapeWellFormedness to admit it explicitly (the current text only constrains `c_X = 0 ⟺ t_X = -`, which permits `c_X = 0|1, t_X = A`), or tighten the rule to also require `c_X = 0|1 ⟹ t_X = -` (which would break Provenance). The framework needs to decide which it means.

### Issue 12: Sh4 Case D's pairwise distinctness extension to A_R^Σ ∪ {τ_new}

**ASN-0094, Sh4 proof Case D**: "Pairwise distinctness on `A_R^Σ ∪ {τ_new}` is established by the IH (which gives pairwise distinctness on A_R^Σ) together with τ_new's slot-pair distinctness from every member of A_R^Σ."

**Problem**: The argument extends pairwise distinctness from `A_R^Σ` (size n) to `A_R^Σ ∪ {τ_new}` (size n+1) by adding distinctness of τ_new from every prior element. But "pairwise distinctness" includes the pair (τ_new, τ_new) — which is trivially address-identical (R1), and the slot-pair predicate doesn't apply (predicate is over distinct tuples). The proof should explicitly note that pairwise distinctness, as stated by Sh4, quantifies over pairs `(τ, τ')` and the conclusion `addr(τ) = addr(τ')` is reflexively satisfied when τ = τ'. Or alternatively, the universal is over `τ ≠ τ'` to begin with.

**Required**: Make the universal scope of Sh4's pairwise-distinctness predicate explicit — either `(A τ, τ' ∈ A_K^Σ : (slot conditions) :: addr(τ) = addr(τ'))` (which subsumes τ = τ' trivially) or `(A τ ≠ τ' ∈ A_K^Σ : ... :: ...)`. The current Sh4 statement is the former, so the (τ_new, τ_new) pair is fine, but the proof should not skip this detail when an induction is bookkeeping pair-existence.

### Issue 13: Sh5 META claim conflates discipline with theorem

**ASN-0094, Sh5 META status**: "Sh5 is a META observation about the framework's organizing discipline, not a mechanical-derivation theorem."

**Problem**: Sh5 is labeled META, but the subsequent paragraph states "The framework *does* guarantee that templates depend only on (i) the shape components, (ii) K's name, and (iii) explicitly named layer-supplied accessors — never on per-K design freedom beyond those." This is a falsifiable claim, not a META observation — it asserts a property of every catalog row. If this is a guarantee, it should be a theorem (or a definition with consequences); if it is META, it is not falsifiable.

**Required**: Either upgrade the "framework guarantees ..." sentence to a definition or claim with explicit type (DEF or LEMMA), or downgrade it to a discipline statement of the form "this framework intends that templates depend only on ...". The current mixed status leaves Sh5's meaning ambiguous.

## OUT_OF_SCOPE

### Topic 1: New canonical shapes beyond the seven catalogued

The catalog lists seven canonical shapes but the Cartesian product of (c_F, c_G, t_F, t_G, idem) admits roughly 200 well-formed combinations. Extending the catalog with new structural patterns (e.g., (0, 0) shapes, tuple-to-document relations with `t_F = A_rel, t_G = A_doc`, many-to-many relations) is acknowledged as an Open Question.

**Why out of scope**: Adding new shapes requires hand-design per the Sh5 META discipline, and the framework presents itself as extensible by future ASNs adding catalog entries.

### Topic 2: Composition closure of the template language

Section "Consequences" (b) explicitly admits "The framework does not establish a closure theorem about these primitives — whether composition can express predicates strictly beyond what the catalog's atomic templates yield is a property of the composition language adopted, not a structural guarantee of Sh5."

**Why out of scope**: Composition closure depends on the choice of composition language (Boolean operators, quantification depth, fixpoint operators), which is layer-level. A future ASN could formalize a particular composition language and study its closure properties.

### Topic 3: Ghost-targeting slot semantics

Open Questions notes that the framework currently restricts `slot_addrs(F) ⊆ t_F^Σ` to already-allocated targets, precluding ghost slot addresses. L9 (ASN-0043) admits ghost spans in non-slot endset positions; whether shapes should ever admit ghost slot addresses is open.

**Why out of scope**: Ghost-targeting slot semantics would require a new state-dependent conformance rule and an analysis of how ghost references resolve as allocation proceeds — a future shape framework extension.

### Topic 4: Cross-process registry consistency

The framework asserts lifetime constancy of `shape : T_cat → Shape` "across the substrate's lifetime", noted as a within-process commitment. Open Questions notes "cross-process consistency (e.g., concurrent shape re-registration in a distributed substrate) is not addressed."

**Why out of scope**: Distributed-substrate semantics are beyond the single-substrate-state model on which ASN-0086 builds.

### Topic 5: Higher-arity relations (arity ≥ 4)

The Scope section explicitly restricts the framework to standard-triple links (arity = 3). Higher-arity links admitted by ASN-0043 L3 are deferred to future shape framework extensions.

**Why out of scope**: Stated explicitly as out of scope by the ASN's Scope section.

VERDICT: REVISE
