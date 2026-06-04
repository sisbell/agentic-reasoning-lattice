# ASN-0099: FINDLINKS Operation

*2026-05-26*

## The Reader's Question

A reader looks at a stretch of content and asks: *what connects here from elsewhere?* This is one half of the Xanadu reader-side promise — that the literature is bidirectionally navigable, and that backlink discovery from the rest of the docuverse must be answerable on demand (Nelson, *Literary Machines* 2/46: "without appreciable delay"). The reader knows only what they see: arranged content at V-positions in some document `d`. They do not see I-addresses directly, do not see the content store, do not see other documents' arrangements, and they certainly do not see the link store. The links the reader wants live in `dom(Σ.L)` at element-level tumbler addresses (L1, ASN-0043), with endsets referencing content I-addresses (L3) rather than V-positions. The arrangement `Σ.M(d)` bridges V-coordinates to I-coordinates.

## A Two-Phase Factoring

The question splits cleanly into two phases.

**Phase 1 (V→I).** Given a document `d ∈ dom(Σ.M)` and a query region `R ⊆ T`, produce the *I-image* of the region:

```
image(R, d, Σ)
  defined when  d ∈ dom(Σ.M)
  ≡             {Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}
```

The single precondition `d ∈ dom(Σ.M)` is load-bearing so that `Σ.M(d)` is defined. V-positions in `R` that are absent from the arrangement contribute nothing to the image — the comprehension restricts to `R ∩ dom(Σ.M(d))`, so it fabricates no I-address absent from the arrangement.

**Phase 2 (I→Link).** Given a set of I-addresses `I ⊆ T`, produce the set of links whose endsets intersect `I`:

```
findlinks(I, Σ) = {a ∈ dom(Σ.L) : (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)}
```

The two phases compose into the reader-facing operation:

```
F12 (TwoPhaseFactoring) — DEFINITION of findlinks_V:
   findlinks_V(R, d, Σ)
     defined when  d ∈ dom(Σ.M)
     ≡             findlinks(image(R, d, Σ), Σ).
```

For `d ∉ dom(Σ.M)`, `findlinks_V(R, d, Σ)` is *undefined* — no silent fallback. For V-positions in `R` outside `dom(Σ.M(d))`, the silent projection in `image` absorbs them; the caller has no pre-validation obligation beyond establishing `d ∈ dom(Σ.M)`.

The factoring matters because the two phases have different stability properties. `Σ.M` is mutable (K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L all modify it); `Σ.L` is monotonic (K.λ adds, L12 forbids modification of existing entries). Phase 1 consults the mutable component; phase 2 consults the monotonic component.

## The Image Set

`R` is unconstrained beyond `R ⊆ T` — single position, contiguous V-span, or any subset. When `R` is a contiguous V-span in subspace `s_C`, ASN-0058's mapping-block decomposition gives the image as a union of disjoint I-runs, one per maximal correspondence run. When `v ∈ R` has `subspace(v) = s_L`, S3★ (ASN-0047) routes `Σ.M(d)(v) ∈ dom(Σ.L)` and the image picks up a link address. The match predicate accepts this without modification: endsets may reference any addresses in `T` (L4, ASN-0043), so the link subspace is admissible as a coverage target.

## The Match Predicate

```
F1 (MatchPredicate):
   For a ∈ dom(Σ.L), I ⊆ T, Σ ∈ 𝒮:
   matches(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅).
```

F1 generalizes ASN-0098's `discoverable_from`. ASN-0098 defines that predicate in *project* form — `discoverable_from(a, d, Σ) ≡ (E i : project(a, i, d, Σ) ≠ ∅)` — whereas F1's `matches` is in *coverage* form. The two coincide by LP12 (DiscoverabilityCharacterisation, ASN-0098), whose per-slot biconditional `project(a, i, d, Σ) ≠ ∅ ⟺ coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅` gives `discoverable_from(a, d, Σ) = matches(a, ran(Σ.M(d)), Σ)`. The existential ranges uniformly over all slots, including the type-endset and any further slots: L7 (ASN-0043) leaves directional significance to the link type, and the reader's question — *what connects here?* — does not privilege from over to.

F1's match is **per-endset overlap**: within each endset, satisfaction is existential over spans, and the per-span test is overlap (`coverage(eᵢ) ∩ I ≠ ∅` unfolds to `(E (s, ℓ) ∈ eᵢ : {t : s ≤ t < s ⊕ ℓ} ∩ I ≠ ∅)`, with an identifiable witness span).

```
F4 (MatchIndividuation):
   The natural alternative match designs — coverage-containment in
   either direction, a cardinality threshold, and the I-independent
   slot tests — each yield an operation distinct from FINDLINKS. The
   witnesses below exhibit, for each such design, a realizable (a, I)
   pair on which it disagrees with F1's per-endset overlap test.
```

*Realizability.* Each witness is realizable: the I-set is a query parameter and endsets are freely chosen at K.λ (L4 places no constraint on span addresses), so every `(a, I)` pair below arises by a K.λ allocation under any document.

