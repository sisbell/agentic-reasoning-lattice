# Note-to-Claim Maturation Stigmergic Protocol

How content matures from an inquiry into a quiescent set of formal claims, traced through the agent registry.

This document specifies the **Note-to-Claim Maturation Stigmergic Protocol** — a protocol in the [Maturation Stigmergic Protocol](../README.md) family. It is a Cachin-sense protocol — a legal succession of agent fires that drives content from one substrate state (an inquiry) to another (an ASN-quiescent set of confirmed claims). The [Lattice-Genesis Maturation Stigmergic Protocol](./lattice-genesis.md) precedes this one: it drives content from a scout signal through lattice creation to the point where the first note exists. Once a note exists, Note-to-Claim takes over from Stage 1. The substrate spec ([`../substrate/`](../substrate/)) is the foundation this protocol composes against: it defines the medium (Σ), the message format (Sh-conf + Sh0–Sh5), the message invariants (PC0–PC6, T_A, Post_A), the process model (AG0–AG7), the termination condition (Q0–Q10), and the scheduling discipline (Run0–Run5). The agent caste docs ([`../agents/`](../agents/)) specify the participant processes. This document specifies the *legal succession* — the sequence of agent fires that constitutes valid protocol execution and the quiescence-tier the protocol terminates at.

The pipeline in full:

> R0–R7 (typed relations + operations) → Sh0–Sh5 (shapes) → PC0–PC6 (predicates) → AG0–AG7 (agents) → Q0–Q10 (quiescence) → Run0–Run5 (runner) → Stigmergic Protocol primitives → **Maturation Stigmergic Protocol** (this layer)

A Maturation Stigmergic Protocol is the composition of multiple Stigmergic Protocol primitives (Correction, Marker, Self-Review, Cycle) plus a small number of sequential hand-offs that together drive content from one architectural state to another. The substrate spec gives recognizability and conditional termination at every scope tier (Q7–Q10); the Maturation Stigmergic Protocol layer is where those tier-by-tier guarantees are sequenced into an end-to-end protocol with a designated termination tier (here: ASN-level lattice quiescence).


## The arc at a glance

```
Inquiry
   │ inquiry_consult                    (stigmergic, per-inquiry)
   ▼
Inquiry + consultations
   │ note_draft                         (stigmergic, per-inquiry → note)
   ▼
Note (open)
   │ note_review ⇄ note_consult ⇄ note_revise   (stigmergic cycle)
   │ — runner re-fires until is_doc_quiescent ∧ confirmed
   ▼
Note (confirmed)
   │ note_statements                    (stigmergic, per-note)
   ▼
Note (confirmed + statements)
   │ claim_decompose                    (sequential — operator-gated)
   ▼
Claims (raw, identity-only)
   │ claim_contract                     (stigmergic, per-claim, one-shot)
   │ claim_formal_contract              (stigmergic, per-claim, one-shot, when applicable)
   │ Family C chain-advance:            (stigmergic, per-claim, chain-tracking)
   │   citation_resolve, claim_signature_resolve, claim_describe
   ▼
Claims (formalized, sidecars fresh)
   │ claim_structural_audit             (stigmergic, scout)
   │   ⇄ claim_structural_revise        (stigmergic, refiner)
   │ full_review or cone_review         (stigmergic, per-claim or per-ASN)
   │   → claim_findings                 (stigmergic, decomposer)
   │   → claim_revise                   (stigmergic, refiner)
   │ — runner re-fires until is_claim_quiescent for each claim
   ▼
Claims (quiescent at claim scope)
   │ — composes upward to ASN-level quiescence (per Q10 monotonicity)
   ▼
ASN quiescent
```

Stages 1–2 are the maturation spine and the sequential bridge. Stage 3 is per-claim formalization. Stage 4 is the claim-level review-and-revise cycle. Each stage is mostly stigmergic — the runner walks the agents whose triggers fire from substrate state. Two sequential hand-offs sit on the spine: *creating an inquiry* (operator authors or promote-agent extracts) and *deciding the note is ready for claim derivation* (operator invokes `claim_decompose`). All other transitions are predicate-driven.


