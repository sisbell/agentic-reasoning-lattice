# Section Repair

You are writing a standalone proof for a property that currently lacks one.
The property's statement exists but its proof is embedded in another
property's section. Write a self-contained Dijkstra-style proof.

## Property

**Label**: {{label}}

### Current Section (incomplete)

{{thin_section}}

### Embedded Proof (reference only)

The following section from another property contains a proof that covers
this property. Use it to understand what needs to be proved, but write
your own standalone argument.

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

## ASN File

The ASN is at `{{asn_path}}`.

## Rules

1. Write the proof directly after the property's bold header in the ASN.
   Insert it after the existing statement text and before the next property's
   bold header.
2. The proof must be self-contained — a reader should understand it
   without reading any other section.
3. Reference dependencies by label (e.g., "By TA1, ...") not by
   section proximity (e.g., "as shown above").
4. If `*Formal Contract:*` is not already present, add one after the proof
   with the applicable fields (Preconditions, Postconditions, Invariant,
   Frame, Axiom, Definition). Preserve exact conditions from the narrative.
5. Do not modify the original combined verification section or any
   other property's section.
6. For axioms or definitional properties (no derivation possible), write
   a brief justification stating why the property holds by definition or
   design, and use `*Axiom:*` in the formal contract.
7. Update the property's Status column in the property table to reflect
   the actual dependencies used in the proof (e.g., change `introduced`
   to `from TA1, TumblerAdd` if those are cited in the proof).
