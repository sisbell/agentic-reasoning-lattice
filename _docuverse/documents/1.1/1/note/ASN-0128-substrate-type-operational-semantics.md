# ASN-0128: Substrate Type Operational Semantics

*Idem semantics at emit, behavior catalog, default predicates, and standard registrations — the operational layer above ASN-0126's shape framework*

ASN-0086 supplies the typed-relation primitives `Emit_K`, `Observe`, `Nullify` over arity-three tuples. ASN-0126 narrows the framework: single-span sources (`|F| = 1`), three shapes by G span count (Unary `|G| = 0`, Binary `|G| = 1`, Multi `|G|` finite), a static shape-conformance gate applied at every emit via the refined transition relation `→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh`, and an immutable registry keyed by coverage class whose value is the type's shape — and the shape alone. What ASN-0126 deliberately defers to a successor (its Open Questions 1–4) — what idempotence *means* at emit, which behaviors the substrate provides, what predicates every registered type receives, and whether any types ship pre-registered — is the subject of this note. The standard retraction registration additionally settles ASN-0126's Open Question 7 (sterilization containment) at the operation surface.

**Depends:** ASN-0043 (Link Ontology), ASN-0086 (Typed Relations on Address Sets), ASN-0126 (Substrate Shape Framework).

## What this note commits

- **Registration record.** Extends the registry value from the shape alone (ASN-0126, The registry) to the triple `(shape, idem, behaviors)`, with a well-formedness condition and invariance inherited from ASN-0126's write discipline.
- **Idem operational semantics.** Specifies what `K.λ_sh` does when the emitted tuple is "the same" as an existing active tuple of a type this registry marks idempotent — including the criterion of sameness (coverage equality), interaction with nullification, born-nullified emits, and concurrent writers. Answers ASN-0126 Open Question 1, whose "successor registry" is the registration record above.
- **Behavior catalog.** Four substrate-provided behaviors apps optionally attach at registration: read-filter, transitive-closure, typed-reverse-lookup, age-staleness. Each unlocks specific predicates whose semantics this note pins. Answers ASN-0126 Open Question 2.
- **Default predicates.** Three predicates every registered type receives, derived from ASN-0086's `Observe_K`. Answers ASN-0126 Open Question 3.
- **Standard registrations.** Three coverage classes the substrate pre-ships in `Σ_init.registry` — the retraction relation R and two universal lifecycle markers — settling ASN-0126 Open Question 4 (which left open whether anything ships pre-registered). R's registration policy routes all retraction through the unit-depth wrapper `Nullify_Binary` and preconditions P-tgt, turning the P-tgt-*conditional* postconditions of ASN-0126's Nullify_Binary contract into guarantees and settling Open Question 7 — and, on surface-disciplined substrates, restoring the disciplined-domain wp simplification ASN-0126 had to abandon as layer-scoped (DR, Standard registrations).

## The registration record

ASN-0126's registry stores, per coverage-class key, the type's shape and nothing else; its dynamics never write the registry after `Σ_init` (P1, RegistryInvariance). This note extends the *value* of each entry from `shape` to the record

`(shape, idem, behaviors)`

where `idem ∈ {⊤, ⊥}` and `behaviors` is a finite set drawn from the catalog below. The keys — coverage classes, unique under `~` — are unchanged.

**R-C0 (RecordWellFormedness).** A registration record is well-formed when `shape ∈ {Unary, Binary, Multi}`, `idem ∈ {⊤, ⊥}`, and every attached behavior is compatible with the rest of the record: read-filter (B1) requires Unary; transitive-closure (B2) and typed-reverse-lookup (B3) require Binary; age-staleness (B4) requires Multi with `idem = ⊥`. `Σ_init.registry` is well-formed entry-wise, on top of ASN-0126's C0 (finiteness, key uniqueness, representatives in `T_admissible`).

