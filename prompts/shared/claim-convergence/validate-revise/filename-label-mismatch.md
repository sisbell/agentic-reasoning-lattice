# Validate-Revise — Filename Label Mismatch

## Context

You are fixing a structural violation of invariant #2 from the Claim File Contract:

> **Filename matches label.** The yaml `label` field equals the file's stem.

The yaml `label` is authoritative. The file's stem must match. When they disagree, rename the file — do not relabel. Relabeling cascades through every cross-file reference; renaming only touches the file itself (references in other files already use the yaml label).

## Correct form

`T4a.yaml` has `label: T4a`. `T0(a).yaml` has `label: T0(a)`. `TA-Pos.yaml` has `label: TA-Pos`.

## File to fix

{file_path}

## Authoritative yaml (do not edit; use for label)

{yaml_bundle}

## Findings in this file

{findings_list}

## Fix instructions

1. Read the yaml to confirm the authoritative `label`.
2. Rename the file pair so stems match the label:
   - `git mv <old-stem>.yaml <label>.yaml`
   - `git mv <old-stem>.md <label>.md`
3. **Reference scan**: other files may reference this claim by its OLD stem if the stem was used in any inline text. Grep the formalization directory for `<old-stem>` (as a word — not as a substring of other labels). For each hit, inspect whether it's a citation to THIS claim:
   - If yes, update it to use the label. Be careful: a plain word like "Prefix" in prose may or may not be a citation — context matters.
   - If the reference is in a structured location (yaml `depends`, markdown `- *Depends:*` section, `*Formal Contract:*` citations), update.
   - If the reference is in narrative prose and its meaning is unambiguous, update. If ambiguous, leave and note in final report.
4. Do not modify this file's contents beyond the rename (step 2 handles the rename; step 3 modifies OTHER files' references). The in-file content should already reference the authoritative label correctly.
5. After the rename and reference updates, the filename-label-mismatch finding should disappear and no references-resolve finding should arise from the rename.

## Do not

- Do not change the yaml `label` value. Yaml is authoritative.
- Do not rename files whose yaml `label` already matches stem (those aren't the targets).
- Do not commit — let the human do that.

## On apparent false positives

Rare for this rule. If a filename legitimately differs from yaml label for some reason I haven't accounted for, stop and report rather than rename.

## Tools

Read, Edit, Grep, Bash. Use `git mv` for renames (preserves history). Use Grep to find old-stem references. Use Edit to update each reference.