## Stage 1 — Inquiry → Confirmed Note

A note matures through stigmergic agent activity until it satisfies the substrate predicate `is_claim_confirmed` (a registry-historical name; on a note it reads "the note is confirmed as ready for claim derivation"). The operator's role is creating the inquiry; everything else is runner-walked.

### Inquiry creation (sequential — operator or promote)

An inquiry doc enters the substrate either:
- *Operator-authored* — the operator drops an inquiry md directly.
- *Emitted by a promote agent* — `note_promote_open_questions` or `note_promote_out_of_scope` extracts an unresolved item from a parent note and emits a new `inquiry` Classifier on the new doc.

Both create an A_doc-addressed inquiry doc carrying the `inquiry` Classifier. The downstream runner activity is identical regardless of source.

### inquiry_consult — gather theory + evidence (stigmergic)

`inquiry_consult` (Family A reviewer at inquiry-stage scope) fires when an inquiry has no `consultation.answer.*` covering it. One fire = decompose the inquiry into questions, run theory + evidence consultations on each, persist per-Q/A answer docs, emit `consultation.questions`, `consultation.answer.<role>`, `consultation.coverage`.

After the fire, the trigger predicate flips: the inquiry now has consultation coverage, so `inquiry_consult`'s skip-when is true. The runner skips it.

### note_draft — synthesize note from consultations (stigmergic)

`note_draft` (Family D one-shot identity grant) fires when an inquiry has consultation done AND no `provenance.synthesis` from the inquiry yet. One fire = synthesize the consultation answers into a note doc, emit `note` Classifier on the new note + `provenance.synthesis(inquiry → note)`.

This is the first stigmergic hand-off in the spine: `inquiry_consult`'s emissions flip `note_draft`'s trigger from ⊥ to ⊤, and the runner fires `note_draft` on the next walk.

### Note maturation cycle (stigmergic, multi-pass)

Once the note exists, three runner-walked agents drive it toward `is_doc_quiescent`:

- **`note_review`** (Family A reviewer) — produces a `review` doc with per-finding `comment.<kind>` decompositions targeting the note. Fires when the note has unreviewed content.
- **`note_consult`** (Family A reviewer at consult-stage) — channel-assigns each open `comment.revise` and gathers theory/evidence consultations. Emits `consultation.assessment`, `consultation.answer.<role>`, `consultation.coverage` per finding. Fires when at least one open revise lacks coverage.
- **`note_revise`** (refiner) — addresses each open revise (using consultation evidence as context), emits `resolution.<kind>` to close it, edits note content. Fires when `is_doc_quiescent ∨ ¬all_open_revises_consulted` is false.

The cycle composes via stigmergic hand-offs:

```
note_review emits comment.revise → note_consult fires (revise lacks coverage)
note_consult emits consultation.coverage → note_revise's compound predicate clears
note_revise emits resolution → comment skip-when flips ⊤
runner re-fires note_review on next cycle (if note has new content edits)
```

The cycle terminates when the note reaches `is_doc_quiescent ∧ is_claim_confirmed` — no open revises AND latest review came up clean.

### note_statements — extract formal statements (stigmergic)

`note_statements` (Family C chain-advance) fires when the note is `is_claim_confirmed` AND the statements supersession chain is shorter than the note's. Emits a statements sidecar attestation, advancing its chain.

This is the bookmark for stage transition: a confirmed note with current statements is *ready for claim decomposition*.


## Stage 2 — Sequential Bridge: claim_decompose

The note → claims transition is the spine's primary sequential hand-off.

### Why sequential

The substrate could in principle predicate-fire `claim_decompose` on `is_claim_confirmed(note) ∧ ¬has_decomposition_provenance(note)`. Why is it operator-gated today?

