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

### Vocabulary — extract conventions and align ASNs

Two-phase process: **extract** builds the canonical vocabulary, **align** rewrites ASNs to match it.

**Phase 1: Build vocabulary incrementally.** Start with the most canonical ASN and add
one at a time, reviewing conflicts at each step.

```bash
# 1. Seed vocabulary from the most well-established ASN
python scripts/extract-vocab.py 4 --dry-run    # preview conflicts + proposed vocab
python scripts/extract-vocab.py 4              # write vocabulary.md
git diff vault/vocabulary.md                   # review

# 2. Add the next ASN — conflicts show where it diverges
python scripts/extract-vocab.py 4 5 --dry-run  # see what ASN-0005 adds/conflicts
python scripts/extract-vocab.py 4 5            # update vocabulary
git diff vault/vocabulary.md                   # review, commit if good

# 3. Continue adding ASNs, reviewing conflicts each time
python scripts/extract-vocab.py 4 5 6          # add ASN-0006
# ... repeat until all ASNs are covered

# Or once confident, process everything at once
python scripts/extract-vocab.py --all
```

Conflicts print to stderr (term, vocab says, ASN says, recommendation). The majority
convention wins. Review the diff after each step — vocabulary.md is the single source
of truth for notation.

**Phase 2: Align ASNs to vocabulary.** Once vocabulary.md is stable, rewrite each ASN
to match. One ASN at a time — review the diff before moving on.

```bash
# Align the most divergent ASN first
python scripts/align-vocab.py 3                # align ASN-0003
git diff vault/asns/                           # review notation changes

# Verify idempotence — re-running should produce no diff
python scripts/align-vocab.py 3                # should be a no-op

# Continue with remaining ASNs
python scripts/align-vocab.py 5
python scripts/align-vocab.py 7
# ...
```

Alignment is notation-only — state component names, property label prefixes, section
headings, type signatures. Proofs, math, and prose content are preserved. Uses opus
by default (needs semantic understanding to map property labels by meaning, not number).

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
| `extract-vocab.py` | Extract vocabulary from ASNs, detect notation conflicts (sonnet) |
| `align-vocab.py` | Align ASN notation to canonical vocabulary (opus, with tools) |

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
| `extract-vocab.md` | `extract-vocab.py` | Vocabulary extraction + conflict detection |
| `align-vocab.md` | `align-vocab.py` | ASN notation alignment to canonical vocabulary |

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
