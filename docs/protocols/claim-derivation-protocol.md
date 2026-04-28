# Claim Derivation Protocol

The protocol that decomposes a converged note into per-claim file pairs. Takes a note (the output of [consultation](consultation-protocol.md) refined through [note convergence](note-convergence-protocol.md)) and produces a structured set of YAML metadata + Markdown body pairs, one per claim, conforming to the [Claim File Contract](../design-notes/claim-file-contract.md). The output enters [claim convergence](claim-convergence-protocol.md) for review/revise cycles.

One-shot — terminates when the structural contract holds on the output. The narrative description of the derivation stage lives in [Claim Derivation](../claim-derivation.md).

Following the modular formalism of Cachin (*Reliable and Secure Distributed Programming*).

---

## 1 Document model

### Document types

| Classifier | What the document is |
|---|---|
| `note` | The input. A converged reasoning document containing claims interleaved in narrative prose. (Same classifier as note convergence input/output.) |
| `claim` | The output. A per-claim file pair — `{label}.yaml` (metadata) + `{label}.md` (body + formal contract). (Also the classifier claim convergence operates on.) |

### Link types

| Type | Subtypes | Role |
|---|---|---|
| `claim` | (flat, one-sided) | Classifier: document is a claim. Filed by decomposition as part of admitting each claim to the lattice. |
| `citation` | (flat) | Claim depends on claim. Filed by decomposition from each claim's `depends:` metadata. |
| `contract` | `axiom`, `definition`, `theorem`, `corollary`, `lemma`, `consequence`, `design-requirement` | Classifier: claim has a formal contract of this kind. Filed by decomposition from each claim's `type:` metadata. |
| `provenance` | `decomposition` | Records that decomposition produced this claim from this note. From = note, to = claim. Audit trail from the source document to each output pair. Sibling of the consultation protocol's `provenance.synthesis` and the maturation protocol's `provenance.{extract,absorb,reset}`. |

The `claim`, `citation`, and `contract` link types are inherited from the [claim convergence protocol](claim-convergence-protocol.md) — claim derivation is the protocol that creates them. The `provenance.derivation` link is this protocol's own provenance primitive (analog of consultation's `provenance.synthesis` link).

---

## 2 Modules used

### 2.1 Substrate

The persistent, append-only link graph. See [Substrate Module](substrate.md). This protocol relies on SUB1 (permanence — for the `claim`, `contract`, `citation`, and `provenance.derivation` links it emits) and SUB2 (query soundness). Claim derivation does not file or interact with retraction links; SUB4–SUB6 are not relied upon.

### 2.2 Structural validator

A mechanical checker (no LLM) that evaluates the per-claim file pairs against the [Claim File Contract](../design-notes/claim-file-contract.md). Used by this protocol's final phase and re-used by claim convergence's [validate-before-review](../patterns/validate-before-review.md) gate.

**Properties relied upon.**

- SV1 (Completeness). Every violation of a structural invariant is reported.
- SV2 (Soundness). Every reported violation is a genuine violation.
- SV3 (Determinism). Given the same input, the validator produces the same output. No LLM, no judgment.

### 2.3 Decomposition prompts

Per-phase LLM prompts that drive section analysis, type classification, dependency extraction, and vocabulary extraction. The prompts enforce structured output (YAML conforming to a schema) so downstream phases can read them mechanically without natural-language parsing.

---

## 3 Participants and events

### Decomposer

Splits the note mechanically at `##` section headers, then invokes per-section LLM calls that produce structured YAML capturing each section's claims (label, name, body, formal contract). The mechanical split is deterministic; the per-section LLM call is parallel across sections. Skips structural sections (e.g., `PREAMBLE`, `Claims Introduced`, `Open Questions`) that contain no derivable claims.

The split-mechanical-then-LLM-analyze pattern is deliberate: section boundaries are reliable markdown structure (deterministic, zero cost, no judgment needed), while identifying claims within a section requires reading the reasoning (LLM judgment). Burning an LLM call on section splitting would add cost and non-determinism to a step that is already solved by string splitting.

### Enricher

Reads the section YAMLs from decomposition. Per-claim, runs three independent LLM passes — type classification (axiom/definition/theorem/...), dependency extraction (which other claims this one cites), and vocabulary extraction (which symbols this claim introduces). Passes are parallel within a claim and across claims. Updates the section YAMLs in place.

This three-pass decomposition (rather than one comprehensive prompt) is a deliberate choice — focused prompts produce more reliable output than broad ones, and parallel execution reduces wall-clock cost.

