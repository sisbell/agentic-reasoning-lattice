# ASN-0075: SHOWDELETIONS Operation

*2026-05-25*

Nelson lists "show deletions" among the operations the system must provide (LM 4/79). The intuition is direct: given two documents that share content history, identify the content that was present in one but is absent from the other. We approach this abstractly. We do not specify how documents come to share history, nor how content is removed from an arrangement — those mechanics belong elsewhere. We specify only what the operation must produce, what guarantees it must offer over its output, and what state it consults.

The central difficulty is that two situations are observationally indistinguishable without further information: content `a` may be absent from document `d`'s arrangement because `d` once contained `a` and removed it (it was *deleted*), or because `d` was never an arrangement that contained `a` (it was *never included*). A "show deletions" operation must distinguish these. We will show that the provenance relation `R` introduced in the transition model supplies exactly the information required, and that any conforming implementation must therefore maintain state components — beyond `(C, L, E, M)` collectively — sufficient to disambiguate the two predicates `DELETED(a, d)` and `NEVER_INCLUDED(a, d)` at every reachable state. Without such components, deletion is not detectable as a kind separate from prior absence.

## Foundation Recap

We take from the foundation:

- **Content store** `Σ.C : T ⇀ Val` (ASN-0036, S0): a partial function from tumblers to content values, append-only with immutable values across transitions.
- **Arrangement** `Σ.M(d) : T ⇀ T` (ASN-0036, S2, S3, S8a, S8-depth): a per-document partial function from V-positions to I-addresses.
- **Entity set** `Σ.E ⊆ T` and its document partition `Σ.E_doc` (ASN-0047).
- **Provenance relation** `Σ.R ⊆ T_elem × E_doc` (ASN-0047), where `T_elem = {a ∈ T : Element(a)} ⊆ T` uses the foundation's element predicate `Element(·)` (ASN-0047): `(a, d) ∈ R` iff document `d` has, at some point in the system's history, contained I-address `a` in its content-subspace arrangement.
- **Provenance permanence** `R ⊆ R'` across transitions (P2, ASN-0047): once `(a, d) ∈ R`, it remains so.
- **Provenance bounds** `Contains_C(Σ) ⊆ R` (P4★, ASN-0047): if `a` is currently in `d`'s content-subspace arrangement, then `(a, d) ∈ R`.
- **Historical fidelity** (P4a, ASN-0047): if `(a, d) ∈ R`, some prior reachable state had `a` in `d`'s content-subspace arrangement.
- **Provenance grounding** `R ⊆ dom(C) × E_doc` (P7, ASN-0047): every provenance pair references content that exists.
- **Origin function** `origin(a)` (ASN-0036, S7): every `a ∈ dom(C)` has a uniquely determined originating document, invariant across states.
- **Subspace projection** `subspace_I(a) = E(a)₁` (ASN-0047, SubspaceConventionAxiom): identifies the content (`s_C`) or link (`s_L`) subspace of an I-address.
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

The reachability hypothesis is load-bearing for the proof: it activates `P4★` (`Contains_C(Σ) ⊆ R`), which ASN-0047 establishes as a composite-boundary property — not as a per-state invariant preserved by every elementary transition. At intermediate states inside a composite, `P4★` may fail, so the lemma's universal claim applies only to states observed at composite boundaries. The hypothesis is discharged structurally at every SHOWDELETIONS invocation by D-BOUND below, which makes composite-boundary state part of the operation's contract rather than a caller obligation.

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

