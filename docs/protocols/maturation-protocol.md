# Maturation Protocol

*The meta-protocol that drives content from question to verified knowledge through the lattice.*

## Overview

The maturation protocol supervises stage protocols connected by transition conditions. Each stage protocol drives one representation toward completion. The maturation protocol monitors readiness signals, triggers transitions between stages, and executes lattice operations that reshape the structure the stage protocols operate on.

It is a meta-protocol — different in kind from the stage protocols it supervises. The stage protocols have agents doing review/revise work with convergence predicates. The maturation protocol has transition conditions connecting them and lattice operations reshaping them.

Multiple notes can be in different stages simultaneously. One foundation note in verification, a second note in claim convergence, a third still in discovery. Foundations maturing before dependents reduces rework, but the protocol does not enforce this ordering as a hard gate — it handles the rework when it occurs. The maturation protocol manages the lattice, not a pipeline.

## The representations

Content matures through four representations, each progressively more precise:

| Representation | Form | Produced by |
|---|---|---|
| **Note** | Narrative prose with embedded claims | [Consultation](consultation-protocol.md) + [note convergence](note-convergence-protocol.md) |
| **Claim files** | Per-claim YAML metadata + markdown body | [Claim derivation protocol](claim-derivation-protocol.md) |
| **Converged contracts** | Formally precise claims where every revise comment has a resolution | [Claim convergence protocol](claim-convergence-protocol.md) |
| **Verified code** | Mechanically checked assertions | Verification protocol |

Each transition is a [representation change](../patterns/representation-change.md). The content doesn't change. The form makes it progressively more checkable.

## The stage protocols

Five protocols execute within the maturation protocol. Each has a defined completion criterion:

**[Consultation protocol](consultation-protocol.md).** Produces the initial note from a campaign-bound inquiry. Two independent channels (theory and evidence) are consulted under enforced vocabulary separation; their outputs are synthesized into a structured note. One-shot — terminates on output production. The consultation protocol is the upstream producer for note convergence; together they constitute the discovery stage.

**[Note convergence protocol](note-convergence-protocol.md).** Drives notes toward stability through review/revise cycles. Finding classification is REVISE / OUT_OF_SCOPE. The convergence predicate — every active `comment.revise` has an active `resolution` — determines when a note is ready for decomposition. OUT_OF_SCOPE findings generate signals that maturation consumes for lattice operations. Operates at note scale.

**[Claim derivation protocol](claim-derivation-protocol.md).** Decomposes a converged note into per-claim file pairs — mechanical section split, per-section claim identification, per-claim classification and dependency extraction. Post-decomposition validation checks the output against the [Claim File Contract](../design-notes/claim-file-contract.md). One-shot — terminates when the structural contract holds on the output.

**[Claim convergence protocol](claim-convergence-protocol.md).** The convergence predicate — every active `comment.revise` has a matching active `resolution` — drives claims toward formal precision. Finding classification is REVISE / OBSERVE. Scope strategies (adaptive, comprehensive) are choreography decisions within the protocol. Operates at claim scale.

**Verification protocol.** Converged contracts are translated into mechanically verifiable code — Dafny for logical consistency, Alloy for bounded model checking, experimental replication for science domains. Failures route back to the appropriate upstream protocol with the verification failure as a finding.

The [validate-before-review](../patterns/validate-before-review.md) pattern is instantiated by any protocol that runs LLM review on structured content. Claim convergence instantiates it before each review. Claim derivation instantiates it as post-decomposition validation. It is a reusable pattern, not a sub-protocol of any single stage.

Both convergence protocols specialize the [convergence protocol](convergence-protocol.md) — the document-type-neutral module that provides the predicate, comment/resolution link types, and safety/liveness properties. The two one-shot protocols (consultation and claim derivation) share the production shape — terminate on output, no convergence predicate — but do not share a formal module.

## Transition conditions and artifacts

