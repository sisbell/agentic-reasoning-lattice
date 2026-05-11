# Quiescence

*The substrate's terminal state, recognizable from inside the predicate language; termination as a conditional theorem.*

`agents.md` introduces an *AgentRegistry* `R` and shows (AG-quiescent) that the convergence condition `quiescent ∈ PL` is itself a closed term in the substrate's static predicate language. This document develops what that means: what the substrate *unconditionally* guarantees about quiescence, what each agent must *contractually* guarantee for the system to converge, and under what *registry-level conditions* termination follows as a theorem.

The pipeline in full:

> R0–R7 (typed relations + operations) → Sh0–Sh5 (shape restrictions, slot accessors, templates) → PC0–PC6 (composed predicates) → AG0–AG7 (agents) → **Q0–Q10** (quiescence) → runner (next document)

Forward-chaining systems generally cannot prove unconditional termination — the field's solutions (stratification, fairness, well-foundedness) all amount to conditions under which termination holds. We continue the chain's discipline of distinguishing what the substrate guarantees from what the registry contracts. The treatment is four layers:

- **Layer 1 — Recognizability (Q0, Q1).** Quiescence is decidable from any state by any observer; once reached, it is stable. Unconditional.
- **Layer 2 — Progress-Discipline (Q2, Q3, Q4).** Each agent contractually flips its own trigger false on each non-no-op fire. Per-agent, locally checkable, AG4-respecting.
- **Layer 3 — Conditional Termination (Q5, Q6).** Given progress-discipline plus bounded cumulative work, real fires are bounded; under fairness (deferred to runner.md), quiescence is reached in finitely many steps. Conditional theorems; both classes of hypothesis stated honestly.
- **Layer 4 — Scope-Parameterized Quiescence (Q7, Q8, Q9, Q10).** All three layers above parameterize cleanly over a *scope predicate* `S`. The substrate admits a hierarchy of canonical scopes — local (per-target), lattice (collection-level), system (cross-lattice) — under which scope quiescence is the natural operational target at each tier.


## Why Not the Well-Founded-Measure Route

Before the development, a remark on what is *not* the right structure here.

A classical termination argument introduces a measure `μ : State → Ord` strictly decreasing on every fire. The substrate's monotonicity (R3) prevents any structural quantity on `Σ.L` from decreasing — `L_K` only grows; `nullified` only grows; `dom(Σ.L)` only grows. The natural compensating quantity — the cardinality of "open work" `|{(A, args) : T_A[Σ](args) = ⊤}|` — can rise on a non-no-op fire when the emission satisfies a *different* agent's trigger. So `μ` would have to be lexicographic over agent strata, and stratification requires the registry to expose a topological ordering of cross-agent trigger dependencies that AG4 (DecisionOpacity) and AG5 (PublicPrivateAsymmetry) deliberately refuse to demand.

The well-founded route remains technically possible — a particular registry can pick a particular measure — but pushing it into the substrate spec forces commitment to either a single fixed measure (too restrictive for general registries) or a meta-rule "every registry must define one" (which is just contractual discipline by another name).

The development below takes the contractual route directly, with the contract stated where it can be locally verified against an agent's spec.


## Layer 1 — Recognizability (Q0, Q1)

The recognizability layer is unconditional. Q0 establishes that quiescence is decidable; Q1 establishes that, once reached, quiescence is stable.

**Q0 — RecognizabilityIsUnconditional.** For every reachable substrate state Σ, the value `quiescent[Σ]` is decidable in finite time by any observer, using only Σ, the agent registry `R`, and the predicate-evaluation machinery of `predicate-composition.md`.

*Proof.* By AG-quiescent (`agents.md`):

`quiescent ≡ (∀ A ∈ R :: (∀ args ∈ [D_A] :: ¬T_A(args)))`

is a closed term in `PL`. By PC4 (Purity), `quiescent[Σ]` is determined by `(Σ.C, Σ.M, Σ.L)` and the registry's static components alone — no observer state, no auxiliary metadata, no agent decision history is consulted. By PC5 (TerminationOnFiniteSubstrate), evaluation halts in finite time on any reachable Σ; QD-fin gives finiteness of each `[D_A]_Σ`, and `R` is finite by AgentRegistry's definition. ∎

**Q1 — QuiescenceIsAbsorbing.** A quiescent state is a fixed point of Fire:

`(A Σ : quiescent[Σ] = ⊤ : (A A ∈ R, args ∈ [D_A]_Σ :: Fire(A, args, Σ) = Σ))`

*Proof.* Suppose `quiescent[Σ] = ⊤`. By the Definition of `quiescent`, for every `A ∈ R` and every `args ∈ [D_A]_Σ`, `T_A[Σ](args) = ⊥`. By the Definition of Fire (`agents.md`), when `T_A[Σ](args) = ⊥` the fire is a no-op and `Fire(A, args, Σ) = Σ`. ∎

*Consequences of Q0 + Q1.*

(a) *Observer-uniformity.* Any two observers evaluating `quiescent[Σ]` against the same Σ produce the same answer. Quiescence is not a matter of perspective; it is a substrate fact.

(b) *No coordination required to detect.* The runner computes `quiescent[Σ]` by direct evaluation — no message-passing, no agent reports, no consensus.

