# Promote Inline

Extracts embedded results (lemmas, consequences, case analyses) from
claim sections into standalone claims.

## Prerequisites

- ASN must be **formalized** — claims must have `*Formal Contract:*`
  sections. The tool uses the contract marker to identify post-contract
  content.
- ASN should be **format-stable** — run the formatter first so claim
  sections are cleanly delimited.

## After Running

Run the formalization pipeline to complete the new claims:

```
./run/formalize.sh <ASN>
```

The pipeline will:
- Add table rows for the new claims (format checker)
- Generate formal contracts (quality rewriter)
- Validate contracts (contract validation)
- Verify proofs (local-review)

## Steps

### Step 1: Scan (sonnet, print-mode)

**Prompt:** `scan.md`

Classifies each post-contract block as:
- **derived** — result with a proof, should be its own claim
- **commentary** — design rationale or notes, stays in place

### Step 2: Promote (opus, agent mode)

**Prompt:** `promote.md`

For each derived result:
- Creates a new claim section with `**LABEL (Name).**` header
- Moves the proof text (does not rewrite it)
- Rewrites the source narrative to cite the new label
- Keeps commentary in place

## Usage

```
python scripts/execute-promotion-plan.py 34              # execute full plan
python scripts/execute-promotion-plan.py 34 --label TA5  # single claim
python scripts/execute-promotion-plan.py 34 --dry-run    # show what would be promoted
```