```
Module: Maturation
  Uses: Consultation, NoteConvergence, NoteDecomposition, ClaimConvergence, Verification

  Consultation → NoteConvergence
    Precondition: ⟨ NoteProduced ⟩ indicated
    Artifact: synthesized note with dependency-mapped claims

  NoteConvergence → NoteDecomposition
    Precondition: ⟨ Converged | note ⟩ indicated, sustained quiet observed
    Artifact: frozen note (markdown + vocabulary + note-level dependencies)

  NoteDecomposition → ClaimConvergence
    Precondition: ⟨ ClaimSetProduced ⟩ indicated, Claim File Contract holds
    Artifact: per-claim file set with claim/contract/citation/decomposition links

  ClaimConvergence → Verification
    Precondition: ⟨ Converged ⟩ indicated, coverage met
    Artifact: claim files with formally precise contracts

  Verification → Done | HardReset
    Precondition: mechanical verification passes (or fails)
    Artifact (on failure): verification failure traced to specific claim
```

Each transition has a readiness signal and a handoff artifact — what is evaluated, and what is passed to the next stage. Detail below:

### Discovery → claim derivation

**Readiness signal.** The note convergence predicate holds — every active `comment.revise` on the note has an active `resolution` — and the choreography observes sustained quiet: few or no substantive findings across the last N cycles, zero new vocabulary coinages, new cycles producing wordsmithing rather than reasoning. Additionally: no other note in discovery owns claims that naturally belong here.

Waiting for foundation dependencies to converge their claims before decomposition reduces rework — foundation contracts will be stable and downstream citations won't need re-verification. But the protocol does not enforce this as a gate. A note can enter decomposition against non-converged foundations. When those foundations later converge and their contracts tighten, the dependent's review cycles will find issues traceable to the changes. The protocol handles the rework through its normal feedback path — new `comment.revise` links filed, predicate goes false, convergence resumes.

**Handoff artifact.** The note file (markdown), plus the note's vocabulary (terms coined during discovery), plus its declared note-level dependencies (`depends: [ASN-NNNN]`). The note is frozen at handoff — it becomes the record of discovery, not a living document.

### Claim derivation → claim convergence

**Readiness signal.** The post-decomposition validator returns zero violations against the [Claim File Contract](../design-notes/claim-file-contract.md). This is a structural validation result, not a convergence predicate in the graph-property sense — decomposition's completion criterion is mechanical checking, not resolved comments. Structural form is valid — one body per file, references resolve, metadata agrees, no dependency cycles.

**Handoff artifact.** The claim file set: per-claim `.md` + `.yaml` pairs, plus the campaign's bridge vocabulary, plus foundation statements from upstream ASNs. Semantic content may be imprecise; structural form must be valid.

### Claim convergence → verification

**Readiness signal.** The convergence predicate holds — every active `comment.revise` on every claim has a matching active `resolution` — and the choreography's coverage obligation is met (reviews have actually been conducted at sufficient scope).

**Handoff artifact.** Converged claim files with formally precise contracts — preconditions, postconditions, invariants, frame conditions, axioms, definitions. Each contract preserves the exact conditions from the claim's narrative. The specific input format for verification (which files, what structure, how contracts map to verifier input) is not yet fully specified — this is a known gap that will be resolved when the verification protocol is formalized.

### Verification → done (or back)

**Readiness signal.** Mechanical verification passes — Dafny/Alloy/replication produces no failures.

**Handoff artifact (on failure).** The verification failure, traced back through the dependency chain to the specific claim and contract that diverged. That claim re-enters claim convergence (or discovery, if the failure reveals a fundamental reasoning gap) with the failure as a finding.

## Lattice operations

Three operations reshape the lattice during maturation. They are not stage transitions — they are structural changes to the lattice itself. The stage protocols generate signals. Maturation acts on them.

### Extract — claims move down

Two notes converge with derivations that independently establish the same concept. The shared concept is extracted into a new foundation note. Both consuming notes gain `citation` links to the new foundation; their bodies shrink to reference rather than re-derive. The new foundation enters note convergence.

**Worked example.** Notes A and B both contain a definition of the same primitive operation, derived independently from different starting points. Maturation observes the duplication via cross-note review and extracts the definition into foundation note F. A and B add `citation` links to F. F enters note convergence as a fresh note. A and B re-enter note convergence with their scope contracted.

**Signal:** structural duplication detected across notes.

### Absorb — claims move toward natural home

Note A contains material that more naturally belongs in existing note B. The material is moved to B. A's content shrinks; B re-enters note convergence with absorbed material.

**Worked example.** During note convergence on note A, a reviewer files `comment.out-of-scope` noting that one of A's derivations is a tangent whose natural home is existing note B. Maturation moves the derivation to B. B re-enters note convergence; A converges without the tangent.

**Signal:** a `comment.out-of-scope` whose content has an identifiable existing home.

