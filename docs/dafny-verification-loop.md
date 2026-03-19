# Dafny Verification Loop — Three-Tier Failure Handling

## Purpose

The modeling pipeline runs linearly: `export.py` → `model.py index` → `model.py dafny`. Dafny errors range from trivial syntax issues to fundamental spec errors requiring revision of the ASN itself. The verification loop automates fix-and-retry for fixable errors and escalates everything else.

**Key constraint:** LLMs cannot truly reason about Dafny proofs — they can pattern-match on error messages and apply known fixes, but they cannot construct novel proof strategies. The loop is conservative: fix what is obviously fixable, escalate everything else.

## Three Tiers of Dafny Failure

| Tier | Category | Examples | Fix location | Automated? |
|------|----------|----------|-------------|------------|
| 1 | Syntax/type | Missing import, type mismatch, wrong arity, undeclared identifier | `.dfy` file | Yes — inner loop |
| 2 | Proof-structural | Proof timeout, insufficient trigger, missing assert hint, wrong case split | `.dfy` file (with ASN/extract context) | Partially — needs extract context |
| 3 | Spec error | Property is wrong, precondition too weak, invariant doesn't hold on valid states | ASN → human reads review → consult → revise | No — human gate after Dafny review |

## Loop Architecture

```
model.py dafny → .dfy file
         │
         ▼
  ┌─ model.py verify-dafny ────────────────┐
  │  dafny verify ASN-NNNN.dfy             │
  │     │                                   │
  │     ├─ pass → done                      │
  │     │                                   │
  │     └─ fail → categorize errors         │
  │          │                              │
  │          ├─ Tier 1 → model_fix.py ──┐   │
  │          │       (syntax/type fix)  │   │
  │          │       re-verify ◄────────┘   │
  │          │       (max 3 inner loops)    │
  │          │                              │
  │          ├─ Tier 2 → model_fix.py ──┐   │
  │          │  (proof fix w/ context)  │   │
  │          │  re-verify ◄─────────────┘   │
  │          │  (max 2 inner loops)         │
  │          │                              │
  │          └─ Tier 3 → ESCAPE             │
  │               generates review finding  │
  │               → revise.py N             │
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
| `lib/model_verify_run.py` | Run `dafny verify`, parse errors, classify tiers, write verification report |
| `lib/model_fix.py` | LLM-assisted fix — read errors + `.dfy` + context, produce patched `.dfy` |
| `lib/model_verify.py` | Orchestrator — full loop with tier escalation |

CLI: `python scripts/model.py verify-dafny N` runs the full loop.

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

The Dafny generation command (`model.py dafny`) writes `STATUS.md` and commits. Review is a separate human-triggered step (`model.py review N`) — run it when you're ready to triage divergences. Unverified files need `model.py fix` first, then `model.py status` to update STATUS.md and commit. If still unverified after fix, read `STATUS.md` and the .dfy source to triage manually.

## Full Pipeline Mode

`model.py verify-dafny N --full` runs the complete modeling pipeline:

1. `export.py N` (if statements stale or missing)
2. `model.py index N` (if proof index stale or missing)
3. `model.py dafny N` (always — fresh generation)
4. Verification loop (this document)

Staleness check: compare file mtimes. If ASN is newer than proof index, regenerate. If proof index is newer than statements, regenerate.

See also: [Modeling](modeling.md) for the full three-step path.
