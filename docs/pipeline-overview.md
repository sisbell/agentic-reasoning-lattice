# Pipeline Overview

Formal specification of the Xanadu hypertext system (udanax-green), derived from two independent authorities: Ted Nelson's design intent (Literary Machines) and Roger Gregory's implementation (udanax-green C source). The pipeline constructs a formal model — not documentation — from which properties are derived, verified, and compiled into a reference implementation.

## The Two Authorities

The pipeline draws on two structurally independent evidence channels:

- **Nelson** — design intent from Literary Machines and related writings. Speaks in design vocabulary: content, identity, permanence, links, documents, sharing, versions. No implementation terms.
- **Gregory** — implementation evidence from the udanax-green codebase and knowledge base. Speaks in technical vocabulary: I-addresses, V-space, spanfilade, subspaces, enfilades, tumblers.

The vocabulary firewall between channels is enforced at the prompt level. This is not a preference — it is structural. If Nelson can use implementation terms, the resulting properties couple to one realization instead of generalizing across implementations. See [Expert Consultation](expert-consultation.md) for details.

## Pipeline Stages

```
inquiries.yaml
     |
     v
+-----------+     Nelson (Literary Machines)
|   draft   | --> Gregory (KB + udanax-green)
+-----------+
     |
  ASN draft
     |
     +---------------------------+
     |                           |
     v                           v
+-----------+             +-----------+
|  review   | <-- cycle   |  promote  | --> inquiries.yaml
+-----------+             +-----------+     (new inquiries)
     |
     v (converged)
+-----------+
|   alloy   |  bounded model checking (counterexample search)
+-----------+
     |
     v (no counterexamples)
+-----------+
|   index   |  classify & label properties
+-----------+
     |
+-----------+
| statements|  extract formal statements from ASN prose
+-----------+
     |
+-----------+
|   dafny   |  generate, verify, write STATUS.md, commit
+-----------+
     |
     ├── unverified → model.py fix N (iterate)
     │                    |
     │                    v
     │              model.py status N (re-verify, commit)
     │
     └── [YOU] read STATUS.md, decide if ready
              |
              v
+-----------+
|  review   |  generate divergence review, commit
+-----------+
     |
     v
[YOU] read review
     ├── CONVERGED → promote to vault/proofs/
     └── REVISE → consult → revise → re-run dafny
     |
     v (promoted)
  Go (compiled) -- verified reference implementation / test oracle
```

## What Each Stage Does

### 1. Discovery (draft)

Turns an inquiry into a new ASN. Decomposes the inquiry into sub-questions for Nelson and Gregory, runs parallel consultations, then synthesizes the answers into a formal ASN using Dijkstra-style derivation.

- **Input:** inquiry from `vault/project-model/ASN-NNNN/project.yaml`
- **Output:** ASN file in `vault/asns/ASN-NNNN-title.md`
- **Human gate (foundation ASNs only):** After consultation, curate questions and answers for layer scope before discovery. See [Consultation Curation](consultation-curation.md).
- **Details:** [Discovery](discovery.md)

### 2. Review/Revise (review + revise)

Two separate commands: `review.py` produces a Dijkstra-style rigor check (correctness, consistency, completeness, clarity) and stops. `revise.py` picks up the findings, runs targeted expert consultations, and revises the ASN. With `--converge`, the revise command loops review → consult → revise until CONVERGED.

- **Input:** ASN in `vault/asns/`
- **Output:** revised ASN, review files in `vault/2-review/ASN-NNNN/`
- **Details:** [Review](review.md)

### 3. Promotion (promote)

Extracts new work from completed ASNs. Open questions and OUT_OF_SCOPE items from reviews are evaluated — questions worth investigating become new inquiries in `inquiries.yaml`.

- **Input:** ASN open questions, review OUT_OF_SCOPE items
- **Output:** new entries in `vault/1-promote/inquiries.yaml`
- **Details:** [Promotion](promotion.md)

### 4. Alloy Bounded Checking (model alloy)

Per-property Alloy model generation and bounded model checking. Searches for counterexamples before investing in full proof. Counterexamples produce a review; revision is handled separately by `revise.py`.

- **Input:** converged ASN
- **Output:** `.als` files in `vault/4-modeling/alloy/ASN-NNNN/`
- **Details:** [Alloy Checking](alloy-checking.md)

### 5. Modeling (model index, statements, dafny)

Three-step path from ASN prose to verified Dafny:

1. **Proof index** — classify each property by type (INV/PRE/POST/FRAME/LEMMA), assign descriptive proof labels
2. **Statement extraction** — pull formal statements from ASN prose into compact Dafny-ready format
3. **Dafny generation** — translate statements into verified Dafny, write STATUS.md, commit
4. **Fix** — fix unverified files iteratively (no commit — iterate freely)
5. **Status** — re-verify, update STATUS.md, commit
6. **Review** — triage divergences from verified files, write review, commit

- **Input:** converged ASN
- **Output:** proof index, formal statements, Dafny in `vault/4-modeling/dafny/ASN-NNNN/modeling-N/`, review in `vault/2-review/`
- **Human gate:** You read STATUS.md after dafny/fix/status. When ready, trigger review. You read the review, then decide whether to run consult → revise or promote verified files to `vault/proofs/`.
- **Details:** [Modeling](modeling.md)

### 6. Fix (model fix)

Agentic baby-steps fixer for unverified Dafny files. Reads the file and verification errors, adds one proof element at a time until verification passes.

- **Input:** unverified `.dfy` files from a modeling directory
- **Output:** fixed `.dfy` files (in place)
- **Details:** [Dafny Verification Loop](dafny-verification-loop.md)

## Feedback Loops

