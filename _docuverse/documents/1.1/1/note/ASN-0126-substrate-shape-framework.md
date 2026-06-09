# ASN-0126: Substrate Shape Framework

*Narrowing the typed-relation framework into a concrete vocabulary apps register against*

ASN-0086 commits the substrate to typed relations of arity three over `(F, G, K)` and provides the operational vocabulary `Emit_K`, `Observe`, `Nullify`. It does not narrow the cardinalities of the F and G slots, nor does it say anything about what an app must look like when it registers a type. Apps interacting with the substrate need more than ASN-0086 gives: a finite shape catalog they can register against, a static shape-conformance check the substrate can apply at every emit, and a registry whose contents do not drift across states. This note supplies that — and only that.

The lattice's actual usage — classifiers, citations, supersession chains, holdings, retractions — is uniformly single-source. The right level of commitment is concrete shapes the substrate can statically check, with everything operational layered on top.

## Single-source

Every typed relation has a single-span source — `|F| = 1`, where `|·|` counts the spans in an endset (the measure is fixed precisely under Shape-conformance below). There is no two-source variant, no zero-source variant, no variadic-F. Across the lattice's usage, classifiers attach to a single address, citations fan out from a single source, supersession chains anchor on a single predecessor, holdings are owned by a single agent. The single-source commitment captures every observed pattern and rejects nothing the substrate is asked to express. Note that the one F span may itself cover a contiguous range or a whole subtree, not merely one address — Nelson confirms "a single source span [may] legitimately cover a range/subtree ... the single-address case is just the smallest (degenerate) instance." The substrate narrows away only the multi-span, discontiguous from-set that the full link store (ASN-0043) would permit; it does not narrow what one span may reach.

The link store underneath the substrate (ASN-0043) permits arbitrary higher arity, and an app needing multi-source relations can interact with the link store directly. The substrate does not provide machinery for that case. Adding it later means a supplemental note, not a revision here.

## Three shapes by G span count

With F fixed at one span, the framework varies only by what G can hold. We measure G by its *span count* (the measure `|·|` defined under Shape-conformance below — the number of spans in the endset, not the number of tumblers in its coverage). Three shapes capture every usage observed in the lattice:

| Shape  | G span count   | What it expresses                                              |
|--------|----------------|-----------------------------------------------------------------|
| Unary  | `\|G\| = 0` (G = ∅) | A predicate or marker on a single source                    |
| Binary | `\|G\| = 1`      | A directed relation to one target span                          |
| Multi  | `\|G\|` finite   | A single source connected to finitely many target spans         |

The Unary shape covers classifiers, lifecycle markers, presence assertions. The Binary shape covers supersession, parent-child, attached-aux relations. The Multi shape covers citations, fan-outs, multi-target connections.

These conditions do **not** partition the space of expressible tuples. Unary (`|G| = 0`) and Binary (`|G| = 1`) are mutually exclusive, but Multi (`|G|` finite) subsumes both — a Multi registration admits every tuple a Unary or Binary registration would, and more. The shapes therefore classify *registrations*, not tuples: a type K is registered once with one shape, and that shape fixes which tuples are well-formed under K. Multi is the permissive endpoint, not a third disjoint bucket. The claim "no fourth shape" is accordingly modest: no recurring lattice pattern needs a G-discipline outside `{empty, singleton, unrestricted-finite}`, nor a multi-span F.

Endset targets are unrestricted. `F` and `G` spans may point anywhere in the tumbler space — to content addresses, to link addresses, or to *ghost* addresses where nothing is stored. This is L4 (EndsetGenerality) and L9 (TypeGhostPermission, ASN-0043) inherited without narrowing. The framework constrains the *span count* per shape; it never constrains the residence of the addresses those spans cover.

## Shape-conformance

