# ASN-0126: Substrate Shape Framework

*Narrowing the typed-relation framework into a concrete vocabulary apps register against*

ASN-0086 commits the substrate to typed relations of arity three over `(F, G, K)` and provides the operational vocabulary `Emit_K`, `Observe`, `Nullify`. It does not narrow the cardinalities of the F and G slots, nor does it say anything about what an app must look like when it registers a type. Apps interacting with the substrate need more than ASN-0086 gives. This note adds three things: a finite shape catalog their types are checked against, a static shape-conformance gate the substrate applies at every emit, and an immutable registry whose contents do not drift across states.

## Single-source

Every typed relation *the framework gates* — every registered type emitted under `→_sh` — has a single-span source — `|F| = 1`, where for an endset `e` we write `|e|` for its *span count*: the number of spans `e` contains, **not** the number of tumblers in `coverage(e)`. This is a commitment about what the framework admits, not about the link store underneath: a tuple filed directly into the link store (ASN-0043) may carry `|F| > 1`. The substrate narrows away only the multi-span, discontiguous from-set that the full link store (ASN-0043) would permit; it does not narrow what one span may reach — the one F span may itself cover a contiguous range or a whole subtree, not merely one address.

The one place this commitment bites against ASN-0086's own vocabulary is retraction. ASN-0086 defines `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` — an *empty* from-set, with the target carried in G. Under `|F| = 1` that empty form fails every shape, so ASN-0086's literal `F = ∅` Nullify has **no** `→_sh` image.

The framework supplies a one-span source in place of the empty one. The retraction wrapper is `Emit_R(Σ, d_retr, [r], {(a, δ(1, #a))})`: a one-span source (`|F| = 1`) and the single target as one unit-depth to-span in G (`|G| = 1`). The canonical fill for the from-slot is the home document's own unit-depth span, `r = (d_retr, δ(1, #d_retr))`. This shape — `|F| = 1`, `|G| = 1` — is exactly **Binary**, so R is registered Binary. Because the target remains in G as that single span, ASN-0086's `nullified`/`L_R`/active-subset machinery, all of which read `coverage(G')` and ignore F, carry over unchanged.

Binary registration is strictly weaker than ASN-0086's UnitDepthRetractionDiscipline: a single G-span of non-unit length — say `(t, δ(2, #t))`, covering a contiguous multi-address range — is equally Binary-conformant. Because `→_sh` gates R by Binary alone, a non-unit (contiguous-range) retraction is a legal `→_sh`-step that withdraws a whole contiguous region at once; unit-depth and R-Scope's single-tuple-scope result `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` hold only when the app routes every retraction through the unit-depth wrapper `Emit_R(Σ, d_retr, [r], {(a, δ(1, #a))})`, which writes the canonical `{(a, δ(1, #a))}` to-span by construction. Only *discontiguous* multi-target retraction falls to the front end.

We settle the relationship to the underlying link store explicitly: `→_sh` is the *complete* transition relation of a framework-governed substrate — every emit it admits is a `K.λ_sh`-step through the gate. The "only conforming tuples" conclusion below is inductive, so it needs a base case the gate cannot supply: we commit that the framework's base state carries an empty link store, `Σ_init.L = ∅` (inherited from ASN-0086's base state). With that base discharged, induction over `→_sh`-steps gives that within such a substrate `dom(Σ.L)` carries only conforming tuples and there is no off-gate path into the link store — the reachable-state conformance invariant P7 (Properties established). An app needing multi-source relations drops to a *different* substrate — ASN-0086's ungated `→`, whose `K.λ` admits arbitrary arity directly.

## Three shapes by G span count

With F fixed at one span, the framework varies only by what G can hold. We measure G by its *span count* `|G|` (Single-source). The framework provides three registrable shapes, parameterized by `|G|`:

| Shape  | G span count   | What it expresses                                              |
|--------|----------------|-----------------------------------------------------------------|
| Unary  | `\|G\| = 0` (G = ∅) | A predicate or marker on a single source                    |
| Binary | `\|G\| = 1`      | A directed relation to one target span                          |
| Multi  | `\|G\|` finite   | A single source connected to finitely many — possibly zero — target spans (subsumes Unary and Binary) |

These conditions do **not** partition the space of expressible tuples: Unary (`|G| = 0`) and Binary (`|G| = 1`) are mutually exclusive, but Multi subsumes both (Shape-conformance). The shapes therefore classify *registrations*, not tuples: a type K is registered once with one shape, and that shape fixes which tuples are well-formed under K.

## Shape-conformance

