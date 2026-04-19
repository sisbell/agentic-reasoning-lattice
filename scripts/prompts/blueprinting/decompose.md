You are analyzing a section from a mathematical specification document. Your job: identify the claims in this section and produce a YAML file describing its structure.

Output ONLY valid YAML. No commentary, no code fences, no explanation.

## YAML structure

```yaml
title: <section header text, without ## prefix>
narrative: |
  <introductory text before the first claim — context, motivation, quotes>
claims:
  - label: <short identifier, e.g. S0, Σ.C, vpos(S, o)>
    name: <PascalCase name, e.g. ContentImmutability>
    body: |
      <full claim text: bold header + statement + justification + proof + formal contract>
```

## Rules

1. Use the label exactly as it appears in the bold header: `**S0 (Content immutability).**` → label is `S0`.
2. For `**Definition (Name).**` headers, the label is the Name, not "Definition": `**Definition (SomeConceptName).**` → label is `SomeConceptName`.
3. The name should be PascalCase. If the header has spaces like "Content immutability", produce `ContentImmutability`.
4. The narrative field captures text that introduces the section before any claim appears. If there is no introductory text, set narrative to empty string.
5. Each claim's body starts at its bold `**Label (Name).**` header and includes everything up to the next claim's bold header (or end of section). Include the formal contract if present — it stays in the body.
6. **Bold sub-headers within a claim are NOT separate claims.** Case splits, consequences, verification steps, and other internal structure (e.g., `**Case A:**`, `**Consequence 1:**`, `**Necessity.**`) stay in the parent claim's body. Only `**Label (Name).**` or `**Definition (Name).**` headers start new claims.
8. If the section has NO claims (e.g., a worked example, open questions, or pure discussion), output:

```yaml
title: <section header>
narrative: |
  <entire section content>
claims: []
```

8. Preserve the original text exactly in narrative and body fields. Do not rewrite, summarize, or reformat.
9. Some sections contain multiple claims. List each one separately.

## Section to analyze

{{section_content}}
