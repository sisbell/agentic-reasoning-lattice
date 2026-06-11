# ASN-0128 Claim Statements

*Source: ASN-0128-substrate-type-operational-semantics.md (revised unknown) — Extracted: 2026-06-10*

## R-C0 — RecordWellFormedness (INV, predicate)

A registration record is well-formed when `shape ∈ {Unary, Binary, Multi}`, `idem ∈ {⊤, ⊥}`, and every attached behavior is compatible with the rest of the record: read-filter (BH1) requires Unary; determinate-walk (BH2) and typed-reverse-lookup (BH3) require Binary; age-staleness (BH4) requires `idem = ⊥`, with no shape clause. R-C0 is enforced by failing construction (R-VAL).

Compatibility table:
- BH1: shape = Unary
- BH2: shape = Binary
- BH3: shape = Binary
- BH4: idem = ⊥ (no shape clause)

`Σ_init.registry` is well-formed entry-wise, on top of ASN-0126's C0 (finiteness, key uniqueness, representatives in `T_admissible`).

---

## R-VAL — ConstructionValidation (LEMMA, lemma)

Both well-formedness conditions are decidable at `Σ_init` construction, and construction is where the substrate checks them — the registry's only write point.

- C0's key uniqueness: pairwise `CoverageEqualityDecidable` (ASN-0086) over the finitely many stored representatives — `O(|registry|²)` decidable tests, each on the representative endsets directly
- Membership of each representative in `T_admissible`: non-emptiness of a finite span set
- R-C0's clauses: finite case checks per entry (shape and idem against their enumerations, each attached behavior against the compatibility table)
- Standard-registration designation adds three pairwise non-equivalence tests over the shipped representatives (R-C1)

A declaration set failing any test yields no `Σ_init`: there is no partially-registered substrate, and no runtime path ever re-validates.

`Σ_init` is the validated extended-record registry adjoined to ASN-0086's three initial components: `Σ_init.C`, `Σ_init.M`, `Σ_init.L` are `Σ_init^{0086}`'s components verbatim, so in particular `Σ_init.L = ∅`.

---

## R1 — ExtendedRegistryInvariance (INV, predicate)

The extended record is constant at every `→_sh*`-reachable state (Definition Reachability, ASN-0126).

ASN-0126's P1 argument is frame-based — every step kind carries `Σ'.registry = Σ.registry` in its frame and no step has the registry in its effect — and reads no part of the stored value, so it lifts to the extended value verbatim.

---

## R2 — IdemStability (LEMMA, lemma)

For any registered K, `idem(K)` takes the same value at every reachable state — immediate from R1, exactly as ASN-0126's P2 (ShapeStability) follows for the shape component.

---

## RP — RecordProjection (LEMMA, lemma)

Let `ρ` act on states by keeping C, M, L and every registry key, and projecting each registry value `(shape, idem, behaviors) ↦ shape`. Then:

(i) `ρ(Σ_init)` is a well-formed ASN-0126 initial state — its C, M, L are ASN-0086's initial components by `Σ_init`'s construction (R-VAL); C0's clauses (finiteness, key uniqueness, representatives in `T_admissible`) are key-side and untouched; and every projected value is a bare shape.

(ii) Each `→_sh` step over extended-record states maps under `ρ` to an ASN-0126 `→_sh` step: the gate's verdict agrees, because `Sh-conf` reads `(F, G)` and the shape component, which `ρ` preserves; the C/M/L effects are identical; and each step kind's registry frame `Σ'.registry = Σ.registry` projects to the same frame.

(iii) By induction on derivation length, every reachable extended-record state `Σ` has `ρ(Σ)` ASN-0126-reachable.

---

## RP-a — SingleStateTransfer (LEMMA, lemma)

An ASN-0126 claim whose conclusion is a predicate of one reachable state, reading only C, M, L, registration status (key-side, `ρ`-preserved), and shapes — the gate's verdicts, P4, P6, FrontierUnification, the projection bridge onto ASN-0086 (compose `π` after `ρ`), and the per-state ASN-0086 results ASN-0126's own B2 carries (R0a among them) — holds at every reachable extended-record state Σ by evaluation at `ρ(Σ)`, ASN-0126-reachable by (iii) and sharing the read components.

