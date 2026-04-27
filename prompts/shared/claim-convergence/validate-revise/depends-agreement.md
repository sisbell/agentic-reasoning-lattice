# Validate-Revise — Depends Agreement

## Context

You are fixing a structural violation of invariant #5 from the Claim File Contract:

> **Depends agreement.** The substrate's set of active `citation` links from this claim and the markdown Formal Contract Depends section name the same set of claims.

The substrate's active citation set is authoritative. The md `*Depends:*` section must mirror it.

The validator emits two finding shapes for this rule:

- **`only_in_store`** — substrate has a citation that md doesn't list. Two interpretations: the proof actually uses the dep and md is missing the bullet (resolution: ADD), or the proof has been rewritten and the substrate citation is stale (resolution: RETRACT).
- **`only_in_md`** — md has a bullet for a dep that has no active substrate citation. This pass does NOT handle that case; mark each such finding as SKIP.

## Correct form

md Formal Contract block:
```
*Formal Contract:*
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies the carrier ℕ and tumbler length.
  - NAT-order (NatStrictTotalOrder) — supplies strict total order < on ℕ.
  - NAT-zero (NatZeroMinimum) — supplies 0 ∈ ℕ as the minimum.
- *Postconditions:* ...
```

Each md depends entry: `  - <label> (<name>) — <brief description>`. The `<label>` is the first token after the bullet and must equal the depended claim's filename stem. Not a kind keyword ("Definition"), not a sub-reference ("T1(c)").

## File to fix

{file_path}

## Canonical metadata (use verbatim; do not guess)

The first row below is the companion claim being fixed. The rows after it are each claim referenced by the substrate's active citations from this file, giving the canonical `name` to use in md Depends entries.

{metadata_bundle}

## Findings in this file

{findings_list}

## Fix instructions

For each finding above, decide its resolution by reading the proof body of the file being fixed:

### `only_in_store` findings

Read the md body (Axiom, Definition, Proof, Derivation, Preconditions, Postconditions). Locate any specific proof step, cited lemma, or used symbol the dep supplies.

- **Use-site found** → **ADD**: insert `  - <label> (<name>) — <brief description>` into the `*Depends:*` block, using label and name from the metadata block above and a gloss naming the concrete usage.
- **No use-site anywhere in the proof** → **RETRACT**: leave md unchanged. The substrate citation is stale from a prior proof version. The orchestrator will file a `retraction` link nullifying it.
- **Uncertain** → **SKIP**: leave md unchanged; describe your doubt in the rationale.

Do NOT fabricate a use-site to justify ADD. Do NOT silently delete bullets you didn't check.

For md entries whose first token is a type keyword (Definition, Axiom, Lemma, Theorem, Corollary, Design-requirement) or a sub-reference (`T1(c)`), rewrite the first token to the actual label from the metadata block. Preserve sub-reference notation as descriptive prose where meaningful (e.g., "transitivity clause T1(c)").

If the md file has no `*Depends:*` section at all (some files embed dependencies inline in the Axiom prose), do NOT restructure the file. Mark all `only_in_store` findings for it as SKIP and note the form in your rationale.

### `only_in_md` findings

Out of scope for this pass. Mark each as SKIP with rationale `"only_in_md is handled by the symmetric cite pass, not this rule"`.

## Required output: `__decisions.json`

Before exiting, you MUST write a file named `__decisions.json` in your working directory containing one entry per finding above. Use the `Edit` tool to create it.

Format:

```json
[
  {"label": "NAT-cancel",   "action": "RETRACT", "rationale": "no use-site found in Axiom/Proof/Derivation"},
  {"label": "NAT-discrete", "action": "RETRACT", "rationale": "not referenced anywhere in proof body"},
  {"label": "NAT-extra",    "action": "ADD",     "rationale": "used in Lemma at line 47"}
]
```

Schema:
- `label` — string; must match a label that appears in the findings list above.
- `action` — string; one of `"ADD"`, `"RETRACT"`, `"SKIP"`.
- `rationale` — short string explaining the decision.

The orchestrator validates this file:
- Missing file, invalid JSON, unknown action, label not in findings, label not in the lattice, or ADD without a corresponding new bullet in your edit → hard error; the pass aborts for this file. **Get the file right.**

## Do not

- Do not edit the proof, Axiom body, Preconditions, Postconditions, or non-Depends content.
- Do not call `git`, `bash`, or any script directly. The orchestrator owns substrate writes.
- Do not commit.
- Do not restructure a file that uses inline-in-Axiom depends form to use a separate block.

## Tools

`Read`, `Edit`. Read the file being fixed; edit the file's md Depends section and create `__decisions.json`. Use the metadata block above for label/name lookups.
