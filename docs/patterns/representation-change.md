# Representation Change

## Pattern

The same content must serve different processes. Each process needs the content in a specific form — narrative for reasoning, structured metadata for automation, formal contracts for verification, executable code for mechanical checking. The content doesn't change. The representation does.

Direct jumps between distant representations fail. Narrative cannot become Dafny in one step — the gap is too large for any agent to bridge reliably. Progressive representation change makes each step tractable: narrative → structured → formal → mechanical. Each transformation is small enough to verify.

## Forces

- **Each process has input requirements.** Discovery produces narrative. Formalization needs per-property files with metadata. Modeling needs formal contracts. Verification needs executable code. No single representation serves all processes.
- **Content is preserved.** The property "content once stored is never modified" is the same claim at every stage. What changes is how it's expressed — as a sentence in a paragraph, as a YAML entry with label S0, as a formal contract with preconditions and postconditions, as a Dafny method with assertions.
- **Large jumps fail.** Asking an agent to go from narrative prose to verified Dafny in one step produces unreliable results. Too many decisions at once — decomposition, classification, formalization, and translation all conflated.
- **Small steps are verifiable.** Each representation change can be checked: does the structured version capture what the narrative said? Does the formal contract match the proof? Does the Dafny code implement the contract? Each step has clear acceptance criteria.

## Structure

```
narrative prose (discovery output)
  │
  representation change: decompose + structure
  │
per-property YAML + markdown (blueprinting output)
  │
  representation change: formalize
  │
formal contracts with preconditions/postconditions (formalization output)
  │
  representation change: translate
  │
Dafny/Alloy code (modeling output)
```

Each arrow is a representation change. The content at the top and bottom is the same claim. The form makes it progressively more precise and more mechanically checkable.

## Composition: Blueprinting

Blueprinting is [scope narrowing](scope-narrowing.md) + representation change applied together.

**Scope narrowing**: a monolithic reasoning document is decomposed into individual properties. Each property becomes an independently addressable unit.

**Representation change**: narrative prose becomes structured metadata (YAML) + body (markdown). The narrative stays in the body for human readers. The metadata makes the formal structure explicit — label, type, dependencies, vocabulary.

Neither alone is sufficient. Scope narrowing without representation change gives you 29 sections of narrative — still not formalizable. Representation change without scope narrowing tries to structure a 15-page document at once — too much for any agent to handle reliably.

Together they produce what formalization needs: small, structured, independently addressable units.

## Applications

### Discovery → blueprinting

Narrative prose → per-property YAML/MD pairs. The largest representation gap in the pipeline. Handled by progressive decomposition: mechanical section split → per-section property identification → per-property classification and enrichment → disassembly into file pairs → validation.

### Formalization → modeling

Formal contracts → Dafny/Alloy code. The contracts specify preconditions, postconditions, invariants. Translation maps these to executable assertions. The representation change is mechanical enough that contract accuracy determines code correctness.

### Assembly → export

Per-property files → formal-statements.md export. The representation change goes in the opposite direction — from detailed per-property files to trimmed summaries for downstream consumers. Content is reduced but the formal content is preserved.

### Review/revise within a representation

Each [review/revise iteration](review-revise-iteration.md) cycle operates within a single representation. Local review works on markdown. Contract review works on formal contracts. Dafny verification works on code. The representation is stable during refinement — changes within the representation, not between representations.

## Relationship to other patterns

[Scope narrowing](scope-narrowing.md) — representation change is a tool that scope narrowing reaches for when the current form doesn't support finer granularity. You can't narrow a narrative document into properties without changing its representation to structured files. Narrowing decides WHAT to focus on. Representation change provides the form that makes the focus possible. Not all narrowing requires representation change — regional review narrows to a cluster without changing form.

[Narrow → Refine → Verify](narrow-refine-verify.md) — representation change serves the primary cycle but is not a phase within it. It happens when needed: before narrowing (blueprinting), after narrowing (extract/absorb), between refinement stages (formalization → modeling). Refinement operates within a single representation — the representation is stable during the review/revise loop.

## Origin

Present from the start — the pipeline has always been discovery → blueprinting → formalization → modeling, each stage producing a different representation of the same content. The pattern was implicit in the pipeline design. It became explicit when blueprinting was redesigned from a single-pass LLM rewrite to progressive decomposition — the recognition that representation change must happen in small, verifiable steps, not in one large jump.
