# Two-Channel Architecture

The mechanism that produces new knowledge for the lattice. Two independent agent channels investigate a question under enforced vocabulary separation. A synthesis agent integrates their outputs into a structured note. The note enters the [note convergence protocol](protocols/note-convergence-protocol.md) for review/revise cycles. The channel architecture governs how the initial note is generated, not how it matures.

## The two channels

The theory channel consults established domain knowledge — literature, models, known principles. The evidence channel analyzes raw evidence — measurements, source code, experimental outputs. A vocabulary firewall prevents each from using the other's terms. The evidence channel reasons from evidence alone. It cannot retrieve known solutions from theoretical vocabulary — it can only report patterns it observes. This forces hypothesis space exploration rather than retrieval.

The firewall is the generative constraint. Without it, the evidence channel borrows theoretical conclusions instead of deriving observations from the data. With it, the evidence channel's findings are independent — when they agree with theory, the agreement is earned. When they disagree, the disagreement is real. The disagreements are where discovery happens.

## Channel asymmetry

The two channels receive different context at question-generation time. The asymmetry is intentional and reflects a representational difference between the two spaces.

**Theory generators see a vocabulary list.** The generator's prompt includes a short, stable list of the theoretical framework's own terms — not modern terminology, not the field's general vocabulary, but the specific words the corpus uses. Maxwell's corpus gets "vis viva, elastic collision, equilibrium, β" — not "degrees of freedom, equipartition, statistical mechanics." Nelson's design gets "content, identity, permanence, links, documents, sharing, versions" — not "I-addresses, spanfilade, enfilade." The vocabulary list bounds the generator's imagination without overwhelming it. Theory space is conceptual and listable.

**Evidence generators see the corpus.** The generator's prompt includes the evidence corpus itself (or a curated synthesis when the corpus is too large). The generator sees the specific substances, measurements, code structures, or artifacts the evidence contains. Without this visibility, evidence questions default to generic retrieval — "what does the corpus report about X?" — because the generator has to imagine what might be there rather than seeing what is there. With corpus visibility, questions target specific content bearing on the inquiry. Evidence space is specific and must be seen.

**Vocabulary must use the corpus's own language.** If the theory vocabulary list contains modern terms the corpus doesn't use, the generator produces questions the corpus can't answer. The evidence corpus must not leak specific values or named patterns into the questions themselves — the answers extract values, the questions do not pre-state them.

## Decomposition

Each inquiry is decomposed into channel-appropriate sub-questions. Theory questions ask what the theoretical framework predicts, requires, or commits to about the inquiry's subject. Evidence questions ask what the empirical record shows bearing on the inquiry. Neither channel sees the other's sub-questions.

The question count per channel is not forced to be symmetric. An inquiry that has more to ask one channel than the other should ask more of that channel. Forced symmetry produces triplicates on the side with less to say.

## Consultation

Each channel answers its own questions from its own corpus. The theory answerer stays inside the theory corpus — it does not invoke results or theories beyond what the corpus contains, and it says so explicitly when a question reaches beyond the corpus's scope. The evidence answerer reports what the data shows — numerical values, units, conditions, citations — and does not theorize about why. Channel discipline is the foundation the synthesis step depends on.

## Synthesis

A synthesis agent reads all answers from both channels and writes a structured note with dependency-mapped claims. The synthesis is the first place both perspectives meet. Where the channels agree, principles are validated. Where they disagree, new hypotheses emerge.

Synthesis is where most vocabulary coinage happens — roughly 70% of a note's coined terms appear here, because synthesis is where incompatible vocabularies must be merged into a single note and no existing word may fit precisely.

## Channel plugins

Channels are self-contained plugins. Each holds source content, consultation code, consultation prompts, and metadata. Channels are named identities in a flat top-level namespace (`channels/`). Campaigns reference them by name. Each channel exposes a two-function interface:

- `generate_questions` — decompose an inquiry into channel-appropriate sub-questions
- `consult` — answer a single question from the channel's corpus

Internal implementation is the channel's business — flat-corpus single invocation, multi-section template assembly, KB-plus-code parallel with tool access, whatever fits. The campaign binds two channel plugins to a target and a bridge vocabulary. The binding is immutable per campaign — any channel change means a new campaign.

## Bridge vocabulary

The unified terms that make a campaign's two channels speak coherently. Curated at campaign creation time, not emergent. Vocabulary is campaign-level because it bridges two specific channels — different pairings produce different bridges. The primary consumer is the reviewer during note convergence, who must interpret claims against both channels' terminology.

## Origin

This architecture was developed to formalize the Xanadu hypertext system — pairing Nelson's design intent (theory) with Gregory's implementation (evidence) under enforced vocabulary separation. The first test of generality was the materials science deployment: Maxwell's 1867 dynamical theory of gases (theory) paired with Dulong & Petit's 1819 specific-heat measurements (evidence). The same channel architecture, same firewall, same synthesis — with domain-specific calibration (vocabulary lists, corpus injection). The architecture transferred. The calibration work was bounded.

## Related

- [Discovery](discovery.md) — the stage that uses the two-channel architecture to produce notes for the lattice.
- [Note Convergence Protocol](protocols/note-convergence-protocol.md) — the protocol that drives the synthesized note toward stability after channels produce it.
- [Architecture](architecture.md) — channel plugins, bridge vocabulary, and campaign bindings in the system's structural reference.
- [The Voice Principle](principles/voice.md) — the Dijkstra voice governs the synthesized note from its first draft. Channel outputs are raw material; the synthesis writes in voice.
