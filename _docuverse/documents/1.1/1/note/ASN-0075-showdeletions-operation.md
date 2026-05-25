# ASN-0075: SHOWDELETIONS Operation

*2026-05-25*

Nelson lists "show deletions" among the operations the system must provide (LM 4/79). The intuition is direct: given two documents that share content history, identify the content that was present in one but is absent from the other. We approach this abstractly. We do not specify how documents come to share history, nor how content is removed from an arrangement — those mechanics belong elsewhere. We specify only what the operation must produce, what guarantees it must offer over its output, and what state it consults.

The central difficulty is that two situations are observationally indistinguishable without further information: content `a` may be absent from document `d`'s arrangement because `d` once contained `a` and removed it (it was *deleted*), or because `d` was never an arrangement that contained `a` (it was *never included*). A "show deletions" operation must distinguish these. We will show that the provenance relation `R` introduced in the transition model supplies exactly the information required, and that any conforming implementation must therefore maintain state components — beyond `(C, L, E, M)` collectively — sufficient to disambiguate the two predicates `DELETED(a, d)` and `NEVER_INCLUDED(a, d)` at every reachable state. Without such components, deletion is not detectable as a kind separate from prior absence.

## Foundation Recap

We take from the foundation:

- **Content store** `Σ.C : T ⇀ Val` (ASN-0036, S0): a partial function from tumblers to content values, append-only with immutable values across transitions.
- **Arrangement** `Σ.M(d) : T ⇀ T` (ASN-0036, S2, S3, S8a, S8-depth): a per-document partial function from V-positions to I-addresses.
- **Entity set** `Σ.E ⊆ T` and its document partition `Σ.E_doc` (ASN-0047).
- **Provenance relation** `Σ.R ⊆ T × E_doc` (ASN-0047): `(a, d) ∈ R` iff document `d` has, at some point in the system's history, contained I-address `a` in its content-subspace arrangement.
- **Provenance permanence** `R ⊆ R'` across transitions (P2, ASN-0047): once `(a, d) ∈ R`, it remains so.
- **Provenance bounds** `Contains_C(Σ) ⊆ R` (P4★, ASN-0047): if `a` is currently in `d`'s content-subspace arrangement, then `(a, d) ∈ R`.
- **Historical fidelity** (P4a, ASN-0047): if `(a, d) ∈ R`, some prior reachable state had `a` in `d`'s content-subspace arrangement.
- **Provenance grounding** `R ⊆ dom(C) × E_doc` (P7, ASN-0047): every provenance pair references content that exists.
- **Origin function** `origin(a)` (ASN-0036, S7): every `a ∈ dom(C)` has a uniquely determined originating document, invariant across states.
- **Subspace projection** `subspace_I(a)` (ASN-0036, S7c): identifies the content (`s_C`) or link (`s_L`) subspace of an I-address.
- **Subspace convention** `s_C = 1, s_L = 2` (ASN-0047, SubspaceConventionAxiom).
- **Link subspace ownership** (CL-OWN, ASN-0047): link-subspace V-positions of `d` map only to link I-addresses with `origin = d`.

We restrict attention to the content subspace throughout. The justification appears in §D-SUBSP.

## The Three States of Content

We classify each pair `(a, d)` with `a ∈ dom(C)`, `subspace_I(a) = s_C`, and `d ∈ E_doc` into one of three states:

```
CURRENT(a, d)         ≡  a ∈ ran(M(d))
DELETED(a, d)         ≡  (a, d) ∈ R  ∧  a ∉ ran(M(d))
NEVER_INCLUDED(a, d)  ≡  (a, d) ∉ R
```

We must show these are exhaustive and mutually exclusive — otherwise the operation's outputs would have undefined classifications.

**Lemma D-EXH (Three-State Exhaustion).** Let `Σ` be a state reachable from `Σ_0` by a finite sequence of valid composite transitions (equivalently, `Σ` is a composite boundary). For every `(a, d)` with `a ∈ dom(Σ.C)`, `subspace_I(a) = s_C`, and `d ∈ Σ.E_doc`, exactly one of `CURRENT(a, d)`, `DELETED(a, d)`, `NEVER_INCLUDED(a, d)` holds.

The reachability hypothesis is load-bearing for the proof: it activates `P4★` (`Contains_C(Σ) ⊆ R`), which ASN-0047 establishes as a composite-boundary property — not as a per-state invariant preserved by every elementary transition. At intermediate states inside a composite, `P4★` may fail, so the lemma's universal claim applies only to states observed at composite boundaries. SHOWDELETIONS is an observational operation (D-OBS) that is only meaningful at reachable states, so the restriction does not narrow its operational scope.

*Proof.* The three predicates correspond to three of the four cases of the cross-product `(a ∈ ran(M(d))) × ((a, d) ∈ R)`:

| `a ∈ ran(M(d))` | `(a, d) ∈ R` | Predicate |
|---|---|---|
| Yes | Yes | CURRENT |
| Yes | No | impossible |
| No  | Yes | DELETED |
| No  | No  | NEVER_INCLUDED |

The "impossible" row is excluded by the following chain. From `a ∈ ran(M(d))` we obtain some `v ∈ dom(M(d))` with `M(d)(v) = a`. From the lemma's hypothesis `a ∈ dom(Σ.C)`, L14 (`dom(C) ∩ dom(L) = ∅`) gives `a ∉ dom(L)`. By S3★-aux, `subspace(v) ∈ {s_C, s_L}`. The contrapositive of S3★'s link clause — `subspace(v) = s_L ⟹ M(d)(v) ∈ dom(L)` — together with `M(d)(v) = a ∉ dom(L)` forces `subspace(v) ≠ s_L`, so `subspace(v) = s_C`. With `v` witnessing `v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ M(d)(v) = a`, the pair `(a, d)` belongs to `Contains_C(Σ)` by definition, and `Contains_C(Σ) ⊆ R` by P4★. So `(a, d) ∈ R`, contradicting `(a, d) ∉ R`.

