## What this is

ASN-0126 defines the **type-registration and admission-control layer for the link (typed-relation) subsystem**. On top of ASN-0086's open `(F, G, K)` substrate it adds a fixed three-shape vocabulary (Unary / Binary / Multi), an immutable per-substrate registry that apps populate at construction, and a static conformance gate the substrate runs at every link emit. It governs *only* the link-emit path; content writes and document allocation are untouched by it.

## Design commitments

These are forced by the claims and downstream design cannot violate them:

- **Every gated link has exactly one source span: `|F| = 1`.** Not zero (no unattributed/empty-from links), not many (no disjoint multi-passage source). The one span is always a connected reach. Empty-from emits — including ASN-0086's original `Nullify` — have *no gated image at all*; they are not rejected with an error, they simply are not steps of `→_sh`.
- **There are exactly three shapes, and a shape constrains only span counts, never coverage.** Unary forces `G = ∅`; Binary forces one G span; Multi places no real bound on G (it only re-asserts `|F| = 1`). Multi structurally subsumes the other two.
- **The registry is immutable and written exactly once — when `Σ_init` is built.** There is no runtime registration. Shape lookup is therefore a constant against a finite, fixed table at every reachable state (P1, P2). This is the keystone: it makes the gate decidable, stateless, and concurrency-free.
- **Types are identified by the *coverage class* of an endset, not by a name.** The registry key is `[K]`; the value is a bare shape. Human-readable labels ("citation," "comment") are app-side conventions over addresses, never substrate state. All type comparison runs through the same coverage-equality decision used everywhere else.
- **The gate adds preconditions only — it never alters the deposit (effect-identity).** A gated emit stores exactly what an ungated one would, at the same fresh address. The whole framework is a refinement that projects cleanly back onto ASN-0086 (the `π` bridge). Violating effect-identity — e.g. "helpfully" normalizing the value inside the gate — would break that bridge.
- **The gate consults no residence check.** It reads span counts and `shape(K)` only; endset spans may name ghost addresses with no stored content. This is inherited and deliberate.
- **Conformance is a born-once, permanent property of every stored link (P3, P6).** Once a tuple is in the store it conforms forever; shape, registration, and the conformance verdict are all state-independent (P4).
- **Retraction must carry a source in this framework.** It is re-expressed as an *attributed Binary* link. The empty-from form is gone by construction.

Conventional (not forced): the canonical retraction from-fill `r = (d_retr, δ(1, #d_retr))`; which types an app registers and with what shapes; single-tuple retraction scope (an app obligation, *not* enforced).

## What must be built

- **A registry:** a finite, immutable map from coverage classes to shapes, populated at construction and never mutated. Must answer "is this type registered?" and "what shape?" by coverage-equality against stored representative endsets.
- **A span-count classifier:** given an endset (a finite *set* of spans), report whether F/G is empty, a singleton, or larger. It must measure span count, *not* coverage, and must not coalesce adjacent spans.
- **A conformance check:** for registered K, decide `Sh-conf` from `shape(K)` and the F/G span-count classes. Pure function.
- **A gated link-emit path:** at every link emit, run, in order, (0) arity-3, (i) registered, (ii) conforming, before depositing; on any failure, no state change.
- **A retraction wrapper** that re-expresses nullify as an attributed Binary emit with the canonical from-fill.
- **A nullification / active-subset derivation** (largely inherited): among well-formed emits, decide which are active versus *born nullified*, and surface only active tuples to queries.
- **An address allocator** (`a_emit`): hand out the next free slot in a home's sibling chain — the chain's *frontier*.

## Implementation approaches

