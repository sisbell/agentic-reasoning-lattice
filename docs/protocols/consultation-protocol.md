# Consultation Protocol

The protocol that produces an initial note from a campaign-bound inquiry. Two independent channels (theory and evidence) are consulted under enforced vocabulary separation; their outputs are synthesized into a structured note. The output enters [note convergence](note-convergence-protocol.md) for review/revise cycles.

One-shot — terminates on output production. The protocol runs once per inquiry. The narrative description of channels, asymmetry, and synthesis lives in [Two-Channel Architecture](../two-channel-architecture.md).

Following the modular formalism of Cachin (*Reliable and Secure Distributed Programming*).

---

## 1 Document model

### Document types

| Classifier | What the document is |
|---|---|
| `inquiry` | The input. A campaign-bound question with consultation parameters (channel question counts, out-of-scope hints). |
| `note` | The output. A synthesized reasoning document (also the classifier note convergence operates on). |

### Link types

| Type | Subtypes | Role |
|---|---|---|
| `inquiry` | (flat, one-sided) | Classifier: document is an inquiry |
| `provenance.synthesis` | (flat) | Records that consultation produced this note from this inquiry. From = inquiry, to = note. |

Sub-questions and raw channel answers are choreography concerns, not protocol primitives. They may be persisted (substrate documents) or transient (intermediate state) — the protocol is silent on this. The substrate-level provenance trail is the inquiry → `provenance.synthesis` → note edge.

---

## 2 Modules used

### 2.1 Substrate

The persistent, append-only link graph. See [Substrate Module](../modules/substrate-module.md). This protocol relies on SUB1 (permanence — for the `provenance.synthesis` provenance link) and SUB2 (query soundness). Consultation does not file or interact with retraction links; SUB4–SUB6 are not relied upon.

### 2.2 Channels

Each channel is a self-contained plugin (see [Two-Channel Architecture](../two-channel-architecture.md)) exposing a two-function interface:

- `generate_questions(inquiry, channel_context)` — decompose an inquiry into channel-appropriate sub-questions. The theory channel receives a vocabulary list as context; the evidence channel receives the corpus (channel asymmetry — see C5).
- `consult(sub_question)` — answer a sub-question from the channel's corpus.

**Properties relied upon.**

- CH1 (Channel grounding). A channel's outputs are derivable from its corpus. The channel reports explicitly when a question reaches beyond corpus scope.
- CH2 (Vocabulary closure). A channel's outputs contain only terms from its corpus and the campaign's bridge vocabulary. No leakage from the other channel.

### 2.3 Bridge vocabulary

A campaign-level dictionary of unified terms that both channels may use. Curated upfront, immutable per campaign. The narrow band of vocabulary that crosses the firewall.

---

## 3 Participants and events

### Decomposer (role, not component)

Question generation for each channel is performed by that channel's `generate_questions` function — the theory channel decomposes theory questions from its vocabulary list, the evidence channel decomposes evidence questions from its corpus. "The decomposer" is shorthand for this per-channel decomposition, not a centralized component. The two invocations are independent — one channel's invocation does not see the other's outputs. Question counts may be asymmetric (an inquiry with more to ask one channel asks more of that channel).

### Theory channel

Answers theory sub-questions from the theory corpus. Stays inside the corpus — does not invoke results or theories beyond what the corpus contains, and says so explicitly when a question reaches beyond the corpus's scope. Does not use evidence-channel terms.

### Evidence channel

Answers evidence sub-questions from the evidence corpus. Reports what the data shows — numerical values, units, conditions, citations. Does not theorize about why. Does not use theory-channel terms.

### Synthesizer

Reads both channels' answers and produces a structured note in the Dijkstra voice with dependency-mapped claims. Coins bridging vocabulary where no existing term fits. Records agreements (validations) and disagreements (new hypotheses or open questions). The synthesizer is the first place both channels' outputs appear together.

### Events

**Requests (input from above).**

- ⟨ Consult | inquiry, campaign ⟩ — initiate the protocol on this inquiry under this campaign's channel pairing and bridge vocabulary.

**Internal events** (visible to participants but not to the upper interface).

- ⟨ Decompose | inquiry, channel ⟩ — produce sub-questions for the channel.
- ⟨ Answer | sub_question, channel ⟩ — channel answers one of its sub-questions.
- ⟨ Synthesize | inquiry, theory_answers, evidence_answers ⟩ — produce a note from the answer sets.