The pipeline is not linear — it has structured feedback loops:

1. **Review → Revise → Review** — the inner convergence loop. Each review cycle tightens the ASN until no significant issues remain.
2. **Alloy → Review** — counterexamples from bounded checking feed back as review findings, triggering ASN revision.
3. **Dafny → Review → [You] → Revise** — Dafny review triages divergences and failures. You read the review and decide whether spec issues warrant a consult → revise cycle.
4. **Promote → Draft** — open questions and out-of-scope items from converged ASNs spawn new inquiries, growing the specification.

## Artifacts by Stage

| Stage | Reads | Writes |
|-------|-------|--------|
| Draft | `inquiries.yaml`, Nelson sources, Gregory KB | `vault/asns/ASN-NNNN-*.md`, `vault/experts/ASN-NNNN/` |
| Review | ASN, `vocabulary.md`, prior reviews | `vault/2-review/ASN-NNNN/review-N.md`, revised ASN |
| Promote | ASN open questions, review OUT_OF_SCOPE items | `vault/1-promote/inquiries.yaml`, `vault/1-promote/ASN-NNNN/` |
| Alloy | ASN, proof index | `vault/4-modeling/alloy/ASN-NNNN/*.als` |
| Index | ASN, existing proof index | `vault/4-modeling/proof-index/ASN-NNNN-proof-index.md` |
| Statements | ASN, proof index | `vault/project-model/ASN-NNNN/formal-statements.md` |
| Dafny | statements, proof index, proof imports | `modeling-N/*.dfy`, `modeling-N/STATUS.md` (commits) |
| Fix | unverified `.dfy` files | fixed `.dfy` files (in place, no commit) |
| Status | `.dfy` files in modeling dir | `modeling-N/STATUS.md` (commits) |
| Review | verified `.dfy` files, statements | `vault/2-review/ASN-NNNN/review-N.md` (commits) |

## CLI Quick Reference

All commands run from the project root as `python scripts/<dispatcher>.py`.

| Command | Purpose |
|---------|---------|
| `draft.py --inquiries N` | Discovery pipeline for inquiry N |
| `review.py N` | Review ASN-N (produce findings, stop) |
| `revise.py N --converge` | Revise ASN-N until converged |
| `promote.py questions N` | Evaluate ASN-N open questions |
| `promote.py scope N` | Evaluate ASN-N review OUT_OF_SCOPE items |
| `model.py alloy N` | Alloy bounded checking for ASN-N |
| `model.py index N` | Classify and label properties |
| `export.py N` | Extract formal statements |
| `model.py dafny N` | Generate Dafny per-property, commit |
| `model.py fix N` | Fix unverified Dafny files with baby-steps |
| `model.py status N` | Re-verify all .dfy files, write STATUS.md, commit |
| `model.py review N` | Generate divergence review from verified files, commit |
| `model.py verify-dafny N` | Verify + fix loop |
| `consult.py nelson "question"` | Ad-hoc Nelson consultation |
| `consult.py gregory "question"` | Ad-hoc Gregory consultation |
| `commit.py` | Commit vault changes (excludes proofs) |
| `commit.py --proofs-only` | Commit vault/proofs/ only (manual promotion) |

See individual docs for full flag reference.

## Shortcuts (`run/`)

Shell scripts that chain common multi-step workflows. Run from the project root.

| Shortcut | Equivalent |
|----------|------------|
| `./run/asn-converge.sh N` | `review.py N` → `revise.py N --converge` |
| `./run/remodel.sh N` | `model.py index N` → `statements N` → `dafny N` |
| `./run/remodel.sh N --property TA3,TA3-strict` | Same, filtered to specific properties |

Use `run/asn-converge.sh` to review and revise an ASN until converged. Use `run/remodel.sh` after revision to regenerate the proof index, statements, and Dafny in one shot.

**Note:** When a review returns VERDICT: CONVERGED with minor REVISE items, the converge script stops without applying the revisions. To get a clean exit, run `python scripts/lib/review_revise.py N` manually, then re-run `./run/asn-converge.sh N` for a final clean review.

## When to Use Each Command

**Starting new work:**
- Have an inquiry in `inquiries.yaml`? → `draft.py --inquiries N`
- Need to investigate something ad-hoc? → `consult.py nelson/gregory "question"`

**Improving an ASN:**
- ASN needs rigor checking? → `review.py N` (produces findings, stops)
- Ready to revise from findings? → `revise.py N`
- Full loop until converged? → `review.py N` then `revise.py N --converge`

**After convergence:**
- Search for counterexamples first → `model.py alloy N`
- Ready for modeling → `model.py index N` then `statements N` then `dafny N`
- Fix proof limitations → `model.py fix N`, then `model.py status N`
- Ready for review → `model.py review N`
- Full pipeline in one shot → `model.py verify-dafny N --full`

**Growing the specification:**
- ASN has open questions worth investigating? → `promote.py questions N`
- Reviews flagged out-of-scope topics? → `promote.py scope N`

## Related Documents

- [Discovery](discovery.md) — creating new ASNs
- [Review](review.md) — review and revision cycles
- [Expert Consultation](expert-consultation.md) — Nelson and Gregory channels
- [Modeling](modeling.md) — from ASN to Dafny
- [Alloy Checking](alloy-checking.md) — bounded model checking
- [Dafny Verification Loop](dafny-verification-loop.md) — three-tier failure handling
- [Promotion](promotion.md) — feeding the pipeline
- [Consultation Curation](consultation-curation.md) — manual scope trimming for foundation ASNs
- [Foundations](foundations.md) — verified building blocks (Types/State/Invariants)
- [Methodology](methodology.md) — design principles
