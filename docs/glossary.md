# Glossary

Terms specific to this reasoning system. Cross-references point to where each term is discussed substantively.

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [Y](#y)

## A

**Accretion.** Growth of the lattice by adding new claims rather than mutating existing ones. The discipline that prevents [Contract Sprawl](equilibrium/contract-sprawl.md). See [Accretion pattern](patterns/accretion.md).

**Apex (cone apex).** The high-dependency claim at the center of a [dependency cone](patterns/dependency-cone.md) — the one that keeps getting revised while its dependencies remain stable.

**Assembly.** The stage that exports formalized claims into `formal-statements.md` and `dependency-graph.yaml` for downstream consumers. Mechanical, no LLM.

**Attractor, Genesis.** A claim that becomes the default home for every fact anyone needs about a concept it introduces. Cause of [Contract Sprawl](equilibrium/contract-sprawl.md).

**Authority.** A source the reasoning system consults — for example, Nelson's design documents (theory authority) or Gregory's implementation (data authority). See [Two Data Authorities](patterns/two-data-authorities.md).

**Axiom.** A claim classified as assumed rather than derived. Stated without proof.

## B

**Blueprinting.** The stage that decomposes a note into per-claim file pairs (YAML metadata + MD body). Produces the structure formalization operates on. See [blueprinting guide](guides/formalization.md).

**Boundary observation.** An out-of-scope finding captured during investigation — enough context to seed a new investigation without expanding the current one. Seed for [scope promotion](patterns/scope-promotion.md).

**Bridge citation.** A citation to a claim that licenses an inference step between two other concepts in a proof. Missing bridge citations are a subtype of [Citation Drift](equilibrium/citation-drift.md#subtype-bridge-citations).

## C

**Campaign.** A scope-bounded research effort that spawns one or more inquiries, each producing a note. Starts with a top-level question; ends when the inquiries it spawned have been investigated and their notes attached to the lattice (or abandoned with a negative result). Scope promotion during review spawns additional inquiries within the same campaign; genuinely new questions spawn new campaigns. See [Architecture](architecture.md).

**Channel asymmetry.** Shape-mismatch between the theory channel and the data channel. Prevents naive merging and forces synthesis to coin bridging vocabulary. See [Channel Asymmetry pattern](patterns/channel-asymmetry.md).

**Citation, inline.** A reference in the proof narrative like "by NAT-wellorder." Part of proof content, not metadata.

**Claim.** A single unit of reasoning within a note. An assertion — something the system says is the case, which can be verified, contested, or refuted. Has a label, type, formal contract, and dependencies. The atomic lattice node. See [Architecture](architecture.md).

**Cone, dependency.** A cluster of tightly coupled claims where an apex keeps being revised while dependencies are stable. See [Dependency Cone pattern](patterns/dependency-cone.md).

**Consult authority.** During revision, return to source material to ground findings in evidence. See [Consult Authority pattern](patterns/consult-authority.md).

**Content.** What the `.md` file holds — narrative, proof, formal contract claims. Distinct from metadata.

**Contract, formal.** The structured claim section of a claim (`*Formal Contract:*`): preconditions, postconditions, invariants, axiom, definition. Part of content.

**Contract Sprawl.** A claim's formal contract keeps growing across cycles because it is a [Genesis Attractor](equilibrium/contract-sprawl.md). See [Contract Sprawl](equilibrium/contract-sprawl.md).

**Corollary.** A claim classified as an immediate consequence of another.

## D

**Data channel.** The agent channel that reads raw evidence (implementation code, experimental measurements) and reports patterns. Forbidden from using theory-level vocabulary. See [Two Data Authorities](patterns/two-data-authorities.md).

**Definition.** A claim classified as introducing named concepts or operations.

**Depends (YAML).** The structured dependency list in a claim's YAML file. The authoritative metadata for dependencies.

**Design requirement.** A claim classified as an architectural or measurement constraint the system imposes.

**Discovery.** The stage producing notes through the [two-channel architecture](patterns/two-data-authorities.md). First stage of the pipeline. See [discovery guide](discovery.md).

**Domain.** The configuration bundle that changes when the engine runs on a different subject area: verifier binding (Dafny / Alloy for software; experimental replication for science), channel sources, vocabulary firewall word lists, foundation glossary. Two bundles that differ in any binding are different domains. A domain can host multiple lattices. See [Architecture](architecture.md).

**Drift, Citation.** The state where citations (YAML depends + inline prose) no longer match the dependencies a proof actually uses. See [Citation Drift](equilibrium/citation-drift.md).

**Driver (Citation Drift).** The cause class that produces drift.
- **Internal driver** — active work inside the same note produces drift within that note. Continuous.
- **Passive driver** — work in an upstream note produces drift in downstream consumers. Event-driven.

**Downward pass.** Second phase of the [V-cycle](design-notes/review-v-cycle.md) — re-verifying at narrower scales after wider-scale corrections.

**Domain language emergence.** The process by which the system coins new prose words for concepts it will reason with, as two-channel synthesis and subsequent review cycles produce claims existing vocabulary can't express. See [Domain Language Emergence](design-notes/domain-language-emergence.md).

## E

**Enumerated surface.** A claim structure that pre-identifies where sub-facts will live (e.g., `T10a.1`, `T10a.2`, ...). Invites [accretion](patterns/accretion.md); prevents Genesis Attractors forming.

**Evidence space.** The space of observed behaviors and measurements the data channel reports. Complement to [hypothesis space](#h).

**Excavation stages.** The predictable stages review/revise findings progress through as cycles deepen: citation accuracy → completeness → structural coherence → mathematical precision → structural organization → prose clarity. See [Review/Revise Iteration](patterns/review-revise-iteration.md).

**Extract/Absorb.** Finding shared concepts across multiple claims and factoring them into new foundation layers. How the lattice grows inward. See [Extract/Absorb pattern](patterns/extract-absorb.md).

## F

**Firewall, vocabulary.** Structural enforcement that the theory channel cannot use data-channel terms and vice versa. Prevents the LLM's training knowledge from shortcutting reasoning. See [Two Data Authorities](patterns/two-data-authorities.md).

**Formal-statements export.** Curated export containing all claim summaries and formal contracts in dependency order. Written to `lattices/xanadu/manifests/ASN-NNNN/formal-statements.md`. Consumed by downstream notes as foundation.

**Formalization.** The stage that rewrites proofs to Dijkstra standard, produces formal contracts, and runs the V-cycle to convergence. See [formalization guide](guides/formalization.md).

**Foundation.** From a downstream note's perspective, any upstream note it depends on. Foundation content is read-only context for the downstream's review cycles.

**Full-review.** Full-scale review reading an entire note. Finds issues invisible to narrower scales: carrier-set conflation, precondition chain gaps, vocabulary collisions, issues in small claims. Renamed from cross-review.

**Full scale.** [Review V-Cycle](design-notes/review-v-cycle.md) scope of the whole note with full foundation context. Renamed from System scale.

## G

**Genesis Attractor.** See Attractor, Genesis.

**Gravitational failure.** An [equilibrium](equilibrium/) pattern whose force acts continuously across review cycles. Requires permanent discipline — prompt framing, coupling monitoring, authoring habits — not a one-time fix. Contrasts with [transitional failure](#t) and [oscillatory failure](#o). Contract Sprawl, Prose Sprawl, Surface Expansion, Index Sprawl, Citation Drift are gravitational.

**Ground state.** The state of genuine convergence across all scales — claim, cluster, and system review all agree there are no remaining issues. Distinguished from "stopped" (no finding in one scale but others can still expose issues). See [V-cycle self-evaluation](design-notes/review-v-cycle.md#the-v-cycle-as-self-evaluation).

## H

**Hypothesis cluster.** A [cone](patterns/dependency-cone.md) in a science domain: apex (hypothesis statement) plus its supporting dependencies (axioms, definitions, data citations, coined concepts). Regional convergence of a hypothesis cluster = hypothesis ready for its scope. See [Science Approach](science/README.md).

**Hypothesis space.** The space of candidate principles and concepts that could organize a domain. Explored by the theory channel. Complement to [evidence space](#e). New [prose coinage](patterns/prose-coinage.md) is a form of hypothesis generation.

## I

**Inquiry.** One initial question that produces one note. 1:1 relationship with the note. A campaign spawns one or more inquiries. The unit of two-channel discovery: theory-channel and data-channel sub-questions are derived from it, consulted independently, synthesized into a single note. See [Architecture](architecture.md).

**Internal driver.** See Driver.

## J

**Join.** Lattice operation. A new node is created above multiple foundations. [Scope promotion](patterns/scope-promotion.md) executes a join.

## L

**Label.** A claim's stable citable handle (e.g., `T0`, `NAT-wellorder`, `TA-Pos`). Set at blueprinting, never changes.

**Lattice.** The coverage target that campaigns build toward: an accumulated verified dependency graph for one subject-area focus. A domain can host multiple lattices. Xanadu is one lattice in the software domain. The lattice operates at two granularities simultaneously: during discovery, notes declare note-level dependencies (`depends:`); during formalization, claims declare claim-level dependencies (`follows_from:`). Which granularity a consuming note sees depends on the consumer's stage. Notes retire gradually as their consumers formalize; the terminal lattice is all claim-to-claim edges with note groupings as provenance metadata. See [Architecture](architecture.md).

**Lemma.** A claim classified as an intermediate result supporting higher-level theorems.

**Local-review.** Local-scale review checking logical gaps, unjustified steps, missing cases, and dependency correctness. One claim at a time with its dependencies as fixed context. Renamed from proof-review.

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

**Pattern language.** The 12+ patterns that govern how agents produce verified knowledge. See [patterns README](patterns/README.md).

**Prose coinage.** The atomic event of coining a new prose word for a concept no existing vocabulary captures precisely (e.g., "action point," "divergence," "subspace"). Occurs in two modes: [synthesis coinage](#s) and [review coinage](#r). Precedes [prose compression](patterns/prose-compression.md). See [Prose Coinage pattern](patterns/prose-coinage.md).

**Prose compression.** A prose-named concept gets a symbol for compact formal manipulation (e.g., "tumbler addition" → `⊕`). Same concept, compressed form. Produced by [review/revise iteration](patterns/review-revise-iteration.md) as concepts are used frequently enough that compact notation pays for itself. See [Prose Compression pattern](patterns/prose-compression.md).

## R

**Rebase.** Re-verifying downstream claims after a foundation changes. Happens automatically via review/revise cycles because changed dependencies invalidate dependents' metadata.

**Regional-review.** Focused review of a specific dependency cone with apex + dependencies as context. Resolves the cluster as a constraint system. Renamed from cone-review.

**Regional-sweep.** Proactive regional-scale review walking the dependency graph bottom-up, running regional-review on every claim meeting the dependency threshold. Renamed from cone-sweep.

**Regional scale.** [Review V-Cycle](design-notes/review-v-cycle.md) scope between local and full — reviewing a dependency cone as a unit. Renamed from Cluster scale.

**Representation change.** Progressive transformation of content through different forms (narrative → structured → formal → mechanical) without changing the underlying claim. See [Representation Change pattern](patterns/representation-change.md).

**Reverse-Course Oscillation.** An [oscillatory failure](#o) in which a reviser's change in cycle N is undone in cycle N+1 because two locally-valid resolutions exist and the cycle has no shared criterion to pick between them. Subtypes by source of undecidability: contract-absent, judgment-call, exhaustiveness-vs-restraint. See [Reverse-Course Oscillation](equilibrium/reverse-course-oscillation.md).

**Review coinage.** [Prose coinage](patterns/prose-coinage.md) that happens during review/revise cycles rather than at synthesis. Occurs in both discovery and formalization. Roughly 30% of a note's coinages. Driven by reviewer pressure surfacing a concept the current text is discussing in ad-hoc prose without a shared name. See [Synthesis coinage](#s) for contrast.

**Review/revise iteration.** Repeating cycles of review (finding issues), revision (fixing them), and re-review until convergence. See [Review/Revise Iteration pattern](patterns/review-revise-iteration.md).

**Reviewer.** The agent that reads content and produces findings. Does not modify.

**Reviser.** The agent that reads a finding and modifies the content to address it. Always paired with a reviewer.

## S

**Scale.** Scope of a review cycle. Three canonical scales: local, regional, full. See [Review V-Cycle](design-notes/review-v-cycle.md).

**Scientific method.** Lineage of the primary pattern — narrow scope, refine through iteration, verify coherence. Every process in the system follows this rhythm.

**Scope narrowing.** Breaking work into smaller tractable pieces by constraining context. See [Scope Narrowing pattern](patterns/scope-narrowing.md).

**Scope promotion.** Elevating out-of-scope boundary observations into their own first-class investigations. How the lattice grows outward. See [Scope Promotion pattern](patterns/scope-promotion.md).

**Scoped inquiry.** Decomposing a question along authority boundaries, with each channel investigating what it can evaluate. See [Scoped Inquiry pattern](patterns/scoped-inquiry.md).

**Self-healing rebase.** When a foundation claim changes, dependents automatically re-verify through the same narrow → refine → verify cycles that built them.

**Self-Report Laundering.** A failure mode of [self-healing](design-notes/self-healing.md#observation-layer-limitation): an evaluator reads the summaries an LLM process produced about itself (commit messages, stats, finding counts) rather than the artifacts it produced (diffs, code, outputs). The generator's own voice gets re-surfaced to the evaluator as if it were independent evidence. Addressed by the [Audit by Content](design-notes/audit-by-content.md) design rule. Lives in the self-healing map rather than the equilibrium patterns because it is a failure of the observation machinery, not of the artifact content.

**Signal.** A mechanical indicator that a disequilibrium pattern is occurring (e.g., a claim's contract growing across cycles signals [Contract Sprawl](equilibrium/contract-sprawl.md)).

**Sprawl.** See Contract Sprawl.

**Structural finding.** A review finding whose root cause is structural rather than semantic — duplicated declarations, dangling references, metadata disagreement, dependency-graph cycles. Symptom of an [Uncontracted Representation Change](equilibrium/uncontracted-representation-change.md).

**Summary.** 1-3 sentence YAML field describing what a claim claims. Produced by the summarize step. Used by downstream foundation loading.

**Summarize.** The step that regenerates the `summary` YAML field using batched LLM calls. Prerequisite to assembly.

**Synthesis.** The step integrating theory-channel and data-channel outputs into a structured note with dependency-mapped claims.

**Synthesis coinage.** [Prose coinage](patterns/prose-coinage.md) that occurs at the synthesis step when two-channel outputs are reconciled. Roughly 70% of a note's coinages happen here, because synthesis is where incompatible vocabularies must be merged into a single note and no existing word may fit precisely. Contrasts with [review coinage](#r) which happens during later review/revise cycles.

## T

**Theorem.** A claim classified as a proven result.

**Theory channel.** The agent channel that consults established theory (design documents, domain models) and makes predictions. Forbidden from referring to specific data. See [Two Data Authorities](patterns/two-data-authorities.md).

**Transclusion.** Including one document's content by reference, not by copy. A Xanadu protocol primitive and the mechanism by which the [lattice](patterns/lattice.md) shares content across nodes.

**Transitional failure.** An [equilibrium](equilibrium/) pattern whose force acts at a representation boundary introduced by a pipeline transition. Fixed once per boundary (by specifying and enforcing the output contract that the transition introduces); does not recur unless a new encapsulation is introduced elsewhere. Contrasts with [gravitational failure](#g) and [oscillatory failure](#o). [Uncontracted Representation Change](equilibrium/uncontracted-representation-change.md) is the transitional pattern documented so far.

**Two data authorities.** The two-channel architecture with vocabulary firewall separating theory from data. See [Two Data Authorities pattern](patterns/two-data-authorities.md).

**Type.** YAML classification of a claim: axiom, definition, design requirement, lemma, theorem, corollary.

## U

**Uncontracted Representation Change.** A [transitional failure](#t) at a [representation change](patterns/representation-change.md) where the pipeline introduces a new unit of structure without specifying what well-formed output means. The structure lands on disk, but no contract says what must hold, and downstream reviewers spend cycles on symptoms of unnamed violations. See [Uncontracted Representation Change](equilibrium/uncontracted-representation-change.md).

**Under-citation.** A proof uses a claim that its Depends list doesn't include. The most common form of [Citation Drift](equilibrium/citation-drift.md).

**Upward pass.** First phase of the [V-cycle](design-notes/review-v-cycle.md) — local review → contract review → regional sweep → full-review, building confidence from narrow to wide scope.

## V

**Validate-before-review.** The pattern of running a mechanical structural-invariant check (validator + per-invariant fix recipes) before each review cycle, so the LLM reviewer sees structurally sound state and spends its cycles on semantic issues. See [Validate Before Review](patterns/validate-before-review.md).

**Validation Principle.** Design commitment that every representation the system operates on must have a structural contract, and no LLM review cycle operates on state that has not been mechanically verified against that contract. Sibling to the [Coupling Principle](principles/coupling.md): coupling governs within-file content health, validation governs across-file structural health. See [The Validation Principle](principles/validation.md).

**Validator.** Mechanical check (pure code, no LLM) of a representation's [structural invariants](#s) against its contract. Exhaustive and cheap; free of the add-bias that compromises LLM-based structural fixes.

**V-cycle (Review V-Cycle).** Multi-scale review architecture composing local, regional, and full scales into upward and downward passes. Inspired by multigrid methods in numerical analysis. See [Review V-Cycle](design-notes/review-v-cycle.md).

**Verify the whole.** Stepping back to original scope after narrowing, to check that the refined pieces cohere. See [Verify the Whole pattern](patterns/verify-the-whole.md).

**Vocabulary (YAML field).** Per-claim dictionary of symbols and their meanings. Shared across the note through aggregation.

**Vocabulary bridge.** Mapping domain language to structural language once so downstream proofs can cite domain concepts grounded in formal structure. See [Vocabulary Bridge pattern](patterns/vocabulary-bridge.md).

**Vocabulary firewall.** See Firewall, vocabulary.

## Y

**YAML (`.yaml`).** The per-claim metadata file. Holds label, name, type, summary, depends, vocabulary. The authoritative source for all metadata.
