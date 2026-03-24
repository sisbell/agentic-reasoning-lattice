# Foundation Audit

You are auditing an ASN for cross-boundary issues with its foundation. Your job is to find problems — not fix them. Report every issue precisely so that a reviewer can prescribe fixes.

## Foundation Statements (current)

{{foundation_statements}}

## ASN Content

{{asn_content}}

## ASN Metadata

- **ASN**: {{asn_label}}
- **Declared depends**: {{depends}}

## Existing Open Issues

{{open_issues}}

## Audit

Read the foundation statements carefully, then read the ASN. Check for the following cross-boundary issues. For each finding, cite the specific foundation property and the specific ASN text.

**Do not report issues already captured in "Existing Open Issues" above.** Only report new findings.

### 1. Stale Labels

The ASN cites a foundation property by an old label that no longer exists in the foundation.

### 2. Local Redefinitions

The ASN defines a property locally (status `introduced`) that already exists in the foundation statements. These should be `cited`.

### 3. Unjustified Domain Extensions

The ASN introduces a function or property that reuses a foundation function's name or formula but applies it to a domain the foundation does not cover. This is a finding even if the registry correctly says `introduced`. Look for cases where the ASN applies a foundation function to addresses, stores, or subspaces outside the foundation function's stated domain.

### 4. Incomplete Precondition Transfer

When the ASN extends a foundation result to a new domain, check whether all preconditions of the foundation result have been accounted for. Foundation statements include "Follows from" lists — each prerequisite must either (a) apply unchanged in the new domain, with explicit justification, or (b) have an explicit analog established by the ASN. A finding occurs when the ASN claims the extension holds but does not address one or more prerequisites from the Follows-from list.

### 5. Structural Drift

The ASN uses or restates a foundation definition but with outdated content — the foundation has changed and the ASN still uses the old version.

### 6. Missing Dependencies

The ASN references properties from a foundation ASN that is NOT in its declared depends list.

### 7. Registry Misclassification

The properties table lists a property as `introduced` or `cited` but the body text contradicts this — a property listed as `cited` that contains a local proof, or a property listed as `introduced` that merely restates a foundation statement.

## Output Format

For each finding, use this format:

```
### [CATEGORY]: [brief title]
**Foundation**: [which foundation property, with its Follows-from list if relevant]
**ASN**: [which ASN section/property, with quoted text]
**Issue**: [what is wrong — be specific about the gap]
**What needs resolving**: [what the ASN must establish or change, without prescribing how]
```

If no new issues are found beyond what is already in "Existing Open Issues," write:

```
NO NEW ISSUES
```
