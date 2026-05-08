# Agents

*The active layer — the only operations that change the substrate.*

`predicate-composition.md` closes the static side of the substrate: typed relations, shape-conformant tuples, and a closed-form predicate language `PL` whose evaluation is read-only and pure (PC4). What `PL` cannot express is *what changes the substrate*. By PC4, predicates have no side effects; by PC6 (ExpressiveClosure), the language is exactly the closure of atomic templates under Boolean composition, quantification, and value composition — every member of which is a pure observation.

The substrate's state transitions in `typed-relations.md` (R0, TupleAddressFreshness; R3, TypedSliceMonotonicity) admit transitions but say nothing about *who* emits or *when*. This document fills that gap. An *agent* is the spec-level construct that holds together the trigger predicate (in `PL`), the action (the only operation that emits), and the provenance binding that attributes every emission to an addressable source.

The pipeline in full:

> R0–R7 (typed relations + operations) → Sh0–Sh5 (shape restrictions, slot accessors, templates) → PC0–PC6 (composed predicates) → **AG0–AG7** (agents) → quiescence + runner (next docs)

The substantive claim of this document is the **public-substrate / private-decision asymmetry** (AG5): the substrate, the predicate language, and quiescence checks are public — every observer evaluates them identically against any given Σ; each agent's *decision interior* — the function from "trigger fired" to "what tuples to emit" — is private. This asymmetry is what eliminates the need for cross-agent consensus algorithms: agents do not have to agree with each other; they have only to each be satisfied with the substrate. The substrate is the agreement medium.

We make this precise, register the static structure of agents, define what a fire does dynamically, and prove the well-typedness properties that justify the runner (next document) treating agents as a uniform population.


## Static / Dynamic Split

Agents inherit the static / dynamic separation from `predicate-composition.md`:

- *Static* (specification time, before any state): an agent's name, trigger expression, scope expression, action signature, and provenance binding. All static components are well-typed against `T_cat` and the shape registry alone; no Σ is consulted.
- *Dynamic* (evaluation / fire time, against a state Σ): trigger evaluation `T_A[Σ]`, scope enumeration `[D_A]_Σ`, action invocation `act_A(args, Σ)`, and the resulting state transition.

We write `T_A`, `D_A`, `act_A` for static components and `T_A[Σ]`, `[D_A]_Σ`, `act_A[Σ]` for their dynamic interpretations, in the notation of `predicate-composition.md`.


## Agent Specification

**Definition — Agent.** An *agent* is a tuple

`A = (name_A, S_A, T_A, D_A, act_A, prov_A)`

with components:

- `name_A ∈ A_doc` — the agent's *address*. Agents are document-addressable so the Provenance shape's from-slot (Sh3 with `t_F = A` ⊇ `A_doc`, `shapes.md`) can attribute emissions to them by ordinary substrate construction.
- `S_A` — a *signature* (a finite product of substrate-derived domains as in `predicate-composition.md`'s Signature definition).
- `T_A : S_A → Bool` — the *trigger predicate*, a member of the static predicate language `PL`.
- `D_A ∈ QD` — the *scope*, a quantification-domain expression whose dynamic interpretation `[D_A]_Σ` enumerates argument tuples to which `T_A` is applied. The component types of `[D_A]_Σ` must unify with `S_A`.
- `act_A : S_A × State → ℘_fin(EmissionSpec)` — the *action*. `EmissionSpec = {(K, F, G) : K ∈ T_cat, F G ∈ Endset, conf_K(F, G)}` is the set of shape-conformant emission specifications (Sh-conf, `shapes.md`).
- `prov_A ∈ T_cat` — the *provenance type* used to attribute this agent's emissions, with `shape(prov_A) = Provenance`.

**Definition — AgentRegistry.** A finite set `R = {A₁, ..., A_n}` of agents, fixed at substrate specification time. The registry is part of the substrate's static spec (alongside `T_cat` and the shape registry); the runner consumes it directly.

The registry's finiteness is essential for quiescence (next document): the convergence condition is a finite ∀ over `R`, and PC6 admits this only when `R` is enumerable in finite time. Substrate specifications that wish to grow the registry dynamically must either (a) commit to a finite static registry that includes provisions for inactive agents, or (b) accept that quiescence becomes a moving target.


## Trigger Well-Typedness (AG0, AG1)

**AG0 — AgentIdentity.** Every agent in `R` has a unique address:

`(A i, j ∈ R : i ≠ j :: name_i ≠ name_j)`

*Justification.* By registry construction — duplicate-name registrations are rejected at spec time. AG0 is the registry's contractual obligation, not a derivable theorem. Without AG0, two agents could share `name_A`, and their emissions would be indistinguishable in the audit trail (Provenance's `from₁(τ) = name_A` would resolve to a non-unique source).

