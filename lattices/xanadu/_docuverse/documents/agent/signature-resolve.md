# Signature Resolve

Pre-flight lattice-builder for symbol ownership. For each claim, types every non-logical symbol in the claim's prose as **introduced by this claim** (vs borrowed from a dep, vs lattice notation primitive). Writes the per-claim `<label>.signature.md` sidecar and emits the `signature` substrate link.

Sister stage to citation-resolve. Where citation-resolve handles label-mentioned references in prose, signature-resolve handles symbol-introduced ownership. Both feed the substrate; both populate data the downstream validator (`declared-symbols-resolve`) consumes.

## Scope

One claim per call. The sweep variant iterates every claim in the ASN; no DAG order required (each claim's signature depends only on its own contract plus its upstream signatures).

## Process

Each call:

1. Read the claim's full body.
2. Read the lattice-wide notation primitives (`notation/notation.md`) — these are language-level symbols always in scope, never claim-introduced.
3. Walk the claim's `citation.depends` transitive closure; collect each upstream claim's signature sidecar content.
4. Read the claim's existing signature sidecar (if any).
5. Sonnet identifies symbols this claim *introduces* (vs borrows, vs primitive).
6. Sonnet returns structured output: `INTRODUCES` (new symbols) and `REMOVES` (symbols no longer in the contract).
7. Orchestrator computes the merged sidecar content and writes it via `emit_attribute(claim, "signature", ...)`. The substrate `signature` classifier link is emitted idempotently.
8. Persists the resolve doc at `_docuverse/documents/signature-resolve/claims/<asn>/<claim>-<run>.md`.
9. Commits.

If Sonnet returns no introductions and no removals, the call is a no-op — no sidecar update, no resolve doc, no commit.

## Trigger

- Sweep: `python scripts/claim-signature-resolve.py <asn>` — every claim in the ASN.
- Single claim: `python scripts/claim-signature-resolve.py <asn> --claim <label>`.

Initial bulk populate is a sweep run on the ASN (cost ~$5–10 per ASN, ~30 min). Ongoing maintenance: rerun on individual claims after their prose changes substantially. Cone-review's safety-net catches gaps the resolver missed (currently expensive — populating signatures lets the cheaper validator do this work mechanically).

## Inputs

- Claim's `.md` body
- Notation primitives list (lattice-wide)
- Upstream signatures (collected from transitive citation.depends)
- Existing signature sidecar (preserved unless prose shifted)

## Outputs

- Updated `<label>.signature.md` sidecar
- `signature` substrate link from claim md → sidecar (idempotent)
- Resolve doc at `_docuverse/documents/signature-resolve/claims/<asn>/<claim>-<run>.md`
- Each citation produced by the *downstream* `declared-symbols-resolve` validator carries `provenance.derivation` traceable back through the validator's fix recipe — distinguishing label-discovered (citation-resolve) from symbol-discovered (this stage feeding the validator) is preserved through the resolve doc and substrate metadata.

## Tools

- Read (claim body for context fetching during reasoning)

The orchestrator handles all writes (sidecar, substrate emit, commit). Sonnet's role is bounded to producing the structured output document. No Edit, no Bash.

## Convergence

Per claim: Sonnet returns empty `INTRODUCES` and `REMOVES` lists. Per-ASN: every claim has been visited at least once and the sidecar reflects current contract state. No iteration needed within a claim — signature determination is a one-shot transformation, not a convergence loop.
