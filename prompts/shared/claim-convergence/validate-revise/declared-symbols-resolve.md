# Validate-Revise — Declared Symbols Resolve

## Context

You are fixing a violation of Claim Document Contract invariant #5: the
claim's substrate citations are missing an owner it structurally
requires. The validator detected a symbol used in the claim's Formal
Contract that isn't traceable through the transitive citation closure
to the claim that owns it.

The fix is narrow: file a substrate citation from the claim being fixed
to the missing owner. Do not edit the markdown — the depends-agreement
pass that follows will sync the md `*Depends:*` section once the
citation exists.

## File to fix

{file_path}

## Canonical metadata (use verbatim; do not guess)

{metadata_bundle}

## Findings in this file

{findings_list}

## Fix instructions

For each finding of the form `uses '<symbol>' but does not depend on its owner '<owner>'`:

1. Add the citation by running:

       PROTOCOL_DOC_PATH=<path-to-the-claim-md> python scripts/cite.py --to <owner>

   Where `<path-to-the-claim-md>` is the file shown under "File to fix"
   above, and `<owner>` is the owner label from the finding (e.g.,
   `NAT-closure`).

2. If multiple findings cite the same owner, run cite.py once for that
   owner — it is idempotent.

The citation is filed in the substrate. The companion markdown is left
alone in this pass.

## Do not

- Do not edit the markdown body.
- Do not file citations to anything other than the owners named in the findings.
- Do not commit.

## Tools

Read, Bash. Use Bash only to invoke `scripts/cite.py`.
