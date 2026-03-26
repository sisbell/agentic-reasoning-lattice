# Xanadu Specification

Formal specification of the Xanadu hypertext system (udanax-green), derived from Ted Nelson's design intent (Literary Machines) and Roger Gregory's implementation (udanax-green C source).

## Overview

```
                          inquiries.yaml
                               |
                               v
                    +---------------------+
                    |   draft (consult)   |  Nelson (Literary Machines)
                    |   consult nelson    |  Gregory (KB + udanax-green)
                    +---------------------+
                               |
                          answers.md
                               |
                               v
                    +---------------------+
                    |   draft (discover)  |  Dijkstra-style derivation
                    +---------------------+
                               |
                           ASN draft
                               |
          +--------------------+
          |                    |
          v                    v
  +-------------------+  +-------------------+
+-|      review       |  | promote questions |
| +-------------------+  | promote scope     |
|         |              +-------------------+
|    review file               |
|         |               inquiries.yaml
|         |               (new inquiries)
|         v
| +-------------------+
| | review (consult)  |  expert evidence
| +-------------------+
|         |
| consultation results
|         |
|         v
| +-------------------+
| | review (revise)   |  targeted fixes
| +-------------------+
|         |
|         v
|     +-----------+
|     |  commit   |
|     +-----------+
|         |
|  repeat |
|  until  |
+---------+
          |
          v (converged)
+-------------------+
|   model alloy     |  bounded model checking (counterexample search)
+-------------------+
          |
  counterexample? → revise ASN
          |
          v (no counterexamples)
+-------------------+
|   model index     |  classify & label properties
+-------------------+
          |
    proof index
          |
          v
+-------------------+
| model statements  |  formal statements from ASN prose
+-------------------+
          |
     extract file
          |
          v
+-------------------+
|   model dafny     |  Dafny module
+-------------------+
          |
          v
  +-------------------+
+-| model verify-dafny|  dafny verify + tier classify
| +-------------------+
|         |
|    pass | fail
|         v
| +-------------------+
| |   (auto fix)      |  LLM-assisted fix (Tier 1/2)
| +-------------------+
|         |
|  retry  |  Tier 3 → escalation report
+---------+           → re-review ASN
          |
          v (verified)
    +-----------+
    |  commit   |
    +-----------+
          |
          v
    Go (compiled)     reference implementation / test oracle
```

## Documentation

| Document | Description |
|----------|-------------|
| [Cheat Sheet](docs/cheat-sheet.md) | When you need to get involved (start here) |
| [Pipeline Overview](docs/pipeline-overview.md) | End-to-end walkthrough of the full pipeline |
| [Discovery](docs/discovery.md) | Creating new ASNs from inquiries |
| [Review](docs/review.md) | Review and revision cycles |
| [Expert Consultation](docs/expert-consultation.md) | Nelson and Gregory channels |
| [Foundations](docs/foundations.md) | Verified building blocks (Types/State/Invariants) |
| [Modeling](docs/modeling.md) | From ASN to verified Dafny |
| [Alloy Checking](docs/alloy-checking.md) | Bounded model checking |
| [Dafny Verification Loop](docs/dafny-verification-loop.md) | Three-tier failure handling |
| [Promotion](docs/promotion.md) | Feeding the pipeline with new inquiries |
| [Extend / Absorb / Rebase](docs/extend-absorb-rebase.md) | Moving properties between ASN layers |
| [Methodology](docs/methodology.md) | Design principles and formal methods grounding |

## CLI Reference

All pipeline commands use verb-based dispatchers in `scripts/`:

```
draft             # inquiry → ASN (questions → consult → discover → commit)
review            # review → consult → revise → commit cycle
promote           # spawn new inquiries from ASN artifacts
  questions       #   from ASN open questions
  scope           #   from review OUT_OF_SCOPE items
model             # formal modeling artifacts
  index           #   proof-index (classify + label properties)
  statements      #   extract formal statements from ASN prose
  alloy           #   Alloy bounded model checking
  dafny           #   Dafny per-property generation + verification
  verify-dafny    #   Dafny verification loop (verify → fix → re-verify)
requirements      # extract Nelson design features from ASNs
consult           # ad-hoc expert consultation
  nelson          #   Nelson (Literary Machines, design intent)
  gregory         #   Gregory (KB synthesis + code exploration)
commit            # commit vault/ changes
```

## Pipelines

### Discovery — produce a new ASN

