# Pipeline

## Blueprinting

Prepare a monolithic ASN for formalization by normalizing format,
disassembling into per-property files, and running quality checks.

```bash
# 1. Format + names
python scripts/blueprint.py 34

# 2. Disassemble into per-property files
python scripts/disassemble.py 34

# 3. Build vocabulary
python scripts/build-vocabulary.py 34

# 4. Lint (run any/all, order doesn't matter)
python scripts/lint.py missing 34       # undeclared label references
python scripts/lint.py inline 34        # embedded results to promote
python scripts/lint.py status 34        # wrong status classifications

# 5. Create promotion plan
python scripts/create-promotion-plan.py 34
# copy triage.md → promotion-plan.md, review and edit

# 6. Execute promotion plan
python scripts/execute-promotion-plan.py 34
python scripts/extract-definition.py 34

# 7. Promote to formalization
python scripts/promote-blueprint.py 34
```

## Formalization

Review and converge proofs, contracts, and cross-property consistency.

```bash
# Full review cycle (local → contract → full → dependency)
python scripts/formalization-review.py 34

# Or run steps individually:
python scripts/local-review.py 34          # verify proofs, fix gaps
python scripts/contract-review.py 34       # validate contracts, fix mismatches
python scripts/full-review.py 34           # whole-ASN structural analysis
python scripts/dependency-review.py 34     # upstream reference validation

# Pick up full-review findings from a previous run:
python scripts/full-review.py 34 --review vault/3-formalization/ASN-0034/reviews/review-7.md

# Assembly (for downstream consumers)
python scripts/formalization-assembly.py 34
```

## Output structure

```
vault/2-blueprints/ASN-NNNN/
  properties/
    _preamble.md
    _table.md
    _vocabulary.md
    T0a.md
    T1.md
    ...
  lint/
    missing.md
    inline.md
    status.md
    triage.md
    promotion-plan.md

vault/3-formalization/ASN-NNNN/
  _table.md
  _vocabulary.md
  T0a.md
  T1.md
  ...
  reviews/
    review-1.md
    ...
```
