# The Validation Principle

Every representation the system operates on must have a structural contract, and no LLM review cycle operates on state whose contract has not been mechanically verified. Structural integrity is a precondition for meaningful review — not a thing review checks, but a thing that must hold before review begins.

## Why

Review cycles are expensive and subject to add-bias. When a reviewer encounters a structural violation — a duplicated declaration, a dangling reference, a metadata disagreement — it reports it as a textual finding. The reviser resolves the finding textually, often by extending content rather than restructuring. Each textual fix adds surface. Each added surface attracts new findings next cycle. The cone grows without converging, not because the reasoning is wrong, but because the structure is broken and the review cycle is the wrong tool to fix it.

Mechanical validation is cheap, exhaustive, and free of add-bias. A validator that checks "one body per file" catches every duplication in one pass. A reviewer that checks the same thing catches one duplication per cycle, framed as "X defined twice," and the reviser may resolve it by inlining — creating a new violation while fixing the reported one.

The principle: get structural issues out of the reviewer's path. The reviewer's job is finding semantic issues — derivation gaps, regime mismatches, smuggled postulates, missing consequences. That job cannot begin productively until the state the reviewer reads is structurally sound.

## The parallel with coupling

The [Coupling Principle](coupling.md) governs content health within a file. Prose and formal content are authored as a pair; their ratio signals whether the file is healthy. Divergence signals sprawl.

The Validation Principle governs structural health across files. Each representation has a contract; mechanical checks signal whether the structure is sound. Violations signal that the representation change was uncontracted or that subsequent operations broke invariants.

Neither subsumes the other. A claim file can have perfect coupling (70/30, no sprawl) while the ASN as a whole has broken structure (that same claim's body duplicated in three files). A structurally perfect ASN can have severe coupling violations within individual files. The reviewer needs both axes clean to do its real work.

| | Coupling | Validation |
|---|---|---|
| Scope | Within a file | Across files |
| What it monitors | Prose:formal ratio | Structural invariants |
| How it's checked | Ratio computation | Mechanical validator |
| Failure mode when absent | [Surface Expansion](../equilibrium/surface-expansion.md) | [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md) |
| What the reviewer sees when it fails | Meta-prose noise | Structural noise |

## The contract

Each representation's structural contract specifies what well-formed state looks like at that representation. The contract is a schema — concrete rules, mechanically checkable. The first instance is the [Claim File Contract](../design-notes/claim-file-contract.md), which specifies valid per-claim file state after blueprinting.

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
- [Validate-Before-Review](../patterns/validate-before-review.md) — the operational pattern that enforces this principle.
- [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md) — the failure mode when a representation has no contract to validate against.
- [Claim File Contract](../design-notes/claim-file-contract.md) — the first instance of a structural contract.