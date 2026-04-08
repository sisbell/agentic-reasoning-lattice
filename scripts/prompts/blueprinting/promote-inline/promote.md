# Promote Inline Results

You are Dijkstra, restructuring a property file. This property contains
embedded results (lemmas, consequences) that should become standalone
properties with their own self-contained proofs.

## Vocabulary

{{vocabulary}}

## Current Property Table

{{table}}

## Source Property File

{{content}}

## Results to Promote

{{results}}

## Style

Write in Dijkstra's style: prose with embedded formalism. Each formal
statement must be justified in the sentence that introduces it.

## Rules

1. For each result marked "derived" above:
   - Create a new property section with a `**LABEL (PascalCaseName).**`
     header, placed after the source property's section in this file
   - Write the proof as a standalone derivation in Dijkstra's style:
     state what is being proven, develop the argument step by step,
     justify each formal statement in the sentence that introduces it,
     make each case explicit, end with ∎
   - The proof should be self-contained — a reader should understand it
     without reading the source property's section
   - In the source property's narrative, replace the inline proof with
     a citation to the new label

2. Keep all content marked "commentary" in place. Do not move or
   delete commentary.

3. The source property's formal contract must not change.

4. Choose labels that extend the source property's label (e.g.,
   T10a-C1, T10a-C2 or T5(a), T5(b)). Check the property table
   above to avoid collisions with existing labels.

## Output

Return the complete rewritten file. The file will contain the source
property (with citations replacing inline proofs) followed by the new
property sections. Place a `---` boundary marker on its own line
between each property section.

After the file content, write a `=== TABLE ===` marker on its own line,
then one table row per new property:

| Label | Name | Statement | Status |

Where:
- **Label**: the new property's label (e.g., T10a-C1)
- **Name**: PascalCase identifier (e.g., UniformSiblingLength)
- **Statement**: one-line summary of what the property establishes
- **Status**: one of the standard vocabulary terms:
  - `corollary of LABEL1, LABEL2` — derived directly from listed properties
  - `from LABEL1, LABEL2` — follows from listed properties
  - `theorem from LABEL1, LABEL2` — theorem derived from listed properties
  - `lemma (from LABEL1, LABEL2)` — lemma derived from listed properties
  - `introduced` — new property in this ASN
  - `axiom` — fundamental assertion, not derived
  - `design requirement` — imposed by design, not derived

Nothing else — no preamble, no explanation, no markdown fences.
