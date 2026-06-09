# ASN-0126: Substrate Shape Framework

*Narrowing the typed-relation framework into a concrete vocabulary apps register against*

ASN-0086 commits the substrate to typed relations of arity three over `(F, G, K)` and provides the operational vocabulary `Emit_K`, `Observe`, `Nullify`. It does not narrow the cardinalities of the F and G slots, nor does it say anything about what an app must look like when it registers a type. Apps interacting with the substrate need more than ASN-0086 gives: a finite shape catalog their types are checked against, a static shape-conformance check the substrate can apply at every emit, and a registry whose contents do not drift across states. This note supplies that — and only that.

The lattice's actual usage is uniformly single-source. The right level of commitment is concrete shapes the substrate can statically check, with everything operational layered on top.

## Single-source

Every typed relation *the framework gates* — every registered type emitted under `→_sh` — has a single-span source — `|F| = 1`, where for an endset `e` we write `|e|` for its *span count*: the number of spans `e` contains, **not** the number of tumblers in `coverage(e)`. This is a commitment about what the framework admits, not about the link store underneath: a tuple filed directly into the link store (ASN-0043) may carry `|F| > 1`. The substrate narrows away only the multi-span, discontiguous from-set that the full link store (ASN-0043) would permit; it does not narrow what one span may reach — the one F span may itself cover a contiguous range or a whole subtree, not merely one address, as Nelson confirms: "a single source span [may] legitimately cover a range/subtree ... the single-address case is just the smallest (degenerate) instance."

The one place this commitment bites against ASN-0086's own vocabulary is retraction. ASN-0086 defines `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` — an *empty* from-set, with the target carried in G. Under `|F| = 1` that empty form fails every shape, so ASN-0086's literal `F = ∅` Nullify has **no** `→_sh` image. This is a genuine, narrow loss of expressiveness, and we state it as such rather than as a faithful carry-over.

What is *not* lost is attribution. In Nelson's design the responsible party for a link rides on a separate, always-present channel — the link's home document, which "indicates who owns it, and not what it points to" — while the from-set records only what the link derives *from*, never who performs it. ASN-0086's `F = ∅` is therefore an *empty derivation slot*, not an unattributed operation; a retraction filed with `F = ∅` is still owned by, and attributed to, its home document `d_retr`. We do not introduce a distinct unattributed-retraction operator, because — Nelson is explicit — a link with no responsible party is not a coherent object.

So the framework supplies the from-slot rather than leaving it empty or open. The retraction wrapper is `Emit_R(Σ, d_retr, [r], {(a, δ(1, #a))})`: a one-span attributing source (`|F| = 1`) and the single target as one unit-depth to-span in G (`|G| = 1`). When the app has a genuine derivation source it supplies that span; for the case ASN-0086 wrote as `F = ∅` — no derivation source — the canonical fill is the home document's own unit-depth span, `r = (d_retr, δ(1, #d_retr))`, which names exactly the owning party ASN-0086's home channel already carries. The from-slot is thus never an unbound parameter: it is either the app's derivation span or this canonical home-document span. This shape — `|F| = 1`, `|G| = 1` — is exactly **Binary**, so R is registered Binary. Because the target remains in G as that single span, ASN-0086's `nullified`/`L_R`/active-subset machinery, all of which read `coverage(G')` and ignore F, carry over unchanged; what changes is only the from-slot, which moves from the inexpressible `∅` to a one-span attribution — the app's source, or canonically the home document.

Binary registration does **not** by itself entail ASN-0086's UnitDepthRetractionDiscipline: a single G-span of non-unit length — say `(t, δ(2, #t))`, covering a contiguous multi-address range — is equally Binary-conformant, so Binary is strictly weaker than the discipline's unit-depth requirement. Consequently `→_sh` does **not** guarantee unit-depth, and it does **not** guarantee R-Scope's single-tuple-scope result `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` — that result needs `coverage(G) = {t : a ≼ t}`, which a non-unit Binary G exceeds. Both are *additional operational disciplines*, not framework guarantees: they hold only when the app routes every retraction through the unit-depth wrapper `Emit_R(Σ, d_retr, [r], {(a, δ(1, #a))})`, which writes the canonical `{(a, δ(1, #a))}` to-span by construction. `→_sh` itself does not mandate that wrapper — it gates R by Binary alone — so an app that invokes the generic gated emit at R with a non-unit range produces a legal `→_sh` retraction that withdraws a whole contiguous region at once. Only *discontiguous* multi-target retraction falls to the front end.