```
python scripts/draft.py --inquiries 4 questions    # preview sub-questions
python scripts/draft.py --inquiries 4 consult      # questions + consultations
python scripts/draft.py --inquiries 4 discover     # consult + discover
python scripts/draft.py --inquiries 4              # full pipeline (through commit)
```

Steps: questions → consult → discover → commit

### Review/Revise — improve an existing ASN

```
python scripts/review.py 9                # 1 cycle: review → consult → revise → commit
python scripts/review.py 9 --cycles 2     # 2 fixed cycles
python scripts/review.py 9 --converge     # loop until CONVERGED (max 5)
python scripts/review.py 9 --converge 8   # loop until CONVERGED (max 8)
python scripts/review.py 9 --review-only  # just review, no consult or revise
python scripts/review.py 9 --resume consult  # skip review, consult + revise from latest
python scripts/review.py 9 --resume revise   # skip review + consult, revise from latest
```

Steps per cycle: review → consult → revise → commit.

**Convergence:** Each review produces a `VERDICT: CONVERGED | REVISE`. CONVERGED means
all remaining issues are minor (prose clarity, formatting) and the formal content is
correct. `--converge` loops until the reviewer returns CONVERGED or the max cycle limit
is reached. `--cycles N` runs exactly N cycles regardless of verdict.

### Alloy — bounded model checking

Run after an ASN has converged. Per-property Alloy generation, bounded checking with
tiered repair, then review → consult → revise → commit if failures remain.

```
python scripts/model.py alloy 1                    # full pipeline (all properties)
python scripts/model.py alloy 1 --property T1      # single property
python scripts/model.py alloy 1 --no-revise         # stop after check + review
python scripts/model.py alloy 1 --skip-check       # generate .als only
python scripts/model.py alloy 1 --dry-run           # show property list + prompt sizes
```

Requires Alloy installed at `/Applications/Alloy.app` (macOS) or `ALLOY_JAR` env var.

Output:
- `vault/4-modeling/alloy/ASN-NNNN/{label}-{Name}.als` (one per property)
- `vault/2-review/ASN-NNNN/review-N.md` (if failures after repair)

### Modeling — proof-index → extract → dafny

Run after an ASN has converged through review. Three steps, each building on the previous:

```
python scripts/normalize.py 4                   # extract formal statements from ASN prose
python scripts/model.py index 4              # classify properties, assign proof labels
python scripts/model.py dafny 4              # generate verified Dafny per property
```

**Proof index** classifies each property by type (INV/PRE/POST/FRAME/LEMMA) and assigns
a descriptive proof label. Re-running after an ASN revision preserves
established labels and flags changes.

**Extract** uses the proof index as a roster to locate each property in the ASN,
extracting just the formal statement. Produces a compact file suitable for Dafny
generation.

**Generate** translates the extract into a Dafny module using datatypes (functional
style). State is an immutable value; operations are pure functions.

Output:
- `vault/4-modeling/proof-index/ASN-NNNN-proof-index.md`
- `vault/project-model/ASN-NNNN/formal-statements.md`
- `vault/proofs/ASN-NNNN.dfy`

### Verification — verify Dafny module with fix loop

Run after generating a Dafny module. Three-tier failure handling with automatic
fix attempts and escalation. See [`docs/dafny-verification-loop.md`](docs/dafny-verification-loop.md).

```
python scripts/model.py verify-dafny 4                     # verify + fix loop
python scripts/model.py verify-dafny 4 --full               # proof-index → extract → generate → verify loop
python scripts/model.py verify-dafny 4 --max-tier1 3        # up to 3 Tier 1 (syntax) fix attempts
python scripts/model.py verify-dafny 4 --max-tier2 2        # up to 2 Tier 2 (proof) fix attempts
python scripts/model.py verify-dafny 4 --dry-run            # check paths, no execution
```

**Tiers:** Tier 1 = syntax/type errors (auto-fix). Tier 2 = proof-structural errors
(fix with extract context). Tier 3 = spec errors (escape to ASN review cycle).

**Escalation:** Tier 1 → 3 attempts → Tier 2. Tier 2 → 2 attempts → Tier 3.
Tier 3 writes an escalation report to `vault/4-modeling/verification/`.

Output:
- `vault/4-modeling/verification/ASN-NNNN-verify-N.md` (verification reports)
- `vault/4-modeling/verification/ASN-NNNN-escalation.md` (Tier 3 escalation)

### Promote — spawn new inquiries from ASN artifacts