### Transcluder

Reads the enriched section YAMLs and writes per-claim `{label}.yaml` (metadata) + `{label}.md` (body + formal contract) pairs to the lattice's directory. Deterministic — no LLM. One file pair per declared claim.

### Validator

Mechanical structural checker. Reads the per-claim file pairs and evaluates them against the [Claim File Contract](../design-notes/claim-file-contract.md)'s structural invariants. Emits a violation report or signals validation success.

### Fix recipe agent

Resolves structural violations reported by the validator. One violation, one fix. Per-invariant recipes constrain each fix to one violation class with a specific resolution strategy. The recipes are documented in [Validate Before Review](../patterns/validate-before-review.md) — each invariant in the [Claim File Contract](../design-notes/claim-file-contract.md) has one corresponding recipe in the validate-before-review pattern's recipe set. Runs after the validator; the validator re-checks after fixes.

### Events

**Requests (input from above).**

- ⟨ Decompose | note ⟩ — initiate the protocol on this note.

**Internal events** (visible to participants but not to the upper interface).

- ⟨ SplitSections | note ⟩ — split the note into section analyses.
- ⟨ Enrich | section_yamls ⟩ — augment each claim with type, dependencies, vocabulary.
- ⟨ Transclude | enriched_sections ⟩ — write per-claim file pairs.
- ⟨ Validate | claim_pairs ⟩ — run structural checks.

**Indications (output upward).**

- ⟨ ClaimSetProduced | note, claims ⟩ — the protocol has produced a valid claim set. Each claim carries the `claim` classifier, a `contract.<kind>` link reflecting its type, `citation` links for its declared dependencies, and a `provenance.derivation` link from the source note.
- ⟨ DerivationFailed | note, violations ⟩ — the validator reported violations that could not be auto-resolved. No claim set is produced.

---

## 4 Termination

The protocol terminates on output production — no convergence predicate, no iteration. A single ⟨ Decompose ⟩ request results in either:

- ⟨ ClaimSetProduced | note, claims ⟩ — success. The Claim File Contract's structural invariants hold on the output. Substrate links are filed per the document model (§1).
- ⟨ DerivationFailed | note, violations ⟩ — failure. The validator reported invariant violations the protocol could not auto-resolve. The output is left in place but does not enter claim convergence.

Termination is structural: the protocol's state machine is split → enrich → transclude → validate → indicate. There is no loop.

---

## 5 Properties

### 5.1 Safety

**B1 (Source coverage).** Every claim in the source note produces exactly one output file pair. No source claim is dropped; no source claim is duplicated across multiple pairs.

**B2 (No fabrication).** Every output file pair corresponds to a claim in the source note. Claim derivation does not invent claims that the source did not contain.

**B3 (Content preservation).** Each source claim's narrative, proof, and formal contract text appears in its corresponding file pair. Textual presence is mechanically checkable (the validator can detect empty bodies or missing contract sections). Semantic fidelity — whether the per-claim form preserves what the narrative actually meant — is not mechanically checkable and surfaces as `comment.revise` findings in claim convergence. B3 guarantees the text arrived; the quality boundary (§5.3) and downstream review guarantee it arrived intact.

**B4 (Source freezing).** The source note is frozen at the moment decomposition begins. It becomes the record of discovery, not a living document. Modifications to the note after decomposition has started do not propagate to the claim file set. The note and the claim files are separate artifacts from this point forward. This connects to the [maturation protocol](maturation-protocol.md)'s hard reset — unfreezing is a cascading structural operation.

**B5 (Structural contract).** On ⟨ ClaimSetProduced ⟩, every steady-state invariant of the [Claim File Contract](../design-notes/claim-file-contract.md) holds on the output: file-pair completeness, filename-matches-label, declaration-matches-label, YAML well-formed, depends agreement, references resolve, declared symbols resolve, acyclic dependency graph, body uniqueness. (Relies on SV1, SV2.)

**B6 (Acyclicity).** The `citation` subgraph induced by the output's `depends:` lists is a directed acyclic graph. Decomposition refuses to emit ⟨ ClaimSetProduced ⟩ if it would introduce a cycle. (Subsumed by B5 but called out separately because it is the property most often violated by enricher errors.)

**B7 (Provenance recording).** On ⟨ ClaimSetProduced | note, claims ⟩, the substrate contains, for each claim in the output: a `claim` classifier on the claim document, a `contract.<kind>` link reflecting its type, `citation` links for its declared dependencies, and a `provenance.derivation` link from the source note to the claim. (Relies on SUB1.)

