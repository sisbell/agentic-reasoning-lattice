# Validate-Revise — Declaration Label Mismatch

## Context

You are fixing a structural violation of the Claim Document Contract:

> **Declaration matches label.** The markdown body contains exactly one bold claim-declaration of the form `**<Label> (<Name>).**`. The label-position equals the filename stem; the parenthetical equals the claim's canonical `name` (the first line of the sibling `<stem>.name.md` doc, recorded by the substrate `name` link). When label and name are the same, the parenthetical repeats it — redundant but uniform. The parenthetical is required in all cases. Type keywords (*axiom*, *definition*, *design-requirement*, *lemma*, *theorem*, *corollary*, *consequence*) do not appear in the label-position.

In this file, the markdown declaration does not match the canonical (label, name) pair — typically because it uses a type keyword (like "Definition") in the label position instead of the filename stem.

## Correct form

Given filename `Divergence.md` with substrate name `Divergence`:

```
**Divergence (Divergence).** <rest of the claim>
```

Given filename `Prefix.md` with substrate name `PrefixRelation`:

```
**Prefix (PrefixRelation).** <rest of the claim>
```

Given filename `T4a.md` with substrate name `SyntacticEquivalence`:

```
**T4a (SyntacticEquivalence).** <rest of the claim>
```

The parenthetical name is mandatory even when label and name are the same, for uniformity.

## File to fix

{file_path}

## Canonical metadata (use verbatim; do not guess)

{metadata_bundle}

## Findings in this file

{findings_list}

## Fix instructions

1. The companion claim's canonical (label, name) pair is shown above. **Use them verbatim — do not guess.** The declaration must be `**<label> (<name>).**`.
2. Locate the bold declaration at the top of the markdown body. It may take the form `**<kind> (<something>).**` where `<kind>` is a type keyword (Definition, Axiom, Lemma, Theorem, Corollary, Design-requirement), or it may have some other drift.
3. Rewrite the declaration to the canonical form using the exact label and name from the metadata shown above.
4. Leave the rest of the sentence (the prose immediately following the `**...**` declaration) unchanged.
5. If a section heading above the declaration duplicates the type keyword (e.g., `## Definition (Span)` above `**Definition (Span).**`), remove or correct the heading so it doesn't reintroduce the drift. Prefer removing the redundant heading over keeping a corrected one.

## Do not

- Do not modify the proof, Formal Contract, or other content beyond the declaration line and any duplicating section heading.
- Do not add meta-commentary.
- Do not commit.

## On apparent false positives

If a finding looks incorrect, it is almost always format drift, not a validator error. The convention: the bold declaration's label-position equals the filename stem; the parenthetical equals the canonical `name`; a type keyword never appears in the label-position. Apply that convention.

## Tools

Read, Edit. Edit only the markdown. Make the minimum change.
