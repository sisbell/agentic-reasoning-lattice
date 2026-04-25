# Audit by Content

*Design note. Operational rule for the evaluation layer.*

## Decision

Evaluation in this system reads the artifact, not the summary. A reviewer reading a sweep's output reads the diffs. An agent reviewing another agent's output reads the revised content. A meta-audit grading a cycle's commits reads the actual changes. Commit messages, diff stats, finding counts, cycle tallies — none of these are evaluation inputs. They are the generator's own account of what it did, and treating that account as evidence is [Self-Report Laundering](self-healing.md#observation-layer-limitation).

## Why

Summaries and artifacts are produced by the same machinery. The summary surface is the generator's voice, re-presented. An evaluator that accepts the summary as evidence inherits every blind spot of the generator that produced it. This is a failure of the self-healing mechanism itself: the evaluator cannot detect what it cannot see, and summaries systematically hide intent/outcome divergence.

## How the system enforces it

The decision has two enforcement sites.

**Prompts.** Evaluator prompts — the full-review prompt, the regional-sweep reviewer, any agent invoked in an audit role — instruct the agent to read artifacts and quote specific content when classifying. The prompt names Self-Report Laundering as a specific failure mode to avoid.

**Context.** Evaluator agents are given the artifact as input, not metadata about it. A pipeline that hands an agent only commit messages and `--stat` output has a configuration gap. The diff text itself is what goes into the context window. Finding texts, revised content, and the structural state being evaluated are passed in directly, not summarized before arrival.

## Rules of the decision

- **Read proportional to stakes.** A high-stakes audit opens each artifact. A low-stakes scan can operate on summaries, but the output must be labelled summary-based.
- **Quote when classifying.** A verdict of "item X is bad" must cite a specific line, hunk, or structural change. No quote, no verdict. Confidence cannot exceed what was read.
- **Expect surprises.** Evaluating a batch and finding no items whose actual effect disagrees with their summary is a signal that reading was summary-level. Either the process was unusually clean or the evaluator did not look.
- **Name shortcuts.** "Based on commit messages only, not diffs" is an honest verdict-qualifier. A confident percentage grade derived from stats is not.

## Signals the decision is being violated

- Evaluator output references `git log --oneline` or `--stat` without quoting specific diff hunks
- Classifications use percentages or graded scores derived from proxy signals
- Stated confidence exceeds what reading depth justifies
- Verdict would change if commit messages were stripped — because messages are what was actually read

## Related

- [Self-Report Laundering](self-healing.md#observation-layer-limitation) — the failure mode this decision addresses.
- [Claim Convergence Protocol](../protocols/claim-convergence-protocol.md) — the review machinery that this rule governs at every scale (local-review, regional-sweep, full-review).
- [Consult Authority](../patterns/consult-authority.md) — the analogous grounding discipline during refinement rather than evaluation. Both commit the agent to reading primary content rather than derivative summary.
