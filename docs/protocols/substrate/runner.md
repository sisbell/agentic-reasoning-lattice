# Runner

*The operational layer that consumes the substrate spec and drives fire sequences toward quiescence.*

The substrate, predicate language, agent registry, and quiescence theorems together specify *what* the architecture is. They do not specify *how* it executes — what schedules fires, what detects violations, what responds when contracts fail. The runner is that layer.

A runner is *outside* the predicate language (it Emits, by AG3) but a *sound consumer* of it: it relies on PC4 (Purity), PC5 (Termination), PC6 (ExpressiveClosure), AG0–AG7, and Q0–Q10 for correctness. Multiple runners can satisfy the same spec; they differ in scheduling discipline, detection strategy, and violation-response policy. This document commits to the minimum operational structure under which `quiescence.md`'s Q6 (TerminationUnderFairness) is constructively realized, identifies the two distinct violation-detection regimes the spec exposes, and parameterizes the runner over a policy module that handles cases the substrate cannot self-resolve.

The pipeline in full:

> R0–R7 (typed relations + operations) → Sh0–Sh5 (shape restrictions, slot accessors, templates) → PC0–PC6 (composed predicates) → AG0–AG7 (agents) → Q0–Q10 (quiescence, Layers 1–4) → **Run0–Run5** (runner)

The substantive claim is that the runner's responsibilities partition cleanly along the spec-time / runtime / operational axes:

- *Spec-time* obligations are discharged by the registry (AG2, Q3 verification of `Post_A`, bounded-W analysis).
- *Runtime* obligations the runner can discharge in `PL` (progress-discipline detection per fire, quiescence detection per state).
- *Operational* obligations sit outside `PL` and require bookkeeping or policy (bounded-W symptom tracking, violation responses, concurrent-fire reconciliation).

The runner inherits exactly the operational column. The other two columns are someone else's responsibility.


## Run0 — RunnerIsOutsidePL

**Run0 — RunnerArchitecture (META).** A runner consists of:

- An *initial-state hook* that produces the starting Σ_0 (typically by reading the substrate's persisted store).
- A *scheduling discipline* that orders the fires it will attempt — a function `next : R × State → Option(R × Args)` returning the next `(A, args)` to fire, or signaling halt.
- A *fire-execution path* that invokes `Fire(A, args, Σ)` (per `agents.md` AG3) and observes the resulting state.
- A *quiescence-detection strategy* that periodically evaluates `quiescent_S[Σ]` for the scope(s) `S` the runner is driving toward terminal (per Q7, Q8) and halts when true. The default scope is `S(x) ≡ ⊤` (global quiescence per Q0/Q1); specific runners may parameterize over local, lattice, or system scope per Q10.
- A *violation-response policy* that maps detected contract violations (per Run3, Run4) to runner actions.

The runner is *outside* the static predicate language `PL` because it Emits via Fire's action invocation; PL is read-only by PC4. The runner is a *sound consumer* of `PL` because every observation it makes — `T_A[Σ]`, `quiescent[Σ]`, post-fire trigger comparison — is a `PL` evaluation, which by PC4 + PC5 yields a deterministic Bool in finite time.

*Status.* Run0 is META: it describes what kind of construct a runner is, not a theorem about substrate state. Multiple runners differing in scheduling discipline or policy module are admissible; each commits to a particular realization of the operational responsibilities.

*Consequences.*

(a) *Runner soundness reduces to spec compliance.* A runner that respects AG3 (sequential composition with provenance), AG6 (preserves R0–R7 and Sh-conf), and AG7 (fire atomicity) cannot violate substrate invariants. Any specific bug in a runner's implementation is a bug at the implementation layer, not a soundness gap in the spec.

(b) *Runners are interchangeable.* Two runners with the same scheduling discipline, detection strategy, and policy module produce equivalent operational behavior on the same registry; the spec admits any such runner without modification.

(c) *Runner state is not substrate state.* Bookkeeping the runner does (fire counters, scheduling queues, violation logs) lives in the runner's process, not in `Σ`. Predicates evaluated against Σ never see this state, by PC4. If the runner needs to *expose* its operational state — e.g., for observability — it must do so via Emit, just like any other agent.


## Run1 — Fair Scheduling

The Q6 hypothesis is *fairness*: every `(A, args)` with `T_A[Σ_k](args) = ⊤` at some reachable `Σ_k` is eventually fired. This document commits to a constructive fair scheduling discipline and proves it satisfies the hypothesis.

**Definition — RoundRobinSchedule.** The *round-robin schedule* is the discipline: at each *cycle*, iterate over the registry `R` in a fixed order; for each `A ∈ R`, iterate over `[D_A]_Σ` (the trigger's argument domain at the current Σ); for each `args` with `T_A[Σ](args) = ⊤`, invoke `Fire(A, args, Σ)`. After completing the cycle, re-evaluate `quiescent[Σ]`; if true, halt; otherwise begin the next cycle.

The cycle structure is essential. Mid-cycle state mutations (each fire updates Σ) do not cause re-iteration within the cycle; the runner trusts that any newly-true `(A', args')` will be picked up at the next cycle's start.

**Run1 — RoundRobinIsFair.** The round-robin schedule is fair: every `(A, args)` with `args ∈ [D_A]_{Σ_k}` and `T_A[Σ_k](args) = ⊤` at some reachable Σ_k is *either* attempted by the runner at some step `m > k`, *or* removed from `[D_A]` (i.e., `args ∉ [D_A]_{Σ_m}`) before such an attempt — discharging the obligation either way.

*Proof.* Suppose `args ∈ [D_A]_{Σ_k}` and `T_A[Σ_k](args) = ⊤`. By Q1 (QuiescenceIsAbsorbing), Σ_k is not quiescent, so the runner does not halt at Σ_k. The runner enters its next cycle at some Σ_{k'} with `k' ≥ k`. At cycle start, the runner iterates through `R` and reaches `A`; for `A`, iterates through `[D_A]_{Σ_{k'}}`. Two cases:

*Case A — args ∈ [D_A]_{Σ_{k'}}:* The runner attempts `(A, args)` at some step `m` during the cycle's processing of A. The attempt is the *choice* of `(A, args)`; whether it is a real fire (if `T_A[Σ_m](args) = ⊤`) or a no-op (if `T_A[Σ_m](args) = ⊥`) does not affect fairness. Obligation discharged by clause (i).

*Case B — args ∉ [D_A]_{Σ_{k'}}:* Some retraction or other domain-shrinking transition removed `args` from `[D_A]` between Σ_k and Σ_{k'}. Obligation discharged by clause (ii); the work represented by `(A, args, k)` has been displaced from active consideration. The runner correctly does not iterate to it.

Note that fairness as stated requires only the *attempt* (or the domain removal); whether the attempt produces a real fire is a separate question governed by the trigger's value at attempt time. Under monotone or stable `[D_A]` (e.g., `dom(Σ.C)`, which by S1 only grows), Case B never arises and every trigger-true args is attempted in some later cycle. Under shrinking domains (e.g., `A_K^Σ` under retraction), Case B handles displacement cleanly. ∎

*Status.* Run1's proof depends on Q1 (the runner doesn't halt prematurely at a non-quiescent state) and on `Σ_k` being reachable (else the universal quantifier is vacuous on `Σ_k`). It does not depend on progress-discipline or bounded W; round-robin is fair regardless of those contracts.

*Consequences.*

(a) *Round-robin is one fair discipline; not the only one.* Priority queues, stratum-aware schedulers, work-stealing schedulers can all be made fair. The runner spec admits any fair scheduler; round-robin is the default for simplicity. A registry with stratification (per Q5's discussion) may benefit from a stratum-respecting scheduler that fires lower strata to quiescence before higher strata; that's a runner-level optimization.

(b) *Fairness is a per-runner property, not a per-spec property.* The substrate spec does not prescribe a specific scheduler. Runners that violate fairness (e.g., always firing the first agent in `R` when its trigger is true) are still spec-compliant in the sense that they do not violate substrate invariants; they simply forfeit Q6's termination guarantee.

(c) *Fairness is unconditional on registry contracts.* Round-robin provides fairness regardless of whether agents are progress-disciplined or whether the registry has bounded W. Termination requires the registry contracts; fairness alone does not. This separation matters under contract violation: even on a malformed registry, the runner schedules fairly — meaning violations are observed across the entire registry, not concentrated on a few agents the scheduler happens to prefer.

**Run2 — RunnerSatisfiesQ6 (THEOREM).** A round-robin runner with per-cycle quiescence detection, operating over a progress-disciplined registry with bounded W, halts in a quiescent state in finitely many cycles.

*Proof.* In three steps.

*Step 1 — Real fires are bounded.* By Q5 (RealFiresAreBounded), `|{non-no-op fires in σ}| ≤ |W(σ)| < ∞`. So there exists a finite step n after which no further non-no-op fire occurs along σ.

*Step 2 — Σ_n is quiescent.* Suppose for contradiction `quiescent[Σ_n] ≠ ⊤`. Then some `(A, args)` has `args ∈ [D_A]_{Σ_n}` and `T_A[Σ_n](args) = ⊤`. By Run1's fairness, this `(A, args)` is either attempted at some step `m > n`, or removed from `[D_A]` before such m. The "removed" branch contradicts `args ∈ [D_A]_{Σ_n}` together with our assumption that Σ_n is the post-last-real-fire state (no further substrate change occurs). So `(A, args)` is attempted at step `m > n`. By the trigger-true precondition `T_A[Σ_n](args) = ⊤` and Q1 (state stable after step n), `T_A[Σ_m](args) = ⊤`, so the attempt is a real fire — contradicting Step 1. Therefore `quiescent[Σ_n] = ⊤`.

*Step 3 — The runner halts.* By Q1, Σ remains at Σ_n for all subsequent cycles. The runner performs per-cycle quiescence detection; the cycle following Σ_n's stabilization evaluates `quiescent[Σ_n] = ⊤` and the runner halts. Since Step 1 bounds the number of real fires by `|W(σ)|` and round-robin completes a cycle in `|R| · max_A |[D_A]_Σ|` attempts, the total cycle count to halt is finite. ∎

*Consequences.*

(a) *Termination is a runner property, conditional on registry contracts.* Run2 closes the chain: substrate guarantees recognizability and per-fire correctness (Q0, Q1); registry guarantees per-agent progress (Q3) and bounded W (Q5); runner guarantees fair scheduling (Run1) and per-cycle detection. The combination yields halting in a quiescent state.

(b) *Q6's proof is now constructive.* The runner spec exhibits an actual scheduler (round-robin) and an actual detection strategy (per-cycle) under which Q6 holds. Future runners with different schedulers or detection strategies must prove their own Run2-equivalents.

(c) *Detection lag is bounded by one cycle.* The per-cycle detection strategy can produce at most `|R| · max_A |[D_A]_Σ|` no-op fires after Σ_n is reached but before quiescence is detected. By Q1 these no-ops preserve Σ; they cost time but not correctness.

(d) *The theorem generalizes to scope-parameterized quiescence.* Run2 is stated for global quiescence (`S(x) ≡ ⊤`); the same proof structure applies to any scope predicate `S ∈ PL` provided the runner's fairness-and-detection guarantee is restricted to in-scope args (Run1's fairness obligation taken over `args` with `S(args, Σ)`, Step 3's per-cycle detection evaluating `quiescent_S[Σ]`). Under those scoped hypotheses the runner halts in a `quiescent_S` state. This is the form the runner takes when the protocol layer drives toward per-document, per-lattice, or per-system terminal states; specific runner deployments commit to their scope discipline operationally.


## Run3 — Progress-Discipline Detection in PL

The first violation regime: detecting per-fire progress-discipline violations.

**Run3 — ProgressViolationDetection.** Progress-discipline violations are detectable in `PL` per fire. After a non-no-op fire of A on `args` producing post-state Σ', the runtime check

`T_A[Σ'](args) = ⊥`

is a single `PL` evaluation. If the check returns ⊥ (i.e., the trigger remains true), A has violated progress-discipline on `(args, Σ)`; the runner has direct evidence of the violation.

*Proof.* `T_A` is in `PL` (AG1). `T_A[Σ'](args)` is its evaluation at the post-fire state, which is a substrate state observable to the runner. By PC4 and PC5, the evaluation is pure and decidable in finite time. The runner observes the result. ∎

*Consequences.*

(a) *Per-fire detection is decidable.* The runner can evaluate `T_A[Σ']` after each fire as part of its loop; the cost is one trigger evaluation per fire, asymptotically the same as the cost of evaluating the trigger before the fire.

(b) *Detection is purely observational.* The runner does not need to compare A's emissions against `Post_A`; it observes the *effect* of the fire on `T_A`. This is the right level of abstraction: progress-discipline is about effects, not about emission contents per se.

(c) *Detection is sound but not complete.* A violation produces direct evidence (`T_A[Σ'](args) = ⊤`); absence of violation in any single fire is not proof that the agent is progress-disciplined globally. An agent that flips `T_A` on most `(args, Σ)` but not all is detected only on the failing fire — and only if that fire is observed.

(d) *Runners can short-circuit.* The Fire definition (`agents.md`) returns Σ unchanged when the trigger is false; operationally, runners typically evaluate `T_A[Σ](args)` *before* invoking Fire and skip the invocation when false. This is observationally equivalent to invoking Fire and getting Σ back, and saves the (small) overhead of an Apply that would have no emissions. The progress-discipline check applies only after non-no-op fires.


## Run4 — Bounded-W Detection Outside PL

The second violation regime: detecting bounded-W violations.

**Run4 — BoundedWDetectionRequiresOperationalBookkeeping (META).** Bounded-W violations are *not* detectable in `PL`. Detection requires operational state (fire counters, history) external to the substrate.

*Justification.* By the reachability argument in `quiescence.md`'s open questions, the cumulative trigger set `W(σ)` quantifies over reachable states, and reachability itself is a fixed-point computation not expressible in `PL` (per PC6 and `predicate-composition.md`'s open question on recursion). `BoundedW` is therefore a meta-level property — checkable at registry-design time by external analysis, but not as a substrate predicate at runtime.

The runner's only recourse for detecting bounded-W *symptoms* at runtime is operational bookkeeping: counting fires, tracking re-fire frequencies, monitoring `|W| / time` growth rates. None of these is a `PL` evaluation; all live in runner-process state.

*Consequences.*

(a) *Bounded-W detection is heuristic.* The runner can detect symptoms suggestive of bounded-W violation (a `(A, args)` re-firing an unusually large number of times, total fires exceeding a registry-sized budget), but cannot decide bounded-W from substrate state alone.

(b) *Heuristic thresholds are operational policy.* What threshold defines "unusually large" is a runner choice. Tight thresholds catch violations early but produce false positives; loose thresholds reduce false positives but allow longer divergent runs. The choice is operational, not substrate-derivable.

(c) *Bounded-W violation symptoms are observable but not provable.* A runner that observes a `(A, args)` firing 1000 times has *evidence* the registry's bounded-W contract may be violated, but no proof. Confirming the violation requires registry-level analysis the runner does not perform.

(d) *The architectural commitment surfaces.* Progress-discipline is detectable in `PL` (Run3); bounded W is not. The runner inherits both detection responsibilities but must implement them through different mechanisms — the first through predicate evaluation, the second through bookkeeping. This asymmetry is structural, not an implementation oversight.

(e) *Stochastic-body agents are a registry-recognized bounded-W pressure.* When `act_A` samples from a distribution (LLM-driven reviewers, model-based scouts), each re-fire is an independent draw and the cumulative trigger set grows even on already-quiescent state. The runner's countermeasure is registered as an operational stopping rule rather than a substrate change — see *Stochastic-agent stopping rules* in *Operational Concerns* below.


## Run5 — Violation-Response Policy

When a runner detects a violation (via Run3 or Run4 mechanisms), it must respond. The substrate spec does not commit to a specific response; instead, the runner is parameterized over a policy module.

**Definition — ViolationKind.** A violation is one of:

- *ProgressDisciplineViolation* `(A, args, Σ)` — observed by Run3: `T_A[Σ'](args) = ⊤` after a fire.
- *BoundedWSymptom* `(A, args, count)` — observed by Run4: re-fire frequency or fire count exceeds heuristic threshold.

**Definition — ViolationResponsePolicy.** A *policy module* `Π` is a function

`Π : ViolationKind → RunnerAction`

with `RunnerAction ∈ {LogContinue, HaltAndEscalate, RetryWithBudget, FlagAndProceed}`. The runner consults Π on each violation observation and applies the returned action.

The runner spec does not prescribe a specific Π; it admits any policy module that respects substrate invariants (does not Emit unauthorized tuples, does not fabricate provenance). Concrete instances of Π are the runner's design choice.

**Run5 — RunnerIsPolicyParameterized (META).** The runner spec is open-parameterized over Π. A runner with policy Π_1 and a runner with policy Π_2 are both spec-compliant; their behavior under violation differs.

*Status.* Run5 is META: it identifies a deferred design surface, not a theorem.

*Consequences.*

(a) *Policy choices are deployment-specific.* A development-time runner might choose `LogContinue` for all violations (loose, observes patterns); a production runner might choose `HaltAndEscalate` for `ProgressDisciplineViolation` and `RetryWithBudget` for `BoundedWSymptom`.

(b) *Policy can degrade gracefully.* `RetryWithBudget` is a typical compromise: the runner attempts to recover from a probabilistic progress-discipline failure by re-running the agent with a budget of re-attempts; if the budget is exhausted, the runner falls back to `HaltAndEscalate`. This corresponds to the *probabilistic progress-discipline* open question in `quiescence.md`.

(c) *Policy outputs are runner state, not substrate state.* `LogContinue` writes to the runner's log; it does *not* emit substrate facts. If a deployment wants the violation to be recorded in the substrate (for audit, for downstream agents to consume), the policy must construct an explicit emission — which itself requires a Provenance binding and shape conformance, no different from any other Emit.


## Worked Example — Producer-Refiner Under Round-Robin

We trace the round-robin runner executing on the producer-refiner registry from `agents.md` and `quiescence.md`, first under contract-respecting refinement (terminates) and then under the failure case (bounded-W symptom triggers Π).

*Registry.* `R = {P, Refiner}` with `P` triggering on unreviewed claims and `Refiner` triggering on unresolved revise comments (per `quiescence.md`'s worked example). Π is the policy `LogContinue` for `ProgressDisciplineViolation`, `HaltAndEscalate` for `BoundedWSymptom` exceeding a threshold of `10 · |R|` fires per `(A, args)` pair.

*Initial state.* `Σ_0` with `dom(Σ_0.C) = {d_1, d_2, d_3}`, where `d_1, d_2` are classified as claims and `d_3` is non-claim content. No reviews, no comments, no resolutions.

### Successful run (refinement does not introduce new claims)

*Cycle 1, starting at Σ_0.*

Round-robin iterates `R = (P, Refiner)`:

For P: iterate `[D_P]_{Σ_0} = dom(Σ_0.C) = {d_1, d_2, d_3}`.
- `args = d_1`: `T_P(d_1) = is_claim(d_1) ∧ ¬has_review(d_1) = ⊤ ∧ ⊤ = ⊤`. Fire. P emits a review classifier targeting `d_1` and a revise comment `τ_1` targeting `d_1`. Provenance tuples emitted by AG3. Run3 check: `T_P[Σ'](d_1) = is_claim(d_1) ∧ ¬⊤ = ⊥`. ✓
- `args = d_2`: similar. Fire. Emits review and revise comment `τ_2` targeting `d_2`. Run3 check passes.
- `args = d_3`: `T_P(d_3) = ⊥ ∧ ... = ⊥`. Skip.

For Refiner: iterate `[D_Refiner]_{Σ_{post-P}} = A_{K_revise} = {τ_1, τ_2}`.
- `args = τ_1`: `T_R(τ_1) = ¬resolved_by(τ_1, K_res) = ⊤`. Fire. Refiner emits a resolution targeting `addr(τ_1)` plus content edits to `d_1`. Content edits do not introduce new claims. Run3 check: `T_R[Σ''](τ_1) = ¬⊤ = ⊥`. ✓
- `args = τ_2`: similar. Fire. Refiner emits resolution targeting `addr(τ_2)` plus content edits to `d_2`. Run3 check passes.

End of cycle 1. Quiescence detection on Σ_1:
- For P: `(∀ d ∈ dom(Σ_1.C) :: ¬T_P(d))`. d_1, d_2 have reviews; d_3 is not a claim; no new content. ✓
- For Refiner: `(∀ τ ∈ A_{K_revise}_{Σ_1} :: ¬T_R(τ))`. Both revise comments resolved. ✓
- `quiescent[Σ_1] = ⊤`. Halt.

Total cycles: 1. Total real fires: 4 (two by P, two by Refiner). Operational bookkeeping: `count[(P, d_1)] = count[(P, d_2)] = count[(Refiner, τ_1)] = count[(Refiner, τ_2)] = 1`. No threshold tripped.

### Failure run (refinement introduces new claims)

Same Σ_0. Same registry except `Refiner`'s content edits introduce a new claim each time it fires (violating the `Post_R` strengthening required for stratification per `quiescence.md`'s worked example).

*Cycle 1.* Same as above through P's fires. Refiner fires on `τ_1`, emits resolution + content edit creating new document `d_4` classified as a claim. Refiner fires on `τ_2`, similarly creating `d_5`. End of cycle: `dom(Σ.C) = {d_1, ..., d_5}`, `d_4, d_5` are unreviewed claims. Quiescence check: `T_P(d_4) = ⊤`, `T_P(d_5) = ⊤`. Not quiescent.

*Cycle 2.* P fires on `d_4` (creating review + revise comment `τ_4`), on `d_5` (creating `τ_5`). Refiner fires on `τ_4` (creating `d_6`), on `τ_5` (creating `d_7`). Continues.

*Cycle k.* By induction, each cycle creates two new claims and two new revise comments. The fire counts grow:
- `count[(P, d_4)] = 1, count[(P, d_5)] = 1, ...` (each new claim fired exactly once by P)
- `count[(Refiner, τ_4)] = 1, ...` (each new comment fired exactly once by Refiner)

Per-`(A, args)` counts stay at 1 (each agent is locally progress-disciplined). But the *aggregate* fire count grows: cycle k has `2k` real fires.

The runner's heuristic threshold catches this through aggregate growth: after some cycle threshold (e.g., `|W| > 10 · |R|` total), Π is invoked with `BoundedWSymptom`. The runner consults Π and applies `HaltAndEscalate`. The runner halts, logs the violation, and escalates to operator intervention.

*Diagnostic observation.* No single `(A, args)` shows pathological re-firing — per-pair counts are all 1. The symptom is *aggregate*, not *per-pair*. Π's threshold function must therefore consider both axes; a per-pair threshold alone would miss this failure mode. This is exactly the kind of operational subtlety that lives in Π's design space, not the substrate spec.


## Operational Concerns

This section gathers operational considerations that fall under the runner's responsibility but do not warrant separate properties.

**Quiescence detection strategy.** Q0 says `quiescent[Σ]` is decidable; it does not say *when* the runner should evaluate it. Two strategies:

- *Per-fire evaluation.* Evaluate `quiescent[Σ_{k+1}]` after every fire. Earliest detection; highest cost.
- *Per-cycle evaluation.* Evaluate `quiescent[Σ_{k+1}]` at the end of each round-robin cycle. Lower cost; small detection lag.

Per-cycle is the default (and is what Run2's proof relies on). The only correctness consequence of detection lag is that the runner may execute a few no-op fires after quiescence is reached but before detection. By Q1 (QuiescenceIsAbsorbing), these no-op fires preserve Σ, so correctness is unaffected; only efficiency is.

**Stochastic-agent stopping rules.** Run4 establishes that bounded-W violations are detected operationally rather than in `PL`. The simplest detection is per-pair fire count; richer heuristics calibrate against the empirical behavior of stochastic agent bodies.

When an agent's `act_A` is stochastic — e.g., an LLM-driven reviewer — its progress-discipline holds with probability `p < 1` on a given fire, and re-fires can produce different emissions on the same Σ. The substrate sees this as bounded-W pressure: cumulative trigger sets grow under repeated draws even on documents the reviewer has already passed CONVERGED on at least once. The operational countermeasure is to gate re-fires against multi-draw evidence rather than single-draw evidence.

Specific rule — *N-consecutive-clean*. The trigger gates off only after the latest N reviews on the target have all come back without `comment.revise` findings. With N fixed at trigger-registration time, the predicate `last_n_reviews_were_clean(addr, n)` lies in `PL` by PC1's bounded-quantification form — N comparisons over the review chain. The operational threshold N is the runner's policy choice; the predicate itself is `PL`-side. This is the preventive analog of Run5's `RetryWithBudget`: rather than retrying after a violation, the gate raises the bar for declaring termination, absorbing the sampler's tail draws without letting them count.

Calibration is empirical. Per [`docs/design-notes/stochastic-quiescence.md`](../../design-notes/stochastic-quiescence.md): `n = 2` for note-scope (large review surface, deep dependency cone where speculative findings have purchase); `n = 1` for per-property claim-scope (small review surface, fewer seams for the reviewer to surface polish work on). Single-CONVERGED proved unstable on ASN-36 note-reviews 79, 90, 93, 94 — each reopened on the next draw. Two-consecutive-CONVERGED reopened at 93+94→95 but with low-value findings ("expand auxiliary lemma"), indicating diminishing returns past the second consecutive clean draw. The design note carries the evidence and the architectural framing; this section records the rule the runner implements.

**Concurrent fires.** AG7 (FireIsAtomicForSubstratePurposes) admits serial scheduling. If the runner relaxes serialization to allow concurrent fires, it must specify a reconciliation rule — what happens when two concurrent fires emit overlapping tuples, when one's emission flips another's trigger mid-fire, when provenance attribution races.

The current runner spec does not commit to concurrent-fire semantics. Runners that relax AG7 must restate Run2's termination proof with explicit interleaving semantics. The Q5/Q6 chain assumed serial scheduling; a parallel theorem is open.

**Initial-state recovery.** The runner's initial state Σ_0 is consumed from the substrate's persisted store. The runner's contract with the persistence layer is at the implementation boundary, similar to its contract with Π at the deployment boundary. If the persisted store is malformed (fails Sh-conf or AG3 invariants), the runner cannot start. Recovery from corrupted persistence is outside the runner spec — it is a substrate-store concern, addressed at the implementation layer (filesystem, database, etc.).

**Observability.** A runner often emits operational state for monitoring: fire counts, cycle durations, violation logs. These are runner-process state, not substrate state. If they need to be substrate-visible (e.g., for downstream agents to consume violation history), the runner must Emit them via the standard interface — meaning they become first-class substrate facts subject to all spec constraints.


## Properties Introduced

| Label                    | Type   | Statement                                                                            | Status     |
|--------------------------|--------|--------------------------------------------------------------------------------------|------------|
| RoundRobinSchedule       | DEF    | A specific fair scheduling discipline iterating R then `[D_A]_Σ` per cycle           | introduced |
| ViolationKind            | DEF    | The two classes of detectable violation: progress-discipline and bounded-W symptom   | introduced |
| ViolationResponsePolicy  | DEF    | A function `Π : ViolationKind → RunnerAction` parameterizing the runner              | introduced |
| Run0                     | META   | RunnerArchitecture — a runner is scheduling + detection + policy, outside `PL`       | introduced |
| Run1                     | LEMMA  | RoundRobinIsFair — every reachable trigger-true `(A, args)` is attempted-or-displaced | introduced |
| Run2                     | THM    | RunnerSatisfiesQ6 — round-robin + per-cycle detection + progress-discipline + bounded W ⟹ halt in quiescent state | introduced |
| Run3                     | LEMMA  | ProgressViolationDetection — `T_A[Σ'](args) = ⊥` is a per-fire `PL` check            | introduced |
| Run4                     | META   | BoundedWDetectionRequiresOperationalBookkeeping — not in `PL`; heuristic only        | introduced |
| Run5                     | META   | RunnerIsPolicyParameterized — runner spec admits any Π respecting invariants         | introduced |


## Open Questions

- *PL-expressible necessary conditions for bounded W.* If a runtime-detectable symptom catches common bounded-W violations (e.g., a `PL` predicate that detects the producer-refiner cycle pattern from `quiescence.md`'s worked example), Run4's operational bookkeeping could be partially absorbed into Run3's `PL`-detection regime. Whether such a necessary condition exists for general registries is open.

- *Optimal scheduling discipline.* Run1 admits round-robin; other disciplines (priority-based, stratum-respecting, work-stealing) can be fair and may converge faster on specific registry classes. Whether any discipline is optimal in a meaningful sense (minimizing fire count, maximizing throughput, reducing detection lag) is registry-dependent and likely an empirical question.

- *Concurrent fire semantics.* AG7 admits serial scheduling. Under what reconciliation rules does concurrent firing remain spec-compliant? The simplest rule is "concurrent fires must be serializable" (i.e., the substrate state after concurrent execution must equal the substrate state under some serial interleaving). Whether weaker rules (last-writer-wins on shape-equivalent emissions; both-emissions-recorded for distinct ones) preserve Q5/Q6 is open.

- *Adaptive scheduling under detected violations.* When the runner detects a `BoundedWSymptom`, the policy module decides what to do. A more aggressive runner could *change* its scheduling discipline in response — e.g., switch from round-robin to priority-based, prioritizing agents with lower violation counts. Whether such adaptivity preserves fairness (and therefore Q6) requires a theorem; the simplest formulation degrades to "any adaptivity must remain fair across the entire run."

- *Runner identity and provenance.* The runner consults the substrate but does not emit on its own behalf — only on behalf of the agents it schedules. Should the runner have its own substrate address (for runner-level provenance, observability, or registry membership)? If yes, the runner becomes a degenerate kind of agent (one whose action is to invoke other agents' actions). If no, runner-level operational state stays out of the substrate. The choice has architectural consequences for self-modifying registries — a runner that registers new agents at runtime would benefit from being itself a substrate citizen.

- *Persistence and restart semantics.* The runner consumes Σ_0 from a persisted store. If a runner halts (gracefully or via crash) and is later restarted, it resumes from the persisted Σ. Q0 + Q1 ensure that quiescence detection is correct on the resumed state, but the runner's *operational state* (fire counters, scheduling position, policy module's history) is lost unless persisted separately. The interaction between substrate persistence (always-on, by R3) and runner persistence (optional, runner-implementation-dependent) deserves a design treatment.

- *Multi-runner coordination.* The current spec assumes a single runner per substrate. Multi-runner deployments — e.g., partitioning the agent registry across runners for throughput — require coordination on quiescence detection (when do all runners agree the system is quiescent?), violation responses (which runner's policy applies?), and concurrent-fire reconciliation across runners. None of this is in the current spec.

- *Aggregate vs per-pair bounded-W symptoms.* The worked example's failure case shows that per-`(A, args)` fire counts can stay at 1 while the aggregate `|W|` grows linearly. A bounded-W threshold function over per-pair counts alone misses this. Π's threshold design needs both axes, but the optimal weighting (when does a symptom warrant `HaltAndEscalate` vs `RetryWithBudget`?) is registry-dependent.