**AG1 — TriggerWellTypedness.** For every `A ∈ R`:

(i) `T_A ∈ PL` — the trigger is a member of the static predicate language with signature `S_A → Bool`.

(ii) `D_A ∈ QD` — the scope is a static quantification-domain expression.

(iii) `S_A` and the component-type product of `[D_A]_Σ` unify under signature unification.

*Proof of decidability at spec time.* Each of (i)–(iii) is a static check independent of Σ.

(i) Membership in `PL` is decidable by structural induction on the predicate term against the shape registry: each leaf is verified to be in `V_atom` (static, see `predicate-composition.md`); each internal node is verified to apply PC0, PC1, or PC2 with type-compatible operands. Each step is finite; the term itself is finite.

(ii) Membership in `QD` is decidable similarly: each leaf is a base domain expression for some `K ∈ T_cat`; each internal node is a filter `{x ∈ D : P(x)}` whose D is recursively in `QD` and whose P is in `PL` with signature `D → Bool`.

(iii) Signature unification reduces to component-by-component type matching against the codomain set `Codom` (`predicate-composition.md`). For each position `i` of `S_A`, the corresponding position in `[D_A]_Σ`'s component product must have the same Codom value. Decidable by finite enumeration.

All three checks are performed at registry construction; non-conformant agents are rejected. ∎

*Consequences.*

(a) *Triggers are type-checkable without state.* A registry can be validated against `T_cat` and the shape registry before any Σ is in hand. This is the static / dynamic separation `predicate-composition.md` was designed to support.

(b) *Trigger evaluation is decidable per fire.* By PC4 (Purity) and PC5 (Termination), each `T_A[Σ](args)` evaluation produces a Bool in finite time. The runner's per-fire cost is bounded.

(c) *Scope is finite per state.* By QD-fin (`predicate-composition.md`), `[D_A]_Σ` is finite at every reachable state, so the runner enumerates a bounded number of argument tuples per agent per cycle.


## Action Well-Typedness (AG2)

**AG2 — ActionWellTypedness (AXIOM).** For every `A ∈ R` and every `(args, Σ)`:

`(A (K, F, G) ∈ act_A(args, Σ) :: K ∈ T_cat ∧ conf_K(F, G))`

That is, every emission specification produced by `act_A` is shape-conformant for its declared type.

*Status.* AG2 is an axiom about the agent registry, not a theorem about agent internals. The substrate cannot inspect the action's body (AG4 below); it can only enforce conformance at Emit time via Sh-conf. AG2 says: *the registry registers only well-typed actions*. Violations of AG2 manifest as Emit failures at fire time, by Sh-conf.

*Justification.* The substrate's only protection against malformed emissions is Sh-conf, which rejects non-conformant tuples at the substrate boundary. Registering an agent whose action emits non-conformant tuples produces a runtime Emit failure on every fire — a soundness bug at the agent layer that the substrate cannot prevent at registration time without inspecting the action's body. AG2 is the registry's contractual obligation that this does not happen.

*Consequences.*

(a) *Actions are bounded per fire.* `℘_fin` in the codomain restricts each fire to a finite emission set. Unbounded fires would prevent termination and, by PC6, would not be substrate-evaluable.

(b) *Conformance is the substrate's enforcement layer.* AG2 says the registry registers conformant actions; Sh-conf says the substrate rejects non-conformant emissions. The two layers compose: registry-level discipline prevents most violations; substrate-level enforcement catches what the registry missed.

