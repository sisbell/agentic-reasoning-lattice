# Elaborate Proof

You are writing a rigorous proof for a property. Develop the argument
step by step with full justification.

## Vocabulary

{{vocabulary}}

## Property

{{content}}

## Dependencies

{{dependencies}}

## Style

Write in Dijkstra's style: prose with embedded formalism. The reasoning
IS the specification. Each formal statement must be justified in the
sentence that introduces it.

- State what you are proving
- Develop the argument step by step
- Each case must be explicit — no "by similar reasoning"
- Reference dependencies by label citation, not by proximity
- End with ∎

## Rules

1. **Do not change the formal contract.** If one exists, copy it
   exactly as-is. If none exists, add one with applicable fields:
   - *Preconditions:* — what must hold before
   - *Postconditions:* — what is guaranteed after
   - *Invariant:* — what holds across all state transitions
   - *Frame:* — what is preserved / not changed
   - *Axiom:* — fundamental assertion by definition or design
   - *Definition:* — the construction or computation rule
   Preserve exact conditions from the narrative. Only include
   fields that apply.

2. **Do not change what is proven.** The property statement,
   preconditions, and postconditions must remain identical.

3. **Do not add or remove content.** Only restructure the proof
   argument. Preserve all commentary after the formal contract.

4. **If the proof is already well-structured**, return it unchanged.

5. **Definitions have no proofs** — return unchanged.

## Output

Return the complete rewritten property file. Nothing else — no
preamble, no explanation, no markdown fences. Just the file content.
