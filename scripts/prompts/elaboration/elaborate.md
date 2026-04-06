# Elaborate

You are writing a rigorous proof for a property. The property may have
no proof, or its proof may be embedded in another property's section
as a sub-claim or corollary.

## Property

**Label**: {{label}}

### Current Section

{{thin_section}}

### Related Section (reference only)

{{host_section}}

### Dependencies

{{dependency_sections}}

## Style

Write in Dijkstra's style: prose with embedded formalism. The reasoning
IS the specification. Each formal statement must be justified in the
sentence that introduces it.

- State what you are proving
- Develop the argument step by step
- Each case must be explicit — no "by similar reasoning"
- Reference dependencies by label citation, not by proximity
- End with ∎

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