(c) *Actions may consult Σ.* The signature includes `State`, so actions can read substrate state to compute their emissions. This is *not* prohibited by purity — the action's *output* is allowed to depend on Σ; only its *side effects* on Σ are governed (it must Emit through the substrate's interface, never modify Σ directly, AG6).


## Provenance Discipline (AG3)

**AG3 — ProvenanceDiscipline (AXIOM).** For every fire of agent `A ∈ R` on args producing emissions `E = act_A(args, Σ)`, the resulting state transition `Σ → Σ'` decomposes as a sequence of pairs of Emits — one *primary* and one *provenance* — per element of `E`. Formally, there is an enumeration `E = {e₁, ..., e_m}` and intermediate states `Σ = Σ₀, Σ₁, Σ₁', Σ₂, Σ₂', ..., Σ_m, Σ_m' = Σ'` such that for each `i ∈ {1, ..., m}`:

(i) `Σ_{i-1}' → Σ_i` via `Emit_{K_i}(F_i, G_i)` where `e_i = (K_i, F_i, G_i)`, allocating fresh `addr(e_i) ∈ A_rel`.

(ii) `Σ_i → Σ_i'` via `Emit_{prov_A}({(name_A, δ(1, #name_A))}, {(addr(e_i), δ(1, #addr(e_i)))})`, allocating fresh `addr(prov_{e_i}) ∈ A_rel`.

(Initial convention: `Σ_0' = Σ`.)

The from-set and to-set of each provenance emission use canonical unit-depth spans (PrefixSpanCoverage, ASN-0043) that denote the singletons `{name_A}` and `{addr(e_i)}` respectively, so the Provenance shape's `(1, 0|1, A, A, ⊤)` constraints are satisfied with `c_F = 1`, `c_G = 1` (the non-empty branch of the `0|1` disjunction).

*Justification.* Without AG3, an emission's source is not recoverable from substrate state. Audit predicates ("which agent emitted τ?") would have to consult out-of-band metadata, violating the "everything important is a substrate fact" discipline of `typed-relations.md`. AG3 makes provenance an ordinary substrate observation.

*Consequences.*