### 5.2 Liveness

**BL1 (Termination).** If the LLM phases (decompose, enrich) complete and the transcluder runs without I/O failure, then the validator either reports success — yielding ⟨ ClaimSetProduced ⟩ — or reports violations — yielding ⟨ DerivationFailed ⟩. The protocol does not loop indefinitely.

**BL2 (Completeness of decomposition).** Every non-structural section of the source note is processed by the decomposer. No section is silently skipped.

### 5.3 Quality boundary

These are content quality targets, not graph properties. The validator does not enforce them; review enforces them. They surface as semantic findings in claim convergence rather than as decomposition errors.

**Summary matches body.** Each claim's YAML `summary` field describes what the markdown body claims. Not a restatement of the formal contract; not stale relative to the body.

**Exterior matches interior.** Each claim's stated postconditions are delivered by its proof. Its preconditions are sufficient for the proof and do not exceed what callers must supply.

**Symbol usage matches declaration.** Symbols declared with a given signature or meaning are used consistently with that declaration throughout the proof.

These three semantic invariants are documented in the [Claim File Contract](../design-notes/claim-file-contract.md) as review-enforced.

### 5.4 Deliberate non-guarantees

**No semantic correctness.** Claim derivation guarantees structural form (B1–B7) but not the semantic correctness of any claim. A claim with a wrong proof, an over-stated postcondition, or an ungrounded operator passes decomposition if its structural form is valid. Semantic pressure comes from claim convergence.

**No semantic preservation beyond text.** B3 (content preservation) is mechanical — the words appear. Whether the per-claim form preserves what the narrative actually meant is a semantic question that surfaces in claim convergence, not decomposition.

**No idempotence.** Re-running decomposition on the same note produces a different claim set (LLM stochasticity in decompose and enrich). Production protocols don't promise the same output twice.

**No iteration.** If the produced claim files are semantically inadequate (wrong types, missing dependencies, unclear proofs), the protocol does not re-run decomposition. Refinement is claim convergence's job.

---

## 6 Algorithm: split → enrich → transclude → validate-transclude → produce-contract → validate-gate

Implements: Claim Derivation Protocol (§1–§5).
Uses: Substrate (§2.1), Structural Validator (§2.2), Decomposition prompts (§2.3).

Six phases. The first three are sequential one-shots. The fourth (validate-transclude) is a quick mechanical substring check at the transclude exit boundary. The fifth (produce-contract) iterates per-claim with bounded retries internal to that phase. The sixth (validate-gate) is a bounded structural-only fix loop that terminates on contract satisfaction or maximum-iterations. The protocol does not run review/revise on semantic content — that is claim convergence's role.

### 6.1 State

- *note* — the input note document (read directly from the docuverse, not copied).
- *sections* — intermediate result: list of (header, content) pairs after mechanical split, written to `_workspace/claim-derivation/<asn>/sections/`.
- *section_yamls* — intermediate result: per-section YAML analyses listing each section's claims and metadata.
- *claim_set* — output: per-claim body markdown + sidecars in `_docuverse/documents/claim/<asn>/`, plus the substrate links described in §1.

### 6.2 Phase 1 — Split

```
upon ⟨ Derive | note ⟩ do
  sections ← split_at_headers(note)            ; deterministic
  section_yamls ← []
  for (header, content) in sections in parallel:
    if is_structural(header):                  ; PREAMBLE, Claims Introduced, etc.
      continue
    yaml_analysis ← invoke_llm(decompose_prompt, content)
    section_yamls.append((header, yaml_analysis))
```

Mechanical section split is deterministic — splits the note's markdown at `##` headers. Per-section LLM analysis runs in parallel across sections. Each LLM call produces structured YAML listing the section's claims (label, name, body extract). The `is_structural` predicate is a closed list defined in the decomposer implementation — currently `PREAMBLE`, `Claims Introduced`, `Open Questions`, and `Worked example`. Sections matching these headers contain metadata, indexes, or illustrative content rather than derivable claims.

### 6.3 Phase 2 — Enrich

```
upon section_yamls produced do
  for each claim in flatten(section_yamls) in parallel:
    type        ← invoke_llm(type_prompt, claim)
    depends     ← invoke_llm(deps_prompt, claim, neighbors)
    vocabulary  ← invoke_llm(vocab_prompt, claim)
    update_yaml(claim, type, depends, vocabulary)
```

