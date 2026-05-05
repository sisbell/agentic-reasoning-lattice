# Claim Decompose

First-pass structural analysis of a note. Mechanically splits the note into sections, then runs an LLM on each non-structural section to produce a YAML hypothesis listing the claims that section appears to introduce.

## Scope

One note per invocation. Reads the note's md from the docuverse. Writes per-section md and yaml files to `_workspace/claim-derivation/<asn_label>/sections/`. Emits no substrate links.

## Process

1. Locate the source note by ASN number and read its md text.
2. Split mechanically at `## ` headers into `(header, content)` pairs.
3. Write each section's content as `NN-slug.md` under the workspace sections dir (including structural sections — PREAMBLE, "Claims Introduced", "Open Questions", "Worked example").
4. For non-structural sections, call the decompose prompt in parallel (sonnet, high effort). Each call produces a YAML structural analysis listing the candidate claims in that section.
5. Write each yaml as `NN-slug.yaml` alongside the md.
6. Commit the workspace changes via `step_commit_asn`.

## Prompts

- `prompts/shared/claim-derivation/decompose.md`

## Tools

- None. Uses `claude --print` with `--tools ""` for the structural-analysis calls.

## Operator Gate

Decompose is the place where new structure is created — every downstream phase (annotate, transclude, produce-contract, validate-gate) builds on the YAML hypothesis this agent produces. The operator inspects the per-section yamls and decides whether the decomposition is sane before letting the rest of the derivation pipeline run. Until the agent has earned trust, this stays operator-invoked rather than predicate-fired.
