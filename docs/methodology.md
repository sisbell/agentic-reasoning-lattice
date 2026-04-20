# Methodology

A human poses a question. The system decomposes it into channel-appropriate sub-questions, launches a structured multi-agent discovery process, and grows a lattice of verified knowledge. The lattice accumulates every finding, revision, and proof as permanent, addressable, dependency-tracked nodes. The methodology is one rhythm applied at every scale: narrow scope, refine through iteration, verify coherence.

![Methodology pipeline](diagrams/methodology-pipeline.svg)

The unit of work is the note (identifier prefix `ASN-NNNN`) — a document covering one topic. Notes form a dependency lattice: each declares what it depends on and what it covers, building on verified foundations. At any point, some notes may be in discovery, others in formalization, others under V-cycle review. The dependency order determines which must stabilize first.

## [Discovery](discovery.md)

Two independent agent channels investigate the question. The theory channel consults established domain knowledge. The data channel analyzes raw evidence. A vocabulary firewall prevents each from using the other's terms — the data channel reasons from evidence alone, forcing hypothesis space exploration rather than retrieval of known solutions.

Each inquiry is decomposed into channel-appropriate sub-questions before consultation begins — theory channel questions framed for hypothesis space, data channel questions framed for evidence space. Neither channel sees the other's sub-questions. A synthesis step integrates both channels into a structured note with dependency-mapped claims. Where the channels agree, principles are validated. Where they disagree, new hypotheses emerge.

Out-of-scope findings flagged during review become candidates for new inquiries, attaching to the lattice as new nodes. The system discovers the questions it should be asking, not just answers to questions posed. This is [scope promotion](patterns/scope-promotion.md) — how the lattice grows outward.

## [Blueprinting](blueprinting.md)

Blueprinting is the meet operation on the lattice: a note-level node becomes many claim-level nodes. A note with dozens of interleaved claims is decomposed into atomic units — one file per claim, dependencies mapped, vocabulary extracted. Each claim is classified (axiom, definition, design requirement, lemma, theorem, corollary) and gets its own statement, justification, and proof.

This decomposition is what makes the V-cycle possible. Claims can be reviewed independently at narrow scope, grouped into clusters at regional scope, and reassembled at document scope. Without blueprinting, the V-cycle has nothing to traverse.

## [The V-Cycle](design-notes/review-v-cycle.md)

The V-cycle is the core of the methodology. It traverses the lattice at three scales, each handling the error class it is efficient at. The architecture is inspired by multigrid methods in numerical analysis (Brandt 1977): multi-scale cycling converges faster than single-scale iteration by matching the solver to the error structure.

**Descend through meets** — decompose to local scale:

- **Local review** — each claim reviewed independently with its dependencies as fixed context. Checks logical gaps, missing cases, dependency correctness, formal contract completeness.
- **Contract review** — validates that each formal contract (preconditions, postconditions, invariants, frame conditions) matches the proof.

**Review at regional scale** — [dependency cones](patterns/dependency-cone.md):

- **Regional sweep** — walks the dependency graph bottom-up. When tightly coupled claims stall single-scale review (one claim thrashing while its dependencies are stable), the cone is detected and reviewed as a unit with focused context. Each cone converges before moving to the next.

**Ascend through joins** — recompose to full scale:

- **Full-review** — full note scan with foundation context. Catches what narrower scales miss: conflation of distinct concepts, precondition chain gaps across distant claims, scope mismatches between proof and narrative.

**Descend again** — verify corrections:

- Any claim changed during the upward pass is re-verified at local and regional scale on the downward pass.

Each scale converges before passing to the next — an adiabatic protocol. The V-cycle repeats until no scale changes anything in a full pass.

**Mechanical verification** (Dafny proofs, Alloy bounded model checking) is a validation layer within the V-cycle. It confirms that converged contracts are logically consistent and faithfully encoded. But the V-cycle catches what mechanical verification cannot — a theorem (GlobalUniqueness) passed Dafny, Alloy, and 30+ single-scale review cycles. Multi-scale review found a counterexample in 8 cycles. The V-cycle discovers; mechanical verification validates.

See the [V-cycle design note](design-notes/review-v-cycle.md) for the theoretical grounding and multigrid analogy.

![Review V-Cycle](diagrams/review-v-cycle.svg)

## The Oracle

