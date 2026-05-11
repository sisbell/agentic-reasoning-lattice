# Stochastic Quiescence

How the protocol handles agents whose progress-discipline holds probabilistically rather than deterministically — the seam between a deterministic stigmergic substrate and stochastic LLM-driven agents, and the operational response that closes it.

## The phenomenon

The substrate spec ([`quiescence.md`](../protocols/substrate/quiescence.md)) develops termination in three layers — recognizability (Q0/Q1), progress-discipline (Q2/Q3/Q4), conditional termination (Q5/Q6) — all under the assumption that each agent's contract holds deterministically. The Definition of ProgressDisciplined says:

> `T_A[Σ](args) = ⊤  ⟹  T_A[Σ'](args) = ⊥`

Every fire that found A's trigger true on `args` produces a state in which A's trigger is false on those same `args`. The implication is hard, not probabilistic. A deterministic agent satisfying progress-discipline produces a fire sequence whose real-fire count is bounded (Q5); under fairness, termination follows (Q6).

LLM-driven agents do not satisfy progress-discipline in the deterministic form. A reviewer fired on a document `d` produces a *sample* from a distribution conditioned on `(d, prompt, model)`. The same fire on the same Σ can emit zero `comment.revise` links one draw and one or more on the next. For a single fire, progress-discipline still holds locally — the emission set determines whether the trigger flips — but the substrate's bounded-W condition, which underwrites termination, becomes a registry-level concern about the cumulative draw distribution across re-fires, not a per-fire contract.

The result is **stochastic quiescence**: a state in which the substrate is structurally quiescent (no open `comment.revise`, no held resources, the link graph satisfies the deterministic predicate `quiescent[Σ]`), but a subsequent reviewer fire on the same state has p > 0 of emitting a new `comment.revise` and breaking quiescence. The break is not driven by a defect in the document, by a change in upstream content, or by a contract ambiguity. It is the sampler's tail.

Two layers of quiescence operate side by side. Substrate quiescence is structural and stable — once `quiescent[Σ]` evaluates true, Q1 guarantees the state is absorbing under Fire. Reviewer quiescence is statistical — CONVERGED is a verdict on one draw, and the next draw is an independent sample. The substrate's gate is firm; the reviewer's gate is statistical evidence about that gate.

## Empirical evidence — ASN-36 reviews 71–96

The note-review/note-revise loop on ASN-0036's strand-model note produced 26 reviews in sequence. Three of them returned CONVERGED with no document changes between adjacent runs.

Review 79 returned CONVERGED. Review 80 reopened with six findings whose revise commit message read "correct dependency citations for S7a, S8, S8a, D-CTG" — citation bookkeeping, no new claim content. Review 90 returned CONVERGED. Review 91 reopened with "clarify subspace identifier placement". Review 93 returned CONVERGED, review 94 returned CONVERGED on the same content, review 95 reopened with "expand S5 frame note and split auxiliary lemma into steps".

The document's word count over those 26 revises grew from 16,485 to 24,744 — a 50% increase. The growth was monotonic; no revise reduced the file. Reviews 71–78 produced an average of 338 words per revise landing structural content (new sections, formal contracts, notation systems, refactored proofs). Reviews 80–96 produced an average of 351 words per revise landing citation polish, dependency-list expansions, and proof-passage sharpening on prose that had already returned CONVERGED at least once.

The single-CONVERGED gate proved unstable: after 79 and after 90, the next draw reopened. The double-CONVERGED window (93 + 94) preceded a reopen on draw 95, but the reopened content was the lowest-value of the session — auxiliary-lemma expansion on prose that had passed two consecutive clean reviews.

The pattern is consistent with a sampler whose probability of returning CONVERGED on a genuinely-done document is high but less than one. Single-draw clean is a coin flip; two-consecutive-clean is meaningful evidence; three would buy diminishing returns at one additional draw's cost.

## Why this is not a substrate problem

