# Agentic Modules

Modules provide the substrate-level services and transformations that protocols compose with. Each module follows the modular formalism of Cachin (*Reliable and Secure Distributed Programming*) — declared events, declared properties, declared composition — but specifies *transformation* rather than ongoing interaction.

## Module vs. protocol

The two shapes differ in what their core specifies, not in formalism:

- A **protocol** governs ongoing interaction between participants. Its core specification is either a predicate over that interaction (the convergence-shaped protocols) or a coordination structure between participants (consultation). Termination is interaction-driven.
- A **module** is a transformation or service. Its core specification is a precondition, a transformation, and a postcondition. Participants run in sequence; they don't interact. Termination is structural.

Both share the Cachin specification surface (events, properties, composition); they differ in whether the underlying shape is interaction or transformation. See the [Protocols overview](../protocols/README.md) for the protocol-shaped specifications.

## The modules

- **[Substrate Module](substrate-module.md)** — persistent, append-only link graph. Every protocol reads from and writes to the substrate. Defines the substrate's operations (MakeLink, FindLinks, FindNumLinks, Retract, ActiveLinks) and properties (SUB1 permanence, SUB2 query soundness, SUB3 count consistency, SUB4–SUB5 retraction nullify-and-shadow, SUB6 retraction idempotence). Defines `retraction` as the only substrate-level link type; all other link types are protocol-defined.

- **[Agent Module](agent-module.md)** — agent identity layer above the substrate. Defines `agent` (classifies a doc as an agent — its address is the agent's identity) and `manages` (declares an agent is currently responsible for an operation). Lets convergence protocols and other modules attribute their work to specific agents (cone-review, full-review, etc.) without protocol identity leaking into the substrate's type system. Properties A1–A6, LA1–LA2.

- **[Claim Derivation Module](claim-derivation-module.md)** — transforms a converged note into per-claim files conforming to the [Claim Document Contract](../design-notes/claim-document-contract.md). Sits between [note convergence](../protocols/note-convergence-protocol.md) and [claim convergence](../protocols/claim-convergence-protocol.md) — a representation change, one note → many claim files. One-shot; terminates when the structural contract holds.

## When something is a module vs. a protocol

If the unit's specification is "given this input, produce this output with these properties" — it's a module. The participants are sequential stages; they don't interact.

If the unit's specification is "participants interact under these rules and termination requires this predicate / coordination structure" — it's a protocol.

The codebase's directory layout reflects this: `docs/modules/` holds the transformation/service specifications, `docs/protocols/` holds the interaction specifications. Both directories follow the same Cachin-style format.

## References

- C. Cachin, R. Guerraoui, L. Rodrigues. *Reliable and Secure Distributed Programming*. Springer, 2nd edition, 2011. The modules here adopt Cachin's modular formalism (interface specifications with declared safety/liveness properties; modules built by composition; explicit upper/lower interfaces).
