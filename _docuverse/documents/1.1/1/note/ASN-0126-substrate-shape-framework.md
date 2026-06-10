# ASN-0126: Substrate Shape Framework

*Narrowing the typed-relation framework into a concrete vocabulary apps register against*

ASN-0086 commits the substrate to typed relations of arity three over `(F, G, K)` and provides the operational vocabulary `Emit_K`, `Observe`, `Nullify`. It does not narrow the cardinalities of the F and G slots, nor does it say anything about what an app must look like when it registers a type. Apps interacting with the substrate need more than ASN-0086 gives. This note adds three things: a finite shape catalog their types are checked against, a static shape-conformance gate the substrate applies at every emit, and an immutable registry whose contents do not drift across states.

## Single-source

Every typed relation the framework gates has a single-span source: `|F| = 1`, where for an endset `e` we write `|e|` for its *span count* — since `Endset = 𝒫_fin(Span)` (ASN-0043), `|e|` is the cardinality of `e` as a finite set of spans. The one F span may itself cover a contiguous range or a whole subtree, not merely one address. In particular `F = ∅` has `|F| = 0`: the rule admits no empty-from source.

## Three shapes by G span count

With F fixed at one span, the framework varies only by what G can hold. We measure G by its span count `|G|`. The framework provides three registrable shapes, parameterized by `|G|`:

| Shape  | G span count   | What it expresses                                              |
|--------|----------------|-----------------------------------------------------------------|
| Unary  | `\|G\| = 0` (G = ∅) | A predicate or marker on a single source                    |
| Binary | `\|G\| = 1`      | A directed relation to one target span                          |
| Multi  | `\|G\|` finite   | A single source connected to finitely many — possibly zero — target spans |

Unary (`|G| = 0`) and Binary (`|G| = 1`) are mutually exclusive; the shapes classify *registrations*, not tuples: a type K is registered once with one shape, and that shape fixes which tuples are well-formed under K.

## The registry

ASN-0043/0086 carry substrate state `Σ = (Σ.C, Σ.M, Σ.L)`. This framework extends that tuple with a fourth, immutable component, the *registry*:

`Σ = (Σ.C, Σ.M, Σ.L, Σ.registry)`

The registry records, for each type an app declares, the shape its tuples must take. It is a partial function `T_admissible/~ ⇀ shape`: a key is a coverage class `[K_j]`, stored concretely as a representative `K_j ∈ T_admissible` against which CoverageEqualityDecidable (ASN-0086) settles membership; the value is the type's **shape** — one of `Unary`, `Binary`, `Multi` (Three shapes by G span count). Keying by coverage class rather than raw endset honours ASN-0086's TypeEquivalence (lifting L8, ASN-0043).

The registry value is the shape alone — *not* a type name; any human-readable label a type bears ("citation," "comment," "counterpart") is an app-side convention over addresses, not substrate state.

A registry is well-formed when shape values lie in `{Unary, Binary, Multi}` and — the condition the shape function's well-definedness actually rests on — *coverage-class keys are unique*: no two entries have `~`-equal keys.

**C0 (RegistryWellFormedness).** `Σ_init.registry` is well-formed (above) and finite: `|Σ_init.registry| < ∞`.

We write `shape(K)` for the shape the well-formed registry — a partial function of coverage classes (above) — records for `[K]`; so `shape(K)` depends only on `[K]`, defined exactly on the registered coverage classes.

## Shape-conformance

The shapes are stated in terms of the span count `|e|` of an endset; F and G are both endsets. The span-count and coverage measures diverge sharply. A single unit-depth span `(a, δ(1, #a))` is one span — `|{(a, δ(1, #a))}| = 1` — yet its coverage is `{t : a ≼ t}`, generally infinite (PrefixSpanCoverage, ASN-0043). Span-count, not coverage, is the measure.

One edge follows from counting spans rather than coverage. Types are keyed by *coverage class* (The registry) — coverage-invariant — but F-conformance counts spans, a coverage-variant notion. So a source presenting one contiguous extent as two abutting spans `(a, ℓ₁)`, `(a ⊕ ℓ₁, ℓ₂)` has `|F| = 2` and fails every shape, even though its coverage equals that of the conformant one-span F. The rule is on the side of the literal emission: **a single-span slot means a single span as emitted**. Counting spans-as-emitted keeps the measure intrinsic to the value.

The predicate `Sh-conf(K, F, G)` is defined only for *registered* K — those for which the registry records a shape. For an unregistered K, `shape(K)` does not exist and `Sh-conf(K, F, G)` carries no truth value. For a typed tuple `(F, G, K)` under a type K registered with shape s, `Sh-conf(K, F, G)` holds when:

- Unary: `|F| = 1` and `G = ∅` (equivalently `|G| = 0`);
- Binary: `|F| = 1` and `|G| = 1`;
- Multi: `|F| = 1` and `|G| < ∞`.

For Multi the conjunct `|G| < ∞` holds for *every* endset by `Endset = 𝒫_fin(Span)`, so Multi places no real bound on G's span count — it is the unrestricted, permissive shape that subsumes Unary and Binary, constraining only F.

`Sh-conf` consults no state-indexed address set: it imposes no residence check, so endset spans may reference any address, including ghost addresses at which nothing is stored. L4 and L9 (ASN-0043) permit this, and the framework inherits the permission unchanged.

