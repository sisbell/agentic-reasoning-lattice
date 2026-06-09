# ASN-0126: Substrate Shape Framework

*Narrowing the typed-relation framework into a concrete vocabulary apps register against*

ASN-0086 commits the substrate to typed relations of arity three over `(F, G, K)` and provides the operational vocabulary `Emit_K`, `Observe`, `Nullify`. It does not narrow the cardinalities of the F and G slots, nor does it say anything about what an app must look like when it registers a type. Apps interacting with the substrate need more than ASN-0086 gives: a finite shape catalog they can register against, a static shape-conformance check the substrate can apply at every emit, and a registry whose contents do not drift across states. This note supplies that — and only that.

The lattice's actual usage — classifiers, citations, supersession chains, holdings, retractions — is uniformly single-source. The right level of commitment is concrete shapes the substrate can statically check, with everything operational layered on top.

## Single-source

Every typed relation has exactly one F. There is no two-source variant, no zero-source variant, no variadic-F. Across the lattice's usage, classifiers attach to a single address, citations fan out from a single source, supersession chains anchor on a single predecessor, holdings are owned by a single agent. The single-source commitment captures every observed pattern and rejects nothing the substrate is asked to express.

The link store underneath the substrate (ASN-0043) permits arbitrary higher arity, and an app needing multi-source relations can interact with the link store directly. The substrate does not provide machinery for that case. Adding it later means a supplemental note, not a revision here.

## Three shapes by G cardinality

With F fixed at 1, the framework varies only by what G can hold. Three shapes capture every usage observed in the lattice and rule out a fourth:

| Shape  | G cardinality | What it expresses                                              |
|--------|---------------|-----------------------------------------------------------------|
| Unary  | G = ∅         | A predicate or marker on a single address                       |
| Binary | G = 1         | A directed relation between two addresses                       |
| Multi  | G = *         | A single source connected to a finite set of target addresses   |

The Unary shape covers classifiers, lifecycle markers, presence assertions. The Binary shape covers supersession, parent-child, attached-aux relations. The Multi shape covers citations, fan-outs, multi-target connections. The lattice expresses everything it needs through these three; no recurring pattern in usage suggests a fourth.

Target domains are general. `F` ranges over `A = A_doc ∪ A_rel` (the address universe of ASN-0086) by default. `G` ranges similarly when present. Apps may narrow either domain at registration time (e.g., a citation relation may restrict G-elements to documents only).

## Shape-conformance

For a typed tuple `(F, G, K)` under a type K registered with shape s, the well-formedness predicate `Sh-conf(K, F, G)` holds when:

- Unary: `|F| = 1` and `G = ∅`;
- Binary: `|F| = 1` and `|G| = 1`;
- Multi: `|F| = 1` and `G` is a finite set of addresses.

In every case the F element lies in K's declared `t_F` domain, and (when present) every G element lies in `t_G`. A tuple violating `Sh-conf` is not a well-formed emission: no `→`-step extends `dom(Σ.L)` with such a tuple, in any reachable state.

The predicate depends only on the tuple's values `(F, G, K)` and the registry entry for K. No other component of Σ is consulted; no other element of `dom(Σ.L)` is inspected. `Sh-conf` is therefore a property of the tuple-plus-registration pair, evaluable identically at any reachable state.

## Registry permanence

The registry is a component of Σ_init. It is invariant across every `→`-step: for every Σ reachable from Σ_init, `Σ.registry = Σ_init.registry`. No transition extends, modifies, or contracts the registry.

This invariance has structural consequences. A type K's shape is a function of K alone — `shape(K)` is well-defined without reference to state, and the same K cannot carry one shape at Σ and another at Σ'. Likewise `idem(K)` and `t_F(K)`, `t_G(K)` are state-independent. `Sh-conf` is therefore stable: `Sh-conf(K, F, G)` evaluates the same against Σ as against any Σ' reachable from Σ.

Distinct registries yield distinct substrates. There is no notion of altering the registry within a single substrate's evolution; the registry is fixed at the moment Σ_init is defined.

## The idem flag

Each registration carries an idem flag with values `⊤` or `⊥`. By the registry's invariance, `idem(K)` is a structural property of K — the same value at every reachable state. The flag's role in well-formedness, in the relationship between tuples with equal `(F, G, K)`, and in the semantics of nullification and re-emission is the subject of a successor note. This note commits to the flag's structural presence and its state-independence; the operational consequences are layered on top.

