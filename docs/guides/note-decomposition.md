# Guide: Note Decomposition

*Updated 2026-04-12.*

## Overview

Blueprinting transforms a monolithic note into per-claim file pairs (`.yaml` metadata + `.md` body) ready for formalization. The process runs: decompose → enrich → disassemble → validate → promote.

## Stages

### Decompose

Two phases:

1. **Mechanical `##` split** — splits the note at section headers. Pure python, no LLM. Each `##` section becomes its own `.md` file in `lattices/xanadu/blueprinting/ASN-NNNN/sections/`.

2. **Per-section LLM analysis** — Sonnet reads each section, produces a `.yaml` file identifying the claims within it (label, name, body). Runs in parallel across sections.

Structural sections (preamble, claim table, worked example, open questions) are skipped from LLM analysis — they're written as `.md` only.

### Enrich

Three per-claim LLM passes, each running all claims in parallel:

1. **Type** — classifies each claim: axiom, definition, design-requirement, lemma, theorem, corollary. Uses Dijkstra-school reasoning to determine if a proof is present, if the claim is a postulate, etc.

2. **Dependencies** — extracts claim labels directly referenced in the proof or design justification. Add-only — lists what the claim uses, not transitive dependencies.

3. **Vocabulary** — identifies notation this claim introduces (not uses). Distinguishes definitions from usages.

Each pass has its own focused prompt. Updates the section YAML files in place.

### Disassemble

Mechanical step — reads section YAMLs, writes per-claim file pairs:

- `{label}.yaml` — metadata only (label, name, type, depends, vocabulary)
- `{label}.md` — body text (statement + justification + proof + formal contract if present)

Filenames are derived from labels mechanically (strip parens, replace spaces/commas). Each YAML contains the original label for reverse lookup.

Structural sections become `_` prefixed files: `_preamble.md`, `_worked-example.md`, etc.

### Validate

Mechanical checks (no LLM):

- Every `.yaml` has a matching `.md` and vice versa
- Required fields present (label, name, type, depends)
- Valid type enum
- No duplicate labels
- YAML parses cleanly
- Body files not empty

Reports PASS/FAIL with details.

### Promote

Copies per-claim `.yaml` + `.md` pairs and structural `_*.md` files from `lattices/xanadu/blueprinting/ASN-NNNN/claims/` to `lattices/xanadu/claim-convergence/ASN-NNNN/`.

## Output Structure

```
lattices/xanadu/blueprinting/ASN-NNNN/
  source.md                          ← copy of the note
  sections/
    00-preamble.md                   ← mechanical split
    01-two-components-of-state.md
    01-two-components-of-state.yaml  ← LLM structural analysis + enrichment
    ...
  claims/
    S0.yaml                          ← metadata
    S0.md                            ← body
    S1.yaml
    S1.md
    Σ.C.yaml
    Σ.C.md
    _preamble.md                     ← structural (no YAML pair)
    _worked-example.md
    _open-questions.md
```

## YAML Metadata Format

```yaml
label: S7
name: StructuralAttribution
type: theorem
depends:
  - S7a
  - S7b
  - S0
  - S4
  - T3
  - T4
vocabulary:
  - symbol: "origin(a)"
    meaning: "document-level prefix of I-address a"
literature_citations:
  - "LM 2/48"
```

- **label** — stable key, never changes. Used for filenames and cross-references.
- **name** — PascalCase. Can change during formalization.
- **type** — classification. Set during enrich, not modified by formalization.
- **depends** — direct dependencies only. Add-only during formalization.
- **vocabulary** — symbols introduced by this claim.
- **literature_citations** — external references (e.g., Nelson's Literary Machines).

