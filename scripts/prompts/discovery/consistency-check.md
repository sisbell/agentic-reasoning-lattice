# Foundation Consistency Check

You are auditing an ASN for consistency with its foundation statements. This is a read-only check — do not suggest fixes, just report findings.

## Foundation Statements (current)

{{foundation_statements}}

## ASN Content

{{asn_content}}

## ASN Metadata

- **ASN**: {{asn_label}}
- **Declared depends**: {{depends}}

## Check

Read the foundation statements carefully, then read the ASN. Report any inconsistencies in the following categories. For each finding, cite the specific line or property. These categories are not exhaustive — apply general reasoning to identify any cross-boundary inconsistency between the foundation and the ASN, even if it does not fit a listed category.

### 1. Stale Labels
The ASN cites a foundation property by an old label that no longer exists in the foundation.

### 2. Local Redefinitions
The ASN defines a property locally (status `introduced`) that already exists in the foundation statements. These should have been promoted to `cited` during a rebase.

### 2a. Unjustified Domain Extensions
The ASN introduces a function or property that reuses a foundation function's name or formula but applies it to a domain the foundation does not cover. This is a finding even if the registry correctly says `introduced`. Look for cases where the ASN applies a foundation function to addresses, stores, or subspaces outside the foundation function's stated domain.

### 2b. Incomplete Precondition Transfer
When the ASN extends a foundation result to a new domain, check whether all preconditions have been accounted for. Perform two checks:

**Mechanical check**: Find the foundation result's "Follows from" list in the foundation text. Copy it verbatim. Then check each prerequisite individually — does it apply unchanged in the new domain (with explicit justification), or does the ASN establish an explicit analog? A finding occurs when one or more prerequisites are unaccounted for.

**Principled check**: Beyond the explicit Follows-from list, check for implicit assumptions the foundation result relies on by context — quantifier domains, subspace restrictions, type constraints, level restrictions. These may not appear in the Follows-from list but are assumed by the foundation's scope.

### 2c. Transfer by Assertion
The ASN claims a foundation argument transfers to a new context using phrases like "by similar reasoning," "the same argument applies," or "the same N cases." Flag any such claim where the ASN does not show that each step of the original argument holds in the new context. The claim may be correct, but it must be verified, not asserted.

### 2d. Quantifier Domain Mismatch
A foundation property is quantified over a specific domain (e.g., "for all a ∈ D₁") and the ASN applies it to an element from a different domain D₂ without verifying membership in D₁ or establishing that the property holds on D₂.

### 2e. Scope Narrowing in Citations
The ASN cites a foundation property but silently drops conditions, cases, or prerequisites from the original. The citation looks correct but the ASN's usage does not account for the full scope of the foundation result.

### 3. Structural Drift
The ASN uses or restates a foundation definition but with outdated content — the foundation has changed and the ASN still uses the old version.

### 4. Missing Dependencies
The ASN references properties from a foundation ASN that is NOT in its declared depends list.

### 5. Exhaustiveness Gaps
The ASN makes a claim about "all" of something (all transitions, all invariants, all endsets) but the foundation has items not covered.

### 6. Registry Mismatches
The properties table lists a property as `introduced` or `cited` but the body text contradicts this — a property listed as `cited` that contains a local proof, or a property listed as `introduced` that merely restates a foundation statement.

## Output Format

For each category, list findings or write "(none)". Be specific — quote the text and cite the foundation property it conflicts with. At the end, write one of:

- `RESULT: CLEAN` — no findings in any category
- `RESULT: n FINDINGS` — where n is the total count