The flag belongs at the framework level rather than in the successor because the structural commitment — every citation registered as `(Multi, ⊤)`, every audit event as `(Multi, ⊥)` — is consulted by apps independently of how the operational semantics resolve.

## Registration entries

Each registry entry records a type K together with:

- a **name** — an opaque string identifier
- a **shape** — one of `Unary`, `Binary`, `Multi`
- an **idem** flag — `⊤` or `⊥`
- a **t_F** domain — `A_doc`, `A_rel`, or `A` (defaulting to `A`)
- a **t_G** domain — same options, omitted for Unary

A registry is well-formed when shape values lie in `{Unary, Binary, Multi}`, idem values lie in `{⊤, ⊥}`, and names are unique within the registry. The substrate makes no commitment about which name strings are admissible — that is the app's namespace. Distinct substrates may carry registries with overlapping names; within one substrate, the name uniquely identifies a registry entry.

## Properties established

This note establishes the following structural properties of every substrate satisfying its commitments:

**P1 (RegistryInvariance).** `Σ.registry = Σ_init.registry` for every Σ reachable from Σ_init.

**P2 (ShapeStability).** For every registered K, `shape(K)` is well-defined without reference to state, and the value is constant on the reflexive-transitive closure of `→`.

**P3 (IdemStability).** For every registered K, `idem(K) ∈ {⊤, ⊥}` is a structural property of K, equal at every reachable state.

**P4 (Sh-confWellFormedness).** No `→`-step extends `dom(Σ.L)` with a tuple `(F, G, K)` for which `Sh-conf(K, F, G)` fails.

**P5 (Sh-confStateIndependence).** For any K, F, G and any reachable Σ, Σ', `Sh-conf(K, F, G)` evaluated against Σ equals `Sh-conf(K, F, G)` evaluated against Σ'.

## Worked illustration

Consider four registry entries:

- `approved`: Unary, idem=⊤
- `succession`: Binary, idem=⊤
- `citation`: Multi, idem=⊤
- `touched`: Multi, idem=⊥

For each, `Sh-conf` partitions candidate tuples into well-formed and not. Under `approved`, a tuple `(F, G, approved)` with `G ≠ ∅` fails `Sh-conf` and cannot appear in `dom(Σ.L)` at any reachable state (P4). Under `succession`, a tuple with `|G| ≠ 1` fails. Under any of the four, a tuple with `|F| ≠ 1` fails. By P5 these partitions are state-independent — the well-formed candidates are the same at every reachable state. By P3, `idem(approved) = ⊤` and `idem(touched) = ⊥` are structural facts equal at every Σ; what `idem = ⊤` then implies for the relationship between two well-formed `approved` tuples with equal `F` is the operational successor's concern.

## Open questions

The following are deliberately left for the successor note that layers operational semantics on top of this framework:

1. **Idem semantics at emit.** What does the substrate do when an app emits a tuple that is "the same as" an active tuple of the same type with `idem=⊤`? What counts as "the same" — `(F, G, K)` values only, or does proposer or emission time enter? How does this interact with nullification, with versioning cascade, and with concurrent emits?

2. **Behavior catalog.** Which substrate-provided behaviors (read-filter, transitive-closure, typed-reverse-lookup, age-staleness, and others not yet named) compose with which shapes, and what predicates does each unlock?

3. **Default predicates.** What predicates does every registered type receive by virtue of its shape and idem flag, independent of any behavior?

4. **Standard registrations.** Whether the substrate ships any types pre-registered — `retired` (Unary, idem=⊤, read-filter) and `supersedes` (Binary, idem=⊤, transitive-closure) are obvious candidates the lattice already uses universally — or whether every app registers all of its own types.

5. **Predicate composition.** Composition rules over the atomic predicates each type receives. Retired ASN-0095's territory.

6. **Extension beyond F=1 and N=3.** When an app eventually needs multi-source relations or richer arity, whether the path is a supplemental note that loosens the constraints here, a parallel framework, or direct link-store interaction.

Each of these can be resolved without revisiting the structural commitments above. The framework here is intentionally minimal: shape vocabulary, conformance check, registry permanence. Everything else layers.