The shapes are stated in terms of the *span count* `|e|` of an endset (Single-source). F and G are endsets, and `Endset = 𝒫_fin(Span)` (ASN-0043) — a finite set of spans, so `|e|` is its cardinality as that set. The span-count and coverage measures diverge sharply. A single unit-depth span `(a, δ(1, #a))` is one span — `|{(a, δ(1, #a))}| = 1` — yet its coverage is `{t : a ≼ t}`, generally infinite (PrefixSpanCoverage, ASN-0043). Every non-empty span `(s, ℓ)` denotes the half-open interval `{t ∈ T : s ≤ t < s ⊕ ℓ}`, which is infinite: by T0(b) (UnboundedLength, ASN-0034) `s` admits unboundedly many proper extensions, each agreeing with `s` through the action point of `ℓ` and so lying below `s ⊕ ℓ` by T1 (LexicographicOrder, ASN-0034), hence in the interval. No non-empty endset therefore has singleton coverage, so a `|coverage(F)| = 1` discipline would admit nothing; span-count, not coverage, is the measure.

One edge follows from counting spans rather than coverage. Types are keyed by *coverage class* (Registration entries) — coverage-invariant — but F-conformance counts spans, a coverage-variant notion. So a source presenting one contiguous extent as two abutting spans `(a, ℓ₁)`, `(a ⊕ ℓ₁, ℓ₂)` has `|F| = 2` and fails every shape, even though its coverage equals that of the conformant one-span F. The rule is on the side of the literal emission: **a single-span slot means a single span as emitted**, and coalescing abutting spans to that canonical form before emit is the app's responsibility wherever a shape constrains a slot to one span — F under every shape, G under Binary — not the substrate's at the gate (udanax-green performs no endset coalescing, `spanf1.c`). (Genuinely discontiguous multi-span F — a gap between spans, hence a *different* coverage — is rejected on its own merits as the multi-source case the substrate does not provide; see Single-source.) Counting spans-as-emitted keeps the measure intrinsic to the value and thus state-independent (P5).

The predicate `Sh-conf(K, F, G)` is defined only for *registered* K — those for which the registry records a shape. For an unregistered K, `shape(K)` does not exist and `Sh-conf(K, F, G)` carries no truth value. For a typed tuple `(F, G, K)` under a type K registered with shape s, `Sh-conf(K, F, G)` holds when:

- Unary: `|F| = 1` and `G = ∅` (equivalently `|G| = 0`);
- Binary: `|F| = 1` and `|G| = 1`;
- Multi: `|F| = 1` and `|G| < ∞`.

For Multi the conjunct `|G| < ∞` holds for *every* endset by `Endset = 𝒫_fin(Span)`, so Multi places no real bound on G's span count — it is the unrestricted, permissive shape, constraining only F.

`Sh-conf` consults nothing about content residence. Endset spans may reference any address, including ghost addresses at which nothing is stored: L4 and L9 (ASN-0043) permit this, Nelson is explicit that "endset addresses do NOT need to resolve to stored content" — the type endset especially "is designed to exploit this" — and Gregory confirms udanax-green enforces no residence check at link creation. The framework inherits that permission unchanged. In particular `Sh-conf` consults no state-indexed address set.

The predicate therefore depends only on the tuple's span counts `|F|`, `|G|` and the shape recorded for K in the registry — a property of the tuple-plus-registration pair, evaluable identically at any reachable state.

### The shape-gated emit

ASN-0086's K.λ step has precondition L3 only (arity ≥ 3, non-empty type slot); it does not inspect span counts, so the bare `→` of ASN-0086 *admits* shape-non-conforming tuples. This framework **refines** the emit step. Define the framework's transition relation

`→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh`,

where `K.λ_sh` is `K.λ` with three added preconditions: (0) *the emitted value is a standard triple* — arity 3, so it carries exactly the two content slots `(F, G)` that `Sh-conf` reads; (i) *K is registered* — the registry records a shape for K; and (ii) `Sh-conf(K, F, G)`. These are read left-to-right under the **domain-discharge ordering**: (0) and (i) jointly discharge the domain condition for (ii). `Sh-conf` is defined only over a standard triple — it reads exactly two content slots, so a higher-arity value `(e₁, e₂, e₃, e₄, K)` has no defined reading — and only for registered K, where `shape(K)` exists. So arity-3 and registration must both hold before (ii) carries a truth value; a value of arity ≠ 3 fails (0) and is simply not a `→_sh`-step, and an unregistered K fails (i) before the conformance test is reached. An emit of value `(F, G, K)` is thus a `→_sh`-step only when it is a standard triple, K names a registered type, and the tuple conforms to K's shape. K.σ and K.α are unchanged.

