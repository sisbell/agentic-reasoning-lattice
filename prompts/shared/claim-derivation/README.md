# Pipeline

## Blueprinting

Prepare a monolithic ASN for formalization by normalizing format,
disassembling into per-claim files, and running quality checks.

```bash
# 1. Format + names
python scripts/blueprint.py NNNN

# 2. Transclude into per-claim files
python scripts/transclude.py NNNN

# 3. Build vocabulary
python scripts/build-vocabulary.py NNNN

# 4. Lint (run any/all, order doesn't matter)
python scripts/lint.py missing NNNN       # undeclared label references
python scripts/lint.py inline NNNN        # embedded results to promote
python scripts/lint.py status NNNN        # wrong status classifications

# 5. Create promotion plan
python scripts/create-promotion-plan.py NNNN
# copy triage.md → promotion-plan.md, review and edit

# 6. Execute promotion plan
python scripts/execute-promotion-plan.py NNNN
python scripts/extract-definition.py NNNN

# 7. Promote to formalization
python scripts/promote-blueprint.py NNNN
```

## Formalization

Review and converge proofs, contracts, and cross-claim consistency.

```bash
# Convergence protocol — regional sweep + whole-ASN review
python scripts/claim-cone-sweep.py NNNN        # cone-scoped review across the DAG
python scripts/claim-full-review.py NNNN       # whole-ASN structural analysis
python scripts/claim-dependency-review.py NNNN # upstream reference validation (standalone)

# Pick up full-review findings from a previous run:
python scripts/claim-full-review.py NNNN --review lattices/<lattice>/formalization/ASN-NNNN/reviews/review-N.md

# Assembly (for downstream consumers)
python scripts/claim-assembly.py NNNN
```

`NNNN` is the ASN number (zero-padded to four digits, e.g. `34` → ASN-0034). `<lattice>` is the lattice directory name.

## Output structure

```
lattices/<lattice>/blueprinting/ASN-NNNN/
  claims/
    _preamble.md
    _table.md
    _vocabulary.md
    <Label>.md
    ...
  lint/
    missing.md
    inline.md
    status.md
    triage.md
    promotion-plan.md

lattices/<lattice>/formalization/ASN-NNNN/
  _table.md
  _vocabulary.md
  <Label>.md
  ...
  reviews/
    review-1.md
    ...
```
