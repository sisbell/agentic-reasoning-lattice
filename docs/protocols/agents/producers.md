# Producers

*The caste-defining act is identity-granting. A producer reads upstream context (substrate state, content, operator spec) and emits a substrate fact that grants new identity to a target — a classifier on a doc, a sidecar attestation chain advance, a coverage relation, a per-finding decomposition.*

This document surveys the 20 producer agents in `scripts/lib/agents/producers/` (plus one composed sub-routine, `claim_finding_override`, treated separately in observation (d)). Producers are the largest caste in the registry. They split into six families by what they grant and how they're invoked.


## What a producer is

A producer is an agent whose primary substrate effect is *new substrate identity*: it brings something into the substrate that wasn't there before, or advances something's supersession chain so downstream predicates flip.

Per `protocols/substrate/`:

- *Substrate side:* producer emissions are typically Classifier-shape (`claim`, `note`, `inquiry`, `review`, `finding`, `patch.*`, `clone`, `extract`), Coverage-shape (`review.coverage`, `consultation.coverage`), Attribute-shape sidecar attestations (`description`, `signature`, `references`, `statements`), and Provenance-shape (`provenance.derivation`, `provenance.synthesis`, `provenance.clone`, `provenance.extract`, `provenance.absorb`).
- *Agent spec* (AG2 + AG3): emissions are shape-conformant (Sh-conf at Emit time); each carries a provenance binding.
- *Progress-discipline* (Layer 2 of `quiescence.md`): each producer's emission contract `Post_A` flips its trigger from ⊤ to ⊥ on the just-handled target. Producers are progress-disciplined locally; whether the protocol they participate in has bounded W is a registry-design question.

**What distinguishes a producer from a scout:** detection happens *upstream* of the producer. A producer takes a decision made elsewhere — an operator's spec md, an LLM's review verdict, a derivation rule applied to upstream facts — and persists the result. A scout's decision logic is internal; a producer's is external.