**Weakest precondition of the shape-gated emit.** We take the postcondition `(a, F, G) ∈ A_K^{Σ'}` — the emitted tuple lands in the *active* subset of its type at the post-state — and reason backward, refining ASN-0086's Case-2 wp.

ASN-0086 (wp Case 2) gives, for the ungated `Emit_K` over `→*`-reachable Σ, with fresh address `a = a_emit(Σ, d)`:

`wp(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) ≡ d ∈ dom(Σ.M) ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G)) ∧ ¬(∃ (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∈ coverage(G'))`.

The three inherited conjuncts read: the home is an allocated document; the emit is not a self-nullifying retraction (the `K ≁ R` escape); and no pre-existing retraction tuple already covers the fresh address. `K.λ_sh` adds three preconditions to `K.λ` — (0) arity 3, (i) K registered, (ii) `Sh-conf(K, F, G)` — while leaving the C/M/L effect and the fresh address `a_emit(Σ, d)` identical (the projection argument below: a `K.λ_sh`-step acts on C/M/L exactly as `K.λ`). The gated emit therefore deposits `(F, G, K)` at `a_emit(Σ, d)` under precisely ASN-0086's post-state map, but is *enabled* on a strictly smaller guard. For a guarded operation `g → S`, `wp(g → S, R) ≡ g ∧ wp(S, R)` when the postcondition requires the operation to fire — and the active-subset postcondition is unattainable if the emit does not fire, since then the tuple is never deposited and `(a, F, G) ∉ A_K^{Σ'}`. With added guard `g_sh ≡ K registered ∧ Sh-conf(K, F, G)` and `wp(S, R)` ASN-0086's Case-2 right-hand side (the arity guard (0) is omitted from `g_sh` because the postcondition already forces it: `A_K^{Σ'}` is defined over the arity-3 slice `|Σ.L(a)| = 3` of ASN-0086, so `(a, F, G) ∈ A_K^{Σ'}` is unattainable for any non-triple emit):

`wp(Emit under →_sh, (a, F, G) ∈ A_K^{Σ'})`
`≡ {g → S guard conjunction}`
`K registered ∧ Sh-conf(K, F, G) ∧ d ∈ dom(Σ.M) ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G)) ∧ ¬(∃ (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∈ coverage(G'))`.

The first two conjuncts are this note's contribution; the remaining three are inherited verbatim. The conjunction is read under the domain-discharge ordering (The shape-gated emit).

This weakest precondition is *strictly stronger* than `K.λ_sh`'s own precondition — and the gap is exactly the two inherited ASN-0086 landing conjuncts. `K.λ_sh`'s precondition is `K.λ`'s enablement precondition (L3 and `d ∈ dom(Σ.M)`) conjoined with the three added guards (0), (i), (ii); it contains neither `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))` nor `¬(∃ (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∈ coverage(G'))`. Those two are not enablement conditions but *landing* conditions — what the post-state must additionally satisfy for the deposited tuple to reach the *active* subset rather than merely the audit slice `L_K^{Σ'}`. The gate (`g_sh ≡ K registered ∧ Sh-conf(K, F, G)`, together with the inherited L3 and `d ∈ dom(Σ.M)`) *enables* the emit and is what P4 rests on; but a legal `→_sh` emit may still fail to land active when an inherited landing conjunct is false — the born-nullified case (demonstrated in Worked illustration).

That third inherited conjunct stays live under `→_sh`: because R is gated by Binary alone (Single-source), `→_sh` admits non-unit retraction to-spans whose coverage can include a fresh address — the mechanism Worked illustration exploits.

We bridge to ASN-0086 through the projection `π(Σ) = (Σ.C, Σ.M, Σ.L)` that forgets the registry — call this **the projection bridge**. Each `→_sh`-step preserves the registry in its frame (Registry permanence) and acts on the C/M/L components exactly as the corresponding ASN-0086 step: a K.σ-step as `K.σ`, a K.α-step as `K.α`, and a `K.λ_sh`-step as a `K.λ` step — its three added preconditions (0), (i), (ii) only *restrict* when it fires, leaving its C/M/L effect and frame identical to `K.λ`'s. Hence whenever `Σ →_sh Σ'`, we have `π(Σ) → π(Σ')` in ASN-0086's relation. By induction on derivation length, `π` maps every `→_sh*`-reachable state to a state `→*`-reachable from ASN-0086's initial state: the framework constructs its `Σ_init` by adjoining the registry to ASN-0086's initial three components and altering none of them, so `π(Σ_init) = Σ_init^{0086}` exactly — the base is ASN-0086's own initial state, trivially `→*`-reachable from itself — and each step extends a `→`-derivation rooted at `Σ_init^{0086}` by the projected step just exhibited. The bridge has two consequences. First, `a_emit` reads only the M and L components, which Σ and `π(Σ)` share, so `a_emit(π(Σ), d) = a_emit(Σ, d)` and `dom(π(Σ).L) = dom(Σ.L)`. Second, ASN-0086's structural lemmas — R0 (fresh-address emission), `a_emit` totality, L-ContiguousPrefix, PrefixSpanCoverage — are quantified over `→*`-reachable three-component states, so they hold at `π(Σ)` for every state Σ this note reasons about; since they constrain only the shared C/M/L components, their conclusions transfer to Σ directly.

**Gate realizability — the liveness dual of P4.** Dual to P4's safety half, P6 asserts that every conforming triple at an allocated home actually fires a `→_sh`-step.

**P6 (GateRealizability).** For any `→_sh`-reachable Σ, any `d ∈ dom(Σ.M)`, any registered K, and any `F, G ∈ Endset` with `Sh-conf(K, F, G) = ⊤`, there exists Σ' with `Σ →_sh Σ'` depositing the standard triple `(F, G, K)` at the fresh address `a = a_emit(Σ, d)`:

`a ∉ dom(Σ.L) ∧ a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K) ∧ home(a) = d`,

with Σ' itself `→_sh`-reachable.

*Proof.* The premises are exactly `Emit_K`'s hypotheses at the projected state, the gate conditions hold for a conforming triple by inspection, and the only real work is lifting `Emit_K`'s ungated `K.λ` step — fired at the pinned address `a_emit` — back to a gated `K.λ_sh` step.

First, `K ∈ T_admissible`. K is registered, so by C0 the registry stores a finite representative endset `K_j ∈ T_admissible` of K's coverage class — and "K registered" means `coverage(K) = coverage(K_j)`. The non-emptiness must be carried from `K_j` to the emitted `K`, since the type slot of the emitted triple is `K`, not the stored representative: `K_j ∈ T_admissible` is non-empty, and every span has length `ℓ > 0`, so `coverage(K_j) ≠ ∅`; hence `coverage(K) = coverage(K_j) ≠ ∅`, so `K ≠ ∅`, i.e. `K ∈ T_admissible`. The emitted type slot is therefore non-empty — discharging both `Emit_K`'s `K ∈ T_admissible` precondition and L3's non-empty-type-slot clause. With `F, G ∈ Endset`, the standard triple `(F, G, K)` discharges L3 directly through R0's value-shape consequence — arity 3, both content slots in `Endset`.

Second, apply ASN-0086's `Emit_K` operation at `π(Σ)`, whose contract pins the fresh address to `a = a_emit(Σ, d)` — the address P6 names. By the projection bridge, `π(Σ)` is `→*`-reachable, so `Emit_K` is applicable. `Emit_K(π(Σ), d, F, G)` — with `d ∈ dom(Σ.M) = dom(π(Σ).M)` and `K ∈ T_admissible` (above) — invokes a `K.λ` step at home `d`, depositing `(F, G, K)`, and pins its fresh address to `a = a_emit(π(Σ), d)` by the operation's contract; it returns `(Σ_{0086}, a)` with `a ∉ dom(π(Σ).L)`, `a ∈ dom(Σ_{0086}.L)`, `home(a) = d`, `Σ_{0086}.L(a) = (F, G, K)`. The projection bridge gives `a_emit(π(Σ), d) = a_emit(Σ, d)` — the address P6 names — and `dom(π(Σ).L) = dom(Σ.L)`, so `a ∉ dom(Σ.L)`.

Third, lift the step. The underlying ASN-0086 step is the `K.λ` step that `Emit_K` realizes at the pinned address `a_emit(Σ, d)`. Form Σ' by adjoining the unchanged registry to `Σ_{0086}`: `Σ'.C = Σ_{0086}.C`, `Σ'.M = Σ_{0086}.M`, `Σ'.L = Σ_{0086}.L`, `Σ'.registry = Σ.registry`. We verify `Σ → Σ'` is a `K.λ_sh`-step. `K.λ_sh` is `K.λ` with the registry framed and three added preconditions; its C/M/L effect is `K.λ`'s, realized by the `Emit_K` step at `a_emit`, and its registry frame `Σ'.registry = Σ.registry` holds by construction. Its preconditions: the inherited L3 and `d ∈ dom(Σ.M)` hold (discharged above and by premise); (0) arity 3 holds — the value is the standard triple `(F, G, K)`; (i) K registered — premise; (ii) `Sh-conf(K, F, G) = ⊤` — premise. All hold, so `Σ → Σ'` is a `K.λ_sh`-step, hence a `→_sh`-step, and Σ' is `→_sh`-reachable. Its post-state map gives `a ∈ dom(Σ'.L)`, `Σ'.L(a) = (F, G, K)`, `home(a) = d`, completing the claim. ∎

