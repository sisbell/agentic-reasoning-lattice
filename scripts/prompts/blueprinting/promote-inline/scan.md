# Scan for Inline Results

You are scanning a property section for embedded results — derived
lemmas, consequences, corollaries, or case analyses that establish
standalone results within a larger property's section. These should
be promoted to their own property sections.

## Property

**Label**: {{label}}

## Property File Content

{{content}}

## Task

Identify any embedded results that should be promoted to standalone
properties. Look for:

- Bold sub-headers like **Consequence N:**, **Lemma:**, **Claim:**
- Case analyses that establish a named result with ∎
- Derived results that other properties or ASNs might cite

Classify each distinct block as one of:

- **derived**: A result with a proof that establishes something
  independently citable. Should be promoted to its own property.
- **commentary**: Design rationale, implementation notes, worked
  examples, or explanatory text. Should stay in place.

Do NOT classify the main property statement, its proof, or its
formal contract as derived — those belong to the property.

For each derived result, suggest a label and PascalCase name based on
what it establishes.

## Output Format

For each block, write one line:

```
derived | SUGGESTED-LABEL | PascalCaseName | one-line description
commentary | — | — | one-line description
```

If there are no embedded results worth promoting, write:

```
(none)
```

Output ONLY the classification lines. No preamble, no explanation.