We settle the relationship to the underlying link store explicitly: `→_sh` is the *complete* transition relation of a framework-governed substrate — every emit it admits is a `K.λ_sh`-step through the gate. The "only conforming tuples" conclusion below is inductive, so it needs a base case the gate cannot supply: we commit that the framework's base state carries an empty link store, `Σ_init.L = ∅` (inherited from ASN-0086's base state). With that base discharged, induction over `→_sh`-steps gives that within such a substrate `dom(Σ.L)` carries only conforming tuples and there is no off-gate path into the link store. (This is what licenses the intro's "at every emit": every emit of a framework substrate is a `→_sh`-step.) An app needing multi-source relations drops to a *different* substrate — ASN-0086's ungated `→`, whose `K.λ` admits arbitrary arity directly.

## Three shapes by G span count

With F fixed at one span, the framework varies only by what G can hold. We measure G by its *span count* `|G|` (Single-source). Three shapes capture every usage observed in the lattice:

| Shape  | G span count   | What it expresses                                              |
|--------|----------------|-----------------------------------------------------------------|
| Unary  | `\|G\| = 0` (G = ∅) | A predicate or marker on a single source                    |
| Binary | `\|G\| = 1`      | A directed relation to one target span                          |
| Multi  | `\|G\|` finite   | A single source connected to finitely many target spans         |

These conditions do **not** partition the space of expressible tuples: Unary (`|G| = 0`) and Binary (`|G| = 1`) are mutually exclusive, but Multi subsumes both (Shape-conformance). The shapes therefore classify *registrations*, not tuples: a type K is registered once with one shape, and that shape fixes which tuples are well-formed under K.

The framework constrains the *span count* per shape, never the residence of the addresses those spans cover (Shape-conformance).

## Shape-conformance

The shapes are stated in terms of the *span count* `|e|` of an endset (Single-source). F and G are endsets, and `Endset = 𝒫_fin(Span)` (ASN-0043) — a finite set of spans, so `|e|` is its cardinality as that set. The span-count and coverage measures diverge sharply. A single unit-depth span `(a, δ(1, #a))` is one span — `|{(a, δ(1, #a))}| = 1` — yet its coverage is `{t : a ≼ t}`, generally infinite (PrefixSpanCoverage, ASN-0043). We count spans, deliberately, rather than coverage, because a coverage-singleton measure `|coverage(F)| = 1` is unsatisfiable. Every non-empty span `(s, ℓ)` denotes the half-open interval `{t ∈ T : s ≤ t < s ⊕ ℓ}`, which is infinite: by T0(b) (UnboundedLength, ASN-0034) `s` admits unboundedly many proper extensions, each agreeing with `s` through the action point of `ℓ` and so lying below `s ⊕ ℓ` by T1 (LexicographicOrder, ASN-0034), hence in the interval. Over `T` *no* endset therefore has singleton coverage, so a `|coverage(F)| = 1` discipline would admit nothing; span-count is the only measure that both captures single-source and is satisfiable.

One edge follows from counting spans rather than coverage. Types are keyed by *coverage class* (Registration entries) — coverage-invariant — but F-conformance counts spans, a coverage-variant notion. So a source presenting one contiguous extent as two abutting spans `(a, ℓ₁)`, `(a ⊕ ℓ₁, ℓ₂)` has `|F| = 2` and fails every shape, even though its coverage equals that of the conformant one-span F. The rule is on the side of the literal emission: **a single-span slot means a single span as emitted**, and coalescing abutting spans to that canonical form before emit is the app's responsibility wherever a shape constrains a slot to one span — F under every shape, G under Binary — not the substrate's at the gate (udanax-green performs no endset coalescing, `spanf1.c`). (Genuinely discontiguous multi-span F — a gap between spans, hence a *different* coverage — is rejected on its own merits as the multi-source case the substrate does not provide; see Single-source.) Counting spans-as-emitted keeps the measure intrinsic to the value and thus state-independent (P5).

The predicate `Sh-conf(K, F, G)` is defined only for *registered* K — those for which the registry records a shape. For an unregistered K, `shape(K)` does not exist and `Sh-conf(K, F, G)` carries no truth value; emits under such K are inadmissible by the registration precondition on `K.λ_sh` (below), never reaching the conformance test. For a typed tuple `(F, G, K)` under a type K registered with shape s, `Sh-conf(K, F, G)` holds when:

- Unary: `|F| = 1` and `G = ∅` (equivalently `|G| = 0`);
- Binary: `|F| = 1` and `|G| = 1`;
- Multi: `|F| = 1` and `|G| < ∞`.

For Multi the conjunct `|G| < ∞` holds for *every* endset by `Endset = 𝒫_fin(Span)`, so Multi places no real bound on G's span count — it is the unrestricted, permissive shape, constraining only F.

`Sh-conf` consults nothing about content residence. Endset spans may reference any address, including ghost addresses at which nothing is stored: L4 and L9 (ASN-0043) permit this, Nelson is explicit that "endset addresses do NOT need to resolve to stored content" — the type endset especially "is designed to exploit this" — and Gregory confirms udanax-green enforces no residence check at link creation. The framework inherits that permission unchanged. In particular `Sh-conf` does not test membership in `dom(Σ.C)`, `dom(Σ.L)`, or any state-indexed address set such as ASN-0086's `A_doc^Σ`, `A_rel^Σ`, `A^Σ`. Were it to, a ghost reference at one state and a stored reference at a later state would yield different verdicts, destroying the state-independence we want (P5).

The predicate therefore depends only on the tuple's span counts `|F|`, `|G|` and the shape recorded for K in the registry — a property of the tuple-plus-registration pair, evaluable identically at any reachable state.

### The shape-gated emit

ASN-0086's K.λ step has precondition L3 only (arity ≥ 3, non-empty type slot); it does not inspect span counts, so the bare `→` of ASN-0086 *admits* shape-non-conforming tuples. This framework **refines** the emit step. Define the framework's transition relation

`→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh`,

where `K.λ_sh` is `K.λ` with three added preconditions: (0) *the emitted value is a standard triple* — arity 3, so it carries exactly the two content slots `(F, G)` that `Sh-conf` reads; (i) *K is registered* — the registry records a shape for K; and (ii) `Sh-conf(K, F, G)`. The three are ordered: (0) and (i) jointly discharge the domain condition for (ii). Precondition (0) is the gate that makes (ii) well-defined: `K.λ` inherited from ASN-0086 admits any arity `N ≥ 3` (its sole arity constraint is L3), but `Sh-conf(K, F, G)` is defined over a standard triple `(F, G, K)` and reads exactly two content slots, so for a higher-arity value `(e₁, e₂, e₃, e₄, K)` it has no defined reading. Rather than give `Sh-conf` an ad-hoc reading on such values, we restrict `→_sh` to arity-3 emits: a value of arity ≠ 3 fails (0) and is simply not a `→_sh`-step. An emit of value `(F, G, K)` is thus a `→_sh`-step only when it is a standard triple, K names a registered type, and the tuple conforms to K's shape. K.σ and K.α are unchanged.

**Weakest precondition of the shape-gated emit.** We take the postcondition `(a, F, G) ∈ A_K^{Σ'}` — the emitted tuple lands in the *active* subset of its type at the post-state — and reason backward, refining ASN-0086's Case-2 wp.

ASN-0086 (wp Case 2) gives, for the ungated `Emit_K` over `→*`-reachable Σ, with fresh address `a = a_emit(Σ, d)`:

`wp(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) ≡ d ∈ dom(Σ.M) ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G)) ∧ ¬(∃ (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∈ coverage(G'))`.

The three inherited conjuncts read: the home is an allocated document; the emit is not a self-nullifying retraction (the `K ≁ R` escape); and no pre-existing retraction tuple already covers the fresh address. `K.λ_sh` adds three preconditions to `K.λ` — (0) arity 3, (i) K registered, (ii) `Sh-conf(K, F, G)` — while leaving the C/M/L effect and the fresh address `a_emit(Σ, d)` identical (the projection argument below: a `K.λ_sh`-step acts on C/M/L exactly as `K.λ`). The gated emit therefore deposits `(F, G, K)` at `a_emit(Σ, d)` under precisely ASN-0086's post-state map, but is *enabled* on a strictly smaller guard. For a guarded operation `g → S`, `wp(g → S, R) ≡ g ∧ wp(S, R)` when the postcondition requires the operation to fire — and the active-subset postcondition is unattainable if the emit does not fire, since then the tuple is never deposited and `(a, F, G) ∉ A_K^{Σ'}`. With added guard `g_sh ≡ K registered ∧ Sh-conf(K, F, G)` and `wp(S, R)` ASN-0086's Case-2 right-hand side (the arity guard (0) is omitted from `g_sh` because the postcondition already forces it: `A_K^{Σ'}` is defined over the arity-3 slice `|Σ.L(a)| = 3` of ASN-0086, so `(a, F, G) ∈ A_K^{Σ'}` is unattainable for any non-triple emit):

`wp(Emit under →_sh, (a, F, G) ∈ A_K^{Σ'})`
`≡ {g → S guard conjunction}`
`K registered ∧ Sh-conf(K, F, G) ∧ d ∈ dom(Σ.M) ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G)) ∧ ¬(∃ (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∈ coverage(G'))`.

The first two conjuncts are this note's contribution; the remaining three are inherited verbatim. Their ordering is load-bearing: `Sh-conf(K, F, G)` carries a truth value only on registered K (Shape-conformance), so `K registered` is the domain-discharging conjunct and the conjunction is read left-to-right, `Sh-conf` evaluated only where defined.

This weakest precondition is *strictly stronger* than `K.λ_sh`'s own precondition — and the gap is exactly the two inherited ASN-0086 landing conjuncts. `K.λ_sh`'s precondition is `K.λ`'s enablement precondition (L3 and `d ∈ dom(Σ.M)`) conjoined with the three added guards (0), (i), (ii); it contains neither `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))` nor `¬(∃ (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∈ coverage(G'))`. Those two are not enablement conditions but *landing* conditions — what the post-state must additionally satisfy for the deposited tuple to reach the *active* subset rather than merely the audit slice `L_K^{Σ'}`. The gate (`g_sh ≡ K registered ∧ Sh-conf(K, F, G)`, together with the inherited L3 and `d ∈ dom(Σ.M)`) *enables* the emit and is what P4 rests on; but a legal `→_sh` emit may still fail to land active when an inherited landing conjunct is false — the born-nullified case, witnessed concretely in the Worked illustration. Such a pre-existing covering tuple is attainable at a general `→_sh`-reachable state, since `→_sh`'s gate enforces only Binary conformance on R, not unit-depth.

*Disciplined-domain simplification (conditional).* The projection `π` (below) places every `→_sh`-reachable state at a `→*`-reachable ASN-0086 state, but **not** at one obeying ASN-0086's unit-depth retraction discipline: `→_sh`'s gate enforces only Binary conformance on R (Single-source), so a general `→_sh`-reachable state may carry an `L_R` tuple with a non-unit (but Binary) range to-span, and the third conjunct's vacuity cannot be imported there. We condition the simplification on ASN-0086's `UnitDepthRetractionDiscipline` — every `L_R` tuple's to-endset has the canonical form `{(t, δ(1, #t))}` — not on layer-reachability, which is too strong: layer-reachability requires every `L_R`-growing step to be an `F = ∅` Nullify, which the framework's *attributed* (`|F| = 1`) retraction leaves at its first emit. The discipline constrains only the to-span shape, agnostic to the from-slot, so a substrate that restricts every retraction emit to the unit-depth to-span form satisfies it while still admitting attributed retractions.

*If* the substrate is so operated — every `L_R` tuple unit-depth — then the third conjunct holds vacuously (the unit-depth discipline with R0a forces `a_emit(Σ, d) ∉ coverage(G')` for every pre-existing retraction tuple), and the wp reduces to `K registered ∧ Sh-conf(K, F, G) ∧ d ∈ dom(Σ.M) ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`, collapsing for a non-retraction conforming emit (`K ≁ R`) to `K registered ∧ Sh-conf(K, F, G) ∧ d ∈ dom(Σ.M)` — the two-conjunct shape gate plus an allocated home. This characterizes what `K.λ_sh` checks only on the unit-depth-disciplined sub-domain; at a general `→_sh`-reachable state the full inherited wp of the preceding paragraph — all three ASN-0086 conjuncts intact — stands.

This note's state carries a fourth component, so `→_sh` is not literally a subrelation of ASN-0086's three-component `→` — the two relate different state types, and "every `→_sh*`-reachable state is `→*`-reachable" cannot be read as a set inclusion between four-tuples and three-tuples. We make the bridge explicit through the projection `π(Σ) = (Σ.C, Σ.M, Σ.L)` that forgets the registry. Each `→_sh`-step preserves the registry in its frame (Registry permanence) and acts on the C/M/L components exactly as the corresponding ASN-0086 step: a K.σ-step as `K.σ`, a K.α-step as `K.α`, and a `K.λ_sh`-step as a `K.λ` step — its three added preconditions (0), (i), (ii) only *restrict* when it fires, leaving its C/M/L effect and frame identical to `K.λ`'s. Hence whenever `Σ →_sh Σ'`, we have `π(Σ) → π(Σ')` in ASN-0086's relation. By induction on derivation length, `π` maps every `→_sh*`-reachable state to a state `→*`-reachable from ASN-0086's initial state: the framework constructs its `Σ_init` by adjoining the registry to ASN-0086's initial three components and altering none of them, so `π(Σ_init) = Σ_init^{0086}` exactly — the base is ASN-0086's own initial state, trivially `→*`-reachable from itself — and each step extends a `→`-derivation rooted at `Σ_init^{0086}` by the projected step just exhibited. ASN-0086's structural lemmas — R0 (fresh-address emission), `a_emit` totality, L-ContiguousPrefix, PrefixSpanCoverage — are quantified over `→*`-reachable three-component states, so they hold at `π(Σ)` for every state Σ this note reasons about; since they constrain only the C/M/L components, which Σ and `π(Σ)` share, their conclusions transfer to Σ directly. All reachability in this note is with respect to `→_sh`, and this projection is what licenses importing those `→`-domain results. Under this definition P4 holds *by construction* of `K.λ_sh`, not as a derived property of the unmodified ASN-0086 relation.

**Gate realizability — the liveness dual of P4.** Dual to P4's safety half, P6 asserts that every conforming triple at an allocated home actually fires a `→_sh`-step.

**P6 (GateRealizability).** For any `→_sh`-reachable Σ, any `d ∈ dom(Σ.M)`, any registered K, and any `F, G ∈ Endset` with `Sh-conf(K, F, G) = ⊤`, there exists Σ' with `Σ →_sh Σ'` depositing the standard triple `(F, G, K)` at the fresh address `a = a_emit(Σ, d)`:

`a ∉ dom(Σ.L) ∧ a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K) ∧ home(a) = d`,

with Σ' itself `→_sh`-reachable.

*Proof.* The premises are exactly `Emit_K`'s hypotheses at the projected state, the gate conditions hold for a conforming triple by inspection, and the only real work is lifting `Emit_K`'s ungated `K.λ` step — fired at the pinned address `a_emit` — back to a gated `K.λ_sh` step.

First, `K ∈ T_admissible`. K is registered, so by C0 the registry stores a finite representative endset `K_j ∈ T_admissible` of K's coverage class — and "K registered" means `coverage(K) = coverage(K_j)`. The non-emptiness must be carried from `K_j` to the emitted `K`, since the type slot of the emitted triple is `K`, not the stored representative: `K_j ∈ T_admissible` is non-empty, and every span has length `ℓ > 0`, so `coverage(K_j) ≠ ∅`; hence `coverage(K) = coverage(K_j) ≠ ∅`, so `K ≠ ∅`, i.e. `K ∈ T_admissible`. The emitted type slot is therefore non-empty — discharging both `Emit_K`'s `K ∈ T_admissible` precondition and L3's non-empty-type-slot clause. With `F, G ∈ Endset`, the standard triple `(F, G, K)` discharges L3 directly through R0's value-shape consequence — arity 3, both content slots in `Endset`.

Second, apply ASN-0086's `Emit_K` operation at `π(Σ)` — not the bare existential R0/`K.λ`-transition. This distinction is the crux of the address claim: R0 delivers merely *some* address fresh against `dom(Σ.L)` and on-chain in `A_L(d)`, and by L-ContiguousPrefix the fresh on-chain addresses are *all* chain indices `j > J_d` — infinitely many — of which `a_emit(Σ, d) = inc(ℓ_prev, 0)` (chain index `J_d + 1`) is only the least; likewise ASN-0086's `K.λ` StateTransition deposits at "a fresh key," not specifically at `a_emit`. It is the `Emit_K` *operation*, whose contract sets "the fresh address is `a = a_emit(Σ, d)`," that pins the address P6 names. By the projection argument above, `π(Σ)` is `→*`-reachable in ASN-0086, so `Emit_K` is applicable. `Emit_K(π(Σ), d, F, G)` — with `d ∈ dom(Σ.M) = dom(π(Σ).M)` and `K ∈ T_admissible` (above) — invokes a `K.λ` step at home `d`, depositing `(F, G, K)`, and pins its fresh address to `a = a_emit(π(Σ), d)` by the operation's contract; it returns `(Σ_{0086}, a)` with `a ∉ dom(π(Σ).L)`, `a ∈ dom(Σ_{0086}.L)`, `home(a) = d`, `Σ_{0086}.L(a) = (F, G, K)`. Since `a_emit` reads only the M and L components, which Σ and `π(Σ)` share, `a_emit(π(Σ), d) = a_emit(Σ, d)` — the address P6 names — and `a ∉ dom(π(Σ).L) = dom(Σ.L)`.

Third, lift the step. The underlying ASN-0086 step is the `K.λ` step that `Emit_K` realizes at the pinned address `a_emit(Σ, d)`. Form Σ' by adjoining the unchanged registry to `Σ_{0086}`: `Σ'.C = Σ_{0086}.C`, `Σ'.M = Σ_{0086}.M`, `Σ'.L = Σ_{0086}.L`, `Σ'.registry = Σ.registry`. We verify `Σ → Σ'` is a `K.λ_sh`-step. `K.λ_sh` is `K.λ` with the registry framed and three added preconditions; its C/M/L effect is `K.λ`'s, realized by the `Emit_K` step at `a_emit`, and its registry frame `Σ'.registry = Σ.registry` holds by construction. Its preconditions: the inherited L3 and `d ∈ dom(Σ.M)` hold (discharged above and by premise); (0) arity 3 holds — the value is the standard triple `(F, G, K)`; (i) K registered — premise; (ii) `Sh-conf(K, F, G) = ⊤` — premise. All hold, so `Σ → Σ'` is a `K.λ_sh`-step, hence a `→_sh`-step, and Σ' is `→_sh`-reachable. Its post-state map gives `a ∈ dom(Σ'.L)`, `Σ'.L(a) = (F, G, K)`, `home(a) = d`, completing the claim. ∎

