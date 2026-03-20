# Rebase ASN Against Updated Foundation

You are updating an ASN after its foundation has changed. Properties that this ASN
previously derived locally are now available in the foundation. Replace local
derivations with citations.

## Foundation Statements (current)

{{foundation_statements}}

## Task

Read the ASN at `{{asn_path}}`.

Scan the ASN's statement registry for properties with status `introduced`. For each
one, check if the same property (or an equivalent) now exists in the foundation
statements above.

For each match:

1. **Replace the local derivation.** Remove the proof and worked examples for that
   property. Replace with a brief citation that preserves the formal statement inline.
   Keep surrounding context that motivates or introduces the property.

   Example — before:
   ```
   **D1** (*DisplacementRoundTrip*). For tumblers a, b with a < b and #a = #b:
     a ⊕ (b ⊖ a) = b

   *Proof.* [multi-paragraph proof]  ∎
   ```

   After:
   ```
   The displacement round-trip is guaranteed by the foundation: for tumblers
   a, b with a < b and #a = #b, a ⊕ (b ⊖ a) = b (D1, ASN-0034).
   ```

2. **Update the registry.** Change status from `introduced` to `cited`. Update
   the label if the foundation uses a different one. Add the foundation ASN
   reference.

3. **Update proofs that reference the rebased property.** If other properties
   in this ASN cite the rebased property by its old label, update the reference
   to use the foundation label.

For properties that do NOT match anything in the foundation, leave them unchanged.

**Targeted edits only.** Do not rewrite the ASN. Do not modify properties that
are not being rebased. Do not add or remove sections.

Write the updated ASN back to `{{asn_path}}` using the Edit tool.
