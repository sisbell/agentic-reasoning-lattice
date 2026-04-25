# Maturation Protocol

*The meta-protocol that drives content from question to verified knowledge through the lattice.*

## Overview

The maturation protocol supervises four stage protocols connected by transition conditions. Each stage protocol drives one representation toward completion. The maturation protocol monitors readiness signals and triggers transitions between stages. It is a meta-protocol — different in kind from the stage protocols it supervises. The stage protocols have agents doing review/revise work. The maturation protocol has transition conditions connecting them.

Multiple notes can be in different stages simultaneously. One foundation note in verification, a second note in claim convergence, a third still in discovery. The ordering constraint is dependency — foundations must mature before dependents — not a global sequence. The maturation protocol manages the lattice, not a pipeline.

## The representations

Content matures through four representations, each progressively more precise:

| Representation | Form | Produced by |
|---|---|---|
| **Note** | Narrative prose with embedded claims | Discovery protocol |
| **Claim files** | Per-claim YAML metadata + markdown body | Blueprinting protocol |
| **Converged contracts** | Formally precise claims where every revise comment has a resolution | [Claim convergence protocol](claim-convergence-protocol.md) |
| **Verified code** | Mechanically checked assertions | Verification protocol |

Each transition is a [representation change](../patterns/representation-change.md). The content doesn't change. The form makes it progressively more checkable.

## The stage protocols

Four stage protocols execute within the maturation protocol. Each has defined participants, exchange format, and convergence criterion:

**Discovery protocol.** A campaign binds a theory channel and an evidence channel to a target. The inquiry is decomposed into channel-appropriate sub-questions. Each channel consults its corpus independently. A synthesis agent integrates both channels into a note. Review/revise cycles deepen the note's reasoning. Operates at note scale — one document, broad context, generative prose as the substrate.

**Blueprinting protocol.** Progressive decomposition of a note into per-claim file pairs — mechanical section split, per-section claim identification, per-claim classification and dependency extraction. Post-decomposition validation checks the output against the [Claim File Contract](../design-notes/claim-file-contract.md).

**[Claim convergence protocol](claim-convergence-protocol.md).** The convergence predicate — every `comment.revise` has a matching `resolution` — drives claims toward formal precision. Finding classification (REVISE/OBSERVE) prevents tightening observations from triggering action. Scope strategies (adaptive, comprehensive) are choreography decisions within the protocol, not protocol-level constructs. Operates at claim scale — per-claim files, narrow focus, precision as the objective.

**Verification protocol.** Converged contracts are translated into mechanically verifiable code — Dafny for logical consistency, Alloy for bounded model checking, experimental replication for science domains. Failures route back to the appropriate upstream protocol with the verification failure as a finding.

The [validate-before-review](../patterns/validate-before-review.md) pattern is instantiated by any protocol that runs LLM review on structured content. Claim convergence instantiates it before each review at either scope. Blueprinting instantiates it as post-decomposition validation. It is a reusable pattern, not a sub-protocol of any single stage.

## Transition conditions and artifacts

Each transition has a readiness signal and a handoff artifact — what is evaluated, and what is passed to the next stage:

### Discovery → blueprinting

**Readiness signal.** The note's review/revise cycles produce diminishing returns. Concrete indicators: zero new vocabulary coinages across the last N cycles, few or no substantive findings, new cycles producing wordsmithing rather than reasoning. Additionally: the note must be a foundation in the lattice (dependencies must have transitioned first), and no other note in discovery owns claims that belong here.

**Handoff artifact.** The note file (markdown), plus the note's vocabulary (terms coined during discovery), plus its declared note-level dependencies (`depends: [ASN-NNNN]`). The note is frozen at handoff — it becomes the record of discovery, not a living document.

### Blueprinting → claim convergence

**Readiness signal.** The post-blueprinting validator returns zero violations against the [Claim File Contract](../design-notes/claim-file-contract.md). Structural form is valid — one body per file, references resolve, metadata agrees, no dependency cycles.

**Handoff artifact.** The claim file set: per-claim `.md` + `.yaml` pairs, plus the campaign's bridge vocabulary, plus foundation statements from upstream ASNs. Semantic content may be imprecise; structural form must be valid.

### Claim convergence → verification

**Readiness signal.** The convergence predicate holds — every `comment.revise` on every claim has a matching `resolution` — and the choreography's coverage obligation is met (reviews have actually been conducted at sufficient scope).

**Handoff artifact.** Converged claim files with formally precise contracts — preconditions, postconditions, invariants, frame conditions, axioms, definitions. Each contract preserves the exact conditions from the claim's narrative.

### Verification → done (or back)

**Readiness signal.** Mechanical verification passes — Dafny/Alloy/replication produces no failures.

**Handoff artifact (on failure).** The verification failure, traced back through the dependency chain to the specific claim and contract that diverged. That claim re-enters claim convergence (or discovery, if the failure reveals a fundamental reasoning gap) with the failure as a finding.

## Lattice operations

Two operations reshape the lattice during maturation without being stage transitions:

**Extract.** Two notes independently derive the same concept. The shared concept is extracted into a new foundation note that both depend on. This is the meet operation — the extracted foundation is the greatest common element below both consumers. The new foundation enters discovery as a new note. The consuming notes' dependencies update to reference it.

