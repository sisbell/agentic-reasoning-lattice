# Self-Healing Areas

Places where the system could detect a disequilibrium pattern from its own operation and respond — either by flagging, proposing a fix, or executing one. Not a design for each area. A map of where self-healing is possible, partially present, or unrealized.

## Already automated

**Dependency cone detection.** Full-review and regional-sweep detect cones mechanically from git revision frequency and run cone-scoped review in response. No human intervention. Demonstrated working on ASN-0036's S8 and ASN-0034's T10a-N.

**Review convergence detection.** A scale converges when its reviewer finds no new issues. Mechanical signal. Already drives loop termination at each scale.

**Cone-sweep bottom-up ordering.** Walks the dependency DAG in topological order so each cone has stable downstream context. Automatic.

**LLM-failure distinction.** Full-review and regional-sweep now distinguish "converged" from "review errored" so a failed cycle doesn't get counted as success. Mechanical.

## Detection ready, action not yet automated

**Contract Sprawl.** Signal: same claim's formal contract grows across multiple cone cycles. Git history + contract-length delta would detect it. Action could range from flagging to proposing a split plan to executing the split. Judgment of what to split and how to name the pieces currently requires human input.

**Citation Drift (internal).** Full-review finds these but only on its own schedule. A dedicated scan between sweeps could surface drift faster. Already self-corrects once detected.

**Bridge-citation gaps.** A subtype of Citation Drift. Detectable by identifying proof steps that move between concepts without citing the claim that licenses the move. Needs LLM-level analysis, not just text matching.

**Non-converging cones.** A cone hitting max_cycles without a "no new issues" signal. Already visible in output. Could be surfaced as a first-class alert and cross-referenced with other signals (is the apex also a sprawl candidate?).

**Vocabulary convergence (readiness signal).** When a note's discovery review/revise cycles stop introducing new coinages or pulling in new upstream terms, the note has finished its invention work and is ready for formalization. Signal: zero new italicized prose terms or coined operators across the last N cycles. Action: flag or auto-promote to formalization. False-positive cost is low (a misfire just triggers formalization one cycle early). Meets all three viability criteria. Complements [Domain Language Emergence](domain-language-emergence.md)'s observation that vocabulary convergence is the natural signal of discovery completion.

## Further out

**Cross-note foundation drift (passive).** When an upstream note changes, every downstream consumer carries citation drift until a rebase pass. No automated mechanism currently scans for passive drift. A cross-note validator could detect "downstream cites label that no longer exists upstream" or "downstream's understanding of upstream is stale."

**Summary staleness.** A claim's summary YAML field may describe old content if the claim has been revised. Summarize.py uses content hashes for its own cache, but a consumer of summaries has no signal that a summary is out of date relative to the formal contract it summarizes.

**Attractor formation, not just sprawl.** Before a claim sprawls, it often shows early signs — new clauses being added about a specific concept, multiple proofs independently citing the same fact through it. Catching attractor formation before sprawl would prevent the cascade entirely. Requires concept-level understanding of what a claim is absorbing.

**Cross-note vocabulary collision.** Two notes using the same symbol for different things, discoverable only by comparing vocabulary YAML across notes. Not currently scanned.

**Proof correctness drift after foundation changes.** A downstream proof might remain technically valid after a foundation changes, but no longer be optimal or cite the most precise axiom. No mechanism currently evaluates this.

## What makes a self-healing target viable

Three requirements that separate viable targets from speculative ones:

1. **Mechanical signal.** The pattern has a signal that doesn't require LLM interpretation to detect (commit frequency, file sizes, cross-reference validity). LLM can be used for analysis once detection fires.
2. **Clear action.** The response doesn't require open-ended judgment. Re-running review, proposing a split plan, or flagging for human are all clear actions. "Fix the note" is not.
3. **Low false-positive cost.** If the detection fires incorrectly, the consequence is tolerable. A false cone detection costs a focused review cycle (small). A false auto-split would create structural damage (large). Detection should fire aggressively; action should escalate carefully.

Dependency cone meets all three — that's why it's already automated. Contract Sprawl meets 1 and 3 at the detection level and 2 at the flag level, which is why flagging is the natural next step and auto-splitting is not.
