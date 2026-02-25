# Xanadu Specification

Formal specification of the Xanadu hypertext system (udanax-green), derived from Ted Nelson's design intent (Literary Machines) and Roger Gregory's implementation (udanax-green C source).

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
python scripts/run-review.py 9                # 1 cycle: review → revise → commit
python scripts/run-review.py 9 --cycles 2     # 2 cycles
python scripts/run-review.py 9 --review-only  # just review, no revise
python scripts/run-review.py 9 --resume revise  # skip review, revise from latest
```

Steps per cycle: review → revise → commit. Stops early if no REVISE items found.

### Triage — promote ASN open questions to new inquiries

```
python scripts/triage-questions.py 12            # evaluate ASN-0012's open questions
python scripts/triage-questions.py 13 --dry-run  # show decisions without updating files
python scripts/triage-questions.py 4 --model sonnet  # faster, less rigorous
```

Reads the ASN's open questions, checks existing triage (vault/triage/ASN-NNNN.md),
and decides which questions warrant new inquiries. Writes full evaluation with
rationale to per-ASN triage file. Updates inquiries.yaml for promoted questions.

### Triage Defers — promote review DEFER items to new inquiries

```
python scripts/triage-defers.py 4                # evaluate ASN-0004's review deferrals
python scripts/triage-defers.py 14 --dry-run     # show extracted defers without invoking Claude
python scripts/triage-defers.py 4 --model sonnet # faster, less rigorous
```

Extracts DEFER sections from an ASN's review files, checks against existing triage
(vault/triage/ASN-NNNN-defers.md), and decides which deferred topics warrant new
inquiries. Re-running passes previous triage as context to avoid re-promoting.

### Standalone scripts

```
python scripts/review-asn.py 9                # review only → vault/reviews/
python scripts/revise-asn.py 9                # revise using latest review
python scripts/revise-asn.py 9 review-1       # revise using specific review
python scripts/commit.py                      # commit vault/ changes
python scripts/commit.py "hint about changes" # commit with context hint
```

## Scripts

| Script | Purpose |
|--------|---------|
| `run-asn.py` | Discovery pipeline — questions → consult → discover → commit |
| `run-review.py` | Review pipeline — review → revise → commit (repeatable cycles) |
| `review-asn.py` | Review an ASN for rigor (opus, no tools) |
| `revise-asn.py` | Revise an ASN based on review feedback (opus, with tools) |
| `commit.py` | Commit vault changes with descriptive messages (sonnet) |
| `consult-experts.py` | Decompose inquiry into sub-questions, run all consultations |
| `discover.py` | Synthesize expert consultation answers into a formal ASN |
| `consult-nelson.py` | Nelson consultation — design intent from Literary Machines |
| `consult-gregory.py` | Gregory consultation — KB synthesis + code exploration |
| `triage-questions.py` | Evaluate ASN open questions → new inquiries (opus) |
| `triage-defers.py` | Evaluate review DEFER items → new inquiries (opus) |
| `extract-vocab.py` | Extract structural conventions from finalized ASNs |

## Prompt Templates

| Template | Used by | Purpose |
|----------|---------|---------|
| `discovery.md` | `discover.py`, `revise-asn.py` | Discovery/revision agent — Dijkstra-style ASN writing |
| `review.md` | `review-asn.py` | Review agent — rigor checking |
| `commit.md` | `commit.py`, `run-asn.py` | Commit message generation |
| `nelson-questions.md` | `consult-experts.py` | Generate Nelson sub-questions from inquiry |
| `gregory-questions.md` | `consult-experts.py` | Generate Gregory sub-questions from inquiry + KB |
| `nelson-agent.md` | `consult-nelson.py` | Nelson answering agent |
| `gregory-synthesis-agent.md` | `consult-gregory.py` | Gregory KB synthesis agent |
| `gregory-code-agent.md` | `consult-gregory.py` | Gregory code exploration agent |
| `triage-questions.md` | `triage-questions.py` | Open question evaluation and inquiry framing |
| `triage-defers.md` | `triage-defers.py` | Review deferral evaluation and inquiry framing |

## Directory Structure

```
vault/
  asns/           — Abstract Specification Notes (ASN-NNNN-title.md)
  consultations/  — Orchestrated consultation output (answers.md per ASN)
  transcripts/    — Individual agent call logs (Nelson/Gregory subagent runs)
  reviews/        — Review outputs (ASN-NNNN-review-N.md)
  inquiries.yaml  — Inquiry definitions driving ASN production
  triage/          — Per-ASN triage decisions (promoted/declined with rationale)
  vocabulary.md   — Shared vocabulary for ASN authors

scripts/          — Pipeline and consultation scripts
  prompts/        — Prompt templates for all agents

resources/        — Source materials (Literary Machines, Nelson's notes, concept maps)

udanax-test-harness/  — Test harness for udanax-green (golden tests, findings, KB)
```
