# Two Data Authorities

## Pattern

When agents reason about a domain, a single source of evidence produces conclusions shaped by its own biases. Theory confirms itself. Data without structure stays anecdotal. Combining them naively lets one contaminate the other — the theory channel interprets data to fit, or the data channel adopts theoretical framing uncritically.

Separate the evidence into two independent channels with enforced boundaries. Each channel reasons from its own source under constraints that prevent it from referencing the other. A synthesis step integrates both. Where the channels agree, findings are validated. Where they disagree, new structure emerges — the disagreement is the discovery.

## Forces

- **Single-source bias.** One channel sees what it expects to see. Theory finds confirmation. Data finds patterns without knowing which ones matter.
- **Contamination.** If theory can reference data, it cherry-picks. If data can use theoretical terms, it imports assumptions. Independence must be enforced, not hoped for.
- **Agreement is validation.** When independent channels reach the same conclusion through different evidence, the conclusion is robust — it doesn't depend on one source's biases.
- **Disagreement is discovery.** When the channels conflict, something new is present — a claim, a distinction, a relationship that neither channel would find alone.

## Structure

```
source A ──→ channel A (constrained) ──┐
                                        ├──→ synthesis ──→ structured output
source B ──→ channel B (constrained) ──┘
```

The constraint is a vocabulary firewall — each channel is prohibited from using the other's terms. Channel A cannot reference Channel B's evidence. Channel B cannot adopt Channel A's framing. The synthesis agent sees both and integrates.

## When it works

- The two sources offer genuinely independent perspectives on the same domain
- The vocabulary firewall is enforceable (the channels have distinct terminologies)
- The synthesis step can identify agreement and disagreement structurally, not just by surface similarity

## When it fails

- One source dominates — the other channel has too little evidence to contribute meaningfully
- The vocabulary firewall leaks — shared terms allow implicit contamination
- The synthesis step forces agreement — disagreements are resolved by picking a winner rather than treated as discovery signals

## Leads to

[Lattice](lattice.md) — the synthesis output becomes a note in the lattice. The two-authority process produces the raw material that the lattice organizes.

[Review/revise iteration](review-revise-iteration.md) — the quality of discovery output determines how much work claim convergence must do. Clean two-authority discovery → fewer gaps → faster review/revise convergence.

## Served by

[Channel Asymmetry](channel-asymmetry.md) — specifies the shape relationship between the two channels. When the channels arrive in incompatible representational shapes, the bridging pressure produces genuine coinage rather than symbol-matching.

## Instantiations

- [Two-Channel Architecture](../two-channel-architecture.md) — the concrete architecture this pattern takes in the xanadu and materials lattices. Specifies channel plugins, vocabulary firewall enforcement, channel asymmetry at question-generation time, and synthesis.
- [Legacy Software Discovery](two-data-authorities-legacy-software.md) — grounded instantiation. Reverse-engineering the principles behind a legacy software system using the designer's material as theory and the working implementation as data. Xanadu is the worked example.

## Applications

### Theory and evidence channels

**Channel A**: consults established theory (Nelson's *Literary Machines*, formal specifications). Cannot reference implementation details or code behavior.

**Channel B**: analyzes raw evidence (Gregory's udanax-green implementation, operational traces). Cannot use theoretical terms or cite design documents.

**Vocabulary firewall**: theory channel cannot say "the code does X." Evidence channel cannot say "Nelson requires X."

**Synthesis**: integrates both into notes with dependency-mapped claims. Each claim traces to theory, evidence, or both. Disagreements become open questions or new claims.

### What it discovered

- T10a allocator discipline — theory described hierarchical allocation, evidence showed `inc(·,0)` sibling streams. The match validated both; the constraints (`k' ∈ {1,2}`) emerged from disagreement about how deep allocation can go.
- Corollary claims from absorb runs (ASN-0055/0057/0060) — evidence found patterns that theory hadn't named. The two-authority synthesis produced new claims that neither channel would have found alone.
- Integration gaps (S7c analogs, GlobalUniqueness citation, backward shift) — places where theory assumed something evidence didn't confirm, or evidence showed something theory hadn't formalized.

## Origin

The two-channel architecture was present from the start — theory and evidence channels separated by vocabulary firewall. The pattern was recognized when the disagreements between channels consistently produced the most valuable discoveries. Agreement was expected; disagreement was where the work happened.
