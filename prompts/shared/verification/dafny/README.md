# Dafny Verification Pipeline

## Steps

### Step 1: Translate (`scripts/dafny.py`)

**Prompt:** `translate-claim.md` + `dafny-reference.dfy`
**Script:** `scripts/lib/verification/dafny/translate.py`
**Function:** `translate_one()`

Per-claim translation. Agent converts a formal contract into verified
Dafny code (up to 24 turns). Uses claim-statements.md as input, proof
modules from `lattices/<lattice>/verification/proofs/` as imports.

The agent writes the .dfy file, runs `dafny verify`, and self-corrects
incrementally until the solver accepts the proof.

### Step 2: Verify (`scripts/lib/verification/dafny/verify.py`)

**Function:** `verify(path)`

Three-way mechanical check:
- **verified** — solver accepts, proceed to validation
- **proof_failure** — compiles but solver rejects proof
- **compile_failure** — doesn't compile after 24 turns (generation failure)

### Step 3: Validate (`scripts/lib/verification/dafny/validate.py`)

**Prompt:** `validate-contract.md`
**Function:** `validate(dafny_source, formal_contract, label)`

Compare Dafny requires/ensures against formal contract fields.
Output: CLEAN or FLAG with detailed mismatch description.
Only runs on verified code.

Batch mode: `validate_batch(asn_num, verification_dir)`

### Step 4: Align → Validate cycle (`scripts/lib/verification/dafny/align.py`)

**Prompt:** `align-with-contract.md`
**Function:** `align_validate_cycle(dfy_path, formal_contract, label)`

When validate returns FLAG, the code verified but drifted from the
formal contract. The align agent fixes the drift using CoT:
read contract → read error → find mismatch → fix minimally.

Cycle: align → verify → validate → if not CLEAN, feed errors back
(max 3 cycles). Errors can be contract flags OR dafny verify failures
— both feed back as input to the next align attempt.

The formal contract is authoritative — align never weakens ensures
or strengthens requires.

Also provides standalone fix entry point via `align.py main()` for
.dfy files with proof failures from Step 2.

## Prompt files

| File | Purpose |
|------|---------|
| `translate-claim.md` | Translate formal contract to Dafny (Leino priming) |
| `dafny-reference.dfy` | Verified pattern examples injected into translation |
| `validate-contract.md` | Gate check: does Dafny match formal contract? (Leino priming) |
| `align-with-contract.md` | Fix proof to match contract with CoT (Leino priming) |

## Script files

| File | Purpose |
|------|---------|
| `scripts/dafny.py` | Top-level wrapper → translate.py |
| `scripts/lib/verification/dafny/translate.py` | Generation loop + orchestration |
| `scripts/lib/verification/dafny/verify.py` | Mechanical dafny verify (three-way) |
| `scripts/lib/verification/dafny/validate.py` | Contract validation (CLEAN/FLAG) |
| `scripts/lib/verification/dafny/align.py` | Contract alignment + fix cycle |
| `scripts/lib/verification/dafny/common.py` | Shared utilities |