For each remaining row, label assignment is direct from the predicate definitions:

- Row 1 (`a ∈ ran(M(d)) ∧ (a, d) ∈ R`): CURRENT holds (definition); DELETED fails (`a ∈ ran(M(d))` falsifies its second conjunct); NEVER_INCLUDED fails (`(a, d) ∈ R`).
- Row 3 (`a ∉ ran(M(d)) ∧ (a, d) ∈ R`): DELETED holds (both conjuncts); CURRENT fails (`a ∉ ran(M(d))`); NEVER_INCLUDED fails (`(a, d) ∈ R`).
- Row 4 (`a ∉ ran(M(d)) ∧ (a, d) ∉ R`): NEVER_INCLUDED holds (definition); CURRENT fails (`a ∉ ran(M(d))`); DELETED fails (`(a, d) ∉ R` falsifies its first conjunct).

In each row exactly one of the three predicates holds, so any pair `(a, d)` falling into any one row is assigned a unique label — establishing mutual exclusion. Exhaustiveness follows from cross-product totality: each of the two binary conditions `a ∈ ran(M(d))` and `(a, d) ∈ R` is either true or false, so every `(a, d)` satisfying the lemma's hypothesis falls into exactly one of the four rows; the impossible row is excluded by the chain above, so every such `(a, d)` lies in one of the three remaining rows and receives exactly one classification. ∎

## Why the Provenance Relation Is Load-Bearing

We now show that the four foundation state components `(C, L, E, M)` together are insufficient to support SHOWDELETIONS — any conforming implementation must maintain auxiliary state components beyond `(C, L, E, M)` that suffice to disambiguate the predicates `DELETED(a, d)` and `NEVER_INCLUDED(a, d)` at every reachable state.

**Lemma D-DISCR (Discrimination Requires Provenance).** No function computable from `(Σ.C, Σ.L, Σ.E, Σ.M)` alone can distinguish `DELETED(a, d)` from `NEVER_INCLUDED(a, d)` for arbitrary `(a, d)`.

*Argument.* We exhibit two reachable states `Σ_1` and `Σ_2` for which `(Σ.C, Σ.L, Σ.E, Σ.M)` agree across every document but `DELETED(a, d)` and `NEVER_INCLUDED(a, d)` disagree.