P6 lands the tuple in the *audit slice* `dom(Σ'.L)` (equivalently `L_K^{Σ'}`), not necessarily the active subset `A_K^{Σ'}` (gate-vs-landing, The shape-gated emit).

## Registry permanence

ASN-0043/0086 carry substrate state `Σ = (Σ.C, Σ.M, Σ.L)`. This framework extends that tuple with a fourth, immutable component:

`Σ = (Σ.C, Σ.M, Σ.L, Σ.registry)`

The registry is fixed when `Σ_init` is defined. To show it never drifts we must reconcile it with the transition relation rather than merely assert permanence. ASN-0086's relation is `→ ≡ K.σ ∪ K.α ∪ K.λ`, refined here to `→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh` (the shape-gating touches only K.λ's precondition, not its frame). A K.σ-step extends `dom(Σ.M)`, a K.α-step extends `dom(Σ.C)`, and a K.λ_sh-step extends `dom(Σ.L)`, each leaving the other two stores framed. We extend every step's frame condition with the registry as an additional framed component:

- K.σ: `Σ'.C = Σ.C`, `Σ'.L = Σ.L`, `Σ'.registry = Σ.registry`;
- K.α: `Σ'.M = Σ.M`, `Σ'.L = Σ.L`, `Σ'.registry = Σ.registry`;
- K.λ_sh: `Σ'.C = Σ.C`, `Σ'.M = Σ.M`, `Σ'.registry = Σ.registry`.