```
python scripts/promote.py questions 12            # evaluate ASN-0012's open questions
python scripts/promote.py questions 13 --dry-run  # show decisions without updating files
python scripts/promote.py scope 4                 # evaluate ASN-0004's review deferrals
python scripts/promote.py scope 14 --dry-run      # show extracted defers without invoking Claude
```

**questions** reads the ASN's open questions, checks existing promotions, and decides
which questions warrant new inquiries. Updates inquiries.yaml for promoted questions.

**scope** extracts OUT_OF_SCOPE sections from an ASN's review files, checks against
existing promotions, and decides which deferred topics warrant new inquiries.

### Ad-hoc expert consultation

```
python scripts/consult.py nelson "What is Nelson's intent for withdrawal?"
python scripts/consult.py nelson --with-png "question"     # enable page image access
python scripts/consult.py gregory "What does INSERT do at a span boundary?"
python scripts/consult.py gregory --kb-only "question"     # KB synthesis only
```

### Other commands

```
python scripts/commit.py                      # commit vault/ changes
python scripts/commit.py "hint about changes" # commit with context hint
python scripts/requirements.py 4 6 9          # extract features from specific ASNs
python scripts/requirements.py                # extract features from all ASNs
```

## Scripts

### Dispatchers (`scripts/`)

| Script | Purpose |
|--------|---------|
| `draft.py` | Discovery pipeline — questions → consult → discover → commit |
| `review.py` | Review pipeline — review → consult → revise → commit (cycles or converge) |
| `model.py` | Formal modeling — index, statements, alloy, dafny, verify-dafny |
| `promote.py` | Spawn new inquiries — questions, scope |
| `consult.py` | Ad-hoc expert consultation — nelson, gregory |
| `requirements.py` | Extract Nelson design features from ASNs |
| `commit.py` | Commit vault changes with descriptive messages (sonnet) |

### Library modules (`scripts/lib/`)

| Script | Purpose |
|--------|---------|
| `common.py` | Shared utilities — read_file, find_asn, invoke_claude, log_usage |
| `draft_pipeline.py` | Discovery orchestration — questions → consult → discover → commit |
| `draft_consult.py` | Decompose inquiry into sub-questions, run all consultations |
| `draft_discover.py` | Synthesize expert consultation answers into a formal ASN |
| `review_pipeline.py` | Review orchestration — review → consult → revise → commit (cycles or converge) |
| `review_check.py` | Review an ASN for rigor, produce VERDICT (opus, no tools) |
| `review_consult.py` | Categorize review findings, run targeted expert consultations (opus) |
| `review_revise.py` | Revise an ASN based on review feedback (opus, with tools) |
| `model_index.py` | Classify properties and assign proof labels (opus, post-convergence) |
| `export_statements.py` | Extract formal property statements from ASN prose (sonnet) |
| `model_alloy.py` | Alloy pipeline — generate, check, repair, review → consult → revise (sonnet) |
| `model_dafny.py` | Generate Dafny per-property specification (opus) |
| `model_verify.py` | Verification loop — verify → fix → re-verify with tier escalation |
| `model_verify_run.py` | Run `dafny verify`, parse errors, classify by tier |
| `model_fix.py` | LLM-assisted Dafny fix from verification errors (sonnet) |
| `consult_nelson.py` | Nelson consultation — design intent from Literary Machines |
| `consult_gregory.py` | Gregory consultation — KB synthesis + code exploration |
| `promote_questions.py` | Evaluate ASN open questions → new inquiries (opus) |
| `promote_scope.py` | Evaluate review DEFER items → new inquiries (opus) |
| `requirements_extract.py` | Extract Nelson design features from ASN prose |

## Prompt Templates

### Discovery prompts (`scripts/prompts/discovery/`)

| Template | Used by | Purpose |
|----------|---------|---------|
| `discovery.md` | `draft_discover.py`, `review_revise.py` | Discovery/revision agent — Dijkstra-style ASN writing |
| `review.md` | `review_check.py` | Review agent — rigor checking |
| `nelson-agent.md` | `consult_nelson.py` | Nelson answering agent |
| `nelson-questions.md` | `draft_consult.py` | Generate Nelson sub-questions from inquiry |
| `gregory-questions.md` | `draft_consult.py` | Generate Gregory sub-questions from inquiry + KB |
| `gregory-synthesis-agent.md` | `consult_gregory.py` | Gregory KB synthesis agent |
| `gregory-code-agent.md` | `consult_gregory.py` | Gregory code exploration agent |
| `triage-questions.md` | `promote_questions.py` | Open question evaluation and inquiry framing |
| `triage-defers.md` | `promote_scope.py` | Review deferral evaluation and inquiry framing |

