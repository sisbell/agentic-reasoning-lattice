# Promote Inline

Extracts embedded results (lemmas, consequences, case analyses) from
property sections into standalone properties.

## Prerequisites

- ASN must be **formalized** — properties must have `*Formal Contract:*`
  sections. The tool uses the contract marker to identify post-contract
  content.
- ASN should be **format-stable** — run the formatter first so property
  sections are cleanly delimited.

## After Running

Run the formalization pipeline to complete the new properties:

```
./run/formalize.sh <ASN>
```

The pipeline will:
- Add table rows for the new properties (format checker)
- Generate formal contracts (quality rewriter)
- Validate contracts (contract validation)
- Verify proofs (proof-review)

## Steps

### Step 1: Scan (sonnet, print-mode)

**Prompt:** `scan.md`

Classifies each post-contract block as:
- **derived** — result with a proof, should be its own property
- **commentary** — design rationale or notes, stays in place

### Step 2: Promote (opus, agent mode)

**Prompt:** `promote.md`

For each derived result:
- Creates a new property section with `**LABEL (Name).**` header
- Moves the proof text (does not rewrite it)
- Rewrites the source narrative to cite the new label
- Keeps commentary in place

## Usage

```
python scripts/execute-promotion-plan.py 34              # execute full plan
python scripts/execute-promotion-plan.py 34 --label TA5  # single property
python scripts/execute-promotion-plan.py 34 --dry-run    # show what would be promoted
```
