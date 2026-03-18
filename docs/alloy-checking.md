# Alloy Checking — Bounded Model Checking

The Alloy pipeline generates per-property Alloy models and runs bounded model checking to search for counterexamples. This is a lightweight pre-check before investing in full Dafny proof — if Alloy finds a counterexample within small bounds, the property is wrong and the ASN needs revision.

## Purpose

Dafny verification is expensive — generating and proving specifications takes significant API time and iteration. Alloy checking is cheap — generating a bounded model and running it takes seconds. Running Alloy first catches property errors early:

- A counterexample from Alloy is a concrete witness that the property doesn't hold
- Fixing the ASN property before Dafny generation avoids wasted proof effort
- Properties that survive Alloy checking are more likely to verify in Dafny

Alloy checking is sound for counterexamples (if it finds one, the property is wrong) but not complete (passing bounded checking doesn't prove the property holds in general).

## How It Works

```
  ASN (converged) + proof index
       |
       v
[1] generate       per-property .als file (sonnet)
       |
       v
[2] self-check     Alloy syntax validation
       |
       v
[3] check          run Alloy (bounded model checking)
       |
       v
  classify result
       |
       +--- pass ---------> done
       +--- syntax-error --> repair attempt → re-check
       +--- counterexample → review finding
       +--- gen-fail ------> skip (logged)
       |
       v (counterexamples found)
[4] review         generate review from counterexamples, commit
       |
       v
     hints: "run revise.py N"
```

## Result Classification

Each property's Alloy check produces one of four outcomes:

| Result | Meaning | Action |
|--------|---------|--------|
| **pass** | No counterexample found within bounds | Property survives (proceed to Dafny) |
| **counterexample** | Concrete witness found | Review generated → revise the ASN via `revise.py` |
| **syntax-error** | Generated `.als` has Alloy syntax issues | Repair attempt, then re-check |
| **gen-fail** | Could not generate a meaningful Alloy model | Logged and skipped |

## Artifacts

### Input

| Artifact | Location | Description |
|----------|----------|-------------|
| ASN | `vault/asns/ASN-NNNN-*.md` | Converged specification |
| Proof index | `vault/4-modeling/proof-index/ASN-NNNN-proof-index.md` | Property labels and types |

### Output

| Artifact | Location | Description |
|----------|----------|-------------|
| Alloy models | `vault/4-modeling/alloy/ASN-NNNN/{label}-{Name}.als` | One per property |
| Review file | `vault/2-review/ASN-NNNN/review-N.md` | If counterexamples found |

## CLI Reference

```bash
# Full pipeline: generate → check → review → commit
python scripts/model.py alloy 1

# Single property
python scripts/model.py alloy 1 --property T1

# Multiple properties
python scripts/model.py alloy 1 --property T1,T3,TA0

# Generate .als files only — no checking
python scripts/model.py alloy 1 --skip-check

# Preview: show property list and prompt sizes
python scripts/model.py alloy 1 --dry-run

# If counterexamples found, revise the ASN
python scripts/revise.py 1
```

### Flags

| Flag | Description |
|------|-------------|
| `--property LABEL[,LABEL,...]` | Process specific properties, comma-separated |
| `--skip-check` | Generate `.als` files only, don't run Alloy |
| `--dry-run` | Show what would run without executing |
| `--no-revise` | (deprecated — Alloy now always stops after review) |

### Requirements

Alloy must be installed:
- **macOS:** `/Applications/Alloy.app`
- **Other:** set `ALLOY_JAR` environment variable to the Alloy `.jar` path

## Feedback into Review

When counterexamples are found, the pipeline generates a review file with concrete evidence of the property failure. This review is committed, and the command prints a hint to run `revise.py`. The Alloy review is a mechanical review — `revise.py` auto-detects it and skips expert consultation, going straight to revision with the counterexample evidence.

This is more targeted than a standard review — instead of "this property might be wrong," the review says "this property fails for state X with inputs Y, producing result Z which violates the claimed guarantee."

## Design Decisions

**Why per-property, not per-ASN?** Properties are independent formal claims. Checking them individually produces focused counterexamples. A monolithic Alloy model would mix concerns and make counterexamples harder to interpret.

**Why sonnet for generation?** Alloy model generation is structured translation — mapping ASN property statements to Alloy syntax. It doesn't require the deep reasoning of opus. Sonnet's speed advantage matters when generating models for many properties.

**Why bounded checking before Dafny?** Alloy runs in seconds vs. minutes-to-hours for Dafny generation and verification. Finding a counterexample in 3 seconds is cheaper than discovering the same issue after a 30-minute Dafny generation and fix cycle.
