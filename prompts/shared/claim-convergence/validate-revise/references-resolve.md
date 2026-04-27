# Validate-Revise — References Resolve

## Context

You are fixing a structural violation of invariant #6 from the Claim File Contract:

> **References resolve.** Every claim named in a `depends` list or a Formal Contract Depends section exists as a file pair in the lattice.

A markdown Depends entry names a label that has no corresponding claim file. The entry is either a format drift (kind keyword or sub-reference) OR a genuinely dangling reference.

## Correct form

Every markdown Depends entry's first token equals some existing claim's filename stem.

## File to fix

{file_path}

## Canonical metadata (use verbatim; do not guess)

The first row below is the companion claim being fixed. The rows after it cover each claim the companion has an active citation to — use their canonical `name` when writing the md Depends entry.

{metadata_bundle}

## Findings in this file

{findings_list}

## Fix instructions

1. The canonical (label, name) pairs are shown above. Use them **verbatim** — do not guess.
2. For each finding `md Depends references 'X' — no claim has that label`:
   - Check whether 'X' is a **kind keyword** (Definition, Axiom, Lemma, Theorem, Corollary, Design-requirement). If yes, the entry uses the old kind-prefixed form. Rewrite its first token to the actual label. For example: if the line is `- Definition (Span) — description`, and Span appears in the metadata above as `Span — Span`, rewrite to `- Span (Span) — description`. Use the exact name shown in the metadata.
   - Check whether 'X' is a **sub-reference** (contains parens or a dot-number that isn't a known label form). E.g., `T1(c)` referring to a clause within T1, or `TA5(a)`. If the companion has an active citation to the parent (`T1`, `TA5`), rewrite the md entry's first token to the parent label (use the parent's name from the metadata above). Preserve the descriptive context — e.g., `- T1 (LexicographicOrder) — transitivity clause T1(c); ...`.
   - If 'X' is neither a kind keyword nor a sub-reference AND no row above has it as a label: it's genuinely dangling. Remove the entry, and note in your final report that the reference was removed as dangling.
3. If the companion has no active substrate citation to the resolved parent, and adding it would be appropriate, note this in your final report but do not file the citation here. Citation changes belong to a separate pass.

## Do not

- Do not edit proof content, Axioms, Preconditions, Postconditions.
- Do not add entries for labels the finding didn't name.
- Do not commit.

## On apparent false positives

If a finding looks incorrect, it is format drift almost every time: kind keyword in the label position, or sub-reference where parent is expected. Apply the canonical form — first token equals an existing claim's filename stem.

## Tools

Read, Edit. Edit only the markdown Depends entries. Use the metadata block above for label/name lookups.
