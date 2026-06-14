## What this is

ASN-0125 defines the **link-editing / versioning capability** of the substrate: how a user "edits" an immutable link. It establishes that EDITLINK is not a primitive but a *composite* — allocate a fresh successor link, then assert a first-class, owned, disputable *supersession claim* relating old to new — and it specifies the supersession relation, its two read views (permanent history vs. revisable operative graph), and the queries (discovery, currency) built on them.

## Design commitments

These are locked in for everything downstream. I mark each **[forced]** (the substrate or an upstream invariant leaves no choice) vs. **[chosen]** (this note's convention; a different layer could decide otherwise).

- **A link is never rewritten in place; "editing" is allocation + assertion. [forced]** EL0 shows the mutation postcondition is not merely unimplemented but *unimplementable* (`wp(S, "L(a)=w") = false` for `w ≠ ℓ₀`). The original stays readable at its own address, with its exact original value, in every future state — unconditionally. No downstream design may offer an in-place update path; there is nothing to implement behind it.
- **Intent is not in the state; a relationship exists only if explicitly asserted. [forced]** EL1: an emission performed "as an edit" and an independent creation with the same parameters are the *same transition with the same post-state*. Value resemblance — even byte-identity — carries zero relational information. Consequence: **no automatic version detection is ever possible**, before or after the fact. Supersession is made, not inferred.
- **The supersession record is a freshly allocated, first-class, addressable link — not a field, not a status flag, not an address-nesting convention. [forced]** EL2 closes every in-place carrier (original's value, successor's value, the address relation, any index marker); EL3 shows the only surviving carrier under this substrate is a typed link-to-link tuple. Critically, "a separate supersession link" and "a typed relation" are *the same object*, not alternatives.
- **The claim's kind is carried by the coverage class of its type slot. [forced mechanism / chosen class]** The only interpretation-free, decidable, *refinable* kind mechanism is the type-slot coverage class (the substrate never reads stored content as semantics). That supersession is `[K_sup]`, distinct from the retraction class `[R]`, is the chosen instantiation; that kind lives in a coverage class is forced.
- **Directionality: from-set = the superseding (new) link, to-set = the superseded (old). [chosen]** "F replaces G," aligned with retraction's acted-upon side.
- **Two views, permanently split: a historical record that is append-only and never erased, and an operative graph that is revisable by retraction. [forced]** This is the spine. `succ_h` is monotone; `succ_o` = `succ_h` minus nullified claims. This split — *not* deletion — is how "claims can be wrong" coexists with "nothing is ever erased."
- **Supersession and retirement are independent acts. [forced]** EL9's three axes — resolution (permanent, ungated), listing (mutable both ways), activity (monotone-down) — are independent, and *superseding moves none of them*. "Supersede and retire" is available only as an explicit second act.
- **"Current version" is irreducibly set-valued; there is no canonical "latest." [forced]** Linear (1), forked (≥2), and standoff (0) results are all reachable; EL13/EL14 prove no state-definable selector recovers a recency-respecting "latest" across homes. The layer owes **disclosure, not decision**.
- **Every surviving reference binds an address, never a position. [forced]** EL10: listing positions re-bind across edit/curation churn; addresses never do.
- **Completeness of the record is a protocol property, not a substrate invariant. [forced]** No coupling constraint can fire on "is an edit," because the distinguishing fact is absent from the state (EL1). The substrate guarantees only the *standing of declarations once made* — permanent, attributed, decidable.

## What must be built

- **An append-only, fresh-key-only link allocator.** One kind of change to the link store: extension at a never-before-used address, homed on the issuing document's flat sibling chain. Must guarantee address freshness even after a link is de-listed.
- **An assertion capability (`assert_sup`).** Given two existing link addresses and a home document, allocate one fresh typed claim "x supersedes y" — at *any* later state, by *any* principal holding a home.
- **The edit composite (`editlink`).** Allocate the successor (the new reading), then assert it supersedes the original. Exactly two allocations; nothing else in state touched. Must also express the degenerate cases: a value-identical edit (re-home/re-attribute) and a *revert* (assertion alone, no successor).
- **A typed-class mechanism** that marks, decidably distinguishes, and *refines* (subtypes) the supersession class via type-slot coverage.
- **The historical/operative read model.** Maintain the full claim history (never pruned) and derive the operative graph by filtering nullified claims.
- **Discovery, in two regimes.** *Archival* (`in(y)`, `out(x)`) computable from the link store alone, at every state, regardless of arrangement; *contextual* — a claim surfaces in a document iff that document currently lists the endpoint.
- **Currency.** A set-valued `current(y)`: operative sinks reachable via `succ_o`, returned *entire*, each member carrying its supporting claims, their homes, and its own activity status.
- **Retraction (`Nullify`, from upstream) wired in** as the sole demotion path — removes a claim from operative standing without erasing it.
- **Attribution** of any claim to its home, derived from the address alone.

## Implementation approaches

**Link store & allocation.** Use an **append-only journal recovered by replay** — exactly this repo's `links.jsonl` + replay model, and the proven shape of udanax-green's granfilade, where (per the evidence) no code path ever mutates a link's endsets in place and every change is a fresh, monotonically-advancing address. The append-only log *is* the immutability invariant made physical: with no overwrite path in the code, EL0/L12 holds by construction rather than by checking. For the in-memory index, a **persistent (structurally-shared) map** (the `im` crate's HAMT) keyed by link address is the right fit — the store is only ever extended at fresh keys, so there is no contention on existing entries and snapshots share structure for free.