**Indications (output upward).**

- ⟨ NoteProduced | inquiry, note ⟩ — the protocol has produced a note. The note carries the `note` classifier and a `provenance.synthesis` link from the inquiry.
- ⟨ ConsultationFailed | inquiry, reason ⟩ — the protocol could not produce a note (channel error, synthesizer failure). No note is created.

---

## 4 Termination

The protocol terminates on output production — no convergence predicate, no iteration. A single ⟨ Consult ⟩ request results in either:

- ⟨ NoteProduced | inquiry, note ⟩ — success. The note is in the substrate and a `provenance.synthesis` link records the provenance.
- ⟨ ConsultationFailed | inquiry, reason ⟩ — failure. No note is created; no `provenance.synthesis` link is filed.

Termination is structural: the protocol's state machine is decompose → consult → synthesize → indicate. There is no loop. Refinement happens downstream in note convergence.

---

## 5 Properties

### 5.1 Safety

**C1 (Vocabulary firewall).** Theory channel outputs contain no terms drawn from the evidence channel's corpus. Evidence channel outputs contain no terms drawn from the theory channel's vocabulary list. Enforced structurally — each channel's input context excludes the other's vocabulary by construction. The synthesizer is the first place both vocabularies appear together. (Relies on CH2.)

**C2 (Channel independence).** Neither channel sees the other's sub-questions or answers during decomposition or consultation. The decomposer's invocations for one channel do not include the other channel's outputs. Synthesis is the first place both channels' outputs meet.

**C3 (Channel discipline — theory).** The theory answerer's outputs are derivable from the theory corpus alone. It does not invoke results outside the corpus and explicitly says so when a question reaches beyond corpus scope. (Relies on CH1.)

**C4 (Channel discipline — evidence).** The evidence answerer's outputs report what the data shows — values, conditions, patterns — without theorizing about causes or invoking theoretical frameworks. The evidence channel describes what is there, not why it is there. Unlike C1 (structurally enforced through context absence), C4 is enforced through the channel's prompt and the corpus's own character — an evidence corpus of measurements and code naturally constrains answers to observations. This is a softer constraint than C1. Violations surface downstream as `comment.revise` findings in note convergence when the reviewer detects evidence claims that theorize. (Relies on CH1.)

**C5 (Channel asymmetry).** Theory generators receive a vocabulary list — the theoretical framework's own terms in the corpus's own language. Evidence generators receive the corpus itself (or a curated synthesis). This asymmetry is structural: theory space is conceptual and listable; evidence space is specific and must be seen. Violating the asymmetry (giving the evidence generator only a vocabulary list) produces generic retrieval questions instead of corpus-specific ones.

**C6 (Synthesis integrity).** Every fact present in either channel's output either appears in the synthesized note or is explicitly noted as a disagreement. The synthesizer does not fabricate facts not derivable from the channels' outputs. Where channels agree, the agreement is noted. Where they disagree, the disagreement is preserved as a finding, not resolved by the synthesizer's own judgment.

**C7 (Provenance recording).** On ⟨ NoteProduced | inquiry, note ⟩, the substrate contains a `provenance.synthesis` link from the inquiry to the note and a `note` classifier on the note document. (Relies on SUB1.)

### 5.2 Liveness

**CL1 (Termination).** If both channels are responsive (each ⟨ Answer ⟩ event eventually returns) and the synthesizer is active, then ⟨ Consult ⟩ eventually produces ⟨ NoteProduced ⟩ or ⟨ ConsultationFailed ⟩.

**CL2 (Completeness of consultation).** Every sub-question produced by the decomposer receives an answer from its channel. No question is silently dropped.

### 5.3 Quality boundary

Content quality targets, not graph properties. They require inspection of document content and are monitored by the choreography that operates the protocol.

**Voice discipline.** The synthesized note is in the Dijkstra voice — prose with embedded formalism, every statement justified where introduced. See [The Voice Principle](../principles/voice.md).

**Content balance.** Notes hold at roughly 90/10 prose-to-formal — higher prose ratio than claim files (70/30) because discovery is generative. See [The Coupling Principle](../principles/coupling.md).

