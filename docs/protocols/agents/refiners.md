# Refiners

*The caste-defining act is closing findings. A refiner reads open `comment.*` tuples in its scope and emits `resolution.<kind>` (and sometimes `retraction`) targeting them, flipping its trigger false.*

This document surveys the four refiner agents in `scripts/lib/agents/refiners/`. It establishes the per-caste documentation format used by sibling caste docs (producers, scouts, workers).


## What a refiner is

A refiner is an agent whose primary substrate effect is *closure* — emitting tuples in self-referential relations (`resolution`, `retraction`) that target open comments, transforming the substrate's open-finding state toward quiescence.

Per `protocols/substrate/`:

- *Substrate side* (canonical shape catalog, with Sh3 admitting `t_G = A_rel` for self-reference): `resolution.<kind>` is a tuple in a Resolution-shape relation `(1, 1, A_doc, A_rel, ⊤)`. Its to-slot targets a comment-tuple's address — R5 makes self-targeting expressible at the substrate level; Sh3 admits it at the shape level. The refiner's emission is what closes the comment; per the Resolution walkthrough in `relation-shapes.md`, Resolution generates no standalone predicate template — it is consumed by the Comment template's `all_K_resolved` reference.
- *Agent spec* (AG3): every emission carries a provenance tuple binding `name_A → addr(emission)`.
- *Progress-discipline* (Q3): the emission contract `Post_A` for a refiner is satisfied by the resolution-emission flipping `T_A` false. After a fire, the refiner's trigger no longer matches the just-closed comment. Locally progress-disciplined.

The refiner caste does not "drive convergence" by itself. Each fire closes one comment (or a per-target batch of comments). The runner walks the trigger across remaining open comments until none remain in scope; that is when the scope is quiescent.


## Caste-internal structure

Every runner-walked refiner has the same shape:

| Component | Role |
|---|---|
| Scope query | Yields candidate addresses — typically `comment.*` tuple addresses (per-comment) or document addresses (per-target batch) |
| Skip-when predicate | A `PL` Boolean — true when the refiner has nothing to do (`has_resolution`, `is_*_clean`, `is_*_quiescent`) |
| Trigger-fires-when | NOT skip-when AND in scope |
| Action | Read the open comment(s), perform domain work, emit `resolution.<kind>` (one per closed comment) |
| Out-of-band side effects | Content edits to the targeted document via Claude Edit / external tools |
| Substrate progress | Each fire flips at least one comment's `has_resolution` from ⊥ to ⊤; per-target predicate becomes false |

Out-of-band side effects (content edits to docs) are not substrate facts — they're filesystem-level changes to documents whose addresses already exist in the substrate. The substrate sees only the resolution and provenance emissions; the *content* of the targeted document is updated through normal file I/O. (R3 monotonicity applies to L_K, not to the content of A_doc-addressed documents.)

*Note on batch granularity.* Per-comment refiners (`claim_revise`) have args = comment-address; the trigger flips per comment. Per-target batch refiners (`claim_structural_revise`, `note_revise`) have args = claim-address or note-address, and a single fire closes *all* open comments on that target; the trigger flips per claim/note, not per closed comment. Q4's locality (per-agent, per-args) holds at the args granularity each refiner declares — the batch is a single Q4-unit, not a sequence of unit-comment fires.


## Runner-walked refiners

Three of four refiners are walked by the standard runner. They satisfy AG0–AG7 + Q0–Q10 + are scheduled per Run1.


### `claim_revise` — per-comment refiner