- *Cycle-control discipline* — the operator wants to inspect the confirmed note before committing to claim decomposition. Decomposition is expensive (LLM cost, downstream formalization work) and the operator wants explicit gate timing.
- *Protocol stage transition marker* — operator invocation makes the stage transition visible and timestamped, useful for audit and debugging.

Per [`../agents/README.md`](../agents/README.md)'s discussion of operator-gated agents: `claim_decompose` is in the *(a) eliminable-by-predicate-registration* category. The substrate spec admits its eventual stigmergization; current operator gating is operational discipline, not architectural necessity.

### claim_decompose — derive claims from confirmed note (sequential)

`claim_decompose` (Family G identity-grant-only, operator-gated) fires when the operator runs the script. One fire = mechanically split the source note at `## ` headers, run a decompose prompt in parallel on each non-structural section, then for every extracted claim:

- write the claim md file under `_docuverse/documents/claim/<asn>/`
- emit substrate identity facts: `claim` Classifier, `label` and `name` sidecars, `provenance.derivation` from source note
- after all claims, emit `transclusion.claim-statements` and supersede the note's statements sidecar

Each derived claim is now a substrate citizen with identity. Stage 2 is complete.


## Stage 3 — Per-claim Formalization (stigmergic spine, parallel across claims)

Each derived claim moves through a fixed formalization sequence. The agents fire in parallel across claims (the runner walks all claims) but in deterministic order on any given claim.

### One-shot identity grants (Family D)

- **`claim_contract`** — classifies the claim's contract kind (theorem / lemma / corollary / definition / axiom / etc.). Trigger: claim lacks a `contract.<kind>` Classifier. Emission: one Classifier link.
- **`claim_formal_contract`** — synthesizes a `*Formal Contract:*` section in the claim md body (when the kind requires one). Trigger: contract.<kind> set ∧ kind requires Formal Contract ∧ no existing Formal Contract section. Emission: chain advance on the claim (substrate effect); content edit to body (out-of-band).

These are one-shot per claim. Once fired, they don't re-fire.

### Chain-advance attribute producers (Family C)

- **`citation_resolve`** — references sidecar; emits `citation.depends/forward` per ref + retractions for stale refs.
- **`claim_signature_resolve`** — signature sidecar.
- **`claim_describe`** — description sidecar.

Each fires when its sidecar's chain is shorter than the claim's chain. The trigger pattern is `is_*_fresh = ⊥`. The action runs an LLM, advances the sidecar's chain via `attest_attribute` or `register_version`.

The chain-advance pattern is what makes this part of the spine *re-entrant*: when a downstream agent edits the claim body, the claim's chain advances, and all Family C predicates flip stale on the next walk.

### Convergence at the formalization stage

When each claim has its `contract.<kind>` Classifier, its Formal Contract section (if applicable), and all Family C sidecars at chain ≥ claim chain, the formalization spine is complete. The substrate is ready for claim review and revision.


## Stage 4 — Claim Review and Revision (stigmergic spine)

This is the substantive convergence cycle. Each claim is driven toward `is_claim_quiescent` through two parallel mechanisms.

### Structural audit cycle (scout-refiner pair)

- **`claim_structural_audit`** (scout) — runs the structural validator on the claim, emits `review.structural` audit doc + per-violation `comment.violation` per detected issue. Trigger: `is_claim_audit_fresh = ⊥` (audit stale or never run).
- **`claim_structural_revise`** (refiner) — closes each `comment.violation` by addressing the structural issue, emits `resolution.<kind>` per closed comment + retractions for depends-agreement RETRACT decisions. Trigger: `is_claim_structurally_clean = ⊥`.

The pair runs as a stigmergic cycle: scout emits violations → refiner fires → refiner closes them → next cycle's scout fire emits an empty audit (clean) → cycle terminates on that claim.

### Content review cycle (producer-decomposer-refiner triple)

