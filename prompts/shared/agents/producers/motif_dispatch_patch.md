# Motif Dispatch — Case 1 Patch Generator

You're deciding whether a rederiving note's claims need to be patched
to cite a canonical claim, or whether they already cite cleanly.

The motif identifies a construct that's already canonicalized in a
base note. This rederiving note has its own claims about the same
construct. Read those claims carefully and decide:

- **PATCH** — the rederiving claims restate or independently prove the
  canonical's content rather than citing it. Generate a patch
  instruction telling the patch agent what to rewrite.
- **NONE** — the rederiving claims already cite the canonical with
  per-context wrappers (specialization, application). No work needed.

## The motif

{{motif}}

## The canonical claim (in the base note)

The base note's relevant claim is in ASN-{{base_label}}. The motif's
attribution rationale (which identified this base) is:

{{attribution_rationale}}

## The rederiving note ({{rederiving_label}}, full body)

{{rederiving_note}}

## Output

A single YAML document — no code fences, no prose preamble:

    action: PATCH       # or NONE
    rationale: |
      One sentence: why patch, or why no patch is needed.
    patch_body: |       # only if action: PATCH; omit for NONE
      Instruction prose for the patch agent. Name the specific claims
      in this note to rewrite, name the canonical they should cite,
      and describe the kind of revision needed (typically "replace
      independent derivation with a citation to canonical").
