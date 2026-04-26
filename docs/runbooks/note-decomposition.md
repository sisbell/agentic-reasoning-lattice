# Runbook: Note Decomposition

*Updated 2026-04-12.*

## Prerequisites

- note has converged through discovery (CONVERGED verdict)
- Working tree is clean (`git status`)
- Upstream dependencies are formalized

## Steps

### 1. Run the full pipeline

```bash
python scripts/blueprint.py <ASN>
```

This runs the entire blueprinting pipeline to completion (decompose → enrich → disassemble → validate), auto-committing each stage.

### 2. Check validation

Validate runs automatically at the end. Must report PASS before promoting.

### 3. Promote to formalization

```bash
python scripts/promote-blueprint.py <ASN>
```

### 4. Individual re-runs (if needed)

```bash
python scripts/decompose.py <ASN>
python scripts/enrich.py <ASN>
python scripts/disassemble.py <ASN>
python scripts/disassemble.py <ASN> --dry-run
python scripts/validate.py <ASN>
```

---

See the [note decomposition guide](../guides/note-decomposition.md) for how the pipeline stages work, output structure, and design decisions.