The shapes are stated in terms of the *span count* of an endset. F and G are endsets, and `Endset = 𝒫_fin(Span)` (ASN-0043) — a finite set of spans. For an endset `e`, write `|e|` for its cardinality *as a finite set of spans*: the number of spans it contains, **not** the number of tumblers in `coverage(e)`. The two measures diverge sharply. A single unit-depth span `(a, δ(1, #a))` is one span — `|{(a, δ(1, #a))}| = 1` — yet its coverage is `{t : a ≼ t}`, generally infinite (PrefixSpanCoverage, ASN-0043). We count spans, deliberately, because (per the Single-source discussion and Nelson's design intent) a source span is *meant* to be able to cover a range or subtree; a coverage-singleton measure `|coverage(F)| = 1` would contradict that intent and is rejected. The only endsets with singleton coverage are those whose single span has unit length at a terminal (childless) address; the framework requires no such thing.

For a typed tuple `(F, G, K)` under a type K registered with shape s, the well-formedness predicate `Sh-conf(K, F, G)` holds when:

- Unary: `|F| = 1` and `G = ∅` (equivalently `|G| = 0`);
- Binary: `|F| = 1` and `|G| = 1`;
- Multi: `|F| = 1` and `|G| < ∞`.

For Multi the conjunct `|G| < ∞` holds for *every* endset by `Endset = 𝒫_fin(Span)`, so Multi places no real bound on G's span count — it is the unrestricted shape, constraining only F. This is intentional, not an oversight: Multi is the permissive endpoint of the catalog (see Three shapes).

`Sh-conf` consults nothing about content residence. Endset spans may reference any address, including ghost addresses at which nothing is stored: L4 and L9 (ASN-0043) permit this, Nelson is explicit that "endset addresses do NOT need to resolve to stored content" — the type endset especially "is designed to exploit this" — and Gregory confirms udanax-green enforces no residence check at link creation. The framework inherits that permission unchanged. In particular `Sh-conf` does not test membership in `dom(Σ.C)`, `dom(Σ.L)`, or any state-indexed address set such as ASN-0086's `A_doc^Σ`, `A_rel^Σ`, `A^Σ`. Were it to, a ghost reference at one state and a stored reference at a later state would yield different verdicts, destroying the state-independence we want (P5).

The predicate therefore depends only on the tuple's span counts `|F|`, `|G|` and the shape recorded for K in the registry. No component of Σ is consulted — not `Σ.C`, not `Σ.L`, not `Σ.M` — and no other element of `dom(Σ.L)` is inspected. `Sh-conf` is a property of the tuple-plus-registration pair, evaluable identically at any reachable state.

### The shape-gated emit

ASN-0086's K.λ step has precondition L3 only (arity ≥ 3, non-empty type slot); it does not inspect span counts, so the bare `→` of ASN-0086 *admits* shape-non-conforming tuples. This framework does not pretend `→` already rejects them — it **refines** the emit step. Define the framework's transition relation

`→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh`,

where `K.λ_sh` is `K.λ` with the added precondition `Sh-conf(K, F, G)`: an emit of value `(F, G, K)` under registered type K is enabled only when the tuple conforms to K's shape. K.σ and K.α are unchanged. All reachability in this note is with respect to `→_sh`. Under this definition P4 holds *by construction* of `K.λ_sh`, not as a derived property of the unmodified ASN-0086 relation.

## Registry permanence

ASN-0043/0086 carry substrate state `Σ = (Σ.C, Σ.M, Σ.L)`. This framework extends that tuple with a fourth, immutable component:

`Σ = (Σ.C, Σ.M, Σ.L, Σ.registry)`

The registry is fixed when `Σ_init` is defined. To show it never drifts we must reconcile it with the transition relation rather than merely assert permanence. ASN-0086's relation is `→ ≡ K.σ ∪ K.α ∪ K.λ`, refined here to `→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh` (the shape-gating touches only K.λ's precondition, not its frame). A K.σ-step extends `dom(Σ.M)`, a K.α-step extends `dom(Σ.C)`, and a K.λ_sh-step extends `dom(Σ.L)`, each leaving the other two stores framed. We extend every step's frame condition with the registry as an additional framed component:

- K.σ: `Σ'.C = Σ.C`, `Σ'.L = Σ.L`, `Σ'.registry = Σ.registry`;
- K.α: `Σ'.M = Σ.M`, `Σ'.L = Σ.L`, `Σ'.registry = Σ.registry`;
- K.λ_sh: `Σ'.C = Σ.C`, `Σ'.M = Σ.M`, `Σ'.registry = Σ.registry`.

No step kind in `→_sh` has the registry in its *effect*; each leaves it in its frame. P1 then follows by induction on the length of a `→_sh*`-derivation: the base case `Σ = Σ_init` is immediate, and each step preserves `Σ.registry = Σ_init.registry` by the frame condition for whichever of the three kinds it is. So for every Σ reachable from Σ_init, `Σ.registry = Σ_init.registry`.