The predicate therefore depends only on the tuple's span counts `|F|`, `|G|` and the shape recorded for K in the registry.

## The shape-gated emit

ASN-0086's K.λ step has precondition L3 only (arity ≥ 3, non-empty type slot); it does not inspect span counts, so the bare `→` of ASN-0086 *admits* shape-non-conforming tuples. This framework **refines** the emit step. Define the framework's transition relation

`→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh`,

where `K.λ_sh` is `K.λ` with three added preconditions: (0) *the emitted value is a standard triple* — arity 3, so it carries exactly the two content slots `(F, G)` that `Sh-conf` reads; (i) *K is registered* — the registry records a shape for K; and (ii) `Sh-conf(K, F, G)`. Precondition (0) makes the value the standard triple (StandardTriple, ASN-0043), fixing `F = e₁` and `G = e₂` as its only two content slots, and (i) supplies `shape(K)` (defined for registered K, The registry) — so `Sh-conf(K, F, G)` (partial on unregistered K, Shape-conformance) is well-defined wherever (ii) is reached. K.σ and K.α are unchanged. The refinement is confined to the guard: `K.λ_sh` adds only preconditions to `K.λ`, so its C/M/L effect, its fresh emission address `a_emit(Σ, d)`, and its C/M/L frame are identical to `K.λ`'s — added preconditions restrict *when* a step fires, not *what* it does. Call this **effect-identity**.

This gate yields the framework's safety guarantee. **P3 (Sh-confWellFormedness).** Every value a `→_sh`-step adjoins to `dom(Σ.L)` is a standard triple `(F, G, K)` whose K is registered and for which `Sh-conf(K, F, G)` holds. It is immediate: `K.λ_sh` is the only step kind that extends `dom(Σ.L)`, and (0), (i), (ii) are among its preconditions — so every deposited value is a standard triple of arity 3 by (0), with K registered by (i) and conforming to K's shape by (ii).

One class of ASN-0086 emits falls outside `→_sh` entirely. The `|F| = 1` rule (Single-source) admits no empty-from source, and `K.λ_sh`'s precondition (ii) enforces it: `Emit_K` is total over `Endset × Endset` and `∅ ∈ Endset`, so `Emit_K(Σ, d, ∅, G)` is a legitimate ASN-0086 invocation, yet — carrying no F span — it has `|F| = 0`; every registrable shape requires `|F| = 1`, so for a registered K precondition (ii) fails and for an unregistered K precondition (i) fails, and either way the emit has **no** `→_sh` image. ASN-0086's `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` is one such empty-from emit, so it too has no `→_sh` image. Retraction must therefore be re-expressed as a single-source emit before the framework can gate it (Retraction as an attributed Binary).

A second class falls outside `→_sh` for a different reason — precondition (0) itself. ASN-0086's `K.λ` admits any arity `N ≥ 3`, but precondition (0) restricts `K.λ_sh` to arity *exactly* 3, so every `N > 3` emission has **no** `→_sh` image. The path to richer arity is left to Open Question 6.

## Registry permanence

The registry is fixed when `Σ_init` is defined (The registry); we now show it never drifts. Write `π(Σ) = (Σ.C, Σ.M, Σ.L)` for the *forgetful projection* that drops the registry, returning an ASN-0086 three-component state. The framework constructs `Σ_init` by adjoining the registry to ASN-0086's three initial components, altering none of them. Two consequences follow. First, forgetting the registry recovers ASN-0086's own initial state exactly: `π(Σ_init) = Σ_init^{0086}`. Second, its base link store is empty, `Σ_init.L = ∅`, inherited from ASN-0086's base state. To show the registry never drifts we reconcile it with the transition relation. ASN-0086's relation is `→ ≡ K.σ ∪ K.α ∪ K.λ`, refined here to `→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh` (by effect-identity, a precondition-only refinement). A K.σ-step extends `dom(Σ.M)`, a K.α-step extends `dom(Σ.C)`, and a K.λ_sh-step extends `dom(Σ.L)`, each leaving the other two stores framed. We extend every step's frame condition with the registry as an additional framed component:

- K.σ: `Σ'.C = Σ.C`, `Σ'.L = Σ.L`, `Σ'.registry = Σ.registry`;
- K.α: `Σ'.M = Σ.M`, `Σ'.L = Σ.L`, `Σ'.registry = Σ.registry`;
- K.λ_sh: `Σ'.C = Σ.C`, `Σ'.M = Σ.M`, `Σ'.registry = Σ.registry`.

No step kind in `→_sh` has the registry in its *effect*; each leaves it in its frame. **P1 (RegistryInvariance).** At every `→_sh*`-reachable state, `Σ.registry = Σ_init.registry` — the registry never drifts. This follows by induction on the length of a `→_sh*`-derivation: the base case `Σ = Σ_init` is immediate, and each step preserves `Σ.registry = Σ_init.registry` by the frame condition for whichever of the three kinds it is.

