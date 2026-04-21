# Question Generator Context

*Design note. Why the theory-channel and evidence-channel question generators receive different amounts of corpus context, and what shape of context is appropriate for each.*

## Overview

The decompose stage produces sub-questions for each channel from the root inquiry. Each channel's question generator assembles its prompt from the inquiry, optional scope exclusions, and — crucially — an optional context load from the channel's own corpus.

The two channels are not configured identically. The theory channel's generator sees only a short, stable list of vocabulary terms. The evidence channel's generator sees the corpus itself (directly or through a curated synthesis). This asymmetry is intentional. It is the operational consequence of the [channel asymmetry](../patterns/channel-asymmetry.md) pattern — the same representational mismatch that makes synthesis valuable also dictates that the two sides' generators must be built differently.

## The two patterns

**Vocabulary-in-prompt (theory side).** The generator's prompt includes a prose list of the domain's theoretical vocabulary. No corpus is loaded. The generator uses this list to shape inquiry-appropriate questions. The theory space is closed and stable enough that a compact vocabulary list bounds the generator's imagination without overwhelming it.

In xanadu, Nelson's theory-side generator uses: *"Nelson thinks about content, identity, permanence, links, documents, users, sharing, and versions."* Eight terms. That list has remained stable across many inquiries. In materials, the equivalent list names theoretical-physics categories: energy, motion, temperature, pressure, molecular motion, degrees of freedom. Again, a handful of terms, stable across the domain.

**Corpus-in-prompt (evidence side).** The generator's prompt reserves a slot filled at generation time with actual content from the evidence corpus. The generator sees what is present in the evidence before producing questions — the specific substances, the specific artifacts, the specific measurements, or whatever content shape the evidence takes.

In xanadu, Gregory's evidence-side generator loads a curated synthesis of the udanax-green implementation: around 60KB of organized prose covering named subsystems (state structure, control flow, frame conditions), with vocabulary specific to the implementation (tumbler, spanfilade, subspace) and references back to specific source locations. The generator uses this map of what exists to ask targeted questions about specific mechanisms.

## Why the asymmetry

Evidence corpora are **specific**. They consist of particular artifacts: measurement tables, source code, experimental outputs, historical documents. A generator that has not seen the corpus cannot produce questions that engage its contents. It can only produce questions about the *idea* of the corpus, framed by the generator's imagination of what such evidence might contain.

Theory corpora are **conceptual**. They carry principles, frameworks, named reasoning structures. The vocabulary that identifies the important moves in a theoretical corpus is usually small and listable — the concepts are more stable than the specific textual instances of them. Listing those terms in the generator's prompt is enough for it to produce questions that use the theory's categories.

The [channel asymmetry](../patterns/channel-asymmetry.md) pattern explains this at the consumed-source level: theory and evidence arrive in fundamentally different representational shapes, and that shape mismatch is what forces synthesis to [construct bridging vocabulary](../patterns/prose-coinage.md). The question-generator context asymmetry is the same mismatch expressed one stage earlier, at the generation of the sub-questions that feed synthesis.

## Failure mode: missing corpus on the evidence side

When the evidence-side generator is configured without corpus injection — given only the inquiry and a vocabulary hint — it cannot ask inquiry-grounded empirical questions. It falls back to what it *can* do without the corpus: framing generic data-retrieval queries about whatever shape of evidence it imagines might exist. Questions take the form *"what does the corpus report about X?"* where X is supplied by the generator rather than by the corpus.

When answered faithfully, these questions produce a catalog of the corpus rather than an analysis of what the corpus implies for the inquiry. Downstream synthesis receives the catalog and has to re-invent the inquiry-corpus connection that the evidence sub-questions should have established.

The materials domain's first full-pipeline run exercised this failure mode directly. Its evidence-side generator was initially built without corpus injection, as a symmetric copy of the theory side. On an inquiry about heat and the constitution of matter, with an evidence corpus documenting a well-known empirical regularity, all ten evidence questions came back as retrieval queries against the corpus — catalog entries about what the data report, none of them engaging the inquiry. The theory side, correctly configured with vocabulary-in-prompt, produced questions that did engage the inquiry. The asymmetric configuration was reproduced from xanadu once the structural reason was recognized.

## Failure mode: excess corpus on the theory side

The symmetric mistake — injecting the full theory corpus into the theory-side generator — has a different pathology. A theory corpus typically contains extensive argumentation and formal development. A generator that has read the whole corpus tends to anchor its questions to the corpus's own organization rather than to the inquiry. Questions become *"what does chapter N say about Y?"* rather than *"what does the theory predict about the inquiry?"* — the inverse failure mode.

Vocabulary-in-prompt sidesteps this. By giving the theory generator only the named terms of the theoretical framework, it stays inquiry-oriented: it has to construct a question that uses theoretical vocabulary to engage the inquiry, rather than a question that asks the theory to explain itself.

## Configuring a new domain

The conceptual decision: for each channel, decide which side of the asymmetry it sits on. Most of the time, the answer follows the consumed-source shape directly. If the channel consumes descriptive/conceptual sources with stable vocabulary (theoretical frameworks, design documents, established principles), its generator uses vocabulary-in-prompt. If it consumes specific artifacts (data, code, measurement records, historical documents), its generator uses corpus-in-prompt.

Two considerations at setup time:

**The vocabulary list, when used, must be stable across inquiries in the domain.** If each inquiry demands a different slice of vocabulary, the list is not doing its job — the generator is being under-served. In that case, the channel may have crossed into corpus-in-prompt territory even though it looks conceptual.

**The corpus injection, when used, must not be so large that it dominates every generation call.** For large or multi-file evidence, a curated synthesis of the corpus — shorter, structured for navigation — replaces the raw corpus. Xanadu's 60KB synthesis of udanax-green is an example of this shape: it documents what is present and how it is organized, without reproducing the raw source. The generator uses the synthesis to know what to ask; the answerer (in the consultation stage) reads the raw corpus to give the answer.

## When the vocabulary-listed approach fails on theory

The vocabulary-list pattern assumes the theoretical space is closed and listable in a paragraph. A theory corpus spanning many frameworks, or a domain where theoretical vocabulary itself evolves over time, may exceed what a static list can bound. At that scale the theory side may need a curated synthesis of its own — a structured map of concepts and their relationships, analogous to the synthesis used on the evidence side but keyed to conceptual vocabulary rather than to specific artifacts.

This case has not yet been observed in xanadu or materials. It is documented as a boundary condition to be aware of when scaling a domain's theoretical coverage beyond the size a vocabulary list can cover.

## Related

- [channel asymmetry](../patterns/channel-asymmetry.md) — the upstream pattern this operationalizes
- [scoped inquiry](../patterns/scoped-inquiry.md) — per-inquiry scoping mechanism that handles target-specific leaks after question generation
- [consult-authority](../patterns/consult-authority.md) — the broader pattern of channel-specialized consultation
