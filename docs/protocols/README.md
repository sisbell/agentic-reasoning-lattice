# Protocol Stack

This directory specifies the architectural protocol stack for the system. It uses *protocol* in Cachin's sense — a legal succession of messages between processes, with well-defined participants, transitions, and termination. The stack distinguishes the protocols themselves (which describe legal successions) from the foundation those protocols compose against (the medium, the message language, the process model, the scheduling discipline).

## The layer distinction

The protocol stack divides into three architectural layers, with each subdirectory mapping cleanly onto a distributed-systems concept:

| Subdirectory | What it is | Cachin terminology |
|---|---|---|
| `substrate/` | Medium + message format + execution model | Communication primitive + system model + message language |
| `agents/` | Process specifications (the actors that emit messages) | Processes / participants |
| `maturation/` | Maturation Stigmergic Protocols (legal successions composing primitives) | Protocol |

Under this division, **only `maturation/` contains protocols in Cachin's strict sense.** Substrate and agents are the foundation those protocols compose against. They are protocol *infrastructure* — necessary to define what messages exist, what processes can send them, and what guarantees hold — but not protocols themselves.

The protocols in `maturation/` are **Maturation Stigmergic Protocols** — content transforms through progressive stages (identity grant, verification, formalization, refinement) toward stable form, terminating at scope quiescence at a designated tier. Coordination is substrate-mediated: agents read substrate state and emit; no direct message passing.

## A finer Cachin mapping

Within each layer, the substrate spec further decomposes into the standard distributed-systems primitives:

| Cachin primitive | Where it lives in the stack |
|---|---|
| System model (what processes exist, what guarantees hold) | `agents/` (AG0–AG7) |
| Communication primitive (the message-emission operation) | Emit, defined in `substrate/types.md` |
| Medium / state (where messages persist) | Σ, the substrate state space (R0–R7) |
| Message format / well-formedness | Shapes (Sh-conf + Sh0–Sh5 in `substrate/shapes.md`) |
| Message invariants | Predicates (PC0–PC6); trigger predicates `T_A` (pre-send) and emission contracts `Post_A` (post-send invariants) |
| Termination condition | Quiescence (Q0–Q10 in `substrate/quiescence.md`) |
| Scheduling discipline | Runner (Run0–Run5 in `substrate/runner.md`) |

This finer split exposes that the substrate itself contains a *primitive protocol* — the Emit protocol that governs valid state transitions of Σ. Maturation protocols compose on top of this primitive protocol.

## Stigmergic Protocol primitives

A Maturation Stigmergic Protocol is rarely monolithic. It is more accurately a *composition* of Stigmergic Protocol primitives, each of which is itself a Cachin-sense protocol with its own safety, liveness, and termination properties:

- **Correction Stigmergic Protocol** — agent A emits `comment.<kind>` on a target; agent B reads the open comment as its trigger condition; B emits `resolution.<kind>` to close. Terminates when the comment has a resolution. The K subtype discriminates use cases (`comment.revise` for content correction; `comment.violation` for structural correction); the protocol mechanism is identical. This is the architectural correction loop — two unreliable decisions checking each other through substrate (AG5).
- **Marker Stigmergic Protocol** — agent A emits a non-comment classifier or status tuple; agent B reads the marker as its initiation condition. Unidirectional; no closure expected of A. Used for stage-transition handoffs and cycle-control gating.
- **Self-Review Stigmergic Protocol** — a single (typically operator-gated) fire emits primary work *plus* a scoped self-review of that work. The self-review's `comment.<kind>` emissions seed downstream Correction Stigmergic Protocol cycles. Compound emission seeding deferred refinement.
- **Cycle Stigmergic Protocol** — agent A fires once per cycle on a target; runner re-fires until the target's quiescence predicate flips ⊤. Convergence pattern; termination via Q5/Q6 + Run2 at the per-target scope.

Each primitive has its own safety property, liveness property (under runner fairness), and termination condition — all defined against the substrate spec. Maturation Stigmergic Protocols compose them into end-to-end content-transformation arcs.