- *Critical "give-up" to be explicit about (Lampson):* **do not content-address the link value for identity.** Links may be byte-identical yet distinct (NonInjectivity); identity is by origin/address, never by value. Content-addressing the underlying spans/content is fine and orthogonal; deduping *links* by endset-hash would be a correctness bug.
- *Allocation:* the next address is the home chain's current max + one flat sibling. Keep a per-home **last-allocated hint** (recomputable by scanning the journal on a miss) rather than authoritative duplicate state. The evidence confirms Green forces successors to flat siblings via its molecule allocator and that the document-style *nesting* allocator is unreachable from link creation — so a flat per-home counter, not a tree, is the proven shape.

**The supersession claim reuses the link store.** A claim *is* a link (EL3), so it lives in the same journal and index — **no separate supersession store.** The evidence is direct here: in Green, link endsets can hold another link's address-span and the endpoint index treats link-to-link spans identically to text spans, so "link-between-links as a supersession record" is mechanically the same machinery, not new machinery. Represent the type as the canonical type-slot coverage and compare with the decidable coverage-equality; mint subtypes as prefix-extended coverages so they stay jointly queryable by one rooted span. If you shortcut to an opaque enum tag you get faster comparison but **lose refinement (subtypes)** — take that shortcut only if you're certain you'll never subtype "correction vs. restyle."

**Historical/operative split — the read model.** Treat the journal as authoritative and build the read views as **hints (recomputable on a miss), never as separately-editable authoritative state.** Both underlying sets are *monotone*: `succ_h` (all `[K_sup]` claims) only grows, and the nullified set (all `[R]` targets) only grows. So:

- Maintain an in-memory **successor graph** for `succ_h` (edges never invalidated) and a growing **nullified set**; derive `succ_o` by filtering edges whose *claim address* is nullified — at query time. Because both inputs are append-only, the indexes need no entry-removal logic at all; Nullify *adds* to the nullified set, it does not delete a claim.
- The cheaper alternative — keep no indexes, scan the journal per query — is fine for small stores and trivially correct; I'd pick it for a first cut and graduate to the maintained graph when chain/fan-out sizes warrant.
- *Why not store a "current/superseded" marker on the entries?* Green's own history is the cautionary tale: the evidence shows its one attempt to make link-version-following structural was abandoned behind a hard-coded-`FALSE` branch, leaving old and new links equally live. That is the right outcome here too — the operative view is a **derived filter over monotone records**, not a mutable flag that could diverge from the log.

**Endpoint indexes for archival discovery.** `in(y)`/`out(x)` need a reverse map from an endpoint address to the claims referencing it, split by slot (to-side vs. from-side). This is precisely an **append-only endpoint index** — Green's spanfilade, which the evidence confirms indexes link-orgl spans exactly as text. Build it as a hint from the journal. A **persistent map** `address → set-of-claims` (per slot) suffices *because the discipline restricts claims to unit-depth single-address spans* — you never need range queries over the endpoint. Keep the range-capable enfilade structure in reserve only if you later relax the discipline to allow span-valued endsets; that's the one change that would force the heavier structure.