*Notational convention.* In the histories below, each `→*` arrow denotes one valid composite under ValidComposite★ (ASN-0047); line breaks are visual aids only, and composite groupings are determined by the coupling requirements of the elementary steps. In particular, K.α must be bundled with a subsequent K.μ⁺/K.ρ pair within the same composite, because K.α's frame leaves `M` unchanged — a standalone-K.α composite would produce `a ∈ dom(C') \ dom(C)` without placing `a` in any arrangement, violating J0 (AllocationPlacementCoupling, ASN-0047). J0 is a composite-boundary coupling evaluated only between the initial and final states of a composite, so the K.μ⁺ need not immediately succeed K.α within the composite — other elementary steps may intervene — but it must lie in the same composite for J0 to be discharged at the boundary. The bundling pattern is exhibited in Histories 1 and 2 below.

A second bundling concerns document creation. K.δ case (ii) with `k = 2` (descent) requires `t ∈ E ∧ zeros(t) ≤ 1`. From `Σ_0` (where the only entity is the bootstrap node `n_0` with `zeros(n_0) = 0`), a single elementary K.δ step produces at most an account (`zeros = 1`). Producing a document (`zeros = 2`) requires a precursor account-creation step. We therefore use `K.δ(d)` as shorthand for a composite containing whatever precursor K.δ steps are needed to satisfy the entity-hierarchy preconditions — for example, the composite `K.δ(A); K.δ(d)` where `A = inc(n_0, 2)` is the account and `d = inc(A, 2)` is the document. The composite is valid by ValidComposite★: each elementary step satisfies its precondition at its intermediate state, and J0/J1★/J1'★ are vacuous because no K.α, K.μ⁺, or K.ρ steps appear. The same convention applies to `K.δ(d_A)` and `K.δ(d_B)` in the worked example below.

Both histories begin at the initial state `Σ_0` (ASN-0047) and share the prefix `K.δ(d); K.δ(d')` — creating two documents `d, d'`. Both then invoke K.α(a, d) to allocate one content address. By K.α's first-emission rule (`{a' ∈ dom(C) : origin(a') = d} = ∅` initially), the allocated address is determinately `a = [d.0.s_C.1]` — a value fixed by `d` alone. Both histories pass the same `d` to the first-emission predicate, so both yield the same allocated address `a`. We further stipulate that both histories pass the *same* `v ∈ Val` argument to K.α — call it `v_a` — so that `C_1(a) = C_2(a) = v_a` and the content-store agreement in the table below holds at the value level. K.α's content-value parameter is a free choice by the caller, and synchronising it across the two histories is the only way to make the `(C, L, E, M)` agreement total. We fix the content-subspace V-position depth at `m_C = 2` throughout both histories — admissible because ValidFirstInsertionPosition (ASN-0036) treats `m` as operational input with `m ≥ 2`, and we choose the minimum so both histories operate with the same depth — giving `v = [s_C, 1] = [1, 1]` in `M(d)` and `v' = [s_C, 1] = [1, 1]` in `M(d')` as the canonical D-MIN★ first positions for each document's initially-empty content subspace. The histories then differ in where `a` is placed and which provenance pairs are recorded.

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

The two halves are necessarily disjoint, and the disjointness is unconditional — it needs neither D-EXH nor any composite-boundary hypothesis. Membership in `DeletedFromAWithB` requires `CURRENT(a, d_B)`, i.e. `a ∈ ran(M(d_B))`; membership in `DeletedFromBWithA` requires `DELETED(a, d_B)`, whose second conjunct is `a ∉ ran(M(d_B))`. The two range-membership conditions on `M(d_B)` are directly contradictory, so no `a` can belong to both halves.

**Observational-discipline axiom (D-BOUND).** SHOWDELETIONS is an observational operation invoked between composites: the pre-state `Σ` is a *composite-boundary state* — reachable from `Σ_0` by a finite sequence of valid composite transitions under ValidComposite★ (ASN-0047). This is a system-level discipline that mirrors Nelson's command-level statelessness, where each protocol command (state-modifying or observational) is the unit of caller interaction; state-modifying commands realise one composite, and observational commands like SHOWDELETIONS read the state between completed composites. The axiom is part of the operation's contract: D-EXH's composite-boundary hypothesis is discharged at every invocation by D-BOUND, not by run-time verification or by appeal to informal "operational scope."

The operation's precondition is `d_A ∈ E_doc ∧ d_B ∈ E_doc ∧ Σ is a composite-boundary state`, with the boundary conjunct supplied structurally by D-BOUND. Its postcondition characterises the result set-theoretically. We capture this in wp form. Let `q` abbreviate the predicate:

```
Result = (DeletedFromAWithB(Σ, d_A, d_B), DeletedFromBWithA(Σ, d_A, d_B))
```

Then `wp(SHOWDELETIONS(d_A, d_B), q) = (d_A ∈ E_doc ∧ d_B ∈ E_doc ∧ Σ is a composite-boundary state)`. The operation always terminates with `q` true when its precondition holds.

Because SHOWDELETIONS is observational (D-OBS below), wp computations for state-level predicates pass through unchanged from the pre-state: `wp(SHOWDELETIONS, P) = (precondition) ∧ P(Σ)` whenever `P` depends only on `Σ`. Two state-level postconditions are worth deriving explicitly, since they characterise *when* the operation surfaces structurally meaningful facts.

*Non-emptiness of one report half.* Let `Q1` abbreviate `DeletedFromAWithB(d_A, d_B) ≠ ∅`. Unpacking the definition of `DeletedFromAWithB`:

```
wp(SHOWDELETIONS(d_A, d_B), Q1)
   =  d_A ∈ E_doc  ∧  d_B ∈ E_doc
    ∧  Σ is a composite-boundary state
    ∧  (E a ∈ dom(C) :  subspace_I(a) = s_C
                       ∧ (a, d_A) ∈ R
                       ∧ a ∉ ran(M(d_A))
                       ∧ a ∈ ran(M(d_B)))