P6 lands the tuple in the *audit slice* `dom(Σ'.L)` (equivalently `L_K^{Σ'}`), and makes **no** claim about the active subset `A_K^{Σ'}`.

## Registry permanence

ASN-0043/0086 carry substrate state `Σ = (Σ.C, Σ.M, Σ.L)`. This framework extends that tuple with a fourth, immutable component:

`Σ = (Σ.C, Σ.M, Σ.L, Σ.registry)`

The registry is fixed when `Σ_init` is defined. To show it never drifts we must reconcile it with the transition relation rather than merely assert permanence. ASN-0086's relation is `→ ≡ K.σ ∪ K.α ∪ K.λ`, refined here to `→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh` (the shape-gating touches only K.λ's precondition, not its frame). A K.σ-step extends `dom(Σ.M)`, a K.α-step extends `dom(Σ.C)`, and a K.λ_sh-step extends `dom(Σ.L)`, each leaving the other two stores framed. We extend every step's frame condition with the registry as an additional framed component:

- K.σ: `Σ'.C = Σ.C`, `Σ'.L = Σ.L`, `Σ'.registry = Σ.registry`;
- K.α: `Σ'.M = Σ.M`, `Σ'.L = Σ.L`, `Σ'.registry = Σ.registry`;
- K.λ_sh: `Σ'.C = Σ.C`, `Σ'.M = Σ.M`, `Σ'.registry = Σ.registry`.

