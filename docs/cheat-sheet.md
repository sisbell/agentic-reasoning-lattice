# Cheat Sheet — Human Operator Guide

## When You Need to Get Involved

| Pipeline produces... | You decide... |
|----------------------|---------------|
| OUT_OF_SCOPE items | Which gaps matter? What to investigate next? |
| Promoted inquiry candidates | Worth a new ASN? Priority? |
| Tier 3 escalation | Is the ASN property wrong, or the proof approach? |
| Golden test failure | Is the spec wrong, or the test wrong? |
| CONVERGED verdict | Ready for formalization, or run more cycles? |

Everything else — review, revise, consult, fix — is delegated.

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
  └──────────────────────────────────────────────┘
                           |
                           v
  ┌──────────────────────────────────────────────┐
  │          VERIFICATION (automated)            │
  │  model.py verify-dafny N                     │
  │  Tier 1/2 fixes are automatic                │
  └──────────────────────────────────────────────┘
                           |
              verified ────┼──── Tier 3 escalation
                           |         |
                           v         v
                         done   [YOU] read escalation report
                                     Is the property wrong? → revise ASN
                                     Is the proof wrong? → adjust Dafny
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
# 2. Full formalization + verification
python scripts/model.py verify-dafny N --full
# 3. If Tier 3 escalation → read the report, decide next step
```

### Investigate something ad-hoc
```bash
python scripts/consult.py nelson "What does Nelson mean by withdrawal?"
python scripts/consult.py gregory "How does INSERT handle span boundaries?"
```

### Fire and forget
```bash
# Draft + converge + formalize (check back later)
python scripts/draft.py --inquiries N && \
python scripts/review.py N --converge && \
python scripts/model.py verify-dafny N --full
```

## Your Reading List (What to Actually Look At)

| Artifact | When | Why |
|----------|------|-----|
| `vault/1-promote/inquiries.yaml` | Before drafting | What's queued |
| OUT_OF_SCOPE items in latest review | After convergence | What's not covered yet |
| Promotion decisions | After `promote.py` | Which new inquiries were created |
| Tier 3 escalation reports | After `verify-dafny` | Properties the prover couldn't handle |
| Golden test failures | After compiling Go oracle | Spec vs. reality disagreements |

**What you don't need to read:** ASN property details, review REVISE items, consultation transcripts, Dafny source. These are for the machines.