Each verified lattice node is a testable prediction: preconditions, postconditions, invariants, formal contract. When a prediction fails against data, the reasoning trail traces the failure back to the specific claim and evidence channel that diverged. This traceability is not instrumented after the fact — it is structural. Every dependency is explicit and permanent. Every finding has a source.

The oracle is the mechanism that makes the lattice systematically improvable. Every failure points to exactly where the reasoning needs revision. The V-cycle re-verifies the affected node and propagates corrections upward through dependents. The lattice self-heals because the oracle identifies not just that something failed, but where and why.

## Self-Healing

When a foundation claim changes, dependents re-verify automatically through the same V-cycle that built them. The lattice self-heals because every dependency is explicit and tracked. A fix at the foundation propagates upward: dependent claims are flagged, re-enter the V-cycle, and adapt. Demonstrated when the GlobalUniqueness fix cascaded through 4 dependent claims that re-verified without manual intervention.

This is a property of the lattice structure, not a feature bolted on. Permanent addresses mean claims never lose their identity. Bidirectional dependencies mean changes are visible in both directions. The V-cycle means re-verification follows the same rhythm that produced the original verification.

## The Pattern Language

Twelve patterns govern how the system operates. They were discovered through operation — each observed before it was named. The primary pattern is [narrow → refine → verify](patterns/narrow-refine-verify.md), the scientific method operationalized for agents. The remaining patterns describe what happens in practice: when review stalls ([dependency cone](patterns/dependency-cone.md)), how questions decompose ([scoped inquiry](patterns/scoped-inquiry.md)), how domain and formal language connect ([vocabulary bridge](patterns/vocabulary-bridge.md)), how the lattice grows ([scope promotion](patterns/scope-promotion.md), [extract/absorb](patterns/extract-absorb.md)).

The patterns compose — every process in the system, at every scale, follows the same narrow → refine → verify rhythm. Discovery narrows questions to channels. Blueprinting narrows documents to claims. The V-cycle narrows review to the scale that matches the error. The pattern language systematically reduces wasted agent computation by routing each problem to the scope that can resolve it.

See [Pattern Language for Agentic Reasoning Systems](patterns/README.md) for the full catalog.

## What the Methodology Produces

The methodology produces a lattice with algebraic structure:

- **Meet** — shared concepts extracted into new foundation layers below both consumers. Blueprinting executes meets. [Extract/absorb](patterns/extract-absorb.md) executes meets: shared definitions become foundation nodes that dependents reference.
- **Join** — new nodes created above multiple foundations. Synthesis executes joins. [Scope promotion](patterns/scope-promotion.md) executes joins: out-of-scope findings become first-class investigations connecting to existing nodes.

The lattice order — which nodes depend on which — is discovered, not imposed. Foundation layers emerge when multiple higher-level documents independently define the same concept. New domain vocabulary emerges because the mathematics requires it, not prescribed in advance.

Every review cycle, finding, and revision is a permanent artifact in the lattice with the same verified, addressable, dependency-tracked structure as the knowledge it produces. The system's operational history is part of the lattice itself.

## What Verification Proves and What It Cannot

**Contracts** are the claims — preconditions, postconditions, invariants. They say what the system guarantees.

**Proofs** are the reasoning that justifies those claims. The proofs can have gaps, and the claims can still be true. A correct contract with a flawed proof is better than no contract at all.

**The V-cycle** checks that contracts are precise, internally consistent, and faithful to the derivation — at three scales. It operates on text and can be wrong, but multi-scale convergence catches what single-scale misses.

**Mechanical verification** (Dafny, Alloy) proves logical consistency. But it cannot tell you whether a postcondition describes what the system *should* do (that is a design question), whether the axioms are the right axioms (those are posited from evidence), or whether the formalized specification matches reality (that requires testing).

**Golden tests** close the final gap — running verified contracts against the real system checks whether the specification matches reality.

The chain of trust: human judgment establishes intent, the V-cycle makes it precise, mechanical verification makes it consistent, testing makes it real.

## Origin

This methodology was developed to formalize the Xanadu hypertext system — a domain where design authority (Ted Nelson) and implementation evidence (Roger Gregory's udanax-green) exist but no formal specification does. What emerged from operating the system was the recognition that the lattice, the pattern language, and the V-cycle constitute a general methodology independent of the domain being formalized. The methodology is the generalization. Xanadu is the origin.