### Scope promotion — questions move out

A `comment.out-of-scope` finding flags a question the current note cannot answer and that no existing note owns. Maturation creates a new inquiry note seeded by the finding. The current note is unchanged; a new sibling appears in the lattice.

**Worked example.** During note convergence on a note about a particular composition operator, a reviewer files `comment.out-of-scope` noting that the operator's behavior under iteration is a separate question worth pursuing. No existing note covers it. Maturation creates a new inquiry "behavior under iteration" with the finding as seed.

**Signal:** a `comment.out-of-scope` whose content cannot be absorbed into any existing note.

### The boundary: REVISE-with-extract vs OUT_OF_SCOPE

Two finding patterns share surface area but resolve differently:

**REVISE-with-extract.** A `comment.revise` finding is resolved by an edit that extracts material into a new foundation. The reviser's `resolution.edit` shrinks the note and adds citations to the extracted foundation. This is an in-note correctness issue — the note was carrying material that should be its own foundation. The note convergence protocol handles the resolution. Maturation handles the extract that follows.

**OUT_OF_SCOPE-with-promote.** A `comment.out-of-scope` finding signals that adjacent material is missing or misplaced — the current note is fine, but the lattice around it needs another node. Maturation handles the entire operation.

The boundary: REVISE-with-extract is "this note is carrying material that should be its own foundation." OUT_OF_SCOPE is "this note is fine; the lattice needs another node." The reviewer's classification draws the line.

### Provenance links

Lattice operations leave audit trails. When extract creates foundation F from material drawn from notes A and B, a `provenance.extract` link records the move. When absorb relocates material from A to B, a `provenance.absorb` link records the source. These are flat audit links — not protocol machinery, not load-bearing for any predicate. They support replay and structural-history reconstruction. Maturation files them when it executes the operation.

## Dependency ordering

Foundations converging before dependents is the efficient path, not the only path. When a foundation's claims are stable, dependents cite stable contracts and review cycles are shorter. When a foundation is still converging, dependents may cite contracts that later tighten — producing rework when the tightened contracts surface new findings downstream.

The protocol is correct either way. The convergence predicate doesn't check foundation maturity. It checks whether active `comment.revise` links have active resolutions. If a foundation changes after a dependent has converged, new review cycles file new `comment.revise` links on the dependent. The predicate goes false. The protocol resumes. Same outcome, more cycles.

The efficient ordering:

- Decompose foundation notes first — their claim structure stabilizes before dependents cite it
- Converge foundation claims before converging dependents — tightened contracts don't cascade rework
- Verify foundations before verifying dependents — verified contracts don't change

This ordering is a choreography recommendation. The maturation protocol recommends it. The convergence predicates enforce correctness regardless of whether it's followed.

## Hard reset

When a foundation turns out to be wrong — not incomplete, but wrong — a hard reset may be necessary. The human executor (§The supervision architecture) makes this judgment; no automated trigger currently exists for hard reset. A note re-enters discovery. Its freeze is revoked. All dependents that entered claim convergence against its claims must also reset — their citation links point at claims that are now unstable. The cascade follows the dependency graph upward.

Hard reset is a defined operation, not an error. It is expensive and destructive. A `provenance.reset` link on each affected note records the cascade. The alternative — leaving dependents building on a known-bad foundation — is worse.

Hard reset is distinct from the foundation-change feedback path. Foundation change handles a foundation whose contracts tightened or shifted during normal convergence — dependents absorb the changes through new `comment.revise` links. Hard reset handles a foundation whose premises were incorrect — dependents can't just re-converge, they may need to re-decompose because the claim structure itself may change.

## Feedback paths

Maturation is not strictly forward. Two feedback paths route content backward:

**Verification failure.** A contract is inconsistent. The claim re-enters claim convergence with the failure as a `comment.revise`. If the failure reveals a fundamental gap, the claim routes back to discovery via hard reset.

**Foundation change.** When a foundation claim changes, dependent notes carry stale citations. Their review cycles detect the staleness through findings traceable to the changed foundation. The maturation protocol doesn't push changes downstream — the convergence predicates detect staleness naturally through new `comment.revise` links filed on affected dependents.

## Quiescence

Lattice operations can trigger re-entry into note convergence, which can generate new `comment.out-of-scope` signals, which can trigger further lattice operations. This settles down — eventually no more triggers fire. But "no more triggers fire" is not a predicate on the link graph. It is quiescence — the absence of activity.

