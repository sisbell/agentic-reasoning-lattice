# Agentic Protocols

The system is a stack of protocols sharing a [substrate](../glossary.md#s) (a persistent, append-only graph of documents and typed links). Following the modular formalism of Cachin (*Reliable and Secure Distributed Programming*) — but for LLM-agent coordination rather than distributed nodes.

A protocol defines what must hold (the convergence predicate, the output contract, the safety and liveness properties). [Choreography](../glossary.md#c) defines how to make it hold (scope strategy, review order, context assembly, concurrency policy). The protocol IS the predicate or contract; everything else is choreography.

## Protocol shapes

Protocols in this system come in two shapes:

- **Convergence-shaped** — iterative; terminates when a graph predicate holds. Note Convergence, Claim Convergence. Safety/liveness include indication soundness for the predicate.
- **Production-shaped** — one-shot, with coordination structure between participants. Consultation. Safety properties are output contracts plus the channel-level invariants (vocabulary firewall, channel independence) that govern the participants while they run.

The companion [Modules](../modules/README.md) — Substrate, Agent, Claim Derivation — also follow Cachin's modular formalism but specify transformation rather than ongoing interaction. They provide what protocols compose with.

## The pipeline

Content matures through four stages, each with its own protocol or protocols:

```
─── discovery stage ──────────                ─── claim derivation → claim convergence ─        ── verification ──
 Consultation ──→ Note Convergence  ──→  Claim Derivation ──→ Claim Convergence      ──→  (Verification, TBD)
 (production)     (convergence)          (module)               (convergence)
                                                                                                                
       │                  │                       │                       │
       │ produces a note  │ refines that          │ decomposes the        │ refines per-claim
       │                  │ note in place         │ note into claim files │ contracts
       │                  │                       │                       │
       │                  │ specialize            │                       │ specialize
       │                  ▼                       │                       ▼
       │      ┌───────────────────────────────────────────────────────────────────┐
       │      │                  Convergence Protocol                             │   shared module
       │      │       predicate + comment/resolution link types + S1-S6, L1-L4    │
       │      └───────────────────────────────────────────────────────────────────┘
       │                                       │
       │                                       ▼ relies on
       ▼                              ┌─────────────────┐
   (substrate)                        │    Substrate    │   permanence (SUB1)
                                      │  (link graph)   │   query soundness (SUB2)
                                      └─────────────────┘   count consistency (SUB3)
```

Above the pipeline sits the meta-protocol:

```
                           ┌──────────────────────────────────────────┐
                           │           Maturation Protocol            │
                           │  composes the pipeline, manages stage    │
                           │  transitions, executes lattice operations│
                           │  (extract, absorb, scope promotion);     │
                           │  reaches quiescence rather than converge │
                           └──────────────────────────────────────────┘
```

The layering enforces what is actually shared vs. what is scale-specific. Both convergence protocols use the same predicate, comment/resolution machinery, and safety guarantees — written once in the convergence module. Each specialization adds what its scale needs: note convergence adds OUT_OF_SCOPE routing for lattice signals; claim convergence adds structural validation, the algorithm, and correctness arguments. The production protocols sit upstream of (consultation) or between (claim derivation) the convergence protocols — they don't specialize the convergence module because they don't have a predicate.

## The protocols

Listed by pipeline position. The shape of each is one-line:

### Discovery stage

- **[Consultation Protocol](consultation-protocol.md)** — *production*; one-shot, terminates on output production. Produces an initial note from a campaign-bound inquiry. Two channels (theory and evidence) consult under enforced vocabulary separation; a synthesizer integrates their outputs. The output enters note convergence. Safety properties: vocabulary firewall, channel independence, channel discipline, channel asymmetry, synthesis integrity, provenance recording.

- **[Note Convergence Protocol](note-convergence-protocol.md)** — *convergence*; iterative, terminates when the predicate holds. Drives notes to stability through review/revise cycles. Specializes the convergence protocol with `note` classifier, `citation` link type (note→note), and `comment.out-of-scope` as the off-ramp. OUT_OF_SCOPE findings do not block the predicate; they signal the maturation protocol that the lattice needs structural work.

### Claim derivation boundary

The [Claim Derivation Module](../modules/claim-derivation-module.md) sits between note convergence and claim convergence. It's a transformation, not a protocol — see [Modules](../modules/README.md).

- **[Claim Convergence Protocol](claim-convergence-protocol.md)** — *convergence*; iterative, terminates when the predicate holds. Drives claims to formal precision. Specializes the convergence protocol with `claim` classifier, `contract.<kind>` link types, `citation` (claim→claim), and structural validation. Includes the iterative algorithm and its correctness arguments.

### Foundation

- **[Convergence Protocol](convergence-protocol.md)** — the document-type-neutral foundation. Defines the convergence predicate (every active `comment.revise` has a matching active `resolution`), the three core link types (`review`, `comment`, `resolution`), and the safety/liveness properties any review/revise process must satisfy. No algorithm — algorithm is choreography.

### Meta

- **[Maturation Protocol](maturation-protocol.md)** — the meta-protocol that composes the pipeline. Manages stage transitions, executes lattice operations (extract, absorb, scope promotion), and reaches [quiescence](../glossary.md#q) — the absence of pending work — rather than convergence. Owns the cascade behavior on hard reset.

## Reading order

For someone new, reading bottom-up tracks the actual dependency:

1. **Modules first.** Read [Substrate Module](../modules/substrate-module.md) (the link graph every protocol uses) and [Agent Module](../modules/agent-module.md) (the identity layer extending it). Both are short and define vocabulary the protocols build on. See [Modules](../modules/README.md) for the overview.
2. **[Convergence Protocol](convergence-protocol.md)** — the shared foundation. Once this is clear, both convergence-shaped specializations are straightforward.
3. **[Note Convergence Protocol](note-convergence-protocol.md)** or **[Claim Convergence Protocol](claim-convergence-protocol.md)** — pick whichever scale matches your interest. They're independent specializations of the foundation.
4. **[Consultation Protocol](consultation-protocol.md)** — the production-shaped protocol upstream of note convergence. The [Claim Derivation Module](../modules/claim-derivation-module.md) is the transformation between note and claim convergence — read it alongside the convergence protocols it bridges.
5. **[Maturation Protocol](maturation-protocol.md)** — composition over the pipeline. Easier to read after the stage protocols are familiar.

For someone already familiar with the system's behavior, top-down works too: maturation explains the pipeline; stage protocols explain how each stage drives toward its predicate or contract; the convergence module factors out what the convergence-shaped protocols share.

## What the protocols don't specify

Protocols define correctness conditions on the link graph (or output artifact, for production-shaped protocols). They deliberately don't specify:

- **Coverage** — whether reviews have actually happened. The convergence predicate is trivially satisfied by zero reviews. Coverage is a choreography obligation.
- **Algorithm** (for the convergence module only) — how to drive the predicate true. The shared convergence module defines the predicate without prescribing how to make it hold; each specialization (note convergence, claim convergence) adds its own algorithm, and each production protocol describes its phases.
- **Termination** (for convergence-shaped protocols) — convergence is not guaranteed. New revise comments can be filed indefinitely; rejected findings can be re-filed. Termination depends on choreography decisions and the finiteness of correctness issues.
- **Idempotence** (for production-shaped protocols) — re-running on the same input produces a different output. LLM stochasticity in the channels (consultation) or in the per-claim passes (claim derivation) is real. Resume support exists; idempotence does not.
- **Ordering** — review order, comment-resolution order, scope assembly order, phase concurrency. Any ordering that satisfies the properties is valid.

These are choreography concerns. They live in the algorithm sections, runbooks, and operational guides — not in the protocol specifications.

## References

- C. Cachin, R. Guerraoui, L. Rodrigues. *Reliable and Secure Distributed Programming*. Springer, 2nd edition, 2011. The protocols here adopt Cachin's modular formalism (interface specifications with declared safety/liveness properties; modules built by composition; explicit upper/lower interfaces).
