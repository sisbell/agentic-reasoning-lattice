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

Read the foundation statements carefully, then read the ASN. Check for the following cross-boundary issues. For each finding, cite the specific foundation property and the specific ASN text. These categories are not exhaustive — apply general reasoning to identify any cross-boundary inconsistency between the foundation and the ASN, even if it does not fit a listed category.

**Do not report issues already captured in "Existing Open Issues" above.** Only report new findings.

### 1. Stale Labels

The ASN cites a foundation property by an old label that no longer exists in the foundation.

### 2. Local Redefinitions

The ASN defines a property locally (status `introduced`) that already exists in the foundation statements. These should be `cited`.

### 3. Unjustified Domain Extensions

The ASN introduces a function or property that reuses a foundation function's name or formula but applies it to a domain the foundation does not cover. This is a finding even if the registry correctly says `introduced`. Look for cases where the ASN applies a foundation function to addresses, stores, or subspaces outside the foundation function's stated domain.

Example: Foundation defines `f(x)` for `x ∈ D₁`. ASN writes `g(x) = f(x)` for `x ∈ D₂` without justifying why `f` is well-defined on `D₂`.

### 4. Incomplete Precondition Transfer

When the ASN extends a foundation result to a new domain, check whether all preconditions have been accounted for. Perform two checks:

**Mechanical check**: Find the foundation result's "Follows from" list in the foundation text. Copy it verbatim. Then check each prerequisite individually — does it apply unchanged in the new domain (with explicit justification), or does the ASN establish an explicit analog? A finding occurs when one or more prerequisites are unaccounted for.

Example: Foundation result R follows from P1, P2, P3, P4, P5. ASN extends R to a new domain and argues P1, P2, and P3 transfer. P4 and P5 are unaccounted for — neither confirmed as domain-independent nor given analogs.

**Principled check**: Beyond the explicit Follows-from list, check for implicit assumptions the foundation result relies on by context — quantifier domains, subspace restrictions, type constraints, level restrictions. These may not appear in the Follows-from list but are assumed by the foundation's scope.

Example: Foundation result R is stated "for all x ∈ D₁" and proved using properties of D₁. ASN extends R to D₂ and addresses every Follows-from prerequisite, but R's proof also assumes all elements have a particular structural property that holds in D₁ by definition but must be separately established for D₂.

### 4a. Transfer by Assertion

The ASN claims a foundation argument transfers to a new context using phrases like "by similar reasoning," "the same argument applies," or "the same N cases." Flag any such claim where the ASN does not show that each step of the original argument holds in the new context. The claim may be correct, but it must be verified, not asserted.

Example: ASN states "by the same three cases as R" but does not show that each case's preconditions hold in the new domain — case 2 may rely on an assumption specific to the original domain.

### 4b. Quantifier Domain Mismatch

A foundation property is quantified over a specific domain (e.g., "for all x ∈ D₁") and the ASN applies it to an element from a different domain D₂ without verifying membership in D₁ or establishing that the property holds on D₂.

Example: Foundation property P states "for all x ∈ D₁, Q(x)." ASN invokes P on element y, but y ∈ D₂ and D₂ ⊄ D₁. The ASN does not verify y ∈ D₁ or prove Q(y) independently.

### 4c. Scope Narrowing in Citations

The ASN cites a foundation property but silently drops conditions, cases, or prerequisites from the original. The citation looks correct but the ASN's usage does not account for the full scope of the foundation result.

Example: Foundation property P has three conditions: C1, C2, C3. ASN cites P but only uses the consequence of C1 and C2, never checking C3. Or: foundation result R covers four cases; ASN cites R but only addresses two of the four cases in its argument.

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