- **`full_review`** (producer, per-ASN scope) or **`cone_review`** (producer, per-apex-claim scope) — runs LLM review, emits `review` Classifier + `review.coverage` over the cone (or whole ASN). Trigger: target is non-quiescent.
- **`claim_findings`** (decomposer) — walks the review doc, emits per-finding `finding` Classifier + `comment.<kind>` link to each affected claim + `provenance.derivation(review → finding)`. Trigger: `is_review_decomposed(review) = ⊥`.
- **`claim_revise`** (refiner) — closes each `comment.revise` by addressing the finding, emits `resolution.<kind>`. Trigger: `has_resolution = ⊥`.

This is a three-stage stigmergic chain. Each stage's emission is the next stage's trigger marker.

### Per-claim quiescence

When a claim has:
- All structural violations resolved (`is_claim_structurally_clean = ⊤`)
- All content findings resolved (`is_claim_quiescent = ⊤`)
- All sidecars fresh (Family C predicates ⊤)

...the local scope `S_local(claim)` is quiescent (per Q10 / `quiescence.md`).

### ASN-level quiescence

When *every* claim under the source note is locally quiescent AND no per-ASN agents (full_review, etc.) are firing, the lattice scope `S_lattice(ASN)` is quiescent. Per Q9 (ScopeMonotonicity), this implies all per-claim scopes are quiescent.

This protocol's *terminal state* is ASN-level quiescence: source note confirmed, all claims formalized, all reviews clean, all comments resolved.


## Off-spine arcs (sequential interventions)

The spine described above is the primary maturation arc. Seven operator-gated agents (six categories of intervention) enable interventions that branch off the spine:

| Agent | When | What it does |
|---|---|---|
| `note_promote_open_questions` | Note has open questions worth their own ASN | Spins off new inquiries; new inquiries enter Stage 1 |
| `note_promote_out_of_scope` | Reviews flagged OUT_OF_SCOPE items worth their own ASN | Spins off new inquiries; new inquiries enter Stage 1 |
| `note_extract` | Operator decides claims should be lifted into a workshop ASN | Creates new ASN with extracted claims; workshop ASN goes through Stages 4–5 |
| `note_absorb` | Workshop ASN is ready to merge back | Integrates extension claims into base; emits self-review; standard cycle picks up findings |
| `note_clone` | Operator wants to experiment without disturbing original | Duplicates an ASN as peer; both ASNs continue through their own Stages 4–5 |
| `note_patch` / `claim_patch` | Targeted fix needed | Modifies content; emits patch-scoped self-review; standard cycle picks up findings |

Off-spine arcs are sequential because they require operator-scope decisions (when to extract, when to absorb, when to patch). They land emissions in substrate that subsequent runner walks pick up — sequential invocation, stigmergic follow-on.

The *modify-then-self-review* pattern (`note_absorb`, `note_patch`, `claim_patch`) is what makes off-spine modify operations productive: the modify-fire seeds the standard refinement cycle by emitting a scoped self-review, and the cycle drives the modified content back to quiescence.


## Protocol invariants

Properties that hold across the entire arc:

- **L1 — Substrate is monotonic at the L_K level.** R3 (TypedSliceMonotonicity) holds throughout. Every emission persists; retractions are themselves emissions.
- **L2 — Each stage's emissions are visible at all subsequent stages.** A consultation answered in Stage 1 is still in substrate (and observable) when Stage 5 fires per-claim review. The substrate is the audit trail.
- **L3 — Stage transitions are predicate-flip events.** A note moves from "open" to "confirmed" because `is_doc_quiescent ∧ ¬has_open_revises ∧ latest_review_clean` flips ⊥ to ⊤. The transition is observable from the substrate alone — no runner state, no operator declaration, no metadata.
- **L4 — Scope quiescence escalates monotonically along the spine.** Local quiescence (per inquiry, per note, per claim) → ASN quiescence (S_lattice) → cross-lattice quiescence (S_system) — each tier reachable only when all inner tiers are quiescent (Q9 ScopeMonotonicity).
- **L5 — Identity-grant-only off-spine arcs are non-disruptive at the spine level.** `note_promote_*` extracts a new ASN that enters the protocol at Stage 1; the parent note's protocol execution proceeds unaffected. `note_extract` creates a workshop ASN whose subsequent absorb is a sequential hand-off back to the parent. `note_clone` duplicates state without merging; the two ASNs evolve independently. *Modify-then-self-review off-spine arcs* (`note_patch`, `claim_patch`, `note_absorb`) are *re-entrant* — they put the target back into the maturation cycle, with quiescence lost until the patch's findings clear (see Open Questions on re-entrant protocols).