No step kind in `→_sh` has the registry in its *effect*; each leaves it in its frame. P1 then follows by induction on the length of a `→_sh*`-derivation: the base case `Σ = Σ_init` is immediate, and each step preserves `Σ.registry = Σ_init.registry` by the frame condition for whichever of the three kinds it is. So for every Σ reachable from Σ_init, `Σ.registry = Σ_init.registry`.

This invariance has structural consequences. A type K's shape is a function of K alone — `shape(K)` depends only on the P1-invariant registry, hence is constant on `→_sh*` (P2), and the same K cannot carry one shape at Σ and another at Σ'. `Sh-conf` is therefore stable on registered types: for registered K it reads only `(F, G)` and `shape(K)`, and since `shape(K)` is registry-determined and the registry is invariant, `Sh-conf(K, F, G)` evaluates the same against Σ as against any Σ' reachable from Σ. Moreover registration status is itself state-independent by P1 — K is registered at Σ iff registered at Σ' — so the predicate is *defined* at Σ exactly when it is defined at Σ' (P5).

Distinct registries yield distinct substrates: the registry is not state the substrate evolves through but a parameter that individuates which substrate one is in.

## Registration entries

Registration is keyed by *coverage class*, not by raw endset. ASN-0086's TypeEquivalence (lifting L8, ASN-0043) identifies type endsets by coverage — `K ~ K' ≡ coverage(K) = coverage(K')` — and treats the type subscript as a coverage-class index, so `L_K = L_{K'}` whenever `K ~ K'`. The registry honours this: the key of an entry is the coverage class `[K]`, equivalently, the registry assigns `~`-equal endsets one and the same entry. Two coverage-equal endsets therefore cannot carry different shapes or idem flags. The coverage class `[K_j]` is keyed concretely by storing any finite member endset `K_j ∈ T_admissible` of that class (C0), against which coverage equality is decidable (CoverageEqualityDecidable, ASN-0086). Each registry entry thus records such a representative endset `K_j` (denoting the coverage class `[K_j]`) together with:

- a **name** — an opaque string identifier
- a **shape** — one of `Unary`, `Binary`, `Multi`
- a reserved **idem** field — value in `{⊤, ⊥}`, fixed at `Σ_init` and frozen by P1; no predicate, gate, or operation in this note reads it, and its semantics are deferred to Open Question 1.