Caste-doc references to protocol composition use the family-level term ("Stigmergic Protocol composition") rather than naming a specific specialization. Castes are protocol-family-agnostic — a producer is a producer because of its substrate-emission pattern, not because of which protocol family it participates in. Specific protocol-family membership is documented at the protocol layer (in `maturation/` for Maturation Stigmergic Protocols, in any future sibling directories for other Stigmergic Protocol families).

## Substrate as message bus

The protocols in this stack are *stigmergic* (Grassé 1959) — coordination is substrate-mediated rather than via direct message passing. The substrate is the message bus, with four properties:

- *Durable* — every message persists (R3 monotonicity).
- *Queryable* — predicates over substrate state are first-class (PC0–PC6).
- *Monotonic at the L_K level* — no message is ever deleted, only superseded by retraction (which is itself an emission).
- *Public* — every process reads the same substrate state (AG5 PublicPrivateAsymmetry).

**Protocol hierarchy in this stack:**

```
Stigmergic Protocols
├── Primitives:
│   ├── Correction Stigmergic Protocol  (comment → resolution closure)
│   ├── Marker Stigmergic Protocol      (classifier-based one-way handoff)
│   ├── Self-Review Stigmergic Protocol (compound modify+review fire)
│   └── Cycle Stigmergic Protocol       (runner-driven convergence)
└── Compositions:
    └── Maturation Stigmergic Protocol  (content-transformation through stages)
        └── Note-to-Claim Maturation Stigmergic Protocol
```

## How to read the stack

For new readers, the recommended order is:

1. `substrate/types.md` — the medium and Emit operation
2. `substrate/shapes.md` — the message format
3. `substrate/predicate-composition.md` — the predicate language for message invariants
4. `substrate/agents.md` — the process model
5. `substrate/quiescence.md` — the termination condition
6. `substrate/runner.md` — the scheduling discipline
7. `agents/README.md` — the agent registry overview, caste taxonomy, and stigmergic vs sequential hand-off framing
8. `agents/{producers,refiners,scouts}.md` — per-agent specifications
9. `maturation/note-to-claim.md` — the Note-to-Claim Maturation Stigmergic Protocol, the first end-to-end protocol in this stack

The substrate spec is forward-only — each document depends on previous ones, with explicit pipeline references. The agent caste docs depend on the substrate spec. Maturation protocols compose against both.

## What is not a protocol

Three categories of artifact that look protocol-shaped but are not protocols in Cachin's sense:

- *The substrate spec.* It defines the system model, communication primitive, message format, and termination condition. It is the foundation protocols compose against, not a protocol itself. (The Emit protocol *is* a primitive protocol, but it is a substrate-level mechanism, not a system-level one.)
- *The agent registry.* Each agent specification is a process specification — what messages a process can send, under what initiation conditions, satisfying what post-send invariants. Processes are participants in protocols, not protocols themselves.
- *The runner.* It is a scheduling discipline — how processes are dispatched. It enforces the fairness assumption that maturation protocols rely on for termination, but it is not itself a protocol.

A useful test: *does this artifact specify a legal succession of agent fires that terminates in quiescence at a designated tier?* If yes, it is a protocol. If it specifies what processes can do, what messages are well-formed, or how processes are dispatched, it is protocol infrastructure.

## Open questions for the protocol layer

Two architectural concerns for future protocol work:

- **Protocol composition.** Multiple maturation protocols can run concurrently. Note-to-claim and (future) cross-lattice synthesis interact through shared substrate state. The composition rules — safety properties under interleaving, fairness across concurrent protocols, termination of compositions — are partially captured by Q9's scope monotonicity and the cross-tier interference open question, but a formal protocol-composition treatment is pending.
- **Operator as protocol participant.** Per `agents/README.md`'s discussion of stigmergic-with-operator-as-producer: in the limit, all coordination is stigmergic, with the operator playing producer-role for content-authoring hand-offs. This makes the operator a *participant* in protocols rather than an external invoker. The formal treatment of operator-as-process (AG0 identity, AG3 provenance, latency relative to runner) is pending.

## Cross-references

- `substrate/` — the primitive protocol layer.
- `agents/` — the process specifications.
- `maturation/` — the protocols proper.
- (External) Cachin, Guerraoui, Rodrigues. *Introduction to Reliable and Secure Distributed Programming.* Springer, 2nd edition, 2011. The system-model / processes / protocol decomposition this stack adopts.