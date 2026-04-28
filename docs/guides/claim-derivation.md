# Guide: Claim Derivation

Claim derivation is a one-shot module that transforms a converged note into per-claim files conforming to the [Claim File Contract](../design-notes/claim-file-contract.md). It sits between [note convergence](../protocols/note-convergence-protocol.md) and [claim convergence](../protocols/claim-convergence-protocol.md). For the formal specification see the [Claim Derivation Module](../modules/claim-derivation-module.md); for execution steps see the [runbook](../runbooks/claim-derivation.md).

## Phases

Six sequential phases, each commits automatically.

### 1. Decompose

Mechanical `##` split of the note's markdown into sections. Per-section LLM analysis (parallel across sections) produces structured YAML listing each section's claims (label, name, body extract, formal contract). Section YAMLs are written to `_workspace/claim-derivation/<asn>/sections/`.

Structural sections (PREAMBLE, Claims Introduced, Open Questions, Worked example) are skipped — they contain metadata, indexes, or illustrative content rather than derivable claims.

### 2. Enrich

Three independent LLM passes per claim, parallel within and across claims. Each pass updates the section YAML in place:

1. **Type** — classifies as axiom, definition, design-requirement, lemma, theorem, corollary, or consequence.
2. **Dependencies** — extracts claim labels referenced in the proof or design justification.
3. **Signature** — extracts non-logical symbols the claim introduces (constants, function symbols, relation symbols).

### 3. Transclude

Mechanical projection — no LLM. For each claim:

- Writes the body markdown `<label>.md` as a verbatim byte-substring of the source note's region (resolved via exact match, then whitespace-normalized).
- Writes the substrate-managed sidecars: `<label>.label.md`, `<label>.name.md`, `<label>.description.md`, and `<label>.signature.md` (only when the enricher's signature pass produced non-empty content).
- Emits substrate links: `claim` and `contract.<kind>` classifiers on the body; `label` / `name` / `description` / `signature` attribute links pointing the body at its sidecars; `citation` links for declared dependencies; `provenance.derivation` link from the source note.

The byte-substring discipline is strict — fuzzy matching is silent acceptance of unexplained drift, so the resolver fails loud on no-match and the failed claim is reported rather than written.

### 4. Validate-transclude

Mechanical substring check, no LLM. Confirms each claim body is a byte-substring of its source note. The next phase (produce-contract) intentionally diverges from this property by appending Formal Contract sections; this check fires here so any earlier drift surfaces before that boundary rather than propagating silently.

### 5. Produce-contract

Per-claim LLM rewrite that synthesizes the Formal Contract section in each claim's body markdown. Bounded internally to three cycles per claim and gated by a review-rewrite prompt that checks for damage to Axioms, Preconditions, Postconditions, and other formal fields. Hash-based dirty detection skips claims whose prose is unchanged since the last successful rewrite.

The same `produce_contract` function lives in `lib/claim_derivation/produce_contract.py` and is reused by claim convergence's quality-pass orchestrator when prose changes during convergence dirty an existing contract.

### 6. Validate-gate

The same gate that claim convergence runs before each review cycle. The validator (mechanical, no LLM) runs every steady-state and transition-checkable structural invariant from the Claim File Contract. For each actionable finding it dispatches a per-rule fix-recipe prompt — operating on a constrained surface (Depends bullets, label-position tokens, citation links) and forbidden by prompt contract from modifying semantic content. Bounded by MAX_ITER iterations (currently 3) plus a no-progress halt.

## Output structure

```
_workspace/claim-derivation/ASN-NNNN/
  sections/
    00-preamble.md                ← mechanical split
    01-two-components-of-state.md
    01-two-components-of-state.yaml  ← LLM analysis + enrichment (workspace-only)
    ...

_docuverse/documents/claim/ASN-NNNN/
  <Label>.md                      ← body: prose, proof, Formal Contract
  <Label>.label.md                ← label sidecar
  <Label>.name.md                 ← name sidecar
  <Label>.description.md          ← description sidecar
  <Label>.signature.md            ← signature sidecar (optional)
```

The section YAMLs in `_workspace/` are workspace-only intermediate state; the module's output is the substrate-classified claim documents and their sidecars in `_docuverse/`. Substrate links classifying each body and pointing at its sidecars live in the substrate's link store.

## Re-running

Re-invoking the module on a note whose derivation has already produced a claim set is destructive: each claim body is overwritten with the byte-aligned source projection (Phase 3), discarding any edits made by claim convergence; Formal Contracts are re-synthesized. The source note is the historical record; the claim set is the current projection. Production choreography routes prose-change cases through claim convergence's own quality pass — which reuses this module's `produce_contract` on dirty claims — not through re-running derivation.

## See also

- [Claim Derivation Module](../modules/claim-derivation-module.md) — formal specification with safety/liveness properties, algorithm, and correctness arguments.
- [Claim File Contract](../design-notes/claim-file-contract.md) — the structural contract this module's output must satisfy.
- [Claim Derivation runbook](../runbooks/claim-derivation.md) — step-by-step execution.
- [Claim Derivation](../claim-derivation.md) — narrative description of the derivation stage.
