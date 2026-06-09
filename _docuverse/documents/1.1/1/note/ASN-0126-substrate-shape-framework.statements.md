# ASN-0126 Claim Statements

*Source: ASN-0126-substrate-shape-framework.md (revised unknown) — Extracted: 2026-06-09*

## Definition — ShapeConformance

For a typed tuple `(F, G, K)` under a type K registered with shape s, `Sh-conf(K, F, G)` holds when:

- Unary: `|F| = 1` and `G = ∅` (equivalently `|G| = 0`);
- Binary: `|F| = 1` and `|G| = 1`;
- Multi: `|F| = 1` and `|G| < ∞`.

`Sh-conf` is defined only for *registered* K — those for which the registry records a shape. For an unregistered K, `shape(K)` does not exist and `Sh-conf(K, F, G)` carries no truth value.

The predicate depends only on the tuple's span counts `|F|`, `|G|` and the shape recorded for K in the registry. No component of Σ is consulted — not `Σ.C`, not `Σ.L`, not `Σ.M` — and no other element of `dom(Σ.L)` is inspected.

---

## Definition — ShapeGatedEmit

`→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh`

where `K.λ_sh` is `K.λ` with three added preconditions:

- (0) *the emitted value is a standard triple* — `|value| = 3`, so it carries exactly the two content slots `(F, G)` that `Sh-conf` reads;
- (i) *K is registered* — the registry records a shape for K;
- (ii) `Sh-conf(K, F, G)`.

The three are ordered: (0) and (i) jointly discharge the domain condition for (ii). K.σ and K.α are unchanged.

---

## Definition — RegistryProjection

`π(Σ) = (Σ.C, Σ.M, Σ.L)`

The projection that forgets the registry. Each `→_sh`-step acts on the C/M/L components exactly as the corresponding ASN-0086 step: a K.σ-step as `K.σ`, a K.α-step as `K.α`, and a `K.λ_sh`-step as a `K.λ` step. Hence whenever `Σ →_sh Σ'`, we have `π(Σ) → π(Σ')` in ASN-0086's relation.

---

## Definition — WpShapeGatedEmit

`wp(Emit under →_sh, (a, F, G) ∈ A_K^{Σ'})`
`≡ K registered ∧ Sh-conf(K, F, G) ∧ d ∈ dom(Σ.M) ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G)) ∧ ¬(∃ (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∈ coverage(G'))`

The first two conjuncts are this note's contribution; the remaining three are inherited verbatim from ASN-0086's Case-2 wp. Their ordering is load-bearing: `Sh-conf(K, F, G)` carries a truth value only on registered K, so `K registered` is the domain-discharging conjunct and the conjunction is read left-to-right, `Sh-conf` evaluated only where defined.

---

## C0 — RegistryWellFormedness (PRE, axiom)

`Σ_init.registry` is well-formed — i.e. it *is* a *finite* partial function `T_admissible/~ ⇀ (name, shape, idem)` with `|Σ_init.registry| < ∞`, realized concretely by storing, for each entry, a *finite representative endset* `K_j ∈ T_admissible` of its coverage class together with `(name, shape, idem)`. Coverage-class keys are unique — no two stored representatives are `~`-equal — so lookup by `[K]`, decided by comparing `coverage(K)` against each stored `coverage(K_j)`, returns at most one entry.

---

## P1 — RegistryInvariance (INV, invariant)

`Σ.registry = Σ_init.registry` for every Σ reachable from `Σ_init`.

*Derived* from the registry's presence in the frame of every `→_sh`-step kind, by induction on derivation length.

Frame conditions per step kind:
- K.σ: `Σ'.C = Σ.C`, `Σ'.L = Σ.L`, `Σ'.registry = Σ.registry`;
- K.α: `Σ'.M = Σ.M`, `Σ'.L = Σ.L`, `Σ'.registry = Σ.registry`;
- K.λ_sh: `Σ'.C = Σ.C`, `Σ'.M = Σ.M`, `Σ'.registry = Σ.registry`.

