# Validate-Revise — Body Uniqueness

## Context

You are fixing a structural violation of invariant #9 from the Claim File Contract:

> **Body uniqueness.** A given claim's body (bold declaration + proof + Formal Contract) appears in exactly one file — the file whose yaml `label` matches the claim. No claim's body is inlined into another claim's file.

This file contains the body of one or more OTHER claims, inlined as if they were part of this file. Those other claims have their own canonical files. Your job is to remove the inlined bodies. This file's own claim stays intact.

## Correct form

A claim file contains exactly one bold declaration of the form `**<Label> (<Name>).**`, followed by proof/derivation prose, followed by exactly one `*Formal Contract:*` block. Citations to other claims (e.g., "by T4a, the field-segment constraint is equivalent to…") stay as prose — they are not bodies and must not be removed.

## File to fix

{file_path}

## Findings in this file

{findings_list}

## Fix instructions

1. Read the file.
2. Identify the file's OWN claim: the bold declaration whose label matches the yaml.label of this file (typically the first bold declaration in the file). This is what must be preserved.
3. For each finding of the form "declaration of X (canonical home: X.md)":
   - Find the bold declaration `**X (...).**` in the file.
   - Delete that declaration line.
   - Delete all text that belongs to X's body: proof prose, case analyses, sub-section headings introduced for X's proof, and X's `*Formal Contract:*` block (everything from the `*Formal Contract:*` line through the last bullet of that block).
   - Stop deletion when you reach either (a) the next bold declaration of another claim, (b) a heading or paragraph that clearly belongs to the surrounding narrative, or (c) the end of the file.
4. If the finding is "N Formal Contract blocks (expected 1)", it's the secondary signal for the declarations above. After removing inlined bodies and their Formal Contracts, the count should drop to 1. No separate action needed.
5. Preserve surrounding prose. Citations like "T4a's reverse direction" or "as shown in T4a" stay — they are references, not bodies.
6. Collapse any double blank lines created by the deletions to single blank lines. Single blank lines between paragraphs are correct.

## Do not

- Do not alter the file's own declaration, own proof, or own Formal Contract block.
- Do not extend, restructure, or refactor surrounding prose.
- Do not add meta-commentary, comments, or "removed" markers.
- Do not change yaml files.
- Do not commit.

## On apparent false positives

If a finding looks incorrect, it is almost always format drift from the canonical form, not a validator error. The convention: each claim has exactly one bold declaration in exactly one file. Apply that convention. If you genuinely cannot identify what constitutes the inlined body (e.g., the text is too tangled with the surrounding prose), stop and report via your final output rather than improvise.

## Tools

Read, Edit. Operate only on the file at the path above. Make the minimum changes required.