Precondition (i) of `K.λ_sh` requires deciding whether the emitted `[K]` is a registered key. By P1 the registry never grows, so by C0 (The registry) it has finitely many keys at *every* reachable state; deciding (i) is then deciding `coverage(K) = coverage(K_j)` against each of the finitely many stored representative endsets `K_j`, and each such test is decidable by CoverageEqualityDecidable (ASN-0086) because it operates on the endsets `K`, `K_j` directly. Finiteness bounds the number of comparisons and CoverageEqualityDecidable discharges each one, so (i) — and hence the whole gate — is a terminating, applicable-at-every-emit check.

The registry's invariance (P1) makes a registered type's shape stable across states. **P2 (ShapeStability).** For any *registered* K, `shape(K)` takes the same value at every `→_sh*`-reachable state: since `shape(K)` is read from the P1-invariant registry, the same K cannot carry one shape at Σ and another at Σ'.

`Sh-conf` respects `~` and is stable on registered types. It respects `~` because for `K ~ K'` it reads only the span counts `|F|`, `|G|` and `shape(K) = shape(K')`, so `Sh-conf(K, F, G) = Sh-conf(K', F, G)`. It is stable because for registered K it reads only `(F, G)` and `shape(K)`, and since `shape(K)` is stable across states (P2), `Sh-conf(K, F, G)` evaluates the same against Σ as against any Σ' reachable from Σ. Moreover registration status is itself state-independent by P1 — K is registered at Σ iff registered at Σ' — so the predicate is *defined* at Σ exactly when it is defined at Σ'. **P4 (Sh-confStateIndependence).** For any *registered* K, any F, G, and any reachable Σ, Σ', `Sh-conf(K, F, G)` is defined at both states and its verdict at Σ equals its verdict at Σ'.

## The projection bridge

Registry permanence introduced the forgetful projection `π`. We now show it is a *bridge*: it carries this framework's gated dynamics onto ASN-0086's ungated dynamics, so that every ASN-0086 result holds, suitably projected, here.

**Lemma (ProjectionBridge).** `π` maps every `→_sh`-step to an ASN-0086 `→`-step, and hence every `→_sh*`-reachable state of this framework to a state `→*`-reachable from ASN-0086's initial state.

