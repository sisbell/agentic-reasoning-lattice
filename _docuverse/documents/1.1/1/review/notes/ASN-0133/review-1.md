# Review of ASN-0133

## REVISE

### Issue 1: Extinction discipline does no deductive work in Q5/Q6, and the hypothesis-independence claim is false

**ASN-0133, Q5 + Q6 closing**: Q5 states "Under extinction discipline and H-W, every fire sequence from Σ₀ contains at most |W(σ)| real (non-no-op) fires," with the proof "extinction discipline makes distinct real fires witness distinct triples (a second fire on the same (ρ, x) requires an intervening re-arm, which re-indexes the witnessed triple)." Q6 then closes: "drop extinction discipline and a rule can spin on one argument… Each hypothesis has its own failure mode, and none is derivable from the others."

**Problem**: `W(σ)` is defined as "the set of (rule, argument, **index**) triples at which a trigger is true along σ." With the step index in the triple, the injection is by index alone, not by extinction:

- A real fire at step `k+1` has `T_ρ(x, Σ_k) = ⊤`, so `(ρ, x, k) ∈ W(σ)`. Two real fires at distinct steps `k+1 ≠ k'+1` give distinct triples because `k ≠ k'`. The map real-fire ↦ `(ρ, x, k)` is injective by the index, whether or not the trigger was extinguished. So `|real fires| ≤ |W(σ)| < ∞` follows from **H-W alone**; extinction is not used. The proof's appeal to "an intervening re-arm… re-indexes the witnessed triple" describes a re-indexing that happens for *any* two fires at different steps — extinction has nothing to do with it.

Worse, H-W as defined already **subsumes** extinction's stated failure mode. If a rule "spins on one argument" — fires on a fixed `x` at infinitely many steps `k₁ < k₂ < …` — then `{(ρ, x, kᵢ)} ⊆ W(σ)` is infinite, so `|W(σ)| = ∞`, violating H-W. Hence under H-W no rule can spin, with or without extinction. The claim "drop extinction discipline and a rule can spin on one argument" is therefore false *while H-W is retained*: to exhibit a spin you must drop H-W too. So extinction is not independent of H-W for the Q5/Q6 conclusions, contradicting "none is derivable from the others."

Note the re-indexing escape does not rescue extinction either: if you re-define `W` as `(rule, argument)` **pairs** (dropping the index), then under *general* extinction a pair can still fire several times (re-arm permitted), so `|real fires| ≤ |pairs|` fails — that pairs bound holds only under the SF at-most-once property (Q5a), not Q5's general extinction. Either indexing leaves Q5's extinction hypothesis idle.

**Required**: State Q5 and Q6 under H-W (+ H-FAIR for Q6) without extinction discipline, since the bound and the termination argument hold under those alone; or, if extinction is retained, relocate its actual role — it is load-bearing in **Q-EXT** (at-most-once per argument) and **Q5a** (the `Σ_ρ |⋃_k [D_ρ]_{Σ_k}|` pairs bound), where it lets you *replace* the meta-level H-W with bounded domain growth. Correct the Q5 proof to attribute injectivity to the step index, and revise the closing independence paragraph: the genuine separable failure modes are (H-W: re-arm cycles diverge) and (H-FAIR: starvation), while "extinction" earns its keep only as the means to discharge H-W cheaply, not as a third independent hypothesis of the general theorem.

### Issue 2: The worked composition mis-classifies the producer trigger as an SF spelling

**ASN-0133, Worked composition, "Class check"**: "Both triggers are negated existentials over grow-only audit slices with step-constant bodies — **SF spellings** by PD0's quantifier and Boolean rules." This is then used to invoke Q-EXT ("With SF, Q-EXT gives at-most-once per argument for both rules") and Q5a.

**Problem**: Only the resolver trigger fits that description. `T_R(c) ≡ ¬(∃ r ∈ L_res :: addr(c) ∈ coverage_G(r))` is a pure negated existential over a grow-only audit slice with a step-constant body — SF, correctly. But the producer trigger is

`T_P(t) ≡ needs_attention(t) ∧ ¬(∃ c ∈ L_cmt :: t ∈ coverage_G(c))` —

a conjunction whose first conjunct `needs_attention(t)` the "Class check" silently drops from its description. PD0's `∧` rule preserves SF only when **both** conjuncts are SF, and `needs_attention`'s spelling is never given, so its class cannot be read off "PD0's quantifier and Boolean rules." Concretely, `T_P` is not ⊥-stable: take a comment-free `t` that does not yet need attention (`T_P(t) = ⊥`); if `needs_attention(t)` later becomes `⊤` with `t` still uncommented, then `T_P(t) = ⊤` — a ⊥→⊤ flip, so `T_P ∉ SF`. The note's own failure-mode discussion ("`needs_attention` flipping ⊤ on fresh addresses") confirms `needs_attention` is not treated as monotone-false. The uniform "both are SF" is exactly a proof-by-"similarly" across two cases that differ.