*Strengthening 1 — Containment from coverage to query (`coverage ⊆ I`).* Witness link `a`: arity 3 with slot 1 `(β, δ(1, #β))`, slot 2 `(γ, δ(1, #γ))`, slot 3 `(α, δ(1, #α))`, where β and γ are same-length siblings of `α` differing at position `#α` (so β ⋠ α, α ⋠ β, γ ⋠ α, α ⋠ γ). Query `I = {α}`. F1 admits via slot 3: `coverage(L(a).e₃) ∩ I = {α} ≠ ∅`. The link-level strengthening predicate is the slot-existential `(E i : coverage(L(a).eᵢ) ⊆ I)`; we check every slot: slot 1's coverage `{t : β ≼ t}` is non-empty (contains β) and disjoint from `{α}` (since β ⋠ α), so `coverage(e₁) ⊄ I`; slot 2 likewise; slot 3's coverage `{t : α ≼ t}` (by PrefixSpanCoverage, ASN-0043) contains `α.0 ∉ I` (any tumbler extending α belongs by T0's allowance of trailing zeros). No slot satisfies `coverage ⊆ I`; strengthening excludes `a`.

*Strengthening 2 — Containment from query to coverage (`I ⊆ coverage`).* Witness: link `a` with one canonical span `(α, δ(1, #α))` at slot 3 (the mandatory non-empty type-endset slot per L3), and slots 1 and 2 empty (permitted by L3 for non-type slots). Query `I = {α, γ}` for any `γ ∈ T` with `α ⋠ γ` (e.g., a same-length sibling differing at position `#α`). F1 admits via slot 3: `coverage(L(a).e₃) ∩ I = {α} ≠ ∅`. The link-level strengthening predicate is the slot-existential `(E i : I ⊆ coverage(eᵢ))`; we check every slot: at slot 3, `coverage(e₃) = {t : α ≼ t}` (by PrefixSpanCoverage, ASN-0043) contains `α` reflexively but not `γ` (since `α ⋠ γ`), so `I ⊄ coverage(e₃)`; at slots 1 and 2 (empty), `coverage(∅) = ∅` cannot contain non-empty `I = {α, γ}`. Strengthening excludes `a`.

*Strengthening 3 — Cardinality threshold (`|coverage ∩ I| ≥ k` for `k > 1`).* Witness: link `a` with one canonical span `(α, δ(1, #α))` at slot 3 (the mandatory non-empty type-endset slot per L3), and slots 1 and 2 empty (permitted by L3 for non-type slots). Query `I = {α}`. The link-level strengthening predicate is the slot-existential `(E i : |coverage(eᵢ) ∩ I| ≥ k)` for `k > 1`; we check every slot: at slot 3, `|coverage(e₃) ∩ I| = |{t : α ≼ t} ∩ {α}| = 1 < k`; at slots 1 and 2 (empty), `|coverage(∅) ∩ I| = |∅ ∩ {α}| = 0 < k`. No slot satisfies the threshold; strengthening excludes `a`. F1 admits via slot 3's singleton overlap.

*Weakening 1 — Slot-vacuous match (`P_⊤(a, I, Σ) ≡ a ∈ dom(Σ.L)`).* Witness: any link `a ∈ dom(Σ.L)` with all `coverage(Σ.L(a).eᵢ)` disjoint from `I`. Concrete instance: `Σ.L(a)` with `(τ, δ(1, #τ))` at slot 3 (the mandatory non-empty type endset), `∅` at slots 1 and 2, and `I = {α}` with `τ ⋠ α` and `α ⋠ τ` (cross-document non-nesting τ). Then `coverage(Σ.L(a).e₃) ∩ I = ∅` and the other slots are coverage-empty, so F1 rejects `a`. `P_⊤` admits `a`. The weakening returns links with no overlap to the query I-set — non-conforming with F1's relevance principle (the OR-across-slots existential over the per-endset overlap test): some span in some endset must witness a non-empty intersection with the request.

*Weakening 2 — Slot-disjunctive ignoring I (`P_∃-slot(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ≠ ∅)`).* Witness: the same `(a, I)` as Weakening 1. `Σ.L(a).e₃ = {(τ, δ(1, #τ))}` is non-empty (mandated by L3), so `coverage(Σ.L(a).e₃) ≠ ∅` and `P_∃-slot` admits `a` regardless of `I`. F1 rejects (no slot's coverage meets `I`). The weakening collapses the I-dependence of the match entirely — every link in `dom(Σ.L)` matches every query, violating the relevance principle.

**Empty endsets at non-type slots.** L3 requires only slot 3 to be non-empty; other slots may carry `∅`. Then `coverage(∅) = ∅` and the slot is never a witness — but other non-empty slots may witness the existential.

## Endset Filtering

A *slot constraint* is a pair `(i, J)` with `i ∈ ℕ⁺`, `J ⊆ T`. A link satisfies the constraint iff its slot `i` exists and the coverage at that slot meets `J`. The positional accessor is undefined for `i > |Σ.L(a)|` (L6), so we fold the out-of-range case into an explicit guard. A filter constraint `(i, J)` is unsatisfiable at `a` when `i > |Σ.L(a)|` (the slot is absent) or `Σ.L(a).eᵢ = ∅` (the slot carries no spans, so `coverage(∅) = ∅` meets no `J`):

```
findlinks_filtered(C, Σ)
  = {a ∈ dom(Σ.L) : (A (i, J) ∈ C : i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)}
```

The from-to query is `{(1, I_from), (2, I_to)}`; the three-endset query adds `(3, I_type)`; a type-only restriction is `{(3, I_type)}`. The filtered form is *not* a strict generalization: the unfiltered match is an existential over slots, the filtered match a universal over constraints. The unfiltered form is recovered as a finite union over single-slot filters:

```
findlinks(I, Σ) = ⋃_{i = 1}^{N} findlinks_filtered({(i, I)}, Σ)
   where N = max{|Σ.L(a)| : a ∈ dom(Σ.L)}  when dom(Σ.L) ≠ ∅
         N = 0                              when dom(Σ.L) = ∅  (empty union = ∅)
```

`L-fin` gives `|dom(Σ.L)| < ∞` so the max is well-defined when the link store is non-empty. The identity holds per link: fix `a ∈ dom(Σ.L)`. The single-slot filter `findlinks_filtered({(i, I)}, Σ)` carries the guard `i ≤ |Σ.L(a)|`, so `a` appears in the `i`-th union term iff `i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅`. Membership of `a` in the union over `1..N` is therefore `(E i : 1 ≤ i ≤ N : i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)`, and the guard `i ≤ |Σ.L(a)|` collapses the range `1..N` to `1..|Σ.L(a)|` (terms with `i > |Σ.L(a)|` are unsatisfiable, and `|Σ.L(a)| ≤ N` by the definition of `N` ensures none below the per-link arity is dropped). That existential is exactly F1's `matches(a, I, Σ)`, so `a` is in the union iff `a ∈ findlinks(I, Σ)`. Set extensionality over `a` closes the identity.

```
F7 (EndsetSymmetry):
   (a) Slot symmetry: matches(a, I, Σ) consults all slots uniformly.
   (b) Filter conjunction: findlinks_filtered(C, Σ) intersects per-slot
       constraints — a link must satisfy every constraint to appear.
```

Both halves follow from the quantifier structure of the definitions: existential ⇒ slot-symmetric; universal ⇒ conjunctive.

## Completeness

The defining obligation is *completeness*: every link in `dom(Σ.L)` satisfying the match predicate must appear in an implementation's output. Let `result : 𝒫(T) × 𝒮 → 𝒫(T)` denote a conforming implementation's output function, where `𝒮` is the Xanadu system state space (states of the form `Σ = (C, L, M, E, R, …)` from ASN-0036, ASN-0043, ASN-0047, ASN-0093). The signature commits the implementation to functionality (equal arguments yield equal outputs).

```
F2 (Completeness):  findlinks(I, Σ) ⊆ result(I, Σ).
F3 (Soundness):     result(I, Σ) ⊆ findlinks(I, Σ).
```

Together F2 ∧ F3 force `result(I, Σ) = findlinks(I, Σ)`. The same conformance contract transfers to the filtered, scoped, and V-side forms, each with its own `result_*` function functional in its arguments and pinned to the corresponding abstract specification:

```
F2-filt ∧ F3-filt:  result_filtered(C, Σ)    = findlinks_filtered(C, Σ).
F2-sco  ∧ F3-sco:   result_scoped(I, S, Σ)   = findlinks_scoped(I, S, Σ).
F2-V    ∧ F3-V:     result_V(R, d, Σ)        = findlinks_V(R, d, Σ),
                    for every (R, d, Σ) with d ∈ dom(Σ.M).
```

The same conjunction-forces-equality argument applies per form, with the predicate adjusted to the operation. F2-V ∧ F3-V is the **primary obligation on `result_V`**: any implementation exposing the V-side surface must satisfy it. When the implementation also exposes the I-side surface satisfying F2 ∧ F3, the factoring equation `result_V(R, d, Σ) = result(image(R, d, Σ), Σ)` follows by F2 ∧ F3 + F2-V ∧ F3-V + F12, since both sides equal `findlinks_V(R, d, Σ)` exactly.

Completeness must hold *unconditionally* with respect to `dom(Σ.L)`: any implementation whose `result(I, Σ)` differs from the comprehension is non-conforming.

## Determinism and Comprehension Invariance

The result depends only on the link store and the query specification:

```
F8 (Determinism):
   findlinks(I, Σ) = findlinks(I, Σ')  whenever Σ.L = Σ'.L.
```

F8 is a property of the abstract operation; the implementation-side consequence `result(I, Σ) = result(I, Σ')` follows from F8 by F2 ∧ F3.

Every claim of the form "the comprehension is unchanged when `Σ.L = Σ'.L`" rests on the same derivation chain, which we state once as a discrete step.

```
ComprehensionInvariantUnderΣL — meta-lemma:
   If Σ.L = Σ'.L as partial functions, then for every comprehension
   over dom(Σ.L) whose membership predicate consults only Σ.L and
   query-data (never Σ.M, Σ.C, Σ.E, Σ.R):
       {a ∈ dom(Σ.L) : P(a, Σ)} = {a ∈ dom(Σ'.L) : P(a, Σ')}.

   The chain: Σ.L = Σ'.L gives dom(Σ.L) = dom(Σ'.L) and per-link
   value equality Σ.L(a) = Σ'.L(a). Component-wise tuple equality on
   Link values (L6) gives |Σ.L(a)| = |Σ'.L(a)| and per-slot endset
   equality Σ.L(a).eᵢ = Σ'.L(a).eᵢ. Coverage is a deterministic
   function of its endset argument, so per-slot coverage agrees.
   Predicates built from these — F1's existential, the filtered
   form's universal, scoped intersection — evaluate identically at
   the two states. Set extensionality closes the equality.
```

A per-link primitive follows under the weaker hypothesis of per-link value preservation `Σ'.L(a) = Σ.L(a)` at a specific `a ∈ dom(Σ.L)`:

```
PerLinkInvarianceUnderValuePreservation — sub-lemma:
   For any link a with a ∈ dom(Σ.L) ∩ dom(Σ'.L) and
   Σ'.L(a) = Σ.L(a):
   - matches(a, I, Σ) ⟺ matches(a, I, Σ') for every I ⊆ T.
   - For every slot constraint (i, J), the per-link filter conjunct
       i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅
     evaluates identically at Σ and Σ'.
   - Consequently, for every constraint set C, the filtered per-link
     universal `(A (i, J) ∈ C : i ≤ |Σ.L(a)| ∧
     coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)` evaluates identically at Σ and Σ'.

   Proof: the per-link steps of ComprehensionInvariantUnderΣL —
   L6's component-wise tuple equality giving |Σ'.L(a)| = |Σ.L(a)|
   and per-slot endset equality Σ'.L(a).eᵢ = Σ.L(a).eᵢ, hence
   per-slot coverage agreement — apply unchanged at the weaker
   hypothesis Σ'.L(a) = Σ.L(a) (a single key rather than the whole
   store). F1's existential and the filtered per-link conjunct each
   consult only |Σ.L(a)| and per-slot coverage, so both evaluate
   identically at the two states.
```

## Arrangement Independence

The I→Link phase consults `Σ.L` and `I` alone. F8 already encodes this. The operationally salient frame condition exercised by editing operations rests on a structural lemma of the substrate: that operations other than K.λ preserve `Σ.L`. This ASN inhabits ASN-0047's *extended* state `Σ = (C, L, M, E, R)`, so the operative vocabulary is ASN-0047's extended-state vocabulary (ValidComposite★), with document registration performed by K.δ (Document case). Throughout this ASN we call an operation *link-store-inert* when it does not modify the link store `Σ.L` — that is, any operation in `V ∖ {K.λ}`. We package the preservation lemma:

```
A1a (PublishedFramePreservation):
   Every atomic operation of V ∖ {K.λ} — {K.α, K.δ, K.μ⁺, K.μ⁻,
   K.μ⁺_L, K.ρ} — publishes `L' = L` in its operative frame (K.μ⁺ and
   K.μ⁻ via ASN-0047's amended extended-state versions), hence
   preserves the link store across its transition Σ → Σ':
       dom(Σ'.L) = dom(Σ.L) ∧ (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a)).
```

```
A1 (KλUniqueLinkStoreModifier) — corollary of A1a:
   The composite K.μ~ (the non-atomic K.μ⁻ + K.μ⁺ composite) preserves
   the link store by transitive composition of A1a at its two
   constituents. With A1a covering the atomic operations, K.λ is
   therefore the unique operation of V that modifies the link store.
   (V = {K.α, K.λ, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L, K.ρ} — ASN-0047's
   extended-state vocabulary, ValidComposite★.)
```

```
F9 (LinkStoreInertPreservation):
   For every transition Σ → Σ' produced by an operation in V ∖ {K.λ}
   and any I ⊆ T:
       findlinks(I, Σ) = findlinks(I, Σ').

   A1 gives Σ.L = Σ'.L across every V ∖ {K.λ} operation. F8 via
   ComprehensionInvariantUnderΣL then forces the equality. For a
   reachable sequence Σ →* Σ' whose every atomic step lies in
   V ∖ {K.λ}, the per-step equalities chain by transitivity.
```

The remaining single-step case — K.λ itself — is the unique operation of V that can change `findlinks(I, ·)` across one step, and the change is fully characterized:

```
F9-λ (KλInducedIncrement):
   For any single-step transition Σ → Σ' produced by K.λ allocating
   a fresh link ℓ_new with endsets (e₁, …, e_N), and any I ⊆ T:
       findlinks(I, Σ') = findlinks(I, Σ) ⊎ ({ℓ_new} if matches(ℓ_new, I, Σ') else ∅).

   The two parts are disjoint (⊎): K.λ's freshness precondition
   ℓ_new ∉ dom(Σ.L) ∪ dom(Σ.C) (ASN-0093) gives ℓ_new ∉ dom(Σ.L),
   so ℓ_new ∉ findlinks(I, Σ).

   Derivation. K.λ's effect-clause gives dom(Σ'.L) = dom(Σ.L) ∪
   {ℓ_new} with Σ'.L(a) = Σ.L(a) for every a ∈ dom(Σ.L) (L12
   supplies value preservation on prior keys; K.λ's effect-clause
   adds only the fresh mapping). Split findlinks(I, Σ') by domain
   into the prior-key contribution from dom(Σ.L) and the fresh-key
   contribution from {ℓ_new}. For each a ∈ dom(Σ.L):
   PerLinkInvarianceUnderValuePreservation at this a transports
   matches(a, I, ·) unchanged from Σ to Σ', so the prior-key part
   contributes exactly findlinks(I, Σ). The fresh-key part
   contributes the singleton {ℓ_new} when matches(ℓ_new, I, Σ')
   holds, and ∅ otherwise.
```

## Transclusion Transparency

```
F6 (TransclusionTransparency):
   For documents d₁, d₂ ∈ dom(Σ.M) and V-positions v₁ ∈ dom(Σ.M(d₁)),
   v₂ ∈ dom(Σ.M(d₂)) with Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂) = α:
       findlinks_V({v₁}, d₁, Σ) = findlinks_V({v₂}, d₂, Σ).
```

`image({v₁}, d₁, Σ) = {α} = image({v₂}, d₂, Σ)` (the silent projection survives the singleton on both sides since both V-positions are in their respective arrangement domains). By F12, both V-side queries unfold to `findlinks({α}, Σ)`, which by functional determinism is one set. The match consulted only the I-image and the link store; the document of origin vanished from the computation.

A link created against `α`'s native location is found via any document that transcludes `α`. The link belongs to its home document by L1a, but its *findability* is at the I-address.

## Identity, Not Value

```
F5 (IdentityNotValue):
   matches(a, I, Σ) consults dom(Σ.L), Σ.L, and coverage(·), never
   Σ.C(·). For distinct α ≠ β, matches(a, {α}, Σ) and
   matches(a, {β}, Σ) are computed independently — each decided by
   address-level membership in coverage(Σ.L(a).eᵢ), with no reference
   to content values.

   Derivation. By inspection of F1's RHS, the existential
   `(E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` consults
   only |Σ.L(a)|, per-slot endsets Σ.L(a).eᵢ, the coverage function
   on endsets, and the I-set — Σ.C does not appear among the consulted
   components. For distinct α ≠ β, the queries matches(a, {α}, Σ) and
   matches(a, {β}, Σ) reduce per slot to the address-level set-
   membership tests `α ∈ coverage(Σ.L(a).eᵢ)` and
   `β ∈ coverage(Σ.L(a).eᵢ)`; these are independent membership
   predicates over coverage sets, with no shared content lookup.
```

If two users write the same string at different I-addresses, links to one are not links to the other. Identity comes from origin (GlobalUniqueness, ASN-0034) and is preserved through every operation touching the content store (P0, ASN-0047); discovery builds on this foundation, not on content equivalence.

## Composite Queries

```
F13 (SetAdditive):
   findlinks(I₁ ∪ I₂, Σ) = findlinks(I₁, Σ) ∪ findlinks(I₂, Σ).
```

Fix `a ∈ dom(Σ.L)` and write `eᵢ = Σ.L(a).eᵢ`, `Pᵢ ≡ coverage(eᵢ) ∩ I₁ ≠ ∅`, `Qᵢ ≡ coverage(eᵢ) ∩ I₂ ≠ ∅`. By distributivity of intersection over union, `coverage(eᵢ) ∩ (I₁ ∪ I₂) = (coverage(eᵢ) ∩ I₁) ∪ (coverage(eᵢ) ∩ I₂)`, and a union of two sets is non-empty iff at least one is, so the per-slot equivalence `coverage(eᵢ) ∩ (I₁ ∪ I₂) ≠ ∅ ⟺ Pᵢ ∨ Qᵢ` holds. This per-slot fact must now be lifted to the comprehension level, whose membership predicate is the slot-existential. Membership of `a` in the left-hand set unfolds and lifts as:

```
a ∈ findlinks(I₁ ∪ I₂, Σ)
  ⟺ (E i : coverage(eᵢ) ∩ (I₁ ∪ I₂) ≠ ∅)     -- definition of findlinks
  ⟺ (E i : Pᵢ ∨ Qᵢ)                            -- per-slot equivalence above
  ⟺ (E i : Pᵢ) ∨ (E i : Qᵢ)                    -- ∃ distributes over ∨
  ⟺ a ∈ findlinks(I₁, Σ) ∨ a ∈ findlinks(I₂, Σ) -- definition of findlinks, twice
  ⟺ a ∈ findlinks(I₁, Σ) ∪ findlinks(I₂, Σ)     -- definition of ∪
```

The load-bearing third step is the distribution of the existential over disjunction, `(E i : Pᵢ ∨ Qᵢ) ⟺ (E i : Pᵢ) ∨ (E i : Qᵢ)`, which carries the per-slot result up to the set equality. Since the chain holds for every `a ∈ dom(Σ.L)`, the two comprehensions are equal.

```
F20 (ImageSetAdditive):
   For d ∈ dom(Σ.M) and R₁, R₂ ⊆ T:
       image(R₁ ∪ R₂, d, Σ) = image(R₁, d, Σ) ∪ image(R₂, d, Σ).
```

The standard image-of-union identity for the partial function `Σ.M(d)`: `image(R, d, Σ) = {Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}`, and intersection distributes over union — `(R₁ ∪ R₂) ∩ dom(Σ.M(d)) = (R₁ ∩ dom(Σ.M(d))) ∪ (R₂ ∩ dom(Σ.M(d)))` — so the image of the union is the union of the images.

```
F20a (VSideAdditive) — consequence of F12 + F20 + F13:
   For d ∈ dom(Σ.M) and R₁, R₂ ⊆ T:
       findlinks_V(R₁ ∪ R₂, d, Σ) = findlinks_V(R₁, d, Σ) ∪ findlinks_V(R₂, d, Σ).
```

The derivation chains the three named identities:

```
findlinks_V(R₁ ∪ R₂, d, Σ)
  = findlinks(image(R₁ ∪ R₂, d, Σ), Σ)                       -- F12 unfold
  = findlinks(image(R₁, d, Σ) ∪ image(R₂, d, Σ), Σ)          -- F20 image-of-union
  = findlinks(image(R₁, d, Σ), Σ) ∪ findlinks(image(R₂, d, Σ), Σ) -- F13 set-additive
  = findlinks_V(R₁, d, Σ) ∪ findlinks_V(R₂, d, Σ)            -- F12 refold (twice)
```

Each step is licensed by exactly one prior identity; the middle step's `findlinks` arguments are I-sets, so F13 applies to them unchanged.

## The Empty Query

For `I = ∅`: every `coverage(e) ∩ ∅ = ∅`, so the slot-existential never witnesses; `findlinks(∅, Σ) = ∅`. Symmetrically `image(∅, d, Σ) = ∅`, and a V-region `R` entirely disjoint from `dom(Σ.M(d))` gives `findlinks_V(R, d, Σ) = ∅`.

When `dom(Σ.L) = ∅` (the initial state, before the first K.λ), every query produces `∅`. F2, F3, F10, F11, F19 all hold vacuously.

For `findlinks_filtered`: the empty constraint set `C = ∅` makes the universal vacuously true at every link, so `findlinks_filtered(∅, Σ) = dom(Σ.L)`. The empty constraint target — any `(i, J) ∈ C` with `J = ∅` — makes that per-constraint conjunct false everywhere, so the filtered result is `∅`.

For `findlinks_scoped(I, ∅, Σ) = findlinks(I, Σ) ∩ ∅ = ∅` by F14.

## Scope

```
F14 (ScopeFilter):
   findlinks_scoped(I, S, Σ) = findlinks(I, Σ) ∩ S
                             = {a ∈ dom(Σ.L) ∩ S : matches(a, I, Σ)}
```

Natural choices for `S`: "all links in document `d`" (`{a : home(a) = d}`), "all links by user `u`", or any access-control narrowing.

The determinism and survivability properties extend uniformly to the filtered and scoped forms:

```
F15 (FilteredDeterminism):  findlinks_filtered(C, Σ) = findlinks_filtered(C, Σ') when Σ.L = Σ'.L.
F16 (ScopedDeterminism):    findlinks_scoped(I, S, Σ) = findlinks_scoped(I, S, Σ') when Σ.L = Σ'.L.
F17 (FilteredSurvivability): findlinks_filtered(C, Σ) = findlinks_filtered(C, Σ') across a K.μ-family step.
F18 (ScopedSurvivability):   findlinks_scoped(I, S, Σ) = findlinks_scoped(I, S, Σ') across a K.μ-family step.
```

F15 follows from ComprehensionInvariantUnderΣL applied to the filtered universal. F16 follows from F8 + intersection-preservation with the query-supplied `S`. F17 follows from F9 (V ∖ {K.λ} steps preserve Σ.L, K.μ~ included) + F15. F18 follows from F9 + intersection-preservation.

## Result Ordering

The result is a set, but the reader is shown an ordered list. We adopt T1's lexicographic order on tumbler addresses:

```
F10 (OrderedResult):
   The result set admits a unique presentation as a sequence
   ⟨a₁, a₂, ..., aₙ⟩ with aⱼ ∈ dom(Σ.L) satisfying matches(aⱼ, I, Σ),
   and a₁ < a₂ < ... < aₙ under T1.
```

Finiteness: F3 gives `result(I, Σ) ⊆ dom(Σ.L)`; L-fin gives `|dom(Σ.L)| < ∞`. T1 is a strict total order on `T` and so restricts to one on any subset. Every finite totally-ordered set admits a unique enumeration by finite induction; the empty result (`n = 0`) is the degenerate case, presented as the empty sequence `⟨⟩`, which is vacuously strictly increasing and trivially unique. The canonical filtered and scoped presentations follow by the same finiteness + total-order argument:

```
F10-filt:  findlinks_filtered(C, Σ) admits a unique strictly T1-increasing sequence.
F10-sco:   findlinks_scoped(I, S, Σ) admits a unique strictly T1-increasing sequence.
```

## Persistent Discoverability (I-Side)

```
F11 (PersistentDiscoverabilityI):
   For any reachable state sequence Σ →* Σ' and any a ∈ dom(Σ.L) with
   matches(a, I, Σ):  a ∈ dom(Σ'.L) ∧ matches(a, I, Σ').
```

LP13 (UnconditionalLinkPersistence, ASN-0098) supplies the multi-step per-link guarantee `a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)`. PerLinkInvarianceUnderValuePreservation applied at this `a` then gives `matches(a, I, Σ) ⟺ matches(a, I, Σ')` — the witness slot found at Σ remains a witness at Σ'.

F11 is an *I-side* persistence claim against a fixed query I-set; the V-side analogue — fixing `(R, d)` and quantifying across edits — is not a theorem of this ASN and could not be, since K.μ⁻ can shrink `ran(Σ.M(d))` (Query 5 below exhibits the divergence concretely).

```
F19 (ResultSetMonotonicity):
   findlinks(I, Σ) ⊆ findlinks(I, Σ') for every reachable Σ →* Σ'.
```

Direct from F11 + the definition of `findlinks`. The V-side asymmetry noted at F11 applies equally here. Monotonicity propagates to the filtered and scoped forms:

```
F19-filt: findlinks_filtered(C, Σ) ⊆ findlinks_filtered(C, Σ').
F19-sco:  findlinks_scoped(I, S, Σ) ⊆ findlinks_scoped(I, S, Σ').
```

F19-filt follows from LP13 + PerLinkInvarianceUnderValuePreservation applied per link: for every `a ∈ findlinks_filtered(C, Σ)`, LP13 gives `a ∈ dom(Σ'.L)` and `Σ'.L(a) = Σ.L(a)`, and PerLinkInvarianceUnderValuePreservation transports the filtered per-link universal unchanged to `Σ'`, so `a ∈ findlinks_filtered(C, Σ')`. F19-sco follows from F19 + intersection-preservation with the query-supplied `S`.

F19 (and its filtered/scoped variants) is the load-bearing consequence behind any indexed implementation's promise: an index that mirrors `findlinks` is never required to remove entries as the state evolves, only to add them.

## A Worked Example

We fix a small instance. State `Σ` has two documents in `dom(Σ.M)`:

- `d_a`: content-bearing. `A_C(d_a)` has produced `α₁ = [d_a.0.s_C.1]`, `α₂ = [d_a.0.s_C.2]`, `α₃ = [d_a.0.s_C.3]`, each with content values `v₁, v₂, v₃ ∈ Val`. Arrangement: `Σ.M(d_a) = {v_a^1 ↦ α₁, v_a^2 ↦ α₂, v_a^3 ↦ α₃}` with `v_a^k = [s_C, k]` of depth 2.
- `d_b`: transcludes `α₂, α₃` from `d_a`. Arrangement: `Σ.M(d_b) = {v_b^1 ↦ α₂, v_b^2 ↦ α₃}` with `v_b^k = [s_C, k]`. We assume `d_b = inc(d_a, 0)`, the next sibling document under the same account, so `d_a < d_b`.
- Type-tumbler addresses `τ_comment, τ_reply, τ_meta` allocated under a separate registry document `d_τ` non-nesting with `d_a` and `d_b`.
- Three links: `ℓ ∈ A_L(d_a)` with slot 1 `(α₂, δ(1, #α₂))`, slot 2 `(α₃, δ(1, #α₃))`, slot 3 `(τ_comment, δ(1, #τ_comment))`; `ℓ' ∈ A_L(d_b)` with slot 1 `(α₃, ·)`, slot 2 `(α₁, ·)`, slot 3 `(τ_reply, ·)`; `ℓ_meta = inc(ℓ', 0) ∈ A_L(d_b)` with slot 1 `(ℓ, δ(1, #ℓ))` (annotation on `ℓ`), slot 2 `∅`, slot 3 `(τ_meta, ·)`.

By PrefixSpanCoverage, each canonical span's coverage is a prefix subtree. The three subtrees over `α₁, α₂, α₃` are pairwise disjoint (siblings with disagreeing final components); the subtrees over `τ_·` are pairwise disjoint and disjoint from content addresses (cross-document non-nesting); `{t : ℓ ≼ t}` is disjoint from any `{t : αᵢ ≼ t}` by subspace separation (`ℓ` has `s_L` at position `#d_a + 2`; each `αᵢ` has `s_C` there). Under T1, `ℓ < ℓ' < ℓ_meta` (across home documents by document-tumbler order, `d_a < d_b`; within `d_b` by `inc(·, 0)` chain order).

**Query 1 (basic match): `findlinks_V({v_a^2}, d_a, Σ)`.** Phase 1: `image({v_a^2}, d_a, Σ) = {α₂}`. Phase 2: at `ℓ`, slot 1's coverage `{t : α₂ ≼ t}` meets `{α₂}` in `{α₂}` (reflexivity of `≼`), so `matches(ℓ, {α₂}, Σ) = true`. At `ℓ'`, no slot's coverage meets `{α₂}` (sibling content-address mismatches; type τ-disjoint). At `ℓ_meta`, slot 1 covers `{t : ℓ ≼ t}` (subspace-disjoint from `{α₂}`), slot 2 is empty, slot 3 is τ-disjoint. Result: `{ℓ}`. This exercises F1's singleton-overlap reading (slot 1 alone witnesses; no strengthening of the intersection condition would let `ℓ` qualify against a singleton `I`) and F7(a)'s slot symmetry.

**Query 2 (F6, transclusion transparency): `findlinks_V({v_b^1}, d_b, Σ)`.** `image({v_b^1}, d_b, Σ) = {α₂}` — the same image as Query 1, because `d_b`'s transclusion of `α₂` produces the same I-address. Phase 2 is identical. Result: `{ℓ}`. The reader querying `d_b`'s view of `α₂` discovers the same link as via `d_a`'s native arrangement: identity travels with the I-address.

**Query 3 (F7, filtered conjunction): `findlinks_filtered({(1, {α₂}), (2, {α₃})}, Σ)`.** "Links from `α₂` to `α₃`". At `ℓ`: slot 1 meets `{α₂}`, slot 2 meets `{α₃}`; both constraints hold. At `ℓ'`: slot 1 covers `{t : α₃ ≼ t}`, intersected with `{α₂}` is `∅` (since `α₃ ⋠ α₂`); the slot-1 constraint fails, the universal fails, `ℓ'` excluded — even though `ℓ'`'s slot 1 *does* meet `{α₃}` (which would have satisfied a slot-1 constraint had we named the to-set under slot 1). At `ℓ_meta`: slot 1 is subspace-disjoint from `{α₂}`; the slot-1 constraint fails. Result: `{ℓ}`. Contrast with the union-form unfiltered query `findlinks({α₂} ∪ {α₃}, Σ) = {ℓ, ℓ'}` — the filtered form is strictly stricter, exercising F7(b)'s filter conjunction.

**Query 4 (cross-subspace, F12 with link-image): `findlinks_V({v_a^L}, d_a, Σ_L)`.** First, perform a K.μ⁺_L transition on `d_a` extending its arrangement with `v_a^L := [s_L, 1]` mapping to `ℓ` (the K.μ⁺_L preconditions are satisfied: `ℓ ∈ dom(Σ.L)`, `origin(ℓ) = d_a`, `ℓ ∉ ran(Σ.M(d_a))`, `v_a^L` is the canonical depth-2 minimum). Call the post-state `Σ_L`; `Σ_L.L = Σ.L` by A1a. Phase 1 at `v_a^L`: `image({v_a^L}, d_a, Σ_L) = {ℓ}` — the image is the *link address* `ℓ`, a member of `dom(Σ_L.L)`. Phase 2: at `ℓ_meta`, slot 1's coverage `{t : ℓ ≼ t}` meets `{ℓ}` in `{ℓ}` (reflexivity), so `matches(ℓ_meta, {ℓ}, Σ_L) = true`. At `ℓ` and `ℓ'`, no slot's coverage extends `ℓ` (subspace/τ-disjointness). Result: `{ℓ_meta}`. The reader selecting a V-position in the link subspace discovers the meta-link annotating `ℓ`. The match predicate is address-agnostic: it consults coverage and overlap, indifferent to whether the image's elements inhabit `dom(C)` or `dom(L)`. S3★'s cross-subspace routing of V-positions to `dom(L)` (ASN-0047) feeds naturally into F1.

**Query 5 (F9, multi-step preservation across V ∖ {K.λ}).** From `Σ`, apply a five-step sequence touching `M`, `C`, `R`, and arrangement contraction — every state component the substrate link-store-inert fragment can modify:

  (i) K.δ case (ii) at `k = 0` from `d_b` creates `d_c = inc(d_b, 0)` (K.δ-ID.zeros-0/1: `zeros(d_c) = 2`, so `IsDocument(d_c)`; K.δ effect places `d_c ∈ Σ_1.E_doc` and `Σ_1.M(d_c) = ∅`). K.δ's published frame names `L' = L` (A1a): `Σ_1.L = Σ.L`.

  (ii) K.α allocates `α_c = [d_c.0.s_C.1]` with value `v_c`. K.α's published frame (A1a): `Σ_2.L = Σ_1.L`.

  (iii) K.μ⁺ extends `Σ_2.M(d_c)` with `v_c^1 ↦ α_c`. K.μ⁺'s amended extended-state frame names `L' = L` (A1a): `Σ_3.L = Σ_2.L`.

  (iv) K.ρ records `(α_c, d_c) ∈ R`. K.ρ's published frame names `L' = L` (A1a): `Σ_4.L = Σ_3.L`.

  (v) K.μ⁻ contracts `Σ_4.M(d_a)` to `{v_a^1 ↦ α₁}`. K.μ⁻'s amended extended-state frame names `L' = L` (A1a): `Σ_5.L = Σ_4.L`.

Transitivity yields `Σ.L = Σ_5.L`. F8 forces `findlinks(I, Σ) = findlinks(I, Σ_5)` for every `I ⊆ T`. At `I = {α₂}`: `findlinks({α₂}, Σ) = {ℓ}` (Query 1) and `findlinks({α₂}, Σ_5) = {ℓ}` by direct evaluation (link values preserved by L12; the slot-1 test at `ℓ` still meets `{α₂}`). The V-side answer at `v_a^2` in `d_a` does change across the chain (the K.μ⁻ step contracts `v_a^2` out of `dom(M(d_a))`, so `findlinks_V({v_a^2}, d_a, Σ_5) = findlinks(∅, Σ_5) = ∅`); the I-side answer at the fixed I-set `{α₂}` does not. F9 holds across the chain.

**Query 6 (F11 + F9-λ, persistence and growth across K.λ).** Query 5's chain stays in V ∖ {K.λ}, so it cannot exercise F11's load-bearing case — the case where `dom(Σ.L)` grows under the persistence claim. We extend `Σ_5` with one K.λ step to surface that case explicitly. From `Σ_5`, apply K.λ allocating `ℓ_new ∈ A_L(d_c)` (the first emission of `d_c`'s link sub-allocator, since no K.λ under `d_c` has fired in the prior chain) with endsets: slot 1 `(α_c, δ(1, #α_c))`, slot 2 `∅`, slot 3 `(τ_meta, δ(1, #τ_meta))` (reusing `τ_meta` from `Σ`'s setup, persisted into `Σ_5` by L12). The freshness precondition discharges because `ℓ_new = [d_c.0.s_L.1]` and `{ℓ' ∈ dom(Σ_5.L) : origin(ℓ') = d_c} = ∅`. Call the post-state `Σ_6`. K.λ's published frame names `L'` as the only modified component; M, C, E, R are unchanged.

*I-side persistence of the `{α₂}` query (F11 across K.λ).* At `Σ_5`, `findlinks({α₂}, Σ_5) = {ℓ}`. At `Σ_6`: `ℓ ∈ dom(Σ_5.L) ⊆ dom(Σ_6.L)` with `Σ_6.L(ℓ) = Σ_5.L(ℓ)` by L12, so PerLinkInvarianceUnderValuePreservation at `ℓ` gives `matches(ℓ, {α₂}, Σ_6) = true`. For the freshly allocated `ℓ_new`: `coverage(ℓ_new.e₁) = {t : α_c ≼ t}` and `coverage(ℓ_new.e₃) = {t : τ_meta ≼ t}`, both disjoint from `{α₂}` (sibling content-address non-nesting between `α_c` and `α₂` under distinct documents `d_c ≠ d_a`; cross-document non-nesting between `τ_meta` and `α₂` by setup). So `matches(ℓ_new, {α₂}, Σ_6) = false`. By F9-λ: `findlinks({α₂}, Σ_6) = findlinks({α₂}, Σ_5) ⊎ ∅ = {ℓ}`. F11's persistence holds across the K.λ step: `ℓ` remains `{α₂}`-discoverable even as `dom(Σ.L)` grows. The load-bearing step is PerLinkInvarianceUnderValuePreservation at `ℓ` specifically.

*I-side growth for a query covering `ℓ_new` (F19 monotonicity at K.λ).* Take `I' = {α_c}`. At `Σ_5`: `α_c ∈ dom(Σ_5.C)` (allocated in Query 5 step (ii)), but no link in `dom(Σ_5.L) = {ℓ, ℓ', ℓ_meta}` mentions `α_c` in any endset coverage (each prior link's slots cover prefix-subtrees over `α₁, α₂, α₃, τ_·, ℓ`, all non-nesting with `α_c` under `d_c`). So `findlinks({α_c}, Σ_5) = ∅`. At `Σ_6`: `matches(ℓ_new, {α_c}, Σ_6) = true` (slot 1's coverage `{t : α_c ≼ t}` contains `α_c` reflexively); the prior-key links remain non-matching by PerLinkInvarianceUnderValuePreservation. By F9-λ: `findlinks({α_c}, Σ_6) = ∅ ⊎ {ℓ_new} = {ℓ_new}`. F19 monotonicity is exhibited: `findlinks({α_c}, Σ_5) = ∅ ⊆ {ℓ_new} = findlinks({α_c}, Σ_6)`. F11 and F19 compose: a query covering the freshly allocated link grows, while every prior matching link remains matched.

## Local Atomicity and the Single-State Setting

By SequentialTransitionAxiom (ASN-0093), every state transition is atomic and uninterruptible; `Σ` is well-defined at every query point. A K.λ commits `a` to `dom(Σ.L)` atomically: by the time the K.λ committing `a` returns, `a` is in `dom(Σ.L)` and the next query at any state succeeding the K.λ must include `a` if `a` matches.

## What We Have Not Specified

- The procedure by which the operation is computed.
- Behavior across multiple physical instances of the link store; partition tolerance; consistency models.
- Caching.
- Access control beyond noting it as an orthogonal scope filter.
- The inverse direction (resolving result endsets back to V-positions) — that is FOLLOWLINK/RETRIEVEENDSETS.
- The *interpretation* a reader should attach to a query with I-addresses outside `dom(Σ.C) ∪ dom(Σ.L)`. The semantics are already pinned by the comprehension — such a query returns exactly the links whose coverage meets `I`, possibly ghost-covering links (LP17, ASN-0098) — but what such a result *means* to the reader is left open.
- A combined filtered-and-scoped operation `findlinks_filtered_scoped(C, S, Σ)`.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| `image(R, d, Σ)` | I-image of a V-region with silent projection | definition |
| `findlinks(I, Σ)` | Discovery operation comprehension | definition |
| `findlinks_V(R, d, Σ)` | Two-phase composite `findlinks(image(R, d, Σ), Σ)` (operation, defined by F12) | definition |
| `findlinks_filtered(C, Σ)` | Filtered form with slot constraints | definition |
| `findlinks_scoped(I, S, Σ)` | Scoped form: `findlinks(I, Σ) ∩ S` | definition |
| ComprehensionInvariantUnderΣL | Meta-lemma: comprehensions over `dom(Σ.L)` with `Σ.L`-only predicates are invariant under `Σ.L = Σ'.L` | introduced (meta-lemma) |
| PerLinkInvarianceUnderValuePreservation | Per-link primitive: match and filtered per-link universal evaluate identically when `Σ'.L(a) = Σ.L(a)` at a specific `a` | introduced (sub-lemma) |
| A1a | PublishedFramePreservation: every atomic op of V ∖ {K.λ} — {K.α, K.δ, K.μ⁺, K.μ⁻, K.μ⁺_L, K.ρ} — preserves `Σ.L` from its published frame (K.μ⁺, K.μ⁻ via ASN-0047's amended extended-state frames, both publishing `L' = L`) | introduced (structural lemma) |
| A1 | KλUniqueLinkStoreModifier: K.λ is the unique operation of V that modifies the link store | introduced (composite lemma) |
| F1 | MatchPredicate definition | definition |
| F2 | Completeness: `findlinks(I, Σ) ⊆ result(I, Σ)` | introduced |
| F3 | Soundness: `result(I, Σ) ⊆ findlinks(I, Σ)` | introduced |
| F2-filt, F3-filt | Filtered conformance pair | introduced |
| F2-sco, F3-sco | Scoped conformance pair | introduced |
| F2-V, F3-V | V-side conformance pair (primary obligation on `result_V`) | introduced |
| F4 | MatchIndividuation: natural alternative match designs (coverage-containment either direction, cardinality threshold, I-independent slot tests) each yield an operation distinct from FINDLINKS, with realizable disagreeing witnesses | introduced |
| F5 | Identity, not value: match consults coverage, not content | introduced |
| F6 | Transclusion transparency | introduced |
| F7 | Endset symmetry (slot equality + filter conjunction) | introduced |
| F8 | Determinism: `findlinks(I, ·)` is a function of `(Σ.L, I)` | introduced |
| F9 | LinkStoreInertPreservation: findlinks invariant across every V ∖ {K.λ} transition, single-step or multi-step | introduced |
| F9-λ | KλInducedIncrement: characterises the K.λ-induced delta to findlinks(I, ·) as disjoint union with a singleton or ∅ depending on whether ℓ_new matches | introduced |
| F10 | Ordered result: canonical T1-sorted presentation | introduced |
| F10-filt, F10-sco | Filtered and scoped ordered presentations | introduced |
| F11 | PersistentDiscoverabilityI: I-side match against fixed I preserved across reachable sequences (distinct from ASN-0098's V-side discoverable_from, which is not persistent) | introduced |
| F12 | TwoPhaseFactoring: `findlinks_V(R, d, Σ) ≡ findlinks(image(R, d, Σ), Σ)` | definition |
| F13 | Set-additive in the I-input | introduced |
| F14 | Scope filter is intersection | introduced |
| F15, F16 | Filtered and scoped determinism | introduced |
| F17, F18 | Filtered and scoped survivability under K.μ-family | introduced |
| F19 | Result-set monotonicity across reachable sequences | introduced |
| F19-filt, F19-sco | Filtered and scoped monotonicity | introduced |
| F20 | Image set-additive | introduced |
| F20a | V-side additive: `findlinks_V(R₁ ∪ R₂, d, Σ) = findlinks_V(R₁, d, Σ) ∪ findlinks_V(R₂, d, Σ)` | introduced |

## Open Questions

What must an implementation maintain to make the completeness obligation auditable — is there a recoverable witness for every reachable state demonstrating that the index agrees with the link store?

Should the abstract specification require any bound on the time between K.λ commitment and the link's appearance in subsequent FINDLINKS results, or is "next query after K.λ" the only abstract handle available?

What is the minimum structural commitment any conforming substrate must make to the link-store-inert fragment of its operation vocabulary in order to support link-discovery invariance under those operations?