**R-VAL (ConstructionValidation).** Both well-formedness conditions are decidable at `Σ_init` construction, and construction is where the substrate checks them — the registry's only write point (ASN-0126, The registry). C0's key uniqueness is pairwise `CoverageEqualityDecidable` (ASN-0086) over the finitely many stored representatives — `O(|registry|²)` decidable tests, each on the representative endsets directly; membership of each representative in `T_admissible` is non-emptiness of a finite span set; and R-C0's clauses are finite case checks per entry (shape and idem against their enumerations, each attached behavior against the compatibility table). A declaration set failing any test yields no `Σ_init`: there is no partially-registered substrate, and no runtime path ever re-validates.

**R1 (ExtendedRegistryInvariance).** The extended record is constant at every `→_sh*`-reachable state (Definition Reachability, ASN-0126). ASN-0126's P1 argument is frame-based — every step kind carries `Σ'.registry = Σ.registry` in its frame and no step has the registry in its effect — and reads no part of the stored value, so it lifts to the extended value verbatim.

**R2 (IdemStability).** For any registered K, `idem(K)` takes the same value at every reachable state — immediate from R1, exactly as ASN-0126's P2 (ShapeStability) follows for the shape component.

The gate is untouched by the extension: `Sh-conf` reads only the shape component (ASN-0126, Shape-conformance), so every ASN-0126 claim — the gate, P3–P6, the projection bridge, gate realizability — holds over extended-record states without modification. The idem flag and the behavior set are read by the *operations and predicates of this note*, never by the gate.

## Idem operational semantics

ASN-0126 leaves what `idem(K)` does — and even what "the same tuple" means — to this note (its Open Question 1). The registration record carries the flag (above); here is its semantics.

**I0 (SamenessIsCoverageEquality).** Two emitted pairs `(F, G)` and `(F', G')` are *the same* for de-duplication iff `coverage(F) = coverage(F')` and `coverage(G) = coverage(G')` — `coverage` over endsets `Endset = 𝒫_fin(Span)` as ASN-0043 defines it — each equality decidable by CoverageEqualityDecidable (ASN-0086). Span-set equality is deliberately *not* the criterion. ASN-0126's central observation is that span count and coverage diverge — one contiguous extent presented as two abutting spans is a different span set with identical coverage — and every observer the substrate provides reads coverage, never decomposition: `Observe` matches from-patterns against `coverage(F)`, the `nullified`/active-subset machinery reads `coverage(G')`, and type identity itself is coverage-keyed (TypeEquivalence). Coverage-equal duplicates would be indistinguishable to every query yet doubly present; collapsing exactly them is what `idem = ⊤` is for. The gate and idem thus measure different things on principle: the gate measures *form* (span count, well-formedness), idem measures *content* (coverage, what the tuple asserts).

**I1 (IdemDedupSemantics).** Under `idem(K) = ⊤`, an emit of `(F, G, K)` is checked against the active subset `A_K^Σ` (ASN-0086): if some `(a, F', G') ∈ A_K^Σ` is the same as `(F, G)` in the sense of I0, the emit returns the existing address `a` and produces no new tuple. The check consults only the `(F, G, K)` values — proposer, emission time, source app are not part of the identity. Its rules are state-independent (they read the input values and the registry, invariant by R1); its *result* depends on the active subset, which varies across states. By R2, the same rules apply to every K-emit at every reachable state.

**I2 (AuditSliceNotConsulted).** The de-duplication test reads `A_K^Σ`, not the audit slice `L_K^Σ`. A tuple emitted and later nullified is in `L_K^Σ` but not in `A_K^Σ`; a subsequent `Emit_K` with the same `(F, G)` is **not** a no-op — it attempts a fresh tuple at a new address. The audit trail records both the original (now nullified) and the new emissions; resurrection-after-nullification is the design intent, not a side effect. One caveat bounds it: the fresh address is the frontier slot of the home's link chain (FrontierUnification, ASN-0126; every `K.λ_sh` deposit lands at the frontier and advances it by one — frontier-landing), and if a prior range-G retraction's coverage includes that slot, the resurrection emit is itself born nullified — irreversibly, by Corollary RangeSterilization (ASN-0126). Resurrection is guaranteed only where the home chain's next slots are unsterilized; the standard retraction registration (Standard registrations) is what keeps substrate-mediated retraction from sterilizing slots in the first place.

**I3 (BornNullifiedTransparency).** ASN-0126's wp analysis (Weakest precondition of the shape-gated emit) separates the gate from the landing: a gate-clearing emit deposits into the audit slice `L_K^{Σ'}`, but lands in the active subset `A_K^{Σ'}` only if two further conjuncts hold — C2 (the emit is not a self-nullifying retraction) and C3 (no pre-existing retraction tuple's coverage includes the fresh address). Under either failure the tuple is *born nullified*: in `L_K^{Σ'}`, absent from `A_K^{Σ'}`. By I2, a later `idem = ⊤` emit with the same `(F, G)` does not see a born-nullified tuple in its dedup check; it consults only the active subset, which is empty for that pair.