## Stigmergic Protocol composition

This Maturation Stigmergic Protocol composes Stigmergic Protocol primitives (Correction, Marker, Self-Review, Cycle — see parent [`../README.md`](../README.md) for the family taxonomy). The protocol's safety, liveness, and termination follow from the primitives' properties under standard composition rules + the substrate's quiescence-tier discipline (Q9 ScopeMonotonicity).

| Stage | Primitive(s) composed | Participants | Safety | Liveness (under fairness) | Termination |
|---|---|---|---|---|---|
| Inquiry consultation | Cycle Stigmergic Protocol | `inquiry_consult` | every inquiry receives at most one set of consultation answers | inquiry without coverage eventually receives consultations | `consultation.answer.*` covers the inquiry |
| Note drafting | Marker Stigmergic Protocol (consultation-as-marker → note_draft) | `note_draft` | at most one `note` Classifier per inquiry's `provenance.synthesis` | inquiry with consultations done eventually produces a note | `provenance.synthesis(inquiry → note)` exists |
| Note review-revise cycle | Cycle + Correction + Marker (note_review cycle; note_revise correction; note_consult sequencing-marker) | `note_review` ⇄ `note_consult` ⇄ `note_revise` | every revise comment closed iff resolution exists; review covers the note | every emitted revise eventually receives a resolution under sequencing | note reaches `is_doc_quiescent ∧ is_claim_confirmed` |
| Decompose hand-off | (sequential operator-gated; not a stigmergic primitive) | `claim_decompose` | claims emitted have correct identity + lineage to source note | (operator-driven; no fairness claim) | one fire emits all derived claims |
| Per-claim formalization | Marker Stigmergic Protocol (one-shot existence + chain-advance triggers) | `claim_contract`, `claim_formal_contract`, Family C chain-advance | each claim eventually has contract.<kind> Classifier, Formal Contract section (when applicable), and fresh sidecars | every formalization predicate eventually flips ⊤ | per-claim formalization predicates ⊤ |
| Per-claim structural cycle | Correction Stigmergic Protocol (K = `comment.violation`) | `claim_structural_audit` ⇄ `claim_structural_revise` | violation closed iff resolution exists | every emitted violation eventually receives a resolution | `is_claim_structurally_clean(claim) = ⊤` |
| Per-claim content cycle | Cycle + Marker + Correction (review cycle; review-as-marker for findings; comment-resolution closure) | `full_review` or `cone_review` → `claim_findings` → `claim_revise` | each finding closed iff resolution exists; reviews cover claims | every uncovered claim eventually reviewed; every comment eventually closed | `is_claim_quiescent(claim) = ⊤` |

Composition rules at work:

- *Stigmergic chaining* — each primitive's emissions flip the next primitive's pre-send invariant `T_A`, satisfying its initiation condition. The runner walks these chains automatically (Run1 fairness ensures every triggered primitive is eventually fired).
- *Sequential bridges* — two operator-mediated transitions (inquiry creation, claim_decompose) interpose between stigmergic chains. Their soundness follows from the operator emitting the right substrate facts; their liveness is operator-side (not a runner-fairness claim).
- *Quiescence-tier composition* — primitives terminate at sub-scope quiescence (per-comment, per-claim). The Maturation Stigmergic Protocol terminates at the next outer tier (per-ASN lattice quiescence). Q9 (ScopeMonotonicity) makes the composition sound: if every sub-scope is quiescent and no outer-tier agent fires, the outer scope is quiescent.
- *Re-entrancy from off-spine arcs* — Self-Review Stigmergic Protocol off-spine fires (`note_patch`, `claim_patch`, `note_absorb`) reset some primitive's pre-send invariant from ⊤ back to ⊥. The cycle re-enters; the primitive's termination property still holds, but the system passes through the sub-quiescent state more than once.

The substrate-spec proof techniques transfer directly:

- *Primitive safety* is proved per-instance from `Post_A` (emission contracts in `PL`).
- *Primitive liveness* under fairness is proved per-instance from `T_A` semantics + Run1 fairness + Run2 (RunnerSatisfiesQ6) at the per-instance scope.
- *Primitive termination* is per-instance quiescence — a special case of Q4 (ConditionalTermination) restricted to the instance's args.
- *Maturation Stigmergic Protocol properties* follow from primitive properties + Q9 (ScopeMonotonicity). The proof is structurally similar to standard distributed-systems protocol composition arguments, with stigmergic message passing as the primitive medium.


## Scope-tier escalation

This protocol is fundamentally a story about *escalating scope quiescence* through Q10's tiers.

| Protocol stage | Active scope | Quiescence target |
|---|---|---|
| Inquiry → consultations | `S_local(inquiry)` | inquiry has consultation coverage |
| Note draft | `S_local(note)` | `provenance.synthesis` exists from inquiry to note |
| Note maturation cycle | `S_local(note)` (expanded over reviews + comments + sidecars) | `is_doc_quiescent(note) ∧ is_claim_confirmed(note)` |
| Decompose to claims | `S_local(note) ∨ ⋁_i S_local(claim_i)` | claims have identity + statements transcluded |
| Per-claim formalization | each `S_local(claim_i)` independently | sidecars fresh, contract classified, Formal Contract synthesized |
| Per-claim review | each `S_local(claim_i)` independently | `is_claim_quiescent(claim_i)` |
| ASN-level quiescence | `S_lattice(ASN) ≈ S_local(note) ∨ ⋁_i S_local(claim_i)` | every claim locally quiescent AND no per-ASN reviewer fires |

