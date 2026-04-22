# Shared Domain Tier

Prompts (and potentially other assets) that apply across every lattice — structural, domain-neutral content that doesn't carry a particular domain's vocabulary.

## `prompts/`

Prompts operating on structural concepts (claim labels, dependency graphs, formal contracts, proof structure, review verdicts) with no references to any specific domain. Each pipeline stage loads prompts through `scripts/lib/shared/paths.py::prompt_path(subpath)`, which prefers a lattice-specific override under `domains/<lattice>/prompts/<subpath>` and falls back to `domains/_shared/prompts/<subpath>`.

A lattice that wants to customize a shared prompt simply authors its own copy at the lattice-specific path. No plumbing changes.
