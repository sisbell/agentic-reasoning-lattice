# Uncontracted Representation Change

A pipeline stage introduces a new unit of structure — per-claim files, per-proof files, typed dependencies, any split of what was previously unified — without specifying what well-formed output means. The structure lands on disk. No contract says what must hold. Downstream agents inherit the structure without the rules and spend review cycles on symptoms of violations that have no names.

## Forces

**Producing is easier than specifying.** Splitting a monolithic ASN into per-claim files is straightforward. Writing down what valid per-claim files look like — one body per file, filename matches label, references resolve, metadata agrees with content, no dependency cycles — is a separate effort that the pipeline doesn't force you to do. The output exists before its contract does.

**The gap is invisible until review.** Malformed output from a transition looks normal. Files exist, they contain content, they parse. Nothing fails until a downstream reviewer starts finding symptoms — duplicate definitions, dangling references, metadata disagreement — without being able to name the structural cause. The absence of a contract produces no error. It produces an indefinite review loop.

**Each new transition resets the pressure.** The temptation to skip the contract is not a one-time event. Every time someone introduces a new structural unit — per-proof files, structured review history, typed dependency edges — the same pressure applies. The output is concrete and shippable. The contract is abstract and skippable. The pressure recurs at every boundary.

## Signal

- **Non-converging cones whose findings are structural, not semantic.** The reviewer finds "X defined twice," "Y cited but missing," "metadata disagrees" — symptoms of structural violations, not reasoning errors. Each cycle resolves one symptom and surfaces another. The cone cannot converge because the root cause is not a content problem.
- **Reverse-course oscillation.** A reviser adds something in cycle N that the reviewer removes in cycle N+1. The structural home of the change is undecided because no contract says where it belongs.
- **Multiple cones independently patching the same gap.** Four cones each rewrite the same notation at their own use-sites rather than extending the source definition once. The contract that would say "every symbol has one defining source" doesn't exist, so each cone invents its own local fix.
- **Review findings that a script could catch.** If most of a cone's findings are mechanically checkable (duplicate declarations, dangling references, metadata agreement, dependency-graph acyclicity), the review cycle is doing a validator's job because no validator exists because no contract defines what to validate.

## Example: ASN-0034 blueprinting

ASN-0034 was blueprinted into ~80 per-claim files. No contract specified what valid per-claim output looks like. One commit (`54f55598`) copied a claim body into a file where the same body already had a canonical home. Sixteen review cycles across two cones found symptoms — definition drift, redundant declarations, inconsistent notation — without ever surfacing the root cause. The T1 cone on the same ASN, whose output happened to satisfy the unwritten rules, converged in four cycles.

A post-hoc analysis found that roughly three-quarters of the sweep's findings were expressible as violations of rules that were never stated: one body per file, every reference resolves, yaml and markdown agree, every symbol cites its source, no cycles in the dependency graph. A mechanical validator checking those rules would have caught them before the first review cycle.

## Resolution

**Write the contract before producing output.** Every transition that introduces new structure specifies its output contract — what must hold for the output to be well-formed. The contract is a schema: concrete rules, mechanically checkable where possible.

**Build the validator from the contract.** The contract gives the validator its checklist. The validator runs at two points: immediately after the transition (catches transition bugs) and before each downstream sweep (catches drift from manual edits or earlier sweeps).

**Reference the contract in prompts.** The review and revise prompts for stages operating on the structured output name the contract's rules. The reviewer can flag root causes ("this body exists in two files") rather than symptoms ("this definition appears twice"). The reviser can check for canonical homes before inlining content.

The first instance is the blueprinting output contract, documented at [Claim File Contract](../design-notes/claim-file-contract.md). The operational pattern that runs the validator and applies fixes is [Validate Before Review](../patterns/validate-before-review.md); the design commitment behind it is the [Validation Principle](../principles/validation.md).

## Related

- [Representation Change](../patterns/representation-change.md) — the pattern this failure mode accompanies. Every representation change introduces a new form with new structural rules. Uncontracted Representation Change is what happens when the change is performed without specifying those rules.
- [Contract Sprawl](contract-sprawl.md), [Prose Sprawl](prose-sprawl.md), [Surface Expansion](surface-expansion.md) — gravitational content failures that compound alongside structural failures at the same site. Fixing content discipline does not fix missing contracts. Fixing contracts does not fix content discipline.
- [Self-Healing Areas](../design-notes/self-healing.md) — the mechanical signals from an uncontracted representation change (duplicate declarations, dangling references, metadata disagreement, dependency cycles) are self-healing candidates once the contract defines what to check.
- [The Coupling Principle](../principles/coupling.md) — addresses content health within a file. Uncontracted Representation Change addresses structural health across files. Neither subsumes the other.
- [The Validation Principle](../principles/validation.md) — the design commitment that preventing this failure mode falls under. Every representation must have a structural contract and validation before review.
- [Validate Before Review](../patterns/validate-before-review.md) — the operational pattern that resolves this failure mode once a contract exists. The validator checks the contract; per-invariant revise recipes fix the violations.