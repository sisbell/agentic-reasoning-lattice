# Alloy Verification Pipeline

## Steps

### Step 1: Translate (`scripts/model.py alloy`)

**Prompt:** `translate-claim.md` + `syntax-reference.md` + `reference.als`
**Script:** `scripts/lib/verification/alloy.py` → `generate_one()`

Per-claim translation. Agent converts a formal contract into an
Alloy model with sigs, predicates, assertions, and check commands.
Runs the Alloy checker and fixes syntax errors in a loop.

### Step 2: Check (mechanical, inline after translation)

Run Alloy bounded model checker. Three outcomes:
- **UNSAT** on check commands — no counterexample found within scope
- **SAT** on check commands — counterexample found
- **Syntax error** — shouldn't happen after translate self-correction

### Step 3: Validate (`scripts/lib/verification/alloy.py` → `contract_review_one()`)

**Prompt:** `validate-contract.md`

Compare Alloy facts/asserts against formal contract fields.
Output: CLEAN or FLAG with detailed mismatch description.
A missing assertion means the counterexample search won't cover
that postcondition.

### Step 4: Align → Validate cycle (`scripts/lib/verification/alloy.py` → `align_validate_cycle()`)

**Prompt:** `align-with-contract.md`

When validate returns FLAG, the model doesn't match the contract.
The align agent fixes the mismatch using CoT: read contract → read
error → find divergence → fix minimally.

Cycle: align → check → validate → if not CLEAN, feed errors back
(max 3 cycles). The formal contract is authoritative — align never
weakens assertions or removes checks.

## Prompt files

| File | Purpose |
|------|---------|
| `translate-claim.md` | Translate formal contract to Alloy (Jackson priming) |
| `syntax-reference.md` | Alloy syntax reference injected into translation |
| `reference.als` | Reference patterns for Alloy modeling |
| `validate-contract.md` | Gate check: does Alloy match formal contract? (Jackson priming) |
| `align-with-contract.md` | Fix model to match contract with CoT (Jackson priming) |
