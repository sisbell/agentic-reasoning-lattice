# Claim File Contract

The output contract for blueprinting. Specifies what well-formed per-claim files look like — what must be true when blueprinting finishes, and what must remain true across every review/revise cycle. The first instance of the transition-contract resolution for [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md).

Scope: this contract governs the per-claim `{label}.yaml` and `{label}.md` file pairs produced by blueprinting. Other artifacts emitted at other stages — the foundation index, the vocabulary aggregation, the `formal-statements.md` export — are separate representation changes with their own contracts. Don't bundle them.

## Two axes

Every invariant is classified along two axes:

**Enforcement.** Structural invariants are mechanically checkable without LLM interpretation — a validator enforces them. Semantic invariants require reading content and judging it — review enforces them. These are disjoint: if an invariant can be expressed as a structural check, it is one. If it requires judgment, it isn't. The whole point of the contract is to keep structural checks out of the review loop.

**Checkability window.** Steady-state invariants are verifiable from the output files alone; they must hold after every revise commit. Transition-checkable invariants require the source artifact (the pre-blueprinting ASN) for comparison; they can only be verified at the moment of the transition. After the first revise, the source is no longer the authoritative comparison point — the committed output is.

## Transactional scope

Invariants apply to committed output, not to intermediate state. A revise that deletes a claim and then fixes its references has a transient broken state between the two operations. The validator does not see that state. It checks the working tree before commit. This matches database transaction semantics: constraints are checked at commit, not at each statement.

A revise is free to violate any invariant mid-step as long as the commit satisfies all of them.

## Authority

A claim's identity appears on three surfaces: the yaml `label` field, the file's stem, and the markdown bold declaration. When these disagree, the yaml `label` is authoritative. Filename (invariant #2) and markdown declaration (invariant #3) must conform to yaml `label`. Cross-file references — `depends` entries, inline citations, exports — resolve against the yaml `label`.

Consequence: when a mismatch is found, the fix is to change the filename or the markdown declaration, not the yaml `label`. Relabeling cascades through every reference in the lattice; the other two are local.

## Structural invariants

### Steady-state — validator runs before every review cycle and after every revise commit

1. **File pair completeness.** For every label in the lattice, both `{label}.yaml` and `{label}.md` exist. No orphan yaml without a body, no orphan body without metadata.

2. **Filename matches label.** The yaml `label` field equals the file's stem. `T4a.yaml` declares `label: T4a`.

3. **Declaration matches label.** The markdown body contains exactly one bold claim-declaration of the form `**<Label> (<Name>).**`. The label-position equals the yaml `label` field; the parenthetical equals the yaml `name` field (when `label == name`, the parenthetical repeats it — redundant but uniform). The parenthetical is required in all cases; this uniformity makes the declaration textually distinguishable from proof-narrative emphasis (e.g., `**Positivity.**`, `**Length.**`). Type keywords (*axiom*, *definition*, *design-requirement*, *lemma*, *theorem*, *corollary*) do not appear in the label-position — those live in the yaml `type` field.

4. **YAML well-formed.** Parses as YAML. Required fields present (`label`, `name`, `type`, `summary`, `depends`). Types as declared in the blueprinting schema.

5. **Depends agreement.** The yaml `depends:` list and the markdown Formal Contract Depends section name the same set of claims. No additions or omissions in either surface.

6. **References resolve.** Every claim named in a `depends` list, a citation, or a Formal Contract Depends section exists as a file pair in the lattice.

7. **Declared symbols resolve.** Every symbol declared in a claim's yaml `vocabulary` field either (a) originates in this claim or (b) originates in a claim reachable through the transitive `depends` closure. No symbol use with an undeclared or unreachable source.

8. **Acyclic dependency graph.** The `depends` relation across all file pairs in the lattice is a DAG.

9. **Body uniqueness.** A given claim's body (bold declaration, proof, formal contract) appears in exactly one file — the file whose label matches the claim. No claim's body is inlined into another claim's file.

### Transition-checkable — validator runs once, at the end of blueprinting

10. **Source coverage.** Every claim in the source ASN produces exactly one file pair. No source claim is dropped; no source claim is duplicated into multiple pairs.

11. **No orphan output.** Every file pair in the output corresponds to a claim in the source ASN. Blueprinting does not invent claims.

12. **Content preservation.** Each source claim's narrative, proof, and formal contract text appears — substantively, not necessarily byte-identically — in its corresponding file pair. A mechanical version of this check: the output file pair's non-boilerplate text is non-empty and contains the claim's summary terms. Anything stronger is a semantic check and belongs to review.

## Semantic invariants — review enforces, not validator

These are established at blueprinting and must be preserved by authoring discipline. They surface as review findings when violated, not as validator errors.

S1. **Summary matches body.** The yaml `summary` describes what the `.md` body claims. Not a restatement of the formal contract; not stale after a revise changes the body.

S2. **Exterior matches interior.** The claim's stated postconditions are delivered by its proof. Its preconditions are sufficient for the proof to proceed and do not exceed what callers must supply.

S3. **Symbol usage matches declaration.** A symbol declared with a given signature or meaning in the vocabulary is used consistently with that declaration throughout the proof. (The validator can check that the declaration exists and resolves; only review can check that the usage respects the declared meaning.)

## Enforcement sites

Three points where the contract is checked:

- **End of blueprinting.** Validator runs all structural invariants (steady-state and transition-checkable). Catches blueprinting bugs before they become inherited state downstream.
- **Before each review cycle.** Validator runs steady-state structural invariants only. Catches drift introduced by prior revise commits, manual edits, or foundation rebases. Runs before the reviewer so the reviewer does not spend cycles on mechanically-detectable symptoms.
- **During review.** Reviewer checks semantic invariants as part of its normal operation. Validator does not touch these.

Running the validator before the reviewer eliminates the reviewer's work on mechanically-detectable symptoms and prevents the add-bias that tempts a reviser to extend rather than restructure.

## What this contract does not cover

- The content of individual claims — what makes a proof correct, a summary accurate, a precondition sufficient. That is review's job.
- Artifacts other than per-claim file pairs. The foundation index, vocabulary aggregation, and formal-statements export each need their own contracts written at the representation changes that produce them.
- Aesthetic or stylistic conventions (e.g., prose length, header formatting). Not invariants — conventions.

## Related

- [The Validation Principle](../principles/validation.md) — the design commitment this contract serves. The principle requires every representation to have a structural contract; this contract is the first instance.
- [Validate Before Review](../patterns/validate-before-review.md) — the operational pattern that consumes this contract. Its validator runs the contract's structural invariants; its per-invariant revise recipes address the violations it finds.
- [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md) — the failure mode this contract addresses. The T4 sweep's non-convergence was a concrete instance: sixteen cycles spent on symptoms of structural violations because no contract specified what well-formed per-claim output meant.
- [Representation Change](../patterns/representation-change.md) — the pattern this contract's existence is a consequence of. Every representation change introduces new structural rules; this contract is the first such rule set written down.
- [Blueprinting guide](../guides/blueprinting.md) — the stage whose output this contract governs.
- [Self-Healing Areas](self-healing.md) — the steady-state structural invariants here are the mechanical-signal self-healing candidates named in that map.
