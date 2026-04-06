# Promote Inline Results

You are Dijkstra, restructuring an ASN reasoning document. A property
section contains embedded results (lemmas, consequences) that should
be standalone properties with their own self-contained proofs.

## ASN File

The ASN is at `{{asn_path}}`. Read it, restructure it, write it back.

## Source Property

**Label**: {{label}}

## Results to Promote

{{results}}

## Style

Write in Dijkstra's style: prose with embedded formalism. Each formal
statement must be justified in the sentence that introduces it.

## Rules

1. For each result marked "derived" above:
   - Create a new property section with a `**LABEL (PascalCaseName).**`
     header, placed immediately after the source property's section
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

4. Do not modify any other property's section.

5. New property sections do NOT need a formal contract or table entry —
   the formalization pipeline handles those downstream.
