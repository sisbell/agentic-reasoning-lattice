# Validate-Revise — Depends Agreement

## Context

You are fixing a structural violation of invariant #5 from the Claim File Contract:

> **Depends agreement.** The yaml `depends:` list and the markdown Formal Contract Depends section name the same set of claims.

The yaml `depends` list is authoritative. The markdown Formal Contract Depends section must name the same set of claims — each entry uses the same label as yaml.

## Correct form

yaml:
```yaml
depends:
- T0
- NAT-order
- NAT-zero
```

markdown Formal Contract block:
```
*Formal Contract:*
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies the carrier ℕ and tumbler length.
  - NAT-order (NatStrictTotalOrder) — supplies strict total order < on ℕ.
  - NAT-zero (NatZeroMinimum) — supplies 0 ∈ ℕ as the minimum.
- *Postconditions:* ...
```

Each md depends entry: `  - <label> (<name>) — <brief description>`. The `<label>` is the first token after the bullet and MUST equal a yaml.label of an existing claim. Not a kind keyword ("Definition"), not a sub-reference ("T1(c)").

## File to fix

{file_path}

## Authoritative yamls (do not edit; use for labels and names)

The first yaml below is the companion yaml for the file being fixed. Its `depends` list is authoritative — the md Depends must match this set. The yamls after it are for each depended claim, giving the `name` field to use in md Depends entries.

{yaml_bundle}

## Findings in this file

{findings_list}

## Fix instructions

1. The authoritative yamls are shown above. Use their `label` and `name` fields **verbatim** — do not guess.
2. Find the markdown Formal Contract block (`*Formal Contract:*`). If present:
   - Find the `- *Depends:*` sub-section.
   - For each companion yaml depend not yet in the md Depends: add a bullet `  - <label> (<name>) — <brief description>`, using label and name from the depended yaml shown above.
   - For each md Depends entry whose first token is a type keyword (Definition, Axiom, Lemma, Theorem, Corollary, Design-requirement), rewrite the first token to the actual label from yaml. E.g., `- Definition (Span) — ...` becomes `- Span (Span) — ...` when yaml.label is Span and yaml.name is Span.
   - For md entries that use sub-reference notation (like `T1(c)`), if the companion yaml depends on the parent only (`T1`), rewrite the md entry's first token to the parent label. Preserve the sub-reference as descriptive prose in the description part (e.g., "transitivity clause T1(c)") if it's meaningful.
   - If an md entry references a label that's not in companion yaml's depends and is not a sub-reference of a yaml depend, it's extraneous — remove the entry.
3. If the markdown file has NO `*Depends:*` section at all (some files embed dependencies inline in the Axiom prose):
   - Do NOT restructure the file to add a structured Depends section. That's a larger design call.
   - Instead, leave such files unchanged and note it in your final summary. Their findings will be surfaced in the judgment-required pass.

## Do not

- Do not change the yaml file.
- Do not edit the proof, Axiom body, Preconditions, Postconditions, or other non-Depends content.
- Do not restructure a file that uses inline-in-Axiom depends form to use a separate block. Leave it for human decision.
- Do not commit.

## On apparent false positives

If a finding looks incorrect, it is almost always format drift (wrong first token, sub-reference notation, kind-word prefix). Apply the canonical form. The yaml label is the authoritative first token of every md depends entry.

## Tools

Read, Edit. Read the companion yaml and the depended-upon yamls for authoritative labels and names. Edit only the markdown Depends section.
