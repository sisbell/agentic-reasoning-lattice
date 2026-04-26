# The Validation Principle

Every representation the system operates on has a structural contract, and no LLM review cycle operates on state whose contract has not been mechanically verified. Structural integrity is a precondition for meaningful review — not a thing review checks, but a thing that must hold before review begins.

## Why

Review cycles are expensive and subject to add-bias. When a reviewer encounters a structural violation — a duplicated declaration, a dangling reference, a metadata disagreement — it reports it as a textual finding. The reviser resolves the finding textually, often by extending content rather than restructuring. Each textual fix adds surface. Each added surface attracts new findings next cycle. The cone grows without converging, not because the reasoning is wrong, but because the structure is broken and the review cycle is the wrong tool to fix it.

Mechanical validation is cheap, exhaustive, and free of add-bias. A validator that checks "one body per file" catches every duplication in one pass. A reviewer that checks the same thing catches one duplication per cycle, framed as "X defined twice," and the reviser may resolve it by inlining — creating a new violation while fixing the reported one.

The principle: get structural issues out of the reviewer's path. The reviewer's job is finding semantic issues — derivation gaps, regime mismatches, smuggled postulates, missing consequences. That job cannot begin productively until the state the reviewer reads is structurally sound.

## The parallel with coupling and voice

The [Coupling Principle](coupling.md) governs content health within a file. Prose and formal content are authored as a pair; their ratio signals whether the file is healthy. Divergence signals sprawl.

The Validation Principle governs structural health across files. Each representation has a contract; mechanical checks signal whether the structure is sound. Violations signal that the representation change was uncontracted or that subsequent operations broke invariants.

The [Voice Principle](voice.md) governs output quality of LLM agents. Positive style structure constrains the reviser to load-bearing prose by construction. Where validation uses enumeration (a closed set of mechanically checkable rules), voice uses positive structure (an open set that can't be enumerated). Validation is the case where enumeration works — structural invariants are finite and checkable. Voice is the case where it doesn't — prose quality is open-ended and judgment-based. The two principles use different mechanisms because they govern different kinds of constraint.

No principle subsumes another. A claim file can have perfect coupling (70/30, no sprawl), perfect structure (all invariants hold), and still contain reviser-drift prose that voice discipline would have prevented. The reviewer needs all three axes clean to do its real work.

| | Coupling | Validation | Voice |
|---|---|---|---|
| Scope | Within a file | Across files | LLM output quality |
| What it monitors | Prose:formal ratio | Structural invariants | Prose form |
| How it's checked | Ratio computation | Mechanical validator | Positive style structure |
| Mechanism | Monitoring | Enumeration (closed set) | Definition (open set) |
| Failure mode when absent | [Surface Expansion](../equilibrium/surface-expansion.md) | [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md) | [Prose Sprawl](../equilibrium/prose-sprawl.md) via add-bias |
| What the reviewer sees when it fails | Meta-prose noise | Structural noise | Reviser drift |

## The contract

Each representation's structural contract specifies what well-formed state looks like at that representation. The contract is a schema — concrete rules, mechanically checkable. The first instance is the [Claim File Contract](../design-notes/claim-file-contract.md), which specifies valid per-claim file state after note decomposition.

Contracts have two classes of rule:

**Structural invariants** — mechanically checkable by the validator. One body per file. Filename matches label. References resolve. Metadata agrees across representations. No dependency cycles. These are the validator's checklist.

**Semantic invariants** — checked by review, not by the validator. Summary matches body. Postconditions match what the proof establishes. Symbol usage in proofs matches declarations. These stay in the reviewer's domain.

The validation principle governs the first class. The second class is the reviewer's job — the job the principle exists to protect.

## Enforcement

The principle is enforced operationally through the [validate-before-review](../patterns/validate-before-review.md) pattern: a mechanical validation pass runs before each review cycle, catches and fixes structural violations, and hands the reviewer structurally sound state. The reviewer never sees structural noise. The validation cycle and the review cycle are separate passes with separate tools, separate prompts, and separate concerns.

## Empirical basis

ASN-0034's T4 sweep ran sixteen review cycles across two cones without converging. Post-hoc analysis found that roughly three-quarters of the findings were expressible as structural invariant violations — duplicate declarations, dangling references, metadata disagreement, symbol use without cited source, dependency cycles. These were mechanically checkable. The review cycle spent sixteen rounds doing a validator's job, at LLM cost, with add-bias compounding at each cycle.

The T1 cone on the same ASN — whose state happened to satisfy the structural invariants — converged in four cycles. The difference was not review quality. The difference was structural soundness of the input.

## Related

- [Coupling Principle](coupling.md) — the parallel principle for content health within files.
- [Voice Principle](voice.md) — the parallel principle for LLM output quality. Validation uses enumeration (structural invariants are a closed set). Voice uses positive structure (prose quality is an open set). The two principles use different mechanisms because they govern different kinds of constraint.
- [Validate-Before-Review](../patterns/validate-before-review.md) — the operational pattern that enforces this principle.
- [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md) — the failure mode when a representation has no contract to validate against.
- [Claim File Contract](../design-notes/claim-file-contract.md) — the first instance of a structural contract.