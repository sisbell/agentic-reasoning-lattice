# Agents

The agentic layer that builds on the substrate spec. Agents are the *only* operations that emit; everything the substrate observes — claims being decomposed, comments being filed, resolutions being closed, lattice operations being recorded — is the trace of agent fires. This directory documents the agents as they exist in `scripts/lib/agents/`, organized by *caste* (the structural role each agent plays in producing substrate change).

Three caste docs survey the registry:

- [`producers.md`](producers.md) — 20 agents that grant new substrate identity
- [`refiners.md`](refiners.md) — 4 agents that close findings
- [`scouts.md`](scouts.md) — 2 agents that detect and report

(`workers.md` would document the workers caste; the directory `scripts/lib/agents/workers/` exists but currently registers no agents.)

The substrate spec at [`../substrate/`](../substrate/) defines what *any* agent must satisfy (AG0–AG7) and how the runner schedules and detects them (Run0–Run5). This directory documents what *these specific agents* do.


## What a caste is

A caste is the structural role an agent plays in the substrate-emission pattern. The substrate spec's AG5 (PublicPrivateAsymmetry) makes the producer-refiner correction loop architecturally load-bearing; the three castes are the natural decomposition of that loop:

- **Producer** — *grants new identity*. Reads upstream context (substrate state, content, operator spec) and emits a substrate fact that brings something new into the substrate (a classifier, a sidecar attestation chain advance, a coverage relation, a per-finding decomposition). Decision happens *upstream* of the producer; the producer persists a result.
- **Refiner** — *closes findings*. Reads open `comment.*` tuples in scope and emits `resolution.<kind>` (and sometimes `retraction`) to flip the comment from open to closed. Per-comment or per-target batch closure.
- **Scout** — *detects and reports*. Reads a structural working surface (validator rules, bridge subgraph density, structural form), runs detection logic *inside the agent*, and emits findings as substrate facts. Decision happens *here*; the substrate sees the result.

The classification follows *primary substrate effect*. An agent that does multiple things in one fire (e.g., `note_absorb`, which both refines and produces) is classified by what it primarily *changes about the substrate state* — `note_absorb`'s primary effect is closure of the integration question, so it's a refiner.


## Agent registry — at a glance

26 agents across three castes (plus 1 composed sub-routine, `claim_finding_override`, which is not an independent agent).

| Working surface | Producers | Refiners | Scouts |
|---|---|---|---|
| Inquiry stage | `inquiry_consult` | — | — |
| Note stage | `note_draft`, `note_review`, `note_consult`, `note_statements`, `full_review` | `note_revise` | — |
| Claim stage | `cone_review`, `claim_findings`, `citation_resolve`, `claim_signature_resolve`, `claim_describe`, `claim_contract`, `claim_formal_contract` | `claim_revise`, `claim_structural_revise` | `claim_structural_audit` |
| Lattice operations | `claim_decompose`\*, `note_extract`\*, `note_clone`\*, `note_patch`\*, `claim_patch`\*, `note_promote_open_questions`\*, `note_promote_out_of_scope`\* | `note_absorb`\* | — |
| Cross-lattice | — | — | `bridge_probe`† |

\* operator-gated. † stub (architectural skeleton; body pending). All others are runner-walked. The *Lattice operations* row consolidates all eight operator-gated agents in the registry, regardless of which stage their target lives at — they are unified by being substrate-undecidable operations that require operator invocation. The remaining stage rows (Inquiry, Note, Claim) contain only runner-walked agents whose triggers fire from substrate state.

**Stats:**

- Runner-walked: 17 (13 producers + 3 refiners + 1 scout)
- Operator-gated: 8 (7 producers + 1 refiner)
- Stubs (planned runner-walked): 1 (`bridge_probe`)
- Sub-routines (not agents): 1 (`claim_finding_override`)


## Two kinds of caste-to-caste hand-off

How does work pass from one caste to the next? Two distinct mechanisms exist in the registry, and the distinction is the structural mechanic that the rest of these docs lean on. The caste-internal patterns surface here as a unified treatment.

**Stigmergic hand-off.** Caste A emits a substrate fact; caste B's predicate reads that fact and flips false; the runner fires B. No operator involvement; coordination is mediated entirely by the substrate.

Examples:

- `full_review` (producer) emits a `review` classifier → `claim_findings`'s predicate `is_review_decomposed = ⊥` is now true → runner fires `claim_findings` on the review.
- `claim_findings` (producer) emits `comment.revise` per finding → `claim_revise`'s predicate `has_resolution = ⊥` is now true on each new comment → runner fires `claim_revise` on each.
- `claim_structural_audit` (scout) emits `comment.violation` per detected violation → `claim_structural_revise`'s predicate `is_claim_structurally_clean = ⊥` is now true on the audited claim → runner fires the refiner.
- `inquiry_consult` (producer) emits `consultation.answer.*` → `note_draft`'s predicate "inquiry has consultation done ∧ no synthesis from inquiry" is now true → runner fires `note_draft`.
- `note_consult` (producer) emits `consultation.coverage` → `note_revise`'s skip-when predicate `¬all_open_revises_consulted` is now false → runner fires `note_revise`.

The runner walks; the substrate state is the only signal.

**Sequential hand-off.** Caste A produces output (a workspace artifact, or a substrate identity at the boundary of a stage); the operator invokes caste B explicitly. No predicate flip; coordination is operator-driven.

Examples:

- An operator decides a workshop ASN is ready to absorb back → drops a spec md into `_workspace/absorbs/` → invokes `note_absorb`. The decision (when, what, how) is operator-side.
- A producer (e.g., `note_revise`) leaves a note in a state the operator decides is ready for `claim_decompose`. The substrate doesn't auto-fire `claim_decompose`; the operator triggers it because the *decision to derive claims now* is operator-scope.
- A reviewer notices a structural issue not covered by the validator. The operator drops a patch md, invokes `note_patch` or `claim_patch`. The decision to patch is operator-scope.

Sequential hand-offs map to operator-gated invocation. The boundary between stigmergic and sequential is exactly the boundary between runner-walked agents (AG1 holds — `T_A ∈ PL`, `D_A ∈ QD`) and operator-gated agents (AG1 does not hold — invocation is filesystem-mediated, outside the runner's coverage).

**Why both exist.** Stigmergic hand-offs handle work the substrate can self-detect (open comments, stale sidecars, undecomposed reviews). Sequential hand-offs handle work the substrate *cannot* self-decide:

- *Lattice operations* (extract, absorb, promote, clone) — the decision *whether to extract* a claim into a workshop ASN is operator scope; the substrate has no predicate for "this should be extracted now."
- *Stage transitions at decision boundaries* — the decision *whether the note is ready for claim derivation* is operator scope; the substrate could in principle predicate it (e.g., `is_doc_quiescent ∧ is_confirmed`) but in current practice the operator decides.
- *Targeted interventions* — patches, structural overrides — are operator-scope by design.

The two hand-off kinds exist precisely because not every coordination decision can or should be substrate-derivable. The substrate spec's open question on *operator-gated agents as Run5 limit cases* (where the policy module's invocation discipline is human rather than algorithmic) is the formal handle on this distinction.

### The operator-gated population splits further

Looking inside the eight operator-gated agents:

- *(a) Eliminable-by-predicate-registration:* `claim_decompose`, `note_promote_open_questions`, `note_promote_out_of_scope`. Substrate state suffices to write a `T_A ∈ PL` predicate (e.g., `is_doc_quiescent(note) ∧ is_confirmed(note) ∧ ¬has_decomposition_provenance(note)` for `claim_decompose`); current operator gating is cycle-control discipline (operator wants to inspect substrate state before triggering, defer LLM-cost scans, mark explicit protocol stage transitions) rather than substrate-undecidability. Could become runner-walked if cycle-control is delegated via authorization-classifier gates.

- *(b) Operator-as-content-author:* `note_patch`, `claim_patch`, `note_absorb`, `note_extract`, `note_clone`. The agent's input is operator-authored content (patch md, spec md). No substrate predicate can synthesize the content; the operator's authorship is the input.

**The (b)-population is already structurally stigmergic.** Workspace docs are substrate citizens — every spec md has an `A_doc` address per typed-relations.md's address-set partition (`A = A_doc ⊔ A_rel`), and AG3 covers provenance for whatever emission creates the spec doc tuple. The only thing preventing (b)-agents from being runner-walked is that current scripts bundle two distinct roles into one invocation: *(i) operator emits the spec doc + classifier* (operator-as-producer) and *(ii) agent processes the spec* (agent's `act_A`). Splitting these roles — operator emits a `spec.<kind>` classifier on the spec doc; agent's `T_A` reads `has_unprocessed_spec(d)` — makes the agent runner-walked with the operator playing producer-role for the spec emission. Under this split, sequential collapses into stigmergic-with-operator-as-producer.

