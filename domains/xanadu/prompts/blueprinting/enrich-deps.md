You are extracting dependencies and literature citations from a single claim in a mathematical specification document.

Output ONLY valid YAML. No commentary, no code fences, no explanation.

## YAML structure

```yaml
depends:
  - <claim label>
literature_citations:
  - <reference string, e.g. "LM 2/14", "LM 4/30">
```

## Rules

1. **depends** — list the claim labels that this claim DIRECTLY depends on. A direct dependency means this claim's proof, formal contract, or design justification invokes that label as a premise, precondition, or motivating gap.
   - Do NOT include transitive dependencies. If this claim uses X, and X was built from Y and Z, do NOT list Y and Z — only list X.
   - Do NOT include claims that are merely mentioned for context or comparison.
   - Do NOT include function names (e.g., subspace, actionPoint, shift) — only claim labels.
   - Just list the label. Do not include the source ASN number.
   - If none, use empty list `[]`.

2. **literature_citations** — list references to external literature. These typically start with `LM` (Literary Machines) followed by a page reference (e.g., `LM 2/14`, `LM 4/30`). If none, use empty list `[]`.

## Claim

Label: {{label}}
Name: {{name}}

### Body

{{body}}
