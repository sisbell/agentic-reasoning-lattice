# Representation Change

## Pattern

The same content must serve different processes. Each process needs the content in a specific form — narrative for reasoning, structured metadata for automation, formal contracts for verification, executable code for mechanical checking. The content doesn't change. The representation does.

Direct jumps between distant representations fail. Narrative cannot become Dafny in one step — the gap is too large for any agent to bridge reliably. Progressive representation change makes each step tractable: narrative → structured → formal → mechanical. Each transformation is small enough to verify.

## Forces

- **Each process has input requirements.** Discovery produces narrative. Claim convergence needs per-claim files with metadata. Modeling needs formal contracts. Verification needs executable code. No single representation serves all processes.
- **Content is preserved.** The claim "content once stored is never modified" is the same claim at every stage. What changes is how it's expressed — as a sentence in a paragraph, as a YAML entry with label S0, as a formal contract with preconditions and postconditions, as a Dafny method with assertions.
- **Large jumps fail.** Asking an agent to go from narrative prose to verified Dafny in one step produces unreliable results. Too many decisions at once — decomposition, classification, convergence, and translation all conflated.
- **Small steps are verifiable.** Each representation change can be checked: does the structured version capture what the narrative said? Does the formal contract match the proof? Does the Dafny code implement the contract? Each step has clear acceptance criteria.

## Structure

```
narrative prose (discovery output)
  │
  representation change: decompose + structure
  │
per-claim YAML + markdown (claim derivation output)
  │
  representation change: converge
  │
formal contracts with preconditions/postconditions (claim convergence output)
  │
  representation change: translate
  │
Dafny/Alloy code (verification output)
```

Each arrow is a representation change. The content at the top and bottom is the same claim. The form makes it progressively more precise and more mechanically checkable.

## Composition: Claim derivation

Claim derivation is [scope narrowing](scope-narrowing.md) + representation change applied together.

**Scope narrowing**: a monolithic note is decomposed into individual claims. Each claim becomes an independently addressable unit.

**Representation change**: narrative prose becomes structured metadata (YAML) + body (markdown). The narrative stays in the body for human readers. The metadata makes the formal structure explicit — label, type, dependencies, vocabulary.

Neither alone is sufficient. Scope narrowing without representation change gives you 29 sections of narrative — still not convergable. Representation change without scope narrowing tries to structure a 15-page document at once — too much for any agent to handle reliably.

Together they produce what claim convergence needs: small, structured, independently addressable units.

## Applications

### Discovery → claim derivation

Narrative prose → per-claim YAML/MD pairs. The largest representation gap in the system. Handled by progressive decomposition: mechanical section split → per-section claim identification → per-claim classification and enrichment → disassembly into file pairs → validation. See the [claim derivation module](../modules/claim-derivation-module.md) for the formal specification.

### Claim convergence → verification

Formal contracts → Dafny/Alloy code. The contracts specify preconditions, postconditions, invariants. Translation maps these to executable assertions. The representation change is mechanical enough that contract accuracy determines code correctness.

### Assembly → export

Per-claim files → formal-statements.md export. The representation change goes in the opposite direction — from detailed per-claim files to trimmed summaries for downstream consumers. Content is reduced but the formal content is preserved.

### Review/revise within a representation

Each [review/revise iteration](review-revise-iteration.md) cycle operates within a single representation. The [convergence protocol](../protocols/convergence-protocol.md) drives review/revise on a stable representation — changes happen within the representation, not between representations. Note convergence refines notes. Claim convergence refines per-claim files. The representation is stable during convergence.

## Relationship to other patterns

[Scope narrowing](scope-narrowing.md) — representation change is a tool that scope narrowing reaches for when the current form doesn't support finer granularity. You can't narrow a narrative document into claims without changing its representation to structured files. Narrowing decides WHAT to focus on. Representation change provides the form that makes the focus possible. Not all narrowing requires representation change — cone-scoped review narrows to a cluster without changing form.

[Narrow → Refine → Verify](narrow-refine-verify.md) — representation change serves the primary cycle but is not a phase within it. It happens when needed: before narrowing (claim derivation), after narrowing (extract/absorb), between refinement stages (claim convergence → verification). Refinement operates within a single representation — the representation is stable during the review/revise loop.

[Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md) — the failure mode when a representation change is performed without specifying what well-formed output means at the new representation. Each arrow in the structure above carries implicit validity rules; the failure occurs when those rules stay implicit. The [Claim Document Contract](../design-notes/claim-document-contract.md) is the first instance of making those rules explicit.

## Origin

Present from the start — the system has always been discovery → claim derivation → claim convergence → verification, each stage producing a different representation of the same content. The pattern was implicit in the protocol architecture. It became explicit when claim derivation was redesigned from a single-pass LLM rewrite to progressive decomposition — the recognition that representation change must happen in small, verifiable steps, not in one large jump.