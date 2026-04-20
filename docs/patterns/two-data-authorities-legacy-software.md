# Two Data Authorities — Legacy Software Discovery

*An instantiation of [Two Data Authorities](two-data-authorities.md) for reverse-engineering the principles behind legacy software systems.*

## Pattern

Legacy software systems embed principles that were never written down explicitly. The original designer had intent; the code has behavior. Over time the two diverge, documentation drifts, and the actual system is understood by no one completely. Reading either side alone is insufficient — the designer's writings are gestural and may not match what shipped; the code is un-interpreted mechanical behavior with implementation-specific naming.

The pattern: treat the designer's material as the theory channel and the working implementation as the data channel. Constrain each so neither contaminates the other. Synthesize into a single note that reconciles intent with behavior, coining names for the correspondences that bridge the two.

## Forces

- **Source of truth is split.** Neither channel alone is authoritative. The designer's intent matters for semantic claims; the code's behavior matters for what actually happens. A single-source approach smuggles in the bias of whichever side was consulted.
- **Implementation drift.** Over the system's life, the code and the design documents diverge. The divergence points are where the interesting discoveries live — places where implementation revealed something the design hadn't anticipated, or where implementation compromised something the design required.
- **Un-interpreted mechanical evidence.** Raw code answers behavioral questions but doesn't say what the behaviors *mean*. Naming what the code is accomplishing is interpretive work that happens outside the code itself.
- **Gestural design prose.** Designer writings often describe the system's purpose and guarantees in descriptive prose without giving a formal algebra. The operations and relations are implicit in the prose, waiting to be extracted.

## Structure

```
Designer's material (books, specs, notes) ──→ theory channel ──┐
                                                                ├──→ synthesis ──→ reasoning doc
Working implementation (source + live system) ──→ data channel ─┘
```

**Theory channel** responsibilities:
- Answer questions about intent, guarantees, semantic commitments
- Return verbatim quotes with source citations (page numbers, section references)
- Do not reference implementation details

**Data channel** responsibilities:
- Answer questions about behavior, mechanisms, relations between behaviors
- Return claims tied to `file:line` references
- Generate new golden tests against the live system when existing tests don't answer
- Do not use design vocabulary

**Synthesis** reconciles the two into named correspondences. Where the theory channel's intent and the data channel's behavior agree, the claim is validated. Where they disagree, the disagreement is the discovery. Concepts that neither channel names directly get coined at this step.

## When it works

- The designer's material is accessible and comprehensive enough to answer intent questions
- The implementation is readable source code (not just binaries) and can be run for behavioral testing
- The design and the implementation were produced with enough independence that they don't simply echo each other
- Both can be framed as evidence against the same kind of abstract claims

## Empirical findings from the Xanadu demonstration

- **Saturation of the implementation channel.** After approximately 80 golden tests, the implementation channel transitioned from probe-heavy to archive-heavy. New questions became answerable from the existing test corpus rather than requiring new probes. The mechanical surface of a bounded legacy system is finite and largely mappable.
- **70/30 coinage split.** Approximately 70% of invented vocabulary appears in first-draft synthesis; 30% emerges in review/revise cycles. The synthesis step does most of the algebra construction; review surfaces precision-critical terms the first draft glossed over. See [domain language emergence](../design-notes/domain-language-emergence.md).
- **Noun/verb source-shape asymmetry.** The designer's material (Nelson's concept catalog) is overwhelmingly noun-heavy: a list of things (tumbler, span, endset, hyperfile) with relations expressed as nominalized prose ("an arithmetic could be developed"). The implementation is verb-present but wrapped in implementation names (`tumbleradd`, `strongsub`, `weaksub`). Synthesis's work is to lift relations out of nominalization and verbs out of implementation-packaging — the coinage comes from bridging these shapes. See [Channel Asymmetry](channel-asymmetry.md).
- **Case study: `subspace`.** ASN-0036's most-used term (117 uses in the final version) was absent from the first draft. It was coined during review cycle 1 when a reviewer pressed on the run-partition claim and the reviser had no word for "what stays fixed under a correspondence run." This is characteristic of the 30% review-driven coinage — the term was precision-critical and did not emerge until review pressure surfaced the gap.

## Leads to

- [Prose Coinage](prose-coinage.md) — the atomic event of inventing a bridging term at the correspondence between channels
- [Lattice](lattice.md) — the synthesis output accumulates into an interlinked body of claims
- [Domain Language Emergence](../design-notes/domain-language-emergence.md) — the aggregate phenomenon of vocabulary building up through repeated coinage

## Origin

Observed on the Xanadu demonstration: reverse-engineering udanax-green (Roger Gregory's C implementation) with Ted Nelson's *Literary Machines* as the designer's source. The two-channel setup was chosen deliberately at the start; the specific dynamics (saturation, noun/verb asymmetry, 70/30 coinage split) were observed as the pipeline ran.
