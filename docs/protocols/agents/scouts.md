# Scouts

*The caste-defining act is detection-and-report. A scout's working surface is some structural property of the substrate (validator rules, bridge subgraph density, structural form); a fire reads that surface, decides what is or isn't there, and emits findings as substrate facts.*

This document surveys the two scout agents in `scripts/lib/agents/scouts/`. One is fully implemented; the other is a registered stub whose body is pending implementation.


## What a scout is

A scout is an agent whose primary substrate effect is *making detection results auditable*. The scout's working surface is structural — it reads the substrate (or external structural facts about content the substrate addresses), runs detection logic *inside the agent*, and emits the detection result as substrate facts: an audit/report classifier doc plus per-finding tuples.

Per `protocols/substrate/`:

- *Substrate side* (canonical shape catalog): a scout's primary emissions are Coverage-shape `review.structural` (or analog) classifier tuples and Comment-shape `comment.violation` (or other K) tuples. Comment shape `(1, 1, A_doc, A_doc, ⊥)` is non-idempotent: each detected violation is a distinct event, even if structurally similar to previous ones.
- *Agent spec* (AG3 + AG5): every emission carries provenance binding `name_A → addr(emission)`. AG4 (DecisionOpacity) keeps the detection logic itself private; AG5 (PublicPrivateAsymmetry) is what makes "substrate sees only the result" structural rather than incidental.
- *Progress-discipline* (per `quiescence.md` Layer 2): a scout's emission contract `Post_A` is satisfied by the audit/report classifier emission. After a fire, the *skip-when* predicate (typically `is_*_fresh`) flips ⊥→⊤ for the just-audited target; since the trigger is `T_A ≡ ¬is_*_fresh ∧ in_scope`, the trigger therefore evaluates ⊥ on that target. Progress-discipline holds: `T_A[Σ](args) = ⊤ ⟹ T_A[Σ'](args) = ⊥`. The trigger skips the just-audited target until staleness recurs (e.g., upon underlying-content edit). Q3 then makes this discipline statically checkable from the emission contract.

**What distinguishes a scout from a producer:** detection happens *inside the agent*. A producer takes a decision made elsewhere (operator, upstream LLM, derivation logic) and persists the result. A scout's substrate emissions encode the result of its own detection logic — the validator runs *here*, the similarity service runs *here*, the gap analysis runs *here*. This is the architectural distinction the `claim_structural_audit` docstring foregrounds: *"Detection happens here, distinguishing this from a producer that just persists detection done upstream."*

**Empty-result emissions are still emissions.** A scout that finds nothing emits the audit/report classifier anyway. The substrate fact "audit ran at moment T on target d" is what makes the `is_*_fresh` predicate evaluable; without the empty-result emission, a clean target would never have a fresh audit doc and the trigger would re-fire indefinitely.

The audit-doc emission itself is *always non-empty* — Coverage shape with `c_G = 1`, targeting the audited entity. What is empty on a zero-finding fire is the *per-finding decomposition*: the canonical Provenance shape `(1, 0|1, A, A, ⊤)` admits `c_G = 0|1` precisely so a `provenance.derivation(audit → ∅)` tuple can record "operation ran with zero output" honestly. The audit doc's existence is what makes `is_*_fresh` evaluable; the empty-derivation tuple at Provenance is what records the zero-decomposition fact.


## Caste-internal structure

Every runner-walked scout has the same shape:

| Component | Role |
|---|---|
| Working surface | A structural property the scout reads — validator output, bridge subgraph topology, etc. May be substrate-resident (link graph) or external-but-substrate-addressable (file content of A_doc-addressed documents) |
| Scope query | Yields candidate target addresses — typically per-target document addresses (per-claim, per-pair, per-region) |
| Skip-when predicate | A `PL` Boolean — true when the most recent audit/report on the target is fresh and complete (`is_*_fresh`, `is_*_audit_clean_or_in_flight`) |
| Trigger-fires-when | NOT skip-when AND in scope (target is stale or has never been audited) |
| Action | Run detection logic over working surface; emit classifier doc + per-finding tuples (or empty audit on null-finding) |
| Substrate emissions | Always: report-classifier + `review.coverage` (or analog) targeting the audited target. Per finding: `finding` classifier + `comment.<violation_kind>` + `provenance.derivation(report → finding)` |
| Out-of-band side effects | None typically — scouts read but do not edit. (Distinct from refiners and operator-gated producers.) |
| Substrate progress | Each fire flips `is_*_fresh(target)` from ⊥ to ⊤. The trigger skips the just-audited target until staleness recurs. |

*Note on Q4 unit.* Scouts are per-target with batch finding emission: args = target-address; one fire emits zero or more findings on that target, all under one Q4-unit. The trigger flips per-target, not per-finding-emitted, exactly like batch refiners.

*Note on staleness.* The `is_*_fresh` predicate is what determines re-fire. Staleness conditions vary per scout — content edit on the audited target, time-based, structural-change-triggered, or substrate-edge-based. This is a design choice on the scout's predicate, not a substrate-spec commitment.


## Runner-walked scouts


### `claim_structural_audit` — per-claim structural scout

| Field | Value |
|---|---|
| Trigger name | `claim-structural-audit` |
| Granularity | per-claim |
| Scope query | each claim-classified derivation of the requested ASN's source note (`per_claim_of_asn`); or every claim (daemon) |
| Skip-when predicate | `is_claim_audit_fresh(claim)` — skip if the latest structural audit was clean OR its findings are still in flight (have unresolved comment.violations awaiting refiner closure) |
| Working surface | structural form of the claim — validator rules over the claim's md content. The validator runs *inside the agent* (loaded from `claim-validate.py` via importlib). |
| Substrate emissions | Always: audit doc with `review.structural` classifier + `review.coverage(audit → claim)`. Per violation: `finding` classifier + `comment.violation` link targeting the claim + `provenance.derivation(audit → finding)`. Even on zero-violations fires, the audit doc is emitted (empty-derivation pattern). |
| Out-of-band | None (read-only on the working surface) |
| Emission contract sketch | `Post_A(claim, Σ, E) ≡ ∃ (K_review.structural, F, G) ∈ E :: claim ∈ coverage(G)` — the audit-doc-with-coverage emission is required regardless of finding count |
| Trigger flip | After fire, `is_claim_audit_fresh(claim) = ⊤`; predicate skips it until staleness (typically: claim content edit) |
| Cross-caste partner | refiner `claim_structural_revise` (closes the `comment.violation` tuples this emits) |

**Architectural notes:**

The classifier subtype `review.structural` parallels `review.content` (used by content reviewers like `full_review`). They share the Coverage shape — the K subtype is the discriminator. This is the same shape-vs-K distinction surfaced in `refiners.md`: one mechanism (`review` shape + `is_*_fresh` predicate machinery) handles both content and structural review channels because the K differentiates use cases without requiring shape divergence.

Detection happening inside the agent matters for AG4 / Q1: the validator's decisions are deterministic and could in principle be reflected into `PL` (per the *transparent agent subclass* open question in `agents.md`), but the substrate spec keeps `act_A`'s body opaque uniformly. The scout's emissions are the only public artifact of its detection.


## Stub / planned scouts


### `bridge_probe` — cross-lattice bridge-discovery scout (STUB)

| Field | Value |
|---|---|
| Trigger name | (none registered yet — stub) |
| Granularity | per (local_claim, remote_lattice) pair |
| Scope query | (pending) — cross-lattice candidate pairs |
| Skip-when predicate | (pending) — likely "bridge from local_claim to remote_lattice is fresh / saturated" |
| Working surface | bridge subgraph: cross-lattice citation links, bridge-member edges, similarity scores from a SimilarityService |
| Detection loop (per the docstring) | (1) similarity hypothesis-probe; (2) structural expansion via cones; (3) region-bounded hypothesis-probes; (4) confirmation; (5) bridge-graph gap analysis |
| Substrate emissions (planned) | cross-lattice `citation` links from confirmed matches; `bridge_member` edges (when a bridge aggregates multiple confirmed matches); a saturation marker on the bridge doc when gap analysis indicates the bridge is mature |
| Out-of-band | None typically — read-only on the working surface; the LLM judge inside the SimilarityService is an internal decision tool, not a substrate edit |
| Cross-caste partner | downstream synthesis producer (planned) — reads saturation markers as its trigger |

**Status.** Architectural skeleton is in place (Agent class shape, helper-service split between this scout and `lib/scout_services/`); the discovery loop body raises `NotImplementedError`. Real implementation lands when probe-agent work begins.

**Architectural notes:**

bridge_probe's scope is *cross-lattice* — it operates at the system scope tier (Q10 of `quiescence.md`). This puts it in a different tier from `claim_structural_audit` (per-claim, lattice-internal). Cross-tier scouts have an additional operational property: their emissions can flip *outer-tier* triggers from ⊥ to ⊤. A new cross-lattice citation can affect lattice-quiescence on either side.

The saturation marker pattern is interesting. The scout does not synthesize or extract — it emits a structural fact ("this bridge is mature") that some downstream producer's trigger reads. This is the *substrate-mediated handoff* pattern: scout decides "ready," producer fires on that fact. The same pattern surfaces in operator-gated lattice ops (modify-then-self-review) where the modify step emits a review and the refiner picks it up. The distinction is who decides ready: an operator (gate-driven) vs. the substrate's gap analysis (scout-driven). Architecturally, both are *substrate-mediated trigger handoffs*; only the source of decision-making differs.


## Cross-caste patterns


### Scout-refiner pair (substrate-mediated)

Mirrors the producer-refiner pair in `refiners.md`. The scout emits a comment-shape tuple (here: `comment.violation` rather than `comment.revise`); the refiner's trigger fires on the open comment; the refiner emits `resolution.<kind>` to close it.

| Scout | Comment kind | Refiner |
|---|---|---|
| `claim_structural_audit` | `comment.violation` (on claim) | `claim_structural_revise` |

The shape is identical to producer-refiner — Comment shape on both `comment.revise` and `comment.violation`, Resolution shape closing either. The K subtype is the only structural difference. This is the *one mechanism, K-discriminated channels* pattern surfaced earlier: comment + resolution machinery handles both `revise` (LLM-emitted) and `violation` (validator-emitted) channels with no separate substrate machinery.


### Substrate-mediated trigger handoff

A scout's emission is a *trigger* for a downstream agent. Two variants:

(i) **Comment-as-trigger** — the scout emits `comment.<kind>`; a refiner trigger fires on the open comment. (This is the scout-refiner pair above.)

(ii) **Marker-as-trigger** — the scout emits a non-comment classifier tuple (`saturation`, `bridge_member`, etc.); a downstream producer's trigger reads the marker and fires accordingly.

Both variants follow the substrate spec's substrate-mediated handoff: no orchestrator, no message-passing, no cross-agent coordination. The substrate state is the medium.


### Scout-role activity beyond the caste

The "scout role" — surveying a working surface and emitting findings — is broader than the `scouts/` caste in the codebase. Three populations perform scout-role work:

(a) *Substrate-citizen scouts* (this caste): predicate-fired, validator-or-similar logic runs inside the agent. The two surveyed here.

(b) *Operator-as-scout* (lattice ops `note_absorb`, `note_extract`, `note_clone`): the operator's *decision* is the scout step; the operator emits a spec md describing what they decided. The agent then performs producer/refiner work. (See `refiners.md` for `note_absorb`; `producers.md` for the others.)

(c) *LLM-as-scout* (`note_promote_open_questions`, `note_promote_out_of_scope`): the operator triggers the scan; the LLM-inside-the-agent decides which items earn new identity. The agent persists the LLM's decisions. The `note_promote_*` docstrings explicitly note this: *"The LLM plays the scout role here; the operator is the trigger."*

The classification "scout caste" reflects the *primary substrate effect* (substrate-citizen detection-and-report). Scout-role activity in the broader sense is distributed across operator gates and LLM decisions inside producer-classified agents. The protocol layer (`maturation/note-to-claim.md` and any future Stigmergic Protocol specializations) is where these scout-role activities compose end-to-end.


## Caste-level observations

(a) *Detection inside the agent is the caste signature.* Scouts run their detection logic during the fire (validator, similarity service, gap analysis). The substrate sees only the result. This contrasts with producers, which persist decisions made elsewhere (operator, upstream LLM).

(b) *Scouts always emit, even on null findings.* The empty-derivation pattern at Provenance shape (`c_G = 0|1`) is what makes "fire produced zero outputs" recordable; the audit-doc Coverage emission is what makes `is_*_fresh` evaluable. A scout that fires on a clean target and emits nothing would be observationally indistinguishable from never having fired — which would break *progress-discipline* (per `quiescence.md` Layer 2's discipline definition): the trigger would remain ⊤ and re-fire indefinitely. Q3's static checkability of progress-discipline is contingent on the emission contract `Post_A` requiring the audit-doc emission unconditionally; the empty-emission case is the contract's non-vacuity test.

(c) *Working surfaces vary; emission shape is uniform.* `claim_structural_audit` reads claim md content via a validator; `bridge_probe` reads cross-lattice citation graph + similarity. Both emit the same shape: a coverage-classifier tuple targeting the surveyed entity, plus per-finding decompositions. The shape uniformity is what lets the runner walk all scouts with one trigger machinery; the working-surface variation is what makes scouts substantive.

(d) *Scope tiers can diverge across scouts.* `claim_structural_audit` is per-claim (within-lattice); `bridge_probe` is cross-lattice (system tier). Same caste, different scope tiers. This is consistent with Q10 — the canonical scope tiers are operationally meaningful at every caste; a caste does not commit to a single tier.

(e) *Cross-tier scouts can break inner-tier quiescence.* A `bridge_probe` fire (system tier, `S_system`) emitting cross-lattice citations can target lattice-internal documents, flipping a per-claim trigger from ⊥ to ⊤ (e.g., a new citation may require a structural audit re-fire on the affected claim). By Q9 (ScopeMonotonicity), system-quiescence implies lattice/local-quiescence — but the converse fails, so an outer-tier fire under inner-tier quiescent windows is exactly the *cross-tier interference* scenario flagged as an open question in `quiescence.md`. Scout caste design at outer tiers must consider the in-flight-emission targeting policy: which inner-tier triggers do this fire's emissions touch, and does the protocol expect those to be stable when the outer scout fires?

(f) *Stub agents in the registry are honest about non-implementation.* `bridge_probe` raises `NotImplementedError` from `run()`. The architectural skeleton is registered (the Agent class, helper services); the body is pending. This is an honest agentic-system convention — accidental fires are loud — that other casts may follow as they expand.

The spec status of stubs is split: stubs are *registration-compliant* (AG0 unique address, AG1 trigger and scope signatures registered, AG3 provenance binding declared) but only *conditionally execution-compliant* — `act_A` does not yet produce a well-formed emission set per AG2 (ActionWellTypedness). Execution compliance is deferred to implementation. The honest stance is that stubs pass the spec's static checks at registration time and explicitly fail at execution time; the runner never reaches their action body because the trigger is not yet registered (or fires only when the operator gates it for development testing).


## What is not in this doc

- *Refiner specs.* `claim_structural_revise` (the partner of `claim_structural_audit`) is in `refiners.md`. The cross-caste pair surfaces here at the trigger-handoff level; the closure side is documented there.
- *Producer specs.* The downstream synthesis producer that will consume `bridge_probe`'s saturation markers is in `producers.md` (when written) or pending implementation.
- *Operator-gated work classified as scout-role.* `note_promote_*` agents play scout-role internally but are classified producers because their primary substrate effect is identity-grant. Documented in `producers.md`. The cross-caste section above sketches the population.
- *Stigmergic Protocol composition.* How `claim_structural_audit` → `claim_structural_revise` and (when implemented) `bridge_probe` → synthesis fit into protocol arcs is the protocol-layer's job. `claim_structural_audit → claim_structural_revise` composes into the Note-to-Claim Maturation Stigmergic Protocol; `bridge_probe`'s downstream is cross-lattice and likely warrants its own protocol family within Stigmergic Protocols (not a Maturation specialization).
- *SimilarityService internals.* `bridge_probe` consumes a SimilarityService that's an LLM-judged similarity engine. Its internals are implementation; the substrate sees only the citation emissions and saturation markers the scout produces from it.