(c) *Halt on first detection.* By Q1, once the runner observes `quiescent[Σ] = ⊤`, it can halt without continuing to monitor — no fire can leave the quiescent state.

(d) *Recognizability is independent of progress and fairness.* Q0 + Q1 hold regardless of whether the registry is progress-disciplined or whether fires are scheduled fairly. Recognizability says nothing about whether quiescence is *reachable*; only that, if reached, it is recognizable and stable.


## Layer 2 — Progress-Discipline (Q2, Q3, Q4)

The recognizability layer says *what* quiescence is. Reaching it requires a contract on agents: that a non-no-op fire on `(A, args)` makes `T_A` false on those args. Without this contract, an agent could fire without affecting its own trigger, and the runner could re-fire the same `(A, args)` indefinitely.

**Definition — ProgressDisciplined.** An agent `A ∈ R` is *progress-disciplined* iff, for every reachable state Σ and every `args ∈ [D_A]_Σ`:

`T_A[Σ](args) = ⊤  ⟹  T_A[Σ'](args) = ⊥`

where `Σ' = Fire(A, args, Σ)` is the post-fire state from AG3 / AG6.

That is: every fire that finds A's trigger true on `args` produces a state in which A's trigger is false on those same `args`. The registry `R` is *progress-disciplined* iff every `A ∈ R` is.

**Q2 — ProgressDisciplineDoesNotConstrainBody.** Progress-discipline constrains the *observable response* of `T_A` to A's emissions. It does not constrain `act_A`'s internal computation logic. AG4 (DecisionOpacity) remains in force.

*Proof.* The definition refers only to `T_A[Σ](args)` (a `PL` evaluation, public by PC4) and `T_A[Σ'](args)` (an equally public `PL` evaluation against the post-fire state). The body of `act_A` is consulted indirectly through `Σ'`, but only through the substrate-visible emissions it produces. Two implementations of `act_A` that produce the same emission set on `(args, Σ)` are indistinguishable from progress-discipline's perspective. ∎

*Consequences.*

(a) *AG4 is preserved.* Progress-discipline does not require the registry to expose `act_A`'s body. Non-deterministic actions (e.g., LLM-driven agents) are admissible — what matters is that *whatever* emissions they produce flip the trigger. Stochastic-body agents may require operational bounded-W defense at the runner layer; see [`docs/design-notes/stochastic-quiescence.md`](../../design-notes/stochastic-quiescence.md).

(b) *The contract is on the emission set, not the algorithm.* An agent satisfies progress-discipline by virtue of a property of its outputs. Different implementations sharing the property are equivalent under this contract.

To verify progress-discipline at spec time, the registry needs a static description of A's emissions strong enough to derive the trigger flip without running `act_A`. We capture this with an emission contract.

**Definition — EmissionContract.** An agent A's *emission contract* is a predicate

`Post_A : S_A × State × ℘_fin(EmissionSpec) → Bool`

with `Post_A ∈ PL` (extended over the EmissionSpec codomain), such that for every `(args, Σ)`:

`Post_A(args, Σ, act_A(args, Σ)) = ⊤`

`Post_A` is part of A's static spec — registered alongside the trigger and scope. The contract describes what the action *promises about its output*; the body of `act_A` is the implementation, which AG4 keeps private.