**Registry storage and lookup.** Because the registry is write-once and tiny (an app's type vocabulary — dozens of entries, not millions), this is the *simplest* persistent object in the system, simpler even than Green's append-only spanfilade: nothing ever appends to it. Two realistic options:

- *Linear scan over stored representatives,* running coverage-equality per entry. Honest, trivially correct, and its O(registry size) cost at each emit is negligible given the bound from C0. Pick this by default.
- *A canonical-key index.* If your type-vocabulary convention is unit-depth singleton endsets `[k]` (as in the note's worked example), coverage equality collapses to *prefix equality* on the tumbler `k`, so you can key an ordered map or radix structure by that prefix and get O(log n) lookups. Pick this only if the registry is large enough to matter or you want the index for other reasons.

Critically, **do not use the `im` crate's persistent maps here.** Persistent (structurally-shared) structures earn their keep under mutation with many shared versions; the registry has exactly one version forever. A plain shared read-only table (an `Arc`-shared immutable map) is strictly better — and it needs no locking, no MVCC, and no torn-read protection, because it is never written after construction. That is a real operational win over the link journal, which does need append discipline.

**Endset representation and span counting.** This is where a naive optimization silently breaks the gate. The udanax-green evidence is unambiguous: Green does **not** coalesce adjacent endset spans — a coverage-contiguous source can be stored as several spans, and its merging logic (`putvspaninlist`) is used *only* for document V-span coverage, never on the link path. Span count and coverage genuinely diverge (one span can carry infinite coverage; two abutting spans can equal a one-span source's coverage). Therefore: **represent endsets as explicit, un-coalesced sets of spans, and keep the coverage-merging path strictly separate from the link path** — exactly Green's split. The good news is the gate never needs a full count: Unary/Binary/Multi only ever ask "empty / singleton / more," a cheap three-way classification.

**The conformance check.** Trivial pure function once the above exist. The only subtlety is partiality (`Sh-conf` undefined for unregistered K). Handle it by *ordering* the gate: check (i) registered before (ii) conforming, so "undefined" never surfaces at runtime — an unregistered emit short-circuits at (i).

**The gated emit choke point.** This is admission control at one place. Effect-identity says you bolt the three-precondition guard onto the *existing* link-deposit path; you do not fork storage. The link store itself is well-served by the proven approach this repo already uses and Green validates structurally: an **append-only journal of link emissions, recovered by replay** (the `links.jsonl` + `paths.json` pattern; Green's permanent I-space link orgls and write-only spanfilade are the same commitment). The registry is *not* part of that journal — nothing appends to it — so store it as a construction-time manifest loaded once before replay begins. The registry is recovery *input* (every journaled step was gated against it), not recovery *output*.

On replay you may, but need not, re-run the gate: P6 guarantees every journaled tuple already conforms, so the journal is authoritative. Re-gating on load is therefore a *defensive integrity check*, not a correctness requirement — cheap enough to be worth running, but treat its verdict as corruption detection, not as authority.

**Two outcomes, two mechanisms — keep them apart.** Clearing the shape gate only earns a tuple a place in the permanent *audit slice* `L_K` (`dom(Σ.L)`). Whether it is *active* (`A_K`) or **born nullified** is a separate, *dynamic* decision (the wp's C2 self-nullification and C3 pre-existing-covering-retraction). Put each function where it belongs: the shape gate is static, pure, and lives at emit; the nullification filter is dynamic and belongs at query time (or as a derived index), and `Observe_K` must read the active subset, never the raw audit slice.

**Nullification / active-subset index.** This is a textbook *hint*: the authoritative source is the link journal (the retraction tuples), and the nullified set is fully recomputable from it. Maintain a nullified-address index incrementally as retractions are emitted (each retraction's to-coverage marks addresses dead) and rebuild it on recovery by replay. If it is ever lost or suspect, recompute — do not treat it as authoritative duplicate state.

**Address allocation (`a_emit` / frontier).** `a_emit` returns a home's frontier — the first unfilled sibling slot — exactly Green's `findnextlinkvsa`. FrontierUnification guarantees every deposit lands at the frontier and advances it by one, so accelerate emit with a **per-home frontier counter** (another hint over the journal), rebuilt on recovery by replay rather than re-scanned each time.

**Retraction wrapper.** Provide `Nullify_Binary` as the blessed, substrate-side entry point that fills the canonical from-fill `r` by construction. The from-fill is what makes a retraction attributable (it answers *who retracts*, at whole-document granularity) and discoverable by an under-`d_retr` `Observe_R` pattern. Raw `Emit_R` with a different source clears the Binary gate but escapes that match, so the wrapper, not raw emit, is the contract you expose for retraction. This is faithful to Green, where retraction is not a delete opcode at all but a permanent link plus a POOM excision — and where a single range delete can withdraw a contiguous run of links, which is precisely the range-retraction the note models.

**Sterilization containment (Open Q7).** The wp analysis exposes a sharp hazard: a single gate-clearing *range-G* retraction whose to-coverage reaches a home's *unfilled* frontier slots poisons that whole block — every future deposit there is born nullified, irreversibly, of any type. The spec leaves the *policy* open. Two implementation stances:

- *Do nothing* — sterilization is an app obligation (route retractions through the unit-depth wrapper **and** aim at a P-tgt-valid target). This is the spec's default and the cheapest correct choice.
- *Substrate containment* — at retraction time, reject (or warn on) a to-coverage that reaches past the filled region into the home's frontier. The frontier and the to-coverage's reach are both already computed, so the check is cheap; it is added mechanism for added safety.

Pick "do nothing" unless a deployment specifically needs the guard; if you add it, it is a pre-emit check on the retraction path only.

## Guarantees to uphold

| Guarantee | How it holds |
|---|---|
| Registry never drifts (P1); shape stable (P2) | **By construction** — never expose a registry mutator. |
| `|F| = 1`; shape conformance of every emit (P3) | **Active** — the gate, at every link emit. |
| Conformance permanent over a tuple's life (P6) | By construction once stored (link immutability, append-only journal). |
| Conformance/registration state-independent (P4) | By construction, given P1 — the gate reads only span counts and the invariant registry. |
| Type identity by coverage class | **Active** — route *all* type comparison through coverage-equality. |
| Effect-identity (gate changes nothing it deposits) | **By construction/discipline** — easily broken; guard against any value mutation inside the gate. |
| Retraction attribution + under-`d` discoverability | **Active** — only if retraction goes through the canonical wrapper; not gate-enforced. |
| Single-tuple retraction scope | **Not a substrate guarantee** — app obligation (or optional containment). |
| Permanence of stored tuples and of nullification | Inherited; **by construction** with an append-only journal. |

## How it fits

- **Leans on ASN-0086** (the typed-relation substrate): `Emit_K` / `Observe` / `Nullify`, the `→` step relation, the active-subset / nullification machinery, coverage-equality decidability, the admissible-type set, and the layer discipline. This note *refines* ASN-0086's link-emit step and *adjoins* the registry; the forgetful projection `π` carries every gated run back to a plain ASN-0086 run, which is how all the inherited results (immutability, retraction stability, the wp skeleton) are imported — with the explicit caveat that *layer-scoped* results do not transfer, because a gated Binary retraction can take steps the original unit-depth discipline forbade.
- **Leans on ASN-0043** (`Endset = 𝒫_fin(Span)`, coverage, prefix-span coverage, link immutability, the standard-triple shape, ghost-address permission) and **ASN-0034** (tumbler ordering and the strict-increase / shift monotonicity that the chain-ascent and frontier arguments rest on — Green's `tumbleradd` provides exactly this `s ⊕ ℓ > s` for valid addresses).
- **Hands to** the successor note(s) that layer *operational semantics* on this vocabulary: idempotence, the behavior catalog, default predicates, predicate composition. This is the schema/admission layer those build on; its Open Questions are explicitly theirs.

Within the stack it sits directly above the raw typed-relation substrate and directly below behavioral semantics — the link subsystem's **type schema and gate**.

## Decisions for the builder

These are implementation choices this note leaves to you (distinct from its spec-level Open Questions for the successor note):

- **`Σ_init` authoring interface.** Construction is the only write to the registry, so you choose how an app *declares* its `[K] ↦ shape` entries — config manifest, builder API, etc. The substrate must support the empty registry (a permanently *link-inert* substrate that can still grow content and documents) as a legal configuration.
- **Registry persistence layout and lookup:** manifest-loaded-before-replay vs journal header; linear scan vs canonical prefix-keyed index (above).
- **Whether to re-gate on replay:** trust the journal (P6) vs defensive re-verification as a corruption check.
- **Concrete endset representation:** any structure that *preserves span count* on the link path (sorted vector of spans, etc.), and a clear boundary marking where coalescing is permitted (coverage computations) and where it is forbidden (the gate).
- **Nullified-set strategy:** recompute-on-demand vs incremental index; rebuild-on-recovery policy.
- **Frontier acceleration:** per-home counter cache vs journal scan.
- **Retraction wrapper placement:** substrate-provided helper (recommended — the from-fill is normative) vs client convention.
- **Sterilization stance under the open policy:** enforce nothing (app obligation, the spec default) vs add a substrate pre-emit containment check.
