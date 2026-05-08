# Glossary

Terms specific to this reasoning system. Cross-references point to where each term is discussed substantively.

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [Y](#y)

## A

**Accretion.** Growth of the lattice by adding new claims rather than mutating existing ones. The discipline that prevents [Contract Sprawl](equilibrium/contract-sprawl.md). See [Accretion pattern](patterns/accretion.md).

**Active links.** A substrate query that returns only tuples in the active subset `A_K = L_K \ {tuples targeted by a retraction}`. The Observe operation supports two views — `A_K` (active, excluding retracted) and `L_K` (full audit trail). Predicate evaluation (per-comment closure, sidecar freshness, etc.) reads `A_K`; audit and history queries read `L_K`. The active-subset check is single-depth: retracting a retraction does not restore the original. See [Substrate spec](protocols/substrate/README.md).

**Adaptive scope.** A claim refinement scope strategy where context grows on demand — the reviewer requests missing references, the scope assembler expands the cone, the review re-runs. Catches within-cone issues efficiently without preloading the whole foundation. Counterpart to [comprehensive scope](#c). A choreography decision, not a protocol-level construct. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Agent registry.** The finite static set `R` of agents the [runner](#r) schedules. Part of the substrate's static spec — registered alongside the type catalog and shape registry. Each agent is a tuple `(name, signature, trigger T_A, scope D_A, action act_A, provenance binding)`. Two populations: runner-walked (predicate-fired by the runner) and operator-gated (invoked by filesystem-mediated signals). See [Agents](protocols/substrate/agents.md) and the [agent caste docs](protocols/agents/).

**Apex (cone apex).** The high-dependency claim at the center of a [dependency cone](patterns/dependency-cone.md) — the one that keeps getting revised while its dependencies remain stable.

**Assembly.** The stage that exports converged claims into `claim-statements.md` and `dependency-graph.yaml` for downstream consumers. Mechanical, no LLM.

**Attractor, Genesis.** A claim that becomes the default home for every fact anyone needs about a concept it introduces. Cause of [Contract Sprawl](equilibrium/contract-sprawl.md).

**Authority.** A source the reasoning system consults — for example, Nelson's design documents (theory authority) or Gregory's implementation (evidence authority). See [Two-Channel Architecture](two-channel-architecture.md).

**Axiom.** A claim classified as assumed rather than derived. Stated without proof.

## B

**Boundary observation.** An out-of-scope finding captured during investigation — enough context to seed a new investigation without expanding the current one. Seed for [scope promotion](patterns/scope-promotion.md).

**Bridge citation.** A citation to a claim that licenses an inference step between two other concepts in a proof. Missing bridge citations are a subtype of [Citation Drift](equilibrium/citation-drift.md#subtype-bridge-citations).

**Bridge vocabulary.** The unified terms that make a campaign's two channels speak coherently. Curated at campaign creation time, not emergent. Campaign-level because it bridges two specific channels — different pairings produce different bridges. The primary consumer is the reviewer during note maturation, who must interpret claims against both channels' terminology. See [Two-Channel Architecture](two-channel-architecture.md).

## C

**Campaign.** Binds a theory channel and an evidence channel to a target and a bridge vocabulary. The operational unit of coordinated investigation. The channel pairing is immutable per campaign — any channel change means a new campaign with a new vocabulary. Ends when its question is answered (verified attachment) or abandoned (negative result). Scope promotion during review spawns additional inquiries within the same campaign; genuinely new questions spawn new campaigns. See [Architecture](architecture.md).

**Caste.** The structural role an agent plays in the substrate-emission pattern. Three castes exist in the registry: [producer](#p) (grants new identity), [refiner](#r) (closes findings), [scout](#s) (detects and reports). Caste classification follows *primary substrate effect* — an agent that does multiple things in one fire is classified by what it primarily changes about substrate state. See [agent registry README](protocols/agents/README.md).

**Channel.** A self-contained plugin holding source content, consultation code, consultation prompts, and metadata. Channels are named identities in a flat top-level namespace (`channels/`). Each channel exposes a two-function interface: `generate_questions` (decompose an inquiry into channel-appropriate sub-questions) and `consult` (answer a single question from the channel's corpus). Internal implementation is the channel's business. Campaigns reference channels by name. See [Architecture](architecture.md).

**Channel asymmetry.** Shape-mismatch between the theory channel and the evidence channel. Theory space is conceptual and listable (vocabulary-in-prompt). Evidence space is specific and must be seen (corpus-in-prompt). Prevents naive merging and forces synthesis to coin bridging vocabulary. See [Channel Asymmetry pattern](patterns/channel-asymmetry.md).

**Choreography.** How a protocol's predicate is driven true in practice — which scope to use, what order to review in, when to alternate strategies, what to assemble as context. Distinguished from the [protocol](#p) itself, which defines only the predicate. Different choreographies satisfy the same predicate. The protocol IS the predicate; everything else is choreography. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Citation, inline.** A reference in the proof narrative like "by NAT-wellorder." Part of proof content, not metadata.

**Citation (link type).** The substrate link that records a dependency between two reasoning units — claim→claim during claim refinement, note→note during note maturation. The lattice edge. Distinct from [inline citation](#c) (proof-narrative reference). A citation may be nullified by a [retraction](#r) link pointing at it; the substrate retains both, and `active_links` queries return only un-retracted citations. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Claim.** A single unit of reasoning within a note. An assertion — something the system says is the case, which can be verified, contested, or refuted. Has a label, type, formal contract, and dependencies. The atomic lattice node. See [Architecture](architecture.md).

**Claim refinement.** The stage that takes per-claim files from claim derivation and runs review/revise cycles until each claim's reasoning is sound. Not cleanup — discovery under precision constraint. Scope narrowing to per-claim files is itself epistemically productive. See [Claim Refinement](claim-refinement.md); protocol details in [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Claim Document Contract.** The structural contract specifying what well-formed per-claim file state looks like after claim derivation. Concrete rules, mechanically checkable: one body per file, filename matches label, references resolve, metadata agrees with content, no dependency cycles. The first instance of the output contract the [Validation Principle](principles/validation.md) requires. See [Claim Document Contract](design-notes/claim-document-contract.md).

**Comment (link type).** A substrate link recording a reviewer finding on a document. Subtypes carry the classification: `comment.revise` requires resolution and participates in the [convergence predicate](#c); `comment.observe` is a non-blocking observation (claim refinement only); `comment.out-of-scope` is a non-blocking signal that the lattice needs structural work (note maturation only). See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Cone, dependency.** A cluster of tightly coupled claims where an apex keeps being revised while dependencies are stable. See [Dependency Cone pattern](patterns/dependency-cone.md).

**Cone-review.** Focused review of a specific dependency cone — apex claim plus its declared dependencies as context. Resolves the cluster as a constraint system. The operational name for cone-scoped review under [adaptive scope](#a) in the [maturation protocol](protocols/maturation/note-to-claim.md).

**Cone-sweep.** Proactive walking of the dependency DAG bottom-up, running cone-review on every apex meeting the dependency-frequency threshold. Implemented in `scripts/claim-cone-sweep.py`. A choreography that satisfies the protocol's coverage obligation by exhausting the apex set.

**Comprehensive scope.** A claim refinement scope strategy where the entire note (or full cone) is loaded into review context before the review runs. Catches cross-cone issues that adaptive scope can miss — vocabulary collisions, citation inconsistencies between dependency clusters, gaps invisible to within-cone reasoning. Counterpart to [adaptive scope](#a). A choreography decision, not a protocol-level construct. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Consult authority.** During revision, return to source material to ground findings in evidence. See [Consult Authority pattern](patterns/consult-authority.md).

**Convergence predicate.** The per-comment closure predicate within the [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md): every `comment.revise` link targeting a document has a matching `resolution` link. Used at both note-stage (note maturation) and claim-stage (claim refinement) of the protocol. The predicate is the termination condition of the Correction Stigmergic Protocol primitive. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Content.** What the `.md` file holds — narrative, proof, formal contract claims. Distinct from metadata.

**Contract, formal.** The structured claim section of a claim (`*Formal Contract:*`): preconditions, postconditions, invariants, axiom, definition. Part of content.

**Contract (link type).** A substrate link classifying a claim by structural kind: `contract.axiom`, `contract.definition`, `contract.theorem`, `contract.corollary`, `contract.lemma`, `contract.consequence`, `contract.design-requirement`. Subtypes name structurally distinct kinds with different required fields. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Coverage.** The choreography's obligation to actually conduct reviews at sufficient scope. The [convergence predicate](#c) is trivially satisfied when no reviews have happened — the protocol says "all filed concerns are addressed," not "sufficient examination has occurred." Coverage is what closes that gap. A protocol-level non-guarantee; a choreography-level requirement. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Contract Sprawl.** A claim's formal contract keeps growing across cycles because it is a [Genesis Attractor](equilibrium/contract-sprawl.md). See [Contract Sprawl](equilibrium/contract-sprawl.md).

**Corollary.** A claim classified as an immediate consequence of another.

**Correction Stigmergic Protocol.** A primitive of the [Stigmergic Protocol](#s) family. Pattern: a scout files a `comment.revise` link on a target document; a refiner observes the comment and emits a `resolution` link plus the corresponding edit; the runner reschedules until every comment is closed. Termination condition: every `comment.revise` on the target has a matching `resolution`. The [convergence predicate](#c) is the per-comment closure form of Correction. Composes with [Cycle](#c) to drive iterative improvement. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Coupling Principle.** Design commitment that prose and formal content are authored as a pair at an artifact-specific ratio (90/10 for notes, 70/30 for claim files). Divergence from the ratio signals decoupling — one surface growing without the other. Prose is the generative substrate; formal notation precipitates from it. Too much prose fails loudly (hand-waving). Too much formal fails silently (discovery stops). One of three principles forming the quality boundary for review. See [The Coupling Principle](principles/coupling.md).

**Cycle Stigmergic Protocol.** A primitive of the [Stigmergic Protocol](#s) family. Pattern: a primary fact (review record, audit, contract) triggers a secondary fact (revise, fix); the secondary fact's emission invalidates the primary's freshness, retriggering the primary; the loop runs until [quiescence](#q). Composes [Correction](#c) or [Self-Review](#s) with a freshness predicate to drive iteration. The [maturation protocol](#m) uses Cycle to drive note maturation and claim refinement to scope quiescence. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

## D

**Decomposition (link type).** A substrate `provenance.derivation` link records that claim derivation produced a claim from a note. From = note, to = claim. Provenance trail from a note to each of its decomposed claim files. Filed by the claim derivation module. Sibling of `provenance.synthesis`, `provenance.extract`, `provenance.absorb`, `provenance.reset`. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Definition.** A claim classified as introducing named concepts or operations.

**Depends.** A claim's dependencies on foundation claims, reified as `citation.depends` substrate tuples. Authored prose-side in the references sidecar (`<stem>.references.md`); the [`citation_resolve`](protocols/agents/producers.md) agent emits the substrate tuples and keeps them in sync as proofs evolve. The forward direction is `citation.forward`. At note granularity, the same shape: substrate `citation` tuples between notes.

**Description (link type).** A substrate-owned link associating a document with a sibling `<stem>.description.md` carrying its prose summary. Multi-line markdown content. The substrate's three document-attribute types (`label`, `name`, `description`) share a structure: typed link from the document to a sibling attribute doc, edited in place when the value changes, link survives content updates. Stage-1 mutability: the doc is overwritten on edit; document-level history will be Xanadu's job at the cut. Retraction is reserved for wrong-link cases, not value updates. See [Relation Shapes](protocols/substrate/shapes.md).

**Design requirement.** A claim classified as an architectural or measurement constraint the system imposes.

**Discovery.** The first stage. Combines three mechanisms to bring new knowledge into the lattice: the [two-channel architecture](two-channel-architecture.md) generates an initial note from independent theory and evidence channels; the [maturation protocol](protocols/maturation/note-to-claim.md) drives the note to stability through review/revise cycles; the [maturation protocol](protocols/maturation/note-to-claim.md) executes the lattice operations (extract, absorb, scope promotion) that discovery's findings trigger. See [Discovery](discovery.md).

**Domain.** The logical configuration of a lattice — which verifier, which channels, which vocabulary firewall. Expressed in `lattices/<L>/config.yaml`, not as a separate directory. Two configurations that differ in any binding are different domains. The domain is what you swap to move the engine from one subject area to another. See [Architecture](architecture.md).

**Drift, Citation.** The state where citations (substrate `citation.depends` tuples + inline prose) no longer match the dependencies a proof actually uses. See [Citation Drift](equilibrium/citation-drift.md).

**Driver (Citation Drift).** The cause class that produces drift.
- **Internal driver** — active work inside the same note produces drift within that note. Continuous.
- **Passive driver** — work in an upstream note produces drift in downstream consumers. Event-driven.

**Domain language emergence.** The process by which the system coins new prose words for concepts it will reason with, as two-channel synthesis and subsequent review cycles produce claims existing vocabulary can't express. See [Domain Language Emergence](design-notes/domain-language-emergence.md).

## E

**Enumerated surface.** A claim structure that pre-identifies where sub-facts will live (e.g., `T10a.1`, `T10a.2`, ...). Invites [accretion](patterns/accretion.md); prevents Genesis Attractors forming.

**Evidence channel.** The agent channel that reads raw evidence (implementation code, experimental measurements) and reports patterns. Forbidden from using theory-level vocabulary. Its question generator sees the corpus itself at generation time (corpus-in-prompt) because evidence space is specific and must be seen. See [Two-Channel Architecture](two-channel-architecture.md).

**Evidence space.** The space of observed behaviors and measurements the evidence channel reports. Complement to [hypothesis space](#h).

**Excavation stages.** The predictable stages review/revise findings progress through as cycles deepen: citation accuracy → completeness → structural coherence → mathematical precision → structural organization → prose clarity. See [Review/Revise Iteration](patterns/review-revise-iteration.md).

**Extract/Absorb.** Finding shared concepts across multiple claims and factoring them into new foundation layers. How the lattice grows inward. See [Extract/Absorb pattern](patterns/extract-absorb.md).

## F

**Finding classification.** The reviewer's classification of each finding by how it should be handled. Two binary schemes apply at different scales. **Note convergence** uses REVISE / OUT_OF_SCOPE — REVISE must fix in-note; OUT_OF_SCOPE signals maturation that adjacent material is missing or misplaced. **Claim refinement** uses REVISE / OBSERVE — REVISE must fix; OBSERVE logs the observation without triggering revision. Both schemes prevent [Surface Expansion](equilibrium/surface-expansion.md) by keeping non-correctness findings from reaching the reviser. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md), [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Firewall, vocabulary.** Structural enforcement that the theory channel cannot use evidence-channel terms and vice versa. Prevents the LLM's training knowledge from shortcutting reasoning. See [Two-Channel Architecture](two-channel-architecture.md).

**Formal-statements export.** Curated export containing all claim summaries and formal contracts in dependency order. Consumed by downstream notes as foundation.

**Foundation.** From a downstream note's perspective, any upstream note it depends on. Foundation content is read-only context for the downstream's review cycles.

**Full-review.** Review reading an entire note's claim set at once. The operational name for review under [comprehensive scope](#c). Finds issues invisible to cone-scoped review: carrier-set conflation, precondition chain gaps, vocabulary collisions, issues in small claims that adaptive scope didn't reach.

**Full scale.** Legacy name for [comprehensive scope](#c) — review of the whole note with full foundation context.

## G

**Genesis Attractor.** See Attractor, Genesis.

**Gravitational failure.** An [equilibrium](equilibrium/) pattern whose force acts continuously across review cycles. Requires permanent discipline — prompt framing, coupling monitoring, voice structure — not a one-time fix. Contrasts with [transitional failure](#t) and [oscillatory failure](#o). Contract Sprawl, Prose Sprawl, Surface Expansion, Index Sprawl, Citation Drift are gravitational.

**Ground state.** The state of genuine convergence — both [adaptive-scope](#a) (cone) and [comprehensive-scope](#c) review agree there are no remaining issues, and the [convergence predicate](#c) holds. Distinguished from "stopped" (no finding at one scope but the other can still expose issues). See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

## H

**Hard reset.** A defined operation in the [maturation protocol](#m) for the case where a foundation turns out to be wrong, not merely incomplete. The note re-enters discovery; its freeze is revoked; all dependents that entered claim refinement against its claims must also reset. A `provenance.reset` link records the cascade. Expensive and destructive — used when the alternative (leaving dependents on a known-bad foundation) is worse. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Hypothesis cluster.** A [cone](patterns/dependency-cone.md) in a science domain: apex (hypothesis statement) plus its supporting dependencies (axioms, definitions, data citations, coined concepts). Convergence of a hypothesis cluster under [adaptive scope](#a) = hypothesis ready for its scope.

**Hypothesis space.** The space of candidate principles and concepts that could organize a domain. Explored by the theory channel. Complement to [evidence space](#e). New [prose coinage](patterns/prose-coinage.md) is a form of hypothesis generation.

## I

**Index Sprawl.** Enumerative prose that grows across review cycles — lists of use-sites, exhaustiveness claims, bundling inventories. The enumerative form of [Surface Expansion](equilibrium/surface-expansion.md). See [Index Sprawl](equilibrium/index-sprawl.md).

**Inquiry.** One initial question that produces one note. 1:1 relationship with the note. A campaign spawns one or more inquiries. The unit of two-channel discovery: theory-channel and evidence-channel sub-questions are derived from it, consulted independently, synthesized into a single note. See [Architecture](architecture.md).

**Internal driver.** See Driver.

## J

**Join.** Lattice operation. A new node is created above multiple foundations. [Scope promotion](patterns/scope-promotion.md) executes a join.

## L

**Label.** A claim's stable citable handle (e.g., `T0`, `NAT-wellorder`, `TA-Pos`). Set at claim derivation, never changes.

**Label (link type).** A substrate-owned link associating a document with a sibling `<stem>.label.md` carrying its short address (the [label](#l) string). One-line file. The substrate-native home for what is currently the filename-stem convention (filenames will not exist in Xanadu). Edit-in-place mutability: renaming a label edits the doc; the link survives. Retraction is reserved for wrong-link cases. See [Relation Shapes](protocols/substrate/shapes.md).

**Lattice.** The coverage target that campaigns build toward: an accumulated verified dependency graph for one subject-area focus. The lattice operates at two granularities simultaneously: during note maturation, notes declare note-level dependencies via substrate `citation` tuples (note→note); during claim refinement, claims declare claim-level dependencies via `citation.depends` / `citation.forward` tuples (claim→claim). Which granularity a consuming note sees depends on the consumer's stage. Notes retire gradually as their consumers enter claim refinement; the terminal lattice is all claim-to-claim edges with note groupings as provenance metadata. See [Architecture](architecture.md).

**Lattice operation.** Collective term for the three structural operations the [maturation protocol](#m) executes on lattice signals: **extract** (claims move down, into a new foundation below consumers), **absorb** (claims move toward natural home, into an existing note), **scope promotion** (questions move out, opening a new inquiry). Distinct from convergence — operations reshape the lattice; convergence stabilizes content within fixed structure. Triggered by signals from note maturation (duplicate derivations, `comment.out-of-scope` findings). See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Lemma.** A claim classified as an intermediate result supporting higher-level theorems.

**Local-review.** *Retired.* Single-claim review was retired during V-cycle consolidation when [adaptive scope](#a) (cone) and [comprehensive scope](#c) were found sufficient to expose all classes of finding. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Local scale.** *Retired.* See [Local-review](#l).

## M

**Markdown body (`.md`).** The file that holds a claim's content: narrative, proof, formal contract.

**Marker Stigmergic Protocol.** A primitive of the [Stigmergic Protocol](#s) family. Pattern: an operator or agent emits a marker tuple (e.g., `note.confirmed`, `claim.derived`, `note.frozen`) declaring a transition has occurred; downstream agents observe markers as preconditions in their triggers. Markers are the substrate's gating mechanism — they sequence stages without out-of-band coordination. Distinct from [Correction](#c) (which closes findings) and [Self-Review](#s) (which audits). See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Maturation Stigmergic Protocol.** The protocol family this stack defines: a substrate-mediated stigmergic protocol composing primitives (Correction, Marker, Self-Review, Cycle) into an end-to-end maturation arc. The first instance is the [Note-to-Claim Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md), which drives content from question to verified knowledge through inquiry consultation, note maturation, claim derivation, per-claim formalization, and per-claim review. Terminates at [scope quiescence](#s) at a designated tier (typically per-ASN). Hosts the lattice operations (extract, absorb, scope promotion) as operator-gated agents within the registry. See the [protocol stack overview](protocols/README.md) and the [maturation protocol doc](protocols/maturation/note-to-claim.md).

**Meet.** Lattice operation. A concept shared by two nodes is extracted into a new foundation layer below both. [Extract/absorb](patterns/extract-absorb.md) executes a meet.

**Metadata.** Per-document attributes carried by sidecar documents (label, name, description, signature, references, statements) and Classifier links (e.g., `contract.<kind>`) in the substrate. Each sidecar is a substrate-citizen document linked to its parent via an Attribute-shape relation. Describes the claim or note; does not constitute its reasoning.

**Modeling.** The stage translating formal contracts into mechanically verifiable code (Dafny, Alloy). Follows claim refinement; precedes verification. The Maturation Stigmergic Protocol's terminal state (per-ASN quiescence) is the input handoff. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

## N

**Narrow → Refine → Verify.** The three-phase cycle every process in the system follows. The primary pattern, rooted in the scientific method. See [Narrow → Refine → Verify](patterns/narrow-refine-verify.md).

**Name (link type).** A substrate-owned link associating a document with a sibling `<stem>.name.md` carrying its canonical human-readable identity (e.g., `CarrierSetDefinition`). One-line file. The string that goes in citation parentheticals (`- T0 (CarrierSetDefinition) — supplies the carrier ℕ`). Edit-in-place mutability; the link survives renames. A renamed name causes parenthetical-mismatch findings across every md citing the renamed claim — the validate-revise machinery sweeps and rewrites. Retraction is reserved for wrong-link cases. See [Relation Shapes](protocols/substrate/shapes.md).

**Note.** A document covering one topic, produced by one inquiry. Contains ~20–40 claims with explicit dependency structure. The format has Dijkstra-EWD lineage: numbered, bounded, self-contained investigations carrying arbitrary formal weight. Serves as the stable interface boundary for discovery-stage consumers; its internal claim set becomes the operational surface for claim-refinement-stage consumers. See [Architecture](architecture.md).

Notes are identified by the legacy prefix `ASN-NNNN` (originally "Abstract Specification Note"), retained opaque for stable addressing across commits, filenames, and cross-references.

**Note maturation.** The note-stage of the [Maturation Stigmergic Protocol](#m): review/revise cycles drive a synthesized note to confirmed stability. Uses the `note` classifier, `citation` link type (note→note dependencies), and `comment.out-of-scope` subtype. Finding classification is REVISE / OUT_OF_SCOPE — there is no OBSERVE at this scale. Out-of-scope findings flag concerns whose resolution lies elsewhere in the lattice and seed lattice operations (extract, absorb, scope promotion). See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Claim derivation.** The stage that decomposes a confirmed note into per-claim documents conforming to the [Claim Document Contract](#c). One fire — the [`claim_decompose`](protocols/agents/producers.md) agent runs once on the source note, emits per-claim Classifier links, label/name sidecars, and `provenance.derivation` per derived claim. The boundary between note maturation and claim refinement; a [representation change](patterns/representation-change.md) (one note → many claim files). Operator-gated within the maturation protocol. See [Claim Derivation](claim-derivation.md); protocol details in [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

## O

**Open surface.** A claim structure that leaves no explicit home for new sub-facts (e.g., "with its standard claims"). Sets the conditions for a [Genesis Attractor](equilibrium/contract-sprawl.md) to form.

**Out-of-scope finding.** A reviewer finding (`comment.out-of-scope`) during note maturation that flags a valid concern whose resolution lies outside the current note. Does not block the convergence predicate. Subscribed to by the [maturation protocol](#m), which routes the finding to one of three lattice operations: absorb (existing home), scope promotion (new inquiry), or extract (new foundation). The off-ramp for the [production drive](design-notes/production-drive.md) at note scale, replacing OBSERVE which is used at claim scale. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Oscillatory failure.** An [equilibrium](equilibrium/) pattern whose force acts at a site of undecidability — two resolutions are both locally valid and nothing in the cycle arbitrates between them. Fixed by establishing the arbitrating criterion (a contract, a convention, or an explicit scope ruling), which varies by subtype. Contrasts with [gravitational failure](#g) and [transitional failure](#t). [Reverse-Course Oscillation](equilibrium/reverse-course-oscillation.md) is the oscillatory pattern documented so far.

**Over-citation.** A Depends entry for a claim the proof doesn't actually use. A form of [Citation Drift](equilibrium/citation-drift.md).

## P

**Passive driver.** See Driver.

**Pattern language.** The patterns that govern how agents produce verified knowledge. See [patterns README](patterns/README.md).

**Per-comment closure predicate.** The substrate predicate evaluated for each `comment.revise` link: does a `resolution` link target this comment? Counts the comment as closed when true. The conjunction over all `comment.revise` links targeting a document is the [convergence predicate](#c) at that document. The same predicate is the termination condition of the [Correction Stigmergic Protocol](#c) primitive. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Producer.** The agent caste that grants new substrate identity — emits new addresses, classifier links, or sidecar documents that didn't exist before. Examples: `note_draft` (synthesizes a note from an inquiry), `claim_decompose` (derives per-claim documents from a confirmed note), `claim_contract` (assigns `contract.<kind>` to a claim), `claim_describe` (emits the description sidecar). Producers are typically operator-gated within the [maturation protocol](#m) — the operator decides when to advance a stage by firing the producer. See [Producers](protocols/agents/producers.md).

**Production drive.** The LLM behavioral force that drives generation of output regardless of whether new output is warranted. Manifests as findings on already-clean material, prose growth without reasoning growth, contract sprawl, and other [Surface Expansion](equilibrium/surface-expansion.md) symptoms. Channeled productively by the OBSERVE off-ramp (claim refinement) and the OUT_OF_SCOPE off-ramp (note maturation) — engagement gets a place to go that doesn't trigger destructive revision. See [Production Drive](design-notes/production-drive.md).

**Prose coinage.** The atomic event of coining a new prose word for a concept no existing vocabulary captures precisely (e.g., "action point," "divergence," "subspace"). Occurs in two modes: [synthesis coinage](#s) and [review coinage](#r). Precedes [prose compression](patterns/prose-compression.md). See [Prose Coinage pattern](patterns/prose-coinage.md).

**Prose compression.** A prose-named concept gets a symbol for compact formal manipulation (e.g., "tumbler addition" → `⊕`). Same concept, compressed form. Produced by [review/revise iteration](patterns/review-revise-iteration.md) as concepts are used frequently enough that compact notation pays for itself. See [Prose Compression pattern](patterns/prose-compression.md).

**Prose Sprawl.** A claim's narrative prose grows across review cycles without corresponding growth in reasoning content. The narrative form of [Surface Expansion](equilibrium/surface-expansion.md). Contained by the [Voice Principle](principles/voice.md) (positive style structure) and finding classification (tightening observations don't reach the reviser). See [Prose Sprawl](equilibrium/prose-sprawl.md).

**Provenance link.** A flat substrate audit link recording structural moves the [maturation protocol](#m) executes. Subtypes: `provenance.extract` (records source notes when material is extracted into a new foundation), `provenance.absorb` (records source when material is moved into an existing note), `provenance.reset` (records cascade when [hard reset](#h) revokes a foundation). Not protocol machinery — not load-bearing for any predicate. Supports replay and structural-history reconstruction. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

## Q

**Quiescence.** The terminal-state condition: every agent's trigger evaluates false at the chosen scope tier (Q0 in `protocols/substrate/quiescence.md`). Scope-parameterized — the maturation protocol can target per-target, per-lattice, or system quiescence (Q7–Q10). Per-claim quiescence: every `comment.revise` on the claim has a matching `resolution`, every audit is fresh, all sidecars are fresh. Per-ASN quiescence: every claim under the source note is locally quiescent. Recognizable from substrate state alone (Q0 RecognizabilityIsUnconditional) — no observer state, no auxiliary metadata. See [Quiescence in the substrate spec](protocols/substrate/quiescence.md).

## R

**Rebase.** Re-verifying downstream claims after a foundation changes. Happens automatically via review/revise cycles because changed dependencies invalidate dependents' metadata.

**Refiner.** The agent caste that closes findings — observes a `comment.revise` and emits a `resolution` link plus the document edit that addresses the finding. Examples: `claim_revise`, `note_revise`, `claim_structural_revise`. Refiners are runner-walked: their triggers fire on observed `comment.revise` links matching their scope. See [Refiners](protocols/agents/refiners.md).

**Representation change.** Progressive transformation of content through different forms (narrative → structured → formal → mechanical) without changing the underlying claim. Each change introduces structural rules at the new form. See [Representation Change pattern](patterns/representation-change.md).

**Resolution (link type).** A substrate link that closes a `comment.revise`. Subtypes: `resolution.edit` (the document was edited to address the finding) or `resolution.reject` (the finding was refused, with a rationale document linked). Once a resolution exists, the per-comment closure predicate counts the comment as resolved — predicates ignore resolved comments. Once emitted, a resolution tuple is permanent in `L_K` (R3 monotonicity); it can be nullified by a [retraction](#r) but not deleted. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Retraction (link type).** A substrate tuple that nullifies a previously-emitted tuple. The retraction's to-set holds the address of the target tuple in `A_rel` — a tuple-to-tuple pointer (R5 self-reference is what makes this expressible). The retracted tuple remains in `L_K` (R3 monotonicity); the active subset `A_K` (R6) excludes any tuple whose address appears in some retraction's to-set. Used by claim refinement to prune stale `citation` links during proof evolution and by note maturation to handle stale citations after absorb/extract. Generalizes to any link type via the same mechanism. Idempotent — duplicate retractions yield the same active set. Shadow semantics: retracting a retraction does not restore the original (the active-subset check is single-depth). See [Relation Shapes — Retraction](protocols/substrate/shapes.md) and [Typed Relations § R6](protocols/substrate/types.md).

**Reverse-Course Oscillation.** An [oscillatory failure](#o) in which a reviser's change in cycle N is undone in cycle N+1 because two locally-valid resolutions exist and the cycle has no shared criterion to pick between them. Subtypes by source of undecidability: contract-absent, judgment-call, exhaustiveness-vs-restraint. Partially contained by finding classification (judgment-call findings become observations and never trigger revision). See [Reverse-Course Oscillation](equilibrium/reverse-course-oscillation.md).

**Review coinage.** [Prose coinage](patterns/prose-coinage.md) that happens during review/revise cycles rather than at synthesis. Occurs in both discovery and claim refinement. Roughly 30% of a note's coinages. Driven by reviewer pressure surfacing a concept the current text is discussing in ad-hoc prose without a shared name. See [Synthesis coinage](#s) for contrast.

**Review (link type / document classifier).** A substrate `review` classifier marks a document as a review record. Comment links from that review attach the findings it produced. Each review cycle produces one review document; comment links accumulate across cycles. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Review/revise iteration.** Repeating cycles of review (finding issues), revision (fixing them), and re-review until convergence. See [Review/Revise Iteration pattern](patterns/review-revise-iteration.md).

**Reviewer.** The agent that reads content and produces findings. Classifies each finding by whether it requires action. Does not modify.

**Reviser.** The agent that reads a finding and modifies the content to address it. Writes in the Dijkstra voice. Always paired with a reviewer.

**Runner.** The scheduling discipline that walks the [agent registry](#a) over substrate state. Reads each agent's trigger predicate, fires the agent when the predicate is true at its scope, observes the emitted tuples, repeats until [quiescence](#q) (every trigger evaluates false). Runner schedule is unspecified — fairness is the only requirement (no agent is starved indefinitely). The runner is part of the substrate's static spec; agents and shapes are the only knobs for protocol authors. See [Runner](protocols/substrate/runner.md).

## S

**Scale.** Scope of a review cycle. Two scopes in current claim refinement: [adaptive scope](#a) (cone — apex plus dependencies, expanded on demand) and [comprehensive scope](#c) (whole note plus full foundation). The legacy three-scale model (local/regional/full) was consolidated to two during V-cycle work; local was retired. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Scientific method.** Lineage of the primary pattern — narrow scope, refine through iteration, verify coherence. Every process in the system follows this rhythm.

**Scope narrowing.** Breaking work into smaller tractable pieces by constraining context. See [Scope Narrowing pattern](patterns/scope-narrowing.md).

**Scope promotion.** Elevating out-of-scope boundary observations into their own first-class investigations. How the lattice grows outward. See [Scope Promotion pattern](patterns/scope-promotion.md).

**Scope quiescence.** [Quiescence](#q) parameterized by scope. Per-claim quiescence: every `comment.revise` on the claim has a matching `resolution`, every audit is fresh, all sidecars are fresh. Per-ASN quiescence: every claim under the source note is locally quiescent. Per-lattice quiescence: every ASN in the lattice is quiescent. Q7–Q10 in the substrate spec define scope-parameterized quiescence formally. The [maturation protocol](#m) terminates at a designated scope tier (typically per-ASN). See [Quiescence](protocols/substrate/quiescence.md).

**Scoped inquiry.** Decomposing a question along authority boundaries, with each channel investigating what it can evaluate. See [Scoped Inquiry pattern](patterns/scoped-inquiry.md).

**Scout.** The agent caste that detects and reports — observes substrate state and emits findings (typically `comment.revise`, `comment.observe`, `comment.out-of-scope`, or audit/review links) without modifying primary content. Examples: `claim_review`, `note_review`, `claim_structural_audit`. Scouts produce the inputs that [refiners](#r) consume. Runner-walked: triggers fire on staleness or coverage signals against substrate state. See [Scouts](protocols/agents/scouts.md).

**Self-healing rebase.** When a foundation claim changes, dependents automatically re-verify through the same narrow → refine → verify cycles that built them.

**Self-Report Laundering.** A failure mode of [self-healing](design-notes/self-healing.md#observation-layer-limitation): an evaluator reads the summaries an LLM process produced about itself (commit messages, stats, finding counts) rather than the artifacts it produced (diffs, code, outputs). The generator's own voice gets re-surfaced to the evaluator as if it were independent evidence. Addressed by the [Audit by Content](design-notes/audit-by-content.md) design rule.

**Self-Review Stigmergic Protocol.** A primitive of the [Stigmergic Protocol](#s) family. Pattern: an agent emits a fact and, in the same fire, emits a self-review (audit) tuple recording the fact's freshness; downstream consumers read the audit; staleness retriggers regeneration. Distinct from [Correction](#c) in that Self-Review audits one's own output rather than another's; common for content-derived attributes (label, name, description sidecars staying in sync with the body). See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Sequential hand-off.** One of two hand-off mechanisms between agents. The downstream agent does not fire on substrate state — an operator-gated trigger (filesystem signal, manual invocation) advances the work. Used at maturation stage transitions where the next stage's preconditions can't be expressed cleanly as a substrate predicate. Contrasts with [stigmergic hand-off](#s). See [agent registry README](protocols/agents/README.md).

**Signal.** A mechanical indicator that a disequilibrium pattern is occurring (e.g., a claim's contract growing across cycles signals [Contract Sprawl](equilibrium/contract-sprawl.md)).

**Sprawl.** See Contract Sprawl, Prose Sprawl, Index Sprawl.

**Stigmergic hand-off.** One of two hand-off mechanisms between agents. The downstream agent's trigger predicate observes substrate facts the upstream agent emitted; firing happens when the runner walks the registry and finds the predicate true. No direct call, no shared state outside the substrate. The dominant hand-off type within the maturation protocol. Contrasts with [sequential hand-off](#s). See [agent registry README](protocols/agents/README.md).

**Stigmergic Protocol.** A protocol family in which agents coordinate by reading and writing a shared substrate, with no direct message passing. Agents observe substrate state, fire when triggers are true, emit tuples; the substrate is the entire communication medium. Cachin's distinction maps as: system model = AG0–AG7 + Run0–Run5; communication primitive = Emit/Observe/Nullify (R0–R7); message format = typed relations under shape constraints (Sh-conf + Sh0–Sh5); termination = [quiescence](#q) (Q0–Q10). The [maturation protocol](#m) is one specialization. Primitives composed within the family: [Correction](#c), [Marker](#m), [Self-Review](#s), [Cycle](#c). See [Protocol Stack overview](protocols/README.md).

**Stigmergy.** Coordination via traces left in a shared environment. Term coined by Pierre-Paul Grassé (1959) in observing how termites coordinate nest construction without direct communication — each modification of the substrate becomes a stimulus for other agents' actions. The substrate-mediated communication model the [Stigmergic Protocol](#s) family adopts. See [Protocol Stack overview](protocols/README.md).

**Structural finding.** A review finding whose root cause is structural rather than semantic — duplicated declarations, dangling references, metadata disagreement, dependency-graph cycles. Symptom of an [Uncontracted Representation Change](equilibrium/uncontracted-representation-change.md).

**Substrate.** The persistent, append-only graph of typed relations on which the protocol stack runs. Properties: tuple identity (R0–R2 — fresh address per emit, injection, permanence), append-only `L_K` (R3), disjoint subspaces `A_doc ⊔ A_rel` (R4), self-reference (R5), active subset (R6 — `A_K = L_K \ {tuples targeted by L_R}`). Operations: `Emit_K` (allocate fresh address, extend `L_K`), `Observe_K` (query against either the active view `A_K` or the audit view `L_K`), `Nullify` (Emit into the retraction relation — not a separate primitive). Shape restrictions (Sh-conf + Sh0–Sh5) constrain which `(F, G)` pairs each typed relation admits. Implementation is filesystem-backed (`_docuverse/`); the spec is implementation-independent. See [Substrate spec](protocols/substrate/README.md).

**Summary.** *Retired.* The 1–3-sentence claim summary previously stored as a YAML field. Replaced by the [description sidecar](#d) (`<stem>.description.md`) and the description Attribute-shape substrate link, maintained by the `claim_describe` agent.

**Surface Expansion.** Across successive review cycles, a claim's textual surface grows monotonically without corresponding growth in reasoning content. The shared mechanism underneath [Contract Sprawl](equilibrium/contract-sprawl.md), [Prose Sprawl](equilibrium/prose-sprawl.md), and [Index Sprawl](equilibrium/index-sprawl.md). Contained by the [Voice Principle](principles/voice.md) (constrains what the reviser writes) and finding classification (constrains what reaches the reviser). See [Surface Expansion](equilibrium/surface-expansion.md).

**Synthesis.** The step integrating theory-channel and evidence-channel outputs into a structured note with dependency-mapped claims. The first place both perspectives meet — agreements validate, disagreements seed new hypotheses. Roughly 70% of a note's vocabulary coinage happens here. See [Two-Channel Architecture](two-channel-architecture.md).

**Synthesis (link type).** A substrate `provenance.synthesis` link records that consultation produced a note from an inquiry. From = inquiry, to = note. Provenance trail from the inquiry to its synthesized output. Filed by the [`note_draft`](protocols/agents/producers.md) agent during the inquiry-consultation stage of the maturation protocol. Sibling of `provenance.derivation`, `provenance.extract`, `provenance.absorb`, `provenance.reset`. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Synthesis coinage.** [Prose coinage](patterns/prose-coinage.md) that occurs at the synthesis step when two-channel outputs are reconciled. Roughly 70% of a note's coinages happen here, because synthesis is where incompatible vocabularies must be merged into a single note and no existing word may fit precisely. Contrasts with [review coinage](#r) which happens during later review/revise cycles.

## T

**Theorem.** A claim classified as a proven result.

**Theory channel.** The agent channel that consults established theory (design documents, domain models) and makes predictions. Forbidden from referring to specific evidence. Its question generator sees a vocabulary list of the framework's own terms (vocabulary-in-prompt) because theory space is conceptual and listable. See [Two-Channel Architecture](two-channel-architecture.md).

**Transition condition.** What the maturation protocol evaluates to decide a representation is ready to advance to the next stage. Each transition has a readiness signal (predicate truth or sustained quiet) and a handoff artifact. Transitions: discovery→claim derivation (note `is_doc_quiescent` ∧ `is_claim_confirmed`), claim derivation→claim refinement ([Claim Document Contract](#c) validates), claim refinement→verification (per-claim quiescence ∧ coverage), verification→done. See [Maturation Stigmergic Protocol](protocols/maturation/note-to-claim.md).

**Transitional failure.** An [equilibrium](equilibrium/) pattern whose force acts at a representation boundary introduced by a stage transition. Fixed once per boundary (by specifying and enforcing the output contract that the transition introduces); recurs at every new boundary because producing is easier than specifying. Contrasts with [gravitational failure](#g) and [oscillatory failure](#o). [Uncontracted Representation Change](equilibrium/uncontracted-representation-change.md) is the transitional pattern documented so far.

**Two-channel architecture.** The mechanism that produces new knowledge for the lattice. Two independent agent channels (theory and evidence) investigate a question under enforced vocabulary separation. A synthesis agent integrates their outputs into a structured note. The note then enters [note maturation](#n) for review/revise cycles. The architecture governs how the initial note is generated, not how it matures. See [Two-Channel Architecture](two-channel-architecture.md).

**Type.** A claim's structural classification — `axiom`, `definition`, `design-requirement`, `lemma`, `theorem`, `corollary`, `consequence`. Reified as a `contract.<kind>` Classifier link in the substrate. Set by the [`claim_contract`](protocols/agents/producers.md) agent.

## U

**Uncontracted Representation Change.** A [transitional failure](#t) at a [representation change](patterns/representation-change.md) where a stage introduces a new unit of structure without specifying what well-formed output means. The structure lands on disk, but no contract says what must hold, and downstream reviewers spend cycles on symptoms of unnamed violations. See [Uncontracted Representation Change](equilibrium/uncontracted-representation-change.md).

**Under-citation.** A proof uses a claim that its Depends list doesn't include. The most common form of [Citation Drift](equilibrium/citation-drift.md).

## V

**Validate-before-review.** The pattern of running a mechanical structural-invariant check (validator + per-invariant fix recipes) before each review cycle, so the LLM reviewer sees structurally sound state and spends its cycles on semantic issues. See [Validate Before Review](patterns/validate-before-review.md) and [design note](design-notes/validate-before-review.md).

**Validation Principle.** Design commitment that every representation the system operates on must have a structural contract, and no LLM review cycle operates on state that has not been mechanically verified against that contract. Uses enumeration because structural invariants are a closed, mechanically checkable set. Sibling to the [Coupling Principle](principles/coupling.md) and [Voice Principle](principles/voice.md). See [The Validation Principle](principles/validation.md).

**Validator.** Mechanical check (pure code, no LLM) of a representation's structural invariants against its contract. Exhaustive and cheap; free of the add-bias that compromises LLM-based structural fixes.

**Verify the whole.** Stepping back to original scope after narrowing, to check that the refined pieces cohere. See [Verify the Whole pattern](patterns/verify-the-whole.md).

**Vocabulary (claim).** Per-claim formal-symbol dictionary (introduces / removes declarations). Lives in the signature sidecar (`<stem>.signature.md`) and is reified to substrate via the signature Attribute-shape link. Maintained by the [`claim_signature_resolve`](protocols/agents/producers.md) agent.

**Vocabulary bridge.** See Bridge vocabulary.

**Vocabulary firewall.** See Firewall, vocabulary.

**Voice Principle.** Design commitment that LLM output is constrained by defining what well-formed output looks like (positive style structure), not by enumerating what it must avoid. The Dijkstra voice — prose with embedded formalism, every statement justified in the sentence that introduces it — leaves no slot for non-reasoning prose. Enumerated prohibition lists leave gaps the agent drifts through. Uses positive definition because prose quality is an open set that can't be enumerated. Sibling to the [Coupling Principle](principles/coupling.md) and [Validation Principle](principles/validation.md). See [The Voice Principle](principles/voice.md).

## Y

**YAML.** *Retired.* Earlier versions of the system stored per-claim metadata (label, name, type, summary, depends, vocabulary) in sibling `.yaml` files. The substrate migration replaced this with attribute-sidecar documents and Classifier links — see [Metadata](#m). Operator-side artifacts (lattice config, spec drops in `_workspace/`) still use YAML frontmatter; per-claim metadata files do not.