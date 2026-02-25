# Extract Vocabulary from ASN(s)

You are updating a shared vocabulary file for a specification project.

## Current Vocabulary

{{vocabulary}}

## Finalized ASN(s)

{{asn_content}}

## Task

Compare the ASN(s) against the current vocabulary. Produce TWO sections separated by a line containing only `---`:

1. **Conflicts** — where the ASN's notation differs from the current vocabulary
2. **Updated vocabulary** — the complete replacement content for vocabulary.md

### Section 1: Conflicts

For each conflict, give a table row:

| Term | Vocabulary says | ASN says | Recommendation |
|------|----------------|----------|----------------|
| ... | ... | ... | ... |

If no conflicts, write "No conflicts found."

### Section 2: Updated vocabulary

Output the complete updated vocabulary.md content. This replaces the file entirely. The vocabulary must contain:

1. **Core Types** — what things ARE (not what they guarantee). Keep existing type definitions. Add any new types the ASN introduces.

2. **Canonical State Components** — state component names and type signatures that become the standard for all ASNs. Example:
   - `Σ.content : IAddr ⇀ Byte` — the content store
   - `d.map : VAddr ⇀ IAddr` — document arrangement (text subspace)

3. **Naming Conventions** — property labeling patterns. What prefix scheme, what pattern for preconditions, postconditions, frame conditions, derived properties, invariants? Describe the PATTERN, not the specific properties.

4. **Organizational Pattern** — what sections an ASN uses and in what order.

5. **Key Distinctions** — keep existing, add any new ones from the ASN.

## Rules

- State components: NAME and TYPE SIGNATURE only. Do NOT include guarantees (e.g., "append-only" or "immutable"). Guarantees are properties to be derived, not vocabulary entries.
- Naming conventions: describe the PATTERN, not specific properties. "R0-R7 for postconditions" is a pattern. "R5 means I-space frame" is a specific property — don't include it.
- If multiple ASNs use different conventions, the MAJORITY convention wins. Note the conflict in Section 1 and use the majority choice in Section 2.
- Keep the vocabulary CONCISE. This is a reference card, not a textbook.

## Output Format

```
[Conflicts table or "No conflicts found."]
---
[Complete vocabulary.md content]
```

Output ONLY the two sections separated by `---`. No commentary, no explanation outside the sections.
