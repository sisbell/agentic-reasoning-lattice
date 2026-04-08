# Blueprinting

Blueprinting takes a converged reasoning document and prepares it for formalization. The ASN enters as a monolithic prose document with embedded properties; it leaves as a directory of individual property files, each classified, contracted, and with dependencies mapped.

```
ASN (monolithic)
     |
  format + disassemble ──→ per-property files + table + vocabulary
     |
  lint (inline, missing, status)
     |
  triage ──→ promotion plan (human-reviewed)
     |
  promote / extract ──→ new property files, reclassifications
     |
  promote to formalization
```

## Formatting and disassembly

The first steps are mechanical. Format the ASN to normalize the property table — consistent PascalCase names, clean markers, uniform structure. Then disassemble: split the monolithic document into one file per property, preserving each property's derivation prose. The table and preamble become structural files (`_table.md`, `_preamble.md`).

After disassembly, build the vocabulary — scan all property files and extract every notation definition into a shared `_vocabulary.md`. This becomes the reference for all downstream tools and reviewers.

At this point you have a directory of property files that together contain exactly the same content as the original ASN, just addressable individually.

## Linting

Three independent lint passes examine the decomposed properties:

**Inline lint** scans each property file for embedded results that should be their own properties. A long derivation may prove an intermediate result that other properties could reference — but because it's buried in prose, no one can depend on it. Inline lint finds these. Each run catches roughly 75% of findings due to non-determinism, so multiple cycles accumulate and deduplicate.

**Missing lint** looks for references to labels that don't exist in the property table — properties that the derivation assumes but no one declared. These are gaps: the reasoning uses something that was never formally stated.

**Status lint** classifies each property — is this really an axiom, or is it derived? Is this labeled as a lemma but actually a definition? The status determines how downstream tools handle the property.

## Triage

Lint produces findings. Triage turns findings into a plan. An LLM examines all inline and missing findings together and produces a promotion plan:

- **Promote** — an embedded result should become its own property (e.g., T0b contains both T0(a) and T0(b), split them)
- **Extract** — an embedded definition should become a standalone definition file (e.g., T12's derivation contains the definition of Span)
- **Leave** — the finding is not actionable (commentary, already covered, too minor)

The promotion plan is a human-editable file. Review it before proceeding — the triage LLM can miss things (it missed T0a and Span in ASN-0034, both had to be manually added). This is the key judgment point in blueprinting.

## Promotion and extraction

Execute the plan. For each promote action, the source property's narrative is rewritten to reference the new property, and the new property gets its own file with derivation and formal contract. For each extract action, the definition is pulled out into a standalone definition file.

After promotion, run status lint again — newly created properties need classification. Apply any reclassifications to the table.

## Entering formalization

The final step copies the property files, table, and vocabulary to the formalization directory. At this point every property has:

- Its own file with derivation prose
- A label and PascalCase name in the table
- A classification (axiom, definition, lemma, corollary, design requirement)
- Dependencies mapped in the table's status column

The property files don't yet have formal contracts — that's what formalization produces. But they have enough structure that formalization can operate on each one independently.