(a) *Every emission has a substrate-recoverable source.* The query `outgoing_{prov_A}(name_A) = {τ ∈ A_{prov_A}^Σ : from₁(τ) = name_A}` (Provenance shape's atomic template, `shapes.md`) returns the addresses of all primary emissions A has ever been responsible for. Audit and attribution are first-class substrate facts.

(b) *Compound emissions stay attributable.* When `|E| > 1`, each `e ∈ E` gets its own provenance tuple. A fire's "why" is recoverable per-emission, not just per-fire.

(c) *Provenance shape is the bridge between agents and substrate.* The Provenance canonical shape (Sh5, `shapes.md`) is what makes agents addressable from inside the substrate. Without it, agents would be a meta-level construct invisible to substrate-level predicates.


## Decision Opacity (AG4)

**AG4 — DecisionOpacity (META).** The function body of `act_A` — the rule by which `act_A(args, Σ)` produces its emission set from `(args, Σ)` — is *not part of the substrate specification*. The registry stores a reference to `act_A` (its signature, its provenance binding, the constraint that its emissions are conformant), not its source code. Two agents `A, A'` with `name_A ≠ name_{A'}` but otherwise-identical static fields and different action bodies are *distinct agents*.

*Status.* AG4 is META, not LEMMA: it is a design property of the spec layer (what the registry chooses to expose) rather than a derivable theorem about substrate state.

*Justification.* Each agent's decision interior must be allowed to be opaque so that:

- LLM-driven agents can use non-deterministic decision processes (the same `(args, Σ)` may produce different emissions on different fires).
- Mechanical agents can use any deterministic algorithm without committing the algorithm's structure to the substrate spec.
- Agents can be reimplemented, optimized, or replaced without re-spec'ing the registry.

The substrate's correctness arguments must therefore depend only on the *external* observable behavior of agents — their triggers, their emissions, their provenance — never on the internal decision logic.

*Consequences.*

(a) *The substrate cannot prove what an agent will emit.* Predicates can ask "what has agent A emitted?" (via Provenance, AG3) but not "what would agent A emit on Σ?" The latter requires running `act_A`, which is private.

(b) *Two fires on identical (args, Σ) may differ.* AG4 admits non-determinism in `act_A`. A second fire on the same input may produce a different emission set; both are equally valid agent fires. The substrate distinguishes them only by their distinct addresses (R0).

(c) *Decision opacity does not weaken substrate guarantees.* R0–R7, Sh-conf, and PC0–PC6 hold regardless of what agents emit; they hold for *any* sequence of conformant emissions. AG4's opacity is contained — it does not propagate into the substrate's invariants.


## Public Substrate / Private Decision (AG5)

**AG5 — PublicPrivateAsymmetry (META).** The substrate exhibits a structural asymmetry between public and private:

(i) *Public.* Σ has the same value to every observer at any given time. `PL` evaluates identically against the same Σ regardless of who is asking. Quiescence checks (preview below; developed in `quiescence.md`) are public predicates. Provenance tuples (AG3) are public. Every emitted fact is public.

(ii) *Private.* Each agent's `act_A` body is private (AG4). The function from `(args, Σ)` to emissions is observable only through its emissions, not directly.

*Status.* AG5 is META — it concerns what kind of architecture this is, not what theorem the architecture admits. The asymmetry is structural, not contingent: changing it would require either making private decisions public (impossible for LLM agents; defeats the abstraction for mechanical ones) or making the substrate private (defeats every property in `typed-relations.md`).

*Consequences.*

(a) *No consensus algorithms are needed.* Two agents do not have to agree with each other about anything; each has only to be satisfied with the substrate. The substrate is the agreement medium. Disagreement at the decision layer is invisible (and irrelevant) at the substrate layer; only agreement on substrate state matters.

(b) *Reliability is structural, not per-agent.* Individual agents may make wrong decisions. The system tolerates this because correction is *structurally available*: a wrong decision is a substrate fact (R3 + AG3) that another agent's trigger can observe and respond to. The producer-refiner pair below is the basic correction mechanism.

(c) *Quiescence is satisfaction, not consensus.* When every agent's trigger evaluates false, no agent is "unhappy" with the substrate. Quiescence does not require that agents agreed with each other internally about *how to interpret* the state; it requires only that no agent's *public predicate* is currently unsatisfied.

(d) *The substrate's reliability does not depend on individual decision quality.* By AG5(i), any agent's wrong decision becomes a public fact that subsequent agents can correct. By PC4 + PC5, the correction is decidable at every state. The system's correctness emerges from substrate accumulation plus predicate re-evaluation, not from individual agent fires being correct.


## Fire (AG6, AG7)

**Definition — Fire.** Given `A ∈ R`, a state Σ, and `args ∈ [D_A]_Σ`, a *fire* of A on args at Σ is the operation:

`Fire(A, args, Σ) ≡ if T_A[Σ](args) then apply(act_A(args, Σ)) else Σ`

where `apply(E)` denotes the sequential composition of Emits described by AG3 (one primary Emit followed by one provenance Emit for each `e ∈ E`, in some enumeration order).

When `T_A[Σ](args) = ⊥`, the fire is a *no-op*: `Fire(A, args, Σ) = Σ`.
When `T_A[Σ](args) = ⊤`, the fire produces `Σ' = apply(act_A(args, Σ))`.

**AG6 — FireIsTransitionPreserving.** Every fire produces a transition `Σ → Σ'` that satisfies R0–R7 (typed-relations.md) and Sh-conf (shapes.md):

`(A A ∈ R, args ∈ [D_A]_Σ, Σ : Σ' = Fire(A, args, Σ) :: Σ → Σ' preserves R0–R7 ∧ Sh-conf)`

*Proof.* Two cases on the trigger value.

*Case T_A[Σ](args) = ⊥ (no-op).* `Σ' = Σ`. The identity transition trivially preserves all invariants.

*Case T_A[Σ](args) = ⊤.* By the Fire definition, `Σ' = apply(E)` where `E = act_A(args, Σ)`. By AG2, `E` is a finite set of shape-conformant emission specs. By AG3, `apply(E)` is a sequential composition of Emits indexed by `E`, with each primary Emit followed by its provenance Emit. We show by induction on the number of completed Emits that R0–R7 and Sh-conf hold at every intermediate state.

*Base.* The initial state `Σ_0 = Σ` satisfies R0–R7 and Sh-conf by hypothesis.

*Step.* Suppose `Σ_k` satisfies the invariants and the next Emit produces `Σ_{k+1}`. The Emit is either:

- A primary Emit `Emit_{K_i}(F_i, G_i)`: by AG2, `(K_i, F_i, G_i) ∈ EmissionSpec` is shape-conformant; by Sh-conf, the substrate accepts the emission. R0 produces a fresh address (L1c + GlobalUniqueness from `typed-relations.md`); R2 binds the new address to its value; R3 extends `L_{K_i}^{Σ_k} ⊆ L_{K_i}^{Σ_{k+1}}`; all other typed slices and the content/arrangement components are held in frame.

- A provenance Emit `Emit_{prov_A}(F', G')` where `F'` is the canonical unit-depth span at `name_A` and `G'` is the canonical unit-depth span at `addr(e_i)`. By the Provenance shape `(1, 0|1, A, A, ⊤)` (Sh5), this satisfies Sh-conf since `coverage(F') = {name_A} ⊆ A`, `coverage(G') = {addr(e_i)} ⊆ A`, `|coverage(F')| = 1`, `|coverage(G')| = 1`. By Sh-conf, the substrate accepts the emission; R0–R3 follow as in the primary case.

By induction, `Σ' = Σ_{2|E|}` satisfies R0–R7 and Sh-conf. ∎

**AG7 — FireAtomicityForSubstratePurposes (AXIOM).** From the substrate's perspective, a fire is atomic: external observers see only the fire-boundary states `Σ` (before) and `Σ' = Fire(A, args, Σ)` (after). Intermediate states `Σ_1, Σ_1', Σ_2, ...` of the AG3 sequence are not exposed.

*Status.* AG7 is an axiom about the runner's behavior, not a theorem about substrate primitives. Per `typed-relations.md`, Emit is the only primitive; multi-emission fires are *sequences* of Emits. AG7 says the runner does not interleave fires from different agents — each fire's emission sequence is contiguous from any external observer's point of view, and predicate evaluation between fires sees only fire-boundary states.

*Justification.* Without AG7, a predicate evaluated mid-fire would observe inconsistent intermediate states (e.g., a primary emission visible without its corresponding provenance tuple — violating the audit guarantee of AG3 from the observer's perspective). AG7 ensures that any Σ' an external observer sees is a fire-boundary state — every primary emission has its provenance tuple, and every fire is "all or nothing" from the audit perspective.

*Consequences.*

(a) *The runner serializes fires.* Concurrent fires require additional infrastructure (locking, transactions, or careful interleaving with explicit reconciliation). AG7 is the simplest discipline; weaker disciplines require extending the spec.

(b) *Mid-fire predicate evaluation is not a meaningful operation.* Predicates evaluate against fire-boundary states only. Asking "is this predicate true *during* a fire" has no well-defined answer.

(c) *Fire is the substrate-level granularity of change.* Although Fire decomposes into Emits internally (AG3), AG7 promotes Fire to the granularity at which observers reason. R3 (TypedSliceMonotonicity) holds at the Emit level *and* the Fire level; AG7 says only the latter is observable.


## Quiescence (Preview)

The runner's terminal condition is *quiescence*: a state Σ at which no agent's trigger evaluates true on any argument tuple in its scope.

**Definition — Quiescent.**

`quiescent(Σ) ≡ (∀ A ∈ R :: (∀ args ∈ [D_A]_Σ :: ¬T_A[Σ](args)))`

**AG-quiescent — QuiescenceIsInPL.** `quiescent ∈ PL` — the quiescence predicate is itself a member of the substrate's predicate language.

*Proof.* By AG1(i), each `T_A ∈ PL` and so `¬T_A ∈ PL` by PC0 (BooleanClosure). By AG1(ii), each `D_A ∈ QD`, so `(∀ args ∈ D_A :: ¬T_A[Σ](args))` is a quantification of a `PL` predicate over a `QD` domain — in `PL` by PC1 (QuantificationClosure). The outer quantifier ranges over `R`, which is a finite static set; modeling it as a base domain (or as a finite folded conjunction `⋀_{A ∈ R}`), the result is in `PL` by PC0/PC1. Therefore `quiescent ∈ PL`. ∎

By PC4 (Purity), `quiescent` is a pure function of Σ. By PC5 (TerminationOnFiniteSubstrate), evaluation halts in finite time at every reachable state. The substrate can recognize its own terminal state from inside the language. The runner (next document) makes this recognition operational.


## Examples

### Producer

A *producer* fires whenever a document needs work that has not yet been done.

`A = producer_review` with:

- `S_A = A_doc`
- `T_A(d) ≡ is_claim(d) ∧ ¬has_review(d)` &nbsp; — PC0 conjunction of two atomic predicates: a Classifier atom and a negated Coverage existential
- `D_A = C_dom` &nbsp; — the content-address domain expression; the trigger filters internally
- `act_A(d, Σ) ≡ {(K_review, ∅, {(d, δ(1, #d))})}` &nbsp; — emit a single Classifier-shape review tuple targeting d
- `prov_A = provenance.review_emission`

The runner enumerates `[D_A]_Σ = dom(Σ.C)`, fires A on each d, and produces a state in which `has_review(d)` is true for every d that was a claim. After firing, `T_A[Σ'](d) = ⊥` and the trigger is no longer satisfied.

### Refiner

A *refiner* fires to address findings someone else flagged.

`A = refiner_revise` with:

- `S_A = A_rel`
- `T_A(τ) ≡ τ ∈ A_{K_revise} ∧ ¬resolved_by(τ, K_res)` &nbsp; — a Boolean atom of Comment shape conjoined with a negated Resolution-existential
- `D_A = A_{K_revise}` &nbsp; — the active comment-revise relation domain expression; the trigger filters internally for already-resolved comments
- `act_A(τ, Σ) ≡ {(K_res, {(refiner_address, δ(1, #refiner_address))}, {(addr(τ), δ(1, #addr(τ)))}), ...}` &nbsp; — emit a Resolution-shape tuple targeting τ, plus content edits
- `prov_A = provenance.refinement`

The runner fires A on every unresolved comment. After firing, `resolved_by(τ, K_res) = ⊤`, and the trigger is no longer satisfied.

### Producer-Refiner Pair

The producer and refiner form a *correction loop* — the canonical instance of AG5(b)'s structural reliability. The producer reads substrate state and emits findings (comments); the refiner reads the findings and emits resolutions plus content edits. Neither decision is reliable in isolation. But:

- The producer's findings persist as substrate facts (R3).
- The refiner reads them as ordinary substrate observations (Comment shape's templates, `shapes.md`).
- The refiner's resolutions and edits are themselves substrate facts; the next producer pass evaluates against the *combined* state.

If both decisions were correct, the predicates flip and quiescence advances. If one was wrong, a downstream predicate stays unsatisfied and another agent fires. Reliability emerges from substrate accumulation plus predicate re-evaluation (AG5(d)), not from individual fires being correct.


## Properties Introduced

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| Agent | DEF | Tuple `(name, S, T, D, act, prov)` with static + dynamic split | introduced |
| AgentRegistry | DEF | Finite static set `R`, part of the substrate spec | introduced |
| EmissionSpec | DEF | Set of shape-conformant emission specifications `(K, F, G)` | introduced |
| Fire | DEF | Trigger evaluation + (conditional) action invocation + emission via AG3 | introduced |
| AG0 | AXIOM | AgentIdentity — every `A ∈ R` has a unique address | introduced |
| AG1 | LEMMA | TriggerWellTypedness — `T_A ∈ PL`, `D_A ∈ QD`, signatures unify (decidable at spec time) | introduced |
| AG2 | AXIOM | ActionWellTypedness — `act_A` produces shape-conformant emissions | introduced |
| AG3 | AXIOM | ProvenanceDiscipline — every emission carries a provenance tuple in `L_{prov_A}` | introduced |
| AG4 | META | DecisionOpacity — `act_A`'s body is private; not in the substrate spec | introduced |
| AG5 | META | PublicPrivateAsymmetry — substrate is public; decisions are private | introduced |
| AG6 | LEMMA | FireIsTransitionPreserving — fires preserve R0–R7 and Sh-conf | introduced |
| AG7 | AXIOM | FireAtomicityForSubstratePurposes — fires are observably all-or-nothing | introduced |
| quiescent | DEF | Predicate over Σ — no agent's trigger fires anywhere in its scope | introduced (developed in `quiescence.md`) |
| AG-quiescent | LEMMA | QuiescenceIsInPL — `quiescent ∈ PL` (= AG1 + PC0 + PC1) | introduced |


## Open Questions

- Should `name_A` be a *substrate fact* (e.g., a Classifier tuple `is_agent(name_A)` in `L_agent`) or a *spec fact* (a registry entry consulted only by the runner)? The current presentation has it both ways: `name_A ∈ A_doc` makes it a substrate-addressable document, but the registry is described as static spec. A cleaner formulation would commit to one — substrate-encoded agents could be discovered, registered dynamically, and audited via Classifier predicates, but at the cost of losing the static-registry guarantees AG0/AG1 rely on.

- Is `D_A` redundant with a tightly-filtered `T_A`? An agent with `D_A = C_dom` and a trigger that filters internally is observably equivalent (under AG6) to an agent with a tight `D_A` and a trigger that's always-true. Should the spec require one canonical form, or admit both as a notational convenience?

- `act_A` consults Σ and returns `EmissionSpec` *values*. Should the action also be allowed to consult its own most-recent emissions during a fire — i.e., to emit a tuple `e₁`, observe `addr(e₁)`, and use that address in `e₂`'s F or G? AG3's provenance discipline implicitly requires this for the runner (which emits `e` then `prov_e` with `addr(e)`); whether the action body itself can do the same — and how AG7 atomicity interacts with such mid-fire reads — is unclear.

- AG4 (DecisionOpacity) treats `act_A`'s body as opaque. But for *deterministic* mechanical agents, the body is well-defined and could in principle be reflected into `PL` via a meta-evaluation operator. Should the spec admit a "transparent agent" subclass whose `act_A` is itself a closed term in some extended language? This would let predicates ask "what would agent A emit on Σ?" — useful for static analysis but breaking the LLM-agent abstraction.

- AG7 (Fire atomicity) is the simplest discipline but may be too strong for high-throughput agent populations. Concurrent-fire semantics with a precise reconciliation rule (e.g., last-writer-wins for shape-equivalent emissions; both-emissions-recorded for distinct ones) would relax AG7 without losing soundness. What invariants would such a relaxation need?

- Quiescence is defined as `(∀ A : (∀ args : ¬T_A))`. Is there a *partial* quiescence — quiescence-relative-to-a-subset-of-agents, or quiescence-relative-to-a-document — that is a more useful operational target? The full quiescence may be unreachable in practice; a partial form might be the actual convergence condition the runner aims for.

- AG3 attaches one provenance tuple per primary emission via a single `prov_A` per agent. Should agents be allowed multiple provenance types — e.g., `prov_A.normal` and `prov_A.exceptional` for two emission classes — to let downstream predicates distinguish them? The current spec collapses this to a single shape; richer attribution is a registry-level extension.

- AG6 establishes that fires preserve substrate invariants but says nothing about fire *progress*. A fire that always produces the same emissions is technically conformant but contributes nothing to convergence. Should the spec admit a *progress predicate* — "every fire either advances quiescence or registers an idempotent no-op" — and if so, can this be expressed in `PL` without making `act_A` transparent (AG4)?

- The quiescence predicate `quiescent ∈ PL` requires `R` to be enumerable as a finite-domain quantifier. The current AgentRegistry is static and finite, so this works. But is there a sense in which `R` itself should be a domain expression in `QD` — e.g., `R = [some Classifier-shape relation]_Σ` — making the registry itself a substrate fact? This is the same question as the first open question, viewed from the quiescence side.