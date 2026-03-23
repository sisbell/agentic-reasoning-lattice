# Rebase ASN Against Updated Foundation

You are updating an ASN after its foundation has changed. Properties that this ASN
previously derived locally are now available in the foundation. Replace local
derivations with citations.

## Foundation Statements (current)

{{foundation_statements}}

## Task

Read the ASN at `{{asn_path}}`.

Perform **three passes** against the foundation statements above.

### Pass 1 — Promote local derivations

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

### Pass 2 — Fix stale citations

Scan the entire ASN for every reference to a foundation property — both in the
body text and in the statement registry. For each citation, verify it against the
current foundation statements above:

1. **Label renames.** If the ASN cites a property by an old label that has been
   renamed in the foundation (e.g., `TripleEndsetStructure` → `NEndsetStructure`),
   update the label everywhere it appears — in prose, formal statements, and the
   registry.

2. **Structural changes.** If the foundation has generalized or narrowed a
   definition (e.g., "exactly three endsets" → "N ≥ 2 endsets"), update the ASN's
   usage to match. This includes local definitions that restate the foundation
   property, formal statements that embed the old definition, and prose that
   describes the old structure.

3. **New foundation material.** If the foundation now defines transitions,
   invariants, or definitions that the ASN's analysis should cover but doesn't
   (e.g., new elementary transitions added to the state model), flag these as
   gaps. Update enumeration lists that claim to be exhaustive (e.g., "all other
   elementary transitions...") to include the new material.

### Pass 3 — Verify consistency

Read through the ASN one final time and check that:

- Every foundation label cited in the ASN matches a label in the foundation
  statements above.
- No property is listed as `introduced` when an equivalent exists in the
  foundation (pass 1 may have missed near-matches).
- The statement registry is consistent with the body text.

**Targeted edits only.** Do not rewrite the ASN. Do not modify properties that
are not affected by foundation changes. Do not add or remove sections beyond
what is needed for the three passes above.

Write the updated ASN back to `{{asn_path}}` using the Edit tool.
