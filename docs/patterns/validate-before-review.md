# Validate Before Review

Structural violations should be resolved mechanically before semantic review begins. When an LLM reviewer sees structural violations, it reports them as textual symptoms and the reviser resolves them textually — creating new violations through add-bias that compound across cycles. Structural noise also drowns semantic findings when both compete for the reviewer's attention. Separating them makes the review cycle converge on what it's actually for.

## Forces

**Structural violations dominate early cycles.** When input state has unresolved structural violations, the majority of review findings are structural. The reviewer discovers them one per cycle, framed as textual observations. A mechanical validator discovers them all at once.

**Add-bias compounds structural fixes.** A reviewer reports "X defined twice." A reviser resolves it by inlining — creating a new violation while closing the reported one. Mechanical fix recipes resolve violations structurally (point to canonical home, delete duplicate, reconcile metadata) without the extend-by-default bias.

**Semantic review on broken state is wasted work.** A reviewer finding a genuine derivation gap in a file whose declaration is duplicated elsewhere produces a fix that may land in the wrong copy. Structural soundness is a precondition for semantic fixes to stick.

**The reviewer can't name what it's seeing.** A reviewer reading concatenated file content sees "ℕ⁺ defined twice" — a textual symptom. It cannot see "T4a's body exists in both T4.md and T4a.md" — the structural cause. The reviewer lacks the framing to distinguish a content error from a structural violation. A validator has exactly that framing because it checks against a contract.

## Signal

Signals the pattern is absent or being violated:

- A cone's review findings are predominantly structural (duplicates, dangling references, metadata disagreement) rather than semantic (derivation gaps, regime mismatches)
- The reviewer's findings are mechanically checkable — a script could verify each one without understanding the reasoning
- Cones oscillate or fail to converge despite findings being addressed each cycle
- The reviser's fixes for structural findings create new structural violations

## Structure

Two separate passes, different tools, different concerns:

1. **Validate-revise.** Mechanical validator checks the structural contract. Targeted fixes resolve violations. Repeats until clean.
2. **Review-revise.** LLM reviewer reads structurally sound state. Produces semantic findings. Reviser applies fixes. This is the existing review cycle, unchanged.

The boundary between them is clean: can a script check it without understanding the content? Validate-revise. Does checking it require reading the reasoning? Review-revise.

## Origin

Derived from ASN-0034's T4 sweep. Two cones ran eight cycles each without converging. Post-hoc analysis found three-quarters of findings were mechanically checkable structural violations. Separating structural validation from semantic review resolved the non-convergence by eliminating structural noise before the reviewer saw the state. The T1 cone on the same ASN — structurally sound input — converged in four cycles with semantic review alone.

## Related

- [The Validation Principle](../principles/validation.md) — the design commitment this pattern operationalizes.
- [The Coupling Principle](../principles/coupling.md) — the parallel principle for content health. Coupling monitors within-file health; validation monitors across-file health.
- [Representation Change](representation-change.md) — the pattern whose output this validates.
- [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md) — the failure mode when no contract exists to validate against. This pattern cannot operate without a contract.
- [Validate-Before-Review Implementation](../design-notes/validate-before-review.md) — how this pattern is implemented: the two-pass cycle, per-invariant fix recipes, and integration with the [claim convergence protocol](../protocols/claim-convergence-protocol.md).