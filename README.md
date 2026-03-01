# Xanadu Specification

Formal specification of the Xanadu hypertext system (udanax-green), derived from Ted Nelson's design intent (Literary Machines) and Roger Gregory's implementation (udanax-green C source).

## Overview

```
                          inquiries.yaml
                               |
                               v
                    +---------------------+
                    |   consult-experts   |  Nelson (Literary Machines)
                    |   consult-nelson    |  Gregory (KB + udanax-green)
                    +---------------------+
                               |
                          answers.md
                               |
                               v
                    +---------------------+
                    |      discover       |  Dijkstra-style derivation
                    +---------------------+
                               |
                           ASN draft
                               |
          +--------------------+
          |                    |
          v                    v
  +-------------------+  +-------------------+
+-|    review-asn     |  | triage-questions  |
| +-------------------+  | triage-defers     |
|         |              +-------------------+
|    review file               |
|         |               inquiries.yaml
|         |               (new inquiries)
|         v
| +-------------------+
| | consult-for-rev.  |  expert evidence
| +-------------------+
|         |
| consultation results
|         |
|         v
| +-------------------+
| |    revise-asn     |  targeted fixes
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
|   contract-asn    |  classify & name properties
+-------------------+
          |
    contract table
          |
          v
    +-----------+
    |  commit   |
    +-----------+
          |
          v
+-------------------+
|   Dafny (future)  |  verified specification
+-------------------+
          |
          v
    Go (compiled)     reference implementation / test oracle
```

## Pipelines

### Discovery — produce a new ASN

```
python scripts/run-asn.py --inquiries 4 questions    # preview sub-questions
python scripts/run-asn.py --inquiries 4 consult      # questions + consultations
python scripts/run-asn.py --inquiries 4 discover     # consult + discover
python scripts/run-asn.py --inquiries 4              # full pipeline (through commit)
```

Steps: questions → consult → discover → commit

### Review/Revise — improve an existing ASN

```
python scripts/run-review.py 9                # 1 cycle: review → consult → revise → commit
python scripts/run-review.py 9 --cycles 2     # 2 cycles
python scripts/run-review.py 9 --review-only  # just review, no consult or revise
python scripts/run-review.py 9 --resume consult  # skip review, consult + revise from latest
python scripts/run-review.py 9 --resume revise   # skip review + consult, revise from latest
```

Steps per cycle: review → consult → revise → commit. Stops early if no REVISE items found.

### Contract — classify properties for Dafny translation

Run after an ASN has converged through review. Produces a property mapping table
in `vault/formalization/contracts/`.

```
python scripts/contract-asn.py 4              # generate contract for ASN-0004
python scripts/contract-asn.py 4 --dry-run    # show prompt size without invoking
```

Each property is classified by type (INV/PRE/POST/FRAME/LEMMA) and assigned a
descriptive Dafny identifier. Re-running after an ASN revision preserves
established names and flags changes. The contract tracks which ASN revision it
was generated against.

Output: `vault/formalization/contracts/ASN-NNNN-contract.md`

### Triage — promote ASN open questions to new inquiries

```
python scripts/triage-questions.py 12            # evaluate ASN-0012's open questions
python scripts/triage-questions.py 13 --dry-run  # show decisions without updating files
python scripts/triage-questions.py 4 --model sonnet  # faster, less rigorous
```

Reads the ASN's open questions, checks existing triage (vault/discovery/triage/ASN-NNNN.md),
and decides which questions warrant new inquiries. Writes full evaluation with
rationale to per-ASN triage file. Updates inquiries.yaml for promoted questions.

### Triage Defers — promote review DEFER items to new inquiries

```
python scripts/triage-defers.py 4                # evaluate ASN-0004's review deferrals
python scripts/triage-defers.py 14 --dry-run     # show extracted defers without invoking Claude
python scripts/triage-defers.py 4 --model sonnet # faster, less rigorous
```

Extracts DEFER sections from an ASN's review files, checks against existing triage
(vault/discovery/triage/ASN-NNNN-defers.md), and decides which deferred topics warrant new
inquiries. Re-running passes previous triage as context to avoid re-promoting.

### Standalone scripts

```
python scripts/review-asn.py 9                # review only → vault/discovery/reviews/
python scripts/consult_for_revision.py 9          # consult for latest review
python scripts/consult_for_revision.py 9 --dry-run  # categorize only, no consultations
python scripts/revise-asn.py 9                # revise using latest review
python scripts/revise-asn.py 9 review-1       # revise using specific review
python scripts/commit.py                      # commit vault/ changes
python scripts/commit.py "hint about changes" # commit with context hint
```

