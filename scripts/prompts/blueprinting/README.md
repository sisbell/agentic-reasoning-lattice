# Blueprinting Pipeline

Prepare a monolithic ASN for formalization by normalizing format,
disassembling into per-property files, and running quality checks.

## Pipeline

```bash
# 1. Format + names + lint unformalized
python scripts/blueprint.py 34

# 2. Disassemble into per-property files
python scripts/disassemble.py 34

# 3. Build vocabulary
python scripts/build-vocabulary.py 34

# 4. Lint (run any/all, order doesn't matter)
python scripts/lint.py missing 34       # undeclared label references
python scripts/lint.py inline 34        # embedded results to promote
python scripts/lint.py status 34        # wrong status classifications

# 5. Manual fixes based on lint findings

# 6. Promote inline results (if lint found any)
python scripts/promote-inline.py 34

# 7. Structure proofs into explicit stages
python scripts/proof-structure.py 34

# 8. Promote to formalization
python scripts/promote-blueprint.py 34
```

## What each step does

| Step | Script | Input | Output |
|------|--------|-------|--------|
| Format | `blueprint.py` | monolithic ASN | formatted ASN + lint report |
| Disassemble | `disassemble.py` | formatted ASN (with `---` markers) | `vault/2-blueprints/ASN-NNNN/properties/` |
| Vocabulary | `build-vocabulary.py` | property files | `_vocabulary.md` |
| Lint missing | `lint.py missing` | property files | `lint/missing.md` |
| Lint inline | `lint.py inline` | property files | `lint/inline.md` |
| Lint status | `lint.py status` | property files (via monolithic ASN) | `lint/status.md` |
| Promote inline | `promote-inline.py` | property files | new property files + updated source |
| Proof structure | `proof-structure.py` | property files | restructured property files |
| Promote | `promote-blueprint.py` | `vault/2-blueprints/` | `vault/3-formalization/ASN-NNNN/` |

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
    unformalized.md
```
