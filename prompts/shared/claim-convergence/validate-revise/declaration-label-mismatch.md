# Validate-Revise — Declaration Label Mismatch

## Context

You are fixing a structural violation of invariant #3 from the Claim File Contract:

> **Declaration matches label.** The markdown body contains exactly one bold claim-declaration of the form `**<Label> (<Name>).**`. The label-position equals the yaml `label` field; the parenthetical equals the yaml `name` field (when `label == name`, the parenthetical repeats it — redundant but uniform). The parenthetical is required in all cases. Type keywords (*axiom*, *definition*, *design-requirement*, *lemma*, *theorem*, *corollary*, *consequence*) do not appear in the label-position.

The yaml `label` is authoritative. The filename and the markdown declaration must conform to it. In this file, the markdown declaration does not match the yaml label — typically because it uses a type keyword (like "Definition") in the label position instead of the claim's actual label.

## Correct form

Given `label: Divergence` and `name: Divergence` in the yaml:

```
**Divergence (Divergence).** <rest of the claim>
```

Given `label: Prefix` and `name: PrefixRelation`:

```
**Prefix (PrefixRelation).** <rest of the claim>
```

Given `label: T4a` and `name: SyntacticEquivalence`:

```
**T4a (SyntacticEquivalence).** <rest of the claim>
```

The parenthetical name is mandatory even when label and name are the same, for uniformity.

## File to fix

{file_path}

## Authoritative yaml (do not edit; use for label and name)

{yaml_bundle}

## Findings in this file

{findings_list}

## Fix instructions

1. The companion yaml is shown above. **Use the `label` and `name` fields from that yaml verbatim — do not guess.** The declaration must be `**<yaml.label> (<yaml.name>).**`.
2. Locate the bold declaration at the top of the markdown body. It may take the form `**<kind> (<something>).**` where `<kind>` is a type keyword (Definition, Axiom, Lemma, Theorem, Corollary, Design-requirement), or it may have some other drift.
3. Rewrite the declaration to the canonical form using the exact label and name from the yaml shown above.
4. Leave the rest of the sentence (the prose immediately following the `**...**` declaration) unchanged.
5. If a section heading above the declaration duplicates the type keyword (e.g., `## Definition (Span)` above `**Definition (Span).**`), remove or correct the heading so it doesn't reintroduce the drift. Prefer removing the redundant heading over keeping a corrected one.

## Do not

- Do not change the yaml file.
- Do not modify the proof, Formal Contract, or other content beyond the declaration line and any duplicating section heading.
- Do not add meta-commentary.
- Do not commit.

## On apparent false positives

If a finding looks incorrect, it is almost always format drift, not a validator error. The convention: the bold declaration's label-position equals yaml.label; the parenthetical equals yaml.name; a type keyword never appears in the label-position. Apply that convention.

## Tools

Read, Edit. Read the yaml for authoritative label/name. Edit only the markdown. Make the minimum change.