No step kind in `→_sh` has the registry in its *effect*; each leaves it in its frame. P1 then follows by induction on the length of a `→_sh*`-derivation: the base case `Σ = Σ_init` is immediate, and each step preserves `Σ.registry = Σ_init.registry` by the frame condition for whichever of the three kinds it is. So for every Σ reachable from Σ_init, `Σ.registry = Σ_init.registry`.

This invariance has structural consequences. A type K's shape is a function of K alone — `shape(K)` is well-defined without reference to state (P2), and the same K cannot carry one shape at Σ and another at Σ'. Likewise `idem(K)` is state-independent (P3). `Sh-conf` is therefore stable on registered types: for registered K it reads only `(F, G)` and `shape(K)`, and since `shape(K)` is registry-determined and the registry is invariant, `Sh-conf(K, F, G)` evaluates the same against Σ as against any Σ' reachable from Σ. Moreover registration status is itself state-independent by P1 — K is registered at Σ iff registered at Σ' — so the predicate is *defined* at Σ exactly when it is defined at Σ' (P5).

Distinct registries yield distinct substrates: the registry is not state the substrate evolves through but a parameter that individuates which substrate one is in.

## Registration entries

Registration is keyed by *coverage class*, not by raw endset. ASN-0086's TypeEquivalence (lifting L8, ASN-0043) identifies type endsets by coverage — `K ~ K' ≡ coverage(K) = coverage(K')` — and treats the type subscript as a coverage-class index, so `L_K = L_{K'}` whenever `K ~ K'`. The registry honours this: the key of an entry is the coverage class `[K]`, equivalently, the registry assigns `~`-equal endsets one and the same entry. Two coverage-equal endsets therefore cannot carry different shapes or idem flags. A coverage class is an abstract object — and, by the unsatisfiability argument above, its coverage set is in general infinite, hence not finitely representable — so the registry realizes the key `[K]` concretely by *storing a finite representative endset* `K_j ∈ T_admissible` of that class. The entry's key is the class `[K_j]` it denotes; lookup by an arbitrary `[K]` compares `coverage(K)` against the stored representative `coverage(K_j)` via CoverageEqualityDecidable (ASN-0086), which operates on endsets and so applies directly to the representatives. Each registry entry thus records a representative endset `K_j` (denoting the coverage class `[K_j]`) together with:

