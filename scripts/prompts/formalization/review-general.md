# General Review — Cross-Cutting Analysis

You review ASNs for cross-cutting consistency issues. Individual proofs have
been verified separately — do not re-verify each proof. Focus on interactions
between properties and structural coherence of the ASN as a whole.

If you notice a proof issue while examining cross-cutting concerns, you may
still flag it.

## Vocabulary

Use this shared vocabulary when interpreting the ASN:

{{vocabulary}}

## Foundation

These ASNs are verified foundations. Check that the ASN under review uses
their definitions consistently.

{{foundation_statements}}

## ASN to Review

{{asn_content}}

## ASN Metadata

- **ASN**: {{asn_label}}
- **Declared depends**: {{depends}}

## What to Check

### 1. Dependency Graph Consistency

The dependency YAML below is mechanically extracted. Compare it against the
actual derivations:

- If a derivation depends on a label NOT listed in its `follows_from`, flag it
- If a `follows_from` entry is NOT actually used in the derivation, flag it
- If the `name` field doesn't match the property's actual name, flag it

```yaml
{{deps_yaml}}
```

### 2. Structural Coherence

- Properties that redefine or contradict each other
- Definitions used inconsistently across properties
- Notation that shifts meaning between sections
- Missing definitions — concepts used but never defined

### 3. Foundation Consistency

- Stale references to foundation properties (wrong label, wrong statement)
- Local redefinitions of foundation concepts
- Missing dependencies on foundation ASNs

### 4. Registry Completeness

- Properties in prose without table entries
- Definitions in prose without table entries
- Table entries without corresponding prose

### 5. Scope Boundaries

- Topics that belong in a future ASN, not this one (OUT_OF_SCOPE)

## Open Issues

The following open issues were identified by prior reviews or mechanical checks.
Each is a **mandatory REVISE finding** — the ASN cannot converge while open
issues remain.

When an open issue reports a circular dependency (e.g., `[cycle] A → B → A`),
determine which direction is correct by reading the actual derivations. One
edge is wrong — flag the incorrect Status entry for removal.

{{open_issues}}

## Output Format

```markdown
# Review of ASN-NNNN

## REVISE

### Issue 1: [specific claim]
**ASN-NNNN, [section]**: "[quoted claim]"
**Problem**: [what's wrong or missing]
**Required**: [what would fix it]

## OUT_OF_SCOPE

### Topic 1: [what's missing but belongs in a future ASN]
**Why out of scope**: [this is new territory, not an error in this ASN]

VERDICT: CONVERGED | REVISE
```

**VERDICT** is mandatory. Use CONVERGED only when there are zero REVISE items.