**Vocabulary coinage.** Most of a note's invented vocabulary emerges at synthesis time — the synthesizer coins terms where the two channels' vocabularies don't overlap and no existing bridge term fits. The remaining vocabulary emerges during note convergence as review deepens the reasoning. The split has been observed but not precisely instrumented; tracking when terms first appear would require provenance across the consultation → note convergence boundary.

### 5.4 Deliberate non-guarantees

**No correctness guarantee.** Channels may report wrong facts (LLM hallucinations, corpus misreadings). The protocol guarantees the firewall, independence, discipline, and synthesis integrity — not the truth of what each channel says. Correctness pressure comes from note convergence (where violations surface as `comment.revise` findings) and ultimately from verification.

**No completeness guarantee.** A consultation may fail to surface relevant content present in the corpus. The protocol does not guarantee exhaustive extraction.

**No convergence.** The protocol runs once per inquiry. There is no predicate that becomes true. Refinement happens in note convergence.

**No idempotence.** Re-running the protocol on the same inquiry produces a different note. Channel responses are non-deterministic (LLM stochasticity); synthesis builds on whatever was answered. Production protocols don't promise the same output twice.

---

## 6 Algorithm: decompose → consult → synthesize

Implements: Consultation Protocol (§1–§5).
Uses: Substrate, Channel plugins (§2.2), Bridge vocabulary (§2.3).

The algorithm is one-shot — a single ⟨ Consult ⟩ invocation produces at most one note. Three phases: decompose, consult, synthesize. There is no convergence loop.

### 6.1 State

- *inquiry* — the input inquiry document.
- *campaign* — resolved from the inquiry (substrate `campaign` link or fallback to lattice default), binding (theory_channel, evidence_channel, bridge_vocabulary) to a target.
- *N_theory*, *N_evidence* — sub-question counts (per-channel, asymmetric allowed). Default sourced from each channel's descriptor; the inquiry may override.
- *answers* — accumulated answer set, filled in during phase 2.

### 6.2 Phase 1 — Decompose

```
upon ⟨ Consult | inquiry, campaign ⟩ do
  theory_qs    ← theory_channel.generate_questions(inquiry, vocab_list, N_theory)
  evidence_qs  ← evidence_channel.generate_questions(inquiry, corpus, N_evidence)
  questions    ← merge(theory_qs, evidence_qs)
  questions    ← filter_scope(questions, out_of_scope, upstream_covers)
```

Each channel's `generate_questions` runs independently. The theory channel sees the campaign's vocabulary list; the evidence channel sees the evidence corpus (channel asymmetry, C5). Neither channel's invocation sees the other's outputs (C2).

`filter_scope` is an orchestrator-level LLM pass (not a named participant) that discards questions falling outside the inquiry's declared `out_of_scope` or duplicating content already established by upstream ASNs (loaded from the inquiry's `depends:` foundation set). It judges semantic overlap, not string match. It runs after both channels have produced their questions and before any consultation begins.

### 6.3 Phase 2 — Consult

```
upon questions decomposed do
  for q in theory_qs in parallel:
    if answer file for q exists:
      load cached answer
    else:
      answer ← theory_channel.consult(q)
      save answer to disk
  for q in evidence_qs sequentially:
    if answer file for q exists:
      load cached answer
    else:
      answer ← evidence_channel.consult(q)
      save answer to disk
```

**Concurrency policy.** Theory consultations run in parallel — they don't use external tools and the channels are stateless. Evidence consultations run sequentially — each uses tools internally (KB queries, source exploration) and parallel tool use across calls would conflict with itself.

**Resume support.** If an answer file for a question already exists on disk, the cached answer is loaded and the consultation is skipped. This makes the algorithm partially idempotent under failure — a process killed mid-consultation resumes where it left off rather than restarting. (The protocol itself is not idempotent — see §5.4 — because re-running on the same inquiry without cached answers produces a different note.)

### 6.4 Phase 3 — Synthesize

```
upon all answers collected do
  combined ← build_combined_output(inquiry, questions, answers)
  note     ← invoke_synthesizer(
               combined,
               foundation_context,
               bridge_vocabulary,
               out_of_scope_hints
             )
  write_note(note)
  emit_synthesis_link(inquiry, note)         ; satisfies C7
  indicate ⟨ NoteProduced | inquiry, note ⟩
```