Maturation reaches quiescence when no transition conditions are met and no lattice operation signals are pending. This is different from convergence (a graph property that becomes true) and different from pure dispatch (fire once and done). The maturation protocol iterates without converging in the predicate sense. It settles.

## Participants

**Agents.** Each stage protocol has its own agents — channels, synthesizers, reviewers, revisers, validators, scope assemblers, translators, verifiers. The agents within a stage protocol are defined by that protocol. The maturation protocol doesn't have agents of its own — it has transition conditions and lattice operation triggers that the stage protocols' outputs satisfy or don't.

**Human (current executor).** The human is currently the maturation protocol's executor — evaluating transition conditions, triggering stage protocols, deciding when to run lattice operations. The human participates at defined exchange points:

- **Pose the initial question.** The question that starts a campaign.
- **Create campaigns.** Choose the channel pairing, curate the bridge vocabulary, set the target. Campaigns are parameters of the maturation protocol — they exist before any stage protocol runs.
- **Set transition thresholds.** How many diminishing-return cycles before decomposition? How strict is the claim file contract? These are policy decisions.
- **Intervene on transition misfires.** If a transition condition fires prematurely or fails to fire when it should, the human overrides. This is the fallback for transition conditions that don't yet capture what readiness actually means for this domain.
- **Evaluate final output.** Are the verified claims the right claims? Do they answer the question? Are the open questions worth pursuing as new campaigns?

The human's role shifts as transition conditions improve. Early in a domain's life, the human intervenes frequently — transition conditions are uncalibrated. Later, the human monitors and evaluates. The protocol runs. The human judges.

## The supervision architecture

The human is the maturation protocol's executor for the foreseeable future. The human triggers transitions by running scripts, evaluates transition conditions by reading stage protocol output, and decides when to run lattice operations. This is a deliberate architectural choice, not a gap waiting to be filled — the transition conditions are not yet reliable enough to automate, and the lattice operations require judgment the system cannot yet provide.

Two future architectures become possible as transition conditions mature:

**Explicit supervisor.** An agent watches the lattice, evaluates transition conditions, and triggers stage protocols. Centralized orchestration. Becomes viable when transition conditions are precise enough that an agent can evaluate them without human judgment.

**Emergent transitions.** Each stage protocol publishes a readiness signal on completion. The next stage protocol subscribes and starts when the signal arrives. Decentralized. Becomes viable when transition conditions are reliable enough that a signal is sufficient — no reasoning about edge cases needed.

The protocol design doesn't depend on which architecture eventually replaces human supervision. The transition conditions and handoff artifacts are the same — only who evaluates them changes.

## Related

- [Substrate Module](substrate.md) — the persistent link graph all protocols operate on. Provides permanence, retraction, and active-link semantics.
- [Convergence Protocol](convergence-protocol.md) — the document-type-neutral module both convergence protocols specialize.
- [Consultation Protocol](consultation-protocol.md) — the upstream producer that generates initial notes from campaign inquiries.
- [Note Convergence Protocol](note-convergence-protocol.md) — the stage protocol that drives notes to stability during discovery.
- [Claim Derivation Protocol](claim-derivation-protocol.md) — the stage protocol that decomposes notes into per-claim files.
- [Claim Convergence Protocol](claim-convergence-protocol.md) — the stage protocol that drives claims to formal precision.
- [Architecture](../architecture.md) — the six-level hierarchy and lattice structure the maturation protocol operates on.
- [Representation Change](../patterns/representation-change.md) — each transition is a representation change.
- [Validate Before Review](../patterns/validate-before-review.md) — a reusable pattern instantiated by multiple stage protocols.
- [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md) — the failure mode when a transition lacks an output contract.
- [Claim File Contract](../design-notes/claim-file-contract.md) — the output contract for the claim derivation → claim convergence transition.
- [Extract/Absorb](../patterns/extract-absorb.md) — lattice operations described in §Lattice operations.
- [Scope Promotion](../patterns/scope-promotion.md) — lattice operation described in §Lattice operations.
- [The Validation Principle](../principles/validation.md), [The Coupling Principle](../principles/coupling.md), [The Voice Principle](../principles/voice.md) — the quality boundary for all stage protocols.

This protocol replaces the pipeline and V-cycle architecture described in earlier versions of the system.