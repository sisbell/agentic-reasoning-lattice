# Claim File Contract

The output contract for claim derivation. Specifies what well-formed per-claim files look like — what must be true when claim derivation finishes, and what must remain true across every review/revise cycle. The first instance of the transition-contract resolution for [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md).

Scope: this contract governs the per-claim outputs produced by the [claim derivation protocol](../protocols/claim-derivation-protocol.md). For each claim the protocol produces:

- a body markdown file `<label>.md` carrying the claim's prose, proof, and Formal Contract section,
- three sidecar markdown files — `<label>.label.md`, `<label>.name.md`, `<label>.description.md` — carrying the claim's substrate-managed attributes,
- substrate links classifying the body and pointing at the sidecars and at related claims (described below).

Other artifacts emitted at other stages — the foundation index, the signature aggregation, the `formal-statements.md` export — are separate representation changes with their own contracts. Don't bundle them.

## Two axes

Every invariant is classified along two axes:

**Enforcement.** Structural invariants are mechanically checkable without LLM interpretation — a validator enforces them. Semantic invariants require reading content and judging it — review enforces them. These are disjoint: if an invariant can be expressed as a structural check, it is one. If it requires judgment, it isn't. The whole point of the contract is to keep structural checks out of the review loop.

**Checkability window.** Steady-state invariants are verifiable from the output files plus the substrate alone; they must hold after every revise commit. Transition-checkable invariants require the source artifact (the pre-decomposition note) for comparison; they can only be verified at the moment of the transition. After the first revise, the source is no longer the authoritative comparison point — the committed output is.

## Transactional scope

Invariants apply to committed output, not to intermediate state. A revise that deletes a claim and then fixes its references has a transient broken state between the two operations. The validator does not see that state. It checks the working tree before commit, plus the substrate as of that commit. This matches database transaction semantics: constraints are checked at commit, not at each statement.

A revise is free to violate any invariant mid-step as long as the commit satisfies all of them.

## Authority

A claim's identity appears on three surfaces: the **filename stem** of its body markdown, the **content of its label sidecar** (`<label>.label.md`), and the **markdown bold declaration** in the body. When these disagree, the filename stem is authoritative. The label sidecar (invariant #4) and the bold declaration (invariant #2) must conform to the stem. Cross-claim references — substrate `citation` links, inline citations, exports — resolve against the filename stem.

Consequence: when a mismatch is found, the fix is to update the label sidecar or the markdown declaration, not the filename. Renaming a file cascades through every reference in the lattice; the other two are local.

## Structural invariants

### Steady-state — validator runs before every review cycle and after every revise commit

1. **File set completeness.** For every claim in the lattice, four required files exist: `<label>.md` (body), `<label>.label.md`, `<label>.name.md`, `<label>.description.md`. A fifth, optional sidecar `<label>.signature.md` exists for claims that introduce non-logical symbols (claims that define no new symbols have no signature sidecar). No orphan body without the required sidecars; no orphan required sidecar without a body. An orphan signature sidecar (no matching body) is a violation; a missing signature sidecar (claim with no introduced symbols) is not.

2. **Declaration matches label.** The markdown body contains exactly one bold claim-declaration of the form `**<Label> (<Name>).**`. The label-position equals the filename stem; the parenthetical equals the name sidecar's content (when label == name, the parenthetical repeats it — redundant but uniform). The parenthetical is required in all cases; this uniformity makes the declaration textually distinguishable from proof-narrative emphasis (e.g., `**Positivity.**`, `**Length.**`). Type keywords (*axiom*, *definition*, *design-requirement*, *lemma*, *theorem*, *corollary*) do not appear in the label-position — those are recorded as the substrate `contract.<kind>` classifier on the body.

3. **Sidecar content well-formed.** The label sidecar contains a single line equal to the filename stem. The name sidecar contains a single line in PascalCase. The description sidecar contains markdown prose summarizing the claim's purpose; non-empty, no required structure. The signature sidecar (when present) contains markdown bullets of the form ``- `<symbol>` — <meaning>``, one per symbol the claim introduces.

4. **Substrate classification complete.** For each claim's body markdown the substrate contains:
   - exactly one active `claim` classifier link with `to_set = [body_md]`,
   - exactly one active `contract.<kind>` classifier link with `to_set = [body_md]` and `kind ∈ {axiom, definition, theorem, corollary, lemma, consequence, design-requirement}`,
   - exactly one active `label` link with `from_set = [body_md], to_set = [<label>.label.md]`,
   - exactly one active `name` link with `from_set = [body_md], to_set = [<label>.name.md]`,
   - exactly one active `description` link with `from_set = [body_md], to_set = [<label>.description.md]`,
   - exactly one active `signature` link with `from_set = [body_md], to_set = [<label>.signature.md]` *if* the claim introduces non-logical symbols (the sidecar exists). Claims with no introduced symbols have no signature link.

5. **Depends agreement.** The set of substrate `citation` links sourced from the claim's body markdown and the set of claim labels named in the body's Formal Contract Depends section name the same set of claims. No additions or omissions in either surface.

