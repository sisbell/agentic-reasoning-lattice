# Format Normalization Revise

You are fixing format issues in an ASN reasoning document. The format
reviewer found the issues listed below. Fix each one in the ASN file.

## Rules

1. **Only fix format issues.** Do not change content, proofs, or derivations.
2. **Property table** must have 4 columns: `| Label | Type | Statement | Status |`
   - If Type column is missing, add it with appropriate types (INV, LEMMA, DEF, etc.)
3. **Prose headers** must use: `**LABEL — Name.**`
   - Replace `**LABEL (Name).**` with `**LABEL — Name.**`
   - Add missing names from the Statement column of the property table
4. **Status vocabulary** must use standard terms:
   - introduced, corollary of, from, theorem from, extends, design requirement, cited
5. Do not add, remove, or reorder properties. Only fix formatting.

## ASN File

The ASN is at `{{asn_path}}`. Read it, fix the format issues, write it back.

## Format Findings

{{findings}}

## Task

Read the ASN file, fix every finding listed above, and write the corrected
file back to the same path. Do not modify any content beyond what the
findings require.