```

So `DeletedFromAWithB` is non-empty exactly when some content address inhabits `d_A`'s history through `R`, has been removed from `d_A`'s current arrangement, and remains in `d_B`'s current arrangement. The fourth conjunct (presence in `d_B`) is what makes the report *recoverable* in the sense of D-IDENT below — every reported deletion has a concrete witness in the partner document. This is not an additional postcondition; it is implicit in the definition of `DeletedFromAWithB`.

*Vacuity of both report halves.* Let `Q0` abbreviate `DeletedFromAWithB(d_A, d_B) = ∅ ∧ DeletedFromBWithA(d_A, d_B) = ∅`. Since SHOWDELETIONS is observational (D-OBS) and `Q0` depends only on `Σ`'s components `M`, `R`, `dom(C)`, `subspace_I` — each evaluable at any state `Σ` — the wp formula is the precondition conjoined with `Q0` unpacked at the pre-state:

```
wp(SHOWDELETIONS(d_A, d_B), Q0)
   =  d_A ∈ E_doc  ∧  d_B ∈ E_doc
    ∧  Σ is a composite-boundary state
    ∧  (A a ∈ dom(C) :  subspace_I(a) = s_C :
            ¬(DELETED(a, d_A)  ∧  CURRENT(a, d_B))
          ∧ ¬(DELETED(a, d_B)  ∧  CURRENT(a, d_A)))