Scope predicates compose by Boolean disjunction (per quiescence.md Layer 4's framing); the dynamic interpretation `[S]_Σ` is a finite address-set obtained by filtering the address universe with `S`. The `≈` for `S_lattice(ASN)` reflects Q10's lattice scope including not just per-doc local scopes but also tuples whose F or G slots reference any doc in the lattice — a strict superset of the per-doc disjunction.

Cross-lattice scope (`S_system`) sits above. This protocol does not normally drive cross-lattice quiescence — that's the bridge_probe / synthesis-producer arc (a separate Stigmergic Protocol, not yet documented).


## The termite analogy

The protocol's structural shape is recognizably stigmergic in the original biological sense (Grassé 1959). Four explicit mappings:

(1) *The substrate is the nest.* A public, durable, accumulating record of every action ever taken. Every termite (every agent) reads it; every termite leaves traces in it. No agent communicates directly with any other. Coordination is entirely substrate-mediated.

(2) *Castes are termite roles.* Producer (build identity), refiner (close findings), scout (detect issues). The caste differentiation is functional, not biological: a Python class is in `agents/refiners/` because that's the structural role its substrate effects play. Caste boundaries are firm at the substrate-effect level (AG5 PublicPrivateAsymmetry); fluid at the implementation level (LLM-as-scout inside producer body, compound-emission lattice ops).

(3) *Pheromone gradients are predicate flips.* In termite mounds, build-pheromones decay over time, gradient-following creates emergent structure. In our system, predicate flips are sharper — a `comment.revise` either has a `resolution` or it doesn't; substrate tuples are monotonic, not gradient-decaying. But the structural role is the same: agents fire because some predicate they read indicates "work needed here," and their emissions leave traces other agents respond to.

(4) *Quiescence is a saturated nest.* When every agent's trigger is false on every args (Q0), no further fire is pending. The colony rests. This is exactly what termites do when the nest is built — they don't keep building because no pheromone gradient pulls them anywhere. The system has reached a state where every reader's check is satisfied.

The analogy is imperfect — termite stigmergy uses gradient-decaying physical traces; our substrate is monotonic typed-tuple emissions. The biological caste differentiation is morphological; ours is structural-functional. But the *coordination mechanism* is the same: decentralized, environment-mediated, emergent. The protocol layer is where this coordination produces complex structure (a confirmed-and-quiescent claim is the protocol-stack equivalent of a finished termite mound: the local rules are simple; the emergent product is a maturation arc with stage transitions, scope-tier escalation, and architectural invariants).


## Open questions

Protocol-layer concerns the substrate spec flagged for resolution at this layer:

- *Cross-tier interference.* `quiescence.md`'s open question on outer-scope agents firing during inner-scope quiescent windows. Concretely in this protocol: a `cone_review` on apex `c_1` can introduce findings affecting `c_2` (downstream of `c_1`'s cone); when `c_2` was previously quiescent, the new findings flip its trigger back to ⊥. This is exactly the cross-tier interference scenario. Protocol implication: per-claim quiescence is provisional; ASN-level quiescence is the actual stable target.
- *Sequential hand-off elimination.* The two sequential hand-offs on the spine (inquiry creation, claim_decompose) are eliminable per [`../agents/README.md`](../agents/README.md)'s (a)-category analysis. Whether to eliminate them, and the operational discipline that justifies retaining cycle-control gating, is a design decision pending.
- *Off-spine arc ordering.* `note_promote_*`, `note_extract`, `note_clone`, `note_patch`, `claim_patch` can fire at multiple protocol stages. When does each make sense? The protocol prose above gives a sketch; explicit protocol-stage ordering rules would strengthen the operator runbook.
- *Per-claim-vs-ASN-level review choice.* `cone_review` is per-apex; `full_review` is per-ASN. The choice between them at any given stage depends on registry-design conventions not fully captured here. A protocol-level rule would help: e.g., "cone_review for incremental work; full_review only at stage transitions."
- *Cross-lattice protocol composition.* The protocol described here ends at ASN quiescence. The cross-lattice synthesis Stigmergic Protocol (involving `bridge_probe` once implemented, and a downstream synthesis producer) is a separate story not yet traced. When two ASNs in different lattices reach quiescence, what triggers the bridge-probing? What's the protocol's exit condition at the cross-lattice tier?
- *Re-entrant protocols after off-spine intervention.* When an operator runs `note_patch` on a confirmed note, the note re-enters its maturation cycle (the patch's self-review emits new findings). The protocol is *re-entrant* — quiescence is not a permanent state. When does an ASN re-confirm after a patch? What invariants survive the perturbation? These are real questions not answered by the substrate spec alone.


## Cross-references

- *Substrate spec:* [`../substrate/`](../substrate/) — the formal definitions every claim in this protocol relies on (R0–R7, Sh-conf + Sh0–Sh5, PC0–PC6, AG0–AG7, Q0–Q10, Run0–Run5).
- *Agent registry:* [`../agents/`](../agents/) — per-agent specs for every agent named in this protocol. The README ([`../agents/README.md`](../agents/README.md)) has the caste taxonomy, the registry table, and the two hand-off types this document composes.
- *Operator runbooks:* (operator-side documentation) — workspace conventions, spec-md formats, script invocations for the sequential hand-offs (inquiry creation, claim_decompose) and off-spine arcs.