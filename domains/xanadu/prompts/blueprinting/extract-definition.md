# Extract Definition

You are extracting a narrative definition from a claim file into a
standalone definition file.

## Vocabulary

{{vocabulary}}

## Current Claim Table

{{table}}

## Source Claim File

{{content}}

## Definitions to Extract

{{findings}}

## Rules

1. For each definition listed above:
   - Create a new definition section with a `**Definition (PascalCaseName).**`
     header, placed after the source claim's section in this file
   - Write the definition as a self-contained statement: state what is
     being defined, give the formal definition, note any conditions or
     constraints
   - Add a formal contract with a `*Definition:*` field stating the
     definition precisely
   - In the source claim's narrative, replace the inline definition
     with a citation: "By **Definition (Name)**, ..." or
     "(see **Definition (Name)**)"

2. Do not alter the source claim's formal contract.

3. Do not move or delete commentary or proof content — only extract
   the definition itself.

4. Choose a label that fits the naming conventions in the table above.
   For a definition extracted from claim LABEL, use a descriptive
   name like `Def-Span` or just the PascalCase name. Check the
   claim table to avoid collisions.

## Output

Return the complete rewritten file. The file will contain the source
claim (with citations replacing inline definitions) followed by the
new definition sections. Place a `---` boundary marker on its own line
between each section.

After the file content, write a `=== TABLE ===` marker on its own line,
then one table row per new definition:

| Label | Name | Statement | Status |

Where:
- **Label**: the new definition's label (e.g., Def-Span)
- **Name**: PascalCase identifier (e.g., Span)
- **Statement**: one-line summary of what the definition introduces
- **Status**: one of the standard vocabulary terms:
  - `introduced` — new definition in this ASN
  - `definition` — a named concept or construction
  - `axiom` — fundamental assertion, not derived
  - `design requirement` — imposed by design, not derived

Nothing else — no preamble, no explanation, no markdown fences.
