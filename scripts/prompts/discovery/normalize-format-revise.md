# Format Normalization Revise

You are fixing format issues in an ASN reasoning document. The format
reviewer found the issues listed below. Fix each one in the ASN file.

## Rules

1. **Only fix format issues.** Do not change content, proofs, or derivations.
2. **Property table** must have 4 columns: `| Label | Type | Statement | Status |`
   - If Type column is missing, add it with appropriate types (INV, LEMMA, DEFINITION, etc.)
3. **Property headers** use: `**LABEL (Name).**`
4. **Definition headers** use: `**Definition (PascalCaseName).**`
   - The name must be PascalCase: `**Definition (TumblerAddition).**` not `**Definition (Tumbler addition).**`
   - Convert multi-word names to PascalCase in both the header and the table label
5. **Status vocabulary** must use standard terms:
   - introduced, corollary of, from, theorem from, extends, design requirement, cited, lemma
6. **Missing table entries**: if a definition or property exists in prose but not
   in the table, add a row. Definitions get type `DEFINITION` and a PascalCase label
   matching the header name.
7. Do not add, remove, or reorder properties. Only fix formatting and add
   missing table entries.

## ASN File

The ASN is at `{{asn_path}}`. Read it, fix the format issues, write it back.

## Format Findings

{{findings}}

## Task

Read the ASN file, fix every finding listed above, and write the corrected
file back to the same path. Do not modify any content beyond what the
findings require.
