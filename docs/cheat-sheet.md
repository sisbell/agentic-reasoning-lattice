# Cheat Sheet — Human Operator Guide

## When You Need to Get Involved

| Pipeline produces... | You decide... |
|----------------------|---------------|
| OUT_OF_SCOPE items | Which gaps matter? What to investigate next? |
| Promoted inquiry candidates | Worth a new ASN? Priority? |
| Dafny review (REVISE items) | Is this a real spec issue or a proof limitation? |
| Tier 3 escalation | Is the ASN property wrong, or the proof approach? |
| Golden test failure | Is the spec wrong, or the test wrong? |
| CONVERGED verdict | Ready for formalization, or run more cycles? |

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
  │  review.py N --converge                      │
  │  review → consult → revise → commit (loop)   │
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
  │  model.py index N                            │
  │  model.py statements N                       │
  │  model.py dafny N                            │
  │  (generates, verifies, STATUS.md + review)   │
  └──────────────────────────────────────────────┘
                           |
              ┌────────────┼────────────┐
              │ verified   │            │ unverified
              │ +divs      │            │
              v            │            v
       [YOU] read review   │     model.py fix N
              |            │            |
     CONVERGED / REVISE    │     [YOU] read STATUS.md
              |            │     triage remaining failures
              v            │            |
     consult → revise      │            v
     (if spec issues)      └──→ promote to vault/proofs/
```

## Typical Session Workflows

### Start a new topic
```bash
# 1. Add inquiry to inquiries.yaml (or use promote.py)
# 2. Run discovery
python scripts/draft.py --inquiries N
# 3. Run review until converged
python scripts/review.py N --converge
# 4. Read OUT_OF_SCOPE items, promote what matters
python scripts/promote.py questions N
python scripts/promote.py scope N
```

### Formalize a converged ASN
```bash
# 1. Alloy pre-check
python scripts/model.py alloy N
# 2. Generate Dafny (stops at review)
python scripts/model.py index N
python scripts/model.py statements N
python scripts/model.py dafny N
# 3. Generate STATUS.md (or check existing one)
python scripts/model.py status N
#    - All verified? → read review, promote
#    - Unverified? → run fix, then re-check status
python scripts/model.py fix N
python scripts/model.py status N
# 4. Read review in vault/2-review/ASN-NNNN/ (covers verified files)
#    - CONVERGED? → promote
#    - REVISE items? → consult → revise, then re-run dafny
# 5. Still-unverified files with divergences? → manual triage
#    Read the .dfy source, decide if it's a spec issue
# 6. Promote verified files to vault/proofs/ (manual copy + proofs-only commit)
cp vault/3-modeling/dafny/ASN-NNNN/modeling-N/*.dfy vault/proofs/ModuleName/
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
python scripts/review.py N --converge && \
python scripts/model.py index N && \
python scripts/model.py statements N && \
python scripts/model.py dafny N
```

## Your Reading List (What to Actually Look At)

| Artifact | When | Why |
|----------|------|-----|
| `vault/1-promote/inquiries.yaml` | Before drafting | What's queued |
| OUT_OF_SCOPE items in latest review | After convergence | What's not covered yet |
| Promotion decisions | After `promote.py` | Which new inquiries were created |
| Dafny review | After `model.py dafny N` | Divergences and quality (verified files only) |
| STATUS.md | After `dafny` or `fix` | What verified, what didn't, divergences, fix history |
| Golden test failures | After compiling Go oracle | Spec vs. reality disagreements |

**What you don't need to read:** ASN property details, consultation transcripts, Dafny source (except when the review flags a spec issue). These are for the machines.
