# Scan for Inline Results

You are scanning a property file for embedded content that should be
extracted — derived results, definitions, or commentary.

## Property

**Label**: {{label}}

## Property File Content

{{content}}

## Task

Identify any embedded content beyond the main property's own statement,
proof, and formal contract. Classify each distinct block as one of:

- **derived**: A result with a proof that establishes something
  independently citable (consequence, lemma, claim). Should be promoted
  to its own property.
- **definition**: A named concept, construction, or notation introduced
  in narrative (e.g., "A span is a pair (s, ℓ)...", "Define the action
  point as..."). Should be extracted to its own definition file.
- **commentary**: Design rationale, implementation notes, worked
  examples, or explanatory text. Should stay in place.

Do NOT classify the main property statement, its proof, or its
formal contract — those belong to the property.

For derived and definition results, suggest a label and PascalCase name.

## Output Format

For each block, write one line:

```
derived | SUGGESTED-LABEL | PascalCaseName | one-line description
definition | SUGGESTED-LABEL | PascalCaseName | one-line description
commentary | — | — | one-line description
```

If there are no embedded results worth extracting, write:

```
(none)
```

Output ONLY the classification lines. No preamble, no explanation.
