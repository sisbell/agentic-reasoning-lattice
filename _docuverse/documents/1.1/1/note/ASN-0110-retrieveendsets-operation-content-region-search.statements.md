# ASN-0110 Claim Statements

*Source: ASN-0110-retrieveendsets-operation-content-region-search.md (revised 2026-06-04) — Extracted: 2026-06-08*

## Definition — Coverage

```
coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})
```

A set of I-addresses. Purely combinatorial property of the endset's span representation; consults no other state component.

## Definition — NMax

```
N_max(Σ) = max{|Σ.L(a)| : a ∈ dom(Σ.L)}        (N_max(Σ) = 0 when dom(Σ.L) = ∅)
```

The greatest arity present in the link store.

## Definition — Image

```
image(R, d, Σ) = {Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}
```

The set of I-addresses that document `d` currently maps V-region `R` to. `image(R, d, Σ) ⊆ ran(Σ.M(d))`; finite for arbitrary `R` because `dom(Σ.M(d))` is finite (S8-fin).

---

## RE-touch — ReTouch (DEFINITION, predicate)

`touches(e, I) ≡ coverage(e) ∩ I ≠ ∅`

## RE-overlap — ReOverlap (LEMMA, lemma)

`touches(e, I) ⟺ (E (s, ℓ) : (s, ℓ) ∈ e : ⟦(s, ℓ)⟧ ∩ I ≠ ∅)`. Since `I` is a finite set of addresses, a span `(s, ℓ) ∈ e` meets it iff some address of `I` lies in its half-open denotation, `(E α : α ∈ I : s ≤ α < s ⊕ ℓ)` — each membership test a pair of comparisons under the tumbler total order (T1/T2, ASN-0034). *Boundary contact is not touching:* the denotation `[s, s ⊕ ℓ)` is half-open, so an address `α = s ⊕ ℓ` sitting exactly at the span's exclusive upper bound is not covered; only `s ≤ α < s ⊕ ℓ` qualifies.

## RE-decide — ReDecide (LEMMA, lemma)

With the region a finite explicit I-set `I ∈ 𝒫_fin(T)`, the touching test is decidable and the search over the store terminates. For a single endset `e` — itself a finite span-set, `Endset = 𝒫_fin(Span)` (ASN-0043) — RE-overlap unfolds `touches(e, I)` into the finite double disjunction `(E (s, ℓ) ∈ e, α ∈ I : s ≤ α < s ⊕ ℓ)`. Each per-pair test is the half-open membership predicate `s ≤ α ∧ α < s ⊕ ℓ`, whose displaced endpoint `s ⊕ ℓ` exists by TA0 and exceeds its start by TA-strict, and whose two comparisons are settled by the intrinsic, terminating tumbler order T2 (ASN-0034). The enclosing search ranges over `dom(Σ.L)` — finite by L-fin (ASN-0093) — and within each link over finitely many slots `i ≤ |Σ.L(a)|` and finitely many spans per endset; the innermost test ranges over the finite `I`. A finite union of finite, decidable tests terminates, so `W(I, Σ)` and every `Eᵢ(I, Σ)` are computable.

## RE-rep — ReRep (LEMMA, lemma)

The result depends only on the region as a *set* `I`, not on how that finite I-set was presented — enumerated directly, resolved from a V-space vspecset at the wire (SS-RETRIEVE-ENDSETS), or produced by the V-side `image` (RE-Vside). Any two inputs denoting the same `I` give the same result, since `touches(e, ·)` is defined through the set `I` alone.

## RE-zero — ReZero (LEMMA, lemma)

When `I = ∅`, no endset touches: `coverage(e) ∩ ∅ = ∅`, so `touches(e, ∅)` is false for every `e`, whence `W(∅, Σ) = ∅` and `Eᵢ(∅, Σ) = ∅` for every `i`. The result is therefore `⟨∅, …, ∅⟩` — a tuple of `N_max(Σ)` empty slots, *not* the empty tuple. The length is fixed by the store's arities (RE-arity), independent of the region, so an empty region yields the same shape as a non-empty one with all-empty contents, and the empty tuple arises only in the degenerate `dom(Σ.L) = ∅` case where `N_max(Σ) = 0`.

## RE-witness — ReWitness (DEFINITION, function)

`W(I, Σ) = {(a, i) : a ∈ dom(Σ.L) ∧ 1 ≤ i ≤ |Σ.L(a)| ∧ touches(Σ.L(a).eᵢ, I)}`

The complete internal account of which endsets qualify — the witness set of (link, slot) pairs.

## RE-result — ReResult (DEFINITION, function)

For each role index `i ≥ 1`,
`Eᵢ(I, Σ) = {Σ.L(a).eᵢ : (a, i) ∈ W(I, Σ)}`.

`Eᵢ` is a set of endset *values* — span-set representations — and its membership is keyed on endset value, i.e. on span-set identity, *not* on coverage. The set comprehension collapses two contributions only when they are equal *as span-sets*.

## RE-arity — ReArity (DEFINITION, function)

`retrieveendsets(I, Σ) = ⟨E₁(I, Σ), …, E_{N_max(Σ)}(I, Σ)⟩`, a tuple of length `N_max(Σ)`. The length is fixed by the maximum arity among *all* links in the store — not the maximum among *touching* links, and not the maximum within the region — so it is stable under which region is queried. When `dom(Σ.L) = ∅` the tuple is empty.

## RE-role — ReRole (LEMMA, lemma)

`e ∈ Eᵢ(I, Σ) ⟺ (E a : a ∈ dom(Σ.L) ∧ i ≤ |Σ.L(a)| : Σ.L(a).eᵢ = e ∧ touches(e, I))`. The same endset *value* may appear under two different roles (one link's from-set may equal another link's to-set), but each occurrence is filed by the slot it occupies, and the families `Eᵢ` are pairwise independent.

## RE-sound — ReSound (LEMMA, lemma)

`resultᵢ(I, Σ) ⊆ Eᵢ(I, Σ)`: every returned endset touches `I`. No endset is returned which fails to touch the region at all.

## RE-complete — ReComplete (LEMMA, lemma)

`Eᵢ(I, Σ) ⊆ resultᵢ(I, Σ)`: every endset that touches `I` is returned. None is omitted. The quantity of *non*-touching endsets elsewhere in the store cannot suppress a touching one: completeness is a statement about the satisfaction set, indifferent to the size of its complement.

## RE-exact — ReExact (THEOREM, lemma)

`resultᵢ(I, Σ) = Eᵢ(I, Σ)`. Soundness and completeness together pin the result down to exactly the touching endsets, leaving an implementation no latitude in *which* endsets to report.

## RE-conform — ReConform (REMARK, lemma)

On a store holding an arity-`N` link with `N > 3` whose slot-`j` endset (`3 < j ≤ N`) touches `I`, we have `Eⱼ(I, Σ) ≠ ∅`, so any implementation emitting only the three standard slots violates RE-complete by dropping slot `j`. A fixed three-slot implementation is therefore a conforming realization of `retrieveendsets` exactly on the *non-empty* sub-class of stores whose links are all arity 3 — where L3 forces `N_max(Σ) = 3` exactly, so the three emitted slots *are* the `N_max(Σ)`-length tuple RE-arity requires, with any role of count zero reported in position as the empty set. The *empty* store is the one representable state that falls outside even this sub-class. It satisfies "all links arity 3" vacuously and is reachable — indeed it is the initial state `L₀ = ∅` — yet there RE-arity and RE-zero fix `N_max(Σ) = 0` and mandate the *empty* tuple `⟨⟩`, whereas a fixed three-slot emission yields `⟨∅, ∅, ∅⟩` of length 3. The two differ, and the empty-slot-in-position discipline does *not* close the gap: that discipline fills only positions *within* `1..N_max(Σ)`, and at `N_max(Σ) = 0` there are no positions to fill. Because L3 forces `N_max(Σ) ≥ 3` on every non-empty store, the empty store is the precise and sole point of divergence.

## RE-full — ReFull (LEMMA, lemma)

For `(a, i) ∈ W(I, Σ)`, the member of `Eᵢ(I, Σ)` contributed by `a` is the complete stored endset `Σ.L(a).eᵢ`, not the clipped span-set denoting `coverage(eᵢ) ∩ I`.

## RE-anon — ReAnon (THEOREM, lemma)

The result `retrieveendsets(I, Σ)` does not determine the set of contributing link addresses. There exist states `Σ`, `Σ'` with
`retrieveendsets(I, Σ) = retrieveendsets(I, Σ')` but `{a : (a, i) ∈ W(I, Σ) for some i} ≠ {a : (a, i) ∈ W(I, Σ') for some i}`.

*Construction.* The link store permits two distinct addresses to hold the same endset sequence (L11b non-injectivity, ASN-0043). Let `Σ` contain a single link `a₁` with value `(e, e', θ)` where `touches(e, I)`. Extend to `Σ'` by allocating a fresh `a₂ ≠ a₁` with the identical value `(e, e', θ)` — admissible by L11b and K.λ (ASN-0093). Now `E₁(I, Σ) = {e} = E₁(I, Σ')`, because the set comprehension collapses the two identical contributions; likewise for every role. So the results coincide. Yet the contributing-link sets are `{a₁}` and `{a₁, a₂}` — different, and of different cardinality. ∎

Corollary: each `|Eᵢ(I, Σ)|` lower-bounds the number of distinct links touching `I` through slot `i`; `max_i |Eᵢ(I, Σ)|` is a sound lower bound on distinct contributing links; the exact count is undetermined.

## RE-reveal — ReReveal (OBSERVATION, lemma)

From `retrieveendsets(I, Σ)` one recovers, for each role, the set of content regions the queried region is connected through — namely the coverages `{coverage(e) : e ∈ Eᵢ(I, Σ)}`. The per-link tuple grouping is *in general* dissolved by role separation. *Conditioned on the out-of-band knowledge that exactly one link touches `I`* — a fact the result itself does not carry — each role-family `Eᵢ` holds at most one endset, and the touching endsets returned across roles are all attributable to that one link. The side condition is essential and is not derivable from the output: the result is indistinguishable from a multi-link state — so the pairing is not recoverable from the result; it becomes attributable only once the contributing-link count is known, out of band, to be 1. Even granting that side condition, the recovery reaches only the *touching* slots: a slot that does not touch contributes nothing to the result and so cannot be reassembled.

## RE-immut — ReImmut (LEMMA, lemma)

Across any transition `Σ → Σ'` and for any link `a ∈ dom(Σ.L)` and slot `i`, the endset value persists unchanged:
`a ∈ dom(Σ'.L) ∧ Σ'.L(a).eᵢ = Σ.L(a).eᵢ`, hence `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` (L12, ASN-0043; LP3★, ASN-0098). The returned endsets are verbatim stored values, and they reference the same content identities forever.

## RE-surv — ReSurv (LEMMA, lemma)

Let the arrangement edit be either a single-step atomic K.μ-family transition `Σ → Σ'` (`K.μ⁺`, `K.μ⁻`, or `K.μ⁺_L`) or the two-step composite `Σ →* Σ'` for `K.μ~` (the named `K.μ⁻ + K.μ⁺` composite), each of which frames `L' = L` — single-step for the atomic operations, by composition of `L' = L` across the two constituents for `K.μ~` (A1a, ASN-0099). Then `retrieveendsets(I, Σ') = retrieveendsets(I, Σ)`.

## RE-det — ReDet (LEMMA, lemma)

`retrieveendsets(I, Σ)` is a function of `(I, Σ.L)` alone. If `Σ.L = Σ'.L` as partial functions then `retrieveendsets(I, Σ) = retrieveendsets(I, Σ')`. The test consults `dom(Σ.L)`, the per-link arities and endset values, and `coverage`; it never consults `Σ.M`, `Σ.C`, or any other component.

## RE-mono — ReMono (LEMMA, lemma)

For every reachable `Σ →* Σ'`, `Eᵢ(I, Σ) ⊆ Eᵢ(I, Σ')`.

*Proof.* For `(a, i) ∈ W(I, Σ)`: multi-step link persistence gives `a ∈ dom(Σ'.L)` with `Σ'.L(a).eᵢ = Σ.L(a).eᵢ` directly over the `Σ →* Σ'` sequence — unconditional link persistence LP13 carries the address and value across the whole reachable run, and LP3★ carries the per-slot coverage invariance `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` (both ASN-0098). Coverage is thus preserved, so `touches` holds at `Σ'` and the same endset value lies in `Eᵢ(I, Σ')`. ∎

## RE-wp — ReWp (LEMMA, lemma)

Let the next transition be a `K.λ` step allocating a link homed at `d` with value `(e₁, …, e_N)`. The `K.λ` binding precondition is:
```
pre ≡ d ∈ dom(Σ.M) ∧ (ℓ_new is produced by d's link sub-allocator A_L(d), first or subsequent emission)
      ∧ N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅
```
The sub-allocator binding *determines* the allocated address `ℓ_new`; freshness `ℓ_new ∉ dom(Σ.L) ∪ dom(Σ.C)` is a derived guarantee. For any endset value `e` and role index `j`,
```
wp(K.λ, "e ∈ Eⱼ(I, Σ')") = pre ∧ ( e ∈ Eⱼ(I, Σ)  ∨  (j ≤ N ∧ eⱼ = e ∧ touches(e, I)) ).
```

Specialising to a *newly entering* endset (`e ∉ Eⱼ(I, Σ)`):
```
wp(K.λ, "e newly in Eⱼ(I, Σ')") = pre ∧ j ≤ N ∧ eⱼ = e ∧ touches(e, I).
```

*Proof.* `K.λ` sets `Σ'.L = Σ.L ∪ {ℓ_new ↦ (e₁, …, e_N)}`. Freshness gives `dom(Σ'.L) = dom(Σ.L) ⊎ {ℓ_new}`. A witness for `e ∈ Eⱼ(I, Σ')` is a link `a ∈ dom(Σ'.L)` with `j ≤ |Σ'.L(a)|`, `Σ'.L(a).eⱼ = e`, and `touches(e, I)`. Two disjoint cases: if `a ∈ dom(Σ.L)`, value preservation (RE-immut) makes the witness condition identical at `Σ`, i.e. exactly `e ∈ Eⱼ(I, Σ)`; if `a = ℓ_new`, then `|Σ'.L(ℓ_new)| = N` and `Σ'.L(ℓ_new).eⱼ = eⱼ`, so the witness reduces to `j ≤ N ∧ eⱼ = e ∧ touches(e, I)`. The two cases are mutually exclusive by freshness, giving the disjunction. ∎

## RE-empty — ReEmpty (LEMMA, lemma)

A region with no touching endset yields `Eᵢ(I, Σ) = ∅` for every `i` — a normal, supported outcome, not an error. But emptiness is not permanent: provided `I ≠ ∅` and `dom(Σ.M) ≠ ∅`, there is a `K.λ` extension `Σ → Σ'` after which the result is non-empty.

*Construction.* Pick `t ∈ I`; the unit-depth span `(t, δ(1, #t))` has coverage `{t' : t ≼ t'} ∋ t`, so an endset `e = {(t, δ(1, #t))}` satisfies `touches(e, I)`. Allocate a link homed at any `d ∈ dom(Σ.M)` with this `e` in slot 1 and any non-empty type endset in slot 3 (K.λ, L3, ASN-0093). Then `e ∈ E₁(I, Σ')`. ∎

## RE-add — ReAdd (LEMMA, lemma)

`Eᵢ(I₁ ∪ I₂, Σ) = Eᵢ(I₁, Σ) ∪ Eᵢ(I₂, Σ)`.

*Proof.* `touches(e, I₁ ∪ I₂) ⟺ coverage(e) ∩ (I₁ ∪ I₂) ≠ ∅ ⟺ coverage(e) ∩ I₁ ≠ ∅ ∨ coverage(e) ∩ I₂ ≠ ∅`, and set-builder distributes over the disjunction. ∎

## RE-Vside — ReVside (DEFINITION, function)

For `d ∈ dom(Σ.M)`,
`retrieveendsets_V(R, d, Σ) = retrieveendsets(image(R, d, Σ), Σ)`.
For `d ∉ dom(Σ.M)` the operation is undefined — there is no silent fallback.

The finite I-set handed to the I-side query is `image(R, d, Σ) = {Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))} ⊆ ran(Σ.M(d))`; `dom(Σ.M(d))` is finite (S8-fin), so `image(R, d, Σ) ∈ 𝒫_fin(T)` unconditionally for arbitrary `R`, meeting RE-decide's precondition. V-positions of `R` not in `dom(Σ.M(d))` contribute nothing to `image(R, d, Σ)`.

## RE-translucent — ReTranslucent (LEMMA, lemma)

If documents `d₁` and `d₂` both arrange a shared I-address `α` (transclusion), and `v₁ ∈ R₁`, `v₂ ∈ R₂` with `Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂) = α`, then for every role `i`, `Eᵢ(image(R₁, d₁, Σ), Σ)` and `Eᵢ(image(R₂, d₂, Σ), Σ)` both contain `Σ.L(a).eᵢ` for every `a ∈ dom(Σ.L)` with `i ≤ |Σ.L(a)|` and `α ∈ coverage(Σ.L(a).eᵢ)`. The touching test sees only `α`'s identity, not which document phrased the query. An endset anchored through transclusion is discovered from any document sharing the content.
