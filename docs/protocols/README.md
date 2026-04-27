# Agentic Protocols

The system is a stack of protocols sharing a [substrate](../glossary.md#s) (a persistent, append-only graph of documents and typed links). Following the modular formalism of Cachin (*Reliable and Secure Distributed Programming*) — but for LLM-agent coordination rather than distributed nodes.

A protocol defines what must hold (the convergence predicate, the output contract, the safety and liveness properties). [Choreography](../glossary.md#c) defines how to make it hold (scope strategy, review order, context assembly, concurrency policy). The protocol IS the predicate or contract; everything else is choreography.

## Two protocol shapes

Protocols in this system come in two shapes:

- **Convergence-shaped** — iterative; terminates when a graph predicate holds. Note Convergence, Claim Convergence. Safety/liveness include indication soundness for the predicate.
- **Production-shaped** — one-shot; terminates on output production. Consultation, Note Decomposition. Safety properties are output contracts plus invariants on the running execution.

Both are full Cachin protocols — declared participants, declared events, declared safety/liveness. The shape is a property of how each is driven, not a separate category. The names already carry the distinction: a reader sees "Convergence" and knows it iterates; a reader sees "Consultation" or "Decomposition" and knows it produces.

## The pipeline

Content matures through four stages, each with its own protocol or protocols:

```
─── discovery stage ──────────                ─── note decomposition → claim convergence ─        ── verification ──
 Consultation ──→ Note Convergence  ──→  Note Decomposition ──→ Claim Convergence      ──→  (Verification, TBD)
 (production)     (convergence)          (production)            (convergence)
                                                                                                                
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

The layering enforces what is actually shared vs. what is scale-specific. Both convergence protocols use the same predicate, comment/resolution machinery, and safety guarantees — written once in the convergence module. Each specialization adds what its scale needs: note convergence adds OUT_OF_SCOPE routing for lattice signals; claim convergence adds structural validation, the algorithm, and correctness arguments. The production protocols sit upstream of (consultation) or between (note decomposition) the convergence protocols — they don't specialize the convergence module because they don't have a predicate.

## The protocols

Listed by pipeline position. The shape of each is one-line:

### Discovery stage

- **[Consultation Protocol](consultation-protocol.md)** — *production*; one-shot, terminates on output production. Produces an initial note from a campaign-bound inquiry. Two channels (theory and evidence) consult under enforced vocabulary separation; a synthesizer integrates their outputs. The output enters note convergence. Safety properties: vocabulary firewall, channel independence, channel discipline, channel asymmetry, synthesis integrity, provenance recording.

- **[Note Convergence Protocol](note-convergence-protocol.md)** — *convergence*; iterative, terminates when the predicate holds. Drives notes to stability through review/revise cycles. Specializes the convergence protocol with `note` classifier, `citation` link type (note→note), and `comment.out-of-scope` as the off-ramp. OUT_OF_SCOPE findings do not block the predicate; they signal the maturation protocol that the lattice needs structural work.

### Note decomposition → claim convergence

- **[Note Decomposition Protocol](note-decomposition-protocol.md)** — *production*; one-shot, terminates when the structural contract holds. Decomposes a converged note into per-claim file pairs (YAML metadata + Markdown body) conforming to the [Claim File Contract](../design-notes/claim-file-contract.md). Safety properties: source coverage, no fabrication, content preservation, source freezing, structural contract, acyclicity, provenance recording. Stage transition (changes representation: one note → many claim files), not a producer-consumer pair. The output enters claim convergence.

- **[Claim Convergence Protocol](claim-convergence-protocol.md)** — *convergence*; iterative, terminates when the predicate holds. Drives claims to formal precision. Specializes the convergence protocol with `claim` classifier, `contract.<kind>` link types, `citation` (claim→claim), and structural validation. Includes the iterative algorithm and its correctness arguments.

### Foundation

- **[Substrate Module](substrate.md)** — the persistent, append-only link graph every protocol reads from and writes to. Defines the substrate's operations (MakeLink, FindLinks, FindNumLinks, Retract, ActiveLinks) and properties (SUB1 permanence, SUB2 query soundness, SUB3 count consistency, SUB4–SUB5 retraction nullify-and-shadow, SUB6 retraction idempotence). Defines `retraction` as the only substrate-level link type; all other link types are protocol-defined.
- **[Agent Module](agent.md)** — the agent identity layer above the substrate. Defines `agent` (classifies a doc as an agent — its address is the agent's identity) and `manages` (declares an agent is currently responsible for an operation). Lets convergence protocols and other modules attribute their work to specific agents (cone-review, full-review, etc.) without protocol identity leaking into the substrate's type system. Cites T9 from the [tumbler algebra](../../lattices/xanadu/claim-convergence/ASN-0034/) for per-asserter ordering. Properties A1–A6, LA1–LA2.
- **[Convergence Protocol](convergence-protocol.md)** — the document-type-neutral foundation. Defines the convergence predicate (every active `comment.revise` has a matching active `resolution`), the three core link types (`review`, `comment`, `resolution`), and the safety/liveness properties any review/revise process must satisfy. No algorithm — algorithm is choreography.

### Meta

- **[Maturation Protocol](maturation-protocol.md)** — the meta-protocol that composes the pipeline. Manages stage transitions, executes lattice operations (extract, absorb, scope promotion), and reaches [quiescence](../glossary.md#q) — the absence of pending work — rather than convergence. Owns the cascade behavior on hard reset.

## Reading order

For someone new to the protocols, reading bottom-up tracks the actual dependency:

1. **[Substrate Module](substrate.md)** — the link graph every protocol uses. The vocabulary (links, retraction, active queries) is defined here.
2. **[Agent Module](agent.md)** — the identity layer extending the substrate for the agent paradigm. Short module; introduces `agent` and `manages` and the per-asserter ordering rule cited via T9.
3. **[Convergence Protocol](convergence-protocol.md)** — the shared foundation. Once this is clear, both convergence-shaped specializations are straightforward.
4. **[Note Convergence Protocol](note-convergence-protocol.md)** or **[Claim Convergence Protocol](claim-convergence-protocol.md)** — pick whichever scale matches your interest. They're independent specializations of the foundation.
5. **[Consultation Protocol](consultation-protocol.md)** and **[Note Decomposition Protocol](note-decomposition-protocol.md)** — the production-shaped protocols. Easier to read after you know what convergence looks like, since these produce input for it.
6. **[Maturation Protocol](maturation-protocol.md)** — composition over the pipeline. Easier to read after the stage protocols are familiar.

For someone already familiar with the system's behavior, top-down works too: maturation explains the pipeline; stage protocols explain how each stage drives toward its predicate or contract; the convergence module factors out what the convergence-shaped protocols share.

## What the protocols don't specify

Protocols define correctness conditions on the link graph (or output artifact, for production-shaped protocols). They deliberately don't specify:

- **Coverage** — whether reviews have actually happened. The convergence predicate is trivially satisfied by zero reviews. Coverage is a choreography obligation.
- **Algorithm** (for the convergence module only) — how to drive the predicate true. The shared convergence module defines the predicate without prescribing how to make it hold; each specialization (note convergence, claim convergence) adds its own algorithm, and each production protocol describes its phases.
- **Termination** (for convergence-shaped protocols) — convergence is not guaranteed. New revise comments can be filed indefinitely; rejected findings can be re-filed. Termination depends on choreography decisions and the finiteness of correctness issues.
- **Idempotence** (for production-shaped protocols) — re-running on the same input produces a different output. LLM stochasticity in the channels (consultation) or in the per-claim passes (note decomposition) is real. Resume support exists; idempotence does not.
- **Ordering** — review order, comment-resolution order, scope assembly order, phase concurrency. Any ordering that satisfies the properties is valid.

These are choreography concerns. They live in the algorithm sections, runbooks, and operational guides — not in the protocol specifications.

## References

- C. Cachin, R. Guerraoui, L. Rodrigues. *Reliable and Secure Distributed Programming*. Springer, 2nd edition, 2011. The protocols here adopt Cachin's modular formalism (interface specifications with declared safety/liveness properties; modules built by composition; explicit upper/lower interfaces).
