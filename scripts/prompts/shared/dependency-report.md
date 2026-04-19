# Dependency Report

You are reporting dependency mismatches between an ASN and its upstream
foundations. Compare the ASN's text and claim table against the
foundation statements and report every inconsistency.

ASNs form a dependency DAG. Foundation ASNs are verified — their
exported statements are ground truth. Dependent ASNs cite foundation
claims. Each claim has a **Follows-from** list tracing its
derivation chain.

Report findings only — do not suggest fixes.

## Foundation Statements (current)

{{foundation_statements}}

## ASN Content

{{asn_content}}

## ASN Metadata

- **ASN**: {{asn_label}}
- **Declared depends**: {{depends}}

## Report

Read the foundation statements carefully, then read the ASN. Report
any dependency mismatches in the following categories. For each finding,
cite the specific line or claim.

### 1. Stale Labels

The ASN cites a foundation claim by an old label that no longer exists in the foundation.

### 2. Structural Drift

The ASN uses or restates a foundation definition but with outdated content — the foundation has changed and the ASN still uses the old version.

### 3. Local Redefinitions

The ASN defines a claim locally (status `introduced`) that already exists in the foundation statements. These should have been promoted to `cited` during a rebase.

Claims with status `confirms LABEL (ASN-NNNN)` intentionally re-derive a foundation result with an independent proof — do not flag them.

### 4. Registry Misclassification

The claims table lists a claim as `introduced` or `cited` but the body text contradicts this — a claim listed as `cited` that contains a local proof, or a claim listed as `introduced` that merely restates a foundation statement.

Claims with status `confirms LABEL (ASN-NNNN)` are expected to have a local proof — do not flag them as misclassified.

### 5. Missing Dependencies

The ASN references claims from a foundation ASN that is NOT in its declared depends list.

## Output Format

For each category, list findings or write "(none)". Be specific — quote the text and cite the foundation claim it conflicts with. At the end, write one of:

- `RESULT: CLEAN` — no findings in any category
- `RESULT: n FINDINGS` — where n is the total count