---

## RP-b — PathTransfer (LEMMA, lemma)

A claim whose conclusion constrains steps or successors transfers by derivation projection. By (ii) and induction, an extended-record derivation `Σ →_sh* Θ` projects to an ASN-0126 derivation `ρ(Σ) →_sh* ρ(Θ)`; single-state hypotheses hold at `ρ(Σ)` by sharing; the ASN-0126 claim applied there constrains `ρ(Θ)`; and the per-successor conclusion, again over shared components, pulls back to Θ.

RangeSterilization and the persistence lemmas R6a/R6c transfer this way; transition invariants (P3 as a step property, L12/L12a) likewise transfer across each genuine extended-record step.

---

## RP-c — StepLift (LEMMA, lemma)

An ASN-0126 claim asserting the existence of a `→_sh` step lifts to the extended-record system when the step's preconditions read only `ρ`-preserved data: the preconditions hold at Σ iff at `ρ(Σ)`, the C/M/L effects are determined identically, and every step kind frames the registry — the asserted step is an extended-record step verbatim.

P5 (GateRealizability) is the canonical instance; the wrapper's miss-branch deposit is admitted at extended-record states by the same lift.

---

## Definition — AddressDenotation (AD)

A span is *address-denoting* iff it is unit-depth, `(x, δ(1, #x))`, and it *denotes* its start `x`.

An endset `e` is address-denoting iff every span in it is, and its denoted set is:

`addrs(e) = {x : (x, δ(1, #x)) ∈ e}`

— finite, since endsets are finite span sets (`Endset = 𝒫_fin(Span)`, ASN-0043), and read off the spans by inspection.

Two result regimes:
- *Membership predicates* (`is_K`, `is_filtered`): take an address argument and test coverage — `addr ∈ coverage(F)` — total over all tuples, address-denoting or not.
- *Enumeration predicates* (`members`, `targets_of`, `sources_to`, `succs`, `tip`, `chain`, `target_of`, `targets_keyed`): return denoted addresses, assembled from `addrs(·)` of the relevant endsets.

`is_in_chain` is Boolean-valued but enumeration-derived: it tests membership in `chain`'s result list — exact denoted vertices, never coverage.

For the minimal/coverage equivalence: for an address-denoting endset `e`, the ≼-minimal elements of `coverage(e)` are exactly the ≼-minimal elements of `addrs(e)`.

---

## Definition — ArgumentMatching (AM)

Arguments naming a **source vertex** — `targets_of(x)`, `succs(x)`, `chain(addr)`, `tip(addr)`, `is_in_chain(addr, ·)`, `target_of(source, K)`, `targets_keyed(source)` — are matched by *exact denotation*: the tuples consulted are those whose F denotes the argument, `x ∈ addrs(F)`.

The one reverse lookup whose argument names an **asserted-about address** — `sources_to(target)` — is matched by *coverage*: `target ∈ coverage(G)`.