[`quiescence.md`](../protocols/substrate/quiescence.md) already names this gap in its [Open Questions](../protocols/substrate/quiescence.md#open-questions):

> *Probabilistic progress-discipline.* For LLM-driven agents, the deterministic form of progress-discipline (per the Definition of ProgressDisciplined) may be operationally unrealistic — the agent may flip its trigger reliably *most* of the time. What does the substrate do when an agent satisfies progress-discipline with probability `p < 1`? Possibilities: log violations and continue; halt; retry; redesign the trigger to capture the probabilistic case.

The substrate's machinery does not need to change. Q0 (recognizability) and Q1 (absorbing) hold unconditionally on the link graph regardless of how the comments in it got there — the LLM origin of an emission is invisible to the predicate evaluation. Progress-discipline's per-fire form is satisfied by an LLM reviewer that emits a `review.content` classifier (flipping `has_been_reviewed`, `latest_review_was_clean`) regardless of whether the draw also produced `comment.revise` links.

The bound that breaks is bounded-W (Q5's registry-level hypothesis): the cumulative trigger set `W(σ)` across a fire sequence. The spec's [What the Runner Inherits](../protocols/substrate/quiescence.md#what-the-runner-inherits) section already states that bounded-W cannot be detected as a PL evaluation and must be defended operationally:

> *Bounded-W* violations cannot be detected this way — bounded W quantifies over reachable states, and reachability is a fixed-point computation outside `PL`. The runner's runtime defense against bounded-W violation is therefore necessarily *operational* — bookkeeping fire counts per `(A, args)` pair, halting on a heuristic threshold — rather than predicate-evaluation.

Stochastic quiescence handling fits exactly into this slot. The substrate stays deterministic. The runner's policy gains a heuristic threshold. The operational response is what the spec already authorizes for bounded-W defense; we are specifying the threshold and its empirical basis.

## Operational response: N-consecutive-CONVERGED

The stopping rule is: the note-review/claim-review trigger gates off once the latest N reviews on a target have all returned CONVERGED with no intervening revise edits. The substrate's predicate-layer extension is a generalization of the existing `latest_review_was_clean` to `last_n_reviews_were_clean(addr, n)` — read the addr's review chain, walk back N, return true iff all N carried `review.content` with zero attached `comment.revise` findings and no revise emissions landed between them.

With N fixed at trigger-registration time, the predicate's evaluation is bounded — N comparisons over the review chain — and the predicate lies in PL by PC1's bounded-quantification form. The operational stopping rule does not escape the predicate language; it composes inside it.

The gate lives at the `note_review` and `claim_review` triggers — the entry points to Stage 1 (note maturation) and Stage 4 (claim review) of the [Note-to-Claim Maturation Stigmergic Protocol](../protocols/maturation/note-to-claim.md). At both stages, the Correction Stigmergic Protocol primitive drives the inner review/revise loop; the N-consecutive-CONVERGED gate is the predicate-layer extension that conditions when each stage's Cycle Stigmergic Protocol primitive re-fires its reviewer against an apparently-quiescent target.

On the empirical evidence above, `n = 2` is the calibrated default. Single-CONVERGED reopens reliably (witnessed at review 79→80 and 90→91). Two-consecutive-CONVERGED reopens, but with low-value findings (witnessed at 93+94→95 with "expand auxiliary lemma"). The marginal information past the second consecutive draw is biased toward the sampler's tail rather than toward correctness findings; the additional draw cost is not justified by the additional findings' content.

The threshold likely scales inversely with operating-table size. Per-property claim files (small surface, less seam-space for a stochastic reviewer to find polish work on) probably converge reliably at `n = 1`; notes (large surface, deeper cone underneath) need `n = 2`. The substrate's predicate generalization admits per-trigger calibration — `claim_review` and `note_review` can pass different `n` values to the same predicate.

"Consecutive" must account for document changes between draws. Two CONVERGED draws separated by a revise emission count as one CONVERGED draw against the new content; the count resets when any revise landed between draws. The predicate's walk-back over the review chain reads each step's revise emissions in addition to the verdict, and stops the count at the first intervening revise.

## What this is not

**Not a substrate change.** Q0–Q10 hold as stated. The link graph stays deterministic. Predicates stay pure functions over substrate state.

**Not pheromone decay.** The substrate's [stigmergic coordination](stigmergic-coordination.md) replaces time-decay with explicit closure-as-emission, deliberately. Stochastic-quiescence handling does not reintroduce decay. Stale `comment.revise` links do not auto-resolve; auditability of every state change remains intact. The operational response operates *before* a finding becomes a substrate emission, or at the trigger-gate layer, not by silently expiring already-emitted findings.

**Not a probabilistic predicate.** The runner's stopping rule reads a deterministic predicate (`last_n_reviews_were_clean`) over substrate state. There is no confidence interval on a substrate fact, no Bayesian quiescence, no "soft" quiescent state.

**Not exploration tuning at the agent.** The reviewer's prompt is not modified to be more or less exploratory. The agent body is treated as an opaque sampler; the runner reasons about its draw distribution by counting consecutive CONVERGED verdicts, not by inspecting confidence or rate-tuning the agent.

## Why classical stigmergic systems do not have this gap

The biological and ACO precedent treats stochasticity as inherent and pervasive. Pheromone deposit is probabilistic. Edge selection is probabilistic — usually a softmax `τ^α · η^β` over local pheromone intensities. Pheromone evaporates by a factor `(1 - ρ)` each step, so old deposits fade unless re-reinforced. The system equilibrates by allowing stochastic exploration to push past stale gradients while decay clears out the speculative trails that exploration laid down.

Our substrate runs on stigmergic coordination *shape* — agents emit into a shared medium, other agents read and decide locally, coordination emerges without direct messaging — but not on stigmergic *dynamics*. We chose deterministic predicates, append-only emissions, and explicit closure instead of decay. The architectural rationale is auditability: every state change leaves a substrate-visible trace, no fact disappears silently, the link graph is a reasoning archive rather than a transient signaling field.

The composition that produces stochastic quiescence is specific to this stack: a deterministic stigmergic substrate plus stochastic LLM agents. The [Maturation Stigmergic Protocol](../protocols/maturation/note-to-claim.md) sits in the [Stigmergic Protocols](../protocols/README.md) family — Cachin-sense protocols whose coordination is substrate-mediated rather than direct-message-passing — and composes the primitives (Correction, Marker, Self-Review, Cycle) without inheriting the probabilistic dynamics of the biological precedent. A non-LLM implementation of the same protocol — a reviewer realized as a static checker or a deterministic policy — would have no stochastic quiescence problem; its progress-discipline would hold in the strict deterministic form. A probabilistic-substrate implementation in the ACO tradition would handle the speculative-finding problem through decay rather than through a consecutive-CONVERGED gate, at the cost of the auditability the substrate currently provides.

The seam is real but localized: the agent layer's body is stochastic; everything else — substrate, predicates, runner — is deterministic. The operational response sits at the trigger gate, which is the architectural boundary between the deterministic protocol layer and the stochastic agent layer.

## What this changes downstream

[`review-revise-iteration.md`](../patterns/review-revise-iteration.md) — the "When it converges" section currently lists four conditions, the last of which is "the reviewer files zero new `comment.revise` links." For a stochastic reviewer this is necessary but not sufficient; the condition is restated as "the reviewer files zero new `comment.revise` links across N consecutive draws on the same content."

[`quiescence.md`](../protocols/substrate/quiescence.md) — the Open Question on probabilistic progress-discipline is no longer open. The substrate stays deterministic; the operational response is specified here; the spec's existing authorization for runner-level bounded-W defense covers the implementation.

[`runner.md`](../protocols/substrate/runner.md) — the stopping rule formalized here is the runner's response to bounded-W risk in registries containing stochastic-body agents. The rule reads as one entry in the runner's policy table alongside fair scheduling and contract-violation handling.

## References

- Grassé, P.-P. (1959). *La reconstruction du nid et les coordinations interindividuelles chez Bellicositermes natalensis et Cubitermes sp.* Insectes Sociaux 6, 41–80. The original stigmergy paper. Treats stochasticity as inherent to the coordination model.
- Dorigo, M., & Stützle, T. (2004). *Ant Colony Optimization.* MIT Press. The canonical engineering treatment of stigmergic systems built on probabilistic deposit, probabilistic transition rules, and pheromone evaporation. Cited for the contrast: ACO's stochastic mechanisms are designed-in; ours arise from a different layer.
- Bonabeau, E., Dorigo, M., & Theraulaz, G. (1999). *Swarm Intelligence: From Natural to Artificial Systems.* Oxford University Press. Treats the stochastic/decay machinery as load-bearing for adaptive coordination, complementing this document's argument that omitting decay forces structural compensation elsewhere.

## Cross-references

- [Quiescence (substrate spec)](../protocols/substrate/quiescence.md) — the deterministic spec whose Open Question on probabilistic progress-discipline this document answers.
- [Stigmergic Coordination](stigmergic-coordination.md) — the design-note that establishes the substrate's explicit-closure-replaces-decay commitment. The choice that closes one design door (decay-based forgetting) and opens this one (operational gating for stochastic agents).
- [Review/Revise Iteration](../patterns/review-revise-iteration.md) — the pattern within which stochastic quiescence is observed. The stopping rule extends that pattern's convergence condition without changing the pattern itself.
- [Surface Expansion](../equilibrium/surface-expansion.md) — the equilibrium failure stochastic-quiescence can amplify on bloated files (the reviewer's tail draws find more seams on more surface). Distinct mechanism, related symptom; the two interact when a Sprawl-affected file is reviewed by a stochastic agent.
- [Reverse-Course Oscillation](../equilibrium/reverse-course-oscillation.md) — a separate failure mode driven by structural undecidability (no shared criterion between reviewer and reviser). Stochastic quiescence operates on a *settled* document; oscillation operates on an *unsettled* one. Both produce non-convergence; the mechanisms and resolutions differ.