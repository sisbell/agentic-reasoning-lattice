# Note Decomposition Protocol

The protocol that decomposes a converged note into per-claim file pairs. Takes a note (the output of [consultation](consultation-protocol.md) refined through [note convergence](note-convergence-protocol.md)) and produces a structured set of YAML metadata + Markdown body pairs, one per claim, conforming to the [Claim File Contract](../design-notes/claim-file-contract.md). The output enters [claim convergence](claim-convergence-protocol.md) for review/revise cycles.

One-shot — terminates when the structural contract holds on the output. The narrative description of the decomposition stage lives in [Note Decomposition](../note-decomposition.md).

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
| `decomposition` | (flat) | Records that decomposition produced this claim from this note. From = note, to = claim. Provenance trail from the source document to each output pair. |

The `claim`, `citation`, and `contract` link types are inherited from the [claim convergence protocol](claim-convergence-protocol.md) — note decomposition is the protocol that creates them. The `decomposition` link is this protocol's own provenance primitive (analog of consultation's `synthesis` link).

Note decomposition does not file `retraction` links. Retraction is a [claim convergence](claim-convergence-protocol.md#retraction-and-proof-evolution) concern — a revisor responding to proof evolution that removes a use-site files a retraction during convergence cycles. Decomposition produces a fresh claim set from a converged note; there are no stale citations to retract at this stage.

---

## 2 Modules used

### 2.1 Substrate

Persistent, append-only graph of documents and typed links.

**Properties relied upon.**

- SUB1 (Permanence). No link is ever removed once created.
- SUB2 (Query soundness). FindLinks returns exactly the links satisfying the constraint conjunction.

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

### Disassembler

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
- ⟨ Disassemble | enriched_sections ⟩ — write per-claim file pairs.
- ⟨ Validate | claim_pairs ⟩ — run structural checks.

**Indications (output upward).**

- ⟨ ClaimSetProduced | note, claims ⟩ — the protocol has produced a valid claim set. Each claim carries the `claim` classifier, a `contract.<kind>` link reflecting its type, `citation` links for its declared dependencies, and a `decomposition` link from the source note.
- ⟨ DecompositionFailed | note, violations ⟩ — the validator reported violations that could not be auto-resolved. No claim set is produced.

---

## 4 Termination

The protocol terminates on output production — no convergence predicate, no iteration. A single ⟨ Decompose ⟩ request results in either:

- ⟨ ClaimSetProduced | note, claims ⟩ — success. The Claim File Contract's structural invariants hold on the output. Substrate links are filed per the document model (§1).
- ⟨ DecompositionFailed | note, violations ⟩ — failure. The validator reported invariant violations the protocol could not auto-resolve. The output is left in place but does not enter claim convergence.

Termination is structural: the protocol's state machine is split → enrich → disassemble → validate → indicate. There is no loop.

---

## 5 Properties

### 5.1 Safety

**B1 (Source coverage).** Every claim in the source note produces exactly one output file pair. No source claim is dropped; no source claim is duplicated across multiple pairs.

**B2 (No fabrication).** Every output file pair corresponds to a claim in the source note. Note decomposition does not invent claims that the source did not contain.

**B3 (Content preservation).** Each source claim's narrative, proof, and formal contract text appears in its corresponding file pair. Textual presence is mechanically checkable (the validator can detect empty bodies or missing contract sections). Semantic fidelity — whether the per-claim form preserves what the narrative actually meant — is not mechanically checkable and surfaces as `comment.revise` findings in claim convergence. B3 guarantees the text arrived; the quality boundary (§5.3) and downstream review guarantee it arrived intact.

**B4 (Source freezing).** The source note is frozen at the moment decomposition begins. It becomes the record of discovery, not a living document. Modifications to the note after decomposition has started do not propagate to the claim file set. The note and the claim files are separate artifacts from this point forward. This connects to the [maturation protocol](maturation-protocol.md)'s hard reset — unfreezing is a cascading structural operation.

**B5 (Structural contract).** On ⟨ ClaimSetProduced ⟩, every steady-state invariant of the [Claim File Contract](../design-notes/claim-file-contract.md) holds on the output: file-pair completeness, filename-matches-label, declaration-matches-label, YAML well-formed, depends agreement, references resolve, declared symbols resolve, acyclic dependency graph, body uniqueness. (Relies on SV1, SV2.)

**B6 (Acyclicity).** The `citation` subgraph induced by the output's `depends:` lists is a directed acyclic graph. Decomposition refuses to emit ⟨ ClaimSetProduced ⟩ if it would introduce a cycle. (Subsumed by B5 but called out separately because it is the property most often violated by enricher errors.)

**B7 (Provenance recording).** On ⟨ ClaimSetProduced | note, claims ⟩, the substrate contains, for each claim in the output: a `claim` classifier on the claim document, a `contract.<kind>` link reflecting its type, `citation` links for its declared dependencies, and a `decomposition` link from the source note to the claim. (Relies on SUB1.)

### 5.2 Liveness

**BL1 (Termination).** If the LLM phases (decompose, enrich) complete and the disassembler runs without I/O failure, then the validator either reports success — yielding ⟨ ClaimSetProduced ⟩ — or reports violations — yielding ⟨ DecompositionFailed ⟩. The protocol does not loop indefinitely.

**BL2 (Completeness of decomposition).** Every non-structural section of the source note is processed by the decomposer. No section is silently skipped.

### 5.3 Quality boundary

These are content quality targets, not graph properties. The validator does not enforce them; review enforces them. They surface as semantic findings in claim convergence rather than as decomposition errors.

**Summary matches body.** Each claim's YAML `summary` field describes what the markdown body claims. Not a restatement of the formal contract; not stale relative to the body.

**Exterior matches interior.** Each claim's stated postconditions are delivered by its proof. Its preconditions are sufficient for the proof and do not exceed what callers must supply.

**Symbol usage matches declaration.** Symbols declared with a given signature or meaning are used consistently with that declaration throughout the proof.

These three semantic invariants are documented in the [Claim File Contract](../design-notes/claim-file-contract.md) as review-enforced.

### 5.4 Deliberate non-guarantees

**No semantic correctness.** Note decomposition guarantees structural form (B1–B7) but not the semantic correctness of any claim. A claim with a wrong proof, an over-stated postcondition, or an ungrounded operator passes decomposition if its structural form is valid. Semantic pressure comes from claim convergence.

**No semantic preservation beyond text.** B3 (content preservation) is mechanical — the words appear. Whether the per-claim form preserves what the narrative actually meant is a semantic question that surfaces in claim convergence, not decomposition.

**No idempotence.** Re-running decomposition on the same note produces a different claim set (LLM stochasticity in decompose and enrich). Production protocols don't promise the same output twice.

**No iteration.** If the produced claim files are semantically inadequate (wrong types, missing dependencies, unclear proofs), the protocol does not re-run decomposition. Refinement is claim convergence's job.

---

## 6 Algorithm: split → enrich → disassemble → validate

Implements: Note Decomposition Protocol (§1–§5).
Uses: Substrate (§2.1), Structural Validator (§2.2), Decomposition prompts (§2.3).

The algorithm is one-shot — a single ⟨ Decompose ⟩ invocation produces at most one claim set. Four phases: split, enrich, disassemble, validate. There is no convergence loop.

### 6.1 State

- *note* — the input note document.
- *sections* — intermediate result: list of (header, content) pairs after mechanical split.
- *section_yamls* — intermediate result: per-section YAML analyses listing each section's claims.
- *claim_pairs* — output: per-claim `{label}.yaml` + `{label}.md` files on disk.

### 6.2 Phase 1 — Split

```
upon ⟨ Decompose | note ⟩ do
  sections ← split_at_headers(note)            ; deterministic
  section_yamls ← []
  for (header, content) in sections in parallel:
    if is_structural(header):                  ; PREAMBLE, Claims Introduced, etc.
      continue
    yaml_analysis ← invoke_llm(decompose_prompt, content)
    section_yamls.append((header, yaml_analysis))
```

Mechanical section split is deterministic — splits the note's markdown at `##` headers. Per-section LLM analysis runs in parallel across sections. Each LLM call produces structured YAML listing the section's claims (label, name, body, formal contract). The `is_structural` predicate is a closed list defined in the decomposer implementation — currently `PREAMBLE`, `Claims Introduced`, `Open Questions`, and `Worked example`. Sections matching these headers contain metadata, indexes, or illustrative content rather than derivable claims. The list extends if new structural section conventions are adopted in the note format.

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

### 6.4 Phase 3 — Disassemble

```
upon enrichment complete do
  for each claim in flatten(section_yamls):
    write_yaml({label}.yaml, claim.metadata)
    write_md({label}.md, claim.body + claim.formal_contract)
```

Deterministic write phase — no LLM. One `{label}.yaml` (metadata) + `{label}.md` (body + formal contract) pair per declared claim. The YAML carries `label`, `name`, `type`, `summary`, `depends`, and (where present) `vocabulary`. The markdown carries the claim's narrative body and its formal contract section.

### 6.5 Phase 4 — Validate

```
upon disassembly complete do
  violations ← validator.check(claim_pairs)
  if violations is empty:
    emit_substrate_links(note, claim_pairs)    ; B7
    indicate ⟨ ClaimSetProduced | note, claim_pairs ⟩
  else:
    apply_fix_recipes(violations, claim_pairs)
    violations ← validator.check(claim_pairs)
    if violations is empty:
      emit_substrate_links(note, claim_pairs)
      indicate ⟨ ClaimSetProduced | note, claim_pairs ⟩
    else:
      indicate ⟨ DecompositionFailed | note, violations ⟩
```

The validator runs every steady-state and transition-checkable invariant from the Claim File Contract. For violations the protocol can auto-resolve (e.g., filename-doesn't-match-label → rename file), per-invariant fix recipes apply mechanically and the validator re-runs. If violations remain after the fix pass, the protocol fails with a violation report.

### 6.6 Termination

The algorithm terminates on ⟨ ClaimSetProduced ⟩ or ⟨ DecompositionFailed ⟩. There is no convergence loop — the validator runs at most twice (initial check + post-fix check). If a violation cannot be auto-resolved, the protocol fails rather than looping.

### 6.7 Known gap

The current implementation does not yet emit the substrate links specified in B7. The `claim` classifier, `contract.<kind>` classifier, `citation` links, and `decomposition` provenance link are filed by `populate-store.py` as a bootstrap mechanism, not by decomposition itself. B7 is therefore aspirational pending substrate emission inside the decomposition pipeline.

---

## 7 Composition

### Stage transition: discovery → note decomposition → claim convergence

Unlike consultation (which is a producer for note convergence — same artifact throughout), note decomposition is a stage transition. It changes the representation: one note → many per-claim file pairs. The artifact at the input (a note) is not the artifact at the output (a claim set). This is a [representation change](../patterns/representation-change.md) — and the boundary most vulnerable to [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md).

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

The [maturation protocol](maturation-protocol.md) governs both transitions. It activates note decomposition after note convergence's predicate holds and activates claim convergence after decomposition's contract holds.

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
- [Note Decomposition](../note-decomposition.md) — narrative description of the decomposition stage.
- [Note Convergence Protocol](note-convergence-protocol.md) — the upstream protocol whose converged output enters decomposition.
- [Claim Convergence Protocol](claim-convergence-protocol.md) — the downstream protocol that operates on decomposition's output.
- [Maturation Protocol](maturation-protocol.md) — composes note decomposition between note and claim convergence.
- [Uncontracted Representation Change](../equilibrium/uncontracted-representation-change.md) — the failure mode the structural contract addresses. T3 incident trace.
- [Validate Before Review](../patterns/validate-before-review.md) — the operational pattern that consumes the structural contract downstream.
- [Representation Change](../patterns/representation-change.md) — note decomposition is the canonical instance.

## References

- C. Cachin, R. Guerraoui, L. Rodrigues. *Reliable and Secure Distributed Programming*. Springer, 2nd edition, 2011.