(`members` takes no address argument; BH4's `age` and `stale` take exact chain addresses and match no endset.)

---

## I0 — SamenessIsCoverageEquality (DEF, definition)

Two emitted pairs `(F, G)` and `(F', G')` are *the same* for de-duplication iff `coverage(F) = coverage(F')` and `coverage(G) = coverage(G')` — `coverage` over endsets `Endset = 𝒫_fin(Span)` as ASN-0043 defines it — each equality decidable by CoverageEqualityDecidable (ASN-0086).

Span-set equality is deliberately *not* the criterion.

For the information bound: for an address-denoting endset `e`, the ≼-minimal elements of `coverage(e)` are exactly the ≼-minimal elements of `addrs(e)`:
- (⊆) Let `t` be ≼-minimal in the coverage. The coverage is the union of the denoted subtrees (PrefixSpanCoverage), so `r ≼ t` for some denoted `r`; `r` itself lies in the coverage (reflexivity of ≼), so `t`'s minimality forces `t = r` — `t` is denoted — and `t` is minimal among denoted addresses, since a denoted `r' ≺ t` would lie in the coverage and contradict `t`'s minimality there.
- (⊇) Let `r` be ≼-minimal among denoted addresses. Then `r` lies in the coverage (reflexivity), and is minimal there: a coverage element `t ≺ r` would lie in some denoted `r''`'s subtree, giving a denoted `r'' ≼ t ≺ r` and contradicting `r`'s minimality among denoted addresses.

---

## I1 — IdemDedupSemantics (DEF, definition)

Under `idem(K) = ⊤`, the de-duplication check belongs to the *surface operation* `Emit_K(Σ, d, F, G)` and to it alone; the transition relation `→_sh` is ASN-0126's, unchanged. The contract has four clauses:

*Order — gate first.* The gate's preconditions (K registered, arity 3, `Sh-conf(K, F, G)`) are evaluated on the presented values before any dedup consultation; a gate-failing call is rejected — no step, no address — even when an I0-equal active tuple exists.

*Miss.* If no member of `A_K^Σ` is I0-equal to `(F, G)`, `Emit_K` invokes `K.λ_sh`, and ASN-0086's emit contract holds as inherited through the gate: a fresh `a = a_emit(Σ, d)`, `home(a) = d`, the deposit `(F, G, K)` at `a`, frame on C, M, and registry.

*Hit.* If some `(a', F', G') ∈ A_K^Σ` is I0-equal to `(F, G)`, `Emit_K` returns `a'` and **takes no step**: `Σ' = Σ`, nothing is deposited. The `d` argument is consulted only on a miss. On a surface-emitted history the matching tuple is unique (I1a); off that discipline several may match, and `Emit_K` returns the T1-least matching address.

*Home validation — branch-local.* On a miss — the only branch that reads `d` — the check is enforced by rejection: a miss with `d ∉ dom(Σ.M)` takes no step and returns no address. On a hit, `d` is not read at all.

---

## I1a — ActiveIdemUniqueness (LEMMA, lemma)

Call a state's K-history *surface-emitted* when every tuple in `L_K^Σ` was deposited through `Emit_K`.

For `idem(K) = ⊤` and surface-emitted K-history, the active subset holds at most one tuple per I0-class:

`(A (a, F, G), (a', F', G') ∈ A_K^Σ : coverage(F) = coverage(F') ∧ coverage(G) = coverage(G') : a = a')`

*Proof* by induction over the `→_sh*` derivation.
- Base: `L_K^{Σ_init} = ∅`, vacuous.
- Step: K.σ and K.α leave `Σ.L` unchanged. A `K.λ_sh` deposit of a non-K tuple leaves `L_K` unchanged and can only shrink `A_K`. A `K.λ_sh` deposit of a K-tuple is, by the surface-emitted hypothesis, the miss branch of an `Emit_K`: at the pre-state its I0-class had no active member, so at the post-state it has at most one.
- No tuple changes class post hoc — coverage is a pure function of the stored endsets, which are immutable (L12 via ASN-0126's B2 and RP-b). ∎

---

## I2 — AuditSliceNotConsulted (LEMMA, lemma)

The de-duplication test reads `A_K^Σ`, not the audit slice `L_K^Σ`. A tuple emitted and later nullified is in `L_K^Σ` but not in `A_K^Σ`; a subsequent `Emit_K` with the same `(F, G)` is **not** a no-op — it attempts a fresh tuple at a new address.

One caveat: the fresh address is the frontier slot of the home's link chain (FrontierUnification, ASN-0126), and if a prior range-G retraction's coverage includes that slot, the resurrection emit is itself born nullified — irreversibly, by Corollary RangeSterilization (ASN-0126; transferred to extended-record states by RP-b).

---

## I3 — BornNullifiedTransparency (LEMMA, lemma)

ASN-0126's wp analysis separates the gate from the landing: a gate-clearing emit deposits into the audit slice `L_K^{Σ'}`, but lands in the active subset `A_K^{Σ'}` only if two further conjuncts hold:
- C2: the emit is not a self-nullifying retraction
- C3: no pre-existing retraction tuple's coverage includes the fresh address

Under either failure the tuple is *born nullified*: in `L_K^{Σ'}`, absent from `A_K^{Σ'}`.

By I2, a later `idem = ⊤` emit with the same `(F, G)` does not see a born-nullified tuple in its dedup check; it consults only the active subset, which is empty for that pair.

---

## I4 — ConcurrentEmitFirstCommit (LEMMA, lemma)

Two writers emitting tuples with same `(F, G, K)` against the same Σ race *ahead of* the substrate relation: `→_sh` is a sequential, interleaved step relation, so a serializing authority orders the two calls before either becomes a step. The emission address is pinned per home to the chain frontier (FrontierUnification, ASN-0126), so allocation is first-to-commit.

For `idem(K) = ⊤`: the winner deposits at the fresh address, and provided the deposit lands active (I3's caveat), the loser's emit, evaluated against the winner's post-state, finds the now-active tuple by I1 and returns the winner's address. If the winner's deposit is born nullified, the loser's dedup check sees an empty class (I2, I3) and the loser deposits a second tuple at the next frontier slot — itself subject to I3.

For `idem(K) = ⊥`: both emissions produce distinct addresses, and both tuples appear in `A_K^{Σ₂}`, the second writer's post-state — again modulo I3's born-nullified cases.

---

## I5 — IdemFalseAlwaysFresh (LEMMA, lemma)

Under `idem(K) = ⊥`, no de-duplication test runs: every `Emit_K` call the gate admits invokes `K.λ_sh` and produces a fresh address regardless of `(F, G)` content, and the new tuple appears in `A_K^{Σ'}` (modulo I3's born-nullified cases).

---

## I6 — IdemEmitSurfaceContract (THEOREM, theorem)

The caller-facing postcondition for `Emit_K` under `idem(K) = ⊤`:

`POST(a★) ≡ (E F★, G★ :: (a★, F★, G★) ∈ A_K^{Σ'} ∧ coverage(F★) = coverage(F) ∧ coverage(G★) = coverage(G))`

*Preconditions — uniform.* K registered, arity 3, `Sh-conf(K, F, G)` — checked first on every call; a gate-failing call is rejected, no step, no address.

*Branch condition.* The admitted call is a *hit* iff some `(a', F', G') ∈ A_K^Σ` is I0-equal to the presented pair, a *miss* otherwise.

*Hit.* No step: `Σ' = Σ`; returned address `a★ = a'`, the T1-least match (unique on surface-emitted K-history, I1a). POST holds at `Σ' = Σ` from the incumbent itself. The branch reads no further input — `d` is not consulted — so it contributes no conjunct beyond the gate.

*Miss.* The branch reads `d` and rejects `d ∉ dom(Σ.M)`. An admitted miss takes the `K.λ_sh` step (RP-c): fresh `a★ = a_emit(Σ, d)`, deposit `(F, G, K)` at `a★`. POST at the post-state is then `(a★, F, G) ∈ A_K^{Σ'}`, which requires C2 and C3; under either failure the deposit is born nullified (I3) and POST fails.

*The wp, assembled:*

`wp(Emit_K under idem = ⊤, POST) ≡ gate ∧ (hit(Σ, F, G) ∨ (d ∈ dom(Σ.M) ∧ C2 ∧ C3))`

*Disciplined-domain reduction.* On a surface-disciplined substrate, C3 holds at every gate-clearing emit and `Emit_K` is invoked at `K ≁ R` only (C2's first disjunct holds outright):

`wp(Emit_K, POST) ≡ gate ∧ (hit(Σ, F, G) ∨ d ∈ dom(Σ.M))`

---

## Definition — Views

- the **audit view** of K at Σ is the audit slice `L_K^Σ` — every K-tuple ever deposited, nullified or not;
- the **active view** is the active subset `A_K^Σ` — deposited and not nullified;
- the **default view** is the active view after the read-filter rewrite (BH1): when some Unary type registered with BH1 has an active tuple whose F-coverage contains an address, that address is subtracted from the two enumeration surfaces BH1 names, on every other type. Absent any BH1 registration, default = active.

---

## Definition — BH1 (ReadFilter)

**Applies to:** Unary

**Effect:** Addresses carrying an active tuple of this type are excluded from the *default view* of enumeration queries on every other registered type.

**Provides:**
- `is_filtered(addr) → Bool` — true iff some `(a, F, ∅) ∈ A_K^Σ` has `addr ∈ coverage(F)`

**Rewrite scope.** BH1 rewrites exactly two enumeration surfaces, on every registered `K' ≠ K`:
- default view of `members(K')` is `{x ∈ members(K') : ¬is_filtered(x)}`
- default view of `targets_of(x)` likewise drops filtered denoted targets

Nothing else is rewritten: active-view equations D1–D3 keep their values, membership predicates are untouched, and raw `Observe_K` (both hist and oper selectors) never filters.

---

## Definition — BH2 (DeterminateWalk)

**Applies to:** Binary

**Effect:** Substrate exposes walk predicates over the active view's *denoted graph*: one edge `x → y` per active address-denoting K-tuple whose F denotes `x` and whose G denotes `y`.

**Provides:**
- `succs(x) → set of addrs` — the denoted targets of active K-tuples whose F denotes `x` (matched by denotation — AM): one step, no closure.
- `chain(addr) → ordered list of addrs` — the maximal *determinate* walk from `addr`: the longest sequence `addr = x₀, x₁, …, xₙ` with each `xᵢ₊₁` the unique successor (`succs(xᵢ) = {xᵢ₊₁}`) and all elements distinct. The walk stops at `xₙ` when:
  - `succs(xₙ) = ∅` (a sink)
  - `|succs(xₙ)| ≥ 2` (a branch)
  - the unique successor already occurs in the sequence (a cycle)
  
  The list prepends `addr` itself, which need not be a vertex. Termination: each extension appends a unique successor — a member of the vertex set `V`, which is finite — and `x₁, …, xₙ` are pairwise distinct, so after `n` extensions `t = |V| − n ≥ 0` is a natural-number bound decreasing by one per extension.
- `tip(addr) → addr | ⊥` — `xₙ` when `chain(addr)` stops at a sink (in particular `addr` itself when it has no outgoing edge); `⊥` when the walk stops at a branch or a cycle.
- `is_in_chain(addr, target) → Bool` — `target ∈ chain(addr)`: membership in the walk's result list — exact denoted vertices, enumeration-derived, not a coverage test.

Chain-walking reads the active view, never the audit slice.

---

## Definition — BH3 (TypedReverseLookup)

**Applies to:** Binary

**Provides:**
- `sources_to(target) → set of addrs` — `⋃ { addrs(F) : (a, F, G) ∈ A_K^Σ ∧ target ∈ coverage(G) }`; argument tested by coverage (AM); result is denoted addresses.
- `target_of(source, K) → addr | ⊥` — when exactly one active K-tuple's F denotes `source` *and* its G is address-denoting, the denoted target `y` (`addrs(G) = {y}`); ⊥ in every other case — none, several, or a unique tuple whose single G-span is non-unit-depth.
- `targets_keyed(source) → map K → addr` — joins `target_of` across every Binary type K registered with BH3; ⊥-valued types are omitted, so the map's keys are exactly those K where `target_of(source, K)` is address-valued.

---

## Definition — BH4 (AgeStaleness)

**Applies to:** any shape, with `idem = ⊥`

**Effect:** Substrate provides age-aware queries and batch-retract tooling. Time reference is *ordinal, not temporal*: age is measured by position in the event's home chain (`chain_d` and the frontier `f_d^Σ` — HomedChain and FrontierUnification, ASN-0126).

**Provides:** for an active event tuple at `a = chain_d(j)`, `d = home(a)`:
- `age(a) → ℕ` — `f_d^Σ − 1 − j`: how many deposits homed at `d` postdate the event. The chain interleaves every type homed at `d`, so age counts the home's subsequent link traffic, not K-events alone.
- `stale(h) → set of event-addrs` — `{a : (a, F, G) ∈ A_K^Σ ∧ age(a) > h}` for an ordinal horizon `h ∈ ℕ`; finite and computable (L-fin; age is arithmetic on chain indices).
- `retract_stale(d_retr, h)` — for a caller-supplied retracting document `d_retr`: one `Nullify_Binary(·, d_retr, a)` per `a ∈ stale(h)`, the stale set evaluated once at the batch's initial state, `d_retr` held constant across the batch.
  - P0: `d_retr ∈ dom(Σ.M)` evaluated once at initial state; on failure issues no constituent — an invalid `d_retr` voids the batch by construction.
  - The batch is a *sequence* of `→_sh` steps, not atomic.
  - P-tgt: each target is an existing link address, so the first disjunct holds throughout by domain monotonicity.

---

## D1 — Members (DEF, definition)

`members(K) → set of addrs` — the denoted F-addresses of the active K-tuples:

`members(K) = ⋃ { addrs(F) : (a, F, G) ∈ A_K^Σ }`

For Unary this is the set of marked addresses; for Binary and Multi it is the set of K-sources. Finite and computable: L-fin bounds the tuples, and each `addrs(F)` is read off finitely many spans (AD).

---

## D2 — IsK (DEF, definition)

`is_K(addr) → Bool` — true iff some `(a, F, G) ∈ A_K^Σ` has `addr ∈ coverage(F)`: the membership regime, total and decidable (AD).

Over address-denoting tuples:

`is_K(addr) ⟺ (E x : x ∈ members(K) : x ≼ addr)`

— `is_K` holds at the denoted sources and all their extensions, while `members` enumerates the sources themselves.

---

## D3 — TargetsOf (DEF, definition)

`targets_of(x) → set of addrs` — for a source address `x`, the denoted targets across the active K-tuples whose F denotes `x`:

`targets_of(x) = ⋃ { addrs(G) : (a, F, G) ∈ A_K^Σ ∧ x ∈ addrs(F) }`

For Unary, ∅ always. The argument is matched by denotation — `x ∈ addrs(F)`, per AM.

The assertion-level forward query (derived composition):

`targets_under(addr) = ⋃ { targets_of(x) : x ∈ members(K) ∧ x ≼ addr }`

Over address-denoting tuples this equals the coverage-keyed alternative `⋃ { addrs(G) : (a, F, G) ∈ A_K^Σ ∧ addr ∈ coverage(F) }`, since `addr ∈ coverage(F) ⟺ (E x : x ∈ addrs(F) : x ≼ addr)` (PrefixSpanCoverage).

---

## D4 — ReverseAccessIsBehavioral (INV, predicate)

Target-side queries — "which sources point at a given target" — are not in the default set. They require the BH3 (typed-reverse-lookup) behavior, which provides `sources_to(target)`. The default trio reads only forward: source membership and source-to-target projection.

---

## R-C1 — DesignationNonCollision (INV, predicate)

The three designated classes are pairwise non-`~`-equivalent:

`[K_ret] ≠ [K_sup]`, `[K_sup] ≠ [K_R]`, `[K_R] ≠ [K_ret]`

This is a construction check alongside R-VAL's others — three more `CoverageEqualityDecidable` tests, each required to come out *unequal* — a colliding designation would violate C0's key uniqueness, and no `Σ_init` could be constructed.

---

## S1 — Retired (DEF, definition)

`retired` (the designated class `[K_ret]`) — Unary, idem=⊤, behaviors={BH1}.

Marks an address as lifecycle-retired: the default view on every other type excludes it (BH1's rewrite scope); active subsets are untouched — nothing is nullified.

---

## S2 — Supersedes (DEF, definition)

`supersedes` (the designated class `[K_sup]`) — Binary, idem=⊤, behaviors={BH2}.

Records that one address supersedes another; `tip()` resolves to the current head when the active supersession edges from the queried address form a determinate, acyclic walk, and to ⊥ at a branch or a cycle (BH2's verdicts).

---

## S3 — Retraction (DEF, definition)

`R` (the designated class `[K_R]`, ASN-0086's RetractionType) — Binary, idem=⊤, behaviors=∅.

ASN-0126 (Retraction as an attributed Binary) establishes the Binary registration and specifies the live retraction operation:

`Nullify_Binary(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, {r}, {(a, δ(1, #a))})`

with canonical from-fill `r = (d_retr, δ(1, #d_retr))`, preconditions P0 (`d_retr ∈ dom(Σ.M)`) and P-reg ([R] registered Binary).

Operation-surface policy: `Nullify_Binary` is the **only** retraction entry point — no direct `Emit_K` with `K ~ R` is in the operation set — and P-tgt is promoted from postcondition hypothesis to enforced precondition:

`P-tgt: a ∈ A_rel^Σ ∨ a = a_emit(Σ, d_retr)`

A call failing P-tgt (or P0, or P-reg) takes no `→_sh` step — the state is unchanged and no address is returned.

A substrate is *surface-disciplined* when every tuple in `L_R^Σ` was deposited through this operation set.

---

## DR — DisciplineRestoration (THEOREM, theorem)

On a surface-disciplined substrate, wp conjunct C3 holds at every gate-clearing emit, so a tuple is born nullified only through C2's self-nullification; and for single-tuple scope — the postcondition of ASN-0086's wp Case 1 — the weakest precondition at this surface is the operation's own:

`wp(Nullify_Binary(Σ, d_retr, a), {t : a ≼ t} ∩ A_rel^{Σ'} = {a}) ≡ P0 ∧ P-reg ∧ P-tgt`

The wrapper's full surface contract, per branch:

*Preconditions — uniform.* P0 (`d_retr ∈ dom(Σ.M)`), P-reg ([R] registered Binary — discharged globally), P-tgt (`a ∈ A_rel^Σ ∨ a = a_emit(Σ, d_retr)`), checked on every call, hits included, P0 first.

*Branch condition.* The admitted call is a *hit* iff some `(b', F', G') ∈ A_R^Σ` has `coverage(F') = subtree(d_retr)` and `coverage(G') = subtree(a)` — I0 instantiated at the wrapper's unit-depth endsets by PrefixSpanCoverage — and a *miss* otherwise.

*Miss.* The wrapper takes the `K.λ_sh` step; ASN-0126's contract holds verbatim: fresh emitter `b = a_emit(Σ, d_retr)`, `home(b) = d_retr`, deposit `({r}, {(a, δ(1, #a))}, R)`, `A_rel^{Σ'} = A_rel^Σ ∪ {b}`; and, P-tgt being enforced, the iff-P-tgt postconditions hold outright:
- `a ∈ nullified(Σ')`
- coverage nullification
- single-tuple scope: `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`
- persistence (RP-b)

*Hit.* **No step**: `Σ' = Σ`. Re-established at `Σ' = Σ` from the pre-existing tuple:
- *Residence:* `a ∈ A_rel^Σ` (self-emit disjunct cannot hit on surface-disciplined substrate: matching to-coverage `subtree(a)` determines root uniquely; self-emit candidate `a_emit(Σ, d_retr) ∉ dom(Σ.L)` while `a ∈ dom(Σ.L)`)
- *Nullification:* matching tuple in `A_R^Σ` with `a ∈ coverage(G')` (reflexivity); `a ∈ nullified(Σ)`; every resident `t` with `a ≼ t` covered likewise
- *Single-tuple scope:* `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`: ⊇ by residence with `a ≼ a`; ⊆ by R0a (FlatLinkDomain) antichain forcing `t = a`
- *Persistence:* R6a/R6c by ASN-0126's B3 and RP-b

C3 vacuity derivation: every surface-emitted R-tuple's to-coverage is `{t : a ≼ t}` at a P-tgt-valid `a`. For any later emit's fresh address `f = chain_d(m)` at Θ:
- `f ≠ a`: `f = a_emit(Θ, d) ∉ dom(Θ.L)` while `a ∈ dom(Θ.L)` (L12a and RP-b)
- `¬(a ≺ f)`: `f = chain_d(m)` has element field `(s_L, 1 + m)` of depth exactly 2 (FrontierUnification); strict prefixes of `f` are `d` (depth zeros ≤ 2, violating L1), `d.0` (zeros 3 but `#E = 0`), `d.0.s_L` (zeros 3 but `#E = 1`) — all violating L1b's `#E ≥ 2`; `a` satisfies L1 and L1b as a link address at Θ, so `a` is none of `f`'s strict prefixes
- Therefore `f ∉ {t : a ≼ t}`, and C3's existential is empty over a surface-disciplined `L_R^Θ`
