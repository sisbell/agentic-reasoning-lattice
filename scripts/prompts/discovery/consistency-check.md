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

Read the foundation statements carefully, then read the ASN. Report any inconsistencies in the following categories. For each finding, cite the specific line or property.

### 1. Stale Labels
The ASN cites a foundation property by an old label that no longer exists in the foundation. Example: citing `TripleEndsetStructure` when the foundation now calls it `NEndsetStructure`.

### 2. Local Redefinitions
The ASN defines a property locally (status `introduced`) that already exists in the foundation statements. These should have been promoted to `cited` during a rebase.

### 2a. Unjustified Domain Extensions
The ASN introduces a function or property that reuses a foundation function's name or formula but applies it to a domain the foundation does not cover. This is a finding even if the registry correctly says `introduced`. Look for cases where the ASN applies a foundation function to addresses, stores, or subspaces outside the foundation function's stated domain.

### 2b. Incomplete Precondition Transfer
When the ASN extends a foundation result to a new domain, check whether all preconditions of the foundation result have been accounted for. Foundation statements include "Follows from" lists — each prerequisite must either (a) apply unchanged in the new domain, with explicit justification, or (b) have an explicit analog established by the ASN. A finding occurs when the ASN claims the extension holds but does not address one or more prerequisites from the Follows-from list.

### 3. Structural Drift
The ASN uses or restates a foundation definition but with outdated content. Example: defining Link as "a triple (F, G, Θ)" when the foundation defines it as "a sequence of N ≥ 2 endsets."

### 4. Missing Dependencies
The ASN references properties from a foundation ASN that is NOT in its declared depends list. Example: citing ASN-0058 properties but not listing 58 in depends.

### 5. Exhaustiveness Gaps
The ASN makes a claim about "all" of something (all transitions, all invariants, all endsets) but the foundation has items not covered. Example: listing "K.α, K.δ, K.ρ preserve M in frame" when K.λ and K.μ⁺_L also do.

### 6. Registry Mismatches
The properties table lists a property as `introduced` or `cited` but the body text contradicts this — e.g., a property listed as `cited (ASN-0034)` but the body contains a local proof, or vice versa.

## Output Format

For each category, list findings or write "(none)". Be specific — quote the text and cite the foundation property it conflicts with. At the end, write one of:

- `RESULT: CLEAN` — no findings in any category
- `RESULT: n FINDINGS` — where n is the total count
