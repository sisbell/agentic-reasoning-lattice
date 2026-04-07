# Format Normalization Revise

You are fixing format issues in an ASN reasoning document. The format
reviewer found the issues listed below. Fix each one in the ASN file.

## Rules

1. **Only fix format issues.** Do not change content, proofs, or derivations.
2. **Property table** must have at least 3 columns: `| Label | Statement | Status |`
3. **Property headers** use: `**LABEL (PascalCaseName).**`
   - The name must be PascalCase with no spaces: `**T1 (LexicographicOrder).**` not `**T1 (Lexicographic order).**`
   - Convert existing names to PascalCase: "Carrier-set definition" → `CarrierSetDefinition`
4. **Definition headers** use: `**Definition (PascalCaseName).**`
   - The name must be PascalCase: `**Definition (TumblerAddition).**` not `**Definition (Tumbler addition).**`
5. **Status vocabulary** must use standard terms:
   - introduced, corollary of, from, theorem from, extends, design requirement, cited, lemma
6. **Missing table entries**: if a definition or property exists in prose but not
   in the table, add a row. Use the PascalCase name as the label for definitions.
7. **Property boundary markers**: insert a horizontal rule (`---`) on its
   own line immediately before each property or definition bold header.
   This marks the boundary between properties for downstream disassembly.
   Do not place `---` before the very first property in the ASN, before
   `##` section headers, or inside worked examples.
8. Do not add, remove, or reorder properties. Only fix formatting, add
   missing table entries, and insert boundary markers.

## ASN File

The ASN is at `{{asn_path}}`. Read it, fix the format issues, write it back.

## Format Findings

{{findings}}

## Task

Read the ASN file, fix every finding listed above, and write the corrected
file back to the same path. Do not modify any content beyond what the
findings require.