**Currency computation.** `current(y)` is a bounded graph reachability + sink test over the operative successor graph. **Compute on demand** (BFS/DFS over the hint graph) — chains are short in the common case, the result changes on every assert/retract, and precomputing it for all links would be churn for no benefit. Terminate naturally on the finite address set; handle revert 2-cycles (they're the standoff case → empty sink set, which is a *legitimate* answer to disclose, not an error).

**Recovery.** Replay the journal to rebuild the link store, the `succ_h` graph, the nullified set, and the endpoint indexes — all deterministic functions of the log. For large stores, **checkpoint the persistent maps** as snapshots and replay only the tail; the structural sharing makes snapshots cheap. Resolving any single link by address must be a **direct store descent needing neither the arrangement nor an "open document"** — the evidence shows Green resolves a link orgl by pure granfilade descent with the open-document gate explicitly bypassed, which is the behavior to preserve (EL9 axis 1).

**Attribution** needs no store: the home is a field-projection of the claim's address. Resolving home → named principal is the ownership layer's job, not this one's.

## Guarantees to uphold

**Hold by construction** (given an append-only store, a fresh-key allocator, and address-projection):

- **Permanence** — original, successor, and every claim remain readable at their addresses with exact values, forever (append-only ⇒ no overwrite path).
- **Record permanence** — `succ_h` is monotone; no claim is ever lost.
- **Address uniqueness** — every allocation is fresh and never reused (requires the allocator to never recycle an address even after de-listing — the one active obligation inside this "by construction" set).
- **Attribution** — every claim is signed by its home, decidably, from the address alone.
- **Endpoint frame** — asserting changes neither endpoint; **reference survival** follows (any pre-existing reference keeps value, coverage, and referent across the edit, and reaches the successor by one archival query).

**Require active enforcement** (protocol discipline at the editing layer):

- **Schema conformance / single-target decidability** — claims must use canonical unit-depth single-address spans and be irreflexive; enforced at assertion time. This is what makes `old`/`new`/`addr` total and `in`/`out` cheap.
- **Non-destructive demotion** — Nullify must be the *only* path out of operative standing, and history must never be pruned.
- **Record completeness** — that every edit is actually asserted (route all edits through the composite). The substrate *cannot* enforce this; if a client emits a bare successor without the claim, the relationship simply does not exist and **cannot be reconstructed later** (EL1).
- **Currency "honesty"** — never fabricate a single "latest." Forks (≥2) and standoffs (0) are correct outcomes to disclose; uniqueness is a reader policy, never a substrate promise.

## How it fits

This is a thin **editing/versioning layer** sitting *above* the typed-relation layer and *above* the substrate:

- **Leans on the typed-relation layer (ASN-0086)** for everything structural — coverage classes, typed slices, the emit/observe/nullify operations, the retraction class `[R]`, and emission addressing. Supersession is *just a designated coverage class* in that layer plus a discipline; `assert_sup` is its `Emit`, currency is built on its `Observe`/`Nullify`.
- **Leans on the immutability and allocation invariants (ASN-0043 / ASN-0093)** for the premise (links are fixed, addresses are fresh flat siblings) and on the **state/transition model (ASN-0047)** for atomic, totally-ordered transitions and the elementary `K.λ` writer.
- **Leans on the span/coverage and persistence/projection results (ASN-0034 / ASN-0098)** for endset coverage, prefix-span semantics, projection (contextual discovery), and unconditional link persistence (resolution axis).
- **Leans on the arrangement/containment layer (ASN-0047)** for listing — contextual discovery is gated by a document's current arrangement.
- **Hands to the ownership layer (ASN-0042)** the home → principal resolution that attribution stops short of.
- **Hands to reader/client layers** the set-valued currency result plus disclosure, for them to narrow by policy.

## Decisions for the builder

- **Pick the concrete supersession class and its subtype layout.** The note fixes only that `[K_sup] ≠ [R]`. You choose the actual coverage class and how correction/revision/etc. subtypes nest under a shared, agreed root so they stay jointly queryable.
- **Pick the class-comparison representation:** full coverage-class equality (spec-faithful, refinable) vs. an opaque tag (faster, no subtypes). Choose by whether you need refinement.
- **Pick the index strategy:** persistent keyed map (sufficient while claims are unit-depth) vs. range-capable enfilade (only if you'll allow span-valued endsets later).
- **Pick hint vs. recompute, and the snapshot policy:** maintain the successor graph / nullified set / endpoint indexes in memory (fast queries, replay-on-restart) vs. scan the journal per query (simplest, correct). Decide checkpoint cadence for recovery.
- **Choose the reader's default currency policy.** The substrate returns `current(y)` entire with attribution and per-member activity; the *client* must default to something — trust only the original owner's claims, prefer a curator, follow per-home latest, drop members whose own link is retracted. None of these is the substrate's call.
- **Decide how the editing layer routes operations** so discipline holds — e.g., a single `editlink` entry point that always performs both steps, and how (or whether) to flag bare emissions that "look like" unasserted edits, knowing they can never be recovered after the fact.
- **Design the fork/standoff workflow.** When `current = ∅` (mutual supersession) or `≥ 2` (fork), decide the presentation and the repair affordance (which claim to Nullify). The substrate makes the standoff survivable; the workflow is yours.
- **Decide the listing default.** The successor is *born unlisted*; seating it in a document's arrangement is a separate act. Choose whether your "edit" gesture also re-lists the successor in place of the original, or leaves listing to a deliberate second step — and remember to bind that listing to the successor's **address**, never its position.