**Q3 — ProgressDisciplineIsStaticallyCheckable.** If A's emission contract `Post_A` is in `PL` and is *strong enough* — meaning: for every `(args, Σ)` with `T_A[Σ](args) = ⊤` and every emission set `E` satisfying `Post_A(args, Σ, E)`, the post-emission state `Σ' = Apply(E, Σ)` satisfies `T_A[Σ'](args) = ⊥` — then A's progress-discipline is verifiable at spec time without running `act_A`.

*Proof.* All three quantifications (over `args`, `Σ`, `E`) range over substrate-derivable domains; `T_A` and `Post_A` are in `PL` by hypothesis. The check

`Post_A(args, Σ, E) ∧ T_A[Σ](args) = ⊤ ⟹ T_A[Apply(E, Σ)](args) = ⊥`

is itself a `PL` formula whose validity reduces to checking that the implication holds for every well-typed `(args, Σ, E)` triple. This is a static spec-time check; the substrate's existence at spec time consists only of the static catalog (T_cat, shape registry, agent registry), with no dynamic state. ∎

*Consequences.*

(a) *Tooling can validate progress-discipline.* A registry-validation tool consumes `T_A`, `D_A`, `Post_A` and produces a verdict. No state is needed; no `act_A` execution is needed.

(b) *Weak emission contracts cannot prove progress-discipline.* If `Post_A ≡ ⊤` (the trivial contract admitting any output), then for many `(args, Σ)` there exist `E` satisfying `Post_A` but not flipping `T_A[Σ'](args)` to false. Verification fails. This is structurally honest: an agent with no observable contract on its output cannot have its output's effect on the trigger predicted.

(c) *Verification is sufficient, not necessary.* Q3 proves a *sufficient* condition for progress-discipline: if `Post_A` is strong enough, A is progress-disciplined. The converse — every progress-disciplined agent admits a sufficiently strong contract in `PL` — is not provable here, and likely not provable in general (the contract may not be expressible in `PL` even though the discipline holds). Tooling failure-to-verify is not proof-of-violation.

**Q4 — ProgressDisciplineIsLocal.** Progress-discipline is a per-agent property: A is progress-disciplined or it is not, independently of any other agent's spec.

*Proof.* The definition quantifies only over A's own arguments and A's own fire results. No `T_B` for `B ≠ A` appears; no joint state across agents is constructed. ∎

*Consequences.*

(a) *Registry construction is compositional.* Adding a progress-disciplined agent to a registry of progress-disciplined agents preserves the property pointwise. There is no "discipline interaction" to manage at registry-construction time.

(b) *Progress-discipline does not imply termination.* Q4 makes progress-discipline a local property, but local progress can compose into global divergence. A pair of progress-disciplined agents can interact through emissions in ways that prevent quiescence (Layer 3 makes this precise). Locality is what makes the property *checkable*; it is not what makes it *sufficient* for termination.


## Layer 3 — Conditional Termination (Q5, Q6)

The final layer composes Layer 2's contracts into a termination theorem, with the bounded-work hypothesis stated as a registry-level condition rather than a substrate guarantee, and fairness stated as a runner-level hypothesis whose proof is deferred to `runner.md`.

**Definition — FireSequence.** A *fire sequence* from initial state Σ_0 is a (finite or countably infinite) sequence

`σ = (Σ_0, fire_1, Σ_1, fire_2, Σ_2, ...)`

where each `fire_k = (A_k, args_k)` with `A_k ∈ R` and `args_k ∈ [D_{A_k}]_{Σ_{k-1}}`, and `Σ_k = Fire(A_k, args_k, Σ_{k-1})`.

A fire sequence is *fair* iff for every reachable state `Σ_k` along σ, every `(A, args)` with `args ∈ [D_A]_{Σ_k}` and `T_A[Σ_k](args) = ⊤` satisfies one of:

(i) `(A, args)` is the chosen `(A_m, args_m)` for some `m > k`; or
(ii) `args ∉ [D_A]_{Σ_m}` for some `m > k` — i.e., the obligation is discharged by domain removal (e.g., retraction of `args` from the active subset) before the runner reaches it.

The two-clause form is necessary because `[D_A]` may shrink under retraction (R6): an `args` that is trigger-true at `Σ_k` may be removed from the domain at some later `Σ_m` before any cycle reaches it. Clause (ii) recognizes that the work has been displaced from active consideration; the runner is not required to attempt fires on absent args. For monotone-growing domains (e.g., `dom(Σ.C)` by S1), clause (ii) never applies and clause (i) is the only operative obligation.

Fairness is a property of the runner's scheduling discipline; we register it here as a hypothesis and defer its constructive proof to `runner.md`.

**Definition — CumulativeTriggerSet.** For a fire sequence σ from Σ_0:

`W(σ) = {(A, args, k) : k ≥ 0 ∧ A ∈ R ∧ args ∈ [D_A]_{Σ_k} ∧ T_A[Σ_k](args) = ⊤}`

That is: the indexed set of (agent, args, state-index) triples at which some trigger is true somewhere in the sequence. Distinct re-occurrences of the same `(A, args)` at different state-indices are distinct elements of `W(σ)`.

**Definition — BoundedW.** Registry R has *bounded W from Σ_0* iff for every fire sequence σ from Σ_0:

`|W(σ)| < ∞`

This is a registry-level property dependent on the initial state and the cumulative emission patterns the registry's agents produce. It is not derivable from R0–R7, Sh0–Sh5, PC0–PC6, or AG0–AG7 alone.

**Q5 — RealFiresAreBounded.** If every `A ∈ R` is progress-disciplined and R has bounded W from Σ_0, then every fire sequence σ from Σ_0 contains at most `|W(σ)|` non-no-op fires.

*Proof.* Consider any non-no-op fire `fire_{k+1} = (A, args)` in σ. By non-no-op-ness, `T_A[Σ_k](args) = ⊤`, so `(A, args, k) ∈ W(σ)`. Each non-no-op fire at step `k+1` therefore *witnesses* an element `(A, args, k) ∈ W(σ)`.

Distinct non-no-op fires witness distinct W-elements. Suppose two non-no-op fires at steps `k+1 < m+1` both witness `(A, args, k)`. Then `A_{k+1} = A_{m+1} = A` and `args_{k+1} = args_{m+1} = args`, and the W-index of both witnessed triples is `k`, requiring `Σ_k = Σ_m`. By A's progress-discipline applied at step `k+1`, `T_A[Σ_{k+1}](args) = ⊥`. Either some intermediate fire flips `T_A` back to true on `args` — in which case the W-element witnessed at step `m+1` has W-index `m`, not `k`, contradicting equality — or no such fire occurs, in which case `T_A[Σ_m](args) = ⊥`, contradicting non-no-op-ness at step `m+1`. Either way, the witnesses are distinct.

The injection from non-no-op fires into `W(σ)` together with `|W(σ)| < ∞` gives the bound. ∎

*Consequences.*

(a) *The bound is on real fires, not total fires.* The runner can produce an infinite sequence of no-op fires (e.g., by repeatedly re-evaluating triggers that are all false). Q5 says only that no infinite sequence is *all real*; eventually, every fire is a no-op.

(b) *Q5 is a substrate-side theorem.* Both hypotheses (progress-discipline, bounded W) are registry contracts; the substrate proves the consequence. No runner-side property is invoked.

**Q6 — TerminationUnderFairness.** Under the hypotheses of Q5 and additionally fair scheduling, the system reaches a state Σ_n with `quiescent[Σ_n] = ⊤` in finitely many steps.

*Proof sketch (full proof deferred to `runner.md`).* By Q5, the number of non-no-op fires is bounded by `|W(σ)|`. After that bound is reached at some step n, all subsequent fires are no-ops, and by Q1 the state is preserved: `Σ_m = Σ_n` for all `m > n`.

Suppose for contradiction `quiescent[Σ_n] ≠ ⊤`. Then some `(A, args)` has `args ∈ [D_A]_{Σ_n}` and `T_A[Σ_n](args) = ⊤`. By fairness, one of two clauses holds: (i) `(A, args)` is the chosen fire at some step `m > n`, or (ii) `args ∉ [D_A]_{Σ_m}` for some `m > n`. Clause (ii) contradicts state preservation `Σ_m = Σ_n` (which gives `[D_A]_{Σ_m} = [D_A]_{Σ_n}`, retaining args). So clause (i) applies: `(A, args)` is fired at step `m > n`. By the trigger-true precondition and state preservation, that fire is non-no-op — contradicting the bound.

Therefore `quiescent[Σ_n] = ⊤`. ∎

*Why the proof is deferred.* "Fair" is a property of the runner's scheduling discipline, not of the substrate. The proof above takes fairness as a black-box hypothesis; `runner.md` commits to a specific fair-scheduling discipline (round-robin over `R × [D_A]_Σ`, priority-based, etc.) and proves Q6 against that discipline. Multiple disciplines yield Q6; the choice is operational.


## Bounded W — Sufficient Conditions

Q5 takes bounded W as a hypothesis. Whether bounded W holds for a given registry is a registry-level analysis problem; the substrate does not decide it. We characterize two structural cases that yield bounded W, and one orthogonal sufficient condition usable in either case.

**Case 1 — Non-retracting registries.** If no agent in `R` emits into a retraction-shape relation, then `nullified(Σ_k) = ∅` for all reachable Σ_k, and active subsets equal their underlying `L_K`'s. By R3, every `L_K` monotonically grows.

In this regime each `PL` atom over a fixed `(A, args)` flips at most once along any fire sequence: positive atoms `⊥ → ⊤` once; the reverse `⊤ → ⊥` is impossible without retraction. A `PL` predicate built by Boolean composition over n atoms can change truth value at most n times for fixed args along a single fire sequence. Therefore the number of `(A, args, k)` entries in `W(σ)` with the same `(A, args)` is bounded by the number of atom-flip events affecting `T_A`'s evaluation on args. If the registry's emissions are themselves bounded — which holds when input is bounded and emissions don't generate unbounded fan-out — then `|W(σ)| < ∞` follows. Most practical non-retracting registries satisfy this.

**Case 2 — Retracting registries.** If some agent in `R` emits into a retraction-shape relation, the active subset can shrink (R6), and `PL` atoms can flip in both directions multiple times per `(A, args)` tuple. Bounded W in this case is *not* a corollary of substrate finiteness. A sufficient (not necessary) condition is:

(i) every retraction-emitting agent is progress-disciplined (Q4 holds);
(ii) retraction emissions are themselves bounded in cumulative count;
(iii) no cycle in the registry's emission-and-retraction graph admits unbounded traversal.

These conditions together imply bounded W. Specific registries (acyclic-by-shape, finite-resource) admit local proofs using their own structural invariants.

**Stratification — orthogonal sufficient condition.** A registry is *stratified* iff there exists `stratum : R → ℕ` such that no agent's emission can flip a strictly-lower-stratum agent's trigger from `⊥` to `⊤`. With finite strata and per-stratum work bounded, total work is bounded: `|W(σ)| ≤ n · max_stratum_work`. Stratification is checkable in either Case 1 or Case 2; it is a useful structural heuristic when the registry's emission graph admits a topological order.

*Status.* This section is META — it characterizes how registries should be analyzed for bounded W, not a substrate-level decision procedure. Whether bounded W is decidable in general is open.


## Worked Example — Producer-Refiner Termination

We verify that the producer-refiner pair from `agents.md` satisfies the Layer 2 contracts and identify the registry-level condition under which bounded W holds.

*Registry.* `R = {P, R}` where:

- `P = (name_P, A_doc, T_P, dom(Σ.C), act_P, prov_P)` with `T_P(d) ≡ is_claim(d) ∧ ¬has_review(d)`. Action: emit a review classifier targeting d, plus zero or more revise comments.
- `R = (name_R, A_rel, T_R, A_{K_revise}, act_R, prov_R)` with `T_R(τ) ≡ ¬resolved_by(τ, K_res)`. Action: emit a resolution targeting τ, plus content edits.

*Layer 2 — Progress-Discipline (verified via emission contracts).*

For P, define `Post_P(d, Σ, E) ≡ (∃ (K_review, ∅, G) ∈ E :: d ∈ coverage(G))`. This contract says: any output of `act_P` on `d` must contain at least one Coverage-shape review tuple targeting `d`. We verify Q3's strong-enough condition: if `T_P[Σ](d) = ⊤` and `Post_P(d, Σ, E) = ⊤`, then `Σ' = Apply(E, Σ)` has `has_review(d) = ⊤` (by Sh5's Coverage walkthrough applied to the emitted review tuple), so `T_P[Σ'](d) = is_claim(d) ∧ ¬⊤ = ⊥`. ✓

For R, define `Post_R(τ, Σ, E) ≡ (∃ (K_res, F, G) ∈ E :: addr(τ) ∈ coverage(G))`. The check is symmetric: if `T_R[Σ](τ) = ⊤` and `Post_R(τ, Σ, E) = ⊤`, then `Σ'` has `resolved_by(τ, K_res) = ⊤`, so `T_R[Σ'](τ) = ⊥`. ✓

By Q3, both agents are progress-disciplined; by Q4, the property is local and the registry composition is automatic.

*Layer 3 — Bounded W (via stratification).*

Define `stratum(P) = 0`, `stratum(R) = 1`.

P enables R: P's revise-comment emissions populate `A_{K_revise}`, flipping `T_R` from `⊥` to `⊤` on the new tuples. Since `stratum(P) = 0 < 1 = stratum(R)`, this respects stratification.

R enables P (only conditionally): R's resolutions populate `A_{K_res}`, which P's trigger does not consult. So resolutions alone do not flip `T_P`. R's content edits, however, modify document arrangements — *if* an edit introduces a new claim (a new `is_claim(d) = ⊤` document), then `T_P[Σ'](d) = ⊤` for that newly-classified document. This would violate stratification (R at stratum 1 enabling P at stratum 0).

The producer-refiner registry satisfies stratification — and therefore bounded W — *iff* the refiner's content edits do not introduce new claims. This is a contract on `Post_R` strengthened beyond resolution-emission: `Post_R` must also forbid content emissions that flip `is_claim` from `⊥` to `⊤`.

*Failure mode under contract violation.* If the refiner's `Post_R` does not forbid claim-introducing edits, the system can loop: P fires on a claim, emits a revise comment; R fires on the comment, emits resolution + content edit that creates a new claim; P fires on the new claim, and so on. Each individual fire is progress-disciplined (Q4 holds locally), but bounded W fails (Q5's hypothesis violated), and termination is not guaranteed.

This concrete failure mode illustrates why Q4 alone is not sufficient and why bounded W (or its sufficient conditions like stratification) is doing real work. Locally-correct agents can compose into globally-divergent registries.


## Layer 4 — Scope-Parameterized Quiescence (Q7, Q8, Q9, Q10)

Layers 1–3 develop quiescence as a global property: every agent's trigger false on every args. Operationally the protocol rarely cares about *global* quiescence; it cares about quiescence on a *scope* — a specific document, a specific lattice, a specific connected component of lattices. We parameterize the development over a scope predicate and identify the canonical operational tiers.

**Definition — Scope.** A *scope* is a Boolean predicate `S : A → Bool` in `PL`, where `A` is the substrate's address universe (`A = dom(Σ.C) ∪ dom(Σ.L)` at any state, by L14 and S1+L-fin a finite union). The dynamic scope set at state Σ is

`[S]_Σ ≡ {x ∈ A : S(x, Σ) = ⊤}`

which is finite at every reachable state (the outer domain is finite by S8-fin + L-fin; the filter preserves finiteness).

*Remark — scope as filter, not as union.* We frame scope as a `PL` Boolean predicate rather than as a `QD` set expression so that scope tiers (local / lattice / system) can be defined by Boolean combinations without requiring `QD` closure under finite union. The two formulations are dynamically equivalent — every `PL` predicate `S` induces a `QD` element via filtering on the address universe, and every `QD` element induces a `PL` membership predicate — but the predicate framing keeps Boolean combinations of scopes within `PL` directly.

**Definition — ScopeQuiescent.** For a scope predicate `S`:

`quiescent_S(Σ) ≡ (∀ A ∈ R, args ∈ [D_A]_Σ : S(args, Σ) :: ¬T_A[Σ](args))`

That is: no agent's trigger fires on any args within the scope. The unscoped `quiescent` of Layers 1–3 is the special case `S(x) ≡ ⊤` (the maximum scope), in which the filter is vacuous and the definition reduces to the original.

**Q7 — ScopeQuiescenceIsInPL.** For any scope predicate `S ∈ PL`, `quiescent_S ∈ PL`.

*Proof.* The definition is a closed term in `PL`: a finite ∀ over `R` (R is a finite static set per AgentRegistry's definition, `agents.md`), an inner ∀ over `[D_A]_Σ` (a quantification domain in `QD`) filtered by `S(args, Σ)` (a `PL` Boolean predicate by hypothesis, admitting filter under PC1's filtered-quantification form), and a Boolean negation of `T_A[Σ](args)` (`T_A ∈ PL` by AG1). All operators are PC0 / PC1; the result lies in `PL`. ∎

**Q8 — ScopeRecognizabilityAndAbsorbing.** For any scope `S`:

(i) *Recognizability inherits from Q0.* `quiescent_S[Σ]` is decidable in finite time on every reachable Σ. By Q7 (`quiescent_S ∈ PL`), PC4 (Purity), and PC5 (TerminationOnFiniteSubstrate), the evaluation is pure and finite.

(ii) *In-scope absorbing inherits from Q1.* If `quiescent_S[Σ] = ⊤`, then for every `A ∈ R` and every `args ∈ [D_A]_Σ` with `S(args, Σ) = ⊤`, `Fire(A, args, Σ) = Σ` — fires whose args lie in `[S]_Σ` are no-ops. (Fires whose args lie *outside* `[S]_Σ` are unconstrained by `quiescent_S`; see Q9 for the directional result.)

*Proof.* (i) Direct from Q7 + PC4 + PC5. (ii) For `args ∈ [S]_Σ` at a `quiescent_S` state, the trigger is false by definition; by Fire's no-op clause (`agents.md`), the fire produces Σ unchanged. ∎

*Consequence — re-entry.* Once a scope is quiescent, the runner can halt activity *within that scope* — though activity at outer scopes may continue, and emissions from outer-scope fires may flip an in-scope trigger from ⊥ to ⊤ at a later state. Re-entry into non-quiescence requires a substrate-observable emission targeting the scope; by Q7 + Q8(i) re-entry is itself detectable per-state.

**Q9 — ScopeMonotonicity.** For scope predicates `S, S'` with `(A x, Σ :: S'(x, Σ) ⟹ S(x, Σ))` (i.e., `[S']_Σ ⊆ [S]_Σ` at every reachable Σ):

`quiescent_S[Σ] = ⊤  ⟹  quiescent_{S'}[Σ] = ⊤`

*Proof.* If every `args ∈ [D_A]_Σ` with `S(args, Σ) = ⊤` has `T_A[Σ](args) = ⊥`, then in particular every `args ∈ [D_A]_Σ` with `S'(args, Σ) = ⊤` does (since `S' ⟹ S`). ∎

The reverse implication does not hold in general. Quiescence on every smaller scope does not entail quiescence on a larger scope if the larger scope contains args outside every smaller scope but inside some agent's `[D_A]_Σ`. Lattice-level agents whose triggers fire on lattice-spanning args (rather than on specific documents) are the canonical case: per-document quiescence everywhere does not imply lattice quiescence when lattice-level work remains.

**Q10 — CanonicalScopeTiers (META).** Three canonical scope tiers structure the protocol's operational use. Each tier corresponds to a natural unit of "done" in the agentic system. The expressions below are scope predicates in `PL` (Boolean combinations of atomic predicates over A).

(i) *Local scope* (per-target / per-role). For a target `d ∈ A`:

`S_local(d)(x) ≡ x = d ∨ (x ∈ A_rel ∧ (∃ K ∈ T_cat :: d ∈ coverage(to_K(x)) ∨ d ∈ coverage(from_K(x))))`

Local quiescence on `d` means no agent's trigger fires on `d` itself or on any tuple that has `d` in either slot. Operationally: "this target is done" — every producer-refiner pair, every scout-revise loop, every audit cycle has run to fixed point on this specific target. This is the per-document granularity at which `claim_revise` and `note_revise` agents resolve.

(ii) *Lattice scope* (collection-level). A *lattice* `L ⊆ A_doc` is a designated set of related documents — typically a connected subgraph under citation, or a registered `lattices/<name>/` directory in the implementation:

`S_lattice(L)(x) ≡ (∃ d ∈ L :: S_local(d)(x))`

Lattice quiescence on `L` is stronger than per-document quiescence within `L`: it additionally requires lattice-spanning agents (whose triggers operate on lattice-wide conditions — cross-document citation consistency, structural-audit predicates) to be false on lattice-scoped args. Operationally: "this lattice is confirmed done within itself" — internal consistency reached.

(iii) *System / cross-lattice scope* (connected). For a set `Lattices` of registered lattices:

`S_system(x) ≡ (∃ L ∈ Lattices :: S_lattice(L)(x))`

System quiescence requires every registered lattice to be lattice-quiescent AND cross-lattice agents (those whose triggers fire on connections between lattices) to be false. Operationally: "the connected component is jointly done" — no lattice has unresolved obligations to its neighbors.

By Q9 (ScopeMonotonicity), since `S_local(d) ⟹ S_lattice(L)` for `d ∈ L` and `S_lattice(L) ⟹ S_system` for `L ∈ Lattices`:

`quiescent_{S_system} ⟹ quiescent_{S_lattice(L)} for every L ⟹ quiescent_{S_local(d)} for every d ∈ L`

The reverse implications fail when agents at outer tiers have unfinished work.

*Status.* Q10 is META — it identifies the canonical tiers the protocol's operational layer uses, not a substrate-level theorem. The scope predicates `S_local`, `S_lattice`, `S_system` are domain-protocol concerns; the substrate spec admits any `PL` Boolean predicate as a scope.

*Consequences.*

(a) *Stigmergic Protocols cross scope tiers.* A composed Stigmergic Protocol (e.g., the Note-to-Claim Maturation Stigmergic Protocol) involves nested or shifting scopes: a note's local quiescence is a precondition for claim decomposition; the resulting claims have their own local scopes; together they may form a lattice-level quiescence target. The protocol layer (above this document) is where these scope transitions are composed.

(b) *Bounded W parameterizes by scope.* `RealFiresAreBounded` (Q5) and `TerminationUnderFairness` (Q6) restated for a scope `S`: real fires *with args satisfying `S`* are bounded by `|W_S(σ)|`, and under fair scheduling that visits the in-scope trigger-true args, `quiescent_S` is reached in finitely many in-scope steps. This is the form the runner's per-scope termination claim takes; the per-scope analog is sketched here and developed in `runner.md`.

(c) *Scope quiescence is observer-uniform.* Q8(i) inherits Q0's observer-uniformity: any two observers evaluating `quiescent_S[Σ]` against the same Σ produce the same answer. Quiescence is a substrate fact at every tier.

(d) *Re-entry is observable.* When an emission at one scope tier flips an in-scope trigger from ⊥ to ⊤ (e.g., a system-level emission targets a lattice document), the affected scope leaves quiescence. By Q7 + Q8(i), this is detectable per-state. Operationally: protocols can monitor scope quiescence transitions both into and out of the quiescent state.


## What the Runner Inherits

Quiescence.md commits the formal framing; runner.md handles the operational machinery. Specifically, runner.md is responsible for:

(a) *Quiescence detection — per-scope.* Per-state evaluation of `quiescent_S[Σ]` for the scope(s) the runner is currently driving toward terminal, decidable by Q7 + Q8(i); halt-on-scope justified by Q8(ii). The runner chooses which scope(s) to evaluate at each cycle; the canonical default is the local scope of each agent's current target tuple, escalated to lattice and system scopes as the protocol progresses. Operational cost (per-fire re-evaluation, incremental detection, cached evaluation, multiple concurrent scopes) is the runner's choice.

(b) *Fair scheduling.* The hypothesis of Q6. Specific schedules — round-robin over `R`, priority queues over trigger-true tuples, fair-by-state — are runner choices. Each must satisfy: every `(A, args)` with `T_A[Σ](args) = ⊤` is eventually fired.

(c) *Behavior under contract violation.* The substrate detects *progress-discipline* violations directly — comparing `T_A[Σ](args)` before a fire and `T_A[Σ'](args)` after is a `PL`-evaluable check by Q2. *Bounded-W* violations cannot be detected this way: bounded W quantifies over reachable states, and reachability is a fixed-point computation outside `PL` (see Open Questions). The runner's runtime defense against bounded-W violation is therefore necessarily *operational* — bookkeeping fire counts per `(A, args)` pair, halting on a heuristic threshold — rather than predicate-evaluation. The architectural commitment is: progress-discipline is verifiable at spec time *and* detectable at runtime; bounded W is verifiable at spec time *only*, and detected at runtime through symptoms rather than direct evaluation. The runner's policy under either kind of violation — log and continue, halt and escalate, retry with a stricter registry — is operational.

(d) *Concurrent fires.* AG7 (substrate-level fire atomicity) admits serial scheduling. If the runner relaxes serialization, it must specify a reconciliation rule for overlapping fires; the Q5/Q6 chain assumed serial scheduling, and concurrent semantics require a parallel theorem.

The boundary is: quiescence.md commits to what is recognizable (Q0/Q1), what is contractually checkable at spec time (Q2/Q3/Q4), and what is conditionally provable from those contracts (Q5). The runner commits to a fair-scheduling policy (justifying Q6), to operational responses when contracts are violated, and — because bounded W is meta-level (see Open Questions) — to runtime bookkeeping for symptoms of bounded-W violation rather than predicate evaluation of bounded W itself.


## Properties Introduced

| Label                | Type   | Statement                                                                                  | Status     |
|----------------------|--------|--------------------------------------------------------------------------------------------|------------|
| ProgressDisciplined  | DEF    | An agent A satisfies `T_A[Σ](args) = ⊤ ⟹ T_A[Fire(A, args, Σ)](args) = ⊥`              | introduced |
| EmissionContract     | DEF    | A predicate `Post_A` in `PL` that A's `act_A` is contractually known to satisfy            | introduced |
| FireSequence         | DEF    | A sequence `(Σ_0, fire_1, Σ_1, fire_2, ...)`; *fair* iff every trigger-true `(A, args)` with `args ∈ [D_A]_{Σ_k}` is later either chosen or removed from `[D_A]` | introduced |
| W(σ)                 | DEF    | Cumulative trigger set across a fire sequence                                              | introduced |
| BoundedW             | DEF    | `|W(σ)| < ∞` for every fire sequence from a given initial state                            | introduced |
| Q0                   | LEMMA  | RecognizabilityIsUnconditional — `quiescent[Σ]` decidable on every reachable Σ            | introduced |
| Q1                   | LEMMA  | QuiescenceIsAbsorbing — quiescent state is a fixed point of Fire                           | introduced |
| Q2                   | LEMMA  | ProgressDisciplineDoesNotConstrainBody — AG4 preserved by the discipline                   | introduced |
| Q3                   | LEMMA  | ProgressDisciplineIsStaticallyCheckable — `Post_A` strong enough ⟹ verifiability        | introduced |
| Q4                   | LEMMA  | ProgressDisciplineIsLocal — per-agent property; no cross-agent coordination                | introduced |
| Q5                   | THM    | RealFiresAreBounded — under progress-discipline + bounded W, real fires `≤ |W(σ)|`         | introduced |
| Q6                   | THM    | TerminationUnderFairness — under Q5 + fair scheduling, quiescence reached in finite steps (proof deferred to `runner.md`) | introduced |
| Scope                | DEF    | A scope is a `PL` Boolean predicate `S : A → Bool`                                          | introduced |
| ScopeQuiescent       | DEF    | `quiescent_S(Σ) ≡ no agent's trigger fires on any args satisfying S`                        | introduced |
| Q7                   | LEMMA  | ScopeQuiescenceIsInPL — `quiescent_S ∈ PL` for every `S ∈ PL`                              | introduced |
| Q8                   | LEMMA  | ScopeRecognizabilityAndAbsorbing — Q0 + Q1 inherit per-scope                                | introduced |
| Q9                   | LEMMA  | ScopeMonotonicity — `S' ⟹ S ⟹ (quiescent_S ⟹ quiescent_{S'})`                       | introduced |
| Q10                  | META   | CanonicalScopeTiers — local / lattice / system as the three operational tiers               | introduced |


## Open Questions

- *Necessity of `PL`-expressible `Post_A`.* Q3 proves sufficiency: a `PL`-expressible emission contract strong enough to derive trigger flipping is sufficient for static verification. The converse — that every progress-disciplined agent admits such a contract — is open. A counterexample would be a deterministic `act_A` whose effect on `T_A` is provable by external reasoning but not by any closed term in `PL`. Such agents would be progress-disciplined but unverifiable at spec time, requiring runtime observation instead.

- *Bounded W decidability.* The bounded-W condition is a registry-level analysis problem with sufficient conditions but no general decision procedure. Whether bounded W is decidable in general (over the fragment of registries expressible in this spec) is open. For specific registry classes (acyclic, stratified, finite-domain) decidability is straightforward; for general registries it likely reduces to a Datalog-style termination problem.

- *Probabilistic progress-discipline.* For LLM-driven agents, the deterministic form of progress-discipline (per the Definition of ProgressDisciplined) may be operationally unrealistic — the agent may flip its trigger reliably *most* of the time. What does the substrate do when an agent satisfies progress-discipline with probability `p < 1`? Possibilities: log violations and continue; halt; retry; redesign the trigger to capture the probabilistic case. The operational response to this case is developed in [`docs/design-notes/stochastic-quiescence.md`](../../design-notes/stochastic-quiescence.md): the substrate spec stays deterministic; the runner's policy gains an N-consecutive-clean stopping rule that fits the spec's existing authorization for operational bounded-W defense.

- *Cross-tier interference.* Q9 (ScopeMonotonicity) shows that outer-scope quiescence implies inner-scope quiescence, but the reverse fails. In a Stigmergic Protocol that targets per-document quiescence followed by lattice quiescence, an outer-scope agent firing during an inner-scope quiescent window can flip the inner scope back out of quiescence (Q8 consequence). What discipline (registry-design, scheduling, or registry partitioning) prevents protocols from oscillating across tier boundaries — and whether such oscillation is even pathological versus necessary — is open. Likely intersects with the protocol layer of the stack.

- *Scope-restricted bounded W.* Q5/Q6 are stated for global W. Q10 consequence (b) sketches the per-scope analog — `W_S(σ)` and per-scope termination — but it is not formally developed here. Whether per-scope bounded W is strictly weaker, equivalent to, or independent of global bounded W is open; in particular, whether a registry can have bounded W on every canonical scope tier without having globally bounded W deserves a structural treatment.

- *Recovery from contract violation.* A non-progress-disciplined agent in `R` does not break Q0 (recognizability holds regardless) but breaks Q5 (real fires no longer bounded). The runner can detect the violation by re-evaluating `T_A[Σ'](args)` after each fire; what it does next — log, halt, escalate — is a runner-level policy. The boundary between "violation that the runner can compensate for" and "violation that requires registry redesign" is not sharp.

- *Recursion and fixed-point predicates.* If `T_A` is a fixed-point predicate (per `predicate-composition.md`'s open question on recursion), progress-discipline as stated may not be the right condition — fixed-point predicates can have non-monotonic semantics that complicate the trigger-flip analysis. Whether quiescence extends naturally to a recursion-admitting predicate language is open.

- *Reachability in `PL`, and the meta-level status of bounded W.* The cumulative trigger set `W(σ)` quantifies over reachable states. Reachability itself is a fixed-point computation: `Σ_k` reachable from `Σ_0` iff there is a finite fire sequence taking Σ_0 to Σ_k. By PC6 (ExpressiveClosure, `predicate-composition.md`) and the open question there on recursion, reachability is *not* in `PL` — `PL`'s closure under PC0–PC2 admits only finite Boolean compositions, finite quantifications, and value composition; no fixed-point operator. Consequently, *bounded W is itself meta-level*: it is a property the registry designer can prove (by hand, by tooling, by abstract interpretation) but the substrate cannot evaluate as a single predicate at any state Σ. This has a sharp architectural consequence — the runner's runtime check for bounded-W violation cannot be a `PL` evaluation; it must be operational bookkeeping (counting non-no-op fires per `(A, args)`, halting on a heuristic threshold). Whether a substrate-level surrogate exists — a `PL`-expressible necessary condition for bounded W that catches common violation patterns — is open. Resolving this affects how `runner.md` commits to violation-detection policy.

- *Apply as a substrate primitive.* Q3's static check uses `Apply(E, Σ)` — the post-emission state. We've left this as a notational convenience inherited from agents.md's AG3 sequential composition. Whether `Apply` deserves a first-class treatment as a substrate primitive (with its own properties about how shape conformance composes through AG3 sequences) is open; for the purposes of Q3 it is enough that `Apply` is well-defined per AG3.