### Modeling prompts (`scripts/prompts/formalization/`)

| Template | Used by | Purpose |
|----------|---------|---------|
| `refine.md` | `model_index.py` | Property classification and proof labeling |
| `export.md` | `export_statements.py` | Extract formal statements from ASN |
| `generate-dafny.md` | `model_dafny.py` | Generate Dafny module from extract |
| `fix-dafny.md` | `model_fix.py` | Fix Dafny errors (Tier 1 syntax, Tier 2 proof) |
| `check-alloy.md` | `model_alloy.py` | Generate Alloy model for bounded checking |

### Shared prompts (`scripts/prompts/`)

| Template | Used by | Purpose |
|----------|---------|---------|
| `commit.md` | `commit.py`, `draft_pipeline.py` | Commit message generation |

## Directory Structure

```
vault/
  asns/             — Deliverable: Abstract Specification Notes (ASN-NNNN-title.md)
  proofs/           — Deliverable: Verified Dafny specification modules
  vocabulary.md     — Shared vocabulary for ASN authors
  requirements/     — Nelson's design features

  project-model/    — Per-ASN definitions (scope, dependencies, stage config)
    ASN-NNNN/       — Per-ASN directory
      project.yaml  — Definition for each active ASN
      formal-statements.md — Extracted formal statements
      dependency-graph.yaml — ASN dependency graph
      open-issues.md — Open issues
    index.md        — Generated DAG overview

  1-promote/        — Stage 1: Promoted questions and deferrals
    inquiries.yaml  — Historical record (scripts read from project-model/)
    ASN-NNNN/       — Per-ASN promoted open questions and deferrals

  2-review/         — Stage 2: Review outputs (review-N.md per ASN)
    ASN-NNNN/

  3-export/        — Stage 3: (deprecated — statements moved to project-model/ASN-NNNN/)

  4-modeling/       — Stage 4: Modeling artifacts
    alloy/          — Alloy models for bounded checking (.als files)
    proof-index/    — Proof index (ASN label → proof label mappings)
    verification/   — Verification reports + escalation files
    dafny/          — Divergence evidence from Dafny generation

  experts/          — Expert consultation results + session transcripts
    ASN-NNNN/
      consultation/ — Initial consultation (answers.md, questions.md)
      consultation-N/ — Per-review consultations
      sessions/     — Individual agent call logs (nelson-N/, gregory-N/)

  usage-log.jsonl   — API call tracking

scripts/            — Pipeline dispatchers and library modules
  draft.py          — Dispatcher: discovery pipeline
  review.py         — Dispatcher: review/revise pipeline
  model.py          — Dispatcher: formal modeling (index, statements, alloy, dafny, verify-dafny)
  promote.py        — Dispatcher: spawn new inquiries (questions, scope)
  consult.py        — Dispatcher: ad-hoc expert consultation (nelson, gregory)
  requirements.py   — Dispatcher: extract Nelson design features
  commit.py         — Commit vault changes
  paths.py          — Shared vault path constants
  lib/              — Library modules (invoked by dispatchers)
  prompts/
    discovery/      — Prompt templates for discovery/review agents
    formalization/  — Prompt templates for proof-index/extract/dafny agents
    commit.md       — Shared commit prompt

notes/              — Design decisions and methodology notes

nelson/             — Nelson's source materials (Literary Machines, concepts, design intent)

udanax-test-harness/  — Test harness for udanax-green (golden tests, findings, KB)
```

## Modeling Path

```
ASN (prose) → Alloy (bounded checking) → proof index (label mapping) → extract (formal statements) → Dafny (verified) → Go (compiled)
```

- **ASN**: Prose specification with formal properties. Neutral labels (S0, PRE1, INS-F2)
  to avoid anchoring bias during review.
- **Proof index**: Maps each ASN label to a proof label, type, and construct. Generated
  post-convergence. Tracks ASN revision for staleness detection.
- **Extract**: Compact formal statements pulled from ASN prose, indexed by proof index.
  Strips narrative to produce Dafny-ready input.
- **Dafny**: Verified specification using datatypes (functional style). State is an
  immutable value; operations are pure functions. No `modifies`, no heap reasoning.
  See `notes/dafny-modeling-decision.md`.
- **Go**: Compiled from Dafny. Serves as verified reference implementation / test oracle.
  Thin stateful wrapper over pure functional core.