Because lookup is by coverage class, `shape` and `Sh-conf` respect `~`: for `K ~ K'`, `shape(K) = shape(K')` and `Sh-conf(K, F, G) = Sh-conf(K', F, G)` (the predicate reads `shape(K)`, which is now a function of `[K]`). This is what makes `shape(·)` a function of the type-as-coverage-class rather than of an arbitrary endset representative — the well-definedness P2 asserts.

A registry is well-formed when shape values lie in `{Unary, Binary, Multi}`, idem values lie in `{⊤, ⊥}`, names are unique within the registry, and — the condition P2 well-definedness actually rests on — *coverage-class keys are unique*: no two entries have `~`-equal keys. Equivalently, a well-formed registry *is* a partial function `T_admissible/~ ⇀ (name, shape, idem)` from coverage classes to entries. This is the load-bearing condition; name-uniqueness is by contrast a convenience for app-side lookup. The substrate makes no commitment about which name strings are admissible — that is the app's namespace. Distinct substrates may carry registries with overlapping names; within one substrate, the name uniquely identifies a registry entry.

C0 constrains `Σ_init.registry` directly, since P1 freezes ill-formed registries as faithfully as well-formed ones.

**C0 (RegistryWellFormedness).** `Σ_init.registry` is well-formed — i.e. it *is* a *finite* partial function `T_admissible/~ ⇀ (name, shape, idem)` with `|Σ_init.registry| < ∞`, realized concretely by storing, for each entry, a *finite representative endset* `K_j ∈ T_admissible` of its coverage class together with `(name, shape, idem)`. Coverage-class keys are unique — no two stored representatives are `~`-equal — so lookup by `[K]`, decided by comparing `coverage(K)` against each stored `coverage(K_j)`, returns at most one entry.

The finiteness conjunct `|Σ_init.registry| < ∞` parallels L-fin (LinkStoreFiniteness, ASN-0043): like the link store, the catalog of registered types is a finite object. Precondition (i) of `K.λ_sh` requires deciding whether the emitted `[K]` is a registered key. By P1 the registry never grows, so by C0 it has finitely many keys at *every* reachable state; deciding (i) is then deciding `coverage(K) = coverage(K_j)` against each of the finitely many stored representative endsets `K_j` (C0), and each such test is decidable by CoverageEqualityDecidable (ASN-0086) because it operates on the endsets `K`, `K_j` directly. Finiteness bounds the number of comparisons and CoverageEqualityDecidable discharges each one, so (i) — and hence the whole gate — is a terminating, applicable-at-every-emit check.

## Properties established

This note establishes the following structural properties of every substrate satisfying its commitments:

**P1 (RegistryInvariance).** `Σ.registry = Σ_init.registry` for every Σ reachable from Σ_init. *Derived* (Registry permanence) from the registry's presence in the frame of every `→_sh`-step kind, by induction on derivation length.

**P2 (ShapeStability).** For every registered K, `shape(K)` depends only on the P1-invariant registry, hence is constant on `→_sh*`. *Derived* from C0 (RegistryWellFormedness, Registration entries) for single-valuedness and P1 (RegistryInvariance, Registry permanence) for state-independence. The same argument applies to the reserved `idem` field — being a registry component, it too is frozen by P1 — though no claim in this note depends on that.

**P4 (Sh-confWellFormedness).** No `→_sh`-step extends `dom(Σ.L)` with a tuple `(F, G, K)` whose K is unregistered, nor with one for which `Sh-conf(K, F, G)` fails. *Derived in The shape-gated emit*: the only store-of-links step is `K.λ_sh`, whose preconditions (0)–(ii) reject every such tuple at the gate.

**P5 (Sh-confStateIndependence).** For any *registered* K and any F, G, and any reachable Σ, Σ', `Sh-conf(K, F, G)` is defined at both states and its verdict at Σ equals its verdict at Σ'. *Derived* (Registry permanence): definedness coincides because registration status is P1-invariant, and the verdict coincides because `Sh-conf` consults only the P1-invariant registry (Shape-conformance), reading the registered `shape(K)` and the tuple's own span counts.

**P6 (GateRealizability).** Every conforming triple at an allocated home fires a `→_sh`-step depositing it at the fresh `a_emit(Σ, d)`. The *liveness* dual of P4. *Derived in The shape-gated emit* (Gate realizability), where the full statement and the audit-slice qualification are given.

