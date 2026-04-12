You are analyzing a section from a mathematical specification document. Your job: identify the properties in this section and produce a YAML file describing its structure.

Output ONLY valid YAML. No commentary, no code fences, no explanation.

## YAML structure

```yaml
title: <section header text, without ## prefix>
narrative: |
  <introductory text before the first property — context, motivation, quotes>
properties:
  - label: <short identifier, e.g. S0, Σ.C, vpos(S, o)>
    name: <PascalCase name, e.g. ContentImmutability>
    body: |
      <property text: bold header + statement + justification + proof>
    formal_contract: |
      <formal contract block if present, omit field if not>
```

## Rules

1. Use the label exactly as it appears in the bold header: `**S0 (Content immutability).**` → label is `S0`.
2. For `**Definition (Name).**` headers, the label is the Name, not "Definition": `**Definition (SomeConceptName).**` → label is `SomeConceptName`.
3. The name should be PascalCase. If the header has spaces like "Content immutability", produce `ContentImmutability`.
4. The narrative field captures text that introduces the section before any property appears. If there is no introductory text, set narrative to empty string.
5. Each property's body starts at its bold `**Label (Name).**` header and includes everything up to the formal contract or the next property's bold header (or end of section).
6. If a property has a `*Formal Contract:*` block, extract it into the `formal_contract` field. If there is no formal contract, omit the field entirely.
7. **Bold sub-headers within a property are NOT separate properties.** Case splits, consequences, verification steps, and other internal structure (e.g., `**Case A:**`, `**Consequence 1:**`, `**Necessity.**`) stay in the parent property's body. Only `**Label (Name).**` or `**Definition (Name).**` headers start new properties.
8. If the section has NO properties (e.g., a worked example, open questions, or pure discussion), output:

```yaml
title: <section header>
narrative: |
  <entire section content>
properties: []
```

9. Preserve the original text exactly in narrative, body, and formal_contract fields. Do not rewrite, summarize, or reformat.
10. Some sections contain multiple properties. List each one separately.

## Section to analyze

{{section_content}}
