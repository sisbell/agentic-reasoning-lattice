# Agentic Protocols

The system is a stack of protocols sharing a [substrate](../glossary.md#s) (a persistent, append-only graph of documents and typed links). Following the modular formalism of Cachin (*Reliable and Secure Distributed Programming*) — but for LLM-agent coordination rather than distributed nodes.

A protocol defines what must hold (the convergence predicate, the link vocabulary, the safety and liveness properties). [Choreography](../glossary.md#c) defines how to make it hold (scope strategy, review order, context assembly). The protocol IS the predicate; everything else is choreography.

## The stack

```
                    ┌─────────────────────────┐
                    │   Maturation Protocol   │   meta-protocol
                    │  (transitions + lattice │   transitions + lattice ops
                    │       operations)       │   reaches quiescence
                    └────────────┬────────────┘
                                 │ activates
                ┌────────────────┴───────────────────┐
                │                                    │
   ┌────────────▼──────────┐     ┌──────────────────▼─────────────┐
   │  Note Convergence     │     │   Claim Convergence            │   stage protocols
   │  (notes, discovery)   │     │   (claims, post-blueprinting)  │   review/revise
   │  REVISE / OUT_OF_SCOPE│     │   REVISE / OBSERVE             │   on different scales
   └────────────┬──────────┘     └──────────────────┬─────────────┘
                │                                    │
                │ both specialize                    │
                │                                    │
                │           ┌────────────────────────┘
                │           │
              ┌─▼───────────▼─┐
              │   Convergence │   shared module
              │     Protocol  │   predicate + comment/resolution link types
              │   (foundation)│   safety/liveness properties (S1-S6, L1-L4)
              └───────────────┘
                       ▲
                       │ relies on
                       │
              ┌────────┴──────┐
              │   Substrate   │   permanence (SUB1)
              │  (link graph) │   query soundness (SUB2)
              └───────────────┘   count consistency (SUB3)
```

The layering enforces what is actually shared vs. what is scale-specific. Both convergence protocols use the same predicate, the same comment/resolution machinery, the same safety guarantees — written once in the convergence module. Each adds the structure its scale needs: note convergence adds OUT_OF_SCOPE routing for lattice signals; claim convergence adds structural validation, the algorithm, and correctness arguments.

## The protocols

- **[Convergence Protocol](convergence-protocol.md)** — the document-type-neutral foundation. Defines the convergence predicate (every `comment.revise` has a matching `resolution`), the three link types (`review`, `comment`, `resolution`), and the safety/liveness properties any review/revise process must satisfy. No algorithm — algorithm is choreography.

- **[Note Convergence Protocol](note-convergence-protocol.md)** — drives notes to stability during discovery. Specializes the convergence protocol with `note` classifier, `citation` link type (note→note), and `comment.out-of-scope` as the off-ramp. OUT_OF_SCOPE findings do not block the predicate; they signal the maturation protocol that the lattice needs structural work.

- **[Claim Convergence Protocol](claim-convergence-protocol.md)** — drives claims to formal precision after blueprinting. Specializes the convergence protocol with `claim` classifier, `contract.<kind>` link types, `citation` (claim→claim), and structural validation. Includes the iterative algorithm and its correctness arguments.

- **[Maturation Protocol](maturation-protocol.md)** — the meta-protocol that supervises stage protocols and executes lattice operations (extract, absorb, scope promotion). Reaches [quiescence](../glossary.md#q) — the absence of pending work — rather than convergence. Owns transitions between stages and the cascade behavior on hard reset.

## Reading order

For someone new to the protocols, reading bottom-up tracks the actual dependency:

1. [Convergence Protocol](convergence-protocol.md) — the shared foundation. Once this is clear, both specializations are straightforward.
2. [Note Convergence Protocol](note-convergence-protocol.md) or [Claim Convergence Protocol](claim-convergence-protocol.md) — pick whichever scale matches your interest. They're independent.
3. [Maturation Protocol](maturation-protocol.md) — composition over the stage protocols. Easier to read after the stage protocols are familiar.

For someone already familiar with the system's behavior, top-down works too: maturation explains the pipeline; stage protocols explain how each stage drives toward its predicate; the convergence module factors out what they share.

## What the protocols don't specify

Protocols define correctness conditions on the link graph. They deliberately don't specify:

- **Coverage** — whether reviews have actually happened. The predicate is trivially satisfied by zero reviews. Coverage is a choreography obligation.
- **Algorithm** (in convergence and note convergence) — how to drive the predicate true. The convergence module defines the predicate without prescribing how to make it hold.
- **Termination** — convergence is not guaranteed. New revise comments can be filed indefinitely; rejected findings can be re-filed. Termination depends on choreography decisions and the finiteness of correctness issues.
- **Ordering** — review order, comment-resolution order, scope assembly order. Any ordering that satisfies the properties is valid.

These are choreography concerns. They live in the algorithm sections (where present), runbooks, and operational guides — not in the protocol specifications.

## References

- C. Cachin, R. Guerraoui, L. Rodrigues. *Reliable and Secure Distributed Programming*. Springer, 2nd edition, 2011. The protocols here adopt Cachin's modular formalism (interface specifications with declared safety/liveness properties; modules built by composition; explicit upper/lower interfaces).