This invariance has structural consequences. A type K's shape is a function of K alone — `shape(K)` is well-defined without reference to state (P2), and the same K cannot carry one shape at Σ and another at Σ'. Likewise `idem(K)` is state-independent (P3). `Sh-conf` is therefore stable: since it reads only `(F, G, K)` and `shape(K)`, and `shape(K)` is registry-determined and the registry is invariant, `Sh-conf(K, F, G)` evaluates the same against Σ as against any Σ' reachable from Σ (P5).

Distinct registries yield distinct substrates. There is no notion of altering the registry within a single substrate's evolution; the registry is fixed at the moment Σ_init is defined.

## The idem flag

Each registration carries an idem flag with values `⊤` or `⊥`. By the registry's invariance, `idem(K)` is a structural property of K — the same value at every reachable state. The flag's role in well-formedness, in the relationship between tuples with equal `(F, G, K)`, and in the semantics of nullification and re-emission is the subject of a successor note. This note commits to the flag's structural presence and its state-independence; the operational consequences are layered on top.

The flag belongs at the framework level rather than in the successor because the structural commitment — every citation registered as `(Multi, ⊤)`, every audit event as `(Multi, ⊥)` — is consulted by apps independently of how the operational semantics resolve.

## Registration entries

Each registry entry records a type K together with:

- a **name** — an opaque string identifier
- a **shape** — one of `Unary`, `Binary`, `Multi`
- an **idem** flag — `⊤` or `⊥`

An earlier draft recorded per-slot residence domains (`t_F`, `t_G` ∈ `{A_doc, A_rel, A}`) and had `Sh-conf` enforce them. We have removed that: those domains are state-indexed (`A_doc^Σ = dom(Σ.C)` etc., ASN-0086) and grow across `→`, so enforcing them would make `Sh-conf` state-dependent (contradicting P5) and would forbid the ghost references L4/L9 and Nelson explicitly sanction. The registry records shape and idem only; endset targets are unconstrained by residence.

A registry is well-formed when shape values lie in `{Unary, Binary, Multi}`, idem values lie in `{⊤, ⊥}`, and names are unique within the registry. The substrate makes no commitment about which name strings are admissible — that is the app's namespace. Distinct substrates may carry registries with overlapping names; within one substrate, the name uniquely identifies a registry entry.

## Properties established

This note establishes the following structural properties of every substrate satisfying its commitments:

**P1 (RegistryInvariance).** `Σ.registry = Σ_init.registry` for every Σ reachable from Σ_init. *Derived* (Registry permanence) from the registry's presence in the frame of every `→_sh`-step kind, by induction on derivation length.

**P2 (ShapeStability).** For every registered K, `shape(K)` is well-defined without reference to state, and the value is constant on the reflexive-transitive closure of `→_sh`. Corollary of P1: `shape(K)` reads only `Σ.registry`, which is invariant.

**P3 (IdemStability).** For every registered K, `idem(K) ∈ {⊤, ⊥}` is a structural property of K, equal at every reachable state. Corollary of P1, by the same argument as P2.

**P4 (Sh-confWellFormedness).** No `→_sh`-step extends `dom(Σ.L)` with a tuple `(F, G, K)` for which `Sh-conf(K, F, G)` fails. *True by construction* of `→_sh`: the only store-of-links step is `K.λ_sh`, whose precondition includes `Sh-conf(K, F, G)`. This is a definitional refinement of ASN-0086's relation, not a property of the unmodified `→` — which does admit non-conforming tuples.

**P5 (Sh-confStateIndependence).** For any K, F, G and any reachable Σ, Σ', `Sh-conf(K, F, G)` evaluated against Σ equals `Sh-conf(K, F, G)` evaluated against Σ'. *Derived*: `Sh-conf` reads only the span counts `|F|`, `|G|` and `shape(K)`; the counts are intrinsic to the values, and `shape(K)` is invariant by P1. No state-indexed set is consulted (Shape-conformance).

## Worked illustration

We fix concrete addresses to check P4 and P5 against a real scenario. Let the content subspace be `s_C = 1` and the link subspace `s_L = 2`. Take a document with prefix `d = 1.1.0.1.0.1` (node `1.1`, user `1`, document `1`; `zeros(d) = 2`). Its content occupies subspace 1:

- `c₁ = 1.1.0.1.0.1.0.1.1`
- `c₂ = 1.1.0.1.0.1.0.1.2`
- `c₃ = 1.1.0.1.0.1.0.1.3`

