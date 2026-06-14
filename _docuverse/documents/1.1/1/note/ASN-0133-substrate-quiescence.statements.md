# ASN-0133 Claim Statements

*Source: ASN-0133-substrate-quiescence.md (revised unknown) — Extracted: 2026-06-13*

## Definition — Rule

A *rule* is a triple `ρ = (D_ρ, T_ρ, Post_ρ)`: a domain expression `D_ρ ∈ QD`, a Boolean trigger `T_ρ : D_ρ → Bool` in PL, and an *emission contract* `Post_ρ` — a meta-level contract over (argument, state, emitted call set) constraining what any fire of ρ must emit, the calls drawn from the operation surface `{Emit_K, Nullify_Binary}`.

A *registry* `R` is a finite set of rules.

A *fire* of `(ρ, x)` at Σ with `x ∈ [D_ρ]_Σ` is: if `T_ρ(x, Σ) = ⊥`, a no-op (`Σ' = Σ`); otherwise the application of some emission set satisfying `Post_ρ(x, Σ, ·)` — a finite sequence of `→_sh` steps through the surface (the gated relation, ASN-0126, over extended-record states by R-TR, ASN-0128), `Σ →_sh* Σ'`.

**(H-FIN)** Every `Post_ρ`-satisfying emission set is finite (equivalently: every admissible fire sequence terminates). The universal is forced: a contract admitting both a finite and an infinite emission set would satisfy a bare `∃`-reading while leaving a body free to choose the infinite one and diverge.