Three independent LLM passes per claim. Each pass has a focused prompt and produces a single field. Passes run in parallel within a claim and across claims. The enriched YAML is written back to the section files in place.

### 6.4 Phase 3 — Transclude

```
upon enrichment complete do
  for each claim in flatten(section_yamls):
    body ← find_in_source(note, claim.llm_body)       ; resolver
    if body is None:
      record_failure(claim); continue
    write_md(<claim_dir>/<label>.md, body)             ; source bytes, not LLM bytes
    write_md(<claim_dir>/<label>.label.md, label)      ; sidecar
    write_md(<claim_dir>/<label>.name.md, name)        ; sidecar
    emit_link(claim, body_md)                          ; classifier
    emit_link(contract.<kind>, body_md)                ; if type set
    emit_link(label, body_md → label_sidecar)
    emit_link(name, body_md → name_sidecar)
    for dep in claim.depends:
      emit_link(citation, body_md → dep_md)
  for each emitted claim:
    emit_link(provenance.derivation, note → body_md)
  relocate_structural_sections(_workspace/.../structural/)
```

The body markdown is a verbatim byte-substring of the source note's region, resolved via the `find_in_source` helper (exact match, then whitespace-normalized). Strict by design — fuzzy matching is silent acceptance of unexplained drift, so the resolver fails loud on no-match and the failed claim is reported rather than written. Description sidecars are not emitted here — that responsibility lies with the summarize stage downstream of derivation.

### 6.5 Phase 3.5 — Validate-transclude

```
upon transclude complete do
  for each claim_md in claim_dir:
    if claim_md is sidecar or _-prefixed: skip
    body ← read(claim_md).rstrip()
    if body not in source_note_text:
      record_violation(claim_md)
  if any violations:
    indicate ⟨ DerivationFailed | note, substring_violations ⟩; halt
```

Mechanical substring check, no LLM. Confirms each claim body is a byte-substring of its source note — the content-preservation invariant at the transclude exit boundary. By construction, transclude's `find_in_source` resolver returns source bytes, so this check passes if transclude is correct. Its role is runtime documentation of the contract: if transclude ever drifts, the failure surfaces here rather than silently propagating into produce-contract.

This is the only phase where the substring property is enforced. Subsequent phases legitimately diverge: produce-contract appends Formal Contract sections (content not in source); validate-revise heals structural form. The Claim File Contract's invariant 12 is transition-checkable at this phase's exit only — never at derivation exit.

### 6.6 Phase 4 — Produce-contract

```
upon transclude complete do
  candidates ← find_claims_needing_quality(asn)
  for each candidate (in dependency order, parallel within levels):
    new_body ← invoke_llm(produce_contract_prompt, candidate, dep_context)
    review_ok ← invoke_llm(review_rewrite_prompt, candidate, new_body)
    if review_ok:
      write_md(claim_path, new_body)
```

Per-claim LLM rewrite that synthesizes the Formal Contract section in each claim's body markdown. Initial synthesis is the protocol's responsibility because the Claim File Contract's steady-state structural invariants (depends agreement, references resolve, declared symbols resolve) presuppose Formal Contract presence; claim convergence operates on already-contract-bearing claims.

The rewrite is bounded internally to three cycles per claim and gated by a review-rewrite prompt that checks for damage to Axioms, Preconditions, Postconditions, and other formal fields. Hash-based dirty detection skips claims whose prose is unchanged since the last successful rewrite, so re-running the protocol on a previously-derived ASN is incremental.

After produce-contract, the body markdown is no longer a byte-substring of the source note — by design. The Claim File Contract's content-preservation invariant (transition-checkable invariant 12) holds at *transclude exit*, not at derivation exit; subsequent phases intentionally diverge.

### 6.7 Phase 5 — Validate-gate

```
upon produce-contract complete do
  for iteration ∈ 1..MAX_ITER:
    findings ← validator.run_all_checks(claim_set)
    actionable ← filter(findings, not_declined, not_acyclic)
    if actionable is empty:
      indicate ⟨ ClaimSetProduced | note, claim_set ⟩
      return
    if no_progress(actionable, prev):
      break
    declined ← validate_revise.run_passes(actionable)
  indicate ⟨ DerivationFailed | note, remaining_findings ⟩
```

The same gate that claim convergence runs before each review cycle. The validator (mechanical, no LLM) runs every steady-state and transition-checkable structural invariant from the Claim File Contract. For each actionable finding it dispatches a per-rule fix-recipe prompt to an LLM; the recipe operates on a constrained surface (Depends bullets, label-position tokens, citation links) and is forbidden by prompt contract from modifying semantic content (proofs, Axioms, Preconditions, Postconditions). Decisions are captured in structured form (`__decisions.json`) that the orchestrator validates before accepting the work.