- a **name** — an opaque string identifier
- a **shape** — one of `Unary`, `Binary`, `Multi`
- an **idem** flag — `⊤` or `⊥`

Because lookup is by coverage class, `shape`, `idem`, and `Sh-conf` all respect `~`: for `K ~ K'`, `shape(K) = shape(K')`, `idem(K) = idem(K')`, and `Sh-conf(K, F, G) = Sh-conf(K', F, G)` (the predicate reads `shape(K)`, which is now a function of `[K]`). This is what makes `shape(·)` and `idem(·)` functions of the type-as-coverage-class rather than of an arbitrary endset representative — the well-definedness P2 and P3 assert.

The **idem** flag carries no in-note role — `Sh-conf` gates on `shape(K)` alone, and idem's operational semantics are wholly deferred (Open question 1). We provision it here nonetheless, rather than in the successor note that will read it, because the registry is immutable (P1): no field can be added to an entry at runtime, so every field the operational layer will eventually consult must already be present at `Σ_init`. Pre-provisioning idem at construction time — and fixing its stability now (P3) — is precisely what lets a successor layer its idem semantics on a field guaranteed already to exist and never to drift. This does not breach the note's "and only that" scope: idem is a reserved slot with a stability guarantee, not an operational commitment; what the slot *means* is exactly what this note leaves open.

