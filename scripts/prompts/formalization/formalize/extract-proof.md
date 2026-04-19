# Section Repair

You are writing a standalone proof for a claim that currently lacks one.
The claim's statement exists but its proof is embedded in another
claim's section. Write a self-contained Dijkstra-style proof.

## Claim

**Label**: {{label}}

### Current Section (incomplete)

{{thin_section}}

### Embedded Proof (reference only)

The following section from another claim contains a proof that covers
this claim. Use it to understand what needs to be proved, but write
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

1. Write the proof directly after the claim's bold header in the ASN.
   Insert it after the existing statement text and before the next claim's
   bold header.
2. The proof must be self-contained — a reader should understand it
   without reading any other section.
3. Reference dependencies by label (e.g., "By TA1, ...") not by
   section proximity (e.g., "as shown above").
4. If `*Formal Contract:*` is not already present, add one after the proof
   with the applicable fields (Preconditions, Postconditions, Invariant,
   Frame, Axiom, Definition). Preserve exact conditions from the narrative.
5. Do not modify the original combined verification section or any
   other claim's section.
6. For axioms or definitional claims (no derivation possible), write
   a brief justification stating why the claim holds by definition or
   design, and use `*Axiom:*` in the formal contract.
7. If the proof cites dependencies not already in the claim's `.yaml`
   file, add them to the `depends` list. Do not remove existing dependencies.
