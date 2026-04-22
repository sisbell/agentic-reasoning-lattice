# Validate Before Review — Design

*Design note. The design decisions behind the [validate-before-review](../patterns/validate-before-review.md) pattern.*

## Invariants

When a representation change splits one artifact into many files, conditions come into existence that must hold for the structure to mean anything. One body per file. Filename matches label. References resolve. Metadata agrees with content. No dependency cycles. These are invariants — conditions that must be true at every stable point, not just at creation.

If an invariant is violated, the structure looks intact but operations on it produce wrong results silently. The structural contract ([Claim File Contract](claim-file-contract.md)) names the invariant set. The validator checks them. The design decisions below follow from taking these conditions seriously.

## Why two passes, not one

The original design ran one pass: an LLM reviewer finds all issues (structural and semantic), an LLM reviser fixes them. This doesn't converge when structural violations are present — the reviewer finds structural symptoms one per cycle, and the reviser's fixes introduce new structural violations through add-bias. Structural and semantic concerns need different tools. The two-pass design separates them: a mechanical pass for structural invariants, then an LLM pass for semantic issues.

## Why mechanical validation, not LLM validation

An LLM reviewer reading "X defined twice" sees a textual symptom. It cannot distinguish "valid inline reference" from "canonical body duplicated across files" because file boundaries were stripped during assembly. A mechanical validator checks against the structural contract directly — it knows which file each declaration lives in, which references resolve, whether metadata agrees. The validator operates on the representation's actual structure, not on a flattened textual projection of it.

Mechanical validation is also exhaustive and cheap. It finds every violation in one pass. LLM review finds one per cycle at LLM cost. For the structural invariants in the claim-file contract, mechanical checking is strictly superior.

## Why per-invariant fix recipes, not a general structural reviser

A single "fix structural issues" prompt would face the same add-bias problem as the reviewer — given multiple violations, the reviser picks the easiest textual fix rather than the correct structural one. Per-invariant recipes constrain the reviser to one violation class at a time with a specific resolution strategy. "Body exists in two files — identify canonical home, remove duplicate" is a clearer instruction than "fix structural issues."

Per-invariant recipes also make the contract auditable. Each recipe corresponds to one contract rule. When a new invariant is added to the contract, it gets one new recipe. When an invariant is retired, its recipe is removed. The mapping is one-to-one.

## Why validate at every scale, not just once

The V-Cycle operates at three scales (local, regional, full). Each scale's revise pass can break invariants — a regional-revise that inlines one claim's body into another's file to reconcile notation violates uniqueness; a full-revise that renames a file without cascading references violates filename-label-match and reference-resolution at once. Invariants are not established once and preserved automatically. Every mutation can break them. Running the validator before each scale's review cycle catches what the previous scale's revisions introduced.

The cost is acceptable. Mechanical validation is fast compared to LLM review. The alternative — validating once at the start and trusting that revise passes preserve invariants — requires every revise prompt to encode structural awareness, which is the conflation the two-pass design exists to avoid.

## What goes in the structural contract vs what stays with the reviewer

The boundary: can a script check it without understanding the content? If yes, it's a structural invariant — the validator checks it. If no, it's a semantic invariant — the reviewer checks it.

"One body per file" is structural — a script can detect duplicate bold declarations. "Postconditions match what the proof establishes" is semantic — checking it requires reading the reasoning. This boundary is clean in practice. The grey zone is small — "every symbol used cites a defining source" is borderline (a script can check citation presence but not whether the citation is the right one). When in doubt, put it in the validator. A false positive from the validator costs one unnecessary fix. A missed structural violation in review costs cycles of non-convergence.

## Intermediate states during fixes

A fix may legitimately break an invariant mid-step — delete a duplicate body, then update references that pointed at it. The invariant holds at the committed output of each validate-revise cycle, not at every intermediate write. The contract must state this explicitly so the validator checks at the right granularity.

## Related

- [Validate Before Review](../patterns/validate-before-review.md) — the pattern these decisions serve.
- [The Validation Principle](../principles/validation.md) — the commitment behind the pattern.
- [Claim File Contract](claim-file-contract.md) — the structural contract the validator checks against. The contract's rules drive the validator's checklist and the per-invariant recipe set.
- [Review V-Cycle](review-v-cycle.md) — the review machinery this runs before at each scale.