The synthesizer receives all answers at once. Its prompt context includes the campaign's bridge vocabulary, the inquiry's foundation context (formal statements from upstream ASNs declared in `depends:`), and the inquiry's out-of-scope hints. The `out_of_scope` field is the same data used in both phases — in §6.2 it filters questions that would duplicate upstream work or stray outside scope; in §6.4 it guides the synthesizer to avoid re-deriving what's already established and to flag boundary material as open questions rather than claimed results. Same source, different effects: filtering prevents wasted consultation, hinting shapes the note's epistemic boundaries. The synthesis prompt enforces the Dijkstra voice — prose with embedded formalism, every statement justified where introduced.

The note is written to the lattice's discovery directory. A `provenance.synthesis` link is filed in the substrate from the inquiry to the note (provenance, per C7).

### 6.5 Termination

The algorithm terminates when ⟨ NoteProduced ⟩ is indicated (success) or when any phase fails irrecoverably — channel error, synthesis failure, irrecoverable filesystem error — in which case ⟨ ConsultationFailed | inquiry, reason ⟩ is indicated and no note is created. Resume from a partial-failure state is supported via the disk-cached answer files (§6.3); restart from a fully failed state requires a fresh ⟨ Consult ⟩ invocation.

---

## 7 Composition

### Producer-consumer with note convergence

The consultation protocol is the upstream producer for the [note convergence protocol](note-convergence-protocol.md). The artifact — the note document — is the same throughout: consultation produces the initial draft; note convergence refines it through review/revise cycles. Both protocols operate on the same `note` classifier.

This is a producer-consumer relationship, not a stage transition. Stage transitions (discovery → claim derivation → claim convergence) change the representation. Consultation → note convergence does not change representation — both operate on the same note. They differ in shape (one-shot production vs. iterative convergence), not in artifact.

```
Module: Discovery
  Uses: Consultation, NoteConvergence
  
  Sequence: Consult → NoteProduced → NoteConvergence.Engage
    Consultation produces note
    Note convergence engages on the produced note
    Convergence indicates ⟨ Converged | note ⟩ when predicate holds
```

### Campaign binding

The ⟨ Consult ⟩ request includes the campaign, which binds the channel pairing and bridge vocabulary. These are campaign-level parameters — the [maturation protocol](maturation-protocol.md) passes them through from the campaign configuration. The consultation protocol does not choose its channels; it receives them.

### Within the maturation protocol

Discovery's stage protocol is note convergence; consultation is its upstream producer. The [maturation protocol](maturation-protocol.md) activates consultation when a new inquiry is added to a campaign and activates note convergence on the produced note.

### Failure modes detected downstream

Violations of C1–C6 frequently surface as findings during note convergence:

- Vocabulary firewall leaks → reviewer flags terms one channel shouldn't have used.
- Channel discipline violations → reviewer flags theory claims grounded in evidence not derivable from the theory corpus, or evidence claims that theorize.
- Synthesis integrity gaps → reviewer flags a claim attributed to one channel that is not derivable from that channel's outputs.

Note convergence is the downstream protocol that detects what consultation failed to enforce. This is one reason note convergence runs after consultation rather than instead of it — review pressure surfaces the violations that the production protocol's safety properties guard against.

---

## Related

- [Two-Channel Architecture](../two-channel-architecture.md) — narrative description of channels, vocabulary firewall, channel asymmetry, synthesis, channel plugin interface.
- [Note Convergence Protocol](note-convergence-protocol.md) — the downstream consumer. Refines the note this protocol produces.
- [Claim Derivation Module](../modules/claim-derivation-module.md) — the protocol that operates on the note after convergence, decomposing it into per-claim files.
- [Convergence Protocol](convergence-protocol.md) — the document-type-neutral module note convergence specializes (consultation does not specialize it; production protocols and convergence protocols share the substrate but not the predicate).
- [Maturation Protocol](maturation-protocol.md) — composes consultation and note convergence within discovery.
- [The Voice Principle](../principles/voice.md) — synthesizer's output discipline.
- [The Coupling Principle](../principles/coupling.md) — 90/10 content balance at note scale.

## References

- C. Cachin, R. Guerraoui, L. Rodrigues. *Reliable and Secure Distributed Programming*. Springer, 2nd edition, 2011.