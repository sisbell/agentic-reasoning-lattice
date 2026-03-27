# Quality Pass

You are rewriting a property's proof to Dijkstra standard and ensuring
it has a complete formal contract.

## Property

**Label**: {{label}}

### Current Section

{{section}}

## Style

Write in Dijkstra's style: prose with embedded formalism. The reasoning
IS the specification. Each formal statement must be justified in the
sentence that introduces it.

- State what you are proving clearly at the start
- A plain English summary alongside the formal statement
- Develop the argument step by step
- Each case must be explicit — no "by similar reasoning"
- Reference dependencies by label citation
- End proofs with ∎

## Formal Contract

Ensure a `*Formal Contract:*` section at the end with applicable fields:

- *Preconditions:* — what must hold before
- *Postconditions:* — what is guaranteed after
- *Invariant:* — what holds across all state transitions (for every s → s')
- *Frame:* — what is preserved / not changed
- *Axiom:* — fundamental assertion by definition or design, not derived
- *Definition:* — the construction or computation rule

Preserve exact conditions from the narrative. Do not add implicit
type constraints. Only include fields that apply.

## ASN File

The ASN is at `{{asn_path}}`.

## Rules

1. Rewrite the proof in the ASN. Keep the property's bold header and
   formal statement unchanged.
2. The proof must be self-contained — a reader should understand it
   without reading any other section.
3. For axioms: state why the property holds by definition or design.
   Use `*Axiom:*` in the formal contract.
4. For definitions: ensure the construction rule is clear. Use
   `*Definition:*` in the formal contract.
5. If the formal contract already exists and is correct, leave it.
   If it's missing or incomplete, add or update it.
6. Do not modify other properties' sections.
