# Reviser Prompt Discipline

*Practice. Guidance for humans authoring or editing the content-reviser prompts so that they resist [reviser add-bias](../equilibrium/prose-sprawl.md#forces) — the default LLM reflex to answer a finding by adding prose rather than by restructuring or deleting.*

## The default failure mode

Given a review finding and freedom to edit, an LLM reviser's first reflex is to append: a justifying sentence, a defensive parenthetical, an explanatory clause, a rebuttal to the finding's concern. The prose grows monotonically even when each individual finding asked for simplification. This is [reviser add-bias](../equilibrium/prose-sprawl.md#forces) and it directly drives [Prose Sprawl](../equilibrium/prose-sprawl.md).

A reviser that isn't explicitly constrained will:

- Add a justifying clause to defend why a flagged construction is actually correct
- Relocate flagged content to a different paragraph instead of deleting it
- Append a bundling-justification paragraph to explain why two axioms coexist
- Insert an exhaustiveness claim ("this list is exhaustive") to preempt future findings
- Write out inline use-site enumerations that belong in metadata

Each response is locally reasonable. Aggregated across cycles, the prose surface grows faster than the reasoning.

## The discipline

Reviser prompts must constrain the default reflex explicitly. Five directives cover the bulk of the failure modes.

**1. Prefer deletion over addition.** When a finding can be resolved by deleting (removing the flagged construction, removing the surrounding justification, replacing a paragraph with nothing), delete. Only add when no deletion resolves the finding.

**2. When a finding says drop X, drop X — do not relocate.** Moving X to a different paragraph, rephrasing X in a new place, or folding X into an adjacent clause all leave the drift in the file. If the finding's remedy is removal, the remedy is removal — the new location does not convert dead-weight prose into load-bearing prose.

**3. Do not justify excluded cases.** If a claim's carrier (or precondition, or scope) excludes a case, do not write prose about what would happen in that case. "If `t` had length 0, then..." for a carrier `T` whose members all satisfy `1 ≤ #t` is defensive prose for a case that cannot arise. Delete any clause whose entire content is "here's what would happen outside the claim's scope."

**4. Do not append meta-commentary about the edit.** No "this structure is exhaustive," no "this matches the convention in sibling claims," no "note that this is consistent with...", no inline commentary about the revise process. Structural facts that readers could confirm by looking at siblings do not belong in the claim under revision.

**5. When adding is genuinely required, add the minimum.** If a finding demands a new axiom, add the axiom statement — not an axiom statement plus a paragraph explaining why it is needed plus an enumeration of downstream consumers plus a defense of the bundling. The axiom is load-bearing; the surrounding exegesis is not.

## What stays

The discipline is about *non-reasoning* prose. These stay untouched:

- Axiom and definition statements in the Formal Contract
- Proof text, case analyses, inference steps
- Preconditions, postconditions, and frame conditions
- Explicit derivation prose that advances the claim's argument
- Dependency citations in the Depends section (with one-line descriptions)

The target is a claim file where every paragraph either states or derives content. Paragraphs that *describe the shape of* other paragraphs are the discipline's scope.

## Where the discipline applies

Every prompt that drives an LLM reviser against a review finding should encode the discipline. In this system:

- `prompts/shared/formalization/revise.md` (and stage-specific variants)
- `prompts/shared/formalization/contract-review/revise.md`
- `prompts/shared/formalization/local-review/revise.md`
- `prompts/shared/formalization/full-review/revise.md`

Validate-revise prompts already encode a narrower version of this discipline ("Do not extend, restructure, or refactor surrounding content") because their scope is structural. The content-reviser prompts are where add-bias most aggressively manifests and where the discipline has the highest leverage.

## Signals the discipline is not working

- Review findings across consecutive cycles reference content added in earlier revise commits
- A finding flagged in cycle N reappears in cycle N+1 in a nearby paragraph
- The claim's word count grows faster than its axiom/proof content
- Prose:formal ratio drifts above the [Coupling Principle](../principles/coupling.md)'s 70/30 target within a sweep

## What the discipline does not cover

- Legitimate content expansion when a finding introduces genuinely new axiomatic material (e.g., a missing dichotomy axiom, a missing precondition). The discipline constrains *non-reasoning* prose; it does not constrain reasoning or axioms that the finding explicitly asks for.
- Structural violations (body duplication, declaration mismatch, etc.). Those are the [validator](../design-notes/claim-file-contract.md)'s domain, fixed by [Validate-Before-Review](../patterns/validate-before-review.md).
- Cross-cycle oscillation that is not prose-based (e.g., reviser adds a cite in one cycle, removes it in the next). That's [Reverse-Course Oscillation](../equilibrium/reverse-course-oscillation.md) — distinct pattern, distinct mechanism.

## Related

- [Prose Sprawl](../equilibrium/prose-sprawl.md) — the failure mode this discipline prevents. Add-bias is named as a force within Prose Sprawl; this note is how that force is resisted operationally.
- [The Coupling Principle](../principles/coupling.md) — the 70/30 prose:formal ratio target and the ratio-drift signal that detects add-bias at the file level.
- [Audit by Content](../design-notes/audit-by-content.md) — the parallel discipline for evaluators, encoded at the prompt layer rather than as a human-facing practice. Both address LLM-behavior failure modes with prompt-level constraints; audit-by-content is the system's own rule (baked into evaluator prompts), while this note is advice to whoever writes the reviser prompts.
- [Validate Before Review](../patterns/validate-before-review.md) — the operational pattern that keeps the reviser's workload focused on semantic issues by pre-clearing structural ones.