**Absorb.** A note in discovery contains claims that naturally belong in another note. The claims are absorbed into the receiving note. The source note's scope contracts.

Both operations can trigger re-entry into discovery for affected notes. They are lattice-level operations within the maturation protocol — they restructure what's being matured, not how maturation proceeds. Extract is how foundation layers are discovered. Absorb is how notes find their natural boundaries.

## Dependency ordering

The maturation protocol's ordering constraint is dependency, not stage. A note can only transition when its upstream dependencies have matured past the same point:

- A note cannot blueprint if it depends on a note that hasn't blueprinted and converged
- A claim cannot converge if its foundation claims haven't converged
- A claim cannot verify if its cited dependencies haven't verified

The lattice matures bottom-up. Foundations transition first. Dependents follow. The protocol doesn't enforce this through a global schedule — it follows from the transition conditions themselves. A note whose dependencies haven't matured won't meet its transition condition because its review cycles will keep finding issues traceable to immature foundations.

## Feedback paths

Maturation is not strictly forward. Three feedback paths route content backward:

**Verification failure.** A contract is inconsistent. The claim re-enters claim convergence with the failure as a finding. If the failure reveals a fundamental gap, the claim routes back to discovery.

**Claim convergence discovery.** Claim convergence surfaces findings that discovery missed — missing axioms, false claims, ungrounded operators. These are reasoning contributions produced by per-claim scrutiny. Resolved within claim convergence — convergence is itself discovery under a precision constraint.

**Foundation change.** When a foundation claim changes, dependent notes carry stale citations. Their review cycles detect the staleness through findings traceable to the changed foundation. The protocol doesn't push changes downstream — the transition conditions detect staleness naturally.

## Participants

**Agents.** Each stage protocol has its own agents — channels, synthesizers, reviewers, revisers, validators, scope assemblers, translators, verifiers. The agents within a stage protocol are defined by that protocol. The maturation protocol doesn't have agents of its own — it has transition conditions that the stage protocols' outputs satisfy or don't.

**Human.** The human participates in the maturation protocol at defined exchange points:

- **Pose the initial question.** The question that starts a campaign.
- **Create campaigns.** Choose the channel pairing, curate the bridge vocabulary, set the target. Campaigns are parameters of the maturation protocol — they exist before any stage protocol runs.
- **Set transition thresholds.** How many diminishing-return cycles before blueprinting? How strict is the claim file contract? These are policy decisions.
- **Intervene on transition misfires.** If a transition condition fires prematurely or fails to fire when it should, the human overrides. This is the fallback for transition conditions that don't yet capture what readiness actually means for this domain.
- **Evaluate final output.** Are the verified claims the right claims? Do they answer the question? Are the open questions worth pursuing as new campaigns?

The human's role shifts as transition conditions improve. Early in a domain's life, the human intervenes frequently — transition conditions are uncalibrated. Later, the human monitors and evaluates. The protocol runs. The human judges.

## The supervision question

The maturation protocol currently has no explicit supervisor agent. The human triggers transitions by running scripts. The transition conditions are evaluated by the human reading the stage protocol's output.

Two future architectures are possible:

**Explicit supervisor.** An agent watches the lattice, evaluates transition conditions, and triggers stage protocols. Centralized orchestration.

**Emergent transitions.** Each stage protocol publishes a readiness signal on completion. The next stage protocol subscribes and starts when the signal arrives. Decentralized.

The choice depends on how reliable the transition conditions become. Unreliable conditions need centralized judgment (a supervisor that can reason about edge cases). Reliable conditions can be decentralized (a signal is a signal). The current state — human as supervisor — is the starting point. The protocol design doesn't depend on the choice; the transition conditions and handoff artifacts are the same either way.

## What this replaces

The original architecture described a fixed pipeline — discovery → blueprinting → formalization → verification — with a human deciding when each stage runs.

The maturation protocol subsumes that design. The pipeline becomes stage protocols connected by transition conditions. "Formalization" becomes the claim convergence protocol. Human orchestration becomes agent-evaluable transition conditions (eventually). The lattice is the substrate that tracks where everything is and what's ready to transition.

The representations are the same. The ordering constraint is the same. What changes is the framing — from a pipeline run by a human to a protocol that monitors readiness and routes content through whatever transition applies.

## Related

- [Claim Convergence Protocol](claim-convergence-protocol.md) — the stage protocol that drives claims to formal precision.
- [Architecture](../architecture.md) — the six-level hierarchy and lattice structure the maturation protocol operates on.
- [Representation Change](../patterns/representation-change.md) — each transition is a representation change.
- [Validate Before Review](../patterns/validate-before-review.md) — a reusable pattern instantiated by multiple stage protocols.
- [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md) — the failure mode when a transition lacks an output contract.
- [Claim File Contract](../design-notes/claim-file-contract.md) — the output contract for the blueprinting → claim convergence transition.
- [Extract/Absorb](../patterns/extract-absorb.md) — lattice operations within the maturation protocol.
- [Scope Promotion](../patterns/scope-promotion.md) — how discovery generates new inquiries within a campaign.
- [The Validation Principle](../principles/validation.md), [The Coupling Principle](../principles/coupling.md), [The Voice Principle](../principles/voice.md) — the quality boundary for all stage protocols.