**Architectural direction.** (a) is eliminable by registering substrate-state predicates. (b) is already structurally stigmergic — what's missing is decoupling the operator-emits-spec step from the agent-processes-spec step. In the limit, all coordination is stigmergic, with two producer populations (substrate-citizen agents and operator-as-content-author) differing in producer identity and emission latency (next-cycle vs operator-decided). The two-hand-off-types description above is the *current operational* distinction; the unified-stigmergic description is the *structural* reading already supported by the substrate spec.


## Stigmergy — the architectural framing (forward-reference)

The stigmergic hand-off is the substrate's primary mechanism for work it can self-detect. Together with sequential hand-offs (for work it cannot), it is what makes the agent registry an agent *system* rather than a list of disconnected actors. Agents do not communicate directly; they leave traces (substrate emissions) that other agents read and respond to. This is exactly stigmergy in the original biological sense (Grassé, *La reconstruction du nid et les coordinations interindividuelles chez Bellicositermes natalensis et Cubitermes sp. La théorie de la stigmergie: Essai d'interprétation du comportement des termites constructeurs*, Insectes Sociaux 6: 41–80, 1959): termites don't tell each other what to do; they leave physical traces in the nest, and other termites act on those traces. The substrate plays the role of the nest; the agent castes play the role of the colony's structural roles.

The full tie-in to the termite analogy — caste differentiation, work-pheromone gradients, stigmergic build-up, quiescence as a saturated nest — is left to the protocol layer ([`../maturation/`](../maturation/)) where end-to-end arcs across multiple castes can be traced. For now, treat the two hand-off types as the working architectural distinction.


## Stigmergic Protocol primitives at the caste boundary

Cross-caste interaction patterns instantiate the Stigmergic Protocol primitives named in the parent [`../README.md`](../README.md). Each primitive's instances in the registry, and the patterns that don't reduce to a single primitive:

- **Correction Stigmergic Protocol** (stigmergic) — the standard correction loop. Agent A emits `comment.<kind>` on a target; agent B reads the open comment as its trigger and emits `resolution.<kind>` to close. The K subtype discriminates use cases without changing the protocol mechanism. Instances:
  - `claim_findings → claim_revise` (K = `comment.revise` on claims)
  - `note_review → note_revise` (K = `comment.revise` on notes)
  - `claim_structural_audit → claim_structural_revise` (K = `comment.violation` on claims; scout-emitted)
- **Marker Stigmergic Protocol** (stigmergic) — non-comment markers flip downstream predicates. The marker emission has no closure expectation on the emitter; the downstream agent reads the marker as its initiation condition. Instances:
  - `full_review → claim_findings` (review classifier as marker)
  - `bridge_probe → synthesis-producer` (saturation marker as marker — planned)
  - Family C chain-advance (parent's chain length as marker for sidecar producers)
  - `inquiry_consult → note_draft` (consultation-coverage as marker for note synthesis)
- **Self-Review Stigmergic Protocol** (sequential — typically operator-gated) — a single fire emits modification *plus* a scoped self-review of the modification. The self-review's `comment.<kind>` emissions seed downstream Correction Stigmergic Protocol cycles. Instances:
  - `note_patch` (producer; patch + patch-scoped review)
  - `claim_patch` (producer; patch + patch-scoped review on claims)
  - `note_absorb` (refiner; integration + integration-scoped review)
- **Cycle Stigmergic Protocol** (stigmergic) — agent fires once per cycle; runner re-fires until target's quiescence predicate flips ⊤. Instances:
  - Family A reviewers (`full_review`, `cone_review`, `note_review`, `inquiry_consult`, `note_consult`) — internal multi-cycle loops retired in favor of runner-driven re-fires. Validates the substrate spec's separation of concerns (Run1 + Run2).

Two cross-caste patterns that don't reduce to a single primitive:

- **Identity-grant-only** (sequential — non-stigmergic-protocol-shaped) — operator-gated lattice ops that create new entities emit lineage links only, with no self-review and no closure cycle. The new entity goes through the standard runner walk on the next cycle. Members: `claim_decompose`, `note_extract`, `note_clone`, `note_promote_open_questions`, `note_promote_out_of_scope`. Not a Stigmergic Protocol primitive because there's no closure-required follow-on; it's an *operator-as-producer emission* that lands new substrate identity.
- **Empty-derivation pattern** (substrate convention) — Provenance shape `(1, 0|1, A, A, ⊤)` admits `c_G = 0|1`, used by scouts (audit ran with no findings) and decomposers (`claim_findings` with CONVERGED verdict) to honestly record zero-output emissions. Not a protocol; a substrate-vocabulary convention that several primitives consume.

Maturation Stigmergic Protocols (e.g., the Note-to-Claim Maturation Stigmergic Protocol) compose these primitives across stages. See [`../maturation/`](../maturation/) for the composition-level treatment.


## Caste-level observations

Surfaced in detail in each caste doc; aggregated here:

(a) *Detection inside vs. detection upstream.* The caste taxonomy splits on where decision logic lives. Producers persist external decisions (operator, upstream LLM, derivation rules). Scouts run their own detection. Refiners' decision space is bounded by the comment they're addressing — they cannot ignore it, they must close it somehow — but the resolution-kind choice (edit vs reject vs retract) and content edits are LLM-driven domain work, comparable to producer decisions but constrained by the comment's semantic content rather than by upstream context.

(b) *AG4 + AG5 hold uniformly.* Across all 26 agents, decision logic is opaque (`act_A`'s body is private), and only emissions are public. This is what makes the architectural pattern composable — the runner doesn't need to know what an agent will do, only that it will conform to its declared emission contract.

(c) *Runner-walked / operator-gated split is consistent.* Refiners: 3 walked, 1 gated. Scouts: 1 walked, 1 stub. Producers: 13 walked, 7 gated. Registry total: 17 walked, 8 gated, 1 stub. The substrate spec (Run0–Run5) covers the walked population; operator-gated agents are spec-compliant on emissions but invocation is out-of-band (Run5's policy-module limit case).

(d) *Caste classification follows primary substrate effect.* `note_absorb` does both producer work (emits an integration review) and refiner work (closes the integration question); it's classified refiner because the caste-defining act is closure. `note_promote_*` has an LLM-as-scout inside the agent body; it's classified producer because the primary substrate effect is identity grant. `claim_formal_contract` emits a chain advance but its trigger is one-shot existence; family classification follows trigger pattern + substrate effect, not user-facing artifact.

(e) *Composed sub-routines are not agents.* `claim_finding_override` lives in `producers/` as code-locality but does not satisfy AG0–AG7 as an independent agent. Treated separately.

(f) *Empty / null fires emit honestly.* Scouts emit audit docs even on zero-violations fires (the substrate fact "audit ran" is what makes `is_*_fresh` evaluable). Decomposers emit empty-derivation tuples on zero-findings reviews (the substrate fact "decompose ran with zero output" anchors `is_review_decomposed = ⊤`). The empty-derivation pattern (Provenance `c_G = 0|1`) is what makes this honest at the substrate level.


## What is not in this doc

- *Per-agent specs.* See [`producers.md`](producers.md), [`refiners.md`](refiners.md), [`scouts.md`](scouts.md). Each caste doc has per-agent tables with trigger, scope, predicate, primary emissions, emission contract, partner.
- *Substrate spec.* See [`../substrate/`](../substrate/) — types, shapes, predicate composition, agents (the formal AG0–AG7 layer), quiescence, runner.
- *Stigmergic Protocol composition.* End-to-end arcs across multiple castes (note → claim, inquiry → note, lattice operations) live at the protocol layer (`../maturation/` and any future Stigmergic Protocol family directories). The two hand-off types and the cross-cutting patterns above are load-bearing components of those arcs.
- *Operator runbooks.* Workspace conventions, spec-md formats, operator-script invocations are implementation, not spec. They live in operator-side documentation, not here.
- *Implementation details.* Helper modules, prompt templates, channel-specific consultation logic, sub-routines like `claim_finding_override` are implementation. The agent docs reference them where relevant (working surface, invocation context) but do not document their internals.