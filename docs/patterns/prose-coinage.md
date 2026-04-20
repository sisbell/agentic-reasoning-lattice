# Prose Coinage

## Pattern

An agent coins a new prose word for a concept the reasoning will refer to from that point forward. The concept is one no existing vocabulary precisely captures; the coined word gives it a handle. The word enters the note's narrative and becomes available for subsequent claims, proofs, and downstream note consumption.

Each coinage is a hypothesis — a structural claim about the domain proposing that the named concept exists and has the claims the reasoning requires of it. Coinage is how the system seeds hypothesis space.

"Action point," "divergence," "displacement," "zero-padded-equal," "subspace" — each was coined at a specific moment when synthesis needed a word for a concept that had no precise term in either channel's source vocabulary.

## Forces

- **Two channels produce outputs with incompatible or incomplete vocabularies.** The theory channel uses one set of words; the data channel uses another. Neither fully captures the reconciled concept synthesis is trying to express.
- **Borrowed terms are imprecise.** Using an existing word that almost-but-not-quite fits propagates the mismatch into every subsequent claim that builds on it.
- **Unnamed concepts can't be cited.** Without a word, the concept cannot be referenced from another claim, another note, or another proof step. It stays buried in the prose of one paragraph.
- **Naming commits.** Once coined, the word propagates through review cycles, into downstream notes, into formalization. A poor choice is expensive to revert.

## Structure

```
Two-channel outputs ─ prose from theory + prose from data
        │
        └── synthesis reconciles
                │
                ├── existing word fits? ── use it
                └── no existing word precise enough? ── coin a new word
                        │
                        └── word enters note narrative
                                │
                                ├── referenced in subsequent claims within the note
                                ├── adopted by downstream notes through their own review cycles
                                └── candidate for prose compression when formal manipulation requires a symbol
```

The coinage is a single event with downstream consequences. The same word gets cited many times after; each citation depends on the coinage being stable.

## When it works

- The concept is precise enough that a single word can capture it (not a vague cluster, not a paragraph's worth of context)
- No existing word in either channel's vocabulary already expresses the concept adequately
- The word is short enough for repeated use in narrative and dense formal contracts
- The coinage happens at the synthesis moment, before the concept gets discussed in other claims under a different ad-hoc phrase each time

## Produced by

Prose coinage happens in two distinct modes:

**Synthesis coinage.** The stage where two-channel outputs get reconciled into a single note. Coining happens in bulk here — roughly 70% of a note's prose coinages appear in the first draft from synthesis.

**Review-driven coinage.** When a reviewer surfaces a concept the current text is discussing in ad-hoc prose without a shared name, revise coins one. This happens in both discovery review cycles AND formalization review cycles (local-review, contract-review, regional-review, full-review).

Discovery-stage review-driven coinage in ASN-0036 produced `subspace` in review cycle 1. Formalization-stage review-driven coinage produced terms like `execution trace`, `initial empty state` (AX-1), `allocation-mediated entry` (AX-2), `hierarchical allocation discipline` (S7d), `element subspace projection` (E₁) — none of which existed in the first draft. Each was coined during regional review when the reviewer pressed on a concept the current text hadn't named.

Roughly 70% of coinage happens in synthesis; the remaining 30% is review-driven and occurs across both discovery and formalization.

## Leads to

[Prose compression](prose-compression.md) — once a coined word is stable and used frequently in formal manipulation, it gets compressed to a symbol. The coinage precedes the compression; both refer to the same concept in different forms.

[Domain language emergence](../design-notes/domain-language-emergence.md) — aggregates many Prose Coinage events across a note and across the lattice into the observed phenomenon of a system-wide vocabulary that accumulates through operation.

[Review/revise iteration](review-revise-iteration.md) — reviewer pressure surfaces concepts that need names; revise performs the coinage or refines an earlier one.

[Vocabulary bridge](vocabulary-bridge.md) — a coined word may become a bridging term used across multiple notes, connecting domain language from one foundation layer to structural language in another.

## Origin

Observed in every note that went through synthesis, and in review cycles at both discovery and formalization stages.

**Synthesis coinage.** ASN-0034's first draft (commit `efb2cf66`, March 2026) already contained coined words including `divergence`, `action point`, `displacement`, `inc`, `zeros`, `sig`, `shift`, `zero tumbler`. Each was a new prose word at the moment of synthesis — neither Nelson's design documents nor Gregory's C source code used them in that form. They were coined to reconcile the two channels' outputs into a single note.

**Discovery-stage review coinage.** ASN-0036's most-cited invented concept, `subspace`, was coined during review/revise cycle 1 (commit `639de0a6`, March 2026) — the reviewer pressed on S8's correspondence-run partition claim, and the reviser coined `subspace(v) = v₁` along with the S8-depth axiom to name the part of a V-position that stays constant within a run.

**Formalization-stage review coinage.** During ASN-0036's regional review work (April 2026), several new prose concepts were coined that didn't exist in the discovery document:
- `execution trace` — coined during S5 cone cycle 1 to restructure S5's proof from model-theoretic to operational
- `initial empty state` (AX-1) — coined to name the starting point of execution traces
- `allocation-mediated entry` (AX-2) — coined to constrain how content enters `dom(C)`
- `hierarchical allocation discipline` (S7d) — coined during S7 regional review when the decomposition required a name for this constraint
- `element subspace projection` (E₁) — coined alongside its symbol during D-CTG-depth cone cycle 2

Each of these is the same pattern operating at a different stage — a reviewer surfaces a concept the current text hadn't named; the reviser coins it.

Prose Coinage is what makes the system's reasoning externalizable and cumulative. Without it, concepts would live in paragraphs of prose with no citable handle, and the lattice would not grow as a structure of named interconnected claims.