---

## P2 — ShapeStability (LEMMA, lemma)

For every registered K, `shape(K)` is well-defined without reference to state, and the value is constant on the reflexive-transitive closure of `→_sh`.

Well-definedness has two halves:

(a) *Single-valuedness* — that lookup by `[K]` returns at most one shape, so `shape(·)` is a function at all — is supplied by **C0**: coverage-class keys are unique.

(b) *State-independence* — that this single value does not change across states — is supplied by **P1**: `shape(K)` reads only `Σ.registry`, which is invariant.

---

## P3 — IdemStability (LEMMA, corollary)

For every registered K, `idem(K) ∈ {⊤, ⊥}` is a structural property of K, equal at every reachable state.

Corollary of C0 and P1, by the same two-premise argument as P2: C0 makes `idem(·)` single-valued (one entry per coverage class), and P1 makes that value state-independent.

---

## P4 — ShConfWellFormedness (LEMMA, safety)

No `→_sh`-step extends `dom(Σ.L)` with a tuple `(F, G, K)` whose K is unregistered, nor with one for which `Sh-conf(K, F, G)` fails.

The only store-of-links step is `K.λ_sh`, whose preconditions are (0) `|value| = 3`, (i) K registered, and (ii) `Sh-conf(K, F, G)`:

- a non-triple value fails (0) and is not a `→_sh`-step at all;
- an unregistered K is rejected by (i) before `Sh-conf` is consulted;
- a registered but non-conforming tuple is rejected by (ii).

---

## P5 — ShConfStateIndependence (LEMMA, lemma)

For any *registered* K and any F, G, and any reachable Σ, Σ', `Sh-conf(K, F, G)` is defined at both states and its verdict at Σ equals its verdict at Σ'.

(a) *Definedness coincides*: By P1 the registry is the invariant `Σ_init.registry`, so K is registered at Σ iff registered at Σ'.

(b) *Verdict coincides*: Where defined, `Sh-conf` reads only the span counts `|F|`, `|G|` and `shape(K)`; the counts are intrinsic to the values, and `shape(K)` is invariant by P1. No state-indexed set is consulted.

---

## P6 — GateRealizability (LEMMA, liveness)

For any `→_sh`-reachable Σ, any `d ∈ dom(Σ.M)`, any registered K, and any `F, G ∈ Endset` with `Sh-conf(K, F, G) = ⊤`, there exists Σ' with `Σ →_sh Σ'` depositing the standard triple `(F, G, K)` at the fresh address `a = a_emit(Σ, d)`:

`a ∉ dom(Σ.L) ∧ a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K) ∧ home(a) = d`

with Σ' itself `→_sh`-reachable.

Sub-claims established in proof:

(a) `K ∈ T_admissible`: K is registered, so by C0 the registry stores a finite representative `K_j ∈ T_admissible` of K's coverage class; `coverage(K_j) ≠ ∅` (every span has length `ℓ > 0`); hence `coverage(K) = coverage(K_j) ≠ ∅`, so `K ≠ ∅`.

(b) *Address pinning*: Since `a_emit` reads only the M and L components, which Σ and `π(Σ)` share, `a_emit(π(Σ), d) = a_emit(Σ, d)`.

(c) *Lift*: Form Σ' by adjoining the unchanged registry to `Σ_{0086}`: `Σ'.C = Σ_{0086}.C`, `Σ'.M = Σ_{0086}.M`, `Σ'.L = Σ_{0086}.L`, `Σ'.registry = Σ.registry`. The step `Σ →_sh Σ'` is a `K.λ_sh`-step: preconditions (0) `|value| = 3`, (i) K registered, (ii) `Sh-conf(K, F, G) = ⊤` all hold by premise; registry frame `Σ'.registry = Σ.registry` holds by construction.