```

The joint report is empty exactly when no content has been deleted from one document while remaining current in the other.

*Supplementary lemma (R-disjointness implies Q0 at composite-boundary states).* Documents with disjoint `R`-projections on the content subspace — `{a : (a, d_A) ∈ R} ∩ {a : (a, d_B) ∈ R} = ∅` — satisfy `Q0` at any composite-boundary state `Σ`. The boundary hypothesis is load-bearing because the argument invokes P4★, which ASN-0047 establishes as a composite-boundary property rather than a per-state invariant. By D-BOUND, every SHOWDELETIONS invocation observes a composite-boundary pre-state, so the lemma's hypothesis is automatically discharged at every invocation. *Proof.* `Q0` requires every `a ∈ dom(C)` to falsify *both* conjuncts `DELETED(a, d_A) ∧ CURRENT(a, d_B)` (conjunct 1) and `DELETED(a, d_B) ∧ CURRENT(a, d_A)` (conjunct 2). Partition `dom(C)` into three groups by `R`-projection membership, and show each group falsifies both conjuncts.

*Group 1: `(a, d_A) ∈ R`.* Disjointness gives `(a, d_B) ∉ R`. For conjunct 1, `CURRENT(a, d_B)` requires `a ∈ ran(M(d_B))`; by the same L14 + S3★-aux + S3★-contrapositive chain unpacked in the proof of D-EXH above — `a ∈ dom(C)` (from the outer quantifier) gives `a ∉ dom(L)` via L14; the witness `v ∈ dom(M(d_B))` for `a ∈ ran(M(d_B))` must satisfy `subspace(v) = s_C` (else S3★'s link clause would force `a ∈ dom(L)`); so `(a, d_B) ∈ Contains_C(Σ)`, which by P4★ — activated by the boundary hypothesis — forces `(a, d_B) ∈ R`, contradicting `(a, d_B) ∉ R`. So `CURRENT(a, d_B)` fails and conjunct 1 is falsified. Conjunct 2 is falsified more directly: `DELETED(a, d_B)` has first conjunct `(a, d_B) ∈ R`, which `(a, d_B) ∉ R` negates outright — no P4★ chain needed.

*Group 2: `(a, d_B) ∈ R`.* By the symmetric argument, disjointness gives `(a, d_A) ∉ R`. Conjunct 2's `CURRENT(a, d_A)` is excluded by the same L14 + S3★ + P4★ chain applied to `d_A`, falsifying conjunct 2; and conjunct 1's `DELETED(a, d_A)` fails directly because its first conjunct `(a, d_A) ∈ R` is negated by `(a, d_A) ∉ R`.

*Group 3: neither `(a, d_A) ∈ R` nor `(a, d_B) ∈ R`.* The address is classified `NEVER_INCLUDED` against both documents; `DELETED(a, d_A)` and `DELETED(a, d_B)` both fail on their first conjuncts, so both conjuncts are falsified trivially.

The three groups are exhaustive (disjointness rules out membership in both `R`-projections, so no fourth group arises). Every `a ∈ dom(C)` falsifies both conjuncts, and `Q0` holds. The argument covers the special case of one or both `R`-projections being empty without separate handling. Documents with synchronised edits (each deletion mirrored in the partner) satisfy `Q0` non-vacuously: for shared content, removal from one is matched by removal from the other.

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

We make the witness-impossibility explicit, mirroring the chain unpacked in D-EXH. Let `ℓ` be a link address with `origin(ℓ) = d_A`, and let `d_B ≠ d_A` be any candidate witness document. We show `ℓ ∉ ran(M(d_B))`. First, by L0 (SubspacePartition, ASN-0047), `subspace_I(ℓ) = s_L`, so `ℓ ∈ dom(L)` (every link address lives in the link store). Suppose for contradiction `ℓ ∈ ran(M(d_B))`: some `v ∈ dom(M(d_B))` has `M(d_B)(v) = ℓ`, and by S3★-aux `subspace(v) ∈ {s_C, s_L}`. We exclude both:

- *Content V-position (`subspace(v) = s_C`).* The content clause of S3★ would force `M(d_B)(v) = ℓ ∈ dom(C)`. But `ℓ ∈ dom(L)`, and L14 (`dom(C) ∩ dom(L) = ∅`) gives `ℓ ∉ dom(C)` — contradiction.
- *Link V-position (`subspace(v) = s_L`).* CL-OWN would force `origin(M(d_B)(v)) = origin(ℓ) = d_B`. But `origin(ℓ) = d_A ≠ d_B` — contradiction.

Both subspaces are excluded, so `ℓ ∉ ran(M(d_B))`. No comparison document other than `d_A` can hold `ℓ` in its arrangement, so the `CURRENT(ℓ, d_B)` witness condition that SHOWDELETIONS requires can never be satisfied across documents for link material.

Restricting SHOWDELETIONS to the content subspace is therefore not an implementation simplification but a structural necessity — derived from L0, L14, S3★, and CL-OWN, not merely asserted. The link subspace requires a separate (and per-document, not cross-document) analysis.

## Identity Preservation

**Claim D-IDENT.** For every `a` in either output set, the returned reference is precisely the I-address `a` — not a copy with new identity.

*Justification.* The output sets are defined as subsets of `dom(C)`. Each element is an existing I-address. We return addresses, not values.

The architectural significance is foundational. An operation that recovers content using these references dereferences existing entries in `C`; it does not allocate new ones. Three guarantees that depend on persistent I-address identity therefore survive recovery:

- *Link survival.* By L3 (NEndsetStructure, ASN-0047), which characterises the link store `L` as a partial function from tumblers to N-tuples of endsets, every link in `dom(L)` references content via endsets — each endset is a set of spans (Shared Vocabulary), and each span is anchored at a start tumbler which references an Istream address. We do not assume every such span starts in `dom(C)`: an endset may reference link addresses in `dom(L)` as well (link-to-link references are permitted). What matters here is the spans that *do* anchor at the content address `a`: such a span references `a`, and `a`, as the start tumbler of some span in some endset, is what those links reference. By P3 (ArrangementMutabilityOnly, ASN-0047), `L` is preserved across all transitions — `L' = L` for every K.μ⁺/K.μ⁻/K.μ~ — so a link whose endset contains a span anchored at `a` continues to reference the same `a` regardless of which arrangements currently expose it.
- *Transclusion integrity.* By S2 (ArrangementFunctionality, ASN-0036) and the content clause of S3★ (GeneralizedReferentialIntegrity, ASN-0047) — `subspace(v) = s_C ⟹ M(d)(v) ∈ dom(C)` — arrangements reference I-addresses by tumbler identity: each content-subspace V-position maps to a determinate `a ∈ dom(C)`. The link clause of S3★ targets `dom(L)` rather than `dom(C)` and is not invoked here; SHOWDELETIONS is restricted to the content subspace (D-SUBSP), so only the content clause is load-bearing for transclusion integrity. If another document's content-subspace arrangement maps a V-position to `a`, that mapping continues to reference the same `a` because P0 (ContentPermanence, ASN-0047, subsuming S0 of ASN-0036) preserves both `dom(C)` and the value at every existing entry across all transitions; no aliasing or shadow copy is introduced.
- *Origin attribution.* By S7 (StructuralAttribution, ASN-0036), `origin(a)` is derivable from `a`'s tumbler alone and is invariant across all states in which `a ∈ dom(C)`. The chain of provenance is not severed by recovery.