## Scripts

| Script | Purpose |
|--------|---------|
| `run-asn.py` | Discovery pipeline — questions → consult → discover → commit |
| `run-review.py` | Review pipeline — review → consult → revise → commit (repeatable cycles) |
| `review-asn.py` | Review an ASN for rigor (opus, no tools) |
| `consult_for_revision.py` | Categorize review findings, run targeted expert consultations (opus) |
| `revise-asn.py` | Revise an ASN based on review feedback (opus, with tools) |
| `contract-asn.py` | Classify properties and assign Dafny names (opus, post-convergence) |
| `commit.py` | Commit vault changes with descriptive messages (sonnet) |
| `consult_experts.py` | Decompose inquiry into sub-questions, run all consultations |
| `discover.py` | Synthesize expert consultation answers into a formal ASN |
| `consult-nelson.py` | Nelson consultation — design intent from Literary Machines |
| `consult-gregory.py` | Gregory consultation — KB synthesis + code exploration |
| `triage-questions.py` | Evaluate ASN open questions → new inquiries (opus) |
| `triage-defers.py` | Evaluate review DEFER items → new inquiries (opus) |

## Prompt Templates

| Template | Used by | Purpose |
|----------|---------|---------|
| `discovery.md` | `discover.py`, `revise-asn.py` | Discovery/revision agent — Dijkstra-style ASN writing |
| `review.md` | `review-asn.py` | Review agent — rigor checking |
| `refine.md` | `contract-asn.py` | Property classification and Dafny naming |
| `commit.md` | `commit.py`, `run-asn.py` | Commit message generation |
| `nelson-questions.md` | `consult_experts.py` | Generate Nelson sub-questions from inquiry |
| `gregory-questions.md` | `consult_experts.py` | Generate Gregory sub-questions from inquiry + KB |
| `nelson-agent.md` | `consult-nelson.py` | Nelson answering agent |
| `gregory-synthesis-agent.md` | `consult-gregory.py` | Gregory KB synthesis agent |
| `gregory-code-agent.md` | `consult-gregory.py` | Gregory code exploration agent |
| `triage-questions.md` | `triage-questions.py` | Open question evaluation and inquiry framing |
| `triage-defers.md` | `triage-defers.py` | Review deferral evaluation and inquiry framing |

## Directory Structure

```
vault/
  modeling/         — The model artifacts
    asns/           — Abstract Specification Notes (ASN-NNNN-title.md)
    dafny/          — Verified specification modules (ASN-NNNN.dfy)
    vocabulary.md   — Shared vocabulary for ASN authors

  discovery/        — Working artifacts of building the model
    inquiries.yaml  — Inquiry definitions driving ASN production
    consultations/  — Orchestrated consultation output (answers.md per ASN)
    transcripts/    — Individual agent call logs (Nelson/Gregory subagent runs)
    reviews/        — Review outputs (ASN-NNNN-review-N.md)
    triage/         — Per-ASN triage decisions (promoted/declined with rationale)

  formalization/    — Working artifacts of encoding the model
    contracts/      — Property contracts (ASN-NNNN-contract.md) — type + Dafny name mappings
    extracts/       — Extracted formal properties (ASN-NNNN-extract.md)

  usage-log.jsonl   — API call tracking

scripts/            — Pipeline and consultation scripts
  paths.py          — Shared vault path constants
  prompts/          — Prompt templates for all agents

notes/              — Design decisions and methodology notes

nelson/             — Nelson's source materials (Literary Machines, concepts, design intent)

udanax-test-harness/  — Test harness for udanax-green (golden tests, findings, KB)
```

## Formalization Path

```
ASN (prose spec) → contract (type + name mapping) → Dafny (verified spec) → Go (compiled)
```

- **ASN**: Prose specification with formal properties. Neutral labels (S0, PRE1, INS-F2)
  to avoid anchoring bias during review.
- **Contract**: Maps each property to a Dafny name, type, and construct. Generated
  post-convergence. Tracks ASN revision for staleness detection.
- **Dafny**: Verified specification using datatypes (functional style). State is an
  immutable value; operations are pure functions. No `modifies`, no heap reasoning.
  See `notes/dafny-modeling-decision.md`.
- **Go**: Compiled from Dafny. Serves as verified reference implementation / test oracle.
  Thin stateful wrapper over pure functional core.
