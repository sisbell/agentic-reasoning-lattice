# Runbook: Blueprinting an ASN

*Rebuilt 2026-04-12 for the YAML-based pipeline.*

## Prerequisites

- ASN has converged through discovery (review/revise cycles, CONVERGED verdict)
- Working tree is clean (`git status`)
- Upstream dependencies are formalized (check `depends` in project.yaml)

## Quick Start

```bash
python scripts/blueprint.py <ASN>
```

Runs the full pipeline: decompose → enrich → disassemble → validate. Each stage auto-commits. Takes ~3-4 minutes (LLM calls in decompose and enrich).

After completion, promote to formalization:

```bash
python scripts/promote-blueprint.py <ASN>
```

## Pipeline Stages

### 1. Decompose

```bash
python scripts/decompose.py <ASN>
```

> **Decision point:** None — trust the output.

Two phases:
1. **Mechanical `##` split** — splits the ASN at section headers. Pure python, no LLM.
2. **Per-section LLM analysis** — Sonnet reads each section, produces a YAML file identifying properties (label, name, body). Runs in parallel.

Structural sections (preamble, property table, worked example, open questions) are skipped from LLM analysis — they're already clean from the split.

**Output:** `vault/2-blueprints/ASN-NNNN/sections/` — paired `.md` + `.yaml` files per section.

**Auto-commits** with hint `decompose`.

### 2. Enrich

```bash
python scripts/enrich.py <ASN>
```

> **Decision point:** None — trust the output.

Three per-property LLM passes, each running all properties in parallel:

1. **Type** — axiom, definition, design-requirement, lemma, theorem, corollary
2. **Dependencies** — property labels referenced in proof/justification
3. **Vocabulary** — notation this property introduces

Updates the section YAML files in place.

**Auto-commits** with hint `enrich`.

### 3. Disassemble

```bash
python scripts/disassemble.py <ASN>
```

> **Decision point:** None — mechanical.

Reads section YAMLs, writes per-property file pairs:
- `{label}.yaml` — metadata (label, name, type, depends, vocabulary)
- `{label}.md` — body text (statement + justification + proof + formal contract if present)

Also writes structural files with `_` prefix: `_preamble.md`, `_worked-example.md`, `_open-questions.md`, etc.

**Output:** `vault/2-blueprints/ASN-NNNN/properties/`

**Auto-commits** with hint `disassemble`.

### 4. Validate

```bash
python scripts/validate.py <ASN>
```

> **Decision point:** Must PASS before promoting.

Mechanical checks (no LLM):
- Every `.yaml` has a matching `.md` and vice versa
- Required fields present (label, name, type, depends)
- Valid type enum
- No duplicate labels
- YAML parses cleanly
- Body files not empty

Reports PASS/FAIL with details.

### 5. Promote to Formalization

```bash
python scripts/promote-blueprint.py <ASN>
```

> **Decision point:** None — mechanical copy.

Copies per-property `.yaml` + `.md` pairs and structural `_*.md` files to `vault/3-formalization/ASN-NNNN/`.

**Auto-commits** with hint `promote-blueprint`.

## Running Individual Steps

Each stage can be run independently for debugging or re-runs:

```bash
python scripts/decompose.py 36         # re-run decompose only
python scripts/enrich.py 36            # re-run enrich only
python scripts/disassemble.py 36       # re-run disassemble only
python scripts/disassemble.py 36 --dry-run  # preview without writing
python scripts/validate.py 36          # check consistency
```

## Output Structure

```
vault/2-blueprints/ASN-NNNN/
  source.md                          ← copy of the ASN
  sections/
    00-preamble.md                   ← mechanical split
    01-two-components-of-state.md
    01-two-components-of-state.yaml  ← LLM structural analysis + enrichment
    ...
  properties/
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