If SHOWDELETIONS returned new identities — fresh I-addresses with the same byte values — all three guarantees would collapse. The recovered content would be unaddressable by existing links, would not match existing transclusions, and would have spurious new origin. Returning addresses is therefore not a presentation choice; it is a correctness requirement.

## Origin Traceability

**Claim D-ORIG.** For every `a` in either output set, `origin(a)` is determined and identifies a unique document — the originating allocator of `a`.

*Justification.* By S7 (ASN-0036), `origin(a)` is defined for every `a ∈ dom(C)` and is invariant across all states in which `a ∈ dom(C)`. The output sets are subsets of `dom(C)`, so `origin` is well-defined on every output element.

The user-facing meaning: any returned address self-identifies its home document. When `d_A` and `d_B` were derived from a common ancestor `d_C`, content inherited from `d_C` and later deleted from `d_A` carries `origin(a) = d_C`. Content originally allocated by some other document and transcluded into `d_A` before deletion carries that other document's address as origin. The output need carry no extra "origin annotation" beyond the address itself — origin is derived structurally from the address.

This matters operationally because it scopes recovery rights and accounting. The originating document is recoverable from the address; recovery operations can verify permissions against `origin`; royalty or attribution mechanisms have the data they need.

## Order Preservation

**Claim D-ORD.** Each output half is a finite subset of `dom(C) ⊆ T`, and therefore inherits the total order T1 (ASN-0034) imposes on tumblers. No separate ordering structure is needed: the addresses are self-ordering, and any presentation may list them in T1 order.