each an element-level I-address with `zeros = 3`. Write `[x] = {(x, δ(1, #x))}` for the unit-depth singleton endset at `x` — a one-span endset, so `|[x]| = 1` whatever `coverage([x])` turns out to be (here `coverage([x]) = {t : x ≼ t}`, by PrefixSpanCoverage).

Consider four registry entries:

- `approved`: Unary, idem=⊤
- `succession`: Binary, idem=⊤
- `citation`: Multi, idem=⊤
- `touched`: Multi, idem=⊥

**Unary.** Emit `(F, G, approved)` with `F = [c₁]`, `G = ∅`. Then `|F| = 1` and `|G| = 0`, so `Sh-conf(approved, [c₁], ∅) = ⊤` and `K.λ_sh` is enabled. The variant `([c₁], [c₂], approved)` has `|G| = 1 ≠ 0`, so `Sh-conf = ⊥`; no `→_sh`-step deposits it into `dom(Σ.L)` at any reachable state (P4).

**Binary.** Emit `(F, G, succession)` with `F = [c₂]`, `G = [c₁]` — "`c₂` supersedes `c₁`." Each endset carries one span, so `|F| = |G| = 1` and `Sh-conf(succession, [c₂], [c₁]) = ⊤`. The two-target variant `G = [c₁] ∪ [c₃]` has `|G| = 2`, failing Binary's `|G| = 1`.

**Multi.** Emit `(F, G, citation)` with `F = [c₁]`, `G = [c₂] ∪ [c₃]` — one source citing two targets. `|F| = 1` and `|G| = 2 < ∞`, so `Sh-conf(citation, [c₁], [c₂] ∪ [c₃]) = ⊤`. (Each of `[c₂]`, `[c₃]` covers a subtree; the span *count* is 2, which is what Multi reads.)

**State-independence (P5), with ghosts.** Take two reachable states: `Σ`, in which only `c₁` has been stored, so `c₂, c₃ ∉ dom(Σ.C)` — they are ghost addresses; and `Σ'`, reachable from `Σ`, in which `c₂, c₃` have since been stored. The citation emit above references `c₂, c₃`. Evaluate `Sh-conf(citation, [c₁], [c₂] ∪ [c₃])` at each: the predicate inspects only the span counts `|F| = 1`, `|G| = 2` and `citation`'s registered shape `Multi` — never `dom(Σ.C)`, never `A_doc^Σ`. It returns `⊤` at both `Σ` and `Σ'`, identically. Had `Sh-conf` enforced a residence domain, the ghost references at `Σ` would have flipped the verdict to `⊥` while `Σ'` returned `⊤`, contradicting P5; because the predicate consults no state-indexed set, the citation is emittable at `Σ` exactly as at `Σ'`, and its ghost targets are admissible (L4/L9). This is the concrete content of both P5 and the no-residence-check decision.

By P3, `idem(approved) = ⊤` and `idem(touched) = ⊥` are structural facts equal at every Σ; what `idem = ⊤` then implies for two well-formed `approved` tuples with equal `F` is the operational successor's concern.

## Open questions

The following are deliberately left for the successor note that layers operational semantics on top of this framework:

1. **Idem semantics at emit.** What does the substrate do when an app emits a tuple that is "the same as" an active tuple of the same type with `idem=⊤`? What counts as "the same" — `(F, G, K)` values only, or does proposer or emission time enter? How does this interact with nullification, with versioning cascade, and with concurrent emits?

2. **Behavior catalog.** Which substrate-provided behaviors (read-filter, transitive-closure, typed-reverse-lookup, age-staleness, and others not yet named) compose with which shapes, and what predicates does each unlock?

3. **Default predicates.** What predicates does every registered type receive by virtue of its shape and idem flag, independent of any behavior?

4. **Standard registrations.** Whether the substrate ships any types pre-registered — `retired` (Unary, idem=⊤, read-filter) and `supersedes` (Binary, idem=⊤, transitive-closure) are obvious candidates the lattice already uses universally — or whether every app registers all of its own types.

5. **Predicate composition.** Composition rules over the atomic predicates each type receives. Retired ASN-0095's territory.

6. **Extension beyond F=1 and N=3.** When an app eventually needs multi-source relations or richer arity, whether the path is a supplemental note that loosens the constraints here, a parallel framework, or direct link-store interaction.

Each of these can be resolved without revisiting the structural commitments above. The framework here is intentionally minimal: shape vocabulary, conformance check, registry permanence. Everything else layers.
