You are extracting dependencies and literature citations from a single property in a mathematical specification document.

Output ONLY valid YAML. No commentary, no code fences, no explanation.

## YAML structure

```yaml
depends:
  - <label or label (ASN-NNNN) for cross-ASN references>
literature_citations:
  - <reference string, e.g. "LM 2/14", "LM 4/30">
```

## Rules

1. **depends** — list the property labels that this property DIRECTLY depends on. A direct dependency means this property's proof, formal contract, or design justification invokes that label as a premise, precondition, or motivating gap.
   - Do NOT include transitive dependencies. If this property uses X, and X was built from Y and Z, do NOT list Y and Z — only list X.
   - Do NOT include properties that are merely mentioned for context or comparison.
   - Include the ASN number for cross-ASN references: `T1 (ASN-0034)`.
   - If none, use empty list `[]`.

2. **literature_citations** — list references to external literature. These typically start with `LM` (Literary Machines) followed by a page reference (e.g., `LM 2/14`, `LM 4/30`). If none, use empty list `[]`.

## Property

Label: {{label}}
Name: {{name}}

### Body

{{body}}

### Formal Contract

{{formal_contract}}