*Justification.* The output sets are subsets of `dom(C)`, finite by C-fin (ASN-0047), and T1 is a strict total order on `T` (ASN-0034). The restriction of a total order to a finite subset is again a total order, so each half is linearly ordered by its own addresses with no appeal to any document's arrangement.

We note explicitly what is *not* recoverable: the V-position order in which a deleted address appeared in the document from which it was removed. V-position information is local to a current arrangement and is not preserved by `R`, so the deleted document's "original ordering" is a property of an arrangement no longer present. The witness document's arrangement does impose a V-order on the still-current addresses, but that order is observable only through the witness and is not part of the abstract output.

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

*Justification.* Each output element is an I-address in `dom(C)`, carrying determinate origin (D-ORIG) and preserved identity (D-IDENT). Any operation whose input type accepts I-addresses (or spans thereof) can consume the output directly. The output is *not* wrapped in V-position structure — wrapping it that way would require either fictitious positions (deleted content has no V-position in the queried document) or borrowed positions from the witness (which would have to be coordinated with the recovery target's address space, an entanglement the abstract output cannot impose). The output is *not* wrapped in content values — wrapping it that way would require copying values into new identities, breaking D-IDENT.

The abstract specification fixes only the set of I-addresses. Because each address retains its identity and self-identifies its origin, an implementation may package the output more compactly — for instance grouping contiguous same-origin runs into spans — without changing what is specified. Any such packaging is a representation choice, not part of the operation's contract; the I-set run-decomposition it would rely on is material for a span/bundle-algebra treatment, not for this operation spec.

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

Consequences: SHOWDELETIONS is repeatable on the same state (yields identical results); it commutes with other observational queries; and a later invocation after intervening state changes correctly reflects the new state. Because the operation is observational, its result is merely delivered to the caller and is not stored as a document or otherwise integrated into the persistent store (**D-STORE**); the system creates no persistent artefact of its own accord.

## State-Functional Independence

**Claim D-RECONS.** The output depends only on the current state `Σ`. It does not depend on the particular sequence of transitions by which `Σ` was reached.

*Justification.* Each predicate `CURRENT`, `DELETED`, `NEVER_INCLUDED` is defined in terms of components of `Σ` only (`M`, `R`, `dom(C)`, `subspace_I`). The output sets are characterised entirely by these projections. Two distinct transition histories yielding the same `Σ` therefore yield identical SHOWDELETIONS outputs.

This is what makes the operation an honest function of state. The user need not know how the system arrived at its current configuration; consulting the current configuration suffices. P4a (historical fidelity, ASN-0047) ensures that whenever the operation reports `DELETED(a, d)`, there really was a past state where `a` was in `d`'s arrangement — but the *route* to that past state is irrelevant to the report itself.

## Edge Cases

*Documents with no shared content.* Both output halves are empty exactly when, for every `a ∈ dom(C)`, `¬(DELETED(a, d_A) ∧ CURRENT(a, d_B))` and `¬(DELETED(a, d_B) ∧ CURRENT(a, d_A))` — equivalently `¬((a, d_A) ∈ R ∧ a ∉ ran(M(d_A)) ∧ a ∈ ran(M(d_B)))` and the symmetric form. This is the condition the definitions of the output sets directly negate.

*Both arrangements empty.* If `dom(M(d_A)) = dom(M(d_B)) = ∅`, then `ran(M(d_A)) = ran(M(d_B)) = ∅`, so `CURRENT` fails for every `a` on both sides. Both halves are empty.

*Same document compared against itself.* If `d_A = d_B`, then for each `a`, `DELETED(a, d_A) ∧ CURRENT(a, d_A)` is contradictory (by D-EXH). Both halves are empty. The operation is well-defined and trivially yields the empty pair.

*Asymmetric population.* If `d_A` has rich history (large `R`-projection) but its current arrangement is empty, while `d_B`'s arrangement currently holds many of the addresses `d_A` historically held, then `DeletedFromAWithB` may be large and `DeletedFromBWithA` may be empty. The asymmetry of the two halves directly mirrors the asymmetry of the editing histories.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| CURRENT | `CURRENT(a, d) ≡ a ∈ ran(M(d))` | introduced |
| DELETED | `DELETED(a, d) ≡ (a, d) ∈ R ∧ a ∉ ran(M(d))` | introduced |
| NEVER_INCLUDED | `NEVER_INCLUDED(a, d) ≡ (a, d) ∉ R` | introduced |
| D-EXH | For every composite-boundary state Σ (reachable by valid composite transitions) and every `(a, d)` with `a ∈ dom(Σ.C)`, `subspace_I(a) = s_C`, `d ∈ Σ.E_doc`, exactly one of CURRENT, DELETED, NEVER_INCLUDED holds | introduced |
| D-DISCR | No function of `(C, L, E, M)` alone can distinguish DELETED from NEVER_INCLUDED; any system supporting SHOWDELETIONS must maintain state components `C*` beyond the four foundation components such that consulting `(C, L, E, M, C*)` at every reachable Σ determines whether each `(a, d)` is DELETED or NEVER_INCLUDED | introduced |
| DeletedFromAWithB | `{a ∈ dom(C) : subspace_I(a) = s_C ∧ DELETED(a, d_A) ∧ CURRENT(a, d_B)}` | introduced |
| DeletedFromBWithA | Symmetric counterpart of DeletedFromAWithB | introduced |
| SHOWDELETIONS | Observational operation `SHOWDELETIONS(d_A, d_B) = (DeletedFromAWithB(d_A, d_B), DeletedFromBWithA(d_A, d_B))` | introduced |
| D-BOUND | SHOWDELETIONS is invoked at composite-boundary states; the boundary condition is part of the operation's contract and discharges D-EXH's hypothesis structurally | introduced |
| D-SUBSP | The operation restricts to the content subspace `s_C`; cross-document deletion comparison is structurally meaningful only there | introduced |
| D-IDENT | Output references are I-addresses themselves; no copies, no new identities | introduced |
| D-ORIG | Every output element `a` has determinate `origin(a)` | introduced |
| D-ORD | Each output half is a finite subset of T, inheriting T1's total order; no separate ordering structure is needed | introduced |
| D-SYM | `SHOWDELETIONS(d_B, d_A)` is the component-swapped pair of `SHOWDELETIONS(d_A, d_B)` | introduced |
| D-ACT | Output is a set of I-addresses in `dom(C)`, directly consumable by any I-address-based operation | introduced |
| D-OBS | SHOWDELETIONS modifies no state component; it is purely observational | introduced |
| D-STORE | The output is not required to be stored as a document; it is a query result | introduced |
| D-RECONS | The output depends only on the current state, not on transition history | introduced |

## Open Questions

What abstract characterisation of "shared content history" between two documents, expressed solely in terms of R, predicts when SHOWDELETIONS will yield non-empty results?

When deleted content has been removed from every document that ever contained it, through what state component does the system still retain the option to expose it for query or recovery?

How should SHOWDELETIONS report content that was deleted from both compared documents but remains current in a third document not in the pair?

If the system supports concurrent state transitions, what consistency model must SHOWDELETIONS observe to deliver coherent joint snapshots of M and R?

How does SHOWDELETIONS generalise to families of more than two documents, and what witness-structure replaces the binary asymmetric pair?

Under what conditions on the witness arrangement does the deletion set admit a finite presentation as a union of contiguous I-address spans, and when must it enumerate addresses singly?

What guarantees must the witness's V-order satisfy to ensure that presentation-ordered output of SHOWDELETIONS corresponds to a user-meaningful reading sequence rather than a structural accident?

Should the system distinguish content "deleted with a witness in a prior arrangement of the same document" from "deleted with a witness in a sibling document," and what additional structure would that distinction require?

What must a restoration operation guarantee so that consuming a subset of a SHOWDELETIONS output reintroduces deleted content into a target arrangement while preserving origin and link-resolvability?
