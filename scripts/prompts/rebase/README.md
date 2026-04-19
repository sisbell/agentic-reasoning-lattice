# Dependency Rebase Pipeline

Validates that an ASN's references to its upstream dependencies are
correct. Runs at any stage — discovery or formalization.

## Steps

### Pass 1: Mechanical (deterministic)

**Script:** `scripts/lib/rebase/reviewer.py` → `check_asn()`
**No prompt — uses** `scripts/lib/formalization/mechanical.py`

Stale labels, missing deps, undeclared cross-ASN references,
prose-only citations. Deterministic, no LLM.

### Pass 2: Cross-reference (LLM, per-claim)

**Prompt:** `review.md`
**Script:** `scripts/lib/rebase/reviewer.py` → `_check_cross_references()`

Three sub-checks:
- Inline name mismatches (deterministic) — T5 cited as wrong name
- Redefinitions (deterministic) — local claim re-derives upstream
- LLM semantic check — deeper comparison for existing upstream refs

### Pass 3: Extension verification (LLM, formalization-only)

**Prompts:** `formalization/rebase/domain-extensions.md`,
`formalization/rebase/transfer-verification.md`,
`formalization/rebase/focused-judgment.md`
**Script:** `scripts/lib/rebase/reviewer.py` → `_check_extensions()`

Verifies extends/parallels claims against formal contracts.
Only produces findings for formalized ASNs with dependency graphs.

### Pass 4: Dependency report (LLM, whole-ASN)

**Prompt:** `shared/dependency-report.md`
**Script:** `scripts/lib/rebase/reviewer.py` → `_check_dependency_report()`

Whole-ASN check for issues per-claim passes can't see:
- Structural drift — foundation changed, ASN uses old version
- Registry misclassification — table says cited but body has local proof
- Exhaustiveness gaps — claims "all" but foundation has items not covered

### Revise (on findings)

**Prompt:** `revise.md`
**Script:** `scripts/lib/rebase/reviser.py`

Finding-driven reviser. Mechanical name fixes applied directly
(no LLM). Other findings go through LLM reviser with Edit tools.

## Convergence

Default: full sweep (all claims each cycle). Also supports
incremental (dirty set + downstream dependents). Cycle limit
protects against infinite retries.

## Prompt files

| File | Location | Purpose |
|------|----------|---------|
| `review.md` | `rebase/` | Per-claim cross-reference check |
| `revise.md` | `rebase/` | Finding-driven reviser |
| `dependency-report.md` | `shared/` | Whole-ASN dependency consistency |
| `domain-extensions.md` | `formalization/rebase/` | Find extension claims |
| `transfer-verification.md` | `formalization/rebase/` | Verify transfer soundness |
| `focused-judgment.md` | `formalization/rebase/` | Judge extension claims |

## Script files

| File | Purpose |
|------|---------|
| `scripts/rebase.py` | Top-level wrapper |
| `scripts/lib/rebase/pipeline.py` | Orchestrator with convergence loop |
| `scripts/lib/rebase/reviewer.py` | Four review passes |
| `scripts/lib/rebase/reviser.py` | Finding-driven fixes |
