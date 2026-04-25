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

## Tools

Read, Edit. Read the yaml. Edit the `depends` list only. No other file, no other field.
