# Cheat Sheet — Human Operator Guide

## When You Need to Get Involved

| Pipeline produces... | You decide... |
|----------------------|---------------|
| OUT_OF_SCOPE items | Which gaps matter? What to investigate next? |
| Promoted inquiry candidates | Worth a new ASN? Priority? |
| Dafny review (REVISE items) | Is this a real spec issue or a proof limitation? |
| Tier 3 escalation | Is the ASN property wrong, or the proof approach? |
| Golden test failure | Is the spec wrong, or the test wrong? |
| CONVERGED verdict | Ready for modeling, or run more cycles? |

Everything else — ASN review, revise, consult, fix — is delegated. Dafny reviews require your sign-off before revising the ASN.

## Pipeline State Diagram

```
                    [YOU] write inquiry
                           |
                           v
  ┌──────────────────────────────────────────────┐
  │              DISCOVERY (automated)           │
  │  draft.py --inquiries N                      │
  │  questions → consult → discover → commit     │
  └──────────────────────────────────────────────┘
                           |
                        ASN draft
                           |
                           v
  ┌──────────────────────────────────────────────┐
  │              REVIEW (automated)              │
  │  review.py N         (findings, stop)        │
  │  revise.py N --converge  (consult→revise loop)│
  └──────────────────────────────────────────────┘
                           |
              CONVERGED ───┼──── OUT_OF_SCOPE items
                           |         |
                           |         v
                           |    [YOU] read OUT_OF_SCOPE items
                           |    promote.py questions N
                           |    promote.py scope N
                           |         |
                           |         v
                           |    [YOU] accept/reject new inquiries
                           |         |
                           |         └──→ inquiries.yaml (loops back to top)
                           |
                           v
  ┌──────────────────────────────────────────────┐
  │            ALLOY CHECK (automated)           │
  │  model.py alloy N                            │
  └──────────────────────────────────────────────┘
                           |
              pass ────────┼──── counterexample
                           |         |
                           |         v
                           |    (auto-revise, or [YOU] inspect)
                           |
                           v
  ┌──────────────────────────────────────────────┐
  │          FORMALIZATION (automated)           │
  │  normalize.py N                                  │
  │  model.py index N                            │
  │  model.py dafny N  (generate, STATUS, commit)│
  └──────────────────────────────────────────────┘
                           |
              ┌────────────┴────────────┐
              │ unverified              │ all verified
              v                         │
       model.py fix N                   │
       model.py status N (commit)       │
              │                         │
              └────────────┬────────────┘
                           │
                    [YOU] read STATUS.md
                           │
                           v
  ┌──────────────────────────────────────────────┐
  │          REVIEW (human-triggered)            │
  │  model.py review N  (review + commit)        │
  └──────────────────────────────────────────────┘
                           |
                    [YOU] read review
                           |
              ┌────────────┴────────────┐
              v                         v
     CONVERGED       SIMPLIFY              REVISE
     promote to      fix .dfy manually,   revise.py N →
     vault/proofs/   re-run review        ./run/remodel.sh N
```

## Typical Session Workflows

### Start a new topic
```bash
# 1. Add inquiry to inquiries.yaml (or use promote.py)
# 2. Run discovery
python scripts/draft.py --inquiries N
# 3. Review, then revise until converged
./run/asn-converge.sh N
# 4. Read OUT_OF_SCOPE items, promote what matters
python scripts/promote.py questions N
python scripts/promote.py scope N
```

### Formalize a converged ASN
```bash
# 1. Alloy pre-check
python scripts/model.py alloy N
# 2. Generate Dafny (generates, verifies, STATUS.md, commits)
./run/remodel.sh N
# 3. Read STATUS.md — any unverified? Fix and re-check
python scripts/model.py fix N
python scripts/model.py status N        # re-verify + commit
# 4. When ready, generate review (human-triggered)
python scripts/model.py review N        # review + commit
# 5. Read review in vault/2-review/ASN-NNNN/
#    - CONVERGED? → promote
#    - REVISE items? → revise.py N, then ./run/remodel.sh N
# 6. Promote verified files to vault/proofs/ (manual copy + proofs-only commit)
cp vault/4-modeling/dafny/ASN-NNNN/modeling-N/*.dfy vault/proofs/ModuleName/
python scripts/commit.py --proofs-only "promote ModuleName from modeling-N"
```

### Investigate something ad-hoc
```bash
python scripts/consult.py nelson "What does Nelson mean by withdrawal?"
python scripts/consult.py gregory "How does INSERT handle span boundaries?"
```

### Fire and forget (up to review gate)
```bash
# Draft + converge + generate Dafny (stops at review — you read it)
python scripts/draft.py --inquiries N && \
./run/asn-converge.sh N && \
./run/remodel.sh N
```

## Your Reading List (What to Actually Look At)

| Artifact | When | Why |
|----------|------|-----|
| `vault/1-promote/inquiries.yaml` | Before drafting | What's queued |
| OUT_OF_SCOPE items in latest review | After convergence | What's not covered yet |
| Promotion decisions | After `promote.py` | Which new inquiries were created |
| STATUS.md | After `dafny`, `fix`, or `status` | What verified, what didn't, divergences, fix history |
| Dafny review | After `model.py review N` | Divergences and quality (verified files only) |
| Golden test failures | After compiling Go oracle | Spec vs. reality disagreements |

**What you don't need to read:** ASN property details, consultation transcripts, Dafny source (except when the review flags a spec issue). These are for the machines.