**P7 (ReachableConformance).** For every `→_sh*`-reachable Σ and every `a ∈ dom(Σ.L)`, the stored tuple `Σ.L(a) = (F, G, K)` has K registered and `Sh-conf(K, F, G) = ⊤`. This is the state-level closure of P4's single-step half — the guarantee a consuming app relies on. *Derived* by induction on derivation length: the base `Σ_init.L = ∅` (Single-source) holds vacuously; each `→_sh`-step either leaves `dom(Σ.L)` unchanged (K.σ, K.α) or extends it by one tuple that P4 forces to be registered and conforming, while every pre-existing tuple persists unchanged by L12 (LinkImmutability, ASN-0043) — applicable through the projection bridge (The shape-gated emit): each `→_sh`-step projects to a `→`-step on which L12 holds, and the L-component is shared (`Σ.L = π(Σ).L`) — preserving the hypothesis.

## Worked illustration

We fix concrete addresses to check P4 and P5 against a real scenario. Let the content subspace be `s_C = 1` and the link subspace `s_L = 2`. Take a document with prefix `d = 1.1.0.1.0.1` (node `1.1`, user `1`, document `1`; `zeros(d) = 2`). Its content occupies subspace 1:

- `c₁ = 1.1.0.1.0.1.0.1.1`
- `c₂ = 1.1.0.1.0.1.0.1.2`
- `c₃ = 1.1.0.1.0.1.0.1.3`

each an element-level I-address with `zeros = 3`. Write `[x] = {(x, δ(1, #x))}` for the unit-depth singleton endset at `x` — a one-span endset, so `|[x]| = 1` whatever `coverage([x])` turns out to be (here `coverage([x]) = {t : x ≼ t}`, by PrefixSpanCoverage).

Consider five registry entries:

- `approved`: Unary
- `succession`: Binary
- `citation`: Multi
- `touched`: Multi
- `retract`: Binary — the framework's retraction type R (the attributed Binary re-expression of ASN-0086's Nullify)

**Unary.** Emit `(F, G, approved)` with `F = [c₁]`, `G = ∅`. Then `|F| = 1` and `|G| = 0`, so `Sh-conf(approved, [c₁], ∅) = ⊤` and `K.λ_sh` is enabled. The variant `([c₁], [c₂], approved)` has `|G| = 1 ≠ 0`, so `Sh-conf = ⊥`; no `→_sh`-step deposits it into `dom(Σ.L)` at any reachable state (P4).

**Binary.** Emit `(F, G, succession)` with `F = [c₂]`, `G = [c₁]` — "`c₂` supersedes `c₁`." Each endset carries one span, so `|F| = |G| = 1` and `Sh-conf(succession, [c₂], [c₁]) = ⊤`. The two-target variant `G = [c₁] ∪ [c₃]` has `|G| = 2`, failing Binary's `|G| = 1`.

**Multi.** Emit `(F, G, citation)` with `F = [c₁]`, `G = [c₂] ∪ [c₃]` — one source citing two targets. `|F| = 1` and `|G| = 2 < ∞`, so `Sh-conf(citation, [c₁], [c₂] ∪ [c₃]) = ⊤`. (Each of `[c₂]`, `[c₃]` covers a subtree; the span *count* is 2, which is what Multi reads.)

**State-independence (P5), with ghosts.** Take two reachable states: `Σ`, in which only `c₁` has been stored, so `c₂, c₃ ∉ dom(Σ.C)` — they are ghost addresses; and `Σ'`, reachable from `Σ`, in which `c₂, c₃` have since been stored. The citation emit above references `c₂, c₃`. Evaluate `Sh-conf(citation, [c₁], [c₂] ∪ [c₃])` at each: the predicate inspects only the span counts `|F| = 1`, `|G| = 2` and `citation`'s registered shape `Multi`, consulting no state-indexed set (Shape-conformance). It returns `⊤` at both `Σ` and `Σ'`, identically. Because the predicate consults no state-indexed set, the citation is emittable at `Σ` exactly as at `Σ'`, and its ghost targets are admissible (L4/L9). This is the concrete content of both P5 and the no-residence-check decision.

**Born nullified (gate fires, tuple lands inactive).** The wp analysis in The shape-gated emit isolates a subtle separation: a gate-enabled emit — (0), (i), (ii) all hold — may still fail the *active-subset* postcondition `(a, F, G) ∈ A_K^{Σ'}` when an inherited ASN-0086 landing conjunct is false. We exhibit a concrete witness, exercising precisely the case the gate does not catch. Link addresses homed at `d` are enumerated `ℓ₁ = 1.1.0.1.0.1.0.2.1`, `ℓ₂ = 1.1.0.1.0.1.0.2.2`, then by sibling advance (`a_emit = inc(ℓ_prev, 0)`). Begin at a state `Σ₀` reachable from `Σ_init` in which two citation links already occupy `ℓ₁, ℓ₂` (so `dom(Σ₀.L) = {ℓ₁, ℓ₂}` homed at `d`).