**(H-ATOM)** A fire's post-state `Σ'` is read as the state immediately after the fire's own `→_sh` steps, with no environment step interleaved among them — the fire is atomic against environment interleaving, and σ's interleaving (H-FAIR) places environment steps only between fires, never inside one.

---

## Definition — QuiescentR

`quiescent_R(Σ) ≡ (∀ ρ ∈ R :: (∀ x ∈ [D_ρ]_Σ :: ¬T_ρ(x, Σ)))`

The outer `∀ ρ ∈ R` is a finite static expansion into a PC0 conjunction (not a PC1 quantification — `R` is a finite metalevel set of rule-triples). Each conjunct `(∀ x ∈ [D_ρ]_Σ :: ¬T_ρ(x, Σ))` is a PL predicate: PC1 over a QD domain, finite at every reachable state (QD-fin), with `¬` by PC0.

---

## Definition — ExtinctionDisciplined

Rule ρ is *extinction-disciplined* iff for every reachable Σ and `x ∈ [D_ρ]_Σ` with `T_ρ(x, Σ) = ⊤`, every fire of `(ρ, x)` yields Σ' with `T_ρ(x, Σ') = ⊥`. A registry is extinction-disciplined iff each rule is.

---

## Definition — FairnessHypothesis

A *fire sequence* `σ = (Σ₀, s₁, Σ₁, s₂, …)` interleaves, from `Σ₀`, two kinds of step: a *fire* of some `(ρ, x)` (atomic against environment interleaving by H-ATOM) and an *environment step* — any non-registry `→_sh*` transition the registry neither issues nor controls.

`σ` is *fair* iff for every `(ρ, x)` and every index `k` with `(ρ, x)` trigger-true at `Σ_k`, some later index `m > k` *discharges that occurrence* one of three ways:
- **real-fired**: a non-no-op fire of `(ρ, x)` at a step past `k`
- **removed** from its domain: `x ∉ [D_ρ]_{Σ_m}`
- **falsified in place**: `T_ρ(x, Σ_m) = ⊥` with `x ∈ [D_ρ]_{Σ_m}` still

This is the *per-occurrence* reading: every trigger-true index incurs its own later discharge.

---

## Definition — StrongFairnessHypothesis

A fire sequence `σ` is *strongly fair* iff every `(ρ, x)` trigger-true at *infinitely many* indices `Σ_k` along σ is *real-fired at infinitely many indices* — GF-taken, not merely eventually taken once.

For infinite σ: `H-SFAIR ⟹ H-FAIR` (the per-occurrence H-FAIR above).

The implication `H-SFAIR ⟹ H-FAIR` fails on finite σ: a finite σ whose final state is trigger-true for `(ρ, x)` satisfies H-SFAIR vacuously yet violates H-FAIR.

---

## Definition — BoundedWork

`W(σ)` is the set of (rule, argument, index) triples at which a trigger is true along σ.

**(H-W)** The registry has *bounded work from Σ₀* iff `|W(σ)| < ∞` for every σ from Σ₀.

---

## Definition — FiniteRealFires

**(H-RF)** A fire sequence from Σ₀ has *finitely many real fires* iff its real (non-no-op) fires are finite in number.

H-W is strictly stronger than H-RF: H-W bounds trigger-true step-instances (`|W(σ)| < ∞`); H-RF bounds only the fires. They come apart at starvation: an SF trigger-true argument the scheduler never fires keeps `(ρ, x, k) ∈ W(σ)` at every step k (`|W(σ)| = ∞`) while contributing no real fire.

---

## Definition — Scope

A *scope* is any Boolean PL predicate `S` over addresses.

The scope's *restriction of ρ* is a QD filter `{x ∈ [D_ρ]_Σ : β_ρ^S(x)}` whose body `β_ρ^S` is a Boolean PL predicate at `D_ρ`'s sort relating the element to `S`.

Standing constraint: `β_ρ^S` must be *S-monotone* — `S` occurring only positively — so that `S' ⟹ S` yields `β_ρ^{S'} ⟹ β_ρ^S` pointwise.

Canonical scoping bodies for tuple-valued `D_ρ`:
- **per-emitter**: `S(addr(x))`, where `addr : Tup → T` is V-TUP's projection
- **per-target**: `(∃ y ∈ addrs_G(x) :: S(y))`, where `addrs_G : Tup → ℘_fin(T)` is V-TUP's to-endset projection — the domain must be the finite denoted set `addrs_G(x)`, never the infinite coverage `⋃{t : y ≼ t, y ∈ addrs_G(x)}`
- **per-source** (symmetric): `(∃ y ∈ addrs_F(x) :: S(y))`

`quiescent_{R,S}(Σ)` restricts Q0's inner quantification to the elements this filter retains.

---

## Q0 — Recognizability (THEOREM)

`quiescent_R ∈ PL` for *every* registry.

For a single-view registry: the conjuncts PC0-conjoin as written.
For a heterogeneous-view registry: each view-parameterized constituent rebuilds at a freely chosen common view via PC3's fixed-view-base device — the four view-parameterized constituents `members`, `targets_of`, `is_K`, `M_K` each rebuilding as `⋃(A_K/L_K, addrs_F)` or its audit analog; the four UV-rewritten fixed-view collections `succs`, `sources_to`, `chain` (reached through `elems` or `is_in_chain`), `stale` each rebuilding as a QD filter over the atom's own raw active reading. The heterogeneous registry pays an explicit fixed-view-base rewrite — a change of spelling, not of value (PC4) — but lands in PL all the same.

Its value at every reachable Σ is decidable in finite time by any observer from Σ and the registry alone — one PL term, pure (PC4) and terminating (PC5), its evaluation finitely many verdicts. Purity makes every verdict observer-uniform.

---

## Q1 — Absorption (LEMMA)

At any Σ with `quiescent_R(Σ)`, every fire of every `(ρ, x)` is a no-op, so `Σ' = Σ`.

*Proof.* Immediate from RG's no-op clause and Q0's definition. ∎

Recognizability and absorption are *unconditional* — they hold for undisciplined registries, unfair schedulers, and divergent systems alike.

---

## Q2 — ContractOnOutputs (LEMMA)

Extinction discipline constrains emissions, not bodies: it is decided by `T_ρ` evaluations at the pre- and post-states — both public PL facts — so any two bodies with the same outputs are equivalent under it, and nondeterministic bodies are admissible whenever *all* their permitted outputs flip the trigger.

---

## Q3 — StaticCheckability (LEMMA)

If `Post_ρ` is *strong enough* — every emission set satisfying it at a trigger-true `(x, Σ)` produces a post-state falsifying `T_ρ(x, ·)` — then ρ is extinction-disciplined.

Read at the **schema level** (all states): a sound over-approximation of X-DEF (all-states ⟹ reachable-states; converse can fail).

Read at the **reachable level** (`(x, Σ)` over reachable trigger-true pairs): reachability-quantified, hence meta-level.

For the **negated-existential marker pattern** — trigger is `¬(∃ c ∈ L_K :: a ∈ coverage_G(c))` over a grow-only audit slice, and `Post_ρ` deposits exactly the witness the `∃` quantifies over — "strong enough" is decided by a finite syntactic comparison of trigger spelling against emission form, no state quantified. This is the decidable case.

For **idem=⊤** marker classes: firing (`T_ρ(a, Σ) = ⊤`) certifies no `c ∈ L_K` covers `a`; a dedup hit would need an active — hence audit (`A_K ⊆ L_K`) — tuple covering it, contradicting the fire. Fire and dedup-hit cannot co-occur: the emit is necessarily a miss and deposits. Even a born-nullified deposit joins `L_K` and flips the audit-read trigger.

Sufficient, not necessary: failure-to-verify is not violation.

---

## Q4 — Locality (LEMMA)

Extinction discipline is per-rule: its definition mentions no other rule. Registries compose pointwise.

---

## Q-EXT — ExtinctionByClass (THEOREM)

If `T_ρ` is an **SF spelling** (⊥-stable, PD0, ASN-0129) and ρ is extinction-disciplined (X-DEF), then ρ fires at most once per argument along any derivation:

For any reachable Σ, `x ∈ [D_ρ]_Σ`, and any fire of `(ρ, x)` at Σ yielding Σ':
- `T_ρ(x, Σ') = ⊥` (by X-DEF)
- For all subsequent states Σ'': `T_ρ(x, Σ'') = ⊥` (by PD0's ⊥-stability, indifferent to whether steps are registry fires or environment steps)

The count of real fires of ρ is bounded by the total growth of `[D_ρ]` alone: `fires(ρ) ≤ |⋃_k [D_ρ]_{Σ_k}|`

*Proof.* Immediate composition of X-DEF with PD0's ⊥-stability. ∎

---

## Q-FLIP — FalsifierAccounting (LEMMA)

For triggers *not* in SF, what can re-arm them is the falsifier inventory ASN-0129's FP enumerates, read with PD1/PD2:
- A retraction shrinking an active slice the trigger reads
- A BH1-type emission moving a default-view result
- A BH4-footprint change from any deposit in a watched home
- A *bare deposit growing an active slice*, which flips an `∃`-shaped active-view trigger `⊥→⊤` (PD1: `(∃ x ∈ M_K :: P(x))` at view active "flips ⊥→⊤ on a K-deposit") or perturbs a non-monotone verdict atom (PD2: a term containing `targets_keyed` is "perturbed by deposits of every BH3-attached Binary type")

Consequence: the folklore "no retraction ⟹ triggers flip at most once" is unsound against the shipped view machinery.

SF triggers are immune: ⊥-stability (PD0) makes a falsified SF trigger permanent against every item above, deposits included.

---

## Q5 — RealFiresAreBounded (LEMMA)

Under H-W alone, every fire sequence from Σ₀ contains at most `|W(σ)|` real (non-no-op) fires.

*Proof.* Each real fire at step k+1 witnesses `(ρ, x, k) ∈ W(σ)`, and the map real-fire ↦ `(ρ, x, k)` is injective by the step index alone (distinct real fires occupy distinct steps, so their triples differ in the index component). Injection into a finite set bounds the count. ∎

Extinction discipline is neither used nor needed: a rule spinning on a fixed `x` would witness infinitely many `(ρ, x, k₁), (ρ, x, k₂), …`, forcing `|W(σ)| = ∞`, so H-W already forbids spinning outright.

---

## Q5a — ExtinctionBound (THEOREM)

For an all-SF, extinction-disciplined registry (every trigger an SF spelling, every rule extinction-disciplined — equivalently, a registry of Marker-pattern rules), under bounded domain growth:

`real fires ≤ Σ_ρ |⋃_k [D_ρ]_{Σ_k}|`

Each argument fires each rule at most once (Q-EXT), so the only unbounded-real-fire route is unbounded new arguments. In the open sequence, `|⋃_k [D_ρ]_{Σ_k}|` bounds external input as much as internal enlargement.

Both hypotheses are load-bearing:
- SF alone does not bound: an SF trigger paired with a contract emitting something other than its own falsifier stays ⊤ on a fixed argument forever (⊥-stability permits ⊤→⊤)
- Extinction discipline alone does not bound: without SF the falsification is not permanent

This supplies **H-RF** by a route disjoint from Q5: it never mentions `W(σ)` and does not establish H-W.

The **closed** special case is degenerate: `bounded-domain-growth ⟺ H-RF` (unbounded growth forces unbounded real fires, and conversely), so Q5a carries no content beyond directly assuming H-RF in a closed registry.

The **open** case: bounded domain growth is *strictly stronger* than H-RF — it implies H-RF, but H-RF does not imply it (a fair scheduler facing an environment that flags infinitely many distinct targets and retracts each before its fire keeps real-fire count at zero while `⋃_k [D_ρ]` grows unbounded).

---

## Q6 — TerminationUnderFairness (THEOREM)

Under H-RF and H-FAIR:

The registry has a last real fire — index N — past which every fire is a no-op (RG), so all state change past N is environment steps.

For any `(ρ, x)` trigger-true at some `Σ_m`, m ≥ N: by H-FAIR, eventually *real-fired* (impossible past N without exceeding H-RF), *removed* from its domain, or *falsified in place*; past N both removal and in-domain falsification are exclusively environment steps.

**Regime (i) — Environment eventually idle** (finitely many environment steps): past both N and the last environment step the state is constant. A non-quiescent constant tail would leave a trigger-true argument forever unfired, unremoved, and unfalsified, contradicting H-FAIR. So the tail is quiescent and absorbing.

**Regime (ii) — All-SF registry** (Q5a's case), grow-only domains: Q5a ⟹ H-RF. SF immunity makes every fired argument permanently trigger-false against every `→_sh` step (step-agnostic). A grow-only domain cannot shrink, so H-FAIR's removal escape is unavailable — each trigger-true argument is eventually real-fired or falsified in place — and for an SF trigger either settling is permanent (Q-EXT). With bounded growth each of the finitely many arguments is eventually settled, so quiescence is *reached and held* under weak H-FAIR alone.

**Non-grow-only domains** under all-SF: the environment can remove an argument before its fire, discharging H-FAIR by removal rather than firing and re-presenting later. Three cases for *reached-and-held* quiescence:

**(1)** Environment alternating ever-fresh trigger-true arguments (each removed before the next): keeps every state non-quiescent — quiescence unreached — but needs unboundedly many distinct arguments, so *bounded domain growth (Q5a) excludes it*.

**(2)** Environment oscillating one argument's domain membership: quiescence reached (each gap state satisfies Q0) but not held (re-presentation is fresh environment input — Q8 re-entry). Survives bounded growth on its single argument. Obstruction to *holding*, not reaching.

**(3)** Environment cycling finitely many trigger-true arguments out of phase: fixed finite set `{x₁, …, x_j}`, each `xᵢ` removed before its fire and re-presented so that at every state at least one stands trigger-true. H-RF holds (zero real fires), bounded growth holds, weak H-FAIR holds (each argument discharged by removal) — yet *no* state is quiescent. Obstruction to *reaching*.

H-SFAIR closes case (3): every `xᵢ` trigger-true at infinitely many indices and never real-fired is forbidden, forcing each `xᵢ` real-fired and SF-settled. Hence: under H-SFAIR (or regime (i)), quiescence is *reached and held* over a non-grow-only domain.

**Finite-σ case:** a fair finite sequence cannot end at a non-quiescent state (a trigger-true argument there left unfired, unremoved, and unfalsified contradicts H-FAIR). ∎

---

## Q7 — ScopeRecognizability (LEMMA)

`quiescent_{R,S} ∈ PL` for *every* registry.

The scope body `β_ρ^S` adds whatever view-sensitive constituents `S` reads — view-parameterized atoms or the UV-rewritten fixed-view collections `succs`/`sources_to`/`chain`/`stale` — to the rebuild Q0 already performs. By Q0's fixed-view-base rewrite, scope quiescence is decidable at every state, observer-uniform, the heterogeneous case again paying a rebuild rather than PL-membership.

---

## Q8 — ScopeAbsorption (LEMMA)

At a scope-quiescent state, in-scope fires are no-ops (absorption relativizes); out-of-scope fires are unconstrained, and an out-of-scope emission may re-arm an in-scope trigger — *re-entry* — which is itself detectable per-state by Q7.

---

## Q9 — AntiMonotoneNesting (LEMMA)

For S-monotone scoping bodies (SC's standing constraint), quiescence is anti-monotone in the scope:

`S' ⟹ S` implies `quiescent_S ⟹ quiescent_{S'}`

*Proof.* `S' ⟹ S` shrinks each filtered domain — `{x ∈ [D_ρ] : β_ρ^{S'}(x)} ⊆ {x ∈ [D_ρ] : β_ρ^S(x)}` by `β_ρ`'s S-monotonicity — and quiescence over the smaller domain is the weaker demand. The converse fails whenever the larger scope holds work no smaller scope sees.

The monotonicity premise is load-bearing: a body with `S` under negation — `β_ρ^S(x) ≡ ¬S(addr(x))` — grows the filtered domain as `S` shrinks, inverting the implication for everywhere-true `S` and everywhere-false `S'`.
