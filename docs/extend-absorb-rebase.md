# Extend / Absorb / Rebase

Commands for moving properties between ASN layers.

## When to Use

A higher-level spec (e.g., ASN-0053 Span Algebra) derives a property that belongs in a lower-level foundation (e.g., ASN-0034 Tumbler Algebra). The property needs to move down without reworking the entire foundation by hand.

## Commands

| Command | Purpose |
|---------|---------|
| `extend.py` | Extract properties into a new small extension ASN |
| `review.py` / `revise.py` | Review/revise the extension (standard cycle) |
| `normalize.py` | Export the extension's statements |
| `absorb.py` | Integrate extension into base reasoning doc |
| `rebase.py` | Update source ASN to cite from updated foundation |

## Case 1: Move Properties Between Domains

Properties D0, D1 in ASN-0053 belong in ASN-0034's domain.

```bash
# 1. Extract into a small extension
python scripts/extend.py -s 53 -t 57 -b 34 --properties D0,D1

# 2. Review/revise the extension (small scope = thorough)
python scripts/review.py 57
python scripts/revise.py 57 --converge

# 3. Export the extension
python scripts/normalize.py 57

# 4. Absorb into base (integrates into ASN-0034 reasoning doc,
#    runs targeted integration review/revise, re-exports ASN-0034,
#    removes extension artifacts)
python scripts/absorb.py 57

# 5. Rebase source (updates ASN-0053 to cite from foundation,
#    runs targeted rebase review/revise, re-exports ASN-0053)
python scripts/rebase.py 53
```

## Case 2: Hand-Crafted Extension, Later Absorbed

Manually create an extension. Review/revise/export it independently. Later absorb.

```bash
# Create ASN-0055 by hand (extends 34, add source: 53 to project model)
# Review/revise/export as normal...

# Absorb into base
python scripts/absorb.py 55

# Rebase source
python scripts/rebase.py 53
```

## Case 3: Permanent Extension

Create an extension and keep it. Don't absorb. The bundling mechanism in `foundation.py` auto-includes it when any ASN depends on the base.

```bash
# Create and converge ASN-0056 (extends 53)
# Review/revise/export as normal...
# Done. Any ASN depending on 53 automatically gets 56's statements.
```

## extend.py

```
python scripts/extend.py -s 53 -t 57 -b 34 --properties D0,D1
```

| Flag | Long | Meaning |
|------|------|---------|
| `-s` | `--source` | ASN where properties currently live |
| `-t` | `--target` | New ASN number to create |
| `-b` | `--base` | What the new ASN extends (the domain it belongs in) |
| | `--properties` | Comma-separated property labels to extract |

Source must != base. Creates reasoning doc + project model. Does not review/export/absorb.

## absorb.py

```
python scripts/absorb.py 57
```

Reads the extension's project model (`extends` and `source` fields). Steps:

1. Integrate extension properties into base **reasoning doc** (Claude agent)
2. Targeted integration review/revise (checks fit, not correctness)
3. Re-export the base
4. Remove extension project model and export file

The extension's reasoning doc is kept as a trace artifact.

## rebase.py

```
python scripts/rebase.py 53
python scripts/rebase.py 53 --properties D0,D1
```

Compares the ASN's local derivations against its foundation. Replaces local proofs with citations where the foundation now covers them. Steps:

1. Claude agent replaces local derivations with citations
2. Targeted rebase review/revise (checks citations, references, registry)
3. Re-export the ASN

## Review Stages

Each stage has its own focused review/revise prompts:

| Stage | Reviews | Ignores |
|-------|---------|---------|
| Extension review | Proof correctness, boundary cases, worked examples | Everything else |
| Integration review (absorb) | Placement, references, formatting, registry | Pre-existing content, proof correctness |
| Rebase review | Citation accuracy, downstream references, registry | Pre-existing content, unrebased properties |

Same rigor at every stage. Different scope.

## Project Model

Extension ASNs use these fields:

```yaml
extends: 34        # base ASN (what this extends)
source: 53         # where properties were extracted from (for absorb/rebase)
depends: [34]
```