*Step 1 — emit a Binary R-tuple with a non-unit G.* Using the generic gated `Emit_R` (not the unit-depth wrapper of Single-source, which could not supply a range G), issue `Emit_R(Σ₀, d, [c₁], G_rng)` with attributing source `[c₁]` (`|F| = 1`) and a *single* range span `G_rng = {(g, δ(3, #g))}` where `g = 1.1.0.1.0.1.0.2.4`; so `|G_rng| = 1` and `coverage(G_rng) = {t : 1.1.0.1.0.1.0.2.4 ≤ t < 1.1.0.1.0.1.0.2.7}`, a contiguous range of three link siblings and their subtrees. The gate fires: (0) the value `([c₁], G_rng, retract)` is a triple; (i) `retract` is registered; (ii) `Sh-conf(retract, [c₁], G_rng) = ⊤` since `retract` is Binary and `|F| = |G_rng| = 1`. This exercises the gap noted in Single-source: the gate admits the non-unit Binary `G_rng`. The tuple deposits at the fresh `a_R = a_emit(Σ₀, d) = inc(ℓ₂, 0) = 1.1.0.1.0.1.0.2.3`. Note `a_R ∉ coverage(G_rng)` (`...2.3 < ...2.4`), so even this retraction lands active — it does not nullify itself. Call the post-state `Σ₁`; now `L_retract^{Σ₁} = {(a_R, [c₁], G_rng)}`.

*Step 2 — emit a conforming non-R tuple into the covered range.* Issue `Emit_citation(Σ₁, d, [c₁], [c₂] ∪ [c₃])`. The fresh address is `a = a_emit(Σ₁, d) = inc(a_R, 0) = 1.1.0.1.0.1.0.2.4 = g`. The gate fires again — (0) triple; (i) `citation` registered; (ii) `Sh-conf(citation, [c₁], [c₂] ∪ [c₃]) = ⊤` (`|F| = 1`, `|G| = 2 < ∞`, Multi). So this is a legal `→_sh`-step and the tuple enters the audit slice `L_citation^{Σ₂}`.

*The landing fails.* Yet `(a, [c₁], [c₂] ∪ [c₃]) ∉ A_citation^{Σ₂}`. Trace the inherited wp third conjunct `¬(∃ (b, F', G') ∈ L_R^{Σ₁} :: a_emit(Σ₁, d) ∈ coverage(G'))`: the retraction tuple `(a_R, [c₁], G_rng) ∈ L_R^{Σ₁}` has `a = g ∈ coverage(G_rng)` (since `g` is the lower endpoint of the half-open range), so the existential holds and the conjunct is *false*. By ASN-0086's `nullified`/`A_K` machinery the citation is born nullified: `a ∈ nullified(Σ₂)`, hence `(a, [c₁], [c₂] ∪ [c₃]) ∉ A_citation^{Σ₂}`. The gate did not reject this call — all of (0), (i), (ii) held — the wp's inherited third conjunct did. This demonstrates The shape-gated emit's gate-vs-landing separation.

## Open questions

The following are deliberately left for the successor note that layers operational semantics on top of this framework:

1. **Idem semantics at emit.** What does the substrate do when an app emits a tuple that is "the same as" an active tuple of the same type with `idem=⊤`? What counts as "the same" — `(F, G, K)` values only, or does proposer or emission time enter? How does this interact with nullification, with versioning cascade, and with concurrent emits?

2. **Behavior catalog.** Which substrate-provided behaviors (read-filter, transitive-closure, typed-reverse-lookup, age-staleness, and others not yet named) compose with which shapes, and what predicates does each unlock?

3. **Default predicates.** What predicates does every registered type receive by virtue of its shape and idem flag, independent of any behavior?

4. **Standard registrations.** Does the substrate ship any types pre-registered — `retired` (Unary, idem=⊤, read-filter), `supersedes` (Binary, idem=⊤, transitive-closure), and the retraction type `R` (Binary) are candidates the lattice already uses universally — or is each substrate's `Σ_init.registry` composed entirely of app-declared entries?

5. **Predicate composition.** Composition rules over the atomic predicates each type receives — the predicate-composition territory left open here.

6. **Extension beyond F=1 and N=3.** When an app eventually needs multi-source relations or richer arity, whether the path is a supplemental note that loosens the constraints here, a parallel framework, or direct link-store interaction.

Each of these can be resolved without revisiting the structural commitments above.
