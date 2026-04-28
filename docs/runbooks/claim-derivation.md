# Runbook: Claim Derivation

## Prerequisites

- The note has converged through note convergence
- Working tree is clean (`git status`)
- Upstream dependencies are derived (their claim docs and substrate links exist)

## Steps

### 1. Run the full pipeline

```bash
python scripts/derive-claims.py <ASN>
```

Phases (each commits automatically):

1. **decompose** — mechanical `##` split + per-section LLM analysis → section yamls in `_workspace/claim-derivation/<asn>/sections/`
2. **enrich** — three LLM passes per claim (type, depends, signature) updating section yamls in place
3. **transclude** — project source-note regions as per-claim docs in `_docuverse/documents/claim/<asn>/`; emit substrate links (`claim`, `contract.<kind>`, `citation`, `label`, `name`, `provenance.derivation`)
4. **validate-transclude** — substring check: each claim body is a byte-substring of its source note (Claim File Contract invariant 12 at transclude exit)
5. **produce-contract** — synthesize Formal Contract section in each claim's body markdown
6. **validate-gate** — comprehensive Claim File Contract validator with bounded structural-only fix recipes; same gate claim convergence runs before each review cycle

Pipeline returns success when the gate reports clean. On failure, partial output is left in place with diagnostic; downstream stages do not operate on a failed derivation.

### 2. Individual phase re-runs (debugging)

```bash
python scripts/derive-claims-split.py <ASN>
python scripts/derive-claims-enrich.py <ASN>
python scripts/derive-claims-transclude.py <ASN>          # accepts --dry-run
python scripts/derive-claims-validate-transclude.py <ASN>
python scripts/derive-claims-produce-contract.py <ASN>    # accepts --force / --label
```

---

See the [claim derivation guide](../guides/claim-derivation.md) for how the pipeline stages work, output structure, and design decisions. Protocol details in the [Claim Derivation Module](../protocols/claim-derivation-module.md).
