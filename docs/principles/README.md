# Principles

Three principles form the quality boundary for building claims. Each protects a different face of the claim-production process. Together they keep the review cycle focused on its actual job — finding semantic issues in the reasoning.

![Principles triangle](../diagrams/principles-triangle.svg)

## The three sides

**[Coupling](coupling.md)** — the content is balanced. Prose and formal content are authored as a pair, at an artifact-specific ratio (90/10 for notes, 70/30 for claim files). Divergence from the ratio signals that one surface is growing without the other. Without coupling, the review cycle drowns in [Surface Expansion](../equilibrium/surface-expansion.md) — meta-prose noise that compounds each cycle.

**[Validation](validation.md)** — the structure is sound. Every representation has a structural contract — mechanically checkable invariants that must hold before review begins. Without validation, the review cycle spends its cycles on structural violations ([Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md)) that a validator would catch in one pass.

**[Voice](voice.md)** — the output is well-formed by construction. Positive style structure (the Dijkstra voice) constrains LLM agents to load-bearing prose. Enumerated prohibition lists leave gaps the agent drifts through. Positive voice leaves no slot for non-reasoning content. Without voice, the reviser's add-bias produces [Prose Sprawl](../equilibrium/prose-sprawl.md) that the other two principles detect but cannot prevent.

## Why three, not one

Each principle uses the mechanism appropriate to its domain:

| Principle | Domain | Mechanism | Why this mechanism |
|-----------|--------|-----------|-------------------|
| Coupling | Content balance | Ratio monitoring | The ratio is a single number; its drift is a diagnosis |
| Validation | Structural integrity | Enumeration | Structural invariants are a closed set — every bad case is enumerable |
| Voice | Output quality | Positive definition | Prose quality is an open set — bad cases can't be enumerated, so define the good case |

Coupling monitors. Validation enumerates. Voice defines. No single mechanism covers all three domains — ratio monitoring can't check structural invariants, enumeration can't constrain open-ended prose, and positive definition can't replace a mechanical validator. The three are complementary, not redundant.

## How the principles were found

Voice was not discovered last. It was the starting condition.

**Voice was present from the beginning.** The discovery stage ran under Dijkstra voice from its first prompt — prose with embedded formalism, named invariants, frame conditions, discovery voice. It worked. Notes converged. Prose stayed coupled to formal content. Nobody called it a principle. It was just "the prompt."

**Voice was lost at a transition.** When formalization began, the prompts changed. A different voice (Lamport), a different stance (precision-checking rather than reasoning), and prescriptive discipline (rank-ordering: delete > restructure > add) replaced the original style. The problems appeared immediately — surface expansion, add-bias, non-convergence, 190,940 words of bloat across 80 claim files.

**Coupling was articulated to diagnose the symptoms.** The prose:formal ratio named what was going wrong with content balance. The 70/30 target for claim files, the 90/10 target for notes, the divergence signal — all of this was built to see the problem clearly. Necessary, but it could only detect the drift, not stop it.

**Validation was articulated to handle structural noise.** With coupling restored through a compress pass, the dominant finding class shifted to structural violations — duplicate declarations, dangling references, metadata disagreement. The structural validator and the claim-file contract were built to clear this noise before the reviewer saw it. Necessary, but the content noise remained.

**Voice was rediscovered.** Going back to the discovery prompts — same Dijkstra style, same notation, same rigor sections, same "what not to write" — fixed what coupling monitoring and structural validation could not. The rank-ordering was removed. The prescriptive discipline was removed. The Dijkstra voice carried the anti-bloat discipline through craft, not rules. Only then was voice named as a principle and understood as the upstream constraint the other two depend on.

The two intermediate principles are genuinely needed — coupling detects drift that voice alone can't prevent (a healthy voice still produces content whose ratio must be monitored), and validation catches structural violations that voice has nothing to say about (file-level invariants are outside prose style). But both were treating symptoms of a voice loss, not independent problems. The system had the right process, lost it during a representation change, built two layers of tooling to manage the consequences, and finally recognized that the original process was the actual fix.

## The Deming parallel

The three principles map to Deming's three layers of quality control: inspection (checking the output), monitoring (measuring the process), and process control (constraining how work is produced). Deming's central insight was about their ordering — the most effective intervention is the one closest to where the work is generated, not the one closest to where the output is consumed.

Voice operates at the point of generation (the reviser's prompt). Coupling operates at the point of measurement (the ratio check). Validation operates at the point of consumption (the reviewer's input). All three are needed, but voice is the most upstream.

Deming's deeper observation was not "discover process control after inspection and monitoring." It was: you already know what good process looks like — stop abandoning it when you change contexts. That is exactly what happened. The discovery prompts had the right process. Formalization abandoned it, suffered the consequences, built inspection and monitoring layers to manage the symptoms, and finally recognized that the original process was the fix.

## What remains for the reviewer

When all three principles hold, the reviewer sees:

- Content that is balanced (coupling holds)
- Structure that is sound (invariants hold)
- Prose that is well-formed (voice discipline held during revision)

What's left is the reasoning itself — derivation gaps, regime mismatches, smuggled postulates, missing consequences, incomplete case analyses. That is the reviewer's job. Everything else has been cleared from its path.