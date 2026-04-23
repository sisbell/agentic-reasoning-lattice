# Reviser Prompt Discipline

*Practice. Guidance for humans authoring or editing the content-reviser prompts. Gives the reviser a rank-ordering over resolution choices so that its default reflex — adding prose — no longer wins the close calls.*

## The default failure mode

Given a review finding and freedom to edit, an LLM reviser's first reflex is to append: a justifying sentence, a defensive parenthetical, an explanatory clause, a rebuttal to the finding's concern. The prose grows monotonically even when each individual finding asked for simplification.

A reviser that isn't explicitly constrained will:

- Add a justifying clause to defend why a flagged construction is actually correct
- Relocate flagged content to a different paragraph instead of deleting it
- Append a bundling-justification paragraph to explain why two axioms coexist
- Insert an exhaustiveness claim ("this list is exhaustive") to preempt future findings
- Write out inline use-site enumerations that belong in metadata

Each response is locally reasonable. Aggregated across cycles, the prose surface grows faster than the reasoning. This is [reviser add-bias](../equilibrium/prose-sprawl.md#forces) driving [Prose Sprawl](../equilibrium/prose-sprawl.md) — the narrative-surface manifestation of [Surface Expansion](../equilibrium/surface-expansion.md).

## The discipline — a rank-ordering

When a review finding admits multiple resolutions that would close it equally well, the reviser follows this ranking:

    delete > restructure > add

**This is a tiebreaker for close calls, not a mandate.** Findings that require adding — a missing axiom, a missing precondition, a needed clarification deletion wouldn't preserve — produce additions regardless of the ranking. The ranking applies only when multiple resolutions would close the finding and the choice between them is genuinely judgment.

Within that scope, five directives:

**1. Prefer deletion over addition.** When a finding can be resolved by deleting the flagged construction or its surrounding justification, delete. Only add when no deletion resolves the finding.

**2. When a finding says drop X, drop X — do not relocate.** Moving X to a different paragraph, rephrasing X in a new place, or folding X into an adjacent clause all leave the drift in the file. Relocation is not deletion.

**3. Do not justify excluded cases.** If a claim's carrier (or precondition, or scope) excludes a case, do not write prose about what would happen in that case. "If `t` had length 0, then..." for a carrier `T` whose members all satisfy `1 ≤ #t` is defensive prose for a case that cannot arise.

**4. Do not append meta-commentary about the edit.** No "this structure is exhaustive," no "this matches the convention in sibling claims," no "note that this is consistent with...", no inline commentary about the revise process. Structural facts that readers could confirm by looking at siblings do not belong in the claim under revision.

**5. When adding is required, add the minimum.** If a finding demands a new axiom, add the axiom statement — not an axiom statement plus a paragraph explaining why it is needed plus an enumeration of downstream consumers plus a defense of the bundling. The axiom is load-bearing; the surrounding exegesis is not.

## Why this specific ordering

The ordering is an empirical response to observed drift, not a universal principle:

- **Minimality.** Deletion is the smallest possible change. Smaller changes are easier to verify and less likely to cascade.
- **Counter-bias.** The LLM reviser's default is toward addition. The ranking nudges it off its default. In a hypothetical system where the reviser was delete-biased — dropping load-bearing content — we would flip the ordering.
- **Surface convergence.** Each addition creates new surface a future reviewer may flag. Each deletion closes a loop. Over many cycles, deletion is convergent; addition is divergent.

None of these arguments prove delete is always the right choice. They show delete is the right tiebreaker *for our failure mode*. When the reviser's natural judgment clearly indicates a non-delete resolution (a missing axiom is only closed by adding it), reviser judgment prevails.

## What stays

The discipline targets *non-reasoning* prose. These stay untouched:

- Axiom and definition statements in the Formal Contract
- Proof text, case analyses, inference steps
- Preconditions, postconditions, and frame conditions
- Explicit derivation prose that advances the claim's argument
- Dependency citations in the Depends section (with one-line descriptions)

The target is a claim file where every paragraph either states or derives content. Paragraphs that *describe the shape of* other paragraphs are the discipline's scope.

## Where the discipline applies

Every prompt that drives an LLM reviser against a review finding should encode the discipline. Currently two prompts in this system:

- `prompts/shared/formalization/local-review/revise.md` — per-claim revisions
- `prompts/shared/formalization/full-review/revise.md` — whole-note revisions

`prompts/shared/formalization/contract-review/fix-contract.md` is a narrower reviser bound to the Formal Contract block; add-bias is less likely there (the contract structure is constrained), but the discipline still applies when prose accompanies the contract edits.

Validate-revise prompts already encode a narrower version of this discipline ("do not extend, restructure, or refactor surrounding content") because their scope is structural. The content-reviser prompts are where add-bias most aggressively manifests and where the discipline has the highest leverage.

## Signals the discipline is not working

- Review findings across consecutive cycles reference content added in earlier revise commits
- A finding flagged in cycle N reappears in cycle N+1 in a nearby paragraph
- The claim's word count grows faster than its axiom/proof content
- Prose:formal ratio drifts above the [Coupling Principle](../principles/coupling.md)'s 70/30 target within a sweep
- Findings-per-cycle is not monotonically decreasing across a converging sweep

## What the discipline does not cover

- **Legitimate content expansion.** When a finding introduces genuinely new axiomatic material — a missing dichotomy axiom, a missing precondition — the fix is addition. The discipline constrains *non-reasoning* prose; it does not constrain reasoning or axioms the finding explicitly asks for.
- **Structural violations** (body duplication, declaration mismatch, etc.). Those are the [validator](../design-notes/claim-file-contract.md)'s domain, fixed by [Validate-Before-Review](../patterns/validate-before-review.md).
- **Reviewer-driven oscillation**. If cycle N's reviewer says "add X" and cycle N+1's reviewer says "remove X," the cycles disagree about whether X is load-bearing. No reviser-side discipline can fix that. See [Reverse-Course Oscillation](../equilibrium/reverse-course-oscillation.md) for the broader failure class.

## Related

- [Surface Expansion](../equilibrium/surface-expansion.md) — the root failure mode the ranking resists. Every deletion-first tiebreaker is a move against surface growth.
- [Prose Sprawl](../equilibrium/prose-sprawl.md) — the narrative-surface form of Surface Expansion. Reviser add-bias is named as a force there; this note is how that force is resisted operationally.
- [The Coupling Principle](../principles/coupling.md) — the 70/30 prose:formal ratio target and the ratio-drift signal that detects add-bias at the file level.
- [Audit by Content](../design-notes/audit-by-content.md) — parallel discipline for evaluators, encoded at the prompt layer rather than as a human-facing practice. Both address LLM-behavior failure modes with prompt-level constraints; audit-by-content is the system's own rule (baked into evaluator prompts), while this note is advice to whoever writes the reviser prompts.
- [Reverse-Course Oscillation](../equilibrium/reverse-course-oscillation.md) — a deterministic ranking has anti-oscillation as a side effect (cycle N and cycle N+1 resolve the same finding the same way), but the ranking's *motivation* is surface reduction, not determinism.
- [Validate Before Review](../patterns/validate-before-review.md) — the operational pattern that keeps the reviser's workload focused on semantic issues by pre-clearing structural ones.
