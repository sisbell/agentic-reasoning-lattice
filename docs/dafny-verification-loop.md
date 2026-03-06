# Dafny Verification Loop — Three-Tier Failure Handling

## Motivation

The formalization pipeline runs linearly: `contract-asn.py` → `extract-properties.py` → `generate-dafny.py`. When Dafny verification fails, there is no automated way to fix and retry. Dafny errors range from trivial syntax issues to fundamental spec errors requiring revision of the ASN itself.

**Key constraint:** LLMs cannot truly reason about Dafny proofs — they can pattern-match on error messages and apply known fixes, but they cannot construct novel proof strategies. The loop must be conservative: fix what is obviously fixable, escalate everything else.

## Three Tiers of Dafny Failure

| Tier | Category | Examples | Fix location | Automated? |
|------|----------|----------|-------------|------------|
| 1 | Syntax/type | Missing import, type mismatch, wrong arity, undeclared identifier | `.dfy` file | Yes — inner loop |
| 2 | Proof-structural | Proof timeout, insufficient trigger, missing assert hint, wrong case split | `.dfy` file (with ASN/extract context) | Partially — needs extract context |
| 3 | Spec error | Property is wrong, precondition too weak, invariant doesn't hold on valid states | ASN → re-review → re-extract → re-generate | No — escape to ASN review cycle |

## Loop Architecture

```
generate-dafny.py → .dfy file
         │
         ▼
  ┌─ verify-dafny.py ──────────────────────┐
  │  dafny verify ASN-NNNN.dfy             │
  │     │                                   │
  │     ├─ pass → done                      │
  │     │                                   │
  │     └─ fail → categorize errors         │
  │          │                              │
  │          ├─ Tier 1 → fix-dafny.py ──┐   │
  │          │       (syntax/type fix)  │   │
  │          │       re-verify ◄────────┘   │
  │          │       (max 3 inner loops)    │
  │          │                              │
  │          ├─ Tier 2 → fix-dafny.py ──┐   │
  │          │  (proof fix w/ context)  │   │
  │          │  re-verify ◄─────────────┘   │
  │          │  (max 2 inner loops)         │
  │          │                              │
  │          └─ Tier 3 → ESCAPE             │
  │               generates review finding  │
  │               → run-review.py --resume  │
  │               → re-extract, re-generate │
  └─────────────────────────────────────────┘
```

## Error Categorization Heuristics

### Tier 1 signals (fix in Dafny)

- `Error: unresolved identifier`, `Error: wrong number of arguments`
- `Error: type mismatch`, `Error: member ... does not exist`
- `Error: invalid UnaryExpression`
- Any error on a line that is pure Dafny syntax (not a property translation)

### Tier 2 signals (proof-structural)

- `Error: A postcondition might not hold` — the ensures clause cannot be proved
- `Error: assertion might not hold` — an intermediate assertion fails
- Verification timeout (> configured limit)
- `Error: decreases expression might not decrease` — termination
- Errors referencing `lemma` bodies

### Tier 3 signals (spec error — escape)

- Tier 2 fix attempted and failed twice
- Error says `requires ... might not hold` on a *caller* (property is internally inconsistent)
- Manual review of Tier 2 failure reveals the property statement itself is wrong

## Escalation Rules

- Tier 1 failures get 3 fix attempts. After 3, escalate to Tier 2.
- Tier 2 failures get 2 fix attempts. After 2, escalate to Tier 3.
- Tier 3 generates a synthetic review finding and exits with a distinct code.

## Scripts

| Script | Role |
|--------|------|
| `verify-dafny.py` | Run `dafny verify`, parse errors, classify tiers, write verification report |
| `fix-dafny.py` | LLM-assisted fix — read errors + `.dfy` + context, produce patched `.dfy` |
| `run-dafny.py` | Orchestrator — full loop with tier escalation (analogous to `run-review.py`) |

## Tier 3 Escalation Output

When the loop exhausts fix attempts, it writes an escalation report:

```markdown
# Dafny Escalation — ASN-NNNN

## Property: [proof label from proof index]

**ASN label:** T4 — Monotonic allocation
**Error:** A postcondition might not hold on line 47
**Fix attempts:** 2
**Assessment:** The invariant as stated does not hold for the empty-state base case.
The ASN property T4 may need a precondition requiring non-empty allocation state.

## Recommended action

Re-run review-revise cycle with this finding as input.
```

This file can be manually fed to `run-review.py` or (future) automatically injected as a review finding.

## Full Pipeline Mode

`run-dafny.py --full` runs the complete formalization pipeline:

1. `contract-asn.py` (if contract stale or missing)
2. `extract-properties.py` (if extract stale or missing)
3. `generate-dafny.py` (always — fresh generation)
4. Verification loop (this plan)

Staleness check: compare file mtimes. If ASN is newer than contract, regenerate contract. If contract is newer than extract, regenerate extract.