6. **References resolve.** Every claim named in a substrate `citation` link's `to_set`, in an inline body citation, or in a Formal Contract Depends section exists as a complete file set in the lattice (per #1) and carries the substrate classification (per #4).

7. **Declared symbols resolve.** Every tracked symbol used in a claim's Formal Contract structural fields (Axiom, Definition, Preconditions, Postconditions, Invariant, Frame) must resolve, via the claim's transitive citation closure, to an owning claim — or be a primitive. The v1 implementation uses a curated symbol-owners table (`lattices/<lattice>/symbol-owners.yaml`) mapping tracked symbols to their owning claim labels; symbols not in the table are ignored (false-negative tolerant; false-positive intolerant).

8. **Acyclic dependency graph.** The substrate `citation` relation across all claim bodies in the lattice is a DAG.

9. **Body uniqueness.** A given claim's body (bold declaration, proof, formal contract) appears in exactly one file — the body markdown whose filename stem matches the claim. No claim's body is inlined into another claim's file.

### Transition-checkable — validator runs once, at the end of claim derivation

10. **Source coverage.** Every claim in the source note produces exactly one file set. No source claim is dropped; no source claim is duplicated into multiple file sets.

11. **No orphan output.** Every file set in the output corresponds to a claim in the source note. Claim derivation does not invent claims.

12. **Content preservation (substring at transclude exit).** At the conclusion of the transclude phase, each claim's body markdown is a byte-substring of its source note (modulo trailing whitespace). This is the simulated-transclusion guarantee at file-level substrate; under tumbler-substrate it becomes structural via VStream spans. Subsequent phases (produce_contract, validate-revise) intentionally diverge the body — produce_contract appends Formal Contract sections; validate-revise heals structural form. The substring property is **transition-checkable at transclude exit only**, not at derivation exit. The transclude commit captures the byte-aligned state in git history.

13. **Provenance recording.** For each claim emitted, the substrate contains exactly one active `provenance.derivation` link with `from_set = [source_note_md], to_set = [body_md]`. The link records that this claim was derived from this note at this stage; it persists permanently regardless of subsequent edits to the body.

## Semantic invariants — review enforces, not validator

These are established at claim derivation and must be preserved by authoring discipline. They surface as review findings when violated, not as validator errors.

S1. **Description matches body.** The description sidecar describes what the body claims. Not a restatement of the formal contract; not stale after a revise changes the body.

S2. **Exterior matches interior.** The claim's stated postconditions are delivered by its proof. Its preconditions are sufficient for the proof to proceed and do not exceed what callers must supply.

S3. **Symbol usage matches declaration.** A symbol declared with a given meaning in the signature is used consistently with that declaration throughout the proof. (The validator can check that the declaration exists and resolves; only review can check that the usage respects the declared meaning.)

## Enforcement sites

Three points where the contract is checked:

- **End of claim derivation.** Validator runs all structural invariants (steady-state and transition-checkable). Catches decomposition bugs before they become inherited state downstream.
- **Before each review cycle.** Validator runs steady-state structural invariants only. Catches drift introduced by prior revise commits, manual edits, or foundation rebases. Runs before the reviewer so the reviewer does not spend cycles on mechanically-detectable symptoms.
- **During review.** Reviewer checks semantic invariants as part of its normal operation. Validator does not touch these.

Running the validator before the reviewer eliminates the reviewer's work on mechanically-detectable symptoms and prevents the add-bias that tempts a reviser to extend rather than restructure.

## What this contract does not cover

- The content of individual claims — what makes a proof correct, a description accurate, a precondition sufficient. That is review's job.
- Artifacts other than per-claim file sets and their substrate classification. The foundation index, signature aggregation, and formal-statements export each need their own contracts written at the representation changes that produce them.
- Aesthetic or stylistic conventions (e.g., prose length, header formatting). Not invariants — conventions.

## Related

- [The Validation Principle](../principles/validation.md) — the design commitment this contract serves. The principle requires every representation to have a structural contract; this contract is the first instance.
- [Validate Before Review](../patterns/validate-before-review.md) — the operational pattern that consumes this contract. Its validator runs the contract's structural invariants; its per-invariant revise recipes address the violations it finds.
- [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md) — the failure mode this contract addresses. The T4 sweep's non-convergence was a concrete instance: sixteen cycles spent on symptoms of structural violations because no contract specified what well-formed per-claim output meant.
- [Representation Change](../patterns/representation-change.md) — the pattern this contract's existence is a consequence of. Every representation change introduces new structural rules; this contract is the first such rule set written down.
- [Claim Derivation Protocol](../protocols/claim-derivation-protocol.md) — the protocol whose output this contract governs.
- [Claim Derivation](../claim-derivation.md) — the narrative guide for the stage.
- [Self-Healing Areas](self-healing.md) — the steady-state structural invariants here are the mechanical-signal self-healing candidates named in that map.
