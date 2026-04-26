# Discovery

Discovery is how new knowledge enters the lattice. A human poses a question. The [two-channel architecture](two-channel-architecture.md) decomposes it into independent investigations — one consulting established theory, one analyzing raw evidence — and synthesizes a structured note. The [note convergence protocol](protocols/note-convergence-protocol.md) drives that note to stability through review/revise cycles. The [maturation protocol](protocols/maturation-protocol.md) handles the lattice operations that discovery's findings trigger.

Three mechanisms, one stage. Channels generate. Convergence refines. Maturation reshapes.

## The campaign

A campaign binds a theory channel and an evidence channel to a target and a bridge vocabulary. The campaign is the unit of coordinated investigation — a sustained effort of inquiries against a specific pairing of sources. "Rediscover the atomic-heat regularity via Maxwell's dynamical theory." "Formalize the Xanadu hypertext protocol from Nelson's design intent and Gregory's implementation."

A campaign begins with a question — broad enough to be interesting, specific enough to be tractable. The question is the entry point. Everything that follows grows from it. One lattice may host multiple campaigns: the same theory against different evidence corpora, competing theories against the same evidence, or entirely new pairings. Each campaign produces notes into the shared lattice; notes from different campaigns can cite each other's foundations.

## Generating the initial note

The [two-channel architecture](two-channel-architecture.md) governs how the initial note is produced. An inquiry is decomposed into channel-appropriate sub-questions. Each channel consults its own corpus independently, separated by the vocabulary firewall. A synthesis agent integrates both channels' answers into a structured note with dependency-mapped claims. Where the channels agree, principles are validated. Where they disagree, new hypotheses emerge.

The synthesized note is written in the Dijkstra voice from its first draft — the [Voice Principle](principles/voice.md) in its original form. Prose with embedded formalism, every statement justified where introduced. The voice was the discipline before the discipline had a name.

## Converging the note

The [note convergence protocol](protocols/note-convergence-protocol.md) drives the synthesized note toward stability. The reviewer reads as Dijkstra — with respect for the effort and no tolerance for hand-waving. Each derivation must walk its cases. Each postulate must be honestly labeled. Each regime condition must be stated where it is load-bearing.

Findings are classified as `comment.revise` or `comment.out-of-scope`:

- **`comment.revise`** — the note's reasoning is wrong, incomplete, or ungrounded. Must be resolved — by edit or by rejection.
- **`comment.out-of-scope`** — the finding is valid but belongs elsewhere. Does not block convergence. Signals the maturation protocol that the lattice needs structural work.

The convergence predicate — every `comment.revise` has a `resolution` — determines when the note has stabilized. Combined with the choreography's observation of sustained quiet (diminishing returns across cycles), convergence signals readiness for [note decomposition](note-decomposition.md).

## Growing the lattice

![Growing the lattice](diagrams/growing-the-lattice.svg)

The first note from a campaign is usually too broad. That's expected. Agents identify natural boundaries — clusters of claims that reason about the same concept independently of other clusters — and split into focused notes, each covering one topic. Discovery runs on each independently.

As discovery proceeds on separate notes, patterns emerge. Two notes independently derive the same claim — both need the same comparison operation, both define the same foundational concept. This duplication signal is itself a discovery. Two independently drafted notes converging on the same commitments means those commitments have an independent existence that neither note should own.

Three lattice operations — executed by the [maturation protocol](protocols/maturation-protocol.md) — reshape the lattice during discovery:

**Extract** — shared concepts move into a new foundation note below both consumers. The extracted foundation contains exactly the commitments both needed and nothing else.

**Absorb** — claims that belong in another note move to their natural home. The source note's scope contracts.

**Scope promotion** — `comment.out-of-scope` findings become candidates for new inquiries. The system discovers the questions it should be asking, not just answers to questions posed.

The lattice grows through this process. Foundation notes emerge at the bottom — discovered by noticing what keeps being re-derived. The lattice deepens as shared concepts are extracted. New domain vocabulary emerges because the mathematics requires it, not prescribed in advance.

## Entering note decomposition

A note is ready to enter note decomposition when:

**The convergence predicate holds and sustained quiet is observed.** Review/revise cycles produce diminishing returns — few or no substantive findings, zero new vocabulary coinages, new cycles producing wordsmithing rather than reasoning. The reasoning has stabilized.

**No other note in discovery owns claims that belong here.** Before entering note decomposition, scan the other notes still in discovery. If any independently derived claims that naturally belong in this note, absorb them first.

Waiting for foundation dependencies to converge their claims before note decomposition reduces rework — but the [maturation protocol](protocols/maturation-protocol.md) does not enforce this as a gate. A note can enter note decomposition against non-converged foundations. The protocol handles the rework through its normal feedback path.

The note is frozen at handoff — it becomes the record of discovery, not a living document.

## Related

- [Two-Channel Architecture](two-channel-architecture.md) — how the initial note is generated through independent channel consultation and synthesis.
- [Consultation Protocol](protocols/consultation-protocol.md) — the formal protocol governing channel consultation and synthesis.
- [Note Convergence Protocol](protocols/note-convergence-protocol.md) — the protocol governing review/revise cycles on notes.
- [Maturation Protocol](protocols/maturation-protocol.md) — the meta-protocol that handles lattice operations and transition conditions.
- [Note Decomposition](note-decomposition.md) — the next stage: decomposing the note into per-claim files.
- [The Voice Principle](principles/voice.md) — the Dijkstra voice present from discovery's first prompt.
- [Scope Promotion](patterns/scope-promotion.md) — how out-of-scope findings become new inquiries.
- [Extract/Absorb](patterns/extract-absorb.md) — lattice operations that reshape the lattice during discovery.