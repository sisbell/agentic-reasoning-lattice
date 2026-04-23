# Validate-Revise — Declared Symbols Resolve

## Context

You are fixing a violation of Claim File Contract invariant #7. The claim's yaml `depends:` list is missing an owner it structurally requires. The validator detected a symbol used in the claim's Formal Contract that isn't traceable through the transitive depends closure to the claim that owns it.

The fix is narrow: add the missing owner label to the yaml's `depends` list. Do not touch anything else.

## Correct form

Given a finding like `uses '+' but does not depend on its owner 'NAT-closure'` against `NAT-addassoc.yaml` whose current content is:

```yaml
label: NAT-addassoc
name: NatAdditionAssociativity
type: axiom
depends: []
summary: |
  ...
```

The fix is:

```yaml
label: NAT-addassoc
name: NatAdditionAssociativity
type: axiom
depends:
- NAT-closure
summary: |
  ...
```

Only the `depends` list changes.

## File to fix

{file_path}

## Authoritative yaml (current state; you will edit this)

{yaml_bundle}

## Findings in this file

{findings_list}

## Fix instructions

1. Read the companion yaml shown above to understand its current structure.
2. For each finding of the form `uses '<symbol>' but does not depend on its owner '<owner>'`:
   - Add `<owner>` as a new entry in the `depends` list.
   - If `depends: []` today, replace with a depends list containing the owner(s).
   - If multiple findings cite the same owner, add it once — do not duplicate.
3. Preserve every existing entry in `depends`.
4. Do not change any other yaml field: `label`, `name`, `type`, `summary`, or anything else must remain byte-identical.
5. Do not edit the companion markdown file. The depends-agreement pass that runs after this one automatically syncs the md Depends section from the yaml.

## Discipline — Resolution ranking

When a review finding admits multiple resolutions that would close it equally well, follow this ranking:

    delete > restructure > add

This is a tiebreaker for close calls, not a mandate. Findings that require adding (a missing axiom, a missing precondition, a needed clarification deletion wouldn't preserve) produce additions regardless. The ranking applies only when the choice between valid resolutions is genuinely judgment.

Within that scope, five directives:

1. **Prefer deletion over addition.** If a finding can be resolved by deleting the flagged construction or its surrounding justification, delete. Only add when no deletion resolves the finding. (For this invariant, adding is always the fix — the missing dependency must be named.)

2. **When a finding says drop X, drop X — do not relocate.** Moving X to a different paragraph, rephrasing X in a new place, or folding X into an adjacent clause all leave the drift in the file. Relocation is not deletion.

3. **Do not justify excluded cases.** If a claim's carrier or precondition excludes a case, do not write prose about what would happen in that case.

4. **No meta-commentary.** No "this structure is exhaustive," no "matches the convention in sibling claims," no inline citation-site enumeration, no defensive justification of past findings.

5. **When adding is required, add the minimum.** A missing owner is a label added to `depends` — not a label plus an inline comment explaining why the dependency is needed plus a defense of its placement.

## Tools

Read, Edit. Read the yaml. Edit the `depends` list only. No other file, no other field.