*Proof.* Each `→_sh`-step preserves the registry in its frame (Registry permanence) and acts on the C/M/L components exactly as the corresponding ASN-0086 step: a K.σ-step as `K.σ`, a K.α-step as `K.α`, and a `K.λ_sh`-step as a `K.λ` step — the last by effect-identity, its C/M/L action being `K.λ`'s. Hence whenever `Σ →_sh Σ'`, `π(Σ) → π(Σ')` in ASN-0086's relation. By induction on derivation length, `π` maps every `→_sh*`-reachable state to a state `→*`-reachable from ASN-0086's initial state: at the base, `π(Σ_init) = Σ_init^{0086}` (Registry permanence), trivially `→*`-reachable from itself; and each step extends a `→`-derivation rooted at `Σ_init^{0086}` by the projected step just exhibited. ∎

The bridge has two consequences.

**(B1) Shared components.** Σ and `π(Σ)` share their C, M, and L components. Every ASN-0086 state-indexed function this note invokes — `a_emit(·, d)`, `A_rel^·`, `L_K^·`, `A_K^·`, and `nullified(·)` — reads only the C/M/L components (in each definition only `dom(Σ.L)`, the link values `Σ.L(·)`, `coverage`, and `origin` appear — never the registry), so each takes equal values at Σ and `π(Σ)` and is thereby well-defined on this note's four-component states by evaluation at the projection, `f(Σ) := f(π(Σ))`. In particular, since `a_emit` reads only M and L, `a_emit(π(Σ), d) = a_emit(Σ, d)` and `dom(π(Σ).L) = dom(Σ.L)`; consequently `A_rel^{π(Σ)} = A_rel^Σ` (AddressPartition, ASN-0086, gives `A_rel^Σ = dom(Σ.L)`).

**(B2) Lemma transfer.** Take any ASN-0086 result whose conclusion is a predicate over the C/M/L components — either of a single `→*`-reachable state, or of a transition between two states each separately exhibited as `→_sh`-reachable. For each state Σ this note reasons about, `π(Σ)` is `→*`-reachable (ProjectionBridge), so the result holds at `π(Σ)`; since it constrains only the shared C/M/L components, its conclusion transfers to Σ directly. B2 yields no `→_sh`-successors: an existence-of-successor conclusion `∃ Σ' : Σ → Σ' ∧ …` transfers only to a `→`-successor of `π(Σ)`, which need not lift to a `→_sh`-step of Σ.

## Gate realizability

The one existence-of-successor result this framework needs — that a *conforming* emit actually fires — does not come from B2, which yields no `→_sh`-successors (The projection bridge). We establish it directly, by applying ASN-0086's `Emit_K` at `π(Σ)` and manually lifting its `K.λ` step back to a `K.λ_sh` step. (This is also why R0 (TupleAddressFreshness, ASN-0086), itself an existence-of-successor result, is reached here by lifting rather than by B2 transfer.) The lift needs one fact about registered types.

**Lemma (RegisteredAdmissible).** Every registered K satisfies `K ∈ T_admissible`. By C0 (RegistryWellFormedness, The registry) the registry stores, for K's coverage class, a finite representative endset `K_j ∈ T_admissible`, and — by the coverage-class keying established there — "K registered" means `coverage(K) = coverage(K_j)`. Non-emptiness must transfer from the stored representative to the emitted type, since the emitted triple's type slot is `K`, not `K_j`: `K_j ∈ T_admissible` is non-empty and every span has length `ℓ > 0`, so `coverage(K_j) ≠ ∅`; hence `coverage(K) = coverage(K_j) ≠ ∅`, so `K ≠ ∅`, i.e. `K ∈ T_admissible`.

**P5 (GateRealizability).** For any `→_sh*`-reachable Σ, any `d ∈ dom(Σ.M)`, any registered K, and any `F, G ∈ Endset` with `Sh-conf(K, F, G) = ⊤`, there exists Σ' with `Σ →_sh Σ'` depositing the standard triple `(F, G, K)` at the fresh address `a = a_emit(Σ, d)`:

`a ∉ dom(Σ.L) ∧ a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K) ∧ home(a) = d`,

with Σ' itself `→_sh*`-reachable.

*Proof.* The premises are exactly `Emit_K`'s hypotheses at the projected state, the gate conditions hold for a conforming triple by inspection, and the only real work is lifting `Emit_K`'s ungated `K.λ` step — fired at the pinned address `a_emit` — back to a gated `K.λ_sh` step.

First, `K ∈ T_admissible` by Lemma (RegisteredAdmissible), since K is registered. The emitted type slot is therefore non-empty — discharging both `Emit_K`'s `K ∈ T_admissible` precondition and L3's non-empty-type-slot clause. With `F, G ∈ Endset`, the standard triple `(F, G, K)` discharges L3 directly through R0's value-shape consequence — arity 3, both content slots in `Endset`.

Second, apply ASN-0086's `Emit_K` operation at `π(Σ)`, whose contract pins the fresh address to `a = a_emit(Σ, d)` — the address P5 names. By the projection bridge (Lemma ProjectionBridge), `π(Σ)` is `→*`-reachable, so `Emit_K` is applicable. `Emit_K(π(Σ), d, F, G)` — with `d ∈ dom(Σ.M) = dom(π(Σ).M)` and `K ∈ T_admissible` (above) — invokes a `K.λ` step at home `d`, depositing `(F, G, K)`, and pins its fresh address to `a = a_emit(π(Σ), d)` by the operation's contract; it returns `(Σ_{0086}, a)` with `a ∉ dom(π(Σ).L)`, `a ∈ dom(Σ_{0086}.L)`, `home(a) = d`, `Σ_{0086}.L(a) = (F, G, K)`. The bridge's shared-components consequence (B1) gives `a_emit(π(Σ), d) = a_emit(Σ, d)` — the address P5 names — and `dom(π(Σ).L) = dom(Σ.L)`, so `a ∉ dom(Σ.L)`.

Third, lift the step. The underlying ASN-0086 step is the `K.λ` step that `Emit_K` realizes at the pinned address `a_emit(Σ, d)`. Form Σ' by adjoining the unchanged registry to `Σ_{0086}`: `Σ'.C = Σ_{0086}.C`, `Σ'.M = Σ_{0086}.M`, `Σ'.L = Σ_{0086}.L`, `Σ'.registry = Σ.registry`. We verify `Σ → Σ'` is a `K.λ_sh`-step. By effect-identity its C/M/L effect is `K.λ`'s, realized by the `Emit_K` step at `a_emit`, and its registry frame `Σ'.registry = Σ.registry` holds by construction. Its preconditions: the inherited L3 and `d ∈ dom(Σ.M)` hold (discharged above and by premise); (0) arity 3 holds — the value is the standard triple `(F, G, K)`; (i) K registered — premise; (ii) `Sh-conf(K, F, G) = ⊤` — premise. All hold, so `Σ → Σ'` is a `K.λ_sh`-step, hence a `→_sh`-step, and Σ' is `→_sh*`-reachable. Its post-state map gives `a ∈ dom(Σ'.L)`, `Σ'.L(a) = (F, G, K)`, `home(a) = d`, completing the claim. ∎

## Retraction as an attributed Binary

The shape-gated emit observed that ASN-0086's empty-from `Nullify` has no `→_sh` image. With the gate and the projection bridge in hand, we re-express retraction so the framework can gate it. To obtain a gated retraction an app registers R as **Binary** and routes through the one-span wrapper `Emit_R(Σ, d_retr, {r}, {(a, δ(1, #a))})` — canonical from-fill `r = (d_retr, δ(1, #d_retr))`, giving `|F| = |G| = 1`. The target stays in G, so ASN-0086's `nullified`/`L_R`/active-subset machinery — all reading `coverage(G')` and ignoring F — carries over unchanged.

