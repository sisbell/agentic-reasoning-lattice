# Self-Healing Areas

Where the system could detect a disequilibrium pattern from its own operation and respond — by flagging, proposing a fix, or executing one. A map, not a design for each area.

## Viability criteria

Three requirements separate viable targets from speculative ones:

1. **Mechanical signal.** The pattern has a signal that doesn't require LLM interpretation to detect (commit frequency, file sizes, cross-reference validity). LLM can be used for analysis once detection fires.
2. **Clear action.** The response doesn't require open-ended judgment. Re-running review, proposing a split plan, or flagging for human are all clear actions. "Fix the note" is not.
3. **Low false-positive cost.** If the detection fires incorrectly, the consequence is tolerable. A false cone detection costs a focused review cycle (small). A false auto-split would create structural damage (large). Detection should fire aggressively; action should escalate carefully.

Criterion 1 is load-bearing for a specific reason: see [Observation-layer limitation](#observation-layer-limitation) below.

## The map

### Convergence and cycle health

**Review convergence.** The convergence predicate — every `comment.revise` has a `resolution` — drives loop termination. Any participant can evaluate it at any time from the link graph. *Automated.*

**Non-converging cones.** A cone hitting max_cycles without the predicate becoming true. Already visible in output. Could be surfaced as a first-class alert and cross-referenced with sprawl signals on the apex claim. Non-convergence detection — oscillation, reject cycling, classification bias — is a choreography and monitoring concern. See [Claim Convergence](../claim-convergence.md) for detection strategies. *Detectable, not yet surfaced.*

**Oscillation detection.** When a file region is modified in opposite directions across consecutive cycles (add in cycle N, remove in cycle N+1), the cone is stuck — not failing to converge but actively oscillating. Sharper signal than cycle-count stationarity. Detectable from diff-level analysis across cycles. *Speculative.*

### Dependency structure

**Dependency cone detection.** Full-review and cone-sweep detect cones mechanically from git revision frequency and run cone-scoped review. *Automated.*

**Cone-sweep bottom-up ordering.** Walks the dependency DAG in topological order so each cone has stable downstream context. *Automated.*

### Sprawl and surface expansion

**Contract Sprawl.** Signal: a claim's formal contract grows across multiple cone cycles. Git history plus contract-length delta would detect it. Flagging is the natural next step; auto-splitting requires judgment about what to split and how to name the pieces. *Detectable, action at flag level only.*

**Attractor formation.** Before a claim sprawls, it often shows early signs — new clauses accreting about a specific concept, multiple proofs independently routing through it. Catching attractor formation before sprawl would prevent the cascade. Requires concept-level understanding of what a claim is absorbing. *Speculative.*

### Structural integrity

**Citation Drift (internal).** Full-review finds these on its own schedule. A dedicated scan between sweeps could surface drift faster. Self-corrects once detected. *Detectable.*

**Bridge-citation gaps.** A subtype of Citation Drift: proof steps that move between concepts without citing the claim that licenses the move. Needs LLM-level analysis, not text matching. *Speculative.*

**Cross-note foundation drift.** When an upstream note changes, every downstream consumer carries citation drift until a rebase pass. A cross-note validator could detect "downstream cites label that no longer exists upstream" or "downstream's understanding of upstream is stale." The [maturation protocol](../protocols/maturation-protocol.md)'s foundation-change feedback path handles this through the convergence predicate — new `comment.revise` links filed on affected dependents. *Detectable; partially handled by protocol.*

**Cross-note vocabulary collision.** Two notes using the same symbol for different things, discoverable by comparing vocabulary YAML across notes. *Speculative — mechanical signal exists but not scanned.*

**Summary staleness.** A claim's summary YAML field may describe old content if the claim has been revised. Content hashes exist for cache but no consumer-facing staleness signal. *Detectable.*

### Stage transitions

**Vocabulary convergence (discovery → claim derivation readiness).** When a note's review/revise cycles stop introducing new coinages or new upstream terms, the note has finished its invention work. Signal: zero new italicized prose terms or coined operators across the last N cycles. The [maturation protocol](../protocols/maturation-protocol.md) uses this as part of the discovery → claim derivation transition condition alongside the [note convergence protocol](../protocols/note-convergence-protocol.md)'s predicate. *Operational as a transition signal.*

**Proof correctness drift after foundation changes.** A downstream proof might remain technically valid after a foundation changes but no longer cite the most precise axiom. No mechanism currently evaluates this. *Speculative.*

### LLM-failure handling

**LLM-failure distinction.** Full-review and cone-sweep distinguish "converged" from "review errored" so a failed cycle doesn't get counted as success. *Automated.*

## Observation-layer limitation

Self-healing depends on observation. When the observation layer itself is compromised, detection fails silently — mechanical signals stay clean while problems compound.

Two observation-layer forces are documented:

**Self-Report Laundering.** An LLM evaluating LLM-produced work reads the summaries the process generated about itself (commit messages, finding counts, diff stats) rather than the artifacts (diffs, revised content). Summaries describe intent. They are silent when intent and outcome diverge. The evaluator's confidence tracks the proxy, not the work.

In a 28-commit sweep audit, a commit classified as middling "accretion/churn" based on stats (`+81 −4`) and message ("4 issues, 3 resolved") turned out to contain the single most architecturally damaging change in the set — inlining a claim body into a file where that body was already canonical elsewhere. The message accurately described the write. It was silent about the [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md) symptom the write created.

**[Production Drive](production-drive.md).** The LLM reviewer's tendency to generate findings and push them toward action. The off-ramp categories (OBSERVE in claim convergence, OUT_OF_SCOPE in note convergence) channel this drive safely. But if the off-ramp is miscalibrated — too attractive, absorbing legitimate REVISE items — the system sees concerns filed but not acted on. The reviewer detected the issue; the classification prevented action. This is a form of detection that fails to produce correction, compromising self-healing through the classification layer rather than through the observation layer.

This is why criterion 1 (mechanical signal) is load-bearing. Mechanical detection — file sizes, cross-reference validity, cycle counts, dependency-graph acyclicity, the convergence predicate itself — is not subject to self-report laundering or production-drive miscalibration. LLM-level evaluation is. The viable self-healing targets are those where a mechanical signal fires first and LLM analysis is invoked only after detection, not as the detection mechanism itself.

For the operational discipline that addresses self-report laundering in evaluation contexts, see [Audit by Content](audit-by-content.md).

## Related

- [Surface Expansion](../equilibrium/surface-expansion.md) — the primary failure mode that sprawl detection targets
- [Contract Sprawl](../equilibrium/contract-sprawl.md) — attractor formation is the early-detection variant
- [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md) — structural-integrity checks are the mechanical-signal form of the validator the uncontracted representation change is missing
- [Audit by Content](audit-by-content.md) — the evaluation discipline that addresses self-report laundering
- [The Coupling Principle](../principles/coupling.md) — the coupling feedback loop is itself a self-healing mechanism operating through prompt calibration
- [Production Drive](production-drive.md) — the LLM behavioral force that compromises self-healing through classification miscalibration
- [Convergence Protocol](../protocols/convergence-protocol.md) — the predicate is itself a mechanical self-healing signal: evaluable by any participant at any time
- [Claim Convergence](../claim-convergence.md) — non-convergence detection strategies (oscillation, reject cycling, classification bias)