| Field | Value |
|---|---|
| Trigger name | `claim-revise` |
| Granularity | per-comment |
| Scope query | each open `comment.revise` whose target is a claim in the requested ASN's derivation set (CLI), or every active `comment.revise` (daemon) |
| Skip-when predicate | `has_resolution(comment)` — comment already has an active `resolution.*` |
| Substrate emissions | one `resolution.<kind>` targeting `addr(comment)` + provenance per AG3 |
| Out-of-band | content edits to the target claim file |
| Emission contract sketch | `Post_A(comment, Σ, E) ≡ ∃ (K_res, F, G) ∈ E :: addr(comment) ∈ coverage(G)` |
| Trigger flip | After fire, `has_resolution(comment) = ⊤`; predicate skips it. Locally progress-disciplined ✓ |
| Cross-caste partner | producer `claim_findings` (emits the `comment.revise` tuples this closes) |


### `claim_structural_revise` — per-claim batch refiner

| Field | Value |
|---|---|
| Trigger name | `claim-structural-revise` |
| Granularity | per-claim (batch — closes all open violations on the claim per fire) |
| Scope query | each claim in the requested ASN's derivation set (`per_claim_of_asn`) |
| Skip-when predicate | `is_claim_structurally_clean(claim)` — every `comment.violation` targeting the claim has an active resolution |
| Substrate emissions | per closed comment: one `resolution.<kind>`; for `depends`-agreement RETRACT decisions: one `retraction` targeting the citation; provenance per AG3 |
| Out-of-band | multi-pass content edits across the claim's files (diff/apply machinery) |
| Emission contract sketch | `Post_A(claim, Σ, E) ≡ (∀ τ ∈ open_violations(claim, Σ) :: ∃ (K_res, F, G) ∈ E :: addr(τ) ∈ coverage(G))` |
| Trigger flip | After fire, every violation on the claim is resolved → `is_claim_structurally_clean(claim) = ⊤`. Locally progress-disciplined per-claim ✓ |
| Cross-caste partner | scout `claim_structural_audit` (emits the `comment.violation` tuples this closes) |


### `note_revise` — per-note batch refiner

| Field | Value |
|---|---|
| Trigger name | `note-revise` |
| Granularity | per-note (batch over all open revises on the note) |
| Scope query | each active non-retired note (`per_active_note`) |
| Skip-when predicate | `is_doc_quiescent(note) ∨ ¬ all_open_revises_consulted(note)` — skip when nothing to revise OR when consult hasn't yet covered every open revise |
| Substrate emissions | per addressed comment: one `resolution.<kind>` (edit or reject); provenance per AG3 |
| Out-of-band | content edits to the note via Claude Edit |
| Emission contract sketch | `Post_A(note, Σ, E) ≡ (∀ τ ∈ open_revises(note, Σ) :: ∃ (K_res, F, G) ∈ E :: addr(τ) ∈ coverage(G))` |
| Trigger flip | After fire, every open revise addressed → `is_doc_quiescent(note) = ⊤`. ✓ |
| Sequencing dependency | Compound predicate forces wait-for-`note_consult` (a producer that intermediates between findings and revises). The wait is enforced via the predicate's second disjunct. |
| Cross-caste partners | producers `full_review` / `cone_review` (emit revise comments) + `note_consult` (sequencing intermediate) |


## Operator-gated refiners

One of four refiners fires from out-of-band signals rather than substrate state.


### `note_absorb` — operator-gated lattice-scope refiner

| Field | Value |
|---|---|
| Trigger name | (none — no entry in `lib/triggers/`) |
| Granularity | lattice-scope (one extension-merge operation per fire) |
| Trigger source | **operator** drops a spec md into a designated workspace location (e.g., `_workspace/absorbs/<filename>.md`); operator invokes the absorb script against that spec. The substrate sees no trigger evaluation — invocation is filesystem-mediated. (See operator runbook for current path conventions and script invocation.) |
| Predicate | n/a (operator-gated) |
| Caste-defining emission | `provenance.absorb(F=[spec_doc], G=[base])` — closes the integration question |
| Compound emissions (see "Modify-then-self-review" pattern below) | `absorb` classifier on spec + `retired` classifier on extension; one-shot integration `review` + per-finding `finding` + `comment.revise` decompositions targeting the integrated base; `provenance.derivation(F=[spec], G=[review])` |
| Out-of-band | content edits to base note (integrate extension claims); content edits to source note (rewrite citations) |
| Closure model | The agent does not drive convergence on the integrated base. The post-integration review's `comment.revise` findings sit in substrate as open links, picked up by `note_revise` on the next runner walk. |

