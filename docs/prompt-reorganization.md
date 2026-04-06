# Prompt Reorganization Plan

## Current state

All prompts in flat directories under `scripts/prompts/`. Discovery and
formalization directories each have 20+ files mixed together with no
structure matching the pipeline they belong to.

## Proposed structure

```
scripts/prompts/
  discovery/
    core/                          # Core discovery pipeline
      discovery.md                 # methodology priming
      review.md                    # discovery review
      filter-questions.md          # question scope filtering
    consultation/                  # Expert consultation
      nelson-agent.md
      nelson-questions.md
      gregory-code-agent.md
      gregory-synthesis-agent.md
      gregory-questions.md
    manage/                        # ASN lifecycle operations
      absorb-base.md
      absorb-review.md
      absorb-revise.md
      absorb-source.md
      extend.md
      export.md
      promote-open-questions.md
      promote-out-of-scope.md
    patch/                         # Discovery patch pipeline
      patch.md
      patch-report.md
      patch-review.md
      patch-revise.md

  formalization/
    format/                        # Format gate
      normalize-format.md
      normalize-format-revise.md
    formalize/                     # Formalize pipeline (quality rewrite)
      quality-pass.md
      repair-section.md
    rebase/                        # Dependency Rebase pipeline
      review.md                    ← already here (scripts/prompts/rebase/)
      revise.md                    ← already here (scripts/prompts/rebase/)
    proof-review/                  # Proof Review pipeline
      verify-proof.md
      revise-proof.md              # finding-driven reviser (shared by multiple pipelines)
    cross-review/                  # Cross-cutting Review pipeline
      foundation-audit.md          ← from discovery/
    assembly/                      # Assembly pipeline
      trim-statements.md
      dep-scan.md
    audit/                         # Audit prompts used by rebase
      surface-check.md             ← from discovery/
      consistency-check.md         ← from discovery/
      dependency-audit.md          ← from discovery/
      domain-extensions.md         ← from discovery/
      transfer-verification.md     ← from discovery/
      focused-judgment.md
      extract-features.md

  modeling/
    dafny/                         # Dafny generation + review
      generate-dafny-property.md
      generate-dafny.md
      dafny-reference.dfy
      dafny-contract-review.md
      fix-dafny.md
      write-dafny-review.md
    alloy/                         # Alloy generation + review
      check-alloy-property.md
      check-alloy.md
      alloy-syntax.md
      alloy-reference.als
      alloy-contract-review.md
      fix-alloy.md
      write-alloy-review.md

  shared/                          # Cross-phase (stays)
    commit.md
    commit-proofs.md

  examples/                        # Stays
    generate.md
    review.md

  test-cases/                      # Stays
    codegen.md
    extract.md
    review.md
```

## Moves

| From | To |
|------|-----|
| `formalization/normalize-format.md` | `formalization/format/normalize-format.md` |
| `formalization/normalize-format-revise.md` | `formalization/format/normalize-format-revise.md` |
| `formalization/quality-pass.md` | `formalization/formalize/quality-pass.md` |
| `formalization/repair-section.md` | `formalization/formalize/repair-section.md` |
| `formalization/verify-proof.md` | `formalization/proof-review/verify-proof.md` |
| `formalization/revise-proof.md` | `formalization/proof-review/revise-proof.md` |
| `formalization/trim-statements.md` | `formalization/assembly/trim-statements.md` |
| `formalization/dep-scan.md` | `formalization/assembly/dep-scan.md` |
| `formalization/focused-judgment.md` | `formalization/audit/focused-judgment.md` |
| `formalization/extract-features.md` | `formalization/audit/extract-features.md` |
| `discovery/foundation-audit.md` | `formalization/cross-review/foundation-audit.md` |
| `discovery/surface-check.md` | `formalization/audit/surface-check.md` |
| `discovery/consistency-check.md` | `formalization/audit/consistency-check.md` |
| `discovery/dependency-audit.md` | `formalization/audit/dependency-audit.md` |
| `discovery/domain-extensions.md` | `formalization/audit/domain-extensions.md` |
| `discovery/transfer-verification.md` | `formalization/audit/transfer-verification.md` |
| `rebase/review.md` | `formalization/rebase/review.md` |
| `rebase/revise.md` | `formalization/rebase/revise.md` |
| `formalization/generate-dafny-property.md` | `modeling/dafny/generate-dafny-property.md` |
| `formalization/generate-dafny.md` | `modeling/dafny/generate-dafny.md` |
| `formalization/dafny-reference.dfy` | `modeling/dafny/dafny-reference.dfy` |
| `formalization/dafny-contract-review.md` | `modeling/dafny/dafny-contract-review.md` |
| `formalization/fix-dafny.md` | `modeling/dafny/fix-dafny.md` |
| `formalization/write-dafny-review.md` | `modeling/dafny/write-dafny-review.md` |
| `formalization/check-alloy-property.md` | `modeling/alloy/check-alloy-property.md` |
| `formalization/check-alloy.md` | `modeling/alloy/check-alloy.md` |
| `formalization/alloy-syntax.md` | `modeling/alloy/alloy-syntax.md` |
| `formalization/alloy-reference.als` | `modeling/alloy/alloy-reference.als` |
| `formalization/alloy-contract-review.md` | `modeling/alloy/alloy-contract-review.md` |
| `formalization/fix-alloy.md` | `modeling/alloy/fix-alloy.md` |
| `formalization/write-alloy-review.md` | `modeling/alloy/write-alloy-review.md` |
| `discovery/discovery.md` | `discovery/core/discovery.md` |
| `discovery/review.md` | `discovery/core/review.md` |
| `discovery/filter-questions.md` | `discovery/core/filter-questions.md` |
| `discovery/nelson-agent.md` | `discovery/consultation/nelson-agent.md` |
| `discovery/nelson-questions.md` | `discovery/consultation/nelson-questions.md` |
| `discovery/gregory-code-agent.md` | `discovery/consultation/gregory-code-agent.md` |
| `discovery/gregory-synthesis-agent.md` | `discovery/consultation/gregory-synthesis-agent.md` |
| `discovery/gregory-questions.md` | `discovery/consultation/gregory-questions.md` |
| `discovery/absorb-base.md` | `discovery/manage/absorb-base.md` |
| `discovery/absorb-review.md` | `discovery/manage/absorb-review.md` |
| `discovery/absorb-revise.md` | `discovery/manage/absorb-revise.md` |
| `discovery/absorb-source.md` | `discovery/manage/absorb-source.md` |
| `discovery/extend.md` | `discovery/manage/extend.md` |
| `discovery/export.md` | `discovery/manage/export.md` |
| `discovery/promote-open-questions.md` | `discovery/manage/promote-open-questions.md` |
| `discovery/promote-out-of-scope.md` | `discovery/manage/promote-out-of-scope.md` |
| `discovery/patch.md` | `discovery/patch/patch.md` |
| `discovery/patch-report.md` | `discovery/patch/patch-report.md` |
| `discovery/patch-review.md` | `discovery/patch/patch-review.md` |
| `discovery/patch-revise.md` | `discovery/patch/patch-revise.md` |

## Scripts that need PROMPTS_DIR updates

Each script that references a moved prompt needs its path constant updated.
This is mechanical — grep for the old path, replace with new. To be done
in a separate session after the moves.