A registry is well-formed when shape values lie in `{Unary, Binary, Multi}`, idem values lie in `{⊤, ⊥}`, names are unique within the registry, and — the condition P2/P3 well-definedness actually rests on — *coverage-class keys are unique*: no two entries have `~`-equal keys. Equivalently, a well-formed registry *is* a partial function `T_admissible/~ ⇀ (name, shape, idem)` from coverage classes to entries. This is the load-bearing condition; name-uniqueness is by contrast a convenience for app-side lookup. The substrate makes no commitment about which name strings are admissible — that is the app's namespace. Distinct substrates may carry registries with overlapping names; within one substrate, the name uniquely identifies a registry entry.

P1 freezes whatever `Σ_init.registry` contains — an ill-formed registry (two `~`-equal keys with differing shapes) exactly as faithfully as a well-formed one — so single-valuedness of `shape(·)` is not a transition property but a separate obligation on `Σ_init` itself, which we raise to an explicit *framework commitment*:

**C0 (RegistryWellFormedness).** `Σ_init.registry` is well-formed — i.e. it *is* a *finite* partial function `T_admissible/~ ⇀ (name, shape, idem)` with `|Σ_init.registry| < ∞`, realized concretely by storing, for each entry, a *finite representative endset* `K_j ∈ T_admissible` of its coverage class together with `(name, shape, idem)`. Coverage-class keys are unique — no two stored representatives are `~`-equal — so lookup by `[K]`, decided by comparing `coverage(K)` against each stored `coverage(K_j)`, returns at most one entry.

The finiteness conjunct `|Σ_init.registry| < ∞` parallels L-fin (LinkStoreFiniteness, ASN-0043): like the link store, the catalog of registered types is a finite object. Precondition (i) of `K.λ_sh` requires deciding whether the emitted `[K]` is a registered key. By P1 the registry never grows, so by C0 it has finitely many keys at *every* reachable state; deciding (i) is then deciding `coverage(K) = coverage(K_j)` against each of the finitely many stored representative endsets `K_j` (C0), and each such test is decidable by CoverageEqualityDecidable (ASN-0086) because it operates on the endsets `K`, `K_j` directly. Finiteness bounds the number of comparisons and CoverageEqualityDecidable discharges each one, so (i) — and hence the whole gate — is a terminating, applicable-at-every-emit check.

## Properties established

This note establishes the following structural properties of every substrate satisfying its commitments:

**P1 (RegistryInvariance).** `Σ.registry = Σ_init.registry` for every Σ reachable from Σ_init. *Derived* (Registry permanence) from the registry's presence in the frame of every `→_sh`-step kind, by induction on derivation length.

**P2 (ShapeStability).** For every registered K, `shape(K)` is well-defined without reference to state, and the value is constant on the reflexive-transitive closure of `→_sh`. *Derived* from C0 (RegistryWellFormedness, Registration entries) for single-valuedness and P1 (RegistryInvariance, Registry permanence) for state-independence.

**P3 (IdemStability).** For every registered K, `idem(K) ∈ {⊤, ⊥}` is a structural property of K, equal at every reachable state. *Corollary of P2*, the same argument applied to the idem field.

**P4 (Sh-confWellFormedness).** No `→_sh`-step extends `dom(Σ.L)` with a tuple `(F, G, K)` whose K is unregistered, nor with one for which `Sh-conf(K, F, G)` fails. *Derived in The shape-gated emit*: the only store-of-links step is `K.λ_sh`, whose preconditions (0)–(ii) reject every such tuple at the gate. P4 records the gate's *enablement* half only.

