# Proof Structure

You are restructuring a property's proof into explicit numbered stages.
The goal is to make the proof's logical structure clear and mechanical
for downstream Dafny translation.

## Vocabulary

{{vocabulary}}

## Property

{{content}}

## Task

Decompose the proof into explicit numbered stages. Each stage should:

1. State what it establishes
2. Derive it step by step — no "by similar reasoning"
3. Reference dependencies by label citation

Keep the Dijkstra style: prose with embedded formalism. The reasoning
IS the specification.

## Rules

1. **Do not change the formal contract.** Copy it exactly as-is.
2. **Do not change what is proven.** The property statement, preconditions,
   and postconditions must remain identical.
3. **Do not add or remove content.** Only restructure the proof argument
   into explicit stages.
4. **Preserve all commentary** after the formal contract unchanged.
5. **If the proof is already staged**, return it unchanged.
6. **Definitions have no proofs** — return unchanged.

## Output

Return the complete rewritten property file. Nothing else — no preamble,
no explanation, no markdown fences. Just the file content.