The loop is bounded by MAX_ITER iterations (currently 3) plus a no-progress halt — if a round reduces no findings count, the gate halts. Findings the reviser declines (returns SKIP for) are tracked across iterations and not re-attempted. Acyclic-depends findings are propose-only — surfaced as warnings but not auto-fixed.

### 6.8 Termination

The algorithm terminates on ⟨ ClaimSetProduced ⟩ or ⟨ DerivationFailed ⟩. The validate-gate has a bounded structural-healing loop; this is not a convergence loop in the note-convergence or claim-convergence sense — it does not iterate against semantic findings, only against mechanical contract violations. ⟨ DerivationFailed ⟩ leaves the partial output in place with the unresolved findings list for diagnosis; downstream stages do not operate on a failed derivation.

### 6.9 Re-running on a prior derivation is destructive

Re-invoking the protocol on a note whose derivation has already produced a claim set will:
- Overwrite each claim body with the byte-aligned source projection (Phase 3), discarding any edits made by claim convergence
- Re-synthesize Formal Contracts (Phase 4) on the freshly-projected bodies
- Re-emit substrate links (idempotent at the classifier level; new `provenance.derivation` link emissions return the existing link's id)

This is consistent with B4 (source freezing): the source note is the historical record; the claim set is the current projection. Re-running discards convergence-loop output. Production choreography routes prose-change cases through claim convergence's own quality pass (which calls produce-contract on dirty claims), not through re-running derivation.

---

## 7 Composition

### Stage transition: discovery → claim derivation → claim convergence

Unlike consultation (which is a producer for note convergence — same artifact throughout), claim derivation is a stage transition. It changes the representation: one note → many per-claim file pairs. The artifact at the input (a note) is not the artifact at the output (a claim set). This is a [representation change](../patterns/representation-change.md) — and the boundary most vulnerable to [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md).

```
Module: Maturation
  Uses: NoteConvergence, NoteDecomposition, ClaimConvergence
  
  Transition: NoteConvergence → NoteDecomposition
    Precondition: ⟨ Converged | note ⟩ indicated by note convergence
    Artifact: frozen note (markdown + vocabulary + note-level dependencies)
  
  Transition: NoteDecomposition → ClaimConvergence
    Precondition: ⟨ ClaimSetProduced ⟩ indicated; Claim File Contract holds
    Artifact: per-claim file set carrying claim/contract/citation/decomposition links
```

The [maturation protocol](maturation-protocol.md) governs both transitions. It activates claim derivation after note convergence's predicate holds and activates claim convergence after decomposition's contract holds.

### Failure modes detected downstream

Violations of B1–B7 that escape the validator surface in claim convergence:

- B1 / B2 / B3 violations (semantic content drift between source and output) surface as `comment.revise` findings during cone or comprehensive review.
- B5 violations (structural contract drift) are caught by claim convergence's [validate-before-review](../patterns/validate-before-review.md) gate before each review cycle.
- Symbol-resolution violations (declared-symbols-resolve invariant) surface as cross-claim review findings traceable to the upstream decomposition decision.

### The T3 incident

The structural contract is non-obvious and load-bearing. The T3 incident — a sweep that ran sixteen cycles without converging because no contract specified what well-formed per-claim output meant — is the documented failure mode that motivates the contract. See [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md) for the trace.

---

## Related

- [Claim File Contract](../design-notes/claim-file-contract.md) — the structural contract this protocol's output must satisfy.
- [Claim Derivation](../claim-derivation.md) — narrative description of the derivation stage.
- [Note Convergence Protocol](note-convergence-protocol.md) — the upstream protocol whose converged output enters decomposition.
- [Claim Convergence Protocol](claim-convergence-protocol.md) — the downstream protocol that operates on decomposition's output.
- [Maturation Protocol](maturation-protocol.md) — composes claim derivation between note and claim convergence.
- [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md) — the failure mode the structural contract addresses. T3 incident trace.
- [Validate Before Review](../patterns/validate-before-review.md) — the operational pattern that consumes the structural contract downstream.
- [Representation Change](../patterns/representation-change.md) — claim derivation is the canonical instance.

## References

- C. Cachin, R. Guerraoui, L. Rodrigues. *Reliable and Secure Distributed Programming*. Springer, 2nd edition, 2011.