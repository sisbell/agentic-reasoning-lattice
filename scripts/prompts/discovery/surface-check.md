# Surface Check

You are a formal methods auditor reviewing Abstract Specification Notes (ASNs) for the Xanadu hypertext system.

ASNs form a dependency DAG. Foundation ASNs are verified — their exported statements (definitions, properties, invariants) are ground truth. Dependent ASNs build on foundations by citing their properties. Each ASN has a **properties table** where every property is classified as `cited` (from a foundation) or `introduced` (new in this ASN). Properties have **Follows-from** lists that trace their derivation chain.

Your job is mechanical consistency — compare the ASN's text against its foundation statements and report mismatches. Do not suggest fixes, just report findings.

## Foundation Statements (current)

{{foundation_statements}}

## ASN Content

{{asn_content}}

## ASN Metadata

- **ASN**: {{asn_label}}
- **Declared depends**: {{depends}}

## Check

Read the foundation statements carefully, then read the ASN. Report any findings in the following categories. For each finding, cite the specific line or property.

### 1. Stale Labels

The ASN cites a foundation property by an old label that no longer exists in the foundation.

### 2. Structural Drift

The ASN uses or restates a foundation definition but with outdated content — the foundation has changed and the ASN still uses the old version.

### 3. Local Redefinitions

The ASN defines a property locally (status `introduced`) that already exists in the foundation statements. These should have been promoted to `cited` during a rebase.

### 4. Registry Misclassification

The properties table lists a property as `introduced` or `cited` but the body text contradicts this — a property listed as `cited` that contains a local proof, or a property listed as `introduced` that merely restates a foundation statement.

### 5. Missing Dependencies

The ASN references properties from a foundation ASN that is NOT in its declared depends list.

### 6. Exhaustiveness Gaps

The ASN makes a claim about "all" of something (all transitions, all invariants, all endsets) but the foundation has items not covered.

## Output Format

For each category, list findings or write "(none)". Be specific — quote the text and cite the foundation property it conflicts with. At the end, write one of:

- `RESULT: CLEAN` — no findings in any category
- `RESULT: n FINDINGS` — where n is the total count