The at-most-once property for `ρ_P` does hold, but through a *different* mechanism than the one cited: firing emits a `cmt` covering `t`, making the **ST** condition `E ≡ (∃ c ∈ L_cmt :: t ∈ coverage_G(c))` permanently true (audit slice grow-only); since `T_P ⟹ ¬E`, `T_P(t)` is then false forever. That is "the fire establishes an ST sub-condition that the trigger negates," not "`T_P` is SF" — so Q-EXT (which requires `T_ρ ∈ SF`) does not apply to `ρ_P` as stated, and the section's only worked termination verification rests on an unestablished class assignment.

**Required**: Fix the one worked example. Cleanest: move the precondition into the domain — `D_{ρ_P} = {t ∈ targets : needs_attention(t)}` (a QD filter), leaving `T_P = ¬(∃ c ∈ L_cmt :: t ∈ coverage_G(c))`, a genuine SF spelling; note the domain is then non-grow-only and is bounded via Q5a's `|⋃_k [D_ρ]_{Σ_k}|` union, matching "terminates iff the target population is bounded." Alternatively, give and justify `needs_attention`'s class, or restate Q-EXT to cover the actual `precondition ∧ ¬(ST-condition)` mechanism and re-derive `ρ_P` under it.

### Issue 3: Q0's "quiescent_R ∈ PL" under-justifies the outer quantifier and ignores view heterogeneity

**ASN-0133, Q0**: "Define `quiescent_R(Σ) ≡ (∀ ρ ∈ R :: (∀ x ∈ [D_ρ]_Σ :: ¬T_ρ(x, Σ)))`. Then `quiescent_R ∈ PL`… Proof. R is finite; each inner quantification is PC1 over a QD domain… negation is PC0."

**Problem**: The proof discharges the *inner* quantifiers (PC1 over `D_ρ ∈ QD`) but glosses the *outer* `∀ ρ ∈ R`. `R` is a finite metalevel set of rule-triples, not a QD domain (for inline-trigger registries it is not even substrate content), so `∀ ρ ∈ R` is not a PC1 quantification. Landing `quiescent_R` in PL requires reading it as a finite **PC0 conjunction** obtained by static expansion over `R` — exactly the move the corpus already makes explicit for `Reg`-quantification in ASN-0129's V-IDX ("Defined by static expansion… denotes the finite conjunction"). Q0 should mirror that, rather than leaving the outer connective to "R is finite."

Two PL constituents may also carry different views, and PC0 conjunction requires constituents to "read the same Σ and the same view (PC3)." Nothing in RG constrains the triggers `T_ρ` to a common view, so for a heterogeneous-view registry `quiescent_R` is not a single PC0/PC3-conforming term — it is a finite metalevel conjunction of separately-viewed PL predicates. The *decidability/observer-uniformity* payload survives in either case (finitely many decidable verdicts), but the asserted "`∈ PL`" — which Q7 inherits "wholesale" for scope quiescence — is what needs the careful statement.

**Required**: State the outer quantifier as a finite static expansion into a PC0 conjunction (cite the V-IDX precedent), and either restrict the "`∈ PL`" claim to single-view registries or downgrade it to "decidable as a finite conjunction of PL predicates." Propagate the corrected wording to Q7.

## OUT_OF_SCOPE

### Topic 1: A general extinction-by-class criterion for `precondition ∧ ¬(SF-condition)` triggers

**Why out of scope**: Issue 2 can be repaired locally (relocate the precondition). But realistic Marker-pattern triggers almost always carry a guard like `needs_attention`, so the truly reusable theorem is a generalized Q-EXT: a rule is at-most-once-per-argument when its fire establishes an ST sub-condition `E` with `T_ρ ⟹ ¬E`, of which `T_ρ ∈ SF` is the special case `E = ¬T_ρ`. Formalizing that criterion (and what registration-time certificate it would need, relative to Open Question 1's `pd_extinct`) is a genuine extension, not a defect in this note's stated SF result.

META: not applicable — the note defines a terminal-state invariant (quiescence), its recognizability and absorption as state guarantees, and conditional-termination theorems with hypotheses partitioned into substrate-unconditional / registration-checkable / scheduler-assumed; this is system-guarantee territory, not implementation mechanics.

VERDICT: REVISE
