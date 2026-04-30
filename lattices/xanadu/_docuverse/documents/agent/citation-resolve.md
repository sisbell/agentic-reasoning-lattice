# Citation Resolve

Pre-flight lattice-builder. For each claim in the ASN, types every claim-label reference in the claim's prose as `depends` (backward) or `forward`. Runs before cone-sweep so the soundness reviewer operates on a complete, typed citation graph rather than reconstructing it from prose during review.

## Scope

One claim per call. The sweep variant iterates every claim in the ASN; no DAG order required (each claim's classifications depend only on its own prose).

## Process

Each call:

1. Read the claim's full body and the substrate's existing `citation.depends` / `citation.forward` lists for this claim.
2. Sonnet reads the prose, identifies label-shaped references, and classifies each as `depends` or `forward`. It can use the Read tool on adjacent claim files for context (writing accurate bullets, distinguishing labels from math variables).
3. Sonnet returns a structured document: `CLASSIFICATIONS` (new ones) and `RETRACTIONS` (existing classifications that no longer fit the prose).
4. Orchestrator validates every emitted label against the cross-ASN label index (fails loudly if any don't resolve).
5. Orchestrator applies changes:
   - Inserts new bullets into `*Depends:*` and `*Forward References:*` sections (creates the `*Forward References:*` section if not yet present)
   - Removes bullets for retracted classifications
   - Emits substrate links: `citation.depends` / `citation.forward` for new classifications, `retraction` for retracted ones
   - Persists the structured output to `_docuverse/documents/citation-resolve/claims/<asn>/<claim>-<run>.md`
   - Emits `citation.resolve` classifier on the resolve doc and `provenance.derivation` from the resolve doc to each emitted citation/retraction link
6. Commits.

If Sonnet returns no classifications and no retractions, the call is a no-op — no resolve doc, no substrate writes, no commit.

## Trigger

- Sweep: `python scripts/claim-citation-resolve.py <asn>` — every claim in the ASN.
- Single claim: `python scripts/claim-citation-resolve.py <asn> --claim <label>`.

## Inputs

- The claim's `.md` body (axiom, proof, all sections)
- Substrate-sourced lists of currently-classified labels for this claim
- Same-ASN claim directory (for Read tool target)
- Cross-ASN root (for fetching foundation claim bodies when needed)

## Outputs

- Edited claim `.md` (added/removed bullets in `*Depends:*` and `*Forward References:*`)
- Substrate links: `citation.depends`, `citation.forward`, `retraction`, `citation.resolve`, `provenance.derivation`
- Resolve doc at `_docuverse/documents/citation-resolve/claims/<asn>/<claim>-<run>.md`

## Tools

- Read (claim bodies for context fetching)

The orchestrator handles all writes (.md edits, substrate emissions, commits) — Sonnet's role is bounded to producing the structured output document. Edit and Bash are not exposed.

## Convergence

A claim is considered fully resolved when Sonnet returns empty `CLASSIFICATIONS` and `RETRACTIONS` lists. A second run on a fully-resolved claim is a no-op (no resolve doc emitted, no commit).

The cone-sweep that follows operates on a lattice where every claim's citation structure has been resolved — no more `MISSING-REFERENCES` over-listing of forward refs, no more wasted expansion rounds chasing references that aren't grounding deps.
