# Glossary

Terms specific to this reasoning system. Cross-references point to where each term is discussed substantively.

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [Y](#y)

## A

**Accretion.** Growth of the reasoning lattice by adding new properties rather than mutating existing ones. The discipline that prevents [Contract Sprawl](equilibrium/contract-sprawl.md). See [Accretion pattern](patterns/accretion.md).

**Apex (cone apex).** The high-dependency property at the center of a [dependency cone](patterns/dependency-cone.md) — the one that keeps getting revised while its dependencies remain stable.

**ASN (Abstract Specification Note).** A reasoning document covering one topic. The unit of work in the methodology. Declares its dependencies, contains properties, participates in the lattice.

**Assembly.** The stage that exports formalized properties into `formal-statements.md` and `dependency-graph.yaml` for downstream consumers. Mechanical, no LLM.

**Attractor, Genesis.** A property that becomes the default home for every fact anyone needs about a concept it introduces. Cause of [Contract Sprawl](equilibrium/contract-sprawl.md).

**Authority.** A source the reasoning system consults — for example, Nelson's design documents (theory authority) or Gregory's implementation (data authority). See [Two Data Authorities](patterns/two-data-authorities.md).

**Axiom.** A property classified as assumed rather than derived. Stated without proof.

## B

**Blueprinting.** The stage that decomposes a reasoning document into per-property file pairs (YAML metadata + MD body). Produces the structure formalization operates on. See [blueprinting guide](guides/formalization.md).

**Boundary observation.** An out-of-scope finding captured during investigation — enough context to seed a new investigation without expanding the current one. Seed for [scope promotion](patterns/scope-promotion.md).

**Bridge citation.** A citation to a property that licenses an inference step between two other concepts in a proof. Missing bridge citations are a subtype of [Citation Drift](equilibrium/citation-drift.md#subtype-bridge-citations).

## C

**Campaign.** A discovery effort investigating a specific question. Produces one or more ASNs and grows the lattice through scope promotion.

**Channel asymmetry.** Shape-mismatch between the theory channel and the data channel. Prevents naive merging and forces synthesis to coin bridging vocabulary. See [Channel Asymmetry pattern](patterns/channel-asymmetry.md).

**Citation, inline.** A reference in the proof narrative like "by NAT-wellorder." Part of proof content, not metadata.

**Cluster scale.** [Verification V-Cycle](design-notes/verification-v-cycle.md) scope between property and system — reviewing a dependency cone as a unit.

**Cone, dependency.** A cluster of tightly coupled properties where an apex keeps being revised while dependencies are stable. See [Dependency Cone pattern](patterns/dependency-cone.md).

**Cone review.** Focused review of a specific dependency cone with apex + dependencies as context. Resolves the cluster as a constraint system.

**Cone sweep.** Proactive cluster-scale review walking the dependency graph bottom-up, running cone review on every property meeting the dependency threshold.

**Consult authority.** During revision, return to source material to ground findings in evidence. See [Consult Authority pattern](patterns/consult-authority.md).

**Content.** What the `.md` file holds — narrative, proof, formal contract claims. Distinct from metadata.

**Contract, formal.** The structured claim section of a property (`*Formal Contract:*`): preconditions, postconditions, invariants, axiom, definition. Part of content.

**Contract Sprawl.** A property's formal contract keeps growing across cycles because it is a [Genesis Attractor](equilibrium/contract-sprawl.md). See [Contract Sprawl](equilibrium/contract-sprawl.md).

**Corollary.** A property classified as an immediate consequence of another.

## D

**Data channel.** The agent channel that reads raw evidence (implementation code, experimental measurements) and reports patterns. Forbidden from using theory-level vocabulary. See [Two Data Authorities](patterns/two-data-authorities.md).

**Definition.** A property classified as introducing named concepts or operations.

**Depends (YAML).** The structured dependency list in a property's YAML file. The authoritative metadata for dependencies.

**Design requirement.** A property classified as an architectural or measurement constraint the system imposes.

**Discovery.** The stage producing reasoning documents through the [two-channel architecture](patterns/two-data-authorities.md). First stage of the pipeline. See [discovery guide](discovery.md).

**Document lattice.** The coarse granularity of the [reasoning lattice](patterns/reasoning-lattice.md) — ASNs as nodes, inter-document dependencies as edges.

**Drift, Citation.** The state where citations (YAML depends + inline prose) no longer match the dependencies a proof actually uses. See [Citation Drift](equilibrium/citation-drift.md).

**Driver (Citation Drift).** The cause class that produces drift.
- **Internal driver** — active work inside the same ASN produces drift within that ASN. Continuous.
- **Passive driver** — work in an upstream ASN produces drift in downstream consumers. Event-driven.

**Downward pass.** Second phase of the [V-cycle](design-notes/verification-v-cycle.md) — re-verifying at narrower scales after wider-scale corrections.

**Domain language emergence.** The process by which the system coins new prose words for concepts it will reason with, as two-channel synthesis and subsequent review cycles produce claims existing vocabulary can't express. See [Domain Language Emergence](design-notes/domain-language-emergence.md).

## E

**Enumerated surface.** A property structure that pre-identifies where sub-facts will live (e.g., `T10a.1`, `T10a.2`, ...). Invites [accretion](patterns/accretion.md); prevents Genesis Attractors forming.

**Evidence space.** The space of observed behaviors and measurements the data channel reports. Complement to [hypothesis space](#h).

**Excavation stages.** The predictable stages review/revise findings progress through as cycles deepen: citation accuracy → completeness → structural coherence → mathematical precision → structural organization → prose clarity. See [Review/Revise Iteration](patterns/review-revise-iteration.md).

**Extract/Absorb.** Finding shared concepts across multiple properties and factoring them into new foundation layers. How the lattice grows inward. See [Extract/Absorb pattern](patterns/extract-absorb.md).

## F

**Firewall, vocabulary.** Structural enforcement that the theory channel cannot use data-channel terms and vice versa. Prevents the LLM's training knowledge from shortcutting reasoning. See [Two Data Authorities](patterns/two-data-authorities.md).

**Formal-statements export.** Curated export containing all property summaries and formal contracts in dependency order. Written to `vault/project-model/ASN-NNNN/formal-statements.md`. Consumed by downstream ASNs as foundation.

**Formalization.** The stage that rewrites proofs to Dijkstra standard, produces formal contracts, and runs the V-cycle to convergence. See [formalization guide](guides/formalization.md).

**Foundation.** From a downstream ASN's perspective, any upstream ASN it depends on. Foundation content is read-only context for the downstream's review cycles.

**Full-review.** System-scale review reading an entire ASN. Finds issues invisible to narrower scales: carrier-set conflation, precondition chain gaps, vocabulary collisions, issues in small properties. Renamed from cross-review.

## G

**Genesis Attractor.** See Attractor, Genesis.

**Ground state.** The state of genuine convergence across all scales — property, cluster, and system review all agree there are no remaining issues. Distinguished from "stopped" (no finding in one scale but others can still expose issues). See [V-cycle self-evaluation](design-notes/verification-v-cycle.md#the-v-cycle-as-self-evaluation).

## H

**Hypothesis cluster.** A [cone](patterns/dependency-cone.md) in a science deployment: apex (hypothesis statement) plus its supporting dependencies (axioms, definitions, data citations, coined concepts). Regional convergence of a hypothesis cluster = hypothesis ready for its scope. See [Science Approach](science/README.md).

**Hypothesis space.** The space of candidate principles and concepts that could organize a domain. Explored by the theory channel. Complement to [evidence space](#e). New [prose coinage](patterns/prose-coinage.md) is a form of hypothesis generation.

## I

**Internal driver.** See Driver.

## J

**Join.** Lattice operation. A new node is created above multiple foundations. [Scope promotion](patterns/scope-promotion.md) executes a join.

## L

**Label.** A property's stable citable handle (e.g., `T0`, `NAT-wellorder`, `TA-Pos`). Set at blueprinting, never changes.

**Lattice, reasoning.** The network of verified properties connected by explicit dependencies. Grows outward through [scope promotion](patterns/scope-promotion.md), inward through [extract/absorb](patterns/extract-absorb.md). See [Reasoning Lattice pattern](patterns/reasoning-lattice.md).

**Lemma.** A property classified as an intermediate result supporting higher-level theorems.

**Local-review.** Property-scale review checking logical gaps, unjustified steps, missing cases, and dependency correctness. One property at a time with its dependencies as fixed context. Renamed from proof-review.

## M

**Markdown body (`.md`).** The file that holds a property's content: narrative, proof, formal contract.

**Meet.** Lattice operation. A concept shared by two nodes is extracted into a new foundation layer below both. [Extract/absorb](patterns/extract-absorb.md) executes a meet.

**Metadata.** What the YAML file holds — label, name, type, summary, depends, vocabulary. Describes the property; does not constitute its reasoning.

**Modeling.** The stage translating formal contracts into mechanically verifiable code (Dafny, Alloy). Follows formalization.

## N

**Narrow → Refine → Verify.** The three-phase cycle every process in the system follows. The primary pattern, rooted in the scientific method. See [Narrow → Refine → Verify](patterns/narrow-refine-verify.md).

## O

**Open surface.** A property structure that leaves no explicit home for new sub-facts (e.g., "with its standard properties"). Sets the conditions for a [Genesis Attractor](equilibrium/contract-sprawl.md) to form.

**Over-citation.** A Depends entry for a property the proof doesn't actually use. A form of [Citation Drift](equilibrium/citation-drift.md).

## P

**Passive driver.** See Driver.

**Pattern language.** The 12+ patterns that govern how agents produce verified knowledge. See [patterns README](patterns/README.md).

**Property.** A single unit of reasoning within an ASN. Has a label, type, formal contract, and dependencies. The cited building block of the lattice.

**Prose coinage.** The atomic event of coining a new prose word for a concept no existing vocabulary captures precisely (e.g., "action point," "divergence," "subspace"). Occurs in two modes: [synthesis coinage](#s) and [review coinage](#r). Precedes [prose compression](patterns/prose-compression.md). See [Prose Coinage pattern](patterns/prose-coinage.md).

**Prose compression.** A prose-named concept gets a symbol for compact formal manipulation (e.g., "tumbler addition" → `⊕`). Same concept, compressed form. Produced by [review/revise iteration](patterns/review-revise-iteration.md) as concepts are used frequently enough that compact notation pays for itself. See [Prose Compression pattern](patterns/prose-compression.md).

**Property lattice.** The fine granularity of the [reasoning lattice](patterns/reasoning-lattice.md) — individual properties as nodes, per-property dependencies as edges.

**Property scale.** [Verification V-Cycle](design-notes/verification-v-cycle.md) scope of one property with its dependencies as fixed context.

## R

**Rebase.** Re-verifying downstream properties after a foundation changes. Happens automatically via review/revise cycles because changed dependencies invalidate dependents' metadata.

**Representation change.** Progressive transformation of content through different forms (narrative → structured → formal → mechanical) without changing the underlying claim. See [Representation Change pattern](patterns/representation-change.md).

**Review coinage.** [Prose coinage](patterns/prose-coinage.md) that happens during review/revise cycles rather than at synthesis. Occurs in both discovery and formalization. Roughly 30% of an ASN's coinages. Driven by reviewer pressure surfacing a concept the current text is discussing in ad-hoc prose without a shared name. See [Synthesis coinage](#s) for contrast.

**Review/revise iteration.** Repeating cycles of review (finding issues), revision (fixing them), and re-review until convergence. See [Review/Revise Iteration pattern](patterns/review-revise-iteration.md).

**Reviewer.** The agent that reads content and produces findings. Does not modify.

**Reviser.** The agent that reads a finding and modifies the content to address it. Always paired with a reviewer.

## S

**Scale.** Scope of a review cycle. Three canonical scales: property, cluster, system. See [Verification V-Cycle](design-notes/verification-v-cycle.md).

**Scientific method.** Lineage of the primary pattern — narrow scope, refine through iteration, verify coherence. Every process in the system follows this rhythm.

**Scope narrowing.** Breaking work into smaller tractable pieces by constraining context. See [Scope Narrowing pattern](patterns/scope-narrowing.md).

**Scope promotion.** Elevating out-of-scope boundary observations into their own first-class investigations. How the lattice grows outward. See [Scope Promotion pattern](patterns/scope-promotion.md).

**Scoped inquiry.** Decomposing a question along authority boundaries, with each channel investigating what it can evaluate. See [Scoped Inquiry pattern](patterns/scoped-inquiry.md).

**Self-healing rebase.** When a foundation property changes, dependents automatically re-verify through the same narrow → refine → verify cycles that built them.

**Signal.** A mechanical indicator that a disequilibrium pattern is occurring (e.g., a property's contract growing across cycles signals [Contract Sprawl](equilibrium/contract-sprawl.md)).

**Sprawl.** See Contract Sprawl.

**Summary.** 1-3 sentence YAML field describing what a property claims. Produced by the summarize step. Used by downstream foundation loading.

**Summarize.** The step that regenerates the `summary` YAML field using batched LLM calls. Prerequisite to assembly.

**Synthesis.** The step integrating theory-channel and data-channel outputs into a structured reasoning document with dependency-mapped claims.

**Synthesis coinage.** [Prose coinage](patterns/prose-coinage.md) that occurs at the synthesis step when two-channel outputs are reconciled. Roughly 70% of an ASN's coinages happen here, because synthesis is where incompatible vocabularies must be merged into a single reasoning document and no existing word may fit precisely. Contrasts with [review coinage](#r) which happens during later review/revise cycles.

**System scale.** [Verification V-Cycle](design-notes/verification-v-cycle.md) scope of the whole ASN with full foundation context.

## T

**Theorem.** A property classified as a proven result.

**Theory channel.** The agent channel that consults established theory (design documents, domain models) and makes predictions. Forbidden from referring to specific data. See [Two Data Authorities](patterns/two-data-authorities.md).

**Transclusion.** Including one document's content by reference, not by copy. A Xanadu protocol primitive and the mechanism by which the [reasoning lattice](patterns/reasoning-lattice.md) shares content across nodes.

**Two data authorities.** The two-channel architecture with vocabulary firewall separating theory from data. See [Two Data Authorities pattern](patterns/two-data-authorities.md).

**Type.** YAML classification of a property: axiom, definition, design requirement, lemma, theorem, corollary.

## U

**Under-citation.** A proof uses a property that its Depends list doesn't include. The most common form of [Citation Drift](equilibrium/citation-drift.md).

**Upward pass.** First phase of the [V-cycle](design-notes/verification-v-cycle.md) — local review → contract review → cone sweep → full-review, building confidence from narrow to wide scope.

## V

**V-cycle (Verification V-Cycle).** Multi-scale review architecture composing property, cluster, and system scales into upward and downward passes. Inspired by multigrid methods in numerical analysis. See [Verification V-Cycle](design-notes/verification-v-cycle.md).

**Verify the whole.** Stepping back to original scope after narrowing, to check that the refined pieces cohere. See [Verify the Whole pattern](patterns/verify-the-whole.md).

**Vocabulary (YAML field).** Per-property dictionary of symbols and their meanings. Shared across the ASN through aggregation.

**Vocabulary bridge.** Mapping domain language to structural language once so downstream proofs can cite domain concepts grounded in formal structure. See [Vocabulary Bridge pattern](patterns/vocabulary-bridge.md).

**Vocabulary firewall.** See Firewall, vocabulary.

## Y

**YAML (`.yaml`).** The per-property metadata file. Holds label, name, type, summary, depends, vocabulary. The authoritative source for all metadata.
