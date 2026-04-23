# Glossary

Terms specific to this reasoning system. Cross-references point to where each term is discussed substantively.

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [Y](#y)

## A

**Accretion.** Growth of the lattice by adding new claims rather than mutating existing ones. The discipline that prevents [Contract Sprawl](equilibrium/contract-sprawl.md). See [Accretion pattern](patterns/accretion.md).

**Apex (cone apex).** The high-dependency claim at the center of a [dependency cone](patterns/dependency-cone.md) — the one that keeps getting revised while its dependencies remain stable.

**Assembly.** The stage that exports formalized claims into `formal-statements.md` and `dependency-graph.yaml` for downstream consumers. Mechanical, no LLM.

**Attractor, Genesis.** A claim that becomes the default home for every fact anyone needs about a concept it introduces. Cause of [Contract Sprawl](equilibrium/contract-sprawl.md).

**Authority.** A source the reasoning system consults — for example, Nelson's design documents (theory authority) or Gregory's implementation (evidence authority). See [Two-Channel Architecture](patterns/two-data-authorities.md).

**Axiom.** A claim classified as assumed rather than derived. Stated without proof.

## B

**Blueprinting.** The stage that decomposes a note into per-claim file pairs (YAML metadata + MD body). A [representation change](patterns/representation-change.md) that introduces structural invariants specified in the [Claim File Contract](design-notes/claim-file-contract.md). Produces the structure formalization operates on. See [Blueprinting](blueprinting.md).

**Boundary observation.** An out-of-scope finding captured during investigation — enough context to seed a new investigation without expanding the current one. Seed for [scope promotion](patterns/scope-promotion.md).

**Bridge citation.** A citation to a claim that licenses an inference step between two other concepts in a proof. Missing bridge citations are a subtype of [Citation Drift](equilibrium/citation-drift.md#subtype-bridge-citations).

**Bridge vocabulary.** The unified terms that make a campaign's two channels speak coherently. Curated at campaign creation time, not emergent. Campaign-level because it bridges two specific channels — different pairings produce different bridges. The primary consumer is the reviewer, who must interpret claims against both channels' terminology. See [Architecture](architecture.md).

## C

**Campaign.** Binds a theory channel and an evidence channel to a target and a bridge vocabulary. The operational unit of coordinated investigation. The channel pairing is immutable per campaign — any channel change means a new campaign with a new vocabulary. Ends when its question is answered (verified attachment) or abandoned (negative result). Scope promotion during review spawns additional inquiries within the same campaign; genuinely new questions spawn new campaigns. See [Architecture](architecture.md).

**Channel.** A self-contained plugin holding source content, consultation code, consultation prompts, and metadata. Channels are named identities in a flat top-level namespace (`channels/`). Each channel exposes a two-function interface: `generate_questions` (decompose an inquiry into channel-appropriate sub-questions) and `consult` (answer a single question from the channel's corpus). Internal implementation is the channel's business. Campaigns reference channels by name. See [Architecture](architecture.md).

**Channel asymmetry.** Shape-mismatch between the theory channel and the evidence channel. Theory space is conceptual and listable (vocabulary-in-prompt). Evidence space is specific and must be seen (corpus-in-prompt). Prevents naive merging and forces synthesis to coin bridging vocabulary. See [Channel Asymmetry pattern](patterns/channel-asymmetry.md).

**Citation, inline.** A reference in the proof narrative like "by NAT-wellorder." Part of proof content, not metadata.

**Claim.** A single unit of reasoning within a note. An assertion — something the system says is the case, which can be verified, contested, or refuted. Has a label, type, formal contract, and dependencies. The atomic lattice node. See [Architecture](architecture.md).

**Claim File Contract.** The structural contract specifying what well-formed per-claim file state looks like after blueprinting. Concrete rules, mechanically checkable: one body per file, filename matches label, references resolve, metadata agrees with content, no dependency cycles. The first instance of the output contract the [Validation Principle](principles/validation.md) requires. See [Claim File Contract](design-notes/claim-file-contract.md).

**Cone, dependency.** A cluster of tightly coupled claims where an apex keeps being revised while dependencies are stable. See [Dependency Cone pattern](patterns/dependency-cone.md).

**Consult authority.** During revision, return to source material to ground findings in evidence. See [Consult Authority pattern](patterns/consult-authority.md).

**Content.** What the `.md` file holds — narrative, proof, formal contract claims. Distinct from metadata.

**Contract, formal.** The structured claim section of a claim (`*Formal Contract:*`): preconditions, postconditions, invariants, axiom, definition. Part of content.

**Contract Sprawl.** A claim's formal contract keeps growing across cycles because it is a [Genesis Attractor](equilibrium/contract-sprawl.md). See [Contract Sprawl](equilibrium/contract-sprawl.md).

**Corollary.** A claim classified as an immediate consequence of another.

**Coupling Principle.** Design commitment that prose and formal content are authored as a pair at an artifact-specific ratio (90/10 for notes, 70/30 for claim files). Divergence from the ratio signals decoupling — one surface growing without the other. Prose is the generative substrate; formal notation precipitates from it. Too much prose fails loudly (hand-waving). Too much formal fails silently (discovery stops). One of three principles forming the quality boundary for review. See [The Coupling Principle](principles/coupling.md).

## D

**Definition.** A claim classified as introducing named concepts or operations.

**Depends (YAML).** The structured dependency list in a claim's YAML file. The authoritative metadata for dependencies.

**Design requirement.** A claim classified as an architectural or measurement constraint the system imposes.

**Discovery.** The stage producing notes through the [two-channel architecture](patterns/two-data-authorities.md). First stage of the pipeline. See [Discovery](discovery.md).

**Domain.** The logical configuration of a lattice — which verifier, which channels, which vocabulary firewall. Expressed in `lattices/<L>/config.yaml`, not as a separate directory. Two configurations that differ in any binding are different domains. The domain is what you swap to move the engine from one subject area to another. See [Architecture](architecture.md).

**Drift, Citation.** The state where citations (YAML depends + inline prose) no longer match the dependencies a proof actually uses. See [Citation Drift](equilibrium/citation-drift.md).

**Driver (Citation Drift).** The cause class that produces drift.
- **Internal driver** — active work inside the same note produces drift within that note. Continuous.
- **Passive driver** — work in an upstream note produces drift in downstream consumers. Event-driven.

**Downward pass.** Second phase of the [V-cycle](design-notes/review-v-cycle.md) — re-verifying at narrower scales after wider-scale corrections.

**Domain language emergence.** The process by which the system coins new prose words for concepts it will reason with, as two-channel synthesis and subsequent review cycles produce claims existing vocabulary can't express. See [Domain Language Emergence](design-notes/domain-language-emergence.md).

## E

**Enumerated surface.** A claim structure that pre-identifies where sub-facts will live (e.g., `T10a.1`, `T10a.2`, ...). Invites [accretion](patterns/accretion.md); prevents Genesis Attractors forming.

**Evidence channel.** The agent channel that reads raw evidence (implementation code, experimental measurements) and reports patterns. Forbidden from using theory-level vocabulary. Its question generator sees the corpus itself at generation time (corpus-in-prompt) because evidence space is specific and must be seen. See [Discovery](discovery.md).

**Evidence space.** The space of observed behaviors and measurements the evidence channel reports. Complement to [hypothesis space](#h).

**Excavation stages.** The predictable stages review/revise findings progress through as cycles deepen: citation accuracy → completeness → structural coherence → mathematical precision → structural organization → prose clarity. See [Review/Revise Iteration](patterns/review-revise-iteration.md).

**Extract/Absorb.** Finding shared concepts across multiple claims and factoring them into new foundation layers. How the lattice grows inward. See [Extract/Absorb pattern](patterns/extract-absorb.md).

## F

**Finding classification.** The reviewer's classification of each finding as requiring action or not. Correctness issues (broken precondition chains, missing axioms, ungrounded operators) must be fixed. Tightening observations (loose phrasing, minor style, alternative framings) are logged but do not trigger revision. Prevents [Surface Expansion](equilibrium/surface-expansion.md) by keeping tightening findings from reaching the reviser. See [Formalization](formalization.md).

**Firewall, vocabulary.** Structural enforcement that the theory channel cannot use evidence-channel terms and vice versa. Prevents the LLM's training knowledge from shortcutting reasoning. See [Discovery](discovery.md).

**Formal-statements export.** Curated export containing all claim summaries and formal contracts in dependency order. Consumed by downstream notes as foundation.

**Formalization.** The stage that rewrites proofs to Dijkstra standard, produces formal contracts, and runs the V-cycle to convergence. Not cleanup — discovery under precision constraint. Scope narrowing to per-claim files is itself epistemically productive. See [Formalization](formalization.md).

**Foundation.** From a downstream note's perspective, any upstream note it depends on. Foundation content is read-only context for the downstream's review cycles.

**Full-review.** Full-scale review reading an entire note. Finds issues invisible to narrower scales: carrier-set conflation, precondition chain gaps, vocabulary collisions, issues in small claims. Renamed from cross-review.

**Full scale.** [Review V-Cycle](design-notes/review-v-cycle.md) scope of the whole note with full foundation context. Renamed from System scale.

## G

**Genesis Attractor.** See Attractor, Genesis.

**Gravitational failure.** An [equilibrium](equilibrium/) pattern whose force acts continuously across review cycles. Requires permanent discipline — prompt framing, coupling monitoring, voice structure — not a one-time fix. Contrasts with [transitional failure](#t) and [oscillatory failure](#o). Contract Sprawl, Prose Sprawl, Surface Expansion, Index Sprawl, Citation Drift are gravitational.

**Ground state.** The state of genuine convergence across all scales — claim, cluster, and system review all agree there are no remaining issues. Distinguished from "stopped" (no finding in one scale but others can still expose issues). See [V-cycle self-evaluation](design-notes/review-v-cycle.md#the-v-cycle-as-self-evaluation).

## H

**Hypothesis cluster.** A [cone](patterns/dependency-cone.md) in a science domain: apex (hypothesis statement) plus its supporting dependencies (axioms, definitions, data citations, coined concepts). Regional convergence of a hypothesis cluster = hypothesis ready for its scope.

**Hypothesis space.** The space of candidate principles and concepts that could organize a domain. Explored by the theory channel. Complement to [evidence space](#e). New [prose coinage](patterns/prose-coinage.md) is a form of hypothesis generation.

## I

**Index Sprawl.** Enumerative prose that grows across review cycles — lists of use-sites, exhaustiveness claims, bundling inventories. The enumerative form of [Surface Expansion](equilibrium/surface-expansion.md). See [Index Sprawl](equilibrium/index-sprawl.md).

**Inquiry.** One initial question that produces one note. 1:1 relationship with the note. A campaign spawns one or more inquiries. The unit of two-channel discovery: theory-channel and evidence-channel sub-questions are derived from it, consulted independently, synthesized into a single note. See [Architecture](architecture.md).

**Internal driver.** See Driver.

## J

**Join.** Lattice operation. A new node is created above multiple foundations. [Scope promotion](patterns/scope-promotion.md) executes a join.

## L

**Label.** A claim's stable citable handle (e.g., `T0`, `NAT-wellorder`, `TA-Pos`). Set at blueprinting, never changes.

**Lattice.** The coverage target that campaigns build toward: an accumulated verified dependency graph for one subject-area focus. The lattice operates at two granularities simultaneously: during discovery, notes declare note-level dependencies (`depends:`); during formalization, claims declare claim-level dependencies (`follows_from:`). Which granularity a consuming note sees depends on the consumer's stage. Notes retire gradually as their consumers formalize; the terminal lattice is all claim-to-claim edges with note groupings as provenance metadata. See [Architecture](architecture.md).

**Lemma.** A claim classified as an intermediate result supporting higher-level theorems.

**Local-review.** Local-scale review checking logical gaps, unjustified steps, missing cases, and dependency correctness. One claim at a time with its dependencies as fixed context. The contract gate: does this claim validly export what downstream claims can cite? Renamed from proof-review.

**Local scale.** [Review V-Cycle](design-notes/review-v-cycle.md) scope of one claim with its dependencies as fixed context. Renamed from Claim scale.

## M

**Markdown body (`.md`).** The file that holds a claim's content: narrative, proof, formal contract.

**Meet.** Lattice operation. A concept shared by two nodes is extracted into a new foundation layer below both. [Extract/absorb](patterns/extract-absorb.md) executes a meet.

**Metadata.** What the YAML file holds — label, name, type, summary, depends, vocabulary. Describes the claim; does not constitute its reasoning.

**Modeling.** The stage translating formal contracts into mechanically verifiable code (Dafny, Alloy). Follows formalization.

## N

**Narrow → Refine → Verify.** The three-phase cycle every process in the system follows. The primary pattern, rooted in the scientific method. See [Narrow → Refine → Verify](patterns/narrow-refine-verify.md).

**Note.** A document covering one topic, produced by one inquiry. Contains ~20–40 claims with explicit dependency structure. The format has Dijkstra-EWD lineage: numbered, bounded, self-contained investigations carrying arbitrary formal weight. Serves as the stable interface boundary for discovery-stage consumers; its internal claim set becomes the operational surface for formalization-stage consumers. See [Architecture](architecture.md).

Notes are identified by the legacy prefix `ASN-NNNN` (originally "Abstract Specification Note"), retained opaque for stable addressing across commits, filenames, and cross-references.

## O

**Open surface.** A claim structure that leaves no explicit home for new sub-facts (e.g., "with its standard claims"). Sets the conditions for a [Genesis Attractor](equilibrium/contract-sprawl.md) to form.

**Oscillatory failure.** An [equilibrium](equilibrium/) pattern whose force acts at a site of undecidability — two resolutions are both locally valid and nothing in the cycle arbitrates between them. Fixed by establishing the arbitrating criterion (a contract, a convention, or an explicit scope ruling), which varies by subtype. Contrasts with [gravitational failure](#g) and [transitional failure](#t). [Reverse-Course Oscillation](equilibrium/reverse-course-oscillation.md) is the oscillatory pattern documented so far.

**Over-citation.** A Depends entry for a claim the proof doesn't actually use. A form of [Citation Drift](equilibrium/citation-drift.md).

## P

**Passive driver.** See Driver.

**Pattern language.** The patterns that govern how agents produce verified knowledge. See [patterns README](patterns/README.md).

**Prose coinage.** The atomic event of coining a new prose word for a concept no existing vocabulary captures precisely (e.g., "action point," "divergence," "subspace"). Occurs in two modes: [synthesis coinage](#s) and [review coinage](#r). Precedes [prose compression](patterns/prose-compression.md). See [Prose Coinage pattern](patterns/prose-coinage.md).

**Prose compression.** A prose-named concept gets a symbol for compact formal manipulation (e.g., "tumbler addition" → `⊕`). Same concept, compressed form. Produced by [review/revise iteration](patterns/review-revise-iteration.md) as concepts are used frequently enough that compact notation pays for itself. See [Prose Compression pattern](patterns/prose-compression.md).

**Prose Sprawl.** A claim's narrative prose grows across review cycles without corresponding growth in reasoning content. The narrative form of [Surface Expansion](equilibrium/surface-expansion.md). Contained by the [Voice Principle](principles/voice.md) (positive style structure) and finding classification (tightening observations don't reach the reviser). See [Prose Sprawl](equilibrium/prose-sprawl.md).

## R

**Rebase.** Re-verifying downstream claims after a foundation changes. Happens automatically via review/revise cycles because changed dependencies invalidate dependents' metadata.

**Regional-review.** Focused review of a specific dependency cone with apex + dependencies as context. Resolves the cluster as a constraint system. Renamed from cone-review.

**Regional-sweep.** Proactive regional-scale review walking the dependency graph bottom-up, running regional-review on every claim meeting the dependency threshold. Renamed from cone-sweep.

**Regional scale.** [Review V-Cycle](design-notes/review-v-cycle.md) scope between local and full — reviewing a dependency cone as a unit. Renamed from Cluster scale.

**Representation change.** Progressive transformation of content through different forms (narrative → structured → formal → mechanical) without changing the underlying claim. Each change introduces structural rules at the new form. See [Representation Change pattern](patterns/representation-change.md).

**Reverse-Course Oscillation.** An [oscillatory failure](#o) in which a reviser's change in cycle N is undone in cycle N+1 because two locally-valid resolutions exist and the cycle has no shared criterion to pick between them. Subtypes by source of undecidability: contract-absent, judgment-call, exhaustiveness-vs-restraint. Partially contained by finding classification (judgment-call findings become observations and never trigger revision). See [Reverse-Course Oscillation](equilibrium/reverse-course-oscillation.md).

**Review coinage.** [Prose coinage](patterns/prose-coinage.md) that happens during review/revise cycles rather than at synthesis. Occurs in both discovery and formalization. Roughly 30% of a note's coinages. Driven by reviewer pressure surfacing a concept the current text is discussing in ad-hoc prose without a shared name. See [Synthesis coinage](#s) for contrast.

**Review/revise iteration.** Repeating cycles of review (finding issues), revision (fixing them), and re-review until convergence. See [Review/Revise Iteration pattern](patterns/review-revise-iteration.md).

**Reviewer.** The agent that reads content and produces findings. Classifies each finding by whether it requires action. Does not modify.

**Reviser.** The agent that reads a finding and modifies the content to address it. Writes in the Dijkstra voice. Always paired with a reviewer.

## S

**Scale.** Scope of a review cycle. Three canonical scales: local, regional, full. See [Review V-Cycle](design-notes/review-v-cycle.md).

**Scientific method.** Lineage of the primary pattern — narrow scope, refine through iteration, verify coherence. Every process in the system follows this rhythm.

**Scope narrowing.** Breaking work into smaller tractable pieces by constraining context. See [Scope Narrowing pattern](patterns/scope-narrowing.md).

**Scope promotion.** Elevating out-of-scope boundary observations into their own first-class investigations. How the lattice grows outward. See [Scope Promotion pattern](patterns/scope-promotion.md).

**Scoped inquiry.** Decomposing a question along authority boundaries, with each channel investigating what it can evaluate. See [Scoped Inquiry pattern](patterns/scoped-inquiry.md).

**Self-healing rebase.** When a foundation claim changes, dependents automatically re-verify through the same narrow → refine → verify cycles that built them.

**Self-Report Laundering.** A failure mode of [self-healing](design-notes/self-healing.md#observation-layer-limitation): an evaluator reads the summaries an LLM process produced about itself (commit messages, stats, finding counts) rather than the artifacts it produced (diffs, code, outputs). The generator's own voice gets re-surfaced to the evaluator as if it were independent evidence. Addressed by the [Audit by Content](design-notes/audit-by-content.md) design rule.

**Signal.** A mechanical indicator that a disequilibrium pattern is occurring (e.g., a claim's contract growing across cycles signals [Contract Sprawl](equilibrium/contract-sprawl.md)).

**Sprawl.** See Contract Sprawl, Prose Sprawl, Index Sprawl.

**Structural finding.** A review finding whose root cause is structural rather than semantic — duplicated declarations, dangling references, metadata disagreement, dependency-graph cycles. Symptom of an [Uncontracted Representation Change](equilibrium/uncontracted-representation-change.md).

**Summary.** 1-3 sentence YAML field describing what a claim claims. Produced by the summarize step. Used by downstream foundation loading.

**Summarize.** The step that regenerates the `summary` YAML field using batched LLM calls. Prerequisite to assembly.

**Surface Expansion.** Across successive review cycles, a claim's textual surface grows monotonically without corresponding growth in reasoning content. The shared mechanism underneath [Contract Sprawl](equilibrium/contract-sprawl.md), [Prose Sprawl](equilibrium/prose-sprawl.md), and [Index Sprawl](equilibrium/index-sprawl.md). Contained by the [Voice Principle](principles/voice.md) (constrains what the reviser writes) and finding classification (constrains what reaches the reviser). See [Surface Expansion](equilibrium/surface-expansion.md).

**Synthesis.** The step integrating theory-channel and evidence-channel outputs into a structured note with dependency-mapped claims.

**Synthesis coinage.** [Prose coinage](patterns/prose-coinage.md) that occurs at the synthesis step when two-channel outputs are reconciled. Roughly 70% of a note's coinages happen here, because synthesis is where incompatible vocabularies must be merged into a single note and no existing word may fit precisely. Contrasts with [review coinage](#r) which happens during later review/revise cycles.

## T

**Theorem.** A claim classified as a proven result.

**Theory channel.** The agent channel that consults established theory (design documents, domain models) and makes predictions. Forbidden from referring to specific evidence. Its question generator sees a vocabulary list of the framework's own terms (vocabulary-in-prompt) because theory space is conceptual and listable. See [Discovery](discovery.md).

**Transitional failure.** An [equilibrium](equilibrium/) pattern whose force acts at a representation boundary introduced by a pipeline transition. Fixed once per boundary (by specifying and enforcing the output contract that the transition introduces); recurs at every new boundary because producing is easier than specifying. Contrasts with [gravitational failure](#g) and [oscillatory failure](#o). [Uncontracted Representation Change](equilibrium/uncontracted-representation-change.md) is the transitional pattern documented so far.

**Two-channel architecture.** The two-channel design with vocabulary firewall separating theory from evidence. Each channel consults its own corpus independently; synthesis is the first place both perspectives meet. See [Discovery](discovery.md).

**Type.** YAML classification of a claim: axiom, definition, design requirement, lemma, theorem, corollary.

## U

**Uncontracted Representation Change.** A [transitional failure](#t) at a [representation change](patterns/representation-change.md) where the pipeline introduces a new unit of structure without specifying what well-formed output means. The structure lands on disk, but no contract says what must hold, and downstream reviewers spend cycles on symptoms of unnamed violations. See [Uncontracted Representation Change](equilibrium/uncontracted-representation-change.md).

**Under-citation.** A proof uses a claim that its Depends list doesn't include. The most common form of [Citation Drift](equilibrium/citation-drift.md).

**Upward pass.** First phase of the [V-cycle](design-notes/review-v-cycle.md) — local review → contract review → regional sweep → full-review, building confidence from narrow to wide scope.

## V

**Validate-before-review.** The pattern of running a mechanical structural-invariant check (validator + per-invariant fix recipes) before each review cycle, so the LLM reviewer sees structurally sound state and spends its cycles on semantic issues. See [Validate Before Review](patterns/validate-before-review.md) and [design note](design-notes/validate-before-review.md).

**Validation Principle.** Design commitment that every representation the system operates on must have a structural contract, and no LLM review cycle operates on state that has not been mechanically verified against that contract. Uses enumeration because structural invariants are a closed, mechanically checkable set. Sibling to the [Coupling Principle](principles/coupling.md) and [Voice Principle](principles/voice.md). See [The Validation Principle](principles/validation.md).

**Validator.** Mechanical check (pure code, no LLM) of a representation's structural invariants against its contract. Exhaustive and cheap; free of the add-bias that compromises LLM-based structural fixes.

**V-cycle (Review V-Cycle).** Multi-scale review architecture composing local, regional, and full scales into upward and downward passes. Inspired by multigrid methods in numerical analysis. See [Review V-Cycle](design-notes/review-v-cycle.md).

**Verify the whole.** Stepping back to original scope after narrowing, to check that the refined pieces cohere. See [Verify the Whole pattern](patterns/verify-the-whole.md).

**Vocabulary (YAML field).** Per-claim dictionary of symbols and their meanings. Shared across the note through aggregation.

**Vocabulary bridge.** See Bridge vocabulary.

**Vocabulary firewall.** See Firewall, vocabulary.

**Voice Principle.** Design commitment that LLM output is constrained by defining what well-formed output looks like (positive style structure), not by enumerating what it must avoid. The Dijkstra voice — prose with embedded formalism, every statement justified in the sentence that introduces it — leaves no slot for non-reasoning prose. Enumerated prohibition lists leave gaps the agent drifts through. Uses positive definition because prose quality is an open set that can't be enumerated. Sibling to the [Coupling Principle](principles/coupling.md) and [Validation Principle](principles/validation.md). See [The Voice Principle](principles/voice.md).

## Y

**YAML (`.yaml`).** The per-claim metadata file. Holds label, name, type, summary, depends, vocabulary. The authoritative source for all metadata.