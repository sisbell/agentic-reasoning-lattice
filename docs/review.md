# Review — Review and Revision Cycles

The review pipeline checks an ASN for rigor, runs targeted expert consultations on findings, then revises the ASN. It cycles until the ASN converges — all significant formal issues are resolved and only minor prose/formatting items remain.

## How It Works

```
     ASN (from vault/asns/)
          |
          v
  [1] review       Dijkstra-style rigor check (opus, no tools)
          |
     VERDICT: CONVERGED or REVISE
          |
          +--- CONVERGED ---> done (commit "converged" marker)
          |
          v (REVISE)
  [2] consult      categorize findings, run targeted consultations
          |
          v
  [3] revise       revise ASN from review + consultation (opus, with tools)
          |
          v
  [4] commit       commit revised ASN + review file
          |
          v
     loop back to [1] (if --converge or --cycles > 1)
```

## Step 1: Review

A Dijkstra-style rigor check examines the ASN against the shared vocabulary (`vault/vocabulary.md`) and prior reviews. The review agent uses opus without tools — pure analysis, no file access. This ensures the review is based solely on the formal content of the ASN.

The review produces structured findings in four categories:

| Category | Meaning | Action |
|----------|---------|--------|
| **OKAY** | Property is correct and well-stated | None |
| **REVISE** | Formal issue requiring correction | Fix in this cycle |
| **OUT_OF_SCOPE** | Issue belongs to a different ASN | Deferred (see [Promotion](promotion.md)) |
| **VERDICT** | Overall assessment: CONVERGED or REVISE | Controls loop |

A review file is written to `vault/2-review/ASN-NNNN/review-N.md`, where N increments with each cycle.

### What a Review Checks

- **Correctness** — are properties logically sound? Do clauses contradict?
- **Consistency** — do properties use vocabulary consistently with other ASNs?
- **Completeness** — are there unstated assumptions or missing frame conditions?
- **Clarity** — are formal statements unambiguous? Can they be mechanically translated?

### Review Output Format

```markdown
# Review of ASN-NNNN — Title (Review N)

## Property DEL1 — REVISE
[Finding: clauses 2 and 3 are jointly inconsistent because...]

## Property DEL2 — OKAY
[Brief confirmation]

## Property DEL3 — OUT_OF_SCOPE
[This concerns versioning, which belongs to ASN-0009]

## VERDICT: REVISE
[Summary of what needs to change]
```

## Step 2: Consultation for Revision

REVISE findings are categorized by what kind of evidence is needed to resolve them:

| Category | Meaning | Action |
|----------|---------|--------|
| **INTERNAL** | Can be resolved from the ASN itself | No consultation needed |
| **NELSON** | Needs design intent clarification | Nelson consultation |
| **GREGORY** | Needs implementation evidence | Gregory consultation |
| **BOTH** | Needs both channels | Both consultations |

The categorization agent (opus) reads the review findings and decides which channel to consult for each REVISE item. Consultations run through the same expert channels used in discovery. Results are written to `vault/experts/ASN-NNNN/consultation-N/`.

## Step 3: Revise

The revision agent (opus with Read/Write/Bash tools) receives:
- The current ASN
- The review findings (REVISE items only)
- Consultation results (if any)
- The shared vocabulary

It revises the ASN to address each finding. The revision agent can modify the ASN in place, add/remove/reword properties, update assumptions, and flag new open questions.

**What the revision agent can change:**
- Property statements (rewording, adding clauses, fixing contradictions)
- Assumptions and preconditions
- Prose explanations
- Open questions list

**What it preserves:**
- Property labels (DEL1 stays DEL1)
- Overall ASN structure
- Properties marked OKAY in the review

If the revision produces no material changes (all findings were already addressed or are minor), it returns exit code 2 and the cycle stops.

## Step 4: Commit

The revised ASN and review file are committed. If the verdict was CONVERGED, the commit message notes convergence.

## Convergence

An ASN is CONVERGED when the review agent determines all remaining issues are minor — prose clarity, formatting, presentation — and the formal content is correct and consistent.

Convergence does not mean the ASN is complete. Open questions may remain (addressed by [Promotion](promotion.md)). It means the properties as stated are internally consistent and well-formed.

### Typical convergence trajectory

Most ASNs converge in 3-7 review cycles. Early cycles catch structural issues (contradictions, missing frame conditions). Later cycles catch consistency issues (vocabulary alignment, assumption completeness). The final cycle often produces only OKAY and minor prose suggestions.

## Artifacts

### Input

| Artifact | Location | Description |
|----------|----------|-------------|
| ASN | `vault/asns/ASN-NNNN-*.md` | The specification to review |
| Vocabulary | `vault/vocabulary.md` | Shared terms and type definitions |
| Prior reviews | `vault/2-review/ASN-NNNN/review-*.md` | Previous review cycles |

### Output

| Artifact | Location | Description |
|----------|----------|-------------|
| Review file | `vault/2-review/ASN-NNNN/review-N.md` | Structured findings |
| Consultation results | `vault/experts/ASN-NNNN/consultation-N/` | Targeted expert answers |
| Revised ASN | `vault/asns/ASN-NNNN-*.md` | Updated specification |

## CLI Reference

```bash
# One review cycle: review → consult → revise → commit
python scripts/review.py 9

# Fixed number of cycles
python scripts/review.py 9 --cycles 2

# Loop until CONVERGED (default max 5 cycles)
python scripts/review.py 9 --converge

# Loop until CONVERGED (custom max)
python scripts/review.py 9 --converge 8

# Review only — no consultation or revision
python scripts/review.py 9 --review-only

# Resume from a specific stage (uses latest review)
python scripts/review.py 9 --resume consult    # skip review, run consult + revise
python scripts/review.py 9 --resume revise     # skip review + consult, just revise
```

### Flags

| Flag | Description |
|------|-------------|
| `--cycles N` | Run exactly N review cycles |
| `--converge [MAX]` | Loop until CONVERGED, max MAX cycles (default 5) |
| `--review-only` | Run review step only, skip consult and revise |
| `--resume STAGE` | Resume from consult or revise using latest review |

### ASN numbering

The ASN argument accepts flexible formats: `9`, `09`, `0009`, `ASN-0009`, or a full file path. All are normalized to `ASN-NNNN`.

## Design Decisions

**Why opus without tools for review?** The review must be pure analysis — reasoning about the formal content of the ASN without being influenced by external files. Giving the reviewer file access would allow it to check implementation details, breaking the abstraction boundary. The review operates within the model, not outside it.

**Why categorize before consulting?** Not every REVISE finding needs expert input. Internal contradictions (clause A vs. clause B) can be resolved from the ASN alone. Categorization avoids unnecessary API calls and keeps consultations focused on questions that actually need external evidence.

**Why a separate consult step between review and revise?** The review identifies what's wrong but doesn't always know the answer. A finding like "DEL1 clause 3 contradicts the permanence guarantee" requires Nelson or Gregory input to resolve correctly. Without the consultation step, the revision agent would have to guess, often introducing new errors.

**Why `--converge` instead of always converging?** Sometimes you want to run a single cycle and inspect the results before continuing. `--converge` is for unattended operation when you trust the pipeline to find the right stopping point.
