# Claim Derivation Module

A transformation module that derives per-claim files from a converged note. Each claim becomes a body markdown file with substrate-managed sidecars (label, name, description, optionally signature) and substrate links classifying the body and recording its dependencies and provenance, conforming to the [Claim File Contract](../design-notes/claim-file-contract.md).

The input is a note refined through [consultation](../protocols/consultation-protocol.md) and [note convergence](../protocols/note-convergence-protocol.md); the output enters [claim convergence](../protocols/claim-convergence-protocol.md) for review/revise cycles.

One-shot — terminates when the structural contract holds on the output. The narrative description of the derivation stage lives in [Claim Derivation](../claim-derivation.md).

This module uses the modular formalism of Cachin (*Reliable and Secure Distributed Programming*) for its specification — events, properties, composition — but it is not a protocol in the interaction sense. Protocols govern ongoing interaction between participants with predicates across that interaction (the convergence protocols, the consultation protocol). This module provides a single transformation: note in, claim set out, postcondition verified. It is a refinement step between two protocols — an adapter that takes note convergence's output and produces claim convergence's input, with the [Claim File Contract](../design-notes/claim-file-contract.md) as the interface contract.

---

## 1 Document model

### Document types

| Classifier | What the document is |
|---|---|
| `note` | The input. A converged reasoning document containing claims interleaved in narrative prose. (Same classifier as note convergence input/output.) |
| `claim` | The output body. A per-claim markdown file `<label>.md` carrying the claim's prose, proof, and Formal Contract section. (Also the classifier claim convergence operates on.) |
| `label` / `name` / `description` / `signature` | Substrate-owned attribute classifiers. Mark the sidecar documents (`<label>.label.md`, `<label>.name.md`, `<label>.description.md`, optional `<label>.signature.md`) that carry the claim's substrate-managed attributes. |

### Link types

| Type | Subtypes | Role |
|---|---|---|
| `claim` | (flat, one-sided) | Classifier: document is a claim. `to_set = [body_md]`. Filed by the module's transclude phase from each enriched section claim. |
| `contract` | `axiom`, `definition`, `theorem`, `corollary`, `lemma`, `consequence`, `design-requirement` | Classifier: claim has a formal contract of this kind. `to_set = [body_md]`. Filed by transclude from the enricher's type classification. |
| `citation` | (flat) | Claim depends on claim. `from_set = [body_md], to_set = [dep_body_md]`. Filed by transclude from the enricher's dependency extraction. |
| `label` / `name` / `description` / `signature` | (flat) | Substrate-owned attribute links pointing each claim body at its sibling sidecar. `from_set = [body_md], to_set = [<stem>.<kind>.md]`. Filed by transclude. `signature` is conditional — present only when the claim introduces non-logical symbols (per [Claim File Contract](../design-notes/claim-file-contract.md) invariant #1: a missing signature sidecar for a claim that introduces no symbols is not a violation; an orphan sidecar without a matching body is). |
| `provenance` | `derivation` | Records that derivation produced this claim from this note. `from_set = [note_md], to_set = [body_md]`. Audit trail from source to output. Sibling of consultation's `provenance.synthesis` and maturation's `provenance.{extract,absorb,reset}`. |

The `claim`, `citation`, `contract`, and the substrate attribute link types are reused across protocols — claim derivation is the module that creates them for each derived claim. The `provenance.derivation` link is this module's own provenance primitive (analog of consultation's `provenance.synthesis`).

---

## 2 Modules used

### 2.1 Substrate

The persistent, append-only link graph. See [Substrate Module](substrate-module.md). This module relies on SUB1 (permanence — for the `claim`, `contract`, `citation`, and `provenance.derivation` links it emits) and SUB2 (query soundness). Claim derivation does not file or interact with retraction links; SUB4–SUB6 are not relied upon.

### 2.2 Structural validator

A mechanical checker (no LLM) that evaluates the per-claim file sets against the [Claim File Contract](../design-notes/claim-file-contract.md). Used by this module's final phase and re-used by claim convergence's [validate-before-review](../patterns/validate-before-review.md) gate.