**P5 (Sh-confStateIndependence).** For any *registered* K and any F, G, and any reachable Σ, Σ', `Sh-conf(K, F, G)` is defined at both states and its verdict at Σ equals its verdict at Σ'. Registration status is itself state-independent: by P1 the registry is the invariant `Σ_init.registry`, so K is registered at Σ iff registered at Σ', and the *definedness* of `Sh-conf(K, F, G)` therefore coincides at the two states. *Derived*: where defined, `Sh-conf` reads only the span counts `|F|`, `|G|` and `shape(K)` and consults no state, per Shape-conformance; the counts are intrinsic to the values, and `shape(K)` is invariant by P1.

**P6 (GateRealizability).** For any `→_sh`-reachable Σ, any `d ∈ dom(Σ.M)`, any registered K, and any `F, G ∈ Endset` with `Sh-conf(K, F, G) = ⊤`, there exists Σ' with `Σ →_sh Σ'` depositing `(F, G, K)` at the fresh `a = a_emit(Σ, d)` (`a ∉ dom(Σ.L)`, `a ∈ dom(Σ'.L)`, `Σ'.L(a) = (F, G, K)`, `home(a) = d`). The *liveness* dual of P4. *Derived in The shape-gated emit* (Gate realizability). P6 lands the tuple in the audit slice `L_K^{Σ'}`, not necessarily the active subset.

## Worked illustration

We fix concrete addresses to check P4 and P5 against a real scenario. Let the content subspace be `s_C = 1` and the link subspace `s_L = 2`. Take a document with prefix `d = 1.1.0.1.0.1` (node `1.1`, user `1`, document `1`; `zeros(d) = 2`). Its content occupies subspace 1:

- `c₁ = 1.1.0.1.0.1.0.1.1`
- `c₂ = 1.1.0.1.0.1.0.1.2`
- `c₃ = 1.1.0.1.0.1.0.1.3`

each an element-level I-address with `zeros = 3`. Write `[x] = {(x, δ(1, #x))}` for the unit-depth singleton endset at `x` — a one-span endset, so `|[x]| = 1` whatever `coverage([x])` turns out to be (here `coverage([x]) = {t : x ≼ t}`, by PrefixSpanCoverage).

Consider five registry entries:

- `approved`: Unary, idem=⊤
- `succession`: Binary, idem=⊤
- `citation`: Multi, idem=⊤
- `touched`: Multi, idem=⊥
- `retract`: Binary, idem=⊤ — the framework's retraction type R (the attributed Binary re-expression of ASN-0086's Nullify)

**Unary.** Emit `(F, G, approved)` with `F = [c₁]`, `G = ∅`. Then `|F| = 1` and `|G| = 0`, so `Sh-conf(approved, [c₁], ∅) = ⊤` and `K.λ_sh` is enabled. The variant `([c₁], [c₂], approved)` has `|G| = 1 ≠ 0`, so `Sh-conf = ⊥`; no `→_sh`-step deposits it into `dom(Σ.L)` at any reachable state (P4).

**Binary.** Emit `(F, G, succession)` with `F = [c₂]`, `G = [c₁]` — "`c₂` supersedes `c₁`." Each endset carries one span, so `|F| = |G| = 1` and `Sh-conf(succession, [c₂], [c₁]) = ⊤`. The two-target variant `G = [c₁] ∪ [c₃]` has `|G| = 2`, failing Binary's `|G| = 1`.

**Multi.** Emit `(F, G, citation)` with `F = [c₁]`, `G = [c₂] ∪ [c₃]` — one source citing two targets. `|F| = 1` and `|G| = 2 < ∞`, so `Sh-conf(citation, [c₁], [c₂] ∪ [c₃]) = ⊤`. (Each of `[c₂]`, `[c₃]` covers a subtree; the span *count* is 2, which is what Multi reads.)

**State-independence (P5), with ghosts.** Take two reachable states: `Σ`, in which only `c₁` has been stored, so `c₂, c₃ ∉ dom(Σ.C)` — they are ghost addresses; and `Σ'`, reachable from `Σ`, in which `c₂, c₃` have since been stored. The citation emit above references `c₂, c₃`. Evaluate `Sh-conf(citation, [c₁], [c₂] ∪ [c₃])` at each: the predicate inspects only the span counts `|F| = 1`, `|G| = 2` and `citation`'s registered shape `Multi`, consulting no state-indexed set (Shape-conformance). It returns `⊤` at both `Σ` and `Σ'`, identically. Had `Sh-conf` enforced a residence domain, the ghost references at `Σ` would have flipped the verdict to `⊥` while `Σ'` returned `⊤`, contradicting P5; because the predicate consults no state-indexed set, the citation is emittable at `Σ` exactly as at `Σ'`, and its ghost targets are admissible (L4/L9). This is the concrete content of both P5 and the no-residence-check decision.

**Born nullified (gate fires, tuple lands inactive).** The wp analysis in The shape-gated emit isolates a subtle separation: a gate-enabled emit — (0), (i), (ii) all hold — may still fail the *active-subset* postcondition `(a, F, G) ∈ A_K^{Σ'}` when an inherited ASN-0086 landing conjunct is false. We exhibit a concrete witness, exercising precisely the case the gate does not catch. Link addresses homed at `d` are enumerated `ℓ₁ = 1.1.0.1.0.1.0.2.1`, `ℓ₂ = 1.1.0.1.0.1.0.2.2`, then by sibling advance (`a_emit = inc(ℓ_prev, 0)`). Begin at a state `Σ₀` reachable from `Σ_init` in which two citation links already occupy `ℓ₁, ℓ₂` (so `dom(Σ₀.L) = {ℓ₁, ℓ₂}` homed at `d`).

*Step 1 — emit a Binary R-tuple with a non-unit G.* We deliberately bypass the framework's unit-depth retraction wrapper — the constructed `Emit_R(Σ, d_retr, [r], {(a, δ(1, #a))})` of Single-source, which writes a unit-depth to-span by construction — and instead invoke the *generic* gated emit `Emit_R` at the registered Binary type R directly, supplying a non-unit range G. This is intentional: the example exercises the gate's Binary-only enforcement, not the wrapper's unit-depth construction, so it must use the generic operation rather than the wrapper (which could not supply a range G). Issue `Emit_R(Σ₀, d, [c₁], G_rng)` with attributing source `[c₁]` (`|F| = 1`) and a *single* range span `G_rng = {(g, δ(3, #g))}` where `g = 1.1.0.1.0.1.0.2.4`; so `|G_rng| = 1` and `coverage(G_rng) = {t : 1.1.0.1.0.1.0.2.4 ≤ t < 1.1.0.1.0.1.0.2.7}`, a contiguous range of three link siblings and their subtrees. The gate fires: (0) the value `([c₁], G_rng, retract)` is a triple; (i) `retract` is registered; (ii) `Sh-conf(retract, [c₁], G_rng) = ⊤` since `retract` is Binary and `|F| = |G_rng| = 1`. This is the crux — Binary admits a *non-unit-length* G span, so the gate enforces only Binary, not ASN-0086's unit-depth retraction discipline; the covering range is genuinely reachable under `→_sh`. The tuple deposits at the fresh `a_R = a_emit(Σ₀, d) = inc(ℓ₂, 0) = 1.1.0.1.0.1.0.2.3`. Note `a_R ∉ coverage(G_rng)` (`...2.3 < ...2.4`), so even this retraction lands active — it does not nullify itself. Call the post-state `Σ₁`; now `L_retract^{Σ₁} = {(a_R, [c₁], G_rng)}`.

*Step 2 — emit a conforming non-R tuple into the covered range.* Issue `Emit_citation(Σ₁, d, [c₁], [c₂] ∪ [c₃])`. The fresh address is `a = a_emit(Σ₁, d) = inc(a_R, 0) = 1.1.0.1.0.1.0.2.4 = g`. The gate fires again — (0) triple; (i) `citation` registered; (ii) `Sh-conf(citation, [c₁], [c₂] ∪ [c₃]) = ⊤` (`|F| = 1`, `|G| = 2 < ∞`, Multi). So this is a legal `→_sh`-step and the tuple enters the audit slice `L_citation^{Σ₂}`.

*The landing fails.* Yet `(a, [c₁], [c₂] ∪ [c₃]) ∉ A_citation^{Σ₂}`. Trace the inherited wp third conjunct `¬(∃ (b, F', G') ∈ L_R^{Σ₁} :: a_emit(Σ₁, d) ∈ coverage(G'))`: the retraction tuple `(a_R, [c₁], G_rng) ∈ L_R^{Σ₁}` has `a = g ∈ coverage(G_rng)` (since `g` is the lower endpoint of the half-open range), so the existential holds and the conjunct is *false*. By ASN-0086's `nullified`/`A_K` machinery the citation is born nullified: `a ∈ nullified(Σ₂)`, hence `(a, [c₁], [c₂] ∪ [c₃]) ∉ A_citation^{Σ₂}`. The gate did not reject this call — all of (0), (i), (ii) held — the wp's inherited third conjunct did. This is the witness that The shape-gated emit's gate-vs-landing separation forward-points to.

By P3, `idem(approved) = ⊤` and `idem(touched) = ⊥` are structural facts equal at every Σ.

## Open questions

The following are deliberately left for the successor note that layers operational semantics on top of this framework:

1. **Idem semantics at emit.** What does the substrate do when an app emits a tuple that is "the same as" an active tuple of the same type with `idem=⊤`? What counts as "the same" — `(F, G, K)` values only, or does proposer or emission time enter? How does this interact with nullification, with versioning cascade, and with concurrent emits?

2. **Behavior catalog.** Which substrate-provided behaviors (read-filter, transitive-closure, typed-reverse-lookup, age-staleness, and others not yet named) compose with which shapes, and what predicates does each unlock?

3. **Default predicates.** What predicates does every registered type receive by virtue of its shape and idem flag, independent of any behavior?

4. **Standard registrations.** Whether the substrate ships any types pre-registered — `retired` (Unary, idem=⊤, read-filter), `supersedes` (Binary, idem=⊤, transitive-closure), and the retraction type `R` (Binary, the attributed re-expression of ASN-0086's Nullify) are obvious candidates the lattice already uses universally — or whether each substrate's `Σ_init.registry` is instead composed entirely of app-declared entries. Nelson names no retraction type and treats his standard set as provisional, so by his design R currently falls on the app-defined side while remaining a candidate for standardization-by-convention.

5. **Predicate composition.** Composition rules over the atomic predicates each type receives — the predicate-composition territory left open here.

6. **Extension beyond F=1 and N=3.** When an app eventually needs multi-source relations or richer arity, whether the path is a supplemental note that loosens the constraints here, a parallel framework, or direct link-store interaction.

Each of these can be resolved without revisiting the structural commitments above.