Binary registration is strictly weaker than ASN-0086's UnitDepthRetractionDiscipline in *two* independent ways, and single-tuple-scope survives only if the app closes *both* gaps. First, Binary gates G by span count alone, so a single G-span of non-unit length — say `(t, δ(2, #t))`, covering a contiguous multi-address range — is equally Binary-conformant, hence a legal `→_sh`-step that withdraws a whole region at once. The unit-depth wrapper closes this first gap by writing the canonical `{(a, δ(1, #a))}` to-span by construction. Second — and this gap the gate cannot see at all — even the unit-depth wrapper attains R-Scope's single-tuple-scope result `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` only when its *target* `a` satisfies R-Scope's hypothesis P-tgt: `a ∈ A_rel^Σ` (an existing link address) or `a = a_emit(Σ, d_retr)` (the fresh self-emit address). The unit-depth *form* is necessary but not sufficient: R-Scope's conclusion rests on R0a (FlatLinkDomain) — link addresses form a prefix-antichain, so the only link `≼`-above a *leaf* target is the target itself. Aim the same wrapper at an interior prefix and that antichain argument lapses. Take the ghost link-subspace root `a = d_retr.0.s_L` — concretely `1.1.0.1.0.1.0.2` when `d_retr = 1.1.0.1.0.1` — for which `zeros(a) = 3` but `#E(a) = 1`, so `a ∉ dom(Σ.L)` and `a ≠ a_emit(Σ, d_retr)`: P-tgt fails on both disjuncts. The wrapper `Emit_R(Σ, d_retr, {r}, {(a, δ(1, #a))})` has `|F| = |G| = 1` and *clears the Binary gate*, yet `coverage({(a, δ(1, #a))}) = {t : a ≼ t}` is the entire link subspace homed at `d_retr`, so `{t : a ≼ t} ∩ A_rel^{Σ'}` contains *every* link homed there (`1.1.0.1.0.1.0.2.1`, `1.1.0.1.0.1.0.2.2`, …), not just `{a}` — single-tuple-scope fails wholesale, and nothing in `→_sh` rejects the call. Single-tuple-scope is therefore an *app obligation* — route through the unit-depth wrapper **and** supply a P-tgt-valid target — not a guarantee `→_sh` discharges.