The validator's declared-symbols-resolve check (Claim File Contract invariant #7) reads two substrate-resident inputs beyond the per-claim files themselves: the lattice's notation document (the always-in-scope set of language-provided symbols, classified by a `notation` link) and the union of all `signature` sidecars (each owning claim's introduced symbols). These are substrate state, not module parameters — the validator queries them at check time.

**Properties relied upon.**

- SV1 (Completeness). Every violation of a structural invariant is reported.
- SV2 (Soundness). Every reported violation is a genuine violation.
- SV3 (Determinism). Given the same input, the validator produces the same output. No LLM, no judgment.

### 2.3 Decomposition prompts

Per-phase LLM prompts that drive section analysis, type classification, dependency extraction, and signature extraction. The prompts enforce structured output (YAML conforming to a schema, written to `_workspace/claim-derivation/<asn>/sections/`) so downstream phases can read them mechanically without natural-language parsing. The intermediate section YAMLs are workspace artifacts only — the module's output is the substrate-classified claim documents and sidecars (§1), not these YAMLs.

---

## 3 Participants and events

### Decomposer

Splits the note mechanically at `##` section headers, then invokes per-section LLM calls that produce structured YAML capturing each section's claims (label, name, body, formal contract). The mechanical split is deterministic; the per-section LLM call is parallel across sections. Skips structural sections (e.g., `PREAMBLE`, `Claims Introduced`, `Open Questions`) that contain no derivable claims.

### Enricher

Reads the section YAMLs from decomposition. Per-claim, runs three independent LLM passes — type classification (axiom/definition/theorem/...), dependency extraction (which other claims this one cites), and signature extraction (which non-logical symbols this claim introduces). Passes are parallel within a claim and across claims. Updates the section YAMLs in place.

### Transcluder

Reads the enriched section YAMLs and projects each claim into the substrate. For each claim the transcluder writes the body markdown (`<label>.md`) — a verbatim byte-substring of the source note's region — plus the substrate-managed sidecars (`<label>.label.md`, `<label>.name.md`, `<label>.description.md`, optionally `<label>.signature.md`), and emits the `claim` and `contract.<kind>` classifiers, the `label` / `name` / `description` / `signature` attribute links to the sidecars, the `citation` links for declared dependencies, and the `provenance.derivation` link from the source note. Deterministic — no LLM.

### Validator

Mechanical structural checker. Reads the per-claim file sets and evaluates them against the [Claim File Contract](../design-notes/claim-file-contract.md)'s structural invariants. Emits a violation report or signals validation success.

### Fix recipe agent

Resolves structural violations reported by the validator. One violation, one fix. Per-invariant recipes constrain each fix to one violation class with a specific resolution strategy. The recipes are documented in [Validate Before Review](../patterns/validate-before-review.md) — each invariant in the [Claim File Contract](../design-notes/claim-file-contract.md) has one corresponding recipe in the validate-before-review pattern's recipe set. Runs after the validator; the validator re-checks after fixes.

### Events

**Requests (input from above).**

- ⟨ Derive | note ⟩ — initiate the module on this note.

**Internal events** (visible to participants but not to the upper interface).

- ⟨ SplitSections | note ⟩ — split the note into section analyses.
- ⟨ Enrich | section_yamls ⟩ — augment each claim with type, dependencies, signature.
- ⟨ Transclude | enriched_sections ⟩ — write per-claim file sets.
- ⟨ Validate | claim_pairs ⟩ — run structural checks.

**Indications (output upward).**

- ⟨ ClaimSetProduced | note, claims ⟩ — the module has produced a valid claim set. Each claim's body markdown carries the `claim` classifier, a `contract.<kind>` link reflecting its type, `label` / `name` / `description` attribute links to its sidecars (and `signature` if applicable), `citation` links for its declared dependencies, and a `provenance.derivation` link from the source note.
- ⟨ DerivationFailed | note, violations ⟩ — the validator reported violations that could not be auto-resolved. No claim set is produced.

---

## 4 Termination

The module terminates on output production — no convergence predicate, no iteration. A single ⟨ Derive ⟩ request results in either:

- ⟨ ClaimSetProduced | note, claims ⟩ — success. The Claim File Contract's structural invariants hold on the output. Substrate links are filed per the document model (§1).
- ⟨ DerivationFailed | note, violations ⟩ — failure. The validator reported invariant violations the module could not auto-resolve. The output is left in place but does not enter claim convergence.

Termination is structural: the module's state machine is split → enrich → transclude → validate → indicate. There is no convergence loop. The validate-gate (§6.7) has a bounded structural-healing loop, but this iterates against mechanical contract violations only — it does not iterate against semantic findings and is not a convergence predicate in the protocol sense.

---

## 5 Properties

The properties are postconditions on the module's output — "when this transformation finishes, these things hold." This differs from the convergence protocols' properties, which are invariants across ongoing interaction. The difference reflects the module's nature: it provides a single transformation, not an ongoing review/revise process.

### 5.1 Safety (output postconditions)

**B1 (Source coverage).** Every claim in the source note produces exactly one output file set. No source claim is dropped; no source claim is duplicated across multiple file sets.

**B2 (No fabrication).** Every output file set corresponds to a claim in the source note. Claim derivation does not invent claims that the source did not contain.

**B3 (Content preservation).** Each source claim's narrative, proof, and formal contract text appears in its corresponding file set. Textual presence is mechanically checkable (the validator can detect empty bodies or missing contract sections). Semantic fidelity — whether the per-claim form preserves what the narrative actually meant — is not mechanically checkable and surfaces as `comment.revise` findings in claim convergence. B3 guarantees the text arrived; the quality boundary (§5.3) and downstream review guarantee it arrived intact.

**B4 (Source freezing).** The source note is frozen at the moment derivation begins. It becomes the record of discovery, not a living document. Modifications to the note after derivation has started do not propagate to the claim file set. The note and the claim files are separate artifacts from this point forward. This connects to the [maturation protocol](../protocols/maturation-protocol.md)'s hard reset — unfreezing is a cascading structural operation.

**B5 (Structural contract).** On ⟨ ClaimSetProduced ⟩, every steady-state invariant of the [Claim File Contract](../design-notes/claim-file-contract.md) holds on the output: file-set completeness (body + required sidecars), declaration matches label, sidecar content well-formed, substrate classification complete (`claim`, `contract.<kind>`, `label`, `name`, `description`, optional `signature` links), depends agreement, references resolve, declared symbols resolve, acyclic dependency graph, body uniqueness. (Relies on SV1, SV2.)

**B6 (Acyclicity).** The `citation` subgraph induced by the output's `depends:` lists is a directed acyclic graph. Derivation refuses to emit ⟨ ClaimSetProduced ⟩ if it would introduce a cycle. (Subsumed by B5 but called out separately because cycles are detected by a distinct check from the rest of B5.)

**B7 (Provenance recording).** On ⟨ ClaimSetProduced | note, claims ⟩, the substrate contains, for each claim in the output: a `claim` classifier on the claim's body markdown, a `contract.<kind>` link reflecting its type, `label` / `name` / `description` attribute links to its sidecars (and `signature` if applicable), `citation` links for its declared dependencies, and a `provenance.derivation` link from the source note to the body. (Relies on SUB1.)

### 5.2 Liveness (termination guarantees)

**BL1 (Termination).** If the LLM phases (split, enrich) complete and the transcluder runs without I/O failure, then the validator either reports success — yielding ⟨ ClaimSetProduced ⟩ — or reports violations — yielding ⟨ DerivationFailed ⟩. The module does not loop indefinitely.

**BL2 (Completeness of derivation).** Every non-structural section of the source note is processed by the decomposer. No section is silently skipped.

### 5.3 Quality boundary

These are review-enforced. The validator does not check them; claim convergence's review/revise cycle does. They surface as semantic findings, not derivation errors.

**Description matches body.** Each claim's description sidecar describes what the markdown body claims. Not a restatement of the formal contract; not stale relative to the body.

**Exterior matches interior.** Each claim's stated postconditions are delivered by its proof. Its preconditions are sufficient for the proof and do not exceed what callers must supply.

**Symbol usage matches declaration.** Symbols declared in a claim's signature with a given meaning are used consistently with that declaration throughout the proof.

These three semantic invariants are documented in the [Claim File Contract](../design-notes/claim-file-contract.md) as review-enforced.

### 5.4 Deliberate non-guarantees

**No semantic correctness.** Claim derivation guarantees structural form (B1–B7) but not the semantic correctness of any claim. A claim with a wrong proof, an over-stated postcondition, or an ungrounded operator passes derivation if its structural form is valid. Semantic pressure comes from claim convergence.

**No semantic preservation beyond text.** B3 (content preservation) is mechanical — the words appear. Whether the per-claim form preserves what the narrative actually meant is a semantic question that surfaces in claim convergence, not derivation.

**No idempotence.** Re-running derivation on the same note produces a different claim set (LLM stochasticity in split and enrich). Production modules don't promise the same output twice.

**No iteration.** If the produced claim files are semantically inadequate (wrong types, missing dependencies, unclear proofs), the module does not re-run derivation. Refinement is claim convergence's job.

**No in-place refinement.** Re-invoking the module on a note whose derivation has already produced a claim set is destructive: each claim body is overwritten with the byte-aligned source projection (Phase 3), discarding any edits made by claim convergence; Formal Contracts are re-synthesized (Phase 4) on the freshly-projected bodies; substrate links are re-emitted (idempotent at the classifier level — `provenance.derivation` re-emission returns the existing link's id). This is consistent with B4 (source freezing): the source note is the historical record; the claim set is the current projection. Production choreography routes prose-change cases through claim convergence's own quality pass — which reuses this module's `produce_contract` on dirty claims (see §6.6) — not through re-running derivation.

---

## 6 Algorithm: split → enrich → transclude → validate-transclude → produce-contract → validate-gate

Implements: Claim Derivation Module (§1–§5).
Uses: Substrate (§2.1), Structural Validator (§2.2), Decomposition prompts (§2.3).

Six phases. The first three are sequential one-shots. The fourth (validate-transclude) is a quick mechanical substring check at the transclude exit boundary. The fifth (produce-contract) iterates per-claim with bounded retries internal to that phase. The sixth (validate-gate) is a bounded structural-only fix loop that terminates on contract satisfaction or maximum-iterations. The module does not run review/revise on semantic content — that is claim convergence's role.

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

Mechanical section split is deterministic — splits the note's markdown at `##` headers. Per-section LLM analysis runs in parallel across sections. Each LLM call produces structured YAML listing the section's claims (label, name, body extract). The `is_structural` predicate is a closed list defined in the decomposer implementation — currently `PREAMBLE`, `Claims Introduced`, `Open Questions`, and `Worked example`. Sections matching these headers contain metadata, indexes, or illustrative content rather than derivable claims. (Worked examples *demonstrate* claims declared elsewhere in the note — their prose contains symbols and reasoning, but no novel claim declarations to extract.)

### 6.3 Phase 2 — Enrich

```
upon section_yamls produced do
  for each claim in flatten(section_yamls) in parallel:
    type       ← invoke_llm(type_prompt, claim)
    depends    ← invoke_llm(deps_prompt, claim, neighbors)
    signature  ← invoke_llm(signature_prompt, claim)
    update_yaml(claim, type, depends, signature)
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
    write_md(<claim_dir>/<label>.description.md, description)
    if claim.signature is non-empty:
      write_md(<claim_dir>/<label>.signature.md, render_bullets(signature))
    emit_link(claim, body_md)                          ; classifier
    emit_link(contract.<kind>, body_md)                ; from type
    emit_link(label, body_md → label_sidecar)          ; attribute
    emit_link(name, body_md → name_sidecar)            ; attribute
    emit_link(description, body_md → description_sidecar)
    if signature sidecar written:
      emit_link(signature, body_md → signature_sidecar)
    for dep in claim.depends:
      emit_link(citation, body_md → dep_md)
  for each emitted claim:
    emit_link(provenance.derivation, note → body_md)
  relocate_structural_sections(_workspace/.../structural/)
```

The body markdown is a verbatim byte-substring of the source note's region, resolved via the `find_in_source` helper (exact match, then whitespace-normalized). Strict by design — fuzzy matching is silent acceptance of unexplained drift, so the resolver fails loud on no-match and the failed claim is reported rather than written. The description sidecar is emitted from the section YAML's prose summary; the signature sidecar is emitted only when the enricher's signature pass produced non-empty content (the claim introduces non-logical symbols).

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

Mechanical substring check, no LLM. Confirms each claim body is a byte-substring of its source note. Produce-contract intentionally diverges from this property in the next phase by appending Formal Contract sections; the check fires here so any earlier drift surfaces before that boundary rather than propagating silently. See Claim File Contract invariant 12 for the property's full statement and checkability window.

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

Per-claim LLM rewrite that synthesizes the Formal Contract section in each claim's body markdown. Initial synthesis is the module's responsibility because the Claim File Contract's steady-state structural invariants (depends agreement, references resolve, declared symbols resolve) presuppose Formal Contract presence; claim convergence operates on already-contract-bearing claims.

The `produce_contract` function lives in this module's library (`lib/claim_derivation/produce_contract.py`) and is reused — same code, same prompts — by claim convergence's quality-pass orchestrator when prose changes during convergence dirty an existing contract. Initial synthesis here, regeneration there; one implementation, two callers. The boundary is the caller's intent (first-time vs. dirty-claim refresh), not separate code paths.

The rewrite is bounded internally to three cycles per claim and gated by a review-rewrite prompt that checks for damage to Axioms, Preconditions, Postconditions, and other formal fields. Hash-based dirty detection skips claims whose prose is unchanged since the last successful rewrite, so re-running the module on a previously-derived ASN is incremental.

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

The algorithm terminates on ⟨ ClaimSetProduced ⟩ or ⟨ DerivationFailed ⟩. The validate-gate has a bounded structural-healing loop; this is not a convergence loop in the note-convergence or claim-convergence sense — it does not iterate against semantic findings, only against mechanical contract violations. ⟨ DerivationFailed ⟩ leaves the partial output in place with the unresolved findings list for diagnosis; downstream protocols do not operate on a failed derivation.

---

## 7 Composition

### Stage transition: discovery → claim derivation → claim convergence

Unlike consultation (which is a producer for note convergence — same artifact throughout), claim derivation is a stage transition. It changes the representation: one note → many per-claim file sets. The artifact at the input (a note) is not the artifact at the output (a claim set). This is a [representation change](../patterns/representation-change.md) — and the boundary most vulnerable to [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md).

```
Module: Maturation
  Uses: NoteConvergence, ClaimDerivation, ClaimConvergence

  Transition: NoteConvergence → ClaimDerivation
    Precondition: ⟨ Converged | note ⟩ indicated by note convergence
    Artifact: frozen note (markdown body, substrate-classified)

  Transition: ClaimDerivation → ClaimConvergence
    Precondition: ⟨ ClaimSetProduced ⟩ indicated; Claim File Contract holds
    Artifact: per-claim body markdown + sidecars, plus the substrate
              links (claim, contract.<kind>, label, name, description,
              signature, citation, provenance.derivation)
```

The [maturation protocol](../protocols/maturation-protocol.md) governs both transitions. It activates claim derivation after note convergence's predicate holds and activates claim convergence after derivation's contract holds.

### Why this is a module, not a protocol

The claim derivation module sits between two protocols in the maturation protocol's composition. Both protocols (note convergence, claim convergence) govern ongoing interaction between participants — reviewer and reviser interact through the substrate over multiple cycles, with a convergence predicate governing completion. Claim derivation does not have this shape:

- Its participants do not interact — they run in sequence (split → enrich → transclude → validate).
- It has no convergence predicate — it has a postcondition (the Claim File Contract holds).
- It does not iterate against semantic findings — the validate-gate iterates against structural violations only, bounded and non-semantic.

It is a refinement step in the Abrial sense: precondition (note converged), transformation (derive claims), postcondition (structural contract holds). It is an adapter in the Cachin sense: it takes one module's output and produces another module's input, with properties ensuring the transformation preserves what matters. The Cachin formalism (events, properties, composition) applies to modules and protocols alike — the difference is in the interaction pattern, not in the specification structure.

### Failure modes detected downstream

Violations of B1–B7 that escape the validator surface in claim convergence:

- B1 / B2 / B3 violations (semantic content drift between source and output) surface as `comment.revise` findings during cone or comprehensive review.
- B5 violations (structural contract drift) are caught by claim convergence's [validate-before-review](../patterns/validate-before-review.md) gate before each review cycle.
- Symbol-resolution violations (declared-symbols-resolve invariant) surface as cross-claim review findings traceable to the upstream derivation decision.

The trace of the failure mode this contract addresses is documented in [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md).

---

## Related

- [Claim File Contract](../design-notes/claim-file-contract.md) — the structural contract this module's output must satisfy.
- [Claim Derivation](../claim-derivation.md) — narrative description of the derivation stage.
- [Note Convergence Protocol](../protocols/note-convergence-protocol.md) — the upstream protocol whose converged output enters derivation.
- [Claim Convergence Protocol](../protocols/claim-convergence-protocol.md) — the downstream protocol that operates on derivation's output.
- [Maturation Protocol](../protocols/maturation-protocol.md) — composes claim derivation between note and claim convergence.
- [Substrate Module](substrate-module.md) — the persistent link graph. Derivation writes claim/contract/citation/provenance.derivation links to it.
- [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md) — the failure mode the structural contract addresses. T3 incident trace.
- [Validate Before Review](../patterns/validate-before-review.md) — the operational pattern that consumes the structural contract downstream.
- [Representation Change](../patterns/representation-change.md) — claim derivation is the canonical instance.

## References

- C. Cachin, R. Guerraoui, L. Rodrigues. *Reliable and Secure Distributed Programming*. Springer, 2nd edition, 2011.
- J.-R. Abrial. *Modeling in Event-B: System and Software Engineering*. Cambridge University Press, 2010.