**What distinguishes a producer from a refiner:** a producer creates new identity; a refiner closes existing findings. The same fire can do both (lattice ops do — see `refiners.md` on `note_absorb`'s compound emission); the caste classification reflects *primary* substrate effect.


## Caste-internal structure

Producers vary more than refiners or scouts in their substrate shape. Five sub-shapes recur:

| Sub-shape | Trigger pattern | Primary emission |
|---|---|---|
| **Cycle producer** | per-target cycle predicate (`is_claim_quiescent`, `is_doc_quiescent`) | review/consultation doc + per-finding substrate |
| **Decomposer** | one-shot existence check on upstream review (`is_review_decomposed`) | per-finding decomposition with `provenance.derivation` |
| **Chain-advance attribute producer** | freshness via supersession-chain comparison (`is_*_fresh`) | sidecar attestation, advances chain |
| **One-shot identity grant** | one-shot existence check on classifier | classifier link |
| **Operator-gated lattice op** | filesystem signal | varies (modify-then-self-review or identity-grant-only) |

The five sub-shapes share AG3 (provenance discipline) and AG6 (transition-preserving). They diverge on trigger semantics, scope granularity, and Q-frame quiescence target.

*Note on Q4 unit for batch producers.* Several producer sub-shapes are batch agents — a single fire emits multiple substrate tuples under one Q4-unit, with the trigger flipping per-target rather than per-emitted-tuple:

- *Family A (cycle reviewers):* args = target-address (note, ASN, claim apex, inquiry); a single cycle-fire emits review-doc + per-finding `comment.<kind>` tuples; the trigger flips per-target on the next walk's quiescence check.
- *Family B (decomposers):* args = source-review-address; a single fire emits per-finding decomposition; the trigger flips per-review (`is_review_decomposed` becomes ⊤).
- *Family G `claim_decompose`:* args = source-note address; a single fire emits per-derived-claim Classifier + sidecar + provenance tuples; the trigger flips per-source-note.

This matches the framing used for batch refiners (`claim_structural_revise`, `note_revise`) in `refiners.md` and per-target scouts (`claim_structural_audit`) in `scouts.md`. Q4's locality (per-agent, per-args) holds at whichever args granularity the producer declares; the batch is a single Q4-unit, not a sequence of unit-tuple fires.


## Runner-walked producers

Thirteen of 20 producers are walked by the standard runner. They satisfy AG0–AG7 + Q0–Q10 and are scheduled per Run1.


### Family A — Reviewers (cycle producers)

Reviewers fire once per cycle on a target that hasn't reached its quiescence target. Each fire produces a review/consultation doc and per-finding substrate. The runner re-fires until the target's predicate flips ⊥→⊤; the iteration loop that used to live inside the agent now lives in the runner.

| Agent | Trigger | Granularity | Skip-when predicate | Primary emissions |
|---|---|---|---|---|
| `full_review` | `full-review` | per-ASN (source note) | source note is `quiescent ∧ ¬confirmed` | `review` classifier + `review.coverage(review → note)` over whole-ASN content |
| `cone_review` | `cone-review` | per-apex-claim | `is_claim_quiescent(apex)` | `review` classifier + `review.coverage` over cone (apex + same-ASN deps + cross-ASN foundation) |
| `note_review` | `note-review` | per-note | (informal — predicate name pending; current discipline is "active non-retired note has unreviewed content"; likely formalizes to a `¬is_note_review_fresh(note)` form once stabilized) | `review` classifier + `review.coverage(review → note)` + `comment.<kind>` per finding |
| `inquiry_consult` | `inquiry-consult` | per-inquiry | inquiry has no `consultation.answer.*` covering it | per-question theory + evidence consultation; `consultation.questions`, `consultation.answer.<role>`, `consultation.coverage` |
| `note_consult` | `note-consult` | per-note | every open `comment.revise` on the note has `consultation.coverage` | channel-assignment of REVISE items + targeted consultations; `consultation.assessment`, `consultation.answer.<role>`, `consultation.coverage` per uncovered finding |

**Sub-pattern: cycle then re-fire.** `cone_review` and `full_review` previously had their own multi-cycle loops; those are now in the runner. The agent does one cycle (validate-gate → assemble → run LLM → emit substrate → commit) and returns. The runner re-fires while the target's quiescence predicate is still false. This is the substrate spec's Run1 + Q5 chain: per-fire bounded work + eventual quiescence under registry-side discipline.

**Sub-pattern: scope tier within reviewer family.** Reviewers operate at different scope tiers:
- `inquiry_consult` is per-inquiry (a stage above note); fires on inquiries before any note exists.
- `note_review` is per-note (note-stage scope).
- `note_consult` is per-note but at a *later* note-stage point (consult-during-revise).
- `full_review` is per-ASN (note + all derived claims).
- `cone_review` is per-apex-claim (claim-stage scope, focused).

The same caste sub-shape (cycle producer) at different scope tiers — exactly the Q10 observation that scope tiers can diverge within a caste.


### Family B — Decomposers

Decomposers fire once per upstream review/consultation that hasn't been broken into per-finding substrate. The predicate is an existence check; once decomposition emissions exist (any outbound `provenance.derivation` from the review), the trigger never re-fires on that source.

| Agent | Trigger | Granularity | Skip-when predicate | Primary emissions |
|---|---|---|---|---|
| `claim_findings` | `claim-findings` | per-review-doc | `is_review_decomposed(review)` — any outbound `provenance.derivation` from the review | per-finding `finding` doc + `comment.<kind>` link to target claim + `provenance.derivation(review → finding)` |

**Empty-derivation handling.** For zero-findings cases (CONVERGED verdict, all findings filtered out), `claim_findings` emits a single empty-set derivation `provenance.derivation(F=[review], G=∅)` — anchoring "decompose ran, produced no derivatives." The Provenance shape admits `c_G = 0|1` per `relation-shapes.md`, which is what makes the empty-G emission well-typed at the substrate level; both `claim_findings` here and scout audits (per `scouts.md`) consume the same admission for honest zero-decomposition recording. The empty-G shape covers the zero-findings disambiguation without a verb-flag classifier.

**Composed sub-routine: `claim_finding_override`.** `claim_findings` composes a classifier-override step inside its action (`apply_classifier_verdict` over the finding list, correcting the reviewer's class on disagreement). The override module lives in `producers/claim_finding_override.py` but is *not* a standalone agent — it has no `T_A`, no `D_A`, no `act_A` of its own; it is a sub-routine called by `claim_findings`'s action. The codebase places it in `producers/` by directory convention, but it does not satisfy AG0–AG7 as an independent agent. (See *Caste-level observations* below for the architectural treatment of sub-routines.)


### Family C — Chain-advance attribute producers

Chain-advance producers maintain an attribute sidecar's supersession chain in step with its parent doc's chain. The predicate is *freshness* — a sidecar is fresh iff its chain is at least as long as the parent's. When the parent is edited, the parent's chain advances; the sidecar is now stale; the producer fires to refresh and advance the sidecar's chain.

| Agent | Trigger | Granularity | Skip-when predicate | Primary emissions |
|---|---|---|---|---|
| `citation_resolve` (via `claim-citation-resolve` trigger) | `claim-citation-resolve` | per-claim | `references_is_fresh(claim)` | references sidecar attestation (advances chain); `citation.depends/forward` per ref; `retraction` for stale refs; `citation.resolve`; `provenance.derivation` |
| `claim_signature_resolve` | `claim-signature-resolve` | per-claim | `signature_is_fresh(claim)` | signature sidecar attestation (advances chain) |
| `claim_describe` | `claim-describe` | per-claim | description chain ≥ claim chain | description sidecar attestation (advances chain) |
| `note_statements` | `note-statements` | per-note | note is `is_claim_confirmed ∧ statements chain ≥ note chain` | statements sidecar attestation (advances chain) |

**Sub-pattern: Attribute shape + chain-advance.** All four attribute producers emit Attribute-shape `(1, 1, A_doc, A_doc, ⊤)` tuples (per `relation-shapes.md`). The supersession-chain mechanism is the substrate's freshness machinery — the predicate compares chain lengths, the producer fires to add a new chain link, the predicate flips ⊤ until the parent advances next.

**Sub-pattern: combined identity-grant + content edit.** `citation_resolve` is a hybrid: it advances the references sidecar's chain (Family C behavior) AND emits citation links + retractions (substrate-citizen graph edits). The sidecar attestation is the freshness signal; the citation/retraction emissions are the substrate state changes the predicate will read on next walk.


### Family D — Per-target one-shot identity grants

These producers grant a single classifier (sometimes with provenance attribution or a content-body emission accompanied by a chain advance) per target. The predicate is a one-shot existence check; once granted, the agent never re-fires on that target. Targets vary across the family — per-claim, per-inquiry — but the trigger pattern (one-shot existence) and the substrate effect (single identity grant) are uniform.

| Agent | Trigger | Granularity | Skip-when predicate | Primary emissions |
|---|---|---|---|---|
| `claim_contract` | `claim-contract` | per-claim | claim has a `contract.<kind>` classifier | one `contract.<kind>` Classifier link |
| `claim_formal_contract` | `claim-formal-contract` | per-claim | `contract.<kind>` is set ∧ kind requires Formal Contract ∧ claim md has `*Formal Contract:*` section | chain advance on the claim (substrate effect); content emission to claim md body (out-of-band) |
| `note_draft` | `note-draft` | per-inquiry | inquiry has consultation done ∧ no `provenance.synthesis` from inquiry yet | `note` Classifier on new note + `provenance.synthesis(inquiry → note)` |

**Sub-pattern: one-shot existence check.** Unlike Family C's chain-comparison freshness, Family D's predicate is *existence* of the granted artifact. Once the artifact exists, the predicate stays ⊤ permanently (modulo retraction). This is the simplest progress-discipline form: the emission directly creates the substrate fact the predicate tests for.

**Sub-pattern: chain-advance with out-of-band content edit.** `claim_formal_contract`'s *substrate* emission is a chain advance on the claim — structurally a Family C-shape effect. Its content edit to the claim md body (the Formal Contract section) is *out-of-band*, not a substrate fact, like refiners' content edits to docs they resolve. The agent appears in Family D because its trigger pattern is one-shot existence (Family D); its substrate effect is chain advance that flips downstream sidecar predicates (description, signature) stale and triggers Family C re-fires. The content edit is the user-visible artifact but is not what the substrate observes. Boundary cases like this are why caste classification follows *trigger pattern + primary substrate effect* rather than user-facing artifact.

**Sub-pattern: scope tier within Family D.** Like Family A reviewers, Family D agents operate at different scope tiers without leaving the family. `claim_contract` and `claim_formal_contract` are per-claim (claim-stage scope); `note_draft` is per-inquiry (a stage above note). The Q10 observation that scope tiers can diverge within a caste applies within a family too — the family criterion is trigger-pattern + substrate-effect, not stage.


## Operator-gated producers

Seven of 20 producers fire from out-of-band signals rather than substrate state. Like `note_absorb` in `refiners.md`, they satisfy AG0, AG2, AG3, AG6, AG7 but *not* AG1 in the runner-walked sense — they have no `T_A` the runner can evaluate; their invocation is filesystem-mediated. They are also outside Run1's fairness coverage (operator discretion drives invocation, not the runner's schedule). They split into two sub-patterns surfaced in `refiners.md`.


### Family F — Modify-then-self-review

Operations that modify existing substrate content emit a one-shot scoped self-review of their primary work.

| Agent | Granularity | Trigger source | Primary emissions |
|---|---|---|---|
| `note_patch` | per-note | operator drops patch md, runs note-patch script | `patch.note` classifier on patch doc; `provenance.derivation(patch → note)`; `review` classifier on patch-scoped review; `review.coverage(review → note)`; `provenance.derivation(patch → review)`; `finding` + `comment.revise` per finding |
| `claim_patch` | per-ASN-claim-set | operator drops patch md, runs claim-patch script | `patch.claim` classifier on patch doc; `provenance.derivation(patch → note)`; `review.content` classifier on patch-scoped review; `review.coverage(review → each derived claim)`; `provenance.derivation(patch → review)`; per-finding decomposition produced by `claim_findings`'s standard re-fire |

Both rely on the standard refinement chain (`note_revise` for note_patch; `claim_findings` → `claim_revise` for claim_patch) to drive convergence on the findings the patch-scoped review emitted. Per `refiners.md`, this is the *modify-then-self-review* sub-pattern of operator-gated lattice ops.


### Family G — Identity-grant-only

Operations that create new substrate entities emit lineage links only — no self-review. The new entity goes through the standard runner walk on the next cycle.

| Agent | Granularity | Trigger source | Primary emissions |
|---|---|---|---|
| `claim_decompose` | per-source-note | operator runs claim-decompose script | per-claim `claim` Classifier + `label` + `name` sidecars + `provenance.derivation(note → claim)` per derived claim; `transclusion.claim-statements` |
| `note_extract` | per-extract-spec | operator drops spec md, runs note-extract script | `extract` classifier on spec; `note` classifier on new ASN; `extends(new → absorb_into)`; `source(new → extract_from)`; `provenance.extract(spec → new)` |
| `note_clone` | per-clone-spec | operator drops spec md, runs note-clone script | `clone` classifier on spec; `note` classifier on new clone; `inquiry` classifier on new inquiry doc; `provenance.clone(origin → clone)`; mirrored `citation.depends` |
| `note_promote_open_questions` | per-source-ASN | operator runs promote script | per-promoted-item `inquiry` classifier; `promotion.open-questions` classifier on audit report; `provenance.derivation(note → report)`; `provenance.derivation(report → each new inquiry)` |
| `note_promote_out_of_scope` | per-source-ASN | operator runs promote script | per-promoted-item `inquiry` classifier; `promotion.out-of-scope` classifier on audit report; `provenance.derivation(note → report)`; `provenance.derivation(report → each new inquiry)` |

**LLM-as-scout in Family G.** `note_promote_open_questions` and `note_promote_out_of_scope` differ from the other identity-grant operations: the LLM-inside-the-agent decides which items earn new identity (acting in the scout role). The operator triggers the scan; the LLM does the selection. Per `scouts.md` (cross-caste section): scout-role activity is broader than the scout caste; here it lives inside producer-classified agents because the *primary substrate effect* is identity grant, not detection-and-report.


## Cross-caste patterns

Patterns surfaced in `refiners.md` and `scouts.md` that recur in producers:

### Producer-refiner pair (cf. `refiners.md`)

The standard refinement chain. Producers in Families A and B emit `comment.<kind>` tuples; refiners close them.

| Producer | Comment kind | Refiner |
|---|---|---|
| `full_review` / `cone_review` (Family A) | `comment.revise` (on note via review.coverage) | `note_revise` |
| `note_review` (Family A) | `comment.<kind>` per finding | `note_revise` |
| `claim_findings` (Family B) | `comment.<kind>` per claim | `claim_revise` |

### Scout-refiner pair (cf. `scouts.md`)

`claim_structural_audit` (scout) → `claim_structural_revise` (refiner). Producers do not directly participate; they're upstream of the structural-audit cycle (e.g., `claim_decompose` and Families C/D produce the claims that the structural scout subsequently audits).

### Modify-then-self-review (cf. `refiners.md`)

Family F (`note_patch`, `claim_patch`) plus `note_absorb` (refiner caste). All three modify existing substrate; all three emit a scoped self-review; all three defer convergence to the standard refinement cycle.

### Identity-grant-only (cf. `refiners.md`)

Family G (`claim_decompose`, `note_extract`, `note_clone`, `note_promote_*`). Create new entities; emit lineage links only; standard cycle handles review on the new targets.

### Substrate-mediated trigger handoff (cf. `scouts.md`)

Two variants surface across producers:

(i) **Comment-as-trigger** — Family A (reviewers) emit `comment.<kind>` tuples that fire the next-stage refiner trigger. The standard producer-refiner pair pattern.

(ii) **Marker-as-trigger** — Family B's `claim_findings` fires on `is_review_decomposed(review) = ⊥` (review without outbound `provenance.derivation`). The Family A reviewer's emission of the review classifier is the marker that triggers Family B. This is a *producer-to-producer* handoff via the substrate state, not via a comment-shape link. Family C's chain-advance freshness is similar in shape: the parent's chain length is a marker the sidecar producer reads.


## Caste-level observations

(a) *Producers vary more than refiners or scouts in shape.* The five sub-shapes (cycle, decomposer, chain-advance, one-shot grant, operator-gated lattice op) reflect that the producer caste covers all "create new substrate identity" work — and "create new identity" takes many forms (a classifier, a sidecar attestation, a coverage relation, a content edit accompanied by chain advance). Refiners and scouts are more uniform because their caste-defining acts are narrower (closure, detection-report).

(b) *Family C is the freshness-machinery family.* Chain-advance producers exist *because* of supersession chains. The substrate spec's `relation-shapes.md` Attribute shape pairs with `attribute_is_fresh` template; Family C is what populates and refreshes those attributes. Without Family C, sidecar predicates would never re-flip stale on parent edits.

(c) *Cycle producers + per-cycle runner detection close Q6 operationally.* Family A's "one cycle per fire, runner re-fires until quiescent" is exactly Run1 (round-robin) + per-cycle quiescence detection from `runner.md` Run2. The historical pattern of having multi-cycle loops *inside* the agent has been retired in favor of the runner-walks-until-quiescent pattern. This is the substrate spec's separation of concerns paying off in practice.

(d) *Composed sub-routines are not agents.* `claim_finding_override` lives in `producers/` but is composed by `claim_findings`'s action body. It has no `T_A`, no `D_A`, no `act_A` of its own. It is *infrastructure used by an agent*, not an agent. The substrate spec admits this distinction: AG0–AG7 apply to entities with their own substrate identity and trigger; helpers and sub-routines are implementation. The codebase's organization (placing them in `agents/<caste>/`) is a code-locality convention, not a substrate-spec claim.

(e) *Scout-role activity inside producer-classified agents is real.* `note_promote_*` agents have an LLM-inside-the-agent doing scout work (deciding which items earn new identity). The caste classification (producer) reflects primary substrate effect; the scout-role activity is a sub-routine. Per `scouts.md`'s cross-caste observation: scout-role is broader than the scout caste; it lives wherever detection happens *during a fire*. For lattice ops, that's inside the producer's body.

(f) *Operator-gated lattice ops cluster in producers.* Seven of eight operator-gated agents in the registry are producers (`claim_decompose`, `note_extract`, `note_clone`, `note_promote_open_questions`, `note_promote_out_of_scope`, `note_patch`, `claim_patch`). The eighth is a refiner (`note_absorb`). Lattice ops are mostly producer-shaped because their primary substrate effect is creating new entities (extract, clone, promote) or stamping new audit identity (patch's review classifier). `note_absorb` is the lone refiner-classified lattice op because its caste-defining act is closing the integration question.

(g) *The runner-walked / operator-gated split is consistent across castes.* Refiners: 3 walked, 1 gated. Scouts: 1 walked, 1 stub (planned walked). Producers: 13 walked, 7 gated. Registry total: 17 walked, 8 gated, 1 stub (~65% walked, ~31% gated). The substrate spec (Run0–Run5) covers the walked population unconditionally. Operator-gated agents are spec-compliant on emissions (Sh-conf, AG3, AG6) but their invocation is out-of-band.

(h) *Producers are where stage-spanning agent activity concentrates.* Inquiry-stage (`inquiry_consult`), note-stage (`note_draft`, `note_review`, `note_consult`), claim-stage (`claim_decompose` → `claim_findings` → `claim_describe`/`claim_signature_resolve`/`citation_resolve`/`claim_contract`/`claim_formal_contract`), lattice-stage (Families F + G). Stigmergic Protocol composition (`maturation/note-to-claim.md`) is therefore mostly a story about producer chains, with refiners and scouts attached at each stage's quiescence point.


## What is not in this doc

- *Refiner specs.* In `refiners.md`. Producer-refiner pairs are surfaced here at the trigger-handoff level; closure machinery is documented there.
- *Scout specs.* In `scouts.md`. Scout-refiner pairs ditto.
- *Stigmergic Protocol composition.* The end-to-end inquiry → note → claim arc — how producers compose across stages and scope tiers — is `maturation/note-to-claim.md`'s job. The patterns surfaced here (cycle-producer-with-runner-loop, modify-then-self-review, identity-grant-only) are load-bearing components of that protocol composition.
- *Operator-side runbooks.* Workspace conventions (`_workspace/extracts/`, `_workspace/patches/note/<ASN>/`, etc.), spec md formats, and operator-script invocations are implementation. They live in operator runbooks, not the spec.
- *Channel and consultation internals.* `inquiry_consult` and `note_consult` consume channel-specific consultation logic in `lib/consultation/consult.py` and per-channel plugins. The channel structure (theory/evidence asymmetry, vocabulary firewalls, synthesis discipline) is consultation-protocol territory and is not specified here at the substrate-protocol layer.
- *LLM prompt templates.* Reviewers, decomposers, and consultation agents all consume prompt templates under `prompts/`. Prompts are implementation; the spec sees only the substrate emissions the prompted LLM ultimately produces (per AG4 — `act_A`'s body is opaque).
- *Sub-routine helpers.* `claim_finding_override` and `_promote_helpers` and `review_helpers` are infrastructure code colocated under `producers/`. They are noted in caste-level observations but do not get per-agent treatment because they are not agents.