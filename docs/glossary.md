# Glossary

Terms specific to this reasoning system. Cross-references point to where each term is discussed substantively.

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [Y](#y)

## A

**Accretion.** Growth of the lattice by adding new claims rather than mutating existing ones. The discipline that prevents [Contract Sprawl](equilibrium/contract-sprawl.md). See [Accretion pattern](patterns/accretion.md).

**Active links.** A substrate query that returns only links not nullified by a retraction. The `ActiveLinks` operation performs the two-step subtraction: fetch matching links, exclude any whose id appears as the target of a `retraction` link. Counterpart to `FindLinks`, which returns all matching links including retracted ones. Convergence predicates and dependency-graph queries use `ActiveLinks` so retracted citations and resolutions don't count. Currently implemented as a protocol-layer helper (`scripts/lib/store/queries.py::active_links`); planned as a substrate operation. See [Substrate Module](protocols/substrate.md).

**Adaptive scope.** A claim convergence scope strategy where context grows on demand — the reviewer requests missing references, the scope assembler expands the cone, the review re-runs. Catches within-cone issues efficiently without preloading the whole foundation. Counterpart to [comprehensive scope](#c). A choreography decision, not a protocol-level construct. See [Claim Convergence Protocol](protocols/claim-convergence-protocol.md).

**Apex (cone apex).** The high-dependency claim at the center of a [dependency cone](patterns/dependency-cone.md) — the one that keeps getting revised while its dependencies remain stable.

**Assembly.** The stage that exports converged claims into `formal-statements.md` and `dependency-graph.yaml` for downstream consumers. Mechanical, no LLM.

**Attractor, Genesis.** A claim that becomes the default home for every fact anyone needs about a concept it introduces. Cause of [Contract Sprawl](equilibrium/contract-sprawl.md).

**Authority.** A source the reasoning system consults — for example, Nelson's design documents (theory authority) or Gregory's implementation (evidence authority). See [Two-Channel Architecture](two-channel-architecture.md).

**Axiom.** A claim classified as assumed rather than derived. Stated without proof.

## B

**Boundary observation.** An out-of-scope finding captured during investigation — enough context to seed a new investigation without expanding the current one. Seed for [scope promotion](patterns/scope-promotion.md).

**Bridge citation.** A citation to a claim that licenses an inference step between two other concepts in a proof. Missing bridge citations are a subtype of [Citation Drift](equilibrium/citation-drift.md#subtype-bridge-citations).

**Bridge vocabulary.** The unified terms that make a campaign's two channels speak coherently. Curated at campaign creation time, not emergent. Campaign-level because it bridges two specific channels — different pairings produce different bridges. The primary consumer is the reviewer during note convergence, who must interpret claims against both channels' terminology. See [Two-Channel Architecture](two-channel-architecture.md).

## C

**Campaign.** Binds a theory channel and an evidence channel to a target and a bridge vocabulary. The operational unit of coordinated investigation. The channel pairing is immutable per campaign — any channel change means a new campaign with a new vocabulary. Ends when its question is answered (verified attachment) or abandoned (negative result). Scope promotion during review spawns additional inquiries within the same campaign; genuinely new questions spawn new campaigns. See [Architecture](architecture.md).

**Channel.** A self-contained plugin holding source content, consultation code, consultation prompts, and metadata. Channels are named identities in a flat top-level namespace (`channels/`). Each channel exposes a two-function interface: `generate_questions` (decompose an inquiry into channel-appropriate sub-questions) and `consult` (answer a single question from the channel's corpus). Internal implementation is the channel's business. Campaigns reference channels by name. See [Architecture](architecture.md).

**Channel asymmetry.** Shape-mismatch between the theory channel and the evidence channel. Theory space is conceptual and listable (vocabulary-in-prompt). Evidence space is specific and must be seen (corpus-in-prompt). Prevents naive merging and forces synthesis to coin bridging vocabulary. See [Channel Asymmetry pattern](patterns/channel-asymmetry.md).

**Choreography.** How a protocol's predicate is driven true in practice — which scope to use, what order to review in, when to alternate strategies, what to assemble as context. Distinguished from the [protocol](#p) itself, which defines only the predicate. Different choreographies satisfy the same predicate. The protocol IS the predicate; everything else is choreography. See [Claim Convergence Protocol](protocols/claim-convergence-protocol.md).

**Citation, inline.** A reference in the proof narrative like "by NAT-wellorder." Part of proof content, not metadata.

**Citation (link type).** The substrate link that records a dependency between two reasoning units — claim→claim during claim convergence, note→note during note convergence. The lattice edge. Distinct from [inline citation](#c) (proof-narrative reference). A citation may be nullified by a [retraction](#r) link pointing at it; the substrate retains both, and `active_links` queries return only un-retracted citations. See [Convergence Protocol](protocols/convergence-protocol.md).

**Claim.** A single unit of reasoning within a note. An assertion — something the system says is the case, which can be verified, contested, or refuted. Has a label, type, formal contract, and dependencies. The atomic lattice node. See [Architecture](architecture.md).

**Claim convergence.** The stage that takes per-claim files from note decomposition and runs review/revise cycles until each claim's reasoning is sound. Not cleanup — discovery under precision constraint. Scope narrowing to per-claim files is itself epistemically productive. See [Claim Convergence](claim-convergence.md); protocol details in [Claim Convergence Protocol](protocols/claim-convergence-protocol.md).

**Claim File Contract.** The structural contract specifying what well-formed per-claim file state looks like after note decomposition. Concrete rules, mechanically checkable: one body per file, filename matches label, references resolve, metadata agrees with content, no dependency cycles. The first instance of the output contract the [Validation Principle](principles/validation.md) requires. See [Claim File Contract](design-notes/claim-file-contract.md).

**Comment (link type).** A substrate link recording a reviewer finding on a document. Subtypes carry the classification: `comment.revise` requires resolution and participates in the [convergence predicate](#c); `comment.observe` is a non-blocking observation (claim convergence only); `comment.out-of-scope` is a non-blocking signal that the lattice needs structural work (note convergence only). See [Convergence Protocol](protocols/convergence-protocol.md).

**Cone, dependency.** A cluster of tightly coupled claims where an apex keeps being revised while dependencies are stable. See [Dependency Cone pattern](patterns/dependency-cone.md).

**Cone-review.** Focused review of a specific dependency cone — apex claim plus its declared dependencies as context. Resolves the cluster as a constraint system. The operational name for cone-scoped review under [adaptive scope](#a) in the [claim convergence protocol](protocols/claim-convergence-protocol.md).

**Cone-sweep.** Proactive walking of the dependency DAG bottom-up, running cone-review on every apex meeting the dependency-frequency threshold. Implemented in `scripts/cone-sweep.py`. A choreography that satisfies the protocol's coverage obligation by exhausting the apex set.

**Comprehensive scope.** A claim convergence scope strategy where the entire note (or full cone) is loaded into review context before the review runs. Catches cross-cone issues that adaptive scope can miss — vocabulary collisions, citation inconsistencies between dependency clusters, gaps invisible to within-cone reasoning. Counterpart to [adaptive scope](#a). A choreography decision, not a protocol-level construct. See [Claim Convergence Protocol](protocols/claim-convergence-protocol.md).

**Consult authority.** During revision, return to source material to ground findings in evidence. See [Consult Authority pattern](patterns/consult-authority.md).

**Convergence predicate.** The graph property that defines when a document set has converged: every `comment.revise` link targeting a document in the set has a matching `resolution` link. Document-type-neutral. Both note convergence and claim convergence use this same predicate. See [Convergence Protocol](protocols/convergence-protocol.md).

**Convergence protocol.** The document-type-neutral module specifying the convergence predicate, the comment/resolution link types, and the safety/liveness properties any review/revise process must satisfy. Specialized by [note convergence](#n) (for notes during discovery) and [claim convergence](#c) (for claims after note decomposition). See [Convergence Protocol](protocols/convergence-protocol.md).

**Consultation protocol.** The protocol that produces an initial note from a campaign-bound inquiry. Two independent channels (theory and evidence) consult under enforced vocabulary separation; a synthesizer integrates their outputs into a structured note. [Production-shaped](#p) — one-shot, terminates on output production. Upstream producer for [note convergence](#n). Safety properties include the vocabulary firewall, channel independence, channel discipline, channel asymmetry, synthesis integrity, and provenance recording. See [Consultation Protocol](protocols/consultation-protocol.md).

**Content.** What the `.md` file holds — narrative, proof, formal contract claims. Distinct from metadata.

**Contract, formal.** The structured claim section of a claim (`*Formal Contract:*`): preconditions, postconditions, invariants, axiom, definition. Part of content.

**Contract (link type).** A substrate link classifying a claim by structural kind: `contract.axiom`, `contract.definition`, `contract.theorem`, `contract.corollary`, `contract.lemma`, `contract.consequence`, `contract.design-requirement`. Subtypes name structurally distinct kinds with different required fields. See [Claim Convergence Protocol](protocols/claim-convergence-protocol.md).

**Coverage.** The choreography's obligation to actually conduct reviews at sufficient scope. The [convergence predicate](#c) is trivially satisfied when no reviews have happened — the protocol says "all filed concerns are addressed," not "sufficient examination has occurred." Coverage is what closes that gap. A protocol-level non-guarantee; a choreography-level requirement. See [Claim Convergence Protocol](protocols/claim-convergence-protocol.md).

**Contract Sprawl.** A claim's formal contract keeps growing across cycles because it is a [Genesis Attractor](equilibrium/contract-sprawl.md). See [Contract Sprawl](equilibrium/contract-sprawl.md).

**Corollary.** A claim classified as an immediate consequence of another.

**Coupling Principle.** Design commitment that prose and formal content are authored as a pair at an artifact-specific ratio (90/10 for notes, 70/30 for claim files). Divergence from the ratio signals decoupling — one surface growing without the other. Prose is the generative substrate; formal notation precipitates from it. Too much prose fails loudly (hand-waving). Too much formal fails silently (discovery stops). One of three principles forming the quality boundary for review. See [The Coupling Principle](principles/coupling.md).

## D

**Decomposition (link type).** A substrate `decomposition` link records that note decomposition produced a claim from a note. From = note, to = claim. Provenance trail from a note to each of its decomposed claim files. Filed by the note decomposition protocol. See [Note Decomposition Protocol](protocols/note-decomposition-protocol.md).

**Definition.** A claim classified as introducing named concepts or operations.

**Depends (YAML).** The structured dependency list in a claim's YAML file. The authoritative metadata for dependencies.

**Description (link type).** A substrate-owned link associating a document with a sibling `<stem>.description.md` carrying its prose summary. Multi-line markdown content. The substrate's three document-attribute types (`label`, `name`, `description`) share a structure: typed link from the document to a sibling attribute doc, edited in place when the value changes, link survives content updates. Stage-1 mutability: the doc is overwritten on edit; document-level history will be Xanadu's job at the cut. Retraction is reserved for wrong-link cases, not value updates. See [Substrate Module §4](protocols/substrate.md).

**Design requirement.** A claim classified as an architectural or measurement constraint the system imposes.

**Discovery.** The first stage. Combines three mechanisms to bring new knowledge into the lattice: the [two-channel architecture](two-channel-architecture.md) generates an initial note from independent theory and evidence channels; the [note convergence protocol](protocols/note-convergence-protocol.md) drives the note to stability through review/revise cycles; the [maturation protocol](protocols/maturation-protocol.md) executes the lattice operations (extract, absorb, scope promotion) that discovery's findings trigger. See [Discovery](discovery.md).

**Domain.** The logical configuration of a lattice — which verifier, which channels, which vocabulary firewall. Expressed in `lattices/<L>/config.yaml`, not as a separate directory. Two configurations that differ in any binding are different domains. The domain is what you swap to move the engine from one subject area to another. See [Architecture](architecture.md).

**Drift, Citation.** The state where citations (YAML depends + inline prose) no longer match the dependencies a proof actually uses. See [Citation Drift](equilibrium/citation-drift.md).

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

**Finding classification.** The reviewer's classification of each finding by how it should be handled. Two binary schemes apply at different scales. **Note convergence** uses REVISE / OUT_OF_SCOPE — REVISE must fix in-note; OUT_OF_SCOPE signals maturation that adjacent material is missing or misplaced. **Claim convergence** uses REVISE / OBSERVE — REVISE must fix; OBSERVE logs the observation without triggering revision. Both schemes prevent [Surface Expansion](equilibrium/surface-expansion.md) by keeping non-correctness findings from reaching the reviser. See [Note Convergence Protocol](protocols/note-convergence-protocol.md), [Claim Convergence Protocol](protocols/claim-convergence-protocol.md).

**Firewall, vocabulary.** Structural enforcement that the theory channel cannot use evidence-channel terms and vice versa. Prevents the LLM's training knowledge from shortcutting reasoning. See [Two-Channel Architecture](two-channel-architecture.md).

**Formal-statements export.** Curated export containing all claim summaries and formal contracts in dependency order. Consumed by downstream notes as foundation.

**Foundation.** From a downstream note's perspective, any upstream note it depends on. Foundation content is read-only context for the downstream's review cycles.

**Full-review.** Review reading an entire note's claim set at once. The operational name for review under [comprehensive scope](#c). Finds issues invisible to cone-scoped review: carrier-set conflation, precondition chain gaps, vocabulary collisions, issues in small claims that adaptive scope didn't reach.

**Full scale.** Legacy name for [comprehensive scope](#c) — review of the whole note with full foundation context.

## G

**Genesis Attractor.** See Attractor, Genesis.

**Gravitational failure.** An [equilibrium](equilibrium/) pattern whose force acts continuously across review cycles. Requires permanent discipline — prompt framing, coupling monitoring, voice structure — not a one-time fix. Contrasts with [transitional failure](#t) and [oscillatory failure](#o). Contract Sprawl, Prose Sprawl, Surface Expansion, Index Sprawl, Citation Drift are gravitational.

**Ground state.** The state of genuine convergence — both [adaptive-scope](#a) (cone) and [comprehensive-scope](#c) review agree there are no remaining issues, and the [convergence predicate](#c) holds. Distinguished from "stopped" (no finding at one scope but the other can still expose issues). See [Claim Convergence Protocol](protocols/claim-convergence-protocol.md).

## H

**Hard reset.** A defined operation in the [maturation protocol](#m) for the case where a foundation turns out to be wrong, not merely incomplete. The note re-enters discovery; its freeze is revoked; all dependents that entered claim convergence against its claims must also reset. A `provenance.reset` link records the cascade. Expensive and destructive — used when the alternative (leaving dependents on a known-bad foundation) is worse. See [Maturation Protocol](protocols/maturation-protocol.md).

**Hypothesis cluster.** A [cone](patterns/dependency-cone.md) in a science domain: apex (hypothesis statement) plus its supporting dependencies (axioms, definitions, data citations, coined concepts). Convergence of a hypothesis cluster under [adaptive scope](#a) = hypothesis ready for its scope.

**Hypothesis space.** The space of candidate principles and concepts that could organize a domain. Explored by the theory channel. Complement to [evidence space](#e). New [prose coinage](patterns/prose-coinage.md) is a form of hypothesis generation.

## I

**Index Sprawl.** Enumerative prose that grows across review cycles — lists of use-sites, exhaustiveness claims, bundling inventories. The enumerative form of [Surface Expansion](equilibrium/surface-expansion.md). See [Index Sprawl](equilibrium/index-sprawl.md).

**Inquiry.** One initial question that produces one note. 1:1 relationship with the note. A campaign spawns one or more inquiries. The unit of two-channel discovery: theory-channel and evidence-channel sub-questions are derived from it, consulted independently, synthesized into a single note. See [Architecture](architecture.md).

**Internal driver.** See Driver.

## J

**Join.** Lattice operation. A new node is created above multiple foundations. [Scope promotion](patterns/scope-promotion.md) executes a join.

## L

**Label.** A claim's stable citable handle (e.g., `T0`, `NAT-wellorder`, `TA-Pos`). Set at note decomposition, never changes.

**Label (link type).** A substrate-owned link associating a document with a sibling `<stem>.label.md` carrying its short address (the [label](#l) string). One-line file. The substrate-native home for what is currently the filename-stem convention (filenames will not exist in Xanadu). Edit-in-place mutability: renaming a label edits the doc; the link survives. Retraction is reserved for wrong-link cases. See [Substrate Module §4](protocols/substrate.md).

**Lattice.** The coverage target that campaigns build toward: an accumulated verified dependency graph for one subject-area focus. The lattice operates at two granularities simultaneously: during discovery, notes declare note-level dependencies (`depends:`); during claim convergence, claims declare claim-level dependencies (`follows_from:`). Which granularity a consuming note sees depends on the consumer's stage. Notes retire gradually as their consumers enter claim convergence; the terminal lattice is all claim-to-claim edges with note groupings as provenance metadata. See [Architecture](architecture.md).

**Lattice operation.** Collective term for the three structural operations the [maturation protocol](#m) executes on lattice signals: **extract** (claims move down, into a new foundation below consumers), **absorb** (claims move toward natural home, into an existing note), **scope promotion** (questions move out, opening a new inquiry). Distinct from convergence — operations reshape the lattice; convergence stabilizes content within fixed structure. Triggered by signals from note convergence (duplicate derivations, `comment.out-of-scope` findings). See [Maturation Protocol](protocols/maturation-protocol.md).

**Lemma.** A claim classified as an intermediate result supporting higher-level theorems.

**Local-review.** *Retired.* Single-claim review was retired during V-cycle consolidation when [adaptive scope](#a) (cone) and [comprehensive scope](#c) were found sufficient to expose all classes of finding. See [Claim Convergence Protocol](protocols/claim-convergence-protocol.md).

**Local scale.** *Retired.* See [Local-review](#l).

## M

**Markdown body (`.md`).** The file that holds a claim's content: narrative, proof, formal contract.

**Maturation protocol.** The meta-protocol that supervises stage protocols and executes lattice operations. Drives content from question to verified knowledge through note convergence, note decomposition, claim convergence, and verification. Owns the three lattice operations (extract, absorb, scope promotion) and the transition conditions between stages. Reaches [quiescence](#q), not convergence — settles when no transitions or operations are pending. See [Maturation Protocol](protocols/maturation-protocol.md).

**Meet.** Lattice operation. A concept shared by two nodes is extracted into a new foundation layer below both. [Extract/absorb](patterns/extract-absorb.md) executes a meet.

**Metadata.** What the YAML file holds — label, name, type, summary, depends, vocabulary. Describes the claim; does not constitute its reasoning.

**Modeling.** The stage translating formal contracts into mechanically verifiable code (Dafny, Alloy). Follows claim convergence. Part of the verification protocol's input phase. See [Maturation Protocol](protocols/maturation-protocol.md).

## N

**Narrow → Refine → Verify.** The three-phase cycle every process in the system follows. The primary pattern, rooted in the scientific method. See [Narrow → Refine → Verify](patterns/narrow-refine-verify.md).

**Name (link type).** A substrate-owned link associating a document with a sibling `<stem>.name.md` carrying its canonical human-readable identity (e.g., `CarrierSetDefinition`). One-line file. The string that goes in citation parentheticals (`- T0 (CarrierSetDefinition) — supplies the carrier ℕ`). Edit-in-place mutability; the link survives renames. A renamed name causes parenthetical-mismatch findings across every md citing the renamed claim — the validate-revise machinery sweeps and rewrites. Retraction is reserved for wrong-link cases. See [Substrate Module §4](protocols/substrate.md).

**Note.** A document covering one topic, produced by one inquiry. Contains ~20–40 claims with explicit dependency structure. The format has Dijkstra-EWD lineage: numbered, bounded, self-contained investigations carrying arbitrary formal weight. Serves as the stable interface boundary for discovery-stage consumers; its internal claim set becomes the operational surface for claim-convergence-stage consumers. See [Architecture](architecture.md).

Notes are identified by the legacy prefix `ASN-NNNN` (originally "Abstract Specification Note"), retained opaque for stable addressing across commits, filenames, and cross-references.

**Note convergence.** The protocol that drives notes to convergence through review/revise cycles within discovery. Specializes the [convergence protocol](#c) with `note` classifier, `citation` link type (note→note dependencies), and `comment.out-of-scope` subtype. Finding classification is REVISE / OUT_OF_SCOPE — there is no OBSERVE at this scale. Out-of-scope findings signal the [maturation protocol](#m) that adjacent material is missing or misplaced. See [Note Convergence Protocol](protocols/note-convergence-protocol.md).

**Note decomposition.** The stage protocol that decomposes a converged note into per-claim file pairs (YAML metadata + Markdown body) conforming to the [Claim File Contract](#c). [Production-shaped](#p) — one-shot, terminates when the structural contract holds. The boundary between note convergence and claim convergence; a [representation change](patterns/representation-change.md) (one note → many claim files). See [Note Decomposition](note-decomposition.md); protocol details in [Note Decomposition Protocol](protocols/note-decomposition-protocol.md).

## O

**Open surface.** A claim structure that leaves no explicit home for new sub-facts (e.g., "with its standard claims"). Sets the conditions for a [Genesis Attractor](equilibrium/contract-sprawl.md) to form.

**Out-of-scope finding.** A reviewer finding (`comment.out-of-scope`) during note convergence that flags a valid concern whose resolution lies outside the current note. Does not block the convergence predicate. Subscribed to by the [maturation protocol](#m), which routes the finding to one of three lattice operations: absorb (existing home), scope promotion (new inquiry), or extract (new foundation). The off-ramp for the [production drive](design-notes/production-drive.md) at note scale, replacing OBSERVE which is used at claim scale. See [Note Convergence Protocol](protocols/note-convergence-protocol.md).

**Oscillatory failure.** An [equilibrium](equilibrium/) pattern whose force acts at a site of undecidability — two resolutions are both locally valid and nothing in the cycle arbitrates between them. Fixed by establishing the arbitrating criterion (a contract, a convention, or an explicit scope ruling), which varies by subtype. Contrasts with [gravitational failure](#g) and [transitional failure](#t). [Reverse-Course Oscillation](equilibrium/reverse-course-oscillation.md) is the oscillatory pattern documented so far.

**Over-citation.** A Depends entry for a claim the proof doesn't actually use. A form of [Citation Drift](equilibrium/citation-drift.md).

## P

**Passive driver.** See Driver.

**Pattern language.** The patterns that govern how agents produce verified knowledge. See [patterns README](patterns/README.md).

**Production drive.** The LLM behavioral force that drives generation of output regardless of whether new output is warranted. Manifests as findings on already-clean material, prose growth without reasoning growth, contract sprawl, and other [Surface Expansion](equilibrium/surface-expansion.md) symptoms. Channeled productively by the OBSERVE off-ramp (claim convergence) and the OUT_OF_SCOPE off-ramp (note convergence) — engagement gets a place to go that doesn't trigger destructive revision. See [Production Drive](design-notes/production-drive.md).

**Production protocol.** A protocol shape — one-shot, terminates on output production rather than iterating toward a graph predicate. Safety properties are output contracts plus invariants on the running execution. [Consultation](#c) and [note decomposition](#n) are production protocols. Distinct from [convergence-shaped](#c) protocols (note convergence, claim convergence) which iterate. The shape is implicit in the protocol name — readers see "consultation" or "decomposition" and know it produces; readers see "convergence" and know it iterates. See [protocols README](protocols/README.md#two-protocol-shapes).

**Prose coinage.** The atomic event of coining a new prose word for a concept no existing vocabulary captures precisely (e.g., "action point," "divergence," "subspace"). Occurs in two modes: [synthesis coinage](#s) and [review coinage](#r). Precedes [prose compression](patterns/prose-compression.md). See [Prose Coinage pattern](patterns/prose-coinage.md).

**Prose compression.** A prose-named concept gets a symbol for compact formal manipulation (e.g., "tumbler addition" → `⊕`). Same concept, compressed form. Produced by [review/revise iteration](patterns/review-revise-iteration.md) as concepts are used frequently enough that compact notation pays for itself. See [Prose Compression pattern](patterns/prose-compression.md).

**Prose Sprawl.** A claim's narrative prose grows across review cycles without corresponding growth in reasoning content. The narrative form of [Surface Expansion](equilibrium/surface-expansion.md). Contained by the [Voice Principle](principles/voice.md) (positive style structure) and finding classification (tightening observations don't reach the reviser). See [Prose Sprawl](equilibrium/prose-sprawl.md).

**Provenance link.** A flat substrate audit link recording structural moves the [maturation protocol](#m) executes. Subtypes: `provenance.extract` (records source notes when material is extracted into a new foundation), `provenance.absorb` (records source when material is moved into an existing note), `provenance.reset` (records cascade when [hard reset](#h) revokes a foundation). Not protocol machinery — not load-bearing for any predicate. Supports replay and structural-history reconstruction. See [Maturation Protocol](protocols/maturation-protocol.md).

## Q

**Quiescence.** The stopping condition of the [maturation protocol](#m): no transition conditions are met and no lattice operation signals are pending. Different from convergence (a graph property that becomes true) and different from pure dispatch (fire once and done). Maturation iterates without converging in the predicate sense — it settles. See [Maturation Protocol](protocols/maturation-protocol.md).

## R

**Rebase.** Re-verifying downstream claims after a foundation changes. Happens automatically via review/revise cycles because changed dependencies invalidate dependents' metadata.

**Representation change.** Progressive transformation of content through different forms (narrative → structured → formal → mechanical) without changing the underlying claim. Each change introduces structural rules at the new form. See [Representation Change pattern](patterns/representation-change.md).

**Resolution (link type).** A substrate link that closes a `comment.revise`. Subtypes: `resolution.edit` (the document was edited to address the finding) or `resolution.reject` (the finding was refused, with a rationale document linked). Once a resolution exists, the predicate counts the comment as resolved — the convergence predicate ignores resolved comments. Once created, a resolution link is permanent (it can be nullified by a [retraction](#r) but never deleted). See [Convergence Protocol](protocols/convergence-protocol.md).

**Retraction (link type).** A flat top-level substrate link that nullifies a previously-filed link. The retraction's `to_set` holds the **link id** of the link being retracted (link-to-link pointer), not a document path. This makes retraction structural: it points at one specific link, not at an endpoint pair. Defined at the substrate layer (one of the substrate-owned link types — see [Substrate Module §4](protocols/substrate.md)); used by claim convergence to prune stale `citation` links during proof evolution and by note convergence to handle stale citations after absorb/extract. Generalizes to any link type via the same mechanism (resolutions, provenance moves, etc.). The retracted link remains in the substrate (SUB1 permanence is preserved); graph queries use the substrate's `ActiveLinks` operation to subtract retracted ids. Idempotent — duplicate retractions are harmless because the set subtraction computes the same active set (SUB6). Shadow semantics: retracting a retraction does not restore the original link (SUB5). See [Substrate Module](protocols/substrate.md) for the formal specification.

**Reverse-Course Oscillation.** An [oscillatory failure](#o) in which a reviser's change in cycle N is undone in cycle N+1 because two locally-valid resolutions exist and the cycle has no shared criterion to pick between them. Subtypes by source of undecidability: contract-absent, judgment-call, exhaustiveness-vs-restraint. Partially contained by finding classification (judgment-call findings become observations and never trigger revision). See [Reverse-Course Oscillation](equilibrium/reverse-course-oscillation.md).

**Review coinage.** [Prose coinage](patterns/prose-coinage.md) that happens during review/revise cycles rather than at synthesis. Occurs in both discovery and claim convergence. Roughly 30% of a note's coinages. Driven by reviewer pressure surfacing a concept the current text is discussing in ad-hoc prose without a shared name. See [Synthesis coinage](#s) for contrast.

**Review (link type / document classifier).** A substrate `review` classifier marks a document as a review record. Comment links from that review attach the findings it produced. Each review cycle produces one review document; comment links accumulate across cycles. See [Convergence Protocol](protocols/convergence-protocol.md).

**Review/revise iteration.** Repeating cycles of review (finding issues), revision (fixing them), and re-review until convergence. See [Review/Revise Iteration pattern](patterns/review-revise-iteration.md).

**Reviewer.** The agent that reads content and produces findings. Classifies each finding by whether it requires action. Does not modify.

**Reviser.** The agent that reads a finding and modifies the content to address it. Writes in the Dijkstra voice. Always paired with a reviewer.

## S

**Scale.** Scope of a review cycle. Two scopes in current claim convergence: [adaptive scope](#a) (cone — apex plus dependencies, expanded on demand) and [comprehensive scope](#c) (whole note plus full foundation). The legacy three-scale model (local/regional/full) was consolidated to two during V-cycle work; local was retired. See [Claim Convergence Protocol](protocols/claim-convergence-protocol.md).

**Scientific method.** Lineage of the primary pattern — narrow scope, refine through iteration, verify coherence. Every process in the system follows this rhythm.

**Scope narrowing.** Breaking work into smaller tractable pieces by constraining context. See [Scope Narrowing pattern](patterns/scope-narrowing.md).

**Scope promotion.** Elevating out-of-scope boundary observations into their own first-class investigations. How the lattice grows outward. See [Scope Promotion pattern](patterns/scope-promotion.md).

**Scoped inquiry.** Decomposing a question along authority boundaries, with each channel investigating what it can evaluate. See [Scoped Inquiry pattern](patterns/scoped-inquiry.md).

**Self-healing rebase.** When a foundation claim changes, dependents automatically re-verify through the same narrow → refine → verify cycles that built them.

**Self-Report Laundering.** A failure mode of [self-healing](design-notes/self-healing.md#observation-layer-limitation): an evaluator reads the summaries an LLM process produced about itself (commit messages, stats, finding counts) rather than the artifacts it produced (diffs, code, outputs). The generator's own voice gets re-surfaced to the evaluator as if it were independent evidence. Addressed by the [Audit by Content](design-notes/audit-by-content.md) design rule.

**Signal.** A mechanical indicator that a disequilibrium pattern is occurring (e.g., a claim's contract growing across cycles signals [Contract Sprawl](equilibrium/contract-sprawl.md)).

**Sprawl.** See Contract Sprawl, Prose Sprawl, Index Sprawl.

**Stage protocol.** A protocol that drives one representation toward completion within the [maturation protocol](#m). Four stage protocols: [note convergence](#n), [note decomposition](#n), [claim convergence](#c), verification. Each has its own participants, exchange format, and termination criterion (a convergence predicate or an output contract, depending on shape). The maturation protocol supervises transitions between them. Distinct from the meta-protocol that supervises them, and from [consultation](#c) which is note convergence's upstream producer rather than a stage protocol. See [Maturation Protocol](protocols/maturation-protocol.md).

**Structural finding.** A review finding whose root cause is structural rather than semantic — duplicated declarations, dangling references, metadata disagreement, dependency-graph cycles. Symptom of an [Uncontracted Representation Change](equilibrium/uncontracted-representation-change.md).

**Substrate.** The persistent, append-only graph of documents and typed links between them. Provides the operational foundation every protocol builds on: link permanence (SUB1 — no link is ever removed), query soundness (SUB2), count consistency (SUB3), retraction nullify-not-remove (SUB4), shadow semantics (SUB5 — retracting a retraction does not restore the original), retraction idempotence (SUB6). Operations: `MakeLink`, `FindLinks` (returns all matching including retracted), `FindNumLinks`, `Retract` (files a `retraction` link targeting another link's id), `ActiveLinks` (returns matches with retracted links subtracted). Defines `retraction` as the only substrate-level link type; all other link types are protocol-defined. Implementation is filesystem-backed (`_store/links.jsonl` plus a SQLite index). Protocols are stated in terms of link existence and type, not storage mechanism — substrate is replaceable as long as its properties hold. See [Substrate Module](protocols/substrate.md).

**Summary.** 1-3 sentence YAML field describing what a claim claims. Produced by the summarize step. Used by downstream foundation loading.

**Summarize.** The step that regenerates the `summary` YAML field using batched LLM calls. Prerequisite to assembly.

**Surface Expansion.** Across successive review cycles, a claim's textual surface grows monotonically without corresponding growth in reasoning content. The shared mechanism underneath [Contract Sprawl](equilibrium/contract-sprawl.md), [Prose Sprawl](equilibrium/prose-sprawl.md), and [Index Sprawl](equilibrium/index-sprawl.md). Contained by the [Voice Principle](principles/voice.md) (constrains what the reviser writes) and finding classification (constrains what reaches the reviser). See [Surface Expansion](equilibrium/surface-expansion.md).

**Synthesis.** The step integrating theory-channel and evidence-channel outputs into a structured note with dependency-mapped claims. The first place both perspectives meet — agreements validate, disagreements seed new hypotheses. Roughly 70% of a note's vocabulary coinage happens here. See [Two-Channel Architecture](two-channel-architecture.md).

**Synthesis (link type).** A substrate `synthesis` link records that consultation produced a note from an inquiry. From = inquiry, to = note. Provenance trail from the inquiry to its synthesized output. Filed by the consultation protocol. See [Consultation Protocol](protocols/consultation-protocol.md).

**Synthesis coinage.** [Prose coinage](patterns/prose-coinage.md) that occurs at the synthesis step when two-channel outputs are reconciled. Roughly 70% of a note's coinages happen here, because synthesis is where incompatible vocabularies must be merged into a single note and no existing word may fit precisely. Contrasts with [review coinage](#r) which happens during later review/revise cycles.

## T

**Theorem.** A claim classified as a proven result.

**Theory channel.** The agent channel that consults established theory (design documents, domain models) and makes predictions. Forbidden from referring to specific evidence. Its question generator sees a vocabulary list of the framework's own terms (vocabulary-in-prompt) because theory space is conceptual and listable. See [Two-Channel Architecture](two-channel-architecture.md).

**Transition condition.** What the [maturation protocol](#m) evaluates to decide a representation is ready to advance to the next stage. Each transition has a readiness signal (predicate truth or sustained quiet) and a handoff artifact (what gets passed to the next stage). Transitions: discovery→note decomposition (note convergence predicate plus sustained quiet), note decomposition→claim convergence (claim file contract validates), claim convergence→verification (claim convergence predicate plus coverage), verification→done. See [Maturation Protocol](protocols/maturation-protocol.md).

**Transitional failure.** An [equilibrium](equilibrium/) pattern whose force acts at a representation boundary introduced by a stage transition. Fixed once per boundary (by specifying and enforcing the output contract that the transition introduces); recurs at every new boundary because producing is easier than specifying. Contrasts with [gravitational failure](#g) and [oscillatory failure](#o). [Uncontracted Representation Change](equilibrium/uncontracted-representation-change.md) is the transitional pattern documented so far.

**Two-channel architecture.** The mechanism that produces new knowledge for the lattice. Two independent agent channels (theory and evidence) investigate a question under enforced vocabulary separation. A synthesis agent integrates their outputs into a structured note. The note then enters [note convergence](#n) for review/revise cycles. The architecture governs how the initial note is generated, not how it matures. See [Two-Channel Architecture](two-channel-architecture.md).

**Type.** YAML classification of a claim: axiom, definition, design requirement, lemma, theorem, corollary.

## U

**Uncontracted Representation Change.** A [transitional failure](#t) at a [representation change](patterns/representation-change.md) where the pipeline introduces a new unit of structure without specifying what well-formed output means. The structure lands on disk, but no contract says what must hold, and downstream reviewers spend cycles on symptoms of unnamed violations. See [Uncontracted Representation Change](equilibrium/uncontracted-representation-change.md).

**Under-citation.** A proof uses a claim that its Depends list doesn't include. The most common form of [Citation Drift](equilibrium/citation-drift.md).

## V

**Validate-before-review.** The pattern of running a mechanical structural-invariant check (validator + per-invariant fix recipes) before each review cycle, so the LLM reviewer sees structurally sound state and spends its cycles on semantic issues. See [Validate Before Review](patterns/validate-before-review.md) and [design note](design-notes/validate-before-review.md).

**Validation Principle.** Design commitment that every representation the system operates on must have a structural contract, and no LLM review cycle operates on state that has not been mechanically verified against that contract. Uses enumeration because structural invariants are a closed, mechanically checkable set. Sibling to the [Coupling Principle](principles/coupling.md) and [Voice Principle](principles/voice.md). See [The Validation Principle](principles/validation.md).

**Validator.** Mechanical check (pure code, no LLM) of a representation's structural invariants against its contract. Exhaustive and cheap; free of the add-bias that compromises LLM-based structural fixes.

**Verify the whole.** Stepping back to original scope after narrowing, to check that the refined pieces cohere. See [Verify the Whole pattern](patterns/verify-the-whole.md).

**Vocabulary (YAML field).** Per-claim dictionary of symbols and their meanings. Shared across the note through aggregation.

**Vocabulary bridge.** See Bridge vocabulary.

**Vocabulary firewall.** See Firewall, vocabulary.

**Voice Principle.** Design commitment that LLM output is constrained by defining what well-formed output looks like (positive style structure), not by enumerating what it must avoid. The Dijkstra voice — prose with embedded formalism, every statement justified in the sentence that introduces it — leaves no slot for non-reasoning prose. Enumerated prohibition lists leave gaps the agent drifts through. Uses positive definition because prose quality is an open set that can't be enumerated. Sibling to the [Coupling Principle](principles/coupling.md) and [Validation Principle](principles/validation.md). See [The Voice Principle](principles/voice.md).

## Y

**YAML (`.yaml`).** The per-claim metadata file. Holds label, name, type, summary, depends, vocabulary. The authoritative source for all metadata.