# Substrate Protocol

A formal specification of the substrate that domain protocols build on — what facts are, what predicates can ask about them, what agents do to them, and how the system reaches a terminal state.

The six documents in this directory form a single chain. Each layer's contracts are explicit; each layer's open questions point cleanly at the next.

> [types](types.md) → [shapes](shapes.md) → [predicate-composition](predicate-composition.md) → [agents](agents.md) → [quiescence](quiescence.md) → [runner](runner.md)


## Strategy

The substrate's design is shaped by five commitments. Each one resolves a tension that would otherwise force a more complicated architecture.

**1. Append-only audit; mutation as set-difference.** The relational primitive `L_K` only grows (R3). Mutation works through *self-reference* (R5): a tuple in the retraction relation `L_R` whose to-set targets another tuple's address. The active subset `A_K = L_K \ {targeted-by-L_R}` is computed live; predicates evaluate against it. No mutation primitive, no version field, no garbage collection — just Emit and set-difference.

**2. Predicates as pure functions of public state.** Everything queryable is determined by `(Σ.C, Σ.M, Σ.L)` and the static spec. No memoization, no caching, no agent decision history is consulted. PC4 (Purity) makes this formal; it has consequences: predicate evaluation in cycle 30 has no memory of cycle 29; concurrent observers see the same answer; stale predicate values cannot poison the system because none are retained.

**3. Public substrate / private decisions.** The substrate, the predicate language, and quiescence checks are public — every observer evaluates them identically. Each agent's decision *interior* — the function from "trigger fired" to "what tuples to emit" — is private (AG4, AG5). This asymmetry eliminates the need for consensus algorithms: agents do not have to agree with each other; they have only to each be satisfied with the substrate. The substrate is the agreement medium.

**4. Static spec / dynamic evaluation split.** Vocabulary (`T_cat`, shape registry, agent registry) and predicate language (`PL`, `QD`) are static — fixed at substrate specification time, type-checkable without any state. Evaluation `[·]_Σ` is dynamic. Predicate compilation can happen against the spec alone; tooling can verify well-typedness without running anything; closure proofs separate syntactic decomposition from semantic evaluation.

**5. Conditional termination, honest about it.** Forward-chaining systems generically cannot prove unconditional termination. The substrate guarantees what it can: quiescence is recognizable from any state (Q0), and recognized states are stable (Q1). Termination is a *theorem* under stated conditions — per-agent progress-discipline (Q3) plus registry-level bounded W (Q5) plus runner-side fairness (Run1). Each condition is checkable at its own layer; none is hidden.

The substrate inherits the relational primitive from Nelson's typed link via ASN-0043. Properties R0–R7 are restatements of ASN-0043 lemmas in relational vocabulary; only R6 (the active subset) is the substrate's own contribution, made possible by R5 (self-reference) and R3 (the audit trail it is computed against).


## Reading Order

Each document depends only on the ones before it. Read in order; do not skip layers.

### 1. [types.md](types.md) — Typed relations and the three operations

Establishes the substrate's primitive: typed relations `L_K ⊆ ℘(A) × ℘(A)` over a partitioned address universe `A = A_doc ⊔ A_rel`. Defines `Emit_K`, `Observe_K`, `Nullify`. Introduces R0–R7, with R6 (active subset) the substrate's own addition to Nelson's link model.

### 2. [shapes.md](shapes.md) — Shape restrictions and predicate templates

Restricts each `L_K` with a *shape* — a tuple `(c_F, c_G, t_F, t_G, idem)` constraining cardinality, target domain, and idempotency. Each canonical shape generates a predicate template family. Introduces Sh-conf (the shape conformance axiom on Emit) and Sh0–Sh5. The shape catalog (Classifier, Attribute, Citation, Comment, Resolution, Retraction, Coverage, Provenance, Tuple-Classifier) is closed and bounds the substrate's expressive ceiling.

### 3. [predicate-composition.md](predicate-composition.md) — The predicate language `PL`

Closes the static side of the substrate. Atomic predicates from Sh5 compose under PC0 (Boolean), PC1 (quantification), PC2 (value composition). Quantification domains form a finite class `QD`. PC4 proves purity; PC5 proves termination; PC6 proves expressive closure — `PL` is exactly the closure of atoms under these three operators. The static `PL` and dynamic `[·]_Σ` distinction is foregrounded throughout.

### 4. [agents.md](agents.md) — The active layer

Introduces *agents* — the only constructs that emit. An agent is a static tuple `(name, S, T, D, act, prov)` plus a dynamic Fire that conditionally invokes `act` and emits with provenance attribution. AG3 (provenance discipline), AG6 (fire transitions preserve substrate invariants), and AG5 (PublicPrivateAsymmetry — the document's substantive claim) commit the spec to the public/private architecture. AG-quiescent shows that the convergence condition is itself in `PL`.

### 5. [quiescence.md](quiescence.md) — The terminal state

Develops the convergence story in three layers. Layer 1 (Q0, Q1): quiescence is recognizable and absorbing — unconditional. Layer 2 (Q2, Q3, Q4): per-agent progress-discipline as a contract, statically checkable via emission contracts `Post_A ∈ PL`. Layer 3 (Q5, Q6): conditional termination — real fires bounded by `|W(σ)|` under progress-discipline + bounded W; full termination requires fairness, deferred to the runner. The producer-refiner failure mode shows why bounded W does real work that progress-discipline cannot.

### 6. [runner.md](runner.md) — The operational layer

Specifies what the spec leaves operational: scheduling, detection, violation response. Run1 exhibits round-robin as a fair scheduling discipline; Run2 closes Q6 against it. Run3 / Run4 split detection into two regimes: progress-discipline violations are PL-detectable per fire; bounded-W violations require operational bookkeeping outside `PL`. Run5 parameterizes the runner over a violation-response policy.


## How the Layers Compose

Each layer adds exactly what is needed for the next; nothing is structural ornament.

| Layer                  | Contributes                                                                | Used by                              |
|------------------------|----------------------------------------------------------------------------|--------------------------------------|
| types (R)              | `L_K`, `addr`, `A_K`, three operations                                     | shapes, predicate-composition        |
| shapes (Sh)            | Shape-conformant relations; predicate templates `Tpl(shape(K))`            | predicate-composition                |
| predicate-composition (PC) | `PL`, `QD`, atom + composition closure                                  | agents (triggers), quiescence        |
| agents (AG)            | Agent registry, Fire semantics, public/private asymmetry                   | quiescence, runner                   |
| quiescence (Q)         | Recognizability, progress-discipline contracts, conditional termination    | runner                               |
| runner (Run)           | Fair scheduling, violation detection, policy parameterization              | (operational)                        |

The chain bottoms out in Nelson's typed link (ASN-0043, ASN-0036, ASN-0034) and tops out at the runner's operational loop. Below the chain are the link-model lemmas the substrate inherits; above it are domain protocols — registries built on the substrate spec.


## What This Specifies vs. What It Does Not

**In scope.** The relational primitive, shape restrictions, predicate language, agent semantics, quiescence theorems, runner operational structure. The full substrate-level contract under which any registry can be evaluated.

**Out of scope.**

- *Implementation.* Filesystem-backed storage, Python module layout, persistence schemas. Deployment artifacts.
- *Domain protocols.* Claim convergence, note convergence, consultation, maturation, discovery — each is a specific registry built on this stack with its own agents, emission contracts, and bounded-W argument.
- *Lattice operations.* Extract, absorb, promote, clone are agent classes within domain registries, not substrate primitives.
- *Multi-runner / multi-substrate.* Single-runner over a single substrate is the assumed scope.

A domain protocol is a triple `(R, {Post_A}_{A∈R}, BoundedWArgument)` — registry, per-agent emission contracts, and the registry-design proof of bounded W. Specific domain protocols formalize one such triple each. The substrate spec admits any registry; specific ones are domain protocols above this stack.


## Property Index

Quick lookup for property numbers cited across the chain.

- **R0–R7** — types.md
- **Sh-conf, Sh0–Sh5** — shapes.md
- **PC0–PC6** — predicate-composition.md
- **AG0–AG7, AG-quiescent** — agents.md
- **Q0–Q6** — quiescence.md
- **Run0–Run5** — runner.md

Each document also includes a *Properties Introduced* table at the end, an *Open Questions* section flagging genuine gaps, and inline citations back to the link-model lemmas in ASN-0043 / ASN-0036 / ASN-0034 where applicable.
