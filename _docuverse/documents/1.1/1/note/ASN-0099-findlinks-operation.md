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

**Phase 2 (I→Link).** Given a set of I-addresses `I ⊆ T`, we first name the per-link relevance test, then collect every link that passes it. For `a ∈ dom(Σ.L)`, `I ⊆ T`, `Σ ∈ 𝒮`:

```
F1 (MatchPredicate):
   matches(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅).
```

The discovery operation collects exactly the matching links:

```
findlinks(I, Σ) = {a ∈ dom(Σ.L) : matches(a, I, Σ)}
```

The two phases compose into the reader-facing operation:

```
F12 (TwoPhaseFactoring) — DEFINITION of findlinks_V:
   findlinks_V(R, d, Σ)
     defined when  d ∈ dom(Σ.M)
     ≡             findlinks(image(R, d, Σ), Σ).
```

For `d ∉ dom(Σ.M)`, `findlinks_V(R, d, Σ)` is *undefined*.

## The Image Set

`R` is unconstrained beyond `R ⊆ T` — single position, contiguous V-span, or any subset. When `R` is a contiguous V-span in subspace `s_C`, ASN-0058's mapping-block decomposition gives the image as a union of I-runs, one per maximal correspondence run; the runs intersecting `R` cover `R ∩ dom(Σ.M(d))` disjointly (B1+B2, ASN-0058) — a run's full V-extent may reach outside `R` when `R` cuts it, so it is the run-intersections `V(βⱼ) ∩ R` that partition `R ∩ dom(Σ.M(d))`, not the full V-extents — but their I-extents may coincide when distinct V-positions share content (S5, ASN-0036; M13/M14, ASN-0058) — the set union absorbs any such overlap. When `v ∈ R` has `subspace(v) = s_L`, S3★ (ASN-0047) routes `Σ.M(d)(v) ∈ dom(Σ.L)` and the image picks up a link address. The match predicate accepts this without modification: endsets may reference any addresses in `T` (L4, ASN-0043), so the link subspace is admissible as a coverage target.

## The Match Predicate

F1's `matches` is the coverage-form of ASN-0098's `discoverable_from`. The existential ranges uniformly over all slots, including the type-endset and any further slots: L7 (ASN-0043) leaves directional significance to the link type, so the match imposes no from/to asymmetry of its own.

```
F4 (MatchIndividuation):
   The witnesses below individuate F1's per-endset overlap test: each
   exhibits an (a, I) pair on which an alternative match design —
   coverage-containment in either direction, a cardinality threshold,
   or an I-independent design (match-all, or a slot test that ignores
   the query) — disagrees with F1. The witnesses are L3-admissible
   states.
```

*Strengthening 1 — Containment from coverage to query (`coverage ⊆ I`).* Witness link `a`: arity 3 with slot 1 `(β, δ(1, #β))`, slot 2 `(γ, δ(1, #γ))`, slot 3 `(α, δ(1, #α))`, where β and γ are same-length siblings of `α` differing at position `#α` (so β ⋠ α, α ⋠ β, γ ⋠ α, α ⋠ γ). Query `I = {α}`. F1 admits via slot 3: `coverage(L(a).e₃) ∩ I = {α} ≠ ∅`. The link-level strengthening predicate is the slot-existential `(E i : coverage(L(a).eᵢ) ⊆ I)`; we check every slot: slot 1's coverage `{t : β ≼ t}` is non-empty (contains β) and disjoint from `{α}` (since β ⋠ α), so `coverage(e₁) ⊄ I`; slot 2 likewise; slot 3's coverage `{t : α ≼ t}` (by PrefixSpanCoverage, ASN-0043) contains `α.0 ∉ I` (any tumbler extending α belongs by T0's allowance of trailing zeros). No slot satisfies `coverage ⊆ I`; strengthening excludes `a`. Non-empty slots 1–2 are load-bearing here, unlike the minimal witnesses of Strengthenings 2/3: the `coverage ⊆ I` direction is satisfied *vacuously* by an empty slot (`coverage(∅) = ∅ ⊆ I`), which would make the strengthened design admit `a` and collapse the disagreement with F1; the sibling spans β, γ give every slot non-empty coverage that genuinely fails `⊆ I`.

*Strengthening 2 — Containment from query to coverage (`I ⊆ coverage`).* Witness: link `a` with one canonical span `(α, δ(1, #α))` at slot 3, and slots 1 and 2 empty. Query `I = {α, γ}` for any `γ ∈ T` with `α ⋠ γ` (e.g., a same-length sibling differing at position `#α`). F1 admits via slot 3: `coverage(L(a).e₃) ∩ I = {α} ≠ ∅`. The link-level strengthening predicate is the slot-existential `(E i : I ⊆ coverage(eᵢ))`; we check every slot: at slot 3, `coverage(e₃) = {t : α ≼ t}` (by PrefixSpanCoverage, ASN-0043) contains `α` reflexively but not `γ` (since `α ⋠ γ`), so `I ⊄ coverage(e₃)`; at slots 1 and 2 (empty), `coverage(∅) = ∅` cannot contain non-empty `I = {α, γ}`. Strengthening excludes `a`.

*Strengthening 3 — Cardinality threshold (`|coverage ∩ I| ≥ k` for `k > 1`).* Witness: link `a` with one canonical span `(α, δ(1, #α))` at slot 3, and slots 1 and 2 empty. Query `I = {α}`. The link-level strengthening predicate is the slot-existential `(E i : |coverage(eᵢ) ∩ I| ≥ k)` for `k > 1`; we check every slot: at slot 3, `|coverage(e₃) ∩ I| = |{t : α ≼ t} ∩ {α}| = 1 < k`; at slots 1 and 2 (empty), `|coverage(∅) ∩ I| = |∅ ∩ {α}| = 0 < k`. No slot satisfies the threshold; strengthening excludes `a`. F1 admits via slot 3's singleton overlap.

*Weakening 1 — Slot-vacuous match (`P_⊤(a, I, Σ) ≡ a ∈ dom(Σ.L)`).* Witness: any link `a ∈ dom(Σ.L)` with all `coverage(Σ.L(a).eᵢ)` disjoint from `I`. Concrete instance: `Σ.L(a)` with `(τ, δ(1, #τ))` at slot 3, `∅` at slots 1 and 2, and `I = {α}` with `τ ⋠ α` and `α ⋠ τ` (cross-document non-nesting τ). Then `coverage(Σ.L(a).e₃) ∩ I = ∅` and the other slots are coverage-empty, so F1 rejects `a`. `P_⊤` admits `a`. The weakening returns links with no overlap to the query I-set — non-conforming with F1's relevance principle (the OR-across-slots existential over the per-endset overlap test): some span in some endset must witness a non-empty intersection with the request.

*Weakening 2 — Slot-disjunctive ignoring I (`P_∃-slot(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ≠ ∅)`).* Witness: the same `(a, I)` as Weakening 1. `Σ.L(a).e₃ = {(τ, δ(1, #τ))}` is non-empty, so `coverage(Σ.L(a).e₃) ≠ ∅` and `P_∃-slot` admits `a` regardless of `I`. F1 rejects (no slot's coverage meets `I`). The weakening collapses the I-dependence of the match entirely — every link in `dom(Σ.L)` matches every query, violating the relevance principle.

## Endset Filtering

A *slot constraint* is a pair `(i, J)` with `i ∈ ℕ⁺`, `J ⊆ T`. A link satisfies the constraint iff its slot `i` exists and the coverage at that slot meets `J`. The positional accessor is undefined for `i > |Σ.L(a)|` (L6), so we fold the out-of-range case into an explicit guard. A filter constraint `(i, J)` is unsatisfiable at `a` when `i > |Σ.L(a)|` (the slot is absent) or `Σ.L(a).eᵢ = ∅` (the slot carries no spans, so `coverage(∅) = ∅` meets no `J`):

```
findlinks_filtered(C, Σ)
  = {a ∈ dom(Σ.L) : (A (i, J) ∈ C : i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)}
```

The universal `(A (i, J) ∈ C : …)` is a *conjunction* over constraints — a link must satisfy every constraint to appear — dual to F1's slot-existential, which consults all slots uniformly and admits a link on the first witness. The from-to query is `{(1, I_from), (2, I_to)}`; the three-endset query adds `(3, I_type)`; a type-only restriction is `{(3, I_type)}`. The filtered form is *not* a strict generalization: the unfiltered match is an existential over slots, the filtered match a universal over constraints. The unfiltered form is recovered as a finite union over single-slot filters:

```
findlinks(I, Σ) = ⋃_{i = 1}^{N} findlinks_filtered({(i, I)}, Σ)
   where N = max{|Σ.L(a)| : a ∈ dom(Σ.L)}  when dom(Σ.L) ≠ ∅
         N = 0                              when dom(Σ.L) = ∅  (empty union = ∅)
```

`L-fin` gives `|dom(Σ.L)| < ∞` so the max is well-defined when the link store is non-empty. The identity holds per link: fix `a ∈ dom(Σ.L)`. The single-slot filter `findlinks_filtered({(i, I)}, Σ)` carries the guard `i ≤ |Σ.L(a)|`, so `a` appears in the `i`-th union term iff `i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅`. Membership of `a` in the union over `1..N` is therefore `(E i : 1 ≤ i ≤ N : i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)`, and the guard `i ≤ |Σ.L(a)|` collapses the range `1..N` to `1..|Σ.L(a)|` (terms with `i > |Σ.L(a)|` are unsatisfiable, and `|Σ.L(a)| ≤ N` by the definition of `N` ensures none below the per-link arity is dropped). That existential is exactly F1's `matches(a, I, Σ)`, so `a` is in the union iff `a ∈ findlinks(I, Σ)`. Set extensionality over `a` closes the identity.

## Completeness

The defining obligation is *completeness*: every link in `dom(Σ.L)` satisfying the match predicate must appear in an implementation's output. Let `result : 𝒫(T) × 𝒮 → 𝒫(T)` denote a conforming implementation's output function, where `𝒮` is the Xanadu system state space (states of the form `Σ = (C, L, E, M, R)` from ASN-0036, ASN-0043, ASN-0047, ASN-0093). The signature commits the implementation to functionality (equal arguments yield equal outputs).

```
F2 (Completeness):  findlinks(I, Σ) ⊆ result(I, Σ).
F3 (Soundness):     result(I, Σ) ⊆ findlinks(I, Σ).
```

Together F2 ∧ F3 force `result(I, Σ) = findlinks(I, Σ)`. Each defined form — `findlinks_filtered`, `findlinks_scoped`, `findlinks_V` — carries the analogous F2 ∧ F3 obligation, pinning a conforming implementation of that form to its abstract specification.

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
   Any membership predicate built from these evaluates identically
   at the two states; set extensionality closes the equality.
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

## Link-Store-Inert Preservation

This ASN inhabits ASN-0047's *extended* state `Σ = (C, L, E, M, R)`. ASN-0047's ValidComposite★ fixes the *atomic* vocabulary as exactly the seven operations `V_atomic = {K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ}`; document registration is performed by K.δ (Document case). The named reordering K.μ~ is the K.μ⁻ + K.μ⁺ composite. For this ASN's preservation reasoning we range over

```
V ≡ V_atomic ∪ {K.μ~}
```

that adjoins the composite K.μ~ to ValidComposite★'s atomic vocabulary. Throughout this ASN we call an operation *link-store-inert* when it does not modify the link store `Σ.L` — that is, any operation in `V ∖ {K.λ}` (every atomic operation but K.λ, together with the composite K.μ~). We package the preservation lemma:

```
A1a (PublishedFramePreservation):
   Every operation of V ∖ {K.λ} preserves the link store across its
   transition — single-step Σ → Σ' for the atomic operations, the
   two-step composite Σ →* Σ' for K.μ~:
       dom(Σ'.L) = dom(Σ.L) ∧ (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a)).
   The atomic operations — V_atomic ∖ {K.λ} = {K.α, K.δ, K.μ⁺, K.μ⁻,
   K.μ⁺_L, K.ρ} — publish `L' = L` in their operative frame (K.μ⁺ and
   K.μ⁻ via ASN-0047's amended extended-state versions). The composite
   K.μ~ (the non-atomic K.μ⁻ + K.μ⁺ composite) preserves Σ.L by
   transitive composition of A1a at its two atomic constituents.
```

```
F9 (LinkStoreInertPreservation):
   For every transition produced by an operation in V ∖ {K.λ}, and any
   I ⊆ T:
       findlinks(I, Σ) = findlinks(I, Σ').

   A1a gives Σ.L = Σ'.L across every V ∖ {K.λ} operation. F8 via
   ComprehensionInvariantUnderΣL then forces the equality. For a
   reachable sequence Σ →* Σ' whose every atomic step lies in
   V_atomic ∖ {K.λ}, the per-step equalities chain by transitivity.
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

## Identity, Not Value

```
F5 (IdentityNotValue):
   matches(a, I, Σ) consults dom(Σ.L), Σ.L, and coverage(·), never
   Σ.C(·). For distinct α ≠ β, matches(a, {α}, Σ) and
   matches(a, {β}, Σ) are computed independently — each reducing per
   slot to the address-level membership test `α ∈ coverage(Σ.L(a).eᵢ)`
   (resp. `β ∈ coverage(Σ.L(a).eᵢ)`), an independent predicate over
   coverage sets with no reference to content values and no shared
   content lookup.
```

If two users write the same string at different I-addresses, links to one are not links to the other. Identity comes from origin (GlobalUniqueness, ASN-0034) and is preserved through every operation touching the content store (P0, ASN-0047); discovery builds on this foundation, not on content equivalence.

## Transclusion Transparency

```
F6 (TransclusionTransparency):
   For documents d₁, d₂ ∈ dom(Σ.M) and V-positions v₁ ∈ dom(Σ.M(d₁)),
   v₂ ∈ dom(Σ.M(d₂)) with Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂) = α:
       findlinks_V({v₁}, d₁, Σ) = findlinks_V({v₂}, d₂, Σ).
```

`image({v₁}, d₁, Σ) = {α} = image({v₂}, d₂, Σ)` (the silent projection survives the singleton on both sides since both V-positions are in their respective arrangement domains). By F12, both V-side queries unfold to `findlinks({α}, Σ)`, which by functional determinism is one set. The match consulted only the I-image and the link store; the document of origin vanished from the computation.

A link created against `α`'s native location is found via any document that transcludes `α`. The link belongs to its home document by L1a, but its *findability* is at the I-address.

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

## Scope

```
F14 (ScopeFilter):
   findlinks_scoped(I, S, Σ) = findlinks(I, Σ) ∩ S
                             = {a ∈ dom(Σ.L) ∩ S : matches(a, I, Σ)}
```

Natural choices for `S`: "all links in document `d`" (`{a : home(a) = d}`), "all links by user `u`", or any access-control narrowing.

Determinism, survivability, and monotonicity transfer to both the filtered and scoped forms, proved per clause below.

```
F15 (FilteredScopedTransfer):
   For both F ∈ {findlinks_filtered(C, ·), findlinks_scoped(I, S, ·)}:
   (a) Determinism:    F(Σ) = F(Σ')  whenever Σ.L = Σ'.L.
   (b) Survivability:  F(Σ) = F(Σ')  across any V ∖ {K.λ} step.
   (c) Monotonicity:   F(Σ) ⊆ F(Σ')  for every reachable Σ →* Σ'.
```

(a) Determinism: the filtered universal consults only `Σ.L` and query-data, so ComprehensionInvariantUnderΣL gives the filtered equality; the scoped form is `findlinks(I, ·) ∩ S` (F14), and F8's base equality is preserved under intersection with the fixed `S`. (b) Survivability: A1a gives `Σ.L = Σ'.L` across every V ∖ {K.λ} step (K.μ~ included), so (b) reduces to (a). (c) Monotonicity: LP13 + PerLinkInvarianceUnderValuePreservation transport the filtered per-link universal unchanged for every surviving link (as in F19), and intersection with the fixed `S` preserves the inclusion for the scoped form.

## Result Ordering

The result is a set, but the reader is shown an ordered list. We adopt T1's lexicographic order on tumbler addresses:

```
F10 (OrderedResult):
   The result set admits a unique presentation as a sequence
   ⟨a₁, a₂, ..., aₙ⟩ with aⱼ ∈ dom(Σ.L) satisfying matches(aⱼ, I, Σ),
   and a₁ < a₂ < ... < aₙ under T1.
```

Finiteness: `findlinks(I, Σ) ⊆ dom(Σ.L)` by definition (the comprehension ranges over `dom(Σ.L)`); L-fin gives `|dom(Σ.L)| < ∞`. T1 is a strict total order on `T` and so restricts to one on any subset. Every finite totally-ordered set admits a unique enumeration by finite induction; the empty result (`n = 0`) is the degenerate case, presented as the empty sequence `⟨⟩`, which is vacuously strictly increasing and trivially unique. The same finiteness + total-order argument gives `findlinks_filtered(C, Σ)` and `findlinks_scoped(I, S, Σ)` each a unique strictly T1-increasing presentation, since both are subsets of the finite, T1-ordered `dom(Σ.L)`.

## Persistent Discoverability (I-Side)

```
F11 (PersistentDiscoverabilityI):
   For any reachable state sequence Σ →* Σ' and any a ∈ dom(Σ.L) with
   matches(a, I, Σ):  a ∈ dom(Σ'.L) ∧ matches(a, I, Σ').
```

LP13 (UnconditionalLinkPersistence, ASN-0098) supplies the multi-step per-link guarantee `a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)`. PerLinkInvarianceUnderValuePreservation applied at this `a` then gives `matches(a, I, Σ) ⟺ matches(a, I, Σ')` — the witness slot found at Σ remains a witness at Σ'.

F11 is an *I-side* persistence claim against a fixed query I-set. The corresponding V-side claim — fixing `(R, d)` and quantifying across edits — is a theorem of neither F11's persistence nor F19's monotonicity below, and could not be: K.μ⁻ can shrink `ran(Σ.M(d))`, so a V-position discoverable at `Σ` may be contracted out of the arrangement at `Σ'`. The right framing for V-side discoverability under a contracting edit is therefore not a persistence theorem but a *weakest precondition*: which pre-states `Σ` guarantee that a fixed link `a` is still V-side discoverable from `d` after the edit? We answer this by composing `image` with ASN-0098's LP12a.

Fix `a ∈ dom(Σ.L)` and a document `d ∈ dom(Σ.M)`. Let `K.μ⁻[d, ℛ]` denote the contraction of `d`'s arrangement that retains the V-position set `ℛ` (ASN-0047's K.μ⁻; we write the retained domain as `ℛ` to free the symbol `R` for the query region). `ℛ` is *not* an arbitrary subset of `dom(Σ.M(d))`: ASN-0047's K.μ⁻ retains only a per-subspace canonical initial segment `ℛ = ⋃ {[S, 1, …, 1, k] : 1 ≤ k ≤ n'_S}` (the retention-count parameterization of LP12a, ASN-0098), required to preserve D-CTG★/D-MIN★. For any `ℛ` that is not such a per-subspace initial segment, `enabled(K.μ⁻[d, ℛ])` is false and no post-state exists. Throughout F21, `ℛ` ranges only over these canonical (enabled) retention domains. The post-state `Σ'` satisfies `dom(Σ'.M(d)) = ℛ` with `Σ'.M(d)(v) = Σ.M(d)(v)` for every `v ∈ ℛ`, and `Σ'.L = Σ.L` by A1a. Recall ASN-0098's `project(a, i, d, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)}`.

```
F21 (VSideContractionWP):
   For a query region R ⊆ T,
       wp(K.μ⁻[d, ℛ], a ∈ findlinks_V(R, d, ·))
         ≡ enabled(K.μ⁻[d, ℛ])
           ∧ (E i : 1 ≤ i ≤ |Σ.L(a)| : project(a, i, d, Σ) ∩ R ∩ ℛ ≠ ∅).
   where enabled(K.μ⁻[d, ℛ]) is K.μ⁻'s applicability predicate (ASN-0047).
```

Derivation. Evaluate the postcondition at `Σ'`. Since K.μ⁻ retains exactly `ℛ` and agrees with `Σ` there, the image collapses to the retained, query-restricted slice:

```
image(R, d, Σ') = {Σ'.M(d)(v) : v ∈ R ∩ dom(Σ'.M(d))} = {Σ.M(d)(v) : v ∈ R ∩ ℛ}.
```

Then, using `Σ'.L = Σ.L` (A1a) to move the match predicate's link-side data back to `Σ`:

```
a ∈ findlinks_V(R, d, Σ')
  ⟺ matches(a, image(R, d, Σ'), Σ')              -- F12 unfold
  ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ {Σ.M(d)(v) : v ∈ R ∩ ℛ} ≠ ∅)   -- F1, A1a
  ⟺ (E i : (E v ∈ R ∩ ℛ : Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)))
  ⟺ (E i : project(a, i, d, Σ) ∩ R ∩ ℛ ≠ ∅)      -- unfold project, push membership
```

Conjoining the applicability guard `enabled(K.μ⁻[d, ℛ])` (so that `Σ'` exists) yields F21.

Two specializations close the loop. *(i) Full-document query.* For `R = T`, `project(a, i, d, Σ) ⊆ dom(Σ.M(d)) ⊇ ℛ` makes `∩ T` a no-op, so the condition reduces to `(E i : project(a, i, d, Σ) ∩ ℛ ≠ ∅)` — exactly LP12a (ASN-0098), since `a ∈ findlinks_V(T, d, Σ) ⟺ discoverable_from(a, d, Σ)` (image(T, d, Σ) = ran(Σ.M(d)), and LP12 of ASN-0098 equates per-slot coverage-meets-range with `project ≠ ∅`). F21 is thus the V-side lift of LP12a through `image`. *(ii) Boundary `ℛ = ∅`.* Total clearance gives `project(a, i, d, Σ) ∩ R ∩ ∅ = ∅` for every slot, so the wp is `false` — no pre-state leaves `a` discoverable from a fully cleared document, matching LP12a's `R = ∅` boundary.

F21 fixes the single-operation contraction wp. Two further situations — a range-preserving reordering, and a contraction followed by an extension — each yield a labeled consequence with its own derivation.

The range-preserving reordering K.μ~ leaves full-document discoverability untouched.

```
F22 (ReorderingDiscoverabilityInvariance):
   For the range-preserving reordering K.μ~ on d and the full-document
   query R = T,
       wp(K.μ~[d], a ∈ findlinks_V(T, d, ·))
         ≡ enabled(K.μ~[d]) ∧ a ∈ findlinks_V(T, d, Σ).
```

Derivation. K.μ~ is the named `K.μ⁻ + K.μ⁺` composite that restores the same range. It is nondeterministic in its witnessing bijection — ASN-0047 admits any length- and subspace-preserving `π` meeting its admissibility clauses — but LP11 (ReorderingBijection, ASN-0098) gives `ran(Σ'.M(d)) = ran(Σ.M(d))` for *every* such `π`, so range invariance is independent of which `π` is chosen. A1a gives `Σ'.L = Σ.L`. For `R = T`, `image(T, d, Σ) = ran(Σ.M(d))`, so write `J := ran(Σ.M(d)) = ran(Σ'.M(d))` for the single image set shared by both states. Evaluating the postcondition at `Σ'`:

```
a ∈ findlinks_V(T, d, Σ')
  ⟺ matches(a, J, Σ')          -- F12 unfold; image(T, d, Σ') = ran(Σ'.M(d)) = J
  ⟺ matches(a, J, Σ)           -- PerLinkInvarianceUnderValuePreservation at a (Σ'.L(a) = Σ.L(a), fixed I-set J)
  ⟺ a ∈ findlinks_V(T, d, Σ)   -- F12 refold; image(T, d, Σ) = J
```

The middle step is licensed because `J` is the *same* set on both sides (range invariance), so the match's I-argument is fixed and only its link-side data moves, which PerLinkInvarianceUnderValuePreservation transports unchanged. Conjoining the applicability guard `enabled(K.μ~[d])` yields F22.

The contraction-then-extension composite is no harder to discover from than the contraction alone.

```
F23 (ContractionExtensionWPWeakening):
   Let σ = K.μ⁻[d, ℛ] ; K.μ⁺[d] be the composite that first contracts
   d's arrangement to ℛ and then extends it (K.μ⁺ adding I-addresses to
   d's range). For the postcondition Q ≡ (a ∈ findlinks_V(R, d, ·)):
       wp(K.μ⁻[d, ℛ], Q) ∧ enabled(σ)  ⟹  wp(σ, Q).
   The composite wp is therefore no stronger than F21's contraction wp:
   on the sub-domain where σ is enabled, every pre-state guaranteeing
   post-contraction discoverability also guarantees post-composite
   discoverability.
```

Derivation, in three steps.

*Step 1 — wp composition.* K.μ⁺[d] is *nondeterministic*: ASN-0047's precondition constrains the added V→I mappings (`dom(M'(d)) ⊃ dom(M(d))`, new mappings caller-selected to preserve D-CTG★/D-MIN★) but does not single one out, so one pre-state admits many post-extension successors. We therefore read `wp` in the demonic sense — `wp(S, Q)(Σ)` holds iff `S` is enabled at `Σ` and *every* successor of `Σ` under `S` satisfies `Q`. The sequential-composition law `wp(S₁ ; S₂, Q) = wp(S₁, wp(S₂, Q))` is Dijkstra's and holds for nondeterministic commands without change, so `wp(σ, Q) = wp(K.μ⁻[d, ℛ], wp(K.μ⁺[d], Q))`, with the chained applicability folded into `enabled(σ)`. (K.μ⁻[d, ℛ], parameterized by its retention domain ℛ as in F21, is deterministic; K.μ⁺[d] carries no analogous parameter and is the nondeterministic factor.)

*Step 2 — extension preserves discoverability.* Let `Σ_m` be any intermediate state (post-contraction) at which `K.μ⁺[d]` is enabled, and let `Σ_m'` be *any* post-extension successor of `Σ_m`. Every such successor satisfies LP9's structural hypotheses (E1) strict domain extension `dom(Σ_m'.M(d)) ⊃ dom(Σ_m.M(d))` and (E2) prior-domain agreement, so LP9 (ExtensionMonotonicity, ASN-0098) gives `project(a, i, d, Σ_m) ⊆ project(a, i, d, Σ_m')` for every slot `i`. Intersecting the fixed region `R` preserves the inclusion: `project(a, i, d, Σ_m) ∩ R ⊆ project(a, i, d, Σ_m') ∩ R`. Unfolding `Q` by the F21 chain (matches over `image(R, d, ·)` equals `(E i : project(a, i, d, ·) ∩ R ≠ ∅)`), a non-empty slot at `Σ_m` is a non-empty slot at `Σ_m'`, so `Q(Σ_m) ⟹ Q(Σ_m')`. Because this holds for *every* successor `Σ_m'`, the demonic reading of `wp(K.μ⁺[d], Q)` — Q at all successors — gives exactly `[Q ⟹ wp(K.μ⁺[d], Q)]` on enabled intermediate states.

*Step 3 — wp is monotone in its postcondition.* From `[Q ⟹ wp(K.μ⁺[d], Q)]` and the monotonicity rule `Q₁ ⟹ Q₂  ⊢  wp(S, Q₁) ⟹ wp(S, Q₂)` instantiated at `S = K.μ⁻[d, ℛ]`, `Q₁ = Q`, `Q₂ = wp(K.μ⁺[d], Q)`, we obtain `wp(K.μ⁻[d, ℛ], Q) ⟹ wp(K.μ⁻[d, ℛ], wp(K.μ⁺[d], Q))`. By Step 1 the right side is `wp(σ, Q)`; conjoining `enabled(σ)` discharges the chained guard. This is F23. Intuitively: a contraction can only remove discoverability, an extension can only add it back, so prefixing the contraction's wp with a subsequent extension never tightens the precondition.

```
F19 (ResultSetMonotonicity):
   findlinks(I, Σ) ⊆ findlinks(I, Σ') for every reachable Σ →* Σ'.
```

Direct from F11 + the definition of `findlinks`. Monotonicity propagates to the filtered and scoped forms as clause (c) of F15.

## The Empty Query

For `I = ∅`: every `coverage(e) ∩ ∅ = ∅`, so the slot-existential never witnesses; `findlinks(∅, Σ) = ∅`. Symmetrically `image(∅, d, Σ) = ∅`, and a V-region `R` entirely disjoint from `dom(Σ.M(d))` gives `findlinks_V(R, d, Σ) = ∅`.

When `dom(Σ.L) = ∅` (the initial state, before the first K.λ), every query produces `∅`. F2 (`findlinks(I, Σ) = ∅ ⊆ result(I, Σ)`) holds vacuously; F3 (`result(I, Σ) ⊆ findlinks(I, Σ) = ∅`) is not vacuous — it forces `result(I, Σ) = ∅`, pinning the implementation output. The ordering (F10), persistence (F11), and monotonicity (F19) claims above also hold vacuously.

For `findlinks_filtered`: the empty constraint set `C = ∅` makes the universal vacuously true at every link, so `findlinks_filtered(∅, Σ) = dom(Σ.L)`. The empty constraint target — any `(i, J) ∈ C` with `J = ∅` — makes that per-constraint conjunct false everywhere, so the filtered result is `∅`.

For `findlinks_scoped(I, ∅, Σ) = findlinks(I, Σ) ∩ ∅ = ∅` by F14.

## A Worked Example

We fix a small instance. State `Σ` has two documents in `dom(Σ.M)`:

- `d_a`: content-bearing. `A_C(d_a)` has produced `α₁ = [d_a.0.s_C.1]`, `α₂ = [d_a.0.s_C.2]`, `α₃ = [d_a.0.s_C.3]`, each with content values `v₁, v₂, v₃ ∈ Val`. Arrangement: `Σ.M(d_a) = {v_a^1 ↦ α₁, v_a^2 ↦ α₂, v_a^3 ↦ α₃}` with `v_a^k = [s_C, k]` of depth 2.
- `d_b`: transcludes `α₂, α₃` from `d_a`. Arrangement: `Σ.M(d_b) = {v_b^1 ↦ α₂, v_b^2 ↦ α₃}` with `v_b^k = [s_C, k]`. We assume `d_b = inc(d_a, 0)`, the next sibling document under the same account, so `d_a < d_b`.
- Type-tumbler addresses `τ_comment, τ_reply, τ_meta` allocated under a separate registry document `d_τ` non-nesting with `d_a` and `d_b`.
- Three links: `ℓ ∈ A_L(d_a)` with slot 1 `(α₂, δ(1, #α₂))`, slot 2 `(α₃, δ(1, #α₃))`, slot 3 `(τ_comment, δ(1, #τ_comment))`; `ℓ' ∈ A_L(d_b)` with slot 1 `(α₃, ·)`, slot 2 `(α₁, ·)`, slot 3 `(τ_reply, ·)`; `ℓ_meta = inc(ℓ', 0) ∈ A_L(d_b)` with slot 1 `(ℓ, δ(1, #ℓ))` (annotation on `ℓ`), slot 2 `∅`, slot 3 `(τ_meta, ·)`.

By PrefixSpanCoverage, each canonical span's coverage is a prefix subtree. The three subtrees over `α₁, α₂, α₃` are pairwise disjoint (siblings with disagreeing final components); the subtrees over `τ_·` are pairwise disjoint and disjoint from content addresses (cross-document non-nesting); `{t : ℓ ≼ t}` is disjoint from any `{t : αᵢ ≼ t}` by subspace separation (`ℓ` has `s_L` at position `#d_a + 2`; each `αᵢ` has `s_C` there). Under T1, `ℓ < ℓ' < ℓ_meta` (across home documents by document-tumbler order, `d_a < d_b`; within `d_b` by `inc(·, 0)` chain order).

**Query 1 (basic match): `findlinks_V({v_a^2}, d_a, Σ)`.** Phase 1: `image({v_a^2}, d_a, Σ) = {α₂}`. Phase 2: at `ℓ`, slot 1's coverage `{t : α₂ ≼ t}` meets `{α₂}` in `{α₂}` (reflexivity of `≼`), so `matches(ℓ, {α₂}, Σ) = true`. At `ℓ'`, no slot's coverage meets `{α₂}` (sibling content-address mismatches; type τ-disjoint). At `ℓ_meta`, slot 1 covers `{t : ℓ ≼ t}` (subspace-disjoint from `{α₂}`), slot 2 is empty, slot 3 is τ-disjoint. Result: `{ℓ}`. This exercises F1's singleton-overlap reading (slot 1 alone witnesses; no strengthening of the intersection condition would let `ℓ` qualify against a singleton `I`) and F1's uniform slot consultation.

**Query 2 (F6, transclusion transparency): `findlinks_V({v_b^1}, d_b, Σ)`.** `image({v_b^1}, d_b, Σ) = {α₂}` — the same image as Query 1, because `d_b`'s transclusion of `α₂` produces the same I-address. Phase 2 is identical. Result: `{ℓ}`. The reader querying `d_b`'s view of `α₂` discovers the same link as via `d_a`'s native arrangement: identity travels with the I-address.

**Query 3 (filtered conjunction): `findlinks_filtered({(1, {α₂}), (2, {α₃})}, Σ)`.** "Links from `α₂` to `α₃`". At `ℓ`: slot 1 meets `{α₂}`, slot 2 meets `{α₃}`; both constraints hold. At `ℓ'`: slot 1 covers `{t : α₃ ≼ t}`, intersected with `{α₂}` is `∅` (since `α₃ ⋠ α₂`); the slot-1 constraint fails, the universal fails, `ℓ'` excluded — even though `ℓ'`'s slot 1 *does* meet `{α₃}` (which would have satisfied a slot-1 constraint had we named the to-set under slot 1). At `ℓ_meta`: slot 1 is subspace-disjoint from `{α₂}`; the slot-1 constraint fails. Result: `{ℓ}`. Contrast with the union-form unfiltered query `findlinks({α₂} ∪ {α₃}, Σ) = {ℓ, ℓ'}` — the filtered form is strictly stricter, exercising the filtered form's constraint conjunction.

**Query 4 (cross-subspace, F12 with link-image): `findlinks_V({v_a^L}, d_a, Σ_L)`.** First, perform a K.μ⁺_L transition on `d_a` extending its arrangement with `v_a^L := [s_L, 1]` mapping to `ℓ` (the K.μ⁺_L preconditions are satisfied: `ℓ ∈ dom(Σ.L)`, `origin(ℓ) = d_a`, `ℓ ∉ ran(Σ.M(d_a))`, `v_a^L` is the canonical depth-2 minimum). Call the post-state `Σ_L`; `Σ_L.L = Σ.L` by A1a. Phase 1 at `v_a^L`: `image({v_a^L}, d_a, Σ_L) = {ℓ}` — the image is the *link address* `ℓ`, a member of `dom(Σ_L.L)`. Phase 2: at `ℓ_meta`, slot 1's coverage `{t : ℓ ≼ t}` meets `{ℓ}` in `{ℓ}` (reflexivity), so `matches(ℓ_meta, {ℓ}, Σ_L) = true`. At `ℓ` and `ℓ'`, no slot's coverage extends `ℓ` (subspace/τ-disjointness). Result: `{ℓ_meta}`. The reader selecting a V-position in the link subspace discovers the meta-link annotating `ℓ`. The match predicate is address-agnostic: it consults coverage and overlap, indifferent to whether the image's elements inhabit `dom(C)` or `dom(L)`. S3★'s cross-subspace routing of V-positions to `dom(L)` (ASN-0047) feeds naturally into F1.

**Query 5 (F9, multi-step preservation across V ∖ {K.λ}).** From `Σ`, apply a five-step sequence touching `M`, `C`, `R`, and arrangement contraction — every state component the substrate link-store-inert fragment can modify:

  (i) K.δ case (ii) at `k = 0` from `d_b` creates `d_c = inc(d_b, 0)` (K.δ-ID.zeros-0/1: `zeros(d_c) = 2`, so `IsDocument(d_c)`; K.δ effect places `d_c ∈ Σ_1.E_doc` and `Σ_1.M(d_c) = ∅`). K.δ's published frame names `L' = L` (A1a): `Σ_1.L = Σ.L`.

  (ii) K.α allocates `α_c = [d_c.0.s_C.1]` with value `v_c`. K.α's published frame (A1a): `Σ_2.L = Σ_1.L`.

  (iii) K.μ⁺ extends `Σ_2.M(d_c)` with `v_c^1 ↦ α_c`. K.μ⁺'s amended extended-state frame names `L' = L` (A1a): `Σ_3.L = Σ_2.L`.

  (iv) K.ρ records `(α_c, d_c) ∈ R`. K.ρ's published frame names `L' = L` (A1a): `Σ_4.L = Σ_3.L`.

  (v) K.μ⁻ contracts `Σ_4.M(d_a)` to `{v_a^1 ↦ α₁}`. K.μ⁻'s amended extended-state frame names `L' = L` (A1a): `Σ_5.L = Σ_4.L`.

Transitivity yields `Σ.L = Σ_5.L`. F8 forces `findlinks(I, Σ) = findlinks(I, Σ_5)` for every `I ⊆ T`. At `I = {α₂}`: `findlinks({α₂}, Σ) = {ℓ}` (Query 1) and `findlinks({α₂}, Σ_5) = {ℓ}` by direct evaluation (link values preserved by L12; the slot-1 test at `ℓ` still meets `{α₂}`). The V-side answer at `v_a^2` in `d_a` does change across the chain (the K.μ⁻ step contracts `v_a^2` out of `dom(M(d_a))`, so `findlinks_V({v_a^2}, d_a, Σ_5) = findlinks(∅, Σ_5) = ∅`); the I-side answer at the fixed I-set `{α₂}` does not. F9 holds across the chain.

**Query 6 (F11 + F9-λ, persistence and growth across K.λ).** From `Σ_5`, apply K.λ allocating `ℓ_new ∈ A_L(d_c)` (the first emission of `d_c`'s link sub-allocator, since no K.λ under `d_c` has fired in the prior chain) with endsets: slot 1 `(α_c, δ(1, #α_c))`, slot 2 `∅`, slot 3 `(τ_meta, δ(1, #τ_meta))` (reusing `τ_meta` from `Σ`'s setup, persisted into `Σ_5` by L12). The freshness precondition discharges because `ℓ_new = [d_c.0.s_L.1]` and `{ℓ' ∈ dom(Σ_5.L) : origin(ℓ') = d_c} = ∅`. Call the post-state `Σ_6`. K.λ's published frame names `L'` as the only modified component; M, C, E, R are unchanged.

*I-side persistence of the `{α₂}` query (F11 across K.λ).* At `Σ_5`, `findlinks({α₂}, Σ_5) = {ℓ}`. At `Σ_6`: `ℓ ∈ dom(Σ_5.L) ⊆ dom(Σ_6.L)` with `Σ_6.L(ℓ) = Σ_5.L(ℓ)` by L12, so PerLinkInvarianceUnderValuePreservation at `ℓ` gives `matches(ℓ, {α₂}, Σ_6) = true`. For the freshly allocated `ℓ_new`: `coverage(ℓ_new.e₁) = {t : α_c ≼ t}` and `coverage(ℓ_new.e₃) = {t : τ_meta ≼ t}`, both disjoint from `{α₂}` (sibling content-address non-nesting between `α_c` and `α₂` under distinct documents `d_c ≠ d_a`; cross-document non-nesting between `τ_meta` and `α₂` by setup). So `matches(ℓ_new, {α₂}, Σ_6) = false`. By F9-λ: `findlinks({α₂}, Σ_6) = findlinks({α₂}, Σ_5) ⊎ ∅ = {ℓ}`. F11's persistence holds across the K.λ step: `ℓ` remains `{α₂}`-discoverable even as `dom(Σ.L)` grows. The load-bearing step is PerLinkInvarianceUnderValuePreservation at `ℓ` specifically.

*I-side growth for a query covering `ℓ_new` (F19 monotonicity at K.λ).* Take `I' = {α_c}`. At `Σ_5`: `α_c ∈ dom(Σ_5.C)` (allocated in Query 5 step (ii)), but no link in `dom(Σ_5.L) = {ℓ, ℓ', ℓ_meta}` mentions `α_c` in any endset coverage (each prior link's slots cover prefix-subtrees over `α₁, α₂, α₃, τ_·, ℓ`, all non-nesting with `α_c` under `d_c`). So `findlinks({α_c}, Σ_5) = ∅`. At `Σ_6`: `matches(ℓ_new, {α_c}, Σ_6) = true` (slot 1's coverage `{t : α_c ≼ t}` contains `α_c` reflexively); the prior-key links remain non-matching by PerLinkInvarianceUnderValuePreservation. By F9-λ: `findlinks({α_c}, Σ_6) = ∅ ⊎ {ℓ_new} = {ℓ_new}`. F19 monotonicity is exhibited: `findlinks({α_c}, Σ_5) = ∅ ⊆ {ℓ_new} = findlinks({α_c}, Σ_6)`. F11 and F19 compose: a query covering the freshly allocated link grows, while every prior matching link remains matched.

## What We Have Not Specified

- The procedure by which the operation is computed.
- Behavior across multiple physical instances of the link store; partition tolerance; consistency models.
- Caching.
- Access control beyond noting it as an orthogonal scope filter.
- The inverse direction (resolving result endsets back to V-positions) — that is FOLLOWLINK/RETRIEVEENDSETS.
- The reader-facing meaning of a query over I-addresses outside `dom(Σ.C) ∪ dom(Σ.L)`.
- A combined filtered-and-scoped operation `findlinks_filtered_scoped(C, S, Σ)`.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| `image(R, d, Σ)` | I-image of a V-region with silent projection | definition |
| `findlinks(I, Σ)` | Discovery operation comprehension | definition |
| `findlinks_filtered(C, Σ)` | Filtered form with slot constraints | definition |
| `findlinks_scoped(I, S, Σ)` | Scoped form: `findlinks(I, Σ) ∩ S` | definition |
| ComprehensionInvariantUnderΣL | Meta-lemma: comprehensions over `dom(Σ.L)` with `Σ.L`-only predicates are invariant under `Σ.L = Σ'.L` | introduced (meta-lemma) |
| PerLinkInvarianceUnderValuePreservation | Per-link primitive: match and filtered per-link universal evaluate identically when `Σ'.L(a) = Σ.L(a)` at a specific `a` | introduced (sub-lemma) |
| A1a | PublishedFramePreservation: every op of V ∖ {K.λ} preserves `Σ.L` | introduced (structural lemma) |
| F1 | MatchPredicate definition | definition |
| F2 | Completeness: `findlinks(I, Σ) ⊆ result(I, Σ)` | introduced |
| F3 | Soundness: `result(I, Σ) ⊆ findlinks(I, Σ)` | introduced |
| F4 | MatchIndividuation: witnesses individuate F1's per-endset overlap test against coverage-containment (either direction), cardinality threshold, and I-independent designs (match-all, query-ignoring slot test) | introduced |
| F5 | Identity, not value: match consults coverage, not content | introduced |
| F6 | Transclusion transparency | introduced |
| F8 | Determinism: `findlinks(I, ·)` is a function of `(Σ.L, I)` | introduced |
| F9 | LinkStoreInertPreservation: findlinks invariant across every V ∖ {K.λ} transition | introduced |
| F9-λ | KλInducedIncrement: characterises the K.λ-induced delta to findlinks(I, ·) as disjoint union with a singleton or ∅ depending on whether ℓ_new matches | introduced |
| F10 | Ordered result: canonical T1-sorted presentation (filtered and scoped forms inherit the same finiteness + total-order argument) | introduced |
| F11 | PersistentDiscoverabilityI: I-side match against fixed I preserved across reachable sequences | introduced |
| F12 | TwoPhaseFactoring: `findlinks_V(R, d, Σ) ≡ findlinks(image(R, d, Σ), Σ)` | definition |
| F13 | Set-additive in the I-input | introduced |
| F14 | Scope filter is intersection | introduced |
| F15 | FilteredScopedTransfer: determinism, survivability, and monotonicity transfer to the filtered and scoped forms (predicates consult only `Σ.L`/query-data and are closed under intersection with `S`) | introduced |
| F19 | Result-set monotonicity across reachable sequences (filtered/scoped instances under F15(c)) | introduced |
| F20 | Image set-additive | introduced |
| F20a | V-side additive: `findlinks_V(R₁ ∪ R₂, d, Σ) = findlinks_V(R₁, d, Σ) ∪ findlinks_V(R₂, d, Σ)` | introduced |
| F21 | VSideContractionWP: weakest precondition for V-side discoverability of a fixed link under K.μ⁻, composing `image` with ASN-0098's LP12a | introduced |
| F22 | ReorderingDiscoverabilityInvariance: full-document V-side discoverability is invariant across the range-preserving reordering K.μ~ (via range invariance + PerLinkInvariance) | introduced |
| F23 | ContractionExtensionWPWeakening: the K.μ⁻ ; K.μ⁺ composite wp is implied by F21's contraction wp on the enabled sub-domain (via wp-composition + LP9 + wp postcondition-monotonicity) | introduced |

## Open Questions

What must an implementation maintain to make the completeness obligation auditable — is there a recoverable witness for every reachable state demonstrating that the index agrees with the link store?

Should the abstract specification require any bound on the time between K.λ commitment and the link's appearance in subsequent FINDLINKS results, or is "next query after K.λ" the only abstract handle available?
