# Review Quality Rewrite

You are reviewing a quality rewrite of a single property in an ASN.
The rewrite should improve proof quality and add/update the formal
contract. It should NOT delete content, modify other properties, or
change meaning.

## Property

**Label**: {{label}}

## Before

{{before}}

## After

{{after}}

## Task

Compare before and after. Check:

1. **No content deleted** — all text from before should be present
   in after (possibly reworded but not removed). Bold headers,
   commentary paragraphs, post-contract material, dependency
   sections must all be preserved.

2. **No meaning changed** — the proof should establish the same
   claims. Steps should not be silently dropped or simplified away.
   Updating the PascalCase name of a cited dependency is acceptable
   as long as the label itself is unchanged.

3. **Formal contract correct** — if added or updated, it should
   match what the proof establishes.

## Output

Write exactly one of:

- `RESULT: PASS` — the rewrite is safe
- `RESULT: FAIL` — followed by what was deleted or damaged

Output ONLY the result line. No preamble, no explanation unless FAIL.