R-Scope (ASN-0086) is proven for the empty-from Nullify over ASN-0086's three-component `→*`-reachable states, not for this Binary wrapper. With a P-tgt-valid target (above), its conclusion nonetheless reaches the wrapper's post-state in three moves. *Bind the post-state.* The Binary wrapper's value is shape-conforming: R is registered Binary and `|F| = |{r}| = 1`, `|G| = |{(a, δ(1, #a))}| = 1`, so `Sh-conf(R, {r}, {(a, δ(1, #a))}) = ⊤`. With `d_retr ∈ dom(Σ.M)` (Nullify's P0), the conforming gated emit therefore exists by P5 (GateRealizability, Gate realizability): let `Σ →_sh Σ'` be the `→_sh`-step it takes, depositing `({r}, {(a, δ(1, #a))}, R)` at the fresh address `a_emit(Σ, d_retr)`. *Apply R-Scope within ASN-0086.* By ProjectionBridge `π(Σ)` is `→*`-reachable, so — `a` meeting P-tgt at `π(Σ)` — R-Scope applies to the empty-from `Nullify(π(Σ), d_retr, a) = Emit_R(π(Σ), d_retr, ∅, {(a, δ(1, #a))})`, whose post-state `Ψ` satisfies `{t : a ≼ t} ∩ A_rel^{Ψ} = {a}`. This is R-Scope at its native transition, *not* a B2 transfer: `Ψ` is not `→_sh`-reachable (the empty-from Nullify is not a `→_sh`-step, The shape-gated emit), so B2 does not reach it (The projection bridge). *Frame the two post-states together* — the load-bearing step. The wrapper's underlying ASN-0086 step `π(Σ) → π(Σ')` (by ProjectionBridge) and the Nullify `π(Σ) → Ψ` both call `a_emit` on the *same* `(π(Σ), d_retr)`, and `a_emit` is blind to F, so both emit at the *identical* fresh address and yield the *same* post-state link domain: `dom(π(Σ').L) = dom(Ψ.L)`, hence `A_rel^{π(Σ')} = A_rel^{Ψ}`. The two post-states differ only in the value stored at that address (`F = ∅` for Nullify, `F = {r}` for the wrapper), which neither `A_rel` nor the fixed target subtree `{t : a ≼ t}` reads. Substituting, `{t : a ≼ t} ∩ A_rel^{π(Σ')} = {t : a ≼ t} ∩ A_rel^{Ψ} = {a}`. Finally B1, applied at the `→_sh*`-reachable Σ', shares the L-component — `A_rel^{π(Σ')} = A_rel^{Σ'}` — giving `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` at the wrapper's four-component post-state.

## Weakest precondition of the shape-gated emit

With the gate (The shape-gated emit) and the projection bridge established, we take the postcondition `(a, F, G) ∈ A_K^{Σ'}` — the emitted tuple lands in the *active* subset of its type at the post-state — and reason backward, refining ASN-0086's Case-2 wp.

ASN-0086 (wp Case 2) gives, for the ungated `Emit_K` over ASN-0086's `→*`-reachable states, with fresh address `a = a_emit(Σ, d)` — and applies to this note's `→_sh*`-reachable Σ by the projection bridge, which sends Σ to the `→*`-reachable `π(Σ)` where wp Case 2 holds (B2), Σ and `π(Σ)` agreeing on the C/M/L components the wp reads (B1):

`wp(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) ≡ d ∈ dom(Σ.M) ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G)) ∧ ¬(∃ (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∈ coverage(G'))`.

The three inherited conjuncts read: the home is an allocated document (C1); the emit is not a self-nullifying retraction — the `K ≁ R` escape (C2); and no pre-existing retraction tuple already covers the fresh address (C3). By effect-identity, the gated emit deposits `(F, G, K)` at `a_emit(Σ, d)` under precisely ASN-0086's post-state map, but is *enabled* on a strictly smaller guard. For a guarded operation `g → S`, `wp(g → S, R) ≡ g ∧ wp(S, R)` when the postcondition requires the operation to fire — and the active-subset postcondition is unattainable if the emit does not fire, since then the tuple is never deposited and `(a, F, G) ∉ A_K^{Σ'}`. With added guard `g_sh ≡ K registered ∧ Sh-conf(K, F, G)` — a *conditional* conjunction, the left conjunct guarding the right exactly as the gate orders (i) before (ii), so that `g_sh` is *false* (not undefined) at an unregistered K (`Sh-conf` partial there, Shape-conformance) — and `wp(S, R)` ASN-0086's Case-2 right-hand side (the arity guard (0) is omitted from `g_sh` because the postcondition's arity-3 slice `|Σ.L(a)| = 3` already forces it):

`wp(Emit under →_sh, (a, F, G) ∈ A_K^{Σ'})`
`≡ {g → S guard conjunction}`
`K registered ∧ Sh-conf(K, F, G) ∧ d ∈ dom(Σ.M) ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G)) ∧ ¬(∃ (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∈ coverage(G'))`.

The underlying `Emit_K` carries two further enablement preconditions — `K ∈ T_admissible` and L3 — but neither contributes a wp conjunct: they are discharged by precondition (0), the input typing `F, G ∈ Endset`, and Lemma (RegisteredAdmissible) (Gate realizability).

This weakest precondition is *strictly stronger* than `K.λ_sh`'s own precondition: the gate (`g_sh ≡ K registered ∧ Sh-conf(K, F, G)`, together with the inherited L3 and `d ∈ dom(Σ.M)`) governs only well-formedness — it *enables* the emit, is what P3 rests on, and deposits the conforming tuple into the *audit* slice `L_K^{Σ'}` — whereas the two remaining inherited conjuncts C2 and C3 govern *landing* in the *active* subset `A_K^{Σ'}`. **Both** can fail for a gate-clearing emit. C2, `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`, fails for a *self-nullifying retraction* — `K ~ R ∧ a_emit(Σ, d) ∈ coverage(G)`, the retraction's own to-set covering its fresh address `a = a_emit(Σ, d)`. A gate-clearing witness is the Binary self-emit `Emit_R(Σ, d, {r}, {(a, δ(1, #a))})` with self-target `a = a_emit(Σ, d)` — the attributed Binary wrapper (Retraction as an attributed Binary) — whose `|F| = |{r}| = 1` and `|G| = 1` clear the gate where the empty-from Nullify it re-expresses has no `→_sh` image. C3, `¬(∃ (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∈ coverage(G'))`, fails when a *pre-existing* `L_R` tuple already covers that address. Under either failure the tuple is *born nullified* — present in the audit slice `L_K^{Σ'}` yet absent from the active subset `A_K^{Σ'}`.

What singles out C3 is not that it can fail — so can C2 — but that it is the conjunct *newly* live under `→_sh`. Under ASN-0086's unit-depth retraction discipline C3 was vacuous: unit-depth to-spans together with R0a (FlatLinkDomain) force `a_emit(Σ, d) ∉ coverage(G')` for every pre-existing `L_R` tuple — the disciplined-domain simplification of ASN-0086's wp Case 2. By Retraction as an attributed Binary, `→_sh` admits non-unit retraction to-spans whose coverage can include a fresh address, so C3 becomes live. C2's self-nullification, by contrast, is inherited from ASN-0086 and already live there.

The dual reading is liveness. Where P3 guarantees every tuple a `→_sh`-step deposits conforms, its liveness dual **P5 (GateRealizability)** — established above (Gate realizability) — guarantees the converse: every conforming triple *can* be deposited by a `→_sh`-step. Safety (P3) and realizability (P5) together pin down exactly which emits the gate admits.

## Reachable conformance

We lift P3's single-step guarantee to an invariant holding at every reachable state. **P6 (ReachableConformance).** For every `→_sh*`-reachable Σ and every `a ∈ dom(Σ.L)`, the stored value `Σ.L(a)` is a standard triple `(F, G, K)` whose K is registered and for which `Sh-conf(K, F, G) = ⊤`. This is the state-level closure of P3's single-step half — the guarantee a consuming app relies on. *Derived* by induction on derivation length: the base `Σ_init.L = ∅` (Registry permanence) holds vacuously; each `→_sh`-step either leaves `dom(Σ.L)` unchanged (K.σ, K.α) or extends it by one tuple that P3 forces to be a standard triple with K registered and conforming. The induction hypothesis being carried is the *predicate* "stored value is a standard triple ∧ K registered ∧ `Sh-conf(K, F, G) = ⊤`," not merely value-persistence. For the tuple a step newly deposits, P3 supplies all three conjuncts — the standard-triple shape from precondition (0) of `K.λ_sh`, registration from (i), conformance from (ii). For a tuple already present, the three conjuncts persist by, in turn: L12 (LinkImmutability, ASN-0043), under which the stored value `(F, G, K)` — and hence its standard-triple shape — persists unchanged, holding at `π(Σ)` and transferred to Σ by the projection bridge (B2), each `→_sh`-step projecting to a `→`-step with the L-component shared (B1, `Σ.L = π(Σ).L`); P1 (RegistryInvariance, Registry permanence), under which K's registration status persists, the registry being invariant so a type registered at Σ is registered at Σ'; and P4 (Sh-confStateIndependence), under which the conformance verdict persists, `Sh-conf(K, F, G)` being defined and evaluating identically at Σ and Σ'.

## Properties established

- **P1 (RegistryInvariance)**
- **P2 (ShapeStability)**
- **P3 (Sh-confWellFormedness)**
- **P4 (Sh-confStateIndependence)**
- **P5 (GateRealizability)**
- **P6 (ReachableConformance)**

## Worked illustration

We fix concrete addresses to check P3 and P4 against a real scenario. Let the content subspace be `s_C = 1` and the link subspace `s_L = 2`. Take a document with prefix `d = 1.1.0.1.0.1` (node `1.1`, user `1`, document `1`; `zeros(d) = 2`). Its content occupies subspace 1:

- `c₁ = 1.1.0.1.0.1.0.1.1`
- `c₂ = 1.1.0.1.0.1.0.1.2`
- `c₃ = 1.1.0.1.0.1.0.1.3`

each an element-level I-address with `zeros = 3`. Write `[x] = {(x, δ(1, #x))}` for the unit-depth singleton endset at `x` — a one-span endset, so `|[x]| = 1` (here `coverage([x]) = {t : x ≼ t}`, by PrefixSpanCoverage).

Consider five registered coverage classes. The registry records only their shapes; the readable labels `approved`, `succession`, `citation`, `touched`, `retract` are the app's own (app-side, not substrate state — The registry):

- `approved`: Unary
- `succession`: Binary
- `citation`: Multi
- `touched`: Multi
- `retract`: Binary — the app-registered retraction type R (the attributed Binary re-expression of ASN-0086's Nullify, Retraction as an attributed Binary)

**Unary.** Emit `(F, G, approved)` with `F = [c₁]`, `G = ∅`. Then `|F| = 1` and `|G| = 0`, so `Sh-conf(approved, [c₁], ∅) = ⊤` and `K.λ_sh` is enabled. The variant `([c₁], [c₂], approved)` has `|G| = 1 ≠ 0`, so `Sh-conf = ⊥`; no `→_sh`-step deposits it into `dom(Σ.L)` at any reachable state (P3).

**Binary.** Emit `(F, G, succession)` with `F = [c₂]`, `G = [c₁]` — "`c₂` supersedes `c₁`." Each endset carries one span, so `|F| = |G| = 1` and `Sh-conf(succession, [c₂], [c₁]) = ⊤`. The two-target variant `G = [c₁] ∪ [c₃]` has `|G| = 2`, failing Binary's `|G| = 1`.

**Multi.** Emit `(F, G, citation)` with `F = [c₁]`, `G = [c₂] ∪ [c₃]` — one source citing two targets. `|F| = 1` and `|G| = 2 < ∞`, so `Sh-conf(citation, [c₁], [c₂] ∪ [c₃]) = ⊤`. (Each of `[c₂]`, `[c₃]` covers a subtree; the span *count* is 2, which is what Multi reads.) The zero-target boundary the table advertises conforms too: `(F, ∅, citation)` with `F = [c₁]` has `|F| = 1` and `|G| = 0 < ∞`, so `Sh-conf(citation, [c₁], ∅) = ⊤`. This Multi tuple is *shape-indistinguishable* from the Unary `([c₁], ∅, approved)` above — same `|F| = 1`, same `G = ∅` — yet it is typed Multi, not Unary; only `citation`'s registration separates the two. Shapes classify registrations, not tuples (Three shapes by G span count).

**Two Multi types coexist (C0).** `citation` and `touched` are both Multi, yet they are distinct registry entries. The registry keys entries by coverage class, not by shape, and C0 (The registry) requires those coverage-class keys be unique — so any number of Multi types may coexist, provided their keys differ (`[K_citation] ≠ [K_touched]`). Emit `(F, G, touched)` with `F = [c₂]`, `G = [c₁] ∪ [c₃]`: `|F| = 1` and `|G| = 2 < ∞`, so `Sh-conf(touched, [c₂], [c₁] ∪ [c₃]) = ⊤` — `⊤` for the same structural reason as `citation`, both reading only `|F| = 1` and `|G| < ∞`. The shapes coincide; the tuples do not. Their type slots carry endsets of distinct coverage class, so the two emits land in distinct typed relations, `L_touched ≠ L_citation` (the type subscript is a coverage-class index, ASN-0086). Shape governs well-formedness; coverage class governs identity. At the opposite extreme C0 permits the *empty* registry `Σ_init.registry = ∅` (`|Σ_init.registry| < ∞` admits 0); there precondition (i) of `K.λ_sh` fails for every emit, so `→_sh` never extends `dom(Σ.L)` — the substrate stays inert until an app registers a type.

**State-independence (P4), with ghosts.** Take two reachable states: `Σ`, in which only `c₁` has been stored, so `c₂, c₃ ∉ dom(Σ.C)` — they are ghost addresses; and `Σ'`, reachable from `Σ`, in which `c₂, c₃` have since been stored. The citation emit above references `c₂, c₃`. Evaluate `Sh-conf(citation, [c₁], [c₂] ∪ [c₃])` at each: by P4 the predicate inspects only the span counts `|F| = 1`, `|G| = 2` and `citation`'s registered shape `Multi`, so it returns `⊤` at both `Σ` and `Σ'`, identically. The citation is thus emittable at `Σ` exactly as at `Σ'`, and its ghost targets are admissible (L4/L9).

**Born nullified (gate fires, tuple lands inactive).** We exhibit a concrete witness of the gate-vs-landing separation given at Weakest precondition of the shape-gated emit. Link addresses homed at `d` form a contiguous chain (L-ContiguousPrefix, ASN-0086, transferred to this note's `→_sh*`-reachable states by the projection bridge, B2), enumerated `ℓ₁ = 1.1.0.1.0.1.0.2.1`, `ℓ₂ = 1.1.0.1.0.1.0.2.2`, then by sibling advance (`a_emit = inc(ℓ_prev, 0)`). Begin at a state `Σ₀` reachable from `Σ_init` in which two citation links already occupy `ℓ₁, ℓ₂` (so `dom(Σ₀.L) = {ℓ₁, ℓ₂}` homed at `d`).

*Step 1 — emit a Binary R-tuple with a non-unit G.* Using the generic gated `Emit_R` (not the unit-depth wrapper of Retraction as an attributed Binary, which could not supply a range G), issue `Emit_R(Σ₀, d, [c₁], G_rng)` with attributing source `[c₁]` (`|F| = 1`) and a *single* range span `G_rng = {(g, δ(3, #g))}` where `g = 1.1.0.1.0.1.0.2.4`; so `|G_rng| = 1` and `coverage(G_rng) = {t : 1.1.0.1.0.1.0.2.4 ≤ t < 1.1.0.1.0.1.0.2.7}`, a contiguous range of three link siblings and their subtrees. The gate fires: (0) the value `([c₁], G_rng, retract)` is a triple; (i) `retract` is registered; (ii) `Sh-conf(retract, [c₁], G_rng) = ⊤` since `retract` is Binary and `|F| = |G_rng| = 1`. This exercises the gap noted in Retraction as an attributed Binary: the gate admits the non-unit Binary `G_rng`. The tuple deposits at the fresh `a_R = a_emit(Σ₀, d) = inc(ℓ₂, 0) = 1.1.0.1.0.1.0.2.3`. Note `a_R ∉ coverage(G_rng)` (`...2.3 < ...2.4`), so even this retraction lands active — it does not nullify itself. Call the post-state `Σ₁`; now `L_retract^{Σ₁} = {(a_R, [c₁], G_rng)}`.

*Step 2 — emit a conforming non-R tuple into the covered range.* Issue `Emit_citation(Σ₁, d, [c₁], [c₂] ∪ [c₃])`. The fresh address is `a = a_emit(Σ₁, d) = inc(a_R, 0) = 1.1.0.1.0.1.0.2.4 = g`. The gate fires again — (0) triple; (i) `citation` registered; (ii) `Sh-conf(citation, [c₁], [c₂] ∪ [c₃]) = ⊤` (`|F| = 1`, `|G| = 2 < ∞`, Multi). So this is a legal `→_sh`-step and the tuple enters the audit slice `L_citation^{Σ₂}`.

*The landing fails.* Yet `(a, [c₁], [c₂] ∪ [c₃]) ∉ A_citation^{Σ₂}`. Trace the inherited wp third conjunct `¬(∃ (b, F', G') ∈ L_R^{Σ₁} :: a_emit(Σ₁, d) ∈ coverage(G'))`: the retraction tuple `(a_R, [c₁], G_rng) ∈ L_R^{Σ₁}` has `a = g ∈ coverage(G_rng)` (since `g` is the lower endpoint of the half-open range), so the existential holds and the conjunct is *false*. By ASN-0086's `nullified`/`A_K` machinery the citation is born nullified: `a ∈ nullified(Σ₂)`, hence `(a, [c₁], [c₂] ∪ [c₃]) ∉ A_citation^{Σ₂}`. The gate did not reject this call — all of (0), (i), (ii) held — the wp's inherited third conjunct did.

## Open questions

The following are left for the successor note that layers operational semantics on this framework:

1. **Idem semantics at emit.** What must the substrate guarantee when an app re-emits a tuple "the same as" an existing active tuple of an idempotent type, and what is the criterion of sameness?

2. **Behavior catalog.** Which substrate-provided behaviors (read-filter, transitive-closure, typed-reverse-lookup, age-staleness) compose with which shapes, and what predicates does each unlock?

3. **Default predicates.** What predicates does every registered type receive by virtue of its shape and idem flag, independent of any behavior?

4. **Standard registrations.** Does the substrate ship any types pre-registered, or is each substrate's `Σ_init.registry` composed entirely of app-declared entries?

5. **Predicate composition.** What composition rules govern the atomic predicates each type receives?

6. **Extension beyond F=1 and N=3.** What path serves an app that needs richer arity — a supplemental note loosening the constraints here, or a parallel framework?