*Notational convention.* In the histories below, each `→*` arrow denotes one valid composite under ValidComposite★ (ASN-0047); line breaks are visual aids only, and composite groupings are determined by the coupling requirements of the elementary steps. In particular, K.α must be bundled with an immediately-following K.μ⁺/K.ρ pair into a single composite, because K.α's frame leaves `M` unchanged — a standalone-K.α composite would produce `a ∈ dom(C') \ dom(C)` without placing `a` in any arrangement, violating J0 (AllocationRequiresPlacement, ASN-0047). The bundling pattern matches the worked example above.

A second bundling concerns document creation. K.δ case (ii) with `k = 2` (descent) requires `t ∈ E ∧ zeros(t) ≤ 1`. From `Σ_0` (where the only entity is the bootstrap node `n_0` with `zeros(n_0) = 0`), a single elementary K.δ step produces at most an account (`zeros = 1`). Producing a document (`zeros = 2`) requires a precursor account-creation step. We therefore use `K.δ(d)` as shorthand for a composite containing whatever precursor K.δ steps are needed to satisfy the entity-hierarchy preconditions — for example, the composite `K.δ(A); K.δ(d)` where `A = inc(n_0, 2)` is the account and `d = inc(A, 2)` is the document. The composite is valid by ValidComposite★: each elementary step satisfies its precondition at its intermediate state, and J0/J1★/J1'★ are vacuous because no K.α, K.μ⁺, or K.ρ steps appear. The same convention applies to `K.δ(d_A)` and `K.δ(d_B)` in the worked example below.

Both histories begin at the initial state `Σ_0` (ASN-0047) and share the prefix `K.δ(d); K.δ(d')` — creating two documents `d, d'`. Both then invoke K.α(a, d) to allocate one content address. By K.α's first-emission rule (`{a' ∈ dom(C) : origin(a') = d} = ∅` initially), the allocated address is determinately `a = [d.0.s_C.1]` — a value fixed by `d` alone. Both histories pass the same `d` to the first-emission predicate, so both yield the same allocated address `a`. The histories then differ in where `a` is placed and which provenance pairs are recorded.

*History 1 (yields DELETED).*

```
Σ_0  →* K.δ(d)
     →* K.δ(d')
     →* K.α(a, d);   K.μ⁺(d,  v  ↦ a);  K.ρ(a, d)
     →* K.μ⁺(d', v' ↦ a);  K.ρ(a, d')
     →* K.μ⁻(d)              [retain n'_{s_C} = 0]
     =   Σ_1
```

The third composite bundles K.α with K.μ⁺(d, v ↦ a) and K.ρ(a, d): K.α produces `a ∈ dom(C')`, K.μ⁺ places `a` in `M(d)` (discharging J0), and K.ρ records `(a, d) ∈ R'` (discharging J1★, since K.μ⁺'s frame leaves `R` unchanged on its own). The fourth composite extends `M(d')` with the same `a` at `v' = [s_C, 1]` and pairs it with K.ρ(a, d') so the composite discharges J1★ end-to-end. The K.μ⁻ step on `d` retains zero content-subspace V-positions (`n'_{s_C} = 0`), removing `v ↦ a` from `M(d)`; by P2 (`R ⊆ R'`), `(a, d) ∈ R_1` persists. Final state: `dom(C_1) = {a}`, `M_1(d) = ∅`, `M_1(d') = {v' ↦ a}`, `(a, d) ∈ R_1`. So `DELETED(a, d)` holds at `Σ_1`.

*History 2 (yields NEVER_INCLUDED).*

```
Σ_0  →* K.δ(d)
     →* K.δ(d')
     →* K.α(a, d);   K.μ⁺(d', v' ↦ a);  K.ρ(a, d')
     =   Σ_2
```

The third composite bundles K.α with K.μ⁺(d', v' ↦ a) and K.ρ(a, d'): K.α produces `a ∈ dom(C')`, K.μ⁺ places `a` in `M(d')` (discharging J0 — J0 requires placement in *some* document's arrangement, not specifically in the origin's), and K.ρ records `(a, d') ∈ R'` (discharging J1★). The composite records `(a, d') ∈ R_2`, but `d` is never extended with `a`, so `(a, d) ∉ R_2`. Final state: `dom(C_2) = {a}`, `M_2(d) = ∅`, `M_2(d') = {v' ↦ a}`, `(a, d) ∉ R_2`. So `NEVER_INCLUDED(a, d)` holds at `Σ_2`.

*Agreement on (C, L, E, M).* Comparing the components of `Σ_1` and `Σ_2`:

| Component | `Σ_1` | `Σ_2` |
|---|---|---|
| `dom(C)` | `{a}` | `{a}` |
| `C` value at `a` | the K.α-supplied value `v_a` | same |
| `L` | `∅` | `∅` |
| `E` | `{n_0, …, d, d'}` | `{n_0, …, d, d'}` |
| `E_doc` | `{d, d'}` | `{d, d'}` |
| `M(d)` | `∅` | `∅` |
| `M(d')` | `{v' ↦ a}` | `{v' ↦ a}` |

Neither history invokes K.λ, so `L_1 = L_2 = ∅`. Both histories execute the same K.δ sequence to create `d` and `d'`, so `E_1 = E_2` (entities are permanent by P1, and no entity-creating step distinguishes the two). `(Σ_1.C, Σ_1.L, Σ_1.E, Σ_1.M) = (Σ_2.C, Σ_2.L, Σ_2.E, Σ_2.M)` on every component. The histories differ only in `R`: `R_1 ⊇ {(a, d), (a, d')}` and `R_2 ⊇ {(a, d')}`, with `(a, d) ∈ R_1 \ R_2`.

Any function `f(C, L, E, M)` returns the same value at both states. But the classifications differ — `DELETED(a, d)` at `Σ_1`, `NEVER_INCLUDED(a, d)` at `Σ_2` — so `f` cannot be a discriminating predicate. ∎

This is the abstract justification for the provenance relation. The negative result is sharp in its full strength: the witnesses pin every component of `(C, L, E, M)` identically across `Σ_1` and `Σ_2`, so no projection or joint consultation of the four foundation components suffices to discriminate. Any system supporting SHOWDELETIONS must therefore maintain state components `C*` *beyond* `(C, L, E, M)`. For every reachable state `Σ` and every pair `(a, d)` with `a ∈ dom(C)` and `d ∈ E_doc`, consulting `(C, L, E, M, C*)` at `Σ` must determine whether `(a, d)` is `DELETED` or `NEVER_INCLUDED`. `R` as defined in ASN-0047 is one such `C*`; the necessity claim is that *some* `C*` adequate to discharge this disambiguation must be present, regardless of its specific representation.

## The SHOWDELETIONS Operation

Let `d_A, d_B ∈ E_doc`. The operation takes two documents and observes the state. We define the asymmetric output sets:

```
DeletedFromAWithB(d_A, d_B)
   =  {a ∈ dom(C) :
         subspace_I(a) = s_C
       ∧ DELETED(a, d_A)
       ∧ CURRENT(a, d_B)}

DeletedFromBWithA(d_A, d_B)
   =  {a ∈ dom(C) :
         subspace_I(a) = s_C
       ∧ DELETED(a, d_B)
       ∧ CURRENT(a, d_A)}
```

Each asymmetric set captures content deleted from one document and still arranged in the other. The presence of the "witness" document (where the content remains current) is what makes the deletion observable as recoverable: every `a` in `DeletedFromAWithB` is reachable through `d_B`'s current view, and the reverse holds symmetrically.

**Definition (SHOWDELETIONS).** The operation is the ordered pair:

```
SHOWDELETIONS(d_A, d_B)
   =  (DeletedFromAWithB(d_A, d_B), DeletedFromBWithA(d_A, d_B))
```

The two halves are necessarily disjoint: by D-EXH, no `a` can simultaneously satisfy `DELETED(a, d_A)` and `CURRENT(a, d_A)`, so an address `a` in `DeletedFromAWithB` cannot be in `DeletedFromBWithA` (the former requires `CURRENT(a, d_B)`, the latter `DELETED(a, d_B)`).

The operation's precondition is `d_A ∈ E_doc ∧ d_B ∈ E_doc`. Its postcondition characterises the result set-theoretically. We capture this in wp form. Let `q` abbreviate the predicate:

```
Result = (DeletedFromAWithB(Σ, d_A, d_B), DeletedFromBWithA(Σ, d_A, d_B))
```

Then `wp(SHOWDELETIONS(d_A, d_B), q) = (d_A ∈ E_doc ∧ d_B ∈ E_doc)`. The operation always terminates with `q` true when its precondition holds.

Because SHOWDELETIONS is observational (D-OBS below), wp computations for state-level predicates pass through unchanged from the pre-state: `wp(SHOWDELETIONS, P) = (precondition) ∧ P(Σ)` whenever `P` depends only on `Σ`. Two state-level postconditions are worth deriving explicitly, since they characterise *when* the operation surfaces structurally meaningful facts.

*Non-emptiness of one report half.* Let `Q1` abbreviate `DeletedFromAWithB(d_A, d_B) ≠ ∅`. Unpacking the definition of `DeletedFromAWithB`:

```
wp(SHOWDELETIONS(d_A, d_B), Q1)
   =  d_A ∈ E_doc  ∧  d_B ∈ E_doc
    ∧  (E a ∈ dom(C) :  subspace_I(a) = s_C
                       ∧ (a, d_A) ∈ R
                       ∧ a ∉ ran(M(d_A))
                       ∧ a ∈ ran(M(d_B)))
```

So `DeletedFromAWithB` is non-empty exactly when some content address inhabits `d_A`'s history through `R`, has been removed from `d_A`'s current arrangement, and remains in `d_B`'s current arrangement. The fourth conjunct (presence in `d_B`) is what makes the report *recoverable* in the sense of D-IDENT below — every reported deletion has a concrete witness in the partner document. This is not an additional postcondition; it is implicit in the definition of `DeletedFromAWithB`.

*Vacuity of both report halves.* Let `Q0` abbreviate `DeletedFromAWithB(d_A, d_B) = ∅ ∧ DeletedFromBWithA(d_A, d_B) = ∅`. Then:

```
wp(SHOWDELETIONS(d_A, d_B), Q0)
   =  d_A ∈ E_doc  ∧  d_B ∈ E_doc
    ∧  (A a ∈ dom(C) :  subspace_I(a) = s_C :
            ¬(DELETED(a, d_A)  ∧  CURRENT(a, d_B))
          ∧ ¬(DELETED(a, d_B)  ∧  CURRENT(a, d_A)))
```

The joint report is empty exactly when no content has been deleted from one document while remaining current in the other. Documents with disjoint `R`-projections on the content subspace — `{a : (a, d_A) ∈ R} ∩ {a : (a, d_B) ∈ R} = ∅` — satisfy `Q0`. For any `a` with `(a, d_A) ∈ R`, disjointness gives `(a, d_B) ∉ R`; for the conjunct `DELETED(a, d_A) ∧ CURRENT(a, d_B)` to hold, `CURRENT(a, d_B)` requires `a ∈ ran(M(d_B))`, which by `P4★` forces `(a, d_B) ∈ R` — contradiction. The symmetric argument excludes `DELETED(a, d_B) ∧ CURRENT(a, d_A)` for any `a` with `(a, d_B) ∈ R`. Addresses with neither `(a, d_A) ∈ R` nor `(a, d_B) ∈ R` are classified `NEVER_INCLUDED` against both documents and trivially satisfy both negations. So every `a ∈ dom(C)` falsifies both conjuncts, and `Q0` holds. The argument covers the special case of one or both `R`-projections being empty without separate handling. Documents with synchronised edits (each deletion mirrored in the partner) satisfy `Q0` non-vacuously: for shared content, removal from one is matched by removal from the other.

## A Worked Example

We illustrate SHOWDELETIONS on the canonical scenario: a document is forked, and the two siblings diverge by each deleting different content. The claims D-EXH, D-IDENT, D-ORIG, and D-SYM can be checked concretely against the resulting state.

*Setup.* Begin at `Σ_0` (the initial state of ASN-0047) and apply the composite

```
Σ_0  →* K.δ(d_A)
     →* K.α(a, d_A);  K.μ⁺(d_A, [1,1] ↦ a);  K.ρ(a, d_A)
     →* K.α(b, d_A);  K.μ⁺(d_A, [1,2] ↦ b);  K.ρ(b, d_A)
     →* K.α(c, d_A);  K.μ⁺(d_A, [1,3] ↦ c);  K.ρ(c, d_A)
     →* K.δ(d_B)                                                  [d_B = inc(d_A, 1)]
     →* K.μ⁺(d_B, [1,1] ↦ a, [1,2] ↦ b, [1,3] ↦ c);  K.ρ(a, d_B);  K.ρ(b, d_B);  K.ρ(c, d_B)
     →* K.μ~(d_A)  [permute so c at [1,2], b at [1,3]]
     →* K.μ⁻(d_A)  [retain n'_{s_C} = 2 of content subspace]
     →* K.μ⁻(d_B)  [retain n'_{s_C} = 2 of content subspace]
     =   Σ
```

The first four lines create `d_A` with three content addresses `a, b, c` (all with `origin = d_A` by S7), arranged at `[1,1], [1,2], [1,3]`; the per-line K.ρ steps record the corresponding provenance, with each `K.μ⁺; K.ρ` bundle satisfying J1★ end-to-end (K.μ⁺'s frame leaves `R` unchanged on its own, so K.ρ is what supplies the provenance update the coupling demands). Line 5 forks `d_A` to `d_B = inc(d_A, 1)` (K.δ case (ii), `k = 1`); line 6 populates `d_B` by transclusion — the *same* I-addresses `a, b, c` are referenced from `d_B`'s V-positions — and records the three accompanying provenance pairs in one composite. The resulting provenance relation contains `R ⊇ {(a, d_A), (b, d_A), (c, d_A), (a, d_B), (b, d_B), (c, d_B)}`.

The last three lines effect a divergent edit. Lines 7–8 reorder `M(d_A)` to put `b` at the trailing position `[1,3]` and then truncate, removing `b` from `d_A`'s arrangement. Line 9 removes `c` from `d_B`'s arrangement directly — no prior rearrangement is needed because `c` is already at the trailing position `[1,3]`, so K.μ⁻ retaining the first two content positions drops exactly `c`. By P2, the deletions leave `R` unchanged.

*Resulting state.*

| Component | Value |
|---|---|
| `dom(C)` | `{a, b, c}` |
| `origin` | `origin(a) = origin(b) = origin(c) = d_A` |
| `E_doc` | `{d_A, d_B}` |
| `M(d_A)` | `{[1,1] ↦ a, [1,2] ↦ c}` |
| `M(d_B)` | `{[1,1] ↦ a, [1,2] ↦ b}` |
| `R ⊇` | `{(a, d_A), (b, d_A), (c, d_A), (a, d_B), (b, d_B), (c, d_B)}` |

*Classifying each pair.* For each of the six pairs `(x, d) ∈ {a, b, c} × {d_A, d_B}`, D-EXH yields a unique classification:

| Pair | `x ∈ ran(M(d))?` | `(x, d) ∈ R?` | Class |
|---|---|---|---|
| `(a, d_A)` | yes | yes | CURRENT |
| `(b, d_A)` | no  | yes | DELETED |
| `(c, d_A)` | yes | yes | CURRENT |
| `(a, d_B)` | yes | yes | CURRENT |
| `(b, d_B)` | yes | yes | CURRENT |
| `(c, d_B)` | no  | yes | DELETED |

*Computing the output.*

```
DeletedFromAWithB(d_A, d_B)  =  {x ∈ dom(C) : DELETED(x, d_A) ∧ CURRENT(x, d_B)}  =  {b}
DeletedFromBWithA(d_A, d_B)  =  {x ∈ dom(C) : DELETED(x, d_B) ∧ CURRENT(x, d_A)}  =  {c}
SHOWDELETIONS(d_A, d_B)       =  ({b}, {c})
```

Only `b` is deleted from `d_A` while remaining in `d_B`; only `c` is deleted from `d_B` while remaining in `d_A`. The shared content `a` is current in both and reported in neither half.

*Verifying the claims on this state.*

- *D-EXH.* The classification table assigns each pair exactly one class; mutual exclusion is by construction (DELETED requires `x ∉ ran(M(d))`, CURRENT requires `x ∈ ran(M(d))`).
- *D-IDENT.* The returned `b` is the same I-address that inhabits `dom(C)` and `ran(M(d_B))` — no value has been copied into a new tumbler. The same holds for `c`.
- *D-ORIG.* `origin(b) = origin(c) = d_A`, derivable from the tumblers themselves via S7. The output addresses self-identify their allocator.
- *D-SYM.* Applying the definition with operands swapped, `DeletedFromAWithB(d_B, d_A) = {x : DELETED(x, d_B) ∧ CURRENT(x, d_A)} = {c}` and `DeletedFromBWithA(d_B, d_A) = {b}`. So `SHOWDELETIONS(d_B, d_A) = ({c}, {b})` — the component-swap of `SHOWDELETIONS(d_A, d_B)`.

The example also illustrates the structural significance of the witness: `b` is reported as deleted from `d_A` only because `d_B` still holds it; if `d_B` had also deleted `b`, the pair `(b, d_A)` would still be DELETED, but `b` would not appear in `DeletedFromAWithB` because the witness condition `CURRENT(b, d_B)` would fail. Cross-document SHOWDELETIONS exposes exactly the asymmetric losses — deletions that one document made and the other did not.

## Distinguishing Deletions from Additions

A naive set-difference of current ranges — `ran(M(d_A)) \ ran(M(d_B))` — would conflate two distinct phenomena: content `d_A` had that `d_B` deleted, and content `d_A` acquired (e.g., through insertion or transclusion) that `d_B` never received. The "show deletions" name and intent target only the former.

Our definition forces the disambiguation by requiring `(a, d_A) ∈ R` for content reported as deleted-from-A. This says: `a` must have been in `d_A`'s arrangement at some point. Content that was only ever in `d_B`'s arrangement satisfies `NEVER_INCLUDED(a, d_A)` rather than `DELETED(a, d_A)`, and is correctly excluded from the deletion report.

The same set-theoretic difference computed without `R` would mislabel additions as deletions. The provenance-aware definition above is therefore not optional — it is what makes the operation deliver on its name.

## Restriction to the Content Subspace

The condition `subspace_I(a) = s_C` is essential.

**Claim D-SUBSP.** SHOWDELETIONS operates only over the content subspace (`s_C`).

*Justification.* Content-subspace addresses can be shared between documents because the system permits one document's content arrangement to map V-positions to I-addresses allocated by another document — content identity transcends document boundaries within the content subspace.

The link subspace differs structurally. By CL-OWN (ASN-0047), if `subspace(v) = s_L` and `M(d)(v) = a`, then `origin(a) = d`: a document's link-subspace V-positions reference only its own link addresses. There is no inheritance of link content across documents in the way that there is for content. So "cross-document deletion of link material" is not a well-formed comparison — each document's link-subspace material is its own, and no comparison document holds it as witness.

Restricting SHOWDELETIONS to the content subspace is therefore not an implementation simplification but a structural necessity. The link subspace requires a separate (and per-document, not cross-document) analysis.

## Identity Preservation

**Claim D-IDENT.** For every `a` in either output set, the returned reference is precisely the I-address `a` — not a copy with new identity.

*Justification.* The output sets are defined as subsets of `dom(C)`. Each element is an existing I-address. We return addresses, not values.

The architectural significance is foundational. An operation that recovers content using these references dereferences existing entries in `C`; it does not allocate new ones. Three guarantees that depend on persistent I-address identity therefore survive recovery:

- *Link survival.* By L3 (NEndsetStructure, ASN-0047) together with the link-store definition `L : T ⇀ Endset^N`, every link in `dom(L)` references content through endset spans whose entries are I-addresses; the address `a` is the link's referent. By P3 (ArrangementMutabilityOnly, ASN-0047), `L` is preserved across all transitions — `L' = L` for every K.μ⁺/K.μ⁻/K.μ~ — so a link whose endset names `a` continues to name the same `a` regardless of which arrangements currently expose it.
- *Transclusion integrity.* By S2 (ArrangementFunctionality, ASN-0036) and S3★ (GeneralizedReferentialIntegrity, ASN-0047), arrangements reference I-addresses by tumbler identity: each V-position maps to a determinate `a ∈ dom(C)`. If another document's arrangement maps a V-position to `a`, that mapping continues to reference the same `a` because P0 (ContentPermanence, ASN-0047, subsuming S0 of ASN-0036) preserves both `dom(C)` and the value at every existing entry across all transitions; no aliasing or shadow copy is introduced.
- *Origin attribution.* By S7 (StructuralAttribution, ASN-0036), `origin(a)` is derivable from `a`'s tumbler alone and is invariant across all states in which `a ∈ dom(C)`. The chain of provenance is not severed by recovery.

If SHOWDELETIONS returned new identities — fresh I-addresses with the same byte values — all three guarantees would collapse. The recovered content would be unaddressable by existing links, would not match existing transclusions, and would have spurious new origin. Returning addresses is therefore not a presentation choice; it is a correctness requirement.

## Origin Traceability

**Claim D-ORIG.** For every `a` in either output set, `origin(a)` is determined and identifies a unique document — the originating allocator of `a`.

*Justification.* By S7 (ASN-0036), `origin(a)` is defined for every `a ∈ dom(C)` and is invariant across all states in which `a ∈ dom(C)`. The output sets are subsets of `dom(C)`, so `origin` is well-defined on every output element.

The user-facing meaning: any returned address self-identifies its home document. When `d_A` and `d_B` were derived from a common ancestor `d_C`, content inherited from `d_C` and later deleted from `d_A` carries `origin(a) = d_C`. Content originally allocated by some other document and transcluded into `d_A` before deletion carries that other document's address as origin. The output need carry no extra "origin annotation" beyond the address itself — origin is derived structurally from the address.

This matters operationally because it scopes recovery rights and accounting. The originating document is recoverable from the address; recovery operations can verify permissions against `origin`; royalty or attribution mechanisms have the data they need.

## Order Preservation

**Claim D-ORD.** If the output is presented as an ordered sequence, the order is consistent with the witness document's V-position ordering of the referenced addresses.

For `DeletedFromAWithB(d_A, d_B)`, define `vpos_B(a) = min{v ∈ dom(M(d_B)) : M(d_B)(v) = a}` under T1. The set `{v ∈ dom(M(d_B)) : M(d_B)(v) = a}` is finite (a subset of `dom(M(d_B))`, finite by S8-fin) and non-empty when `a ∈ ran(M(d_B))`, so the minimum exists. We use the minimum rather than asserting uniqueness because S5 (UnrestrictedSharing, ASN-0036) permits a single I-address to occupy multiple V-positions within one document — S2 establishes that `M(d_B)` is a function (each V-position maps to at most one I-address) but does *not* preclude its inverse from being multi-valued. The minimum under T1 is a canonical representative chosen deterministically from whatever multiplicity the arrangement contains. The output is ordered such that for any `a, a'` with `vpos_B(a) < vpos_B(a')` under T1 (ASN-0034), `a` precedes `a'` in the presentation. Symmetrically for `DeletedFromBWithA` using `vpos_A(a) = min{v ∈ dom(M(d_A)) : M(d_A)(v) = a}`.

*Justification.* Deleted content has no V-position in the document from which it was deleted: V-position information is local to a current arrangement and is not preserved by `R`. So the deleted document's "original ordering" of the content is not observable in the current state — it was a property of an arrangement no longer present. The only observable V-ordering is the witness document's. Choosing the witness order for presentation is the only choice that uses observable data.

We note explicitly what is *not* claimed: the order in which `a` appeared in `d_A` before deletion is *not* recoverable. A user who needs to act on the content reads it in the witness's order — which is convenient, because that is also the order in which it appears when accessed through the witness.

## Symmetry

**Claim D-SYM.** Argument swap maps each output half into the other:

```
SHOWDELETIONS(d_A, d_B)  =  (X, Y)
SHOWDELETIONS(d_B, d_A)  =  (Y, X)
```

where `X = DeletedFromAWithB(d_A, d_B)` and `Y = DeletedFromBWithA(d_A, d_B)`.

*Justification.* By name-substitution in the definitions: `DeletedFromAWithB(d_B, d_A)` reads as "addresses with `DELETED(a, d_B) ∧ CURRENT(a, d_A)`," which is exactly `DeletedFromBWithA(d_A, d_B)`. Likewise the other half.

The content-level guarantee — the union of both halves as a set of I-addresses — is therefore symmetric in the operands. The presentation labelling (which half is "from A" vs. "from B") swaps accordingly. This matches the design intent that correspondence between documents is a structural fact about shared content and not an asymmetric query over arguments.

## Actionability

**Claim D-ACT.** The output is in a form usable as input to any operation that consumes I-addresses to produce arrangement extensions.

*Justification.* Each output element is an I-address in `dom(C)`. Any operation whose input type accepts I-addresses (or spans thereof) can consume the output directly. The output is *not* wrapped in V-position structure — wrapping it that way would require either fictitious positions (deleted content has no V-position in the queried document) or borrowed positions from the witness (which would have to be coordinated with the recovery target's address space, an entanglement the abstract output cannot impose). The output is *not* wrapped in content values — wrapping it that way would require copying values into new identities, breaking D-IDENT.

The natural compact form is therefore a set of I-spans, each tagged with the originating document so that contiguous runs sharing the same origin can be grouped. Formally, drawing on the span and bundle algebras:

A *deletion witness run* is a triple `(i_start, ℓ, origin)` such that, using the OrdinalShift of ASN-0034:

- every address in `{i_start, shift(i_start, 1), …, shift(i_start, ℓ − 1)}` belongs to the deletion set;
- every such address satisfies `origin(a) = origin`;
- no contiguous extension to the left or right is also in the deletion set with the same origin.

The decomposition into maximal witness runs is uniquely determined by the deletion set itself. The deletion set is finite (a subset of `dom(C)`, finite by C-fin, ASN-0047) and totally ordered under T1 (ASN-0034). Define adjacency on the deletion set: two addresses `a, a'` are *I-adjacent* iff (`a' = shift(a, 1)` or `a = shift(a', 1)`) and `origin(a) = origin(a')`. I-adjacency is symmetric by construction; its reflexive-transitive closure is therefore an equivalence relation, which partitions the deletion set into equivalence classes. Each class is a maximal `T1`-contiguous run of addresses sharing one origin — a witness run. Within `dom(C)`, every content address has element-field length 2 — each `A_C(d)` emits via `inc(·, 0)` from the length-2 first emission `[d.0.s_C.1]`, and `inc(·, 0)` preserves length by TA5(c) of ASN-0034 — giving total tumbler length `L_d + 3` where `L_d = #d`. To establish that no `t ∈ dom(C)` lies strictly between consecutive emissions `a = [d.0.s_C.k]` and `a' = shift(a, 1) = [d.0.s_C.k+1]` of `A_C(d)` under T1, we split on `origin(t)`:

- *Same origin, same length* (`origin(t) = d`, `#t = L_d + 3`). Then `t` shares the prefix `[d.0.s_C]` with `a` and `a'` (every emission of `A_C(d)` does). The three tumblers agree on positions 1 through `L_d + 2`, so T1 reduces to the last component: `a < t < a'` forces `k < t_{L_d+3} < k + 1`, which T0 discreteness on ℕ excludes.
- *Longer length* (`#t > L_d + 3`). For `a < t < a'` to coexist with `#t > #a = #a'`, T1 forces `t` to extend `a`'s prefix `[d.0.s_C.k]`: any divergence at a position `j ≤ L_d + 3` would place `t` strictly outside `[a, a']` (divergence with `t_j > a_j` at `j < L_d + 3` gives `t_j > a'_j` since `a` and `a'` agree there, so `t > a'`; divergence at `j = L_d + 3` either falls in the impossible gap by T0 discreteness or forces `t_{L_d+3} ≥ k+1 = a'_{L_d+3}`, giving `t ≥ a'`). So `t = [d.0.s_C.k.x_1.x_2 …]` for some non-empty positive-component suffix. By S7 (ASN-0036), `origin(t) = N.0.U.0.D = d` (the three zeros of `t` are exactly those of `d.0.s_C`, so T4b's element-field projection truncates to give the same document-level prefix as `a`). So `t ∈ dom(C)` with `origin(t) = d` requires `t` to have been emitted by `A_C(d)` — but every emission of `A_C(d)` has element-field length exactly 2 (universality of `#E = 2` across the allocator's stream), forcing `#t = L_d + 3`, contradicting `#t > L_d + 3`.
- *Different origin* (`origin(t) = d' ≠ d`). The document-level prefixes `d` and `d'` are distinct, so T1 lexicographic comparison applied to `d` and `d'` (with the prefix branch handling the nested case `d ≺ d'` or `d' ≺ d`: at position `min(L_d, L_{d'}) + 1` the shorter prefix's extension carries a zero separator while the longer prefix carries a non-zero component) fixes some position `p` at which every emission of `A_C(d)` carries `d`'s component and every emission of `A_C(d')` carries `d'`'s component, with both prefixes agreeing on positions before `p`. So every emission of one allocator T1-precedes every emission of the other, and `t` cannot lie strictly between two emissions of `A_C(d)`.

In every case, no `t ∈ dom(C)` lies strictly between `a` and `a'`. Shift-adjacency within one allocator's stream therefore implies T1-consecutiveness in `dom(C)`, making each I-adjacency equivalence class T1-contiguous within `dom(C)`. The partition is unique because I-adjacency is determinate: `shift(·, 1)` is a function (OrdinalShift, ASN-0034) and `origin` is a function on `dom(C)` (S7, ASN-0036), so for any pair `(a, a')` in the deletion set the adjacency predicate evaluates to a fixed truth value. The partition is finite because the deletion set is finite. We emphasise that this decomposition is on the deletion set viewed as an I-set — it is not the V→I block decomposition of any document's arrangement (ASN-0058, M11–M12); two I-adjacent same-origin addresses may be non-V-adjacent in any particular witness's arrangement, and V-adjacent positions in a witness's arrangement may map to non-I-adjacent or different-origin addresses, so the two notions of "run" do not coincide. The witness-run collection can be enumerated, transmitted, and consumed without information loss.

We emphasise: this presentation is a *form*, not a *fundamental commitment*. The abstract specification fixes only the set of I-addresses. The run-grouping presentation is a useful packaging that preserves identity (every position is its original I-address) and origin (every address shares the named origin), making the output efficient to transmit while remaining compositional.

## Observational Frame

**Claim D-OBS.** SHOWDELETIONS does not modify any state component.

Formally, for state `Σ = (C, L, E, M, R)` and the state `Σ'` obtaining after the operation:

```
Σ'.C  =  Σ.C
Σ'.L  =  Σ.L
Σ'.E  =  Σ.E
Σ'.R  =  Σ.R
(A d ∈ E_doc ::  Σ'.M(d) = Σ.M(d))
```

The operation reads `M(d_A)`, `M(d_B)`, and `R`; it computes the output sets; it returns them. No transition relation is invoked.

Consequences: SHOWDELETIONS is repeatable on the same state (yields identical results); it commutes with other observational queries; and a later invocation after intervening state changes correctly reflects the new state.

## Output Need Not Be Stored

**Claim D-STORE.** The output is not required to be stored as a document or otherwise integrated into the persistent content store.

*Justification (negative claim).* SHOWDELETIONS is observational (D-OBS); its result is delivered to the caller. The caller may inspect, transform, retain, or discard the result. The system does not, of its own accord, create a new document or other persistent artefact to hold the result.

If a user wishes to capture a particular SHOWDELETIONS result for sharing or future reference, they have separate mechanisms for doing so: they may compose a new document whose arrangement transcludes the recovered I-spans (using D-IDENT's identity preservation), or they may establish correspondence assertions between the two compared documents. These captures are user actions, not built-in obligations of SHOWDELETIONS.

The justification for keeping the operation observational rather than constructive: SHOWDELETIONS is a function of state (D-RECONS below). Functions can be recomputed from their inputs whenever needed. Storing the result would buy persistence at the cost of staleness — any subsequent state change makes a stored result potentially out of date. The system is more flexible with observation than with creation.

## State-Functional Independence

**Claim D-RECONS.** The output depends only on the current state `Σ`. It does not depend on the particular sequence of transitions by which `Σ` was reached.

*Justification.* Each predicate `CURRENT`, `DELETED`, `NEVER_INCLUDED` is defined in terms of components of `Σ` only (`M`, `R`, `dom(C)`, `subspace_I`). The output sets are characterised entirely by these projections. Two distinct transition histories yielding the same `Σ` therefore yield identical SHOWDELETIONS outputs.

This is what makes the operation an honest function of state. The user need not know how the system arrived at its current configuration; consulting the current configuration suffices. P4a (historical fidelity, ASN-0047) ensures that whenever the operation reports `DELETED(a, d)`, there really was a past state where `a` was in `d`'s arrangement — but the *route* to that past state is irrelevant to the report itself.

## Edge Cases

*Documents with no shared content.* If for every `a ∈ dom(C)`, `¬((a, d_A) ∈ R ∧ a ∈ ran(M(d_B)))` and `¬((a, d_B) ∈ R ∧ a ∈ ran(M(d_A)))`, then no address satisfies either asymmetric definition. Both output halves are empty. The operation succeeds and reports no deletions — correctly so, because the documents have no shared content history through which one could witness deletions in the other.

*Both arrangements empty.* If `dom(M(d_A)) = dom(M(d_B)) = ∅`, then `ran(M(d_A)) = ran(M(d_B)) = ∅`, so `CURRENT` fails for every `a` on both sides. Both halves are empty.

*Same document compared against itself.* If `d_A = d_B`, then for each `a`, `DELETED(a, d_A) ∧ CURRENT(a, d_A)` is contradictory (by D-EXH). Both halves are empty. The operation is well-defined and trivially yields the empty pair.

*Asymmetric population.* If `d_A` has rich history (large `R`-projection) but its current arrangement is empty, while `d_B`'s arrangement currently holds many of the addresses `d_A` historically held, then `DeletedFromAWithB` may be large and `DeletedFromBWithA` may be empty. The asymmetry of the two halves directly mirrors the asymmetry of the editing histories.

## Composability with Restoration

While we do not specify any restoration operation here, we note that the output's form makes restoration *possible*. The output is a set of I-addresses in `dom(C)`, each carrying determinate origin (D-ORIG) and preserving identity (D-IDENT). A restoration operation consuming a subset of these addresses can extend a target document's arrangement to include them at fresh V-positions, with `origin` and link-resolvability preserved because no new identities are introduced.

The user-facing meaning: a "show deletions" query feeds naturally into a "bring back this part" follow-up, with no loss of identity in the round trip. That is what makes the operation more than diagnostic.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| CURRENT | `CURRENT(a, d) ≡ a ∈ ran(M(d))` | introduced |
| DELETED | `DELETED(a, d) ≡ (a, d) ∈ R ∧ a ∉ ran(M(d))` | introduced |
| NEVER_INCLUDED | `NEVER_INCLUDED(a, d) ≡ (a, d) ∉ R` | introduced |
| D-EXH | For every reachable state Σ and every `(a, d)` with `a ∈ dom(Σ.C)`, `subspace_I(a) = s_C`, `d ∈ Σ.E_doc`, exactly one of CURRENT, DELETED, NEVER_INCLUDED holds | introduced |
| D-DISCR | No function of `(C, L, E, M)` alone can distinguish DELETED from NEVER_INCLUDED; any system supporting SHOWDELETIONS must maintain state components `C*` beyond the four foundation components such that consulting `(C, L, E, M, C*)` at every reachable Σ determines whether each `(a, d)` is DELETED or NEVER_INCLUDED | introduced |
| DeletedFromAWithB | `{a ∈ dom(C) : subspace_I(a) = s_C ∧ DELETED(a, d_A) ∧ CURRENT(a, d_B)}` | introduced |
| DeletedFromBWithA | Symmetric counterpart of DeletedFromAWithB | introduced |
| SHOWDELETIONS | Observational operation `SHOWDELETIONS(d_A, d_B) = (DeletedFromAWithB(d_A, d_B), DeletedFromBWithA(d_A, d_B))` | introduced |
| D-SUBSP | The operation restricts to the content subspace `s_C`; cross-document deletion comparison is structurally meaningful only there | introduced |
| D-IDENT | Output references are I-addresses themselves; no copies, no new identities | introduced |
| D-ORIG | Every output element `a` has determinate `origin(a)` | introduced |
| D-ORD | Output presentation, when ordered, is consistent with the witness document's V-position ordering | introduced |
| D-SYM | `SHOWDELETIONS(d_B, d_A)` is the component-swapped pair of `SHOWDELETIONS(d_A, d_B)` | introduced |
| D-ACT | Output is in a form consumable by I-address-based operations; deletion witness runs `(i_start, ℓ, origin)` are the natural compact form | introduced |
| D-OBS | SHOWDELETIONS modifies no state component; it is purely observational | introduced |
| D-STORE | The output is not required to be stored as a document; it is a query result | introduced |
| D-RECONS | The output depends only on the current state, not on transition history | introduced |
| DeletionWitnessRun | Triple `(i_start, ℓ, origin)` denoting a maximal contiguous I-address run in the deletion set sharing one originating document | introduced |

## Open Questions

What abstract characterisation of "shared content history" between two documents, expressed solely in terms of R, predicts when SHOWDELETIONS will yield non-empty results?

When deleted content has been removed from every document that ever contained it, through what state component does the system still retain the option to expose it for query or recovery?

How should SHOWDELETIONS report content that was deleted from both compared documents but remains current in a third document not in the pair?

If the system supports concurrent state transitions, what consistency model must SHOWDELETIONS observe to deliver coherent joint snapshots of M and R?

How does SHOWDELETIONS generalise to families of more than two documents, and what witness-structure replaces the binary asymmetric pair?

Under what conditions on the witness arrangement does the deletion set admit a finite presentation as a union of contiguous I-address spans, and when must it enumerate addresses singly?

What guarantees must the witness's V-order satisfy to ensure that presentation-ordered output of SHOWDELETIONS corresponds to a user-meaningful reading sequence rather than a structural accident?

Should the system distinguish content "deleted with a witness in a prior arrangement of the same document" from "deleted with a witness in a sibling document," and what additional structure would that distinction require?