**I4 (ConcurrentEmitFirstCommit).** Two writers emitting tuples with same `(F, G, K)` against the same Σ race *ahead of* the substrate relation: `→_sh` is a sequential, interleaved step relation (it inherits ASN-0086's model — concurrency has no semantics inside it), so a serializing authority orders the two calls before either becomes a step. The emission address is pinned per home to the chain frontier (FrontierUnification, ASN-0126), so allocation is first-to-commit. For `idem = ⊤`, the winner produces the active tuple at the fresh address; the loser's emit, evaluated against the winner's post-state, finds the now-active tuple by I1 and returns its address. For `idem = ⊥`, both emissions produce distinct addresses; both appear in `A_K^Σ`.

**I5 (IdemFalseAlwaysFresh).** Under `idem(K) = ⊥`, no de-duplication test runs. Every `K.λ_sh` emit produces a fresh address regardless of `(F, G)` content, and the new tuple appears in `A_K^Σ` (modulo I3's born-nullified cases).

## Behaviors

A behavior is substrate-provided machinery an app optionally attaches at registration, as the `behaviors` component of the registration record; attaching one unlocks additional predicates. Behaviors compose; an app may attach any subset compatible with the registered shape and idem flag (R-C0).

### B1 (read-filter)

**Applies to:** Unary
**Effect:** Addresses carrying an active tuple of this type are excluded from substrate default queries on every other registered type.
**Provides:** `is_filtered(addr) → Bool` — true iff some `(a, F, ∅) ∈ A_K^Σ` has `addr ∈ coverage(F)`. Implicit exclusion of `addr` from `members(K')` and from any `targets_of(F')` result that would include `addr`, for every registered type `K' ≠ K`, unless the caller requests the audit view explicitly.

Adopted by lifecycle markers that should "vanish" from active queries; the substrate-shipped `retired` is the canonical case.

### B2 (transitive-closure)

**Applies to:** Binary
**Effect:** Substrate treats the relation as transitive and exposes chain-walking predicates over the active subset.
**Provides:** `tip(addr) → addr` (forward-walk to the maximal element of the chain rooted at addr; returns addr itself when no outgoing active tuple exists), `chain(addr) → ordered list of addrs`, `is_in_chain(addr, target) → Bool`.

Chain-walking reads `A_K^Σ`, never the audit slice: a nullified mid-chain tuple breaks the chain at that point, and `tip` resolves to the last element reachable through active tuples. Whether an audit-view chain walk is also needed is left open (Open question 6).

Adopted by chained-replacement relations; the substrate-shipped `supersedes` is the canonical case.

### B3 (typed-reverse-lookup)

**Applies to:** Binary
**Effect:** Substrate exposes reverse lookup and a type-keyed forward variant.
**Provides:** `sources_to(target) → set of addrs` (all F such that some `(a, F, G) ∈ A_K^Σ` has `target ∈ coverage(G)`), `target_of(source, K) → addr | ⊥` (typed forward lookup; returns the G-address when exactly one active K-tuple carries that F, ⊥ when none or several — Binary fixes each *tuple's* `|G| = 1`, not the number of active tuples per source, so functionality in F is an app convention, not a shape guarantee), `targets_keyed(source) → map K → addr` (joining `target_of` across every Binary type K registered with B3).

Adopted by relations where target-side queryability matters operationally — attached auxiliaries, named pointers.

### B4 (age-staleness)

**Applies to:** Multi with idem=⊥
**Effect:** Substrate provides age-aware queries and batch-retract tooling, using the emission ordering of `Emit_K` as the time reference.
**Provides:** `stale(threshold_seconds) → set of event-addrs`, `retract_stale(threshold_seconds)` (batch operation issuing one `Nullify_Binary` per stale event), `age(event_addr) → seconds`.

Adopted by time-bounded leases or short-lived assertions.

## Default predicates

Every registered type K, regardless of attached behaviors, exposes three source-side predicates derived from ASN-0086's `Observe_K`.

**D1 (Members).** `members(K) → set of addrs` — the F-coverage of every active K-tuple, unioned over `A_K^Σ`. Formally `members(K) = ⋃ { coverage(F) : (a, F, G) ∈ A_K^Σ }`. For Unary this is the set of marked addresses; for Binary and Multi it is the set of K-sources.

**D2 (IsK).** `is_K(addr) → Bool` — true iff `addr ∈ members(K)`, equivalently iff some `(a, F, G) ∈ A_K^Σ` has `addr ∈ coverage(F)`. Uniform across shapes: it asks whether `addr` is the source of an active K-tuple.

**D3 (TargetsOf).** `targets_of(F) → set of addrs` — the union of G-coverages across all active K-tuples with that F (the same for Binary and Multi: Binary bounds each tuple's `|G|`, not the number of active tuples sharing a source). For Unary, ∅ always.

**D4 (ReverseAccessIsBehavioral).** Target-side queries — "which F-addresses point at a given target" — are not in the default set. They require the B3 (typed-reverse-lookup) behavior, which provides `sources_to(target)`. The default trio reads only forward: source membership and source-to-target projection. Reverse access is a behavior-conditional capability, deliberately opt-in: a type that does not need reverse access carries no substrate commitment to its existence.

D1–D3 are well-defined on every reachable state by ASN-0086's active-subset definition and R1 ensuring K's registration record is consulted identically at every state.

## Standard registrations

ASN-0126 leaves open whether each substrate's `Σ_init.registry` is composed entirely of app-declared entries (its Open Question 4). This note answers: three coverage classes ship in `Σ_init.registry` for every substrate, supplied as part of substrate initialization rather than app registration. Every other type is app-registered; the substrate ships only the lifecycle, supersession, and retraction universals.

**S1 (Retired).** `retired` — Unary, idem=⊤, behaviors={B1}. Marks an address as no longer active; default queries on every other type exclude it.

**S2 (Supersedes).** `supersedes` — Binary, idem=⊤, behaviors={B2}. Records that one address supersedes another; `tip()` resolves to the current head of the supersession chain rooted at the queried address. The supersession link is the canonical whole-document metalink of Nelson's design (the pattern ASN-0126's attribution analysis grounds in LM 4/52–4/53).

**S3 (Retraction).** `R` — Binary, idem=⊤, behaviors=∅. The retraction relation; ASN-0126 (Retraction as an attributed Binary) establishes the Binary registration and specifies the live retraction operation as a full contract: the unit-depth wrapper `Nullify_Binary(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, {r}, {(a, δ(1, #a))})` with canonical from-fill `r = (d_retr, δ(1, #d_retr))`, preconditions P0 (`d_retr ∈ dom(Σ.M)`) and P-reg ([R] registered Binary), and postconditions: unconditional coverage nullification, target-nullification iff residence, single-tuple scope iff P-tgt, and persistence (via B2/B3 transfer of R6a/R6c). Where ASN-0126 frames R as app-registered, this note ships it — with R in `Σ_init.registry`, retraction is uniformly available without per-app declaration, and the contract's P-reg precondition is discharged globally, on every substrate. Binary is a *choice* among the four [R] configurations ASN-0126 sweeps: unregistered [R] gives an audit-only substrate where no `Emit_R` has a `→_sh` image, and Unary [R] forces `G = ∅`, emptying every retraction's to-coverage — retraction-inert. Shipping Binary selects the one configuration where retraction is expressible, accepting that the wp's C2/C3 conjuncts are live (ASN-0126, Weakest precondition).

The shipped registration carries an operation-surface policy that settles ASN-0126's Open Question 7. ASN-0126's contract deliberately puts **no** precondition on the target — P-tgt "is not assumed, it conditions the postconditions": single-tuple scope holds *iff* P-tgt held at the pre-state, and the gate, being static, cannot check the residence disjunct. The operational layer is not so constrained: operations already read state (I1's dedup reads `A_K^Σ`). This note therefore exposes `Nullify_Binary` as the **only** retraction entry point — no direct `Emit_K` with `K ~ R` is in the operation set — and *promotes P-tgt from postcondition hypothesis to enforced precondition*: `a ∈ A_rel^Σ` or `a = a_emit(Σ, d_retr)`. The wrapper's unit-depth to-span closes ASN-0126's first gap by construction; the P-tgt precondition closes the second; together they convert the contract's iff-P-tgt clauses into unconditional guarantees of the operation surface and make sterilization (Corollary RangeSterilization) unreachable through substrate-mediated retraction. (Since `nullified` reads only `L_R` — the one coverage class R occupies — no app-registered type can sterilize either: containment is complete.)

The policy buys back what ASN-0126's gated layer lost. Call a substrate *surface-disciplined* when every tuple in `L_R^Σ` was deposited through this operation set — i.e., every retraction is wrapper-routed with a P-tgt-valid target.

**DR (DisciplineRestoration).** *On a surface-disciplined substrate, wp conjunct C3 holds at every gate-clearing emit, so a tuple is born nullified only through C2's self-nullification; and the weakest precondition of `Nullify_Binary` at this surface is `P0 ∧ P-reg ∧ P-tgt`.* Every R-tuple's to-coverage is a subtree `{t : a ≼ t}` at a P-tgt-valid `a` — an existing link address or the deposit's own. A later emit's fresh address is its home chain's frontier slot (FrontierUnification, ASN-0126), and link addresses form a prefix-antichain at every reachable state (R0a, FlatLinkDomain, ASN-0086, via the bridge), so no later link address lies strictly under `a`; nor can it equal `a` (key freshness). Hence no policy-emitted retraction's coverage ever contains a later fresh address — C3's existential is empty, and ASN-0126's disciplined-domain wp simplification, abandoned at the substrate layer as layer-scoped (its projection-bridge exclusion), is restored one layer up as a guarantee of this operation surface. For `Nullify_Binary` itself, once `P0 ∧ P-reg ∧ P-tgt` admits the call, every postcondition of ASN-0126's contract holds unconditionally — completing the wp Case-1 parallelism ASN-0126's review trail left open. The quantifier is real: a substrate whose `L_R` contains pre-policy or bypass-emitted range-G tuples is outside DR's scope, and there I2's sterilization caveat is the operative bound.

No behavior is attached to R: retraction's effect on `A_K^Σ` is built into ASN-0086's active-subset semantics rather than surfaced as a derived predicate. Two consequences of the wrapper's from-fill are worth naming. First, attribution is observable without B3: `Observe_R` matches the from-fill at whole-document granularity — ASN-0126 scopes this match to *wrapper-routed* retractions (a gated `Emit_R` whose one from-span lies elsewhere escapes the under-`d_retr` pattern), and under this note's wrapper-only surface that qualifier saturates: every retraction is wrapper-routed, so the convention — F answers *who retracts*, G carries *what is retracted* — holds totally. Second, idem identity degenerates in F: the from-fill is per-document, so by I0 two retractions are the same iff they share the retracting document and a coverage-equal target — re-retracting the same target from the same document dedups to the existing tuple, which is the desired idempotence of retraction.

**The operation set.** With S3's policy in place, the operation surface an app invokes is ASN-0126's refined set `{Emit_K, Observe_K, Nullify_Binary}` — gated emit for non-R types, pure reads, and the wrapped retraction — with this note's idem semantics layered on `Emit_K` and the behavior/default predicates layered on `Observe_K`.

## An abstract registry example

The example below uses generic type names — `marker`, `aux`, `fanout`, `event` — to illustrate behaviors against shapes the substrate-shipped registrations don't exhaust. These names are not standard registrations and not predictions of what specific apps will register; they exist only to exhibit the framework's mechanics.

Consider a registry composed of the three substrate-shipped entries plus four illustrative app entries, each a full registration record `(shape, idem, behaviors)`:

| Name | Shape | idem | Behaviors | Source |
|------|-------|------|-----------|--------|
| `retired` | Unary | ⊤ | read-filter | substrate |
| `supersedes` | Binary | ⊤ | transitive-closure | substrate |
| `R` | Binary | ⊤ | — | substrate |
| `marker` | Unary | ⊤ | — | illustrative |
| `aux` | Binary | ⊤ | typed-reverse-lookup | illustrative |
| `fanout` | Multi | ⊤ | — | illustrative |
| `event` | Multi | ⊥ | age-staleness | illustrative |

The four illustrative entries cover the shape-and-behavior cells the substrate-shipped three leave unexhausted: Unary without read-filter (`marker`), Binary with typed-reverse-lookup (`aux`), Multi with idem=⊤ (`fanout`), and Multi with idem=⊥ + age-staleness (`event`).

**Emit under idem=⊤ Multi.** An emit of `fanout` with `F = a_src`, `G = [a_t1, a_t2, a_t3]` runs the gate: K registered (✓), Sh-conf with |F|=1 (✓), `K.λ_sh` admits. The active-subset check finds no existing coverage-equal tuple, so the emit produces a fresh address. A repeat emit with the same `(F, G)` — including a re-decomposed G whose spans differ but whose coverage is equal (I0) — finds the now-active tuple and returns its address (no new tuple).

**Emit under idem=⊥ Multi with age-staleness.** An emit of `event` with `F = a_actor`, `G = [a_obj]` produces a fresh address regardless of any existing event. The age-staleness behavior records the emission timestamp; `age(event_addr)` returns elapsed seconds. A later `retract_stale(600)` issues one `Nullify_Binary` per active event older than 10 minutes, in batch — each unit-depth and P-tgt-valid (the target is an existing link address), so the batch cannot sterilize.

**Read-filter on Unary lifecycle.** Emit `marker` on `a_x`, then emit `retired` on the same `a_x`. `is_retired(a_x)` returns true; `members(marker)` excludes `a_x` from its default output (read-filter excludes), unless the caller requests the audit view explicitly. The original `marker` tuple is still in `L_K^Σ`; only its visibility in default queries is filtered.

**Typed-reverse-lookup on Binary.** Emit `aux` with `F = a_p`, `G = [a_aux1]`. `target_of(a_p, aux)` returns `a_aux1`. A separate emit of a different Binary type (say a hypothetical second `aux2`) at `F = a_p` with `G = [a_aux2]` gives `target_of(a_p, aux2) = a_aux2`, and `targets_keyed(a_p)` returns `{aux: a_aux1, aux2: a_aux2}`.

**Born-nullified case (I3).** Suppose a pre-existing active R-tuple has to-endset covering some address `a*` that `K.λ_sh` is about to allocate as the fresh address of a `fanout` emit with `F = a_src`. The gate admits (the emit is shape-conformant under `fanout`'s Multi registration), and the new tuple is deposited at `a*` in `L_{fanout}^{Σ'}`. By ASN-0086's active-subset semantics, `a*` is covered by an active retraction, so the new tuple is not in `A_{fanout}^{Σ'}` — it is born nullified (the C3 failure of I3). The tuple contributes nothing to any default predicate query on `fanout`: it does not enlarge `members(fanout)`, does not surface in `targets_of`, and a later idem=⊤ emit with the same `(F, G)` will not see it (per I2). Note such a covering R-tuple cannot arise through `Nullify_Binary` (DR, Standard registrations); the case is reachable only on a substrate that is not surface-disciplined — pre-policy history or a bypassed operation surface — and the gate-level question this leaves is Open question 3.

## What this note doesn't cover

- **Predicate composition.** Composition rules over the atomic default predicates and the behavior-unlocked predicates — the territory ASN-0095 occupied before retirement. A separate successor (ASN-0126 Open Question 5).
- **Behavior-behavior interaction edge cases.** When two behaviors attach to the same type (e.g., transitive-closure and typed-reverse-lookup on the same Binary), their interaction is mostly orthogonal but the predicate set's closure under composition is deferred to the predicate-composition successor.
- **Extensions beyond F=1 and N=3.** Multi-span sources and richer arity are ASN-0126 Open Question 6's territory — a supplemental note loosening the constraints, or a parallel framework; this note inherits the F=1, N=3 envelope unchanged.
- **Cascade-with and single-source-restriction.** Two behaviors considered but not exercised by any registration this note commits on. Deferred until a forcing function appears.

## Open questions

1. **B1 × B3 interaction on filtered targets.** When an address carries an active `read-filter` (B1) tuple and is also a target of some Binary type with `typed-reverse-lookup` (B3), what does `sources_to(filtered_addr)` return — the empty set (B1 dominates) or the actual sources (B3 dominates)? Either choice is defensible; this note doesn't settle it.

2. **Cross-type composite queries.** When a query spans types with different idem values (e.g., counting active tuples of one idem=⊤ Multi type *and* one idem=⊥ Multi type matching some predicate), what does the composite count commit on — set-semantics on each type's active subset and sum the cardinalities? The bag-vs-set question splits cleanly per type, but composite queries inherit both.

3. **Gate-level reinforcement of sterilization containment.** S3 contains sterilization at the operation surface (`Nullify_Binary`-only, P-tgt preconditioned). Should the gate also be refined — making non-unit G non-conformant for R specifically — as defense in depth, at the cost of a type-sensitive gate clause ASN-0126 deliberately avoided? Relatedly, what are the error semantics when this note's P-tgt precondition fails — rejected call, or fall back to ASN-0126's contract behavior (the call is admitted; coverage nullification still holds unconditionally; single-tuple scope is forfeited per its iff-P-tgt clause)?

4. **Attribution of substrate-shipped types.** The three standard registrations (`retired`, `supersedes`, `R`) ship in `Σ_init.registry` without an "originating app." Whether `provenance.import` (or similar) should be emitted for them at Σ_init to give them an explicit provenance, or whether substrate-shipped types are inherently un-attributable, is unspecified.

5. **Behavior catalog growth.** Candidates considered but excluded from the four: conflict-detection (idem=⊤ violation surfacing), materialization (view caching as a substrate concern), behavior versioning (when a behavior's semantics evolve). Each could ship in a supplemental note when a forcing use case appears.

6. **Audit-view chain walking.** B2's chain predicates read the active subset, so a nullified mid-chain tuple breaks the chain. Whether an audit-view variant of `chain()`/`tip()` — walking `L_K^Σ` to recover historical chains — is a substrate obligation or an app-side reconstruction is left open.

7. **Registry evolution.** Registration remains construction-time-only: an app that needs a new type after `Σ_init` has no path here, and P1/R1 are built on that immutability. Migration to a successor registry, substrate rebuild, or a versioned-registry relaxation of P1 (per-epoch stability) are all coherent directions; each is new machinery this note deliberately does not open.

8. **Multi-app registry composition.** This note's `Σ_init.registry` is the three substrate-shipped entries plus app declarations, but nothing governs how *several* apps sharing one substrate merge their declarations into the single registry — or what resolves a coverage-class collision, between two apps or between an app and a substrate-shipped key. C0's key uniqueness states the constraint; the construction protocol that achieves it is unspecified.

9. **Retraction-attribution query semantics.** With every retraction wrapper-routed, the from-fill makes "all retractions by document `d`" expressible as an `Observe_R` from-pattern (S3). What query language this supports — pattern algebra over retraction attributions, composition with the default predicates, interaction with B1 filtering of the retracting document itself — is unaddressed; S3 fixes the convention, not the queries over it.