**Why operator-gated:** lattice operations (extract, absorb, promote, clone) are *operator decisions* — the substrate cannot decide *whether* to absorb an extension because that judgment is an operator-scope call. The caste classification (refiner) is correct because the caste-defining act is closing the integration question; the gate is just the invocation mechanism.

**Architectural distinction.** Runner-walked refiners satisfy AG1's full spec (trigger predicate `T_A ∈ PL`, scope `D_A ∈ QD` on substrate state). Operator-gated refiners have no `T_A` the runner can evaluate — their "trigger" is a filesystem signal external to substrate state. They satisfy AG0, AG2, AG3, AG6, AG7 (well-formed substrate emissions, transition-preserving, atomic) but not AG1 in the runner-walked sense. They are spec-compliant agents whose invocation is out-of-band.

Consequently, operator-gated agents are also outside `runner.md`'s Run1 fairness coverage — their invocation is at operator discretion rather than runner schedule. They can be viewed as a limit case of Run5 (`RunnerIsPolicyParameterized`) where the policy module's invocation discipline is human rather than algorithmic. Q5/Q6's termination chain therefore covers only runner-walked agents; operator-gated activity proceeds on its own clock.

This is a real two-population split inside the agent registry. The substrate's runner spec (Run0–Run5) covers the runner-walked population. Operator-gated agents have parallel machinery — operator scripts, workspace conventions, gate detection — that is implementation, not spec.


## Cross-caste patterns


### Producer-refiner pair (substrate-mediated)

The standard refinement chain:

> producer emits a `comment.<kind>` tuple → refiner's trigger fires on the open comment → refiner emits `resolution.*` → next walk's runner skips the (now-resolved) comment

Three pairs exist among the runner-walked refiners:

| Producer | Comment kind | Refiner |
|---|---|---|
| `claim_findings` | `comment.revise` (on claim) | `claim_revise` |
| `claim_structural_audit` *(scout)* | `comment.violation` (on claim) | `claim_structural_revise` |
| `full_review` / `cone_review` | `comment.revise` (on note) | `note_revise` |

The pattern is exactly the producer-refiner correction loop from `protocols/substrate/agents.md` (AG5 consequence): two unreliable decisions checking each other through the substrate.

*Note on comment kinds.* `comment.revise` and `comment.violation` share the Comment shape (per `relation-shapes.md`); they differ only in `K` (the typed kind). This is why a single resolution mechanism (Resolution-shape tuples targeting a comment address) handles both — the shape-level constraint is uniform, the kind-level discrimination is what separates producer-refiner pairs from scout-refiner pairs at the registry level.

**Sequencing dependencies via compound predicates.** `note_revise` waits for `note_consult` to fire on each open revise before closing. This is enforced by the trigger's compound predicate `is_doc_quiescent ∨ ¬ all_open_revises_consulted`. The sequencing is substrate-mediated — `note_revise` cannot fire before `note_consult` has updated each open revise's substrate state.

This pattern is general: refiner sequencing is enforced by adding a "downstream-prerequisite-met" disjunct to the refiner's skip-when predicate. No out-of-band coordination, no orchestrator needed; the substrate state mediates the order.


### Operator-gated lattice operations: two sub-patterns

Three refiner-or-producer agents in the registry are operator-gated lattice operations: `note_absorb` (refiner), `note_patch` (producer), `claim_patch` (producer). They share *operator-gated* and *deferred-refinement*; they split on whether they emit a self-review:

#### Modify-then-self-review

Operations that **modify existing substrate content** emit a one-shot scoped self-review of their primary work. Pattern:

1. Operator gate (filesystem drop)
2. Primary work: modify existing content (integrate extension into base, apply patch)
3. *Same fire* emits `review` + per-finding `finding` + `comment.revise` decomposition targeting the modified entity
4. `provenance.derivation(F=[primary_op], G=[review])` ties the review to the operation
5. Standard refinement cycle (`note_revise` / `claim_revise`) picks up the comments on next walk

Members: `note_absorb` (refiner), `note_patch` (producer), `claim_patch` (producer).

The self-review is *scoped* — `review.coverage` targets the specific modification, not a full re-review. This is what justifies emitting it from inside the lattice op rather than letting standard reviewers fire later: standard reviewers would either re-review the entire entity (wasteful) or might not re-fire at all (their predicate may not detect the modification).

#### Identity-grant-only (forward-reference to producers)

Operations that **create new substrate entities** emit lineage links only — no self-review. The new entity goes through the standard runner walk, where `full_review` / `cone_review` / `inquiry_consult` will fire on it as a fresh target on the next cycle.

Members (all producers, surveyed in `producers.md` when written): `note_extract`, `note_clone`, `note_promote_open_questions`, `note_promote_out_of_scope`.

The split between the two sub-patterns is principled:

> Modifies existing content → self-review (scoped to the modification).
> Creates new entity → no self-review (standard cycle handles the new target).

A modification needs an explicit, scoped review because the standard reviewer's predicate may not re-fire on modified content. A new entity does not need one because the standard reviewer will fire on a fresh target naturally.


## Caste-level observations

(a) *Refiners are AG3-load-bearing.* Every refiner depends on AG3 (provenance discipline) for its emissions to be auditable; the resolution-targeting-comment relationship is a self-referential link (R5) whose authorship is recoverable only via provenance.

(b) *Refiners are not progress-disciplined for the system, only for themselves.* Q3 (local progress-discipline) holds for each runner-walked refiner: a fire flips the just-closed comment's `has_resolution` to ⊤. This is per-comment progress; *system-level* progress (bounded W) requires that the producer-emitting-comments side also be progress-disciplined and that no cycle of producer-refiner emission produces unbounded fan-out. The claim-introducing-edit failure mode in `quiescence.md`'s worked example is exactly such a cycle.

(c) *The runner-walked / operator-gated split is structural.* The substrate spec (Run0–Run5) covers runner-walked agents. Operator-gated agents are spec-compliant in the sense that they emit conformant substrate facts (Sh-conf, AG3) but their invocation mechanism is outside the runner. This split surfaces explicitly in `note_absorb` here and in `note_patch` / `claim_patch` / extract / clone / promote when those are surveyed.

(d) *Lattice operations are compound-emission agents.* `note_absorb` plays both refiner role (closes integration question) and producer role (emits integration review) in one fire. The caste classification reflects the *primary* substrate effect; the secondary emissions (the integration review) are what enable downstream refinement to fire. This is what the modify-then-self-review pattern captures.


## What is not in this doc

- *Producer specs.* Producer caste is surveyed in `producers.md` (when written). The producer-refiner pairs cited here have their producer halves there.
- *Scout specs.* Scout caste is surveyed in `scouts.md`. The scout-refiner pair (`claim_structural_audit` → `claim_structural_revise`) has its scout half there.
- *Stigmergic Protocol composition.* The end-to-end note-to-claim arc — how producers, refiners, and scouts compose across scope tiers (per-document → per-ASN → lattice → cross-lattice) — is documented in `maturation/note-to-claim.md`. The modify-then-self-review and identity-grant-only patterns surface there as load-bearing components of the protocol composition.
- *Operator-side machinery.* Workspace conventions, spec-md formats, operator script invocations are implementation details. They are sketched here for context but specified at the implementation layer (operator runbooks, scripts/note